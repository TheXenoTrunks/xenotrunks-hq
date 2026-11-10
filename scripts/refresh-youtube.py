#!/usr/bin/env python3
"""Refresh content/videos-auto.json from Xeno Trunks' public YouTube RSS feeds.

No API key or secret is needed. Run from anywhere:

    python3 scripts/refresh-youtube.py            # update the files in place
    python3 scripts/refresh-youtube.py --dry-run  # change nothing; write a report to youtube-dry-run/

What it does
- Reads the channel uploads feed (latest ~15 videos and Shorts).
- Also reads the channel's Shorts playlist feed (UUSH...) when YouTube serves it,
  so Shorts are labelled even if the main feed links them as /watch.
- If YouTube's RSS feeds are down (they returned 404 for every channel on
  10 Nov 2026), falls back to the public channel pages (/videos and /shorts tabs)
  and reads each video's public watch page for its exact title and date.
- Keeps only Xenoverse 2 mod trailers and showcases (title and, when needed,
  description). Official DLC trailers, other-game uploads and memes are dropped.
- Removes duplicates by video ID, newest first, and keeps older *mod trailers*
  that are already in the file (so older trailers do not fall off the RSS window)
  up to MAX_ITEMS.
- Thumbnails: https://i.ytimg.com/vi/<ID>/hqdefault.jpg (saved to assets/yt/<ID>.jpg).
- Links: https://www.youtube.com/shorts/<ID> for Shorts, https://www.youtube.com/watch?v=<ID> otherwise.

Used by .github/workflows/refresh-youtube.yml (manual runs only, never commits to main).
The daily schedule in that workflow stays commented out until Xeno Trunks approves it.
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

CHANNEL_ID = "UCFpwz174y2HmOdL1DUCLjCw"
TAIL = CHANNEL_ID[2:]
FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
FEED_FALLBACKS = [
    f"https://www.youtube.com/feeds/videos.xml?playlist_id=UU{TAIL}",    # all uploads
]
SHORTS_FEED = f"https://www.youtube.com/feeds/videos.xml?playlist_id=UUSH{TAIL}"
LONG_FEED = f"https://www.youtube.com/feeds/videos.xml?playlist_id=UULF{TAIL}"
MAX_ITEMS = 16
PER_TAB = 8
CHANNEL_PAGE = f"https://www.youtube.com/channel/{CHANNEL_ID}"
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": "CONSENT=YES+1",
}
ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}

# Title-only hard exclusions (official recaps, channel intro, other games).
TITLE_EXCLUDE = re.compile(
    r"(?:"
    r"\bchannel\s+trailer\b|"
    r"\bofficial\s+(?:character\s+)?teaser\b|"
    r"\bofficial\s+trailer\b|"
    r"\bfuture\s+saga\b|"
    r"\bhero\s+of\s+justice\b|"
    r"\bhero\s+vote\b|"
    r"\bconton\s+city\s+vote\b|"
    r"\bsparking!?\s*zero\b|"
    r"\bbudokai\s+tenkaichi\b|"
    r"\bdb\s*legends\b|"
    r"\bdragon\s*ball\s+legends\b|"
    r"\bthe\s+breakers\b|"
    r"\bkakarot\b|"
    r"\bdokkan\b|"
    r"\bmanga\s+motion\b|"
    r"\btheme\s+park\b|"
    r"\bjump\s+assemble\b"
    r")",
    re.I,
)
# Strong title signals that this upload itself is a Xenoverse 2 mod trailer/showcase.
# Includes the common typo "Parrellel Quest".
TITLE_INCLUDE = re.compile(
    r"(?:"
    r"\bmods?\b|"
    r"\bmodded\b|"
    r"\bx2m\b|"
    r"custom\s+transformation|"
    r"custom(?:\s+made)?\s+p[ae]r+[ae]?llel\s+quest|"
    r"custom\s+pq\b|"
    r"what[\s-]*if\s+(?:custom\s+)?(?:pq|p[ae]r+[ae]?llel\s+quest)\b|"
    r"p[ae]r+[ae]?llel\s+quest\s+trailer|"
    r"modded\s+p[ae]r+[ae]?llel\s+quest"
    r")",
    re.I,
)
DESC_INCLUDE = re.compile(
    r"(?:"
    r"new\s+modded\s+p[ae]r+[ae]?llel\s+quest|"
    r"custom(?:\s+made)?\s+p[ae]r+[ae]?llel\s+quest|"
    r"custom\s+modded\s+p[ae]r+[ae]?llel\s+quest|"
    r"modded\s+p[ae]r+[ae]?llel\s+quest|"
    r"modded\s+into\s+dragon\s*ball\s+xenoverse|"
    r"first\s+custom\s+p[ae]r+[ae]?llel\s+quest|"
    r"custom\s+fan-?made|"
    r"custom\s+dragon\s+ball\s+xenoverse\s*2\s+mod|"
    r"xenoverse\s*2\s+custom\s+transformation|"
    r"what[\s-]*if\s+(?:custom\s+)?(?:pq|p[ae]r+[ae]?llel\s+quest)|"
    r"mod:\s*custom|"
    r"mod\s+download\s+link"
    r")",
    re.I,
)
XV2_RE = re.compile(r"xenoverse\s*2|xenoverse2|\bdbxv2\b|\bxv2\b|\bx2m\b", re.I)


def site_root() -> Path:
    return Path(__file__).resolve().parents[1]


def classify_mod_trailer(title: str, description: str | None) -> str:
    """Return 'yes', 'no', or 'need_desc'.

    'need_desc' means the title is not enough; a description is required to decide.
    Official DLC trailers, other-game uploads and the channel intro are 'no'.
    """
    title = title or ""
    if TITLE_EXCLUDE.search(title):
        return "no"
    if TITLE_INCLUDE.search(title):
        # "This Goku Mod … Xenoverse 2 Custom Transformation" and
        # "Yamcha's Resolve Trailer (What-if Custom PQ)" etc.
        return "yes"
    if description is None:
        return "need_desc"
    blob = f"{title}\n{description}"
    if not XV2_RE.search(blob) and not DESC_INCLUDE.search(description):
        return "no"
    if DESC_INCLUDE.search(description):
        return "yes"
    return "no"


def public_item(item: dict) -> dict:
    return {k: v for k, v in item.items() if not k.startswith("_")}


def fetch(url: str, timeout: int = 30, browser: bool = False) -> bytes:
    headers = dict(BROWSER_HEADERS) if browser else {
        "User-Agent": "Mozilla/5.0 (compatible; XenoTrunksHQ-RSS/4.0)",
        "Accept": "application/atom+xml, application/xml, text/xml, */*",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as res:
        return res.read()


def fetch_feed(url: str) -> list[dict] | None:
    try:
        data = fetch(url)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"  feed unavailable: {url} ({exc})", file=sys.stderr)
        return None
    head = data.lstrip()[:80].lower()
    if head.startswith(b"<!doctype") or head.startswith(b"<html"):
        print(f"  feed returned HTML, not XML: {url}", file=sys.stderr)
        return None
    try:
        return parse_feed(data)
    except ET.ParseError as exc:
        print(f"  feed XML could not be parsed: {url} ({exc})", file=sys.stderr)
        return None


def make_item(vid: str, title: str, published: str, is_short: bool, description: str = "") -> dict:
    item = {
        "id": vid,
        "title": title,
        "published": published,
        "type": "short" if is_short else "video",
        "url": f"https://www.youtube.com/shorts/{vid}" if is_short else f"https://www.youtube.com/watch?v={vid}",
        "thumb": f"assets/yt/{vid}.jpg",
        "thumb_cdn": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
    }
    if description:
        item["_description"] = description
    return item


def _entry_description(entry: ET.Element) -> str:
    for path in ("media:group/media:description", "media:description", "atom:summary", "atom:content"):
        el = entry.find(path, NS)
        if el is not None and (el.text or "").strip():
            return el.text.strip()
    return ""


def parse_feed(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    items = []
    for entry in root.findall("atom:entry", NS):
        vid = (entry.findtext("yt:videoId", default="", namespaces=NS) or "").strip()
        if not ID_RE.match(vid):
            continue
        title = (entry.findtext("atom:title", default="", namespaces=NS) or "").strip()
        published = (entry.findtext("atom:published", default="", namespaces=NS) or "").strip()
        link_el = entry.find("atom:link", NS)
        href = (link_el.get("href") if link_el is not None else "") or ""
        items.append(make_item(vid, title, published, "/shorts/" in href, _entry_description(entry)))
    return items


def _initial_data(html: str) -> dict | None:
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def _ids_in(obj, out: list) -> None:
    if isinstance(obj, dict):
        vid = obj.get("videoId")
        if isinstance(vid, str) and ID_RE.match(vid):
            out.append(vid)
        for v in obj.values():
            _ids_in(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _ids_in(v, out)


def tab_ids(tab: str) -> list[str]:
    try:
        html = fetch(f"{CHANNEL_PAGE}/{tab}", browser=True).decode("utf-8", "replace")
    except Exception as exc:
        print(f"  channel page unavailable: {tab} ({exc})", file=sys.stderr)
        return []
    data = _initial_data(html)
    if not data:
        print(f"  channel page had no video data: {tab}", file=sys.stderr)
        return []
    ids: list[str] = []
    _ids_in(data, ids)
    return list(dict.fromkeys(ids))[:PER_TAB]


def watch_details(vid: str) -> tuple[str, str, str, str] | None:
    """Return (title, publish date, channel id, description) from the public watch page."""
    try:
        html = fetch(f"https://www.youtube.com/watch?v={vid}", browser=True).decode("utf-8", "replace")
    except Exception as exc:
        print(f"  watch page unavailable: {vid} ({exc})", file=sys.stderr)
        return None
    title = re.search(r'<meta name="title" content="([^"]*)"', html)
    date = re.search(r'"publishDate":"([^"]+)"', html) or re.search(r'<meta itemprop="datePublished" content="([^"]+)"', html)
    chan = re.search(r'"channelId":"(UC[A-Za-z0-9_-]{22})"', html)
    desc = re.search(r'<meta name="description" content="([^"]*)"', html)
    if not desc:
        short = re.search(r'"shortDescription":("(?:\\.|[^"\\])*")', html)
        if short:
            try:
                desc_text = json.loads(short.group(1))
            except json.JSONDecodeError:
                desc_text = ""
        else:
            desc_text = ""
    else:
        desc_text = desc.group(1)
    if not title:
        return None
    import html as _h
    return (
        _h.unescape(title.group(1)).strip(),
        (date.group(1) if date else ""),
        (chan.group(1) if chan else ""),
        _h.unescape(desc_text or "").strip(),
    )


def from_channel_pages() -> list[dict]:
    items = []
    for tab, is_short in (("videos", False), ("shorts", True)):
        for vid in tab_ids(tab):
            det = watch_details(vid)
            if not det:
                continue
            title, published, chan, desc = det
            if chan and chan != CHANNEL_ID:  # never import someone else's video
                print(f"  skipped {vid}: belongs to another channel", file=sys.stderr)
                continue
            items.append(make_item(vid, title, published, is_short, desc))
    return items


def ensure_description(item: dict) -> None:
    if item.get("_description"):
        return
    det = watch_details(item["id"])
    if not det:
        return
    title, published, chan, desc = det
    if chan and chan != CHANNEL_ID:
        item["_foreign"] = True
        return
    if desc:
        item["_description"] = desc
    if title and not item.get("title"):
        item["title"] = title
    if published and not item.get("published"):
        item["published"] = published


def decide_item(item: dict, fetch_if_needed: bool = True) -> str:
    """Return 'yes', 'no', or 'undecided' (needed a description that could not be fetched)."""
    if item.get("_foreign"):
        return "no"
    verdict = classify_mod_trailer(item.get("title") or "", item.get("_description"))
    if verdict != "need_desc" or not fetch_if_needed:
        return "undecided" if verdict == "need_desc" else verdict
    ensure_description(item)
    if item.get("_foreign"):
        return "no"
    verdict = classify_mod_trailer(item.get("title") or "", item.get("_description") if item.get("_description") is not None else None)
    if verdict == "need_desc":
        return "undecided"
    return verdict


def filter_mod_trailers(items: list[dict], *, keep_undecided: bool) -> tuple[list[dict], list[dict], list[dict]]:
    """Return (kept, dropped, undecided)."""
    kept, dropped, undecided = [], [], []
    for it in items:
        verdict = decide_item(it, fetch_if_needed=True)
        if verdict == "yes":
            kept.append(it)
        elif verdict == "undecided":
            undecided.append(it)
            if keep_undecided:
                kept.append(it)
        else:
            dropped.append(it)
    return kept, dropped, undecided


def dedupe(items: list[dict]) -> tuple[list[dict], list[str]]:
    seen, out, dups = set(), [], []
    for it in items:
        if it["id"] in seen:
            dups.append(it["id"])
            continue
        seen.add(it["id"])
        out.append(it)
    return out, dups


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Do not change site files; write a report folder instead.")
    ap.add_argument("--report-dir", default="youtube-dry-run")
    args = ap.parse_args()

    root = site_root()
    out = root / "content" / "videos-auto.json"
    old = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {"items": []}

    print("Fetching uploads feed…")
    feed_items = fetch_feed(FEED)
    used = FEED
    if not feed_items:
        for alt in FEED_FALLBACKS:
            feed_items = fetch_feed(alt)
            if feed_items:
                used = alt
                break
    shorts: list[dict] = []
    longs: list[dict] = []
    if feed_items:
        shorts = fetch_feed(SHORTS_FEED) or []
        longs = fetch_feed(LONG_FEED) or []
    else:
        print("RSS unavailable; reading the public channel pages instead…")
        feed_items = from_channel_pages()
        used = f"{CHANNEL_PAGE}/videos + /shorts (RSS fallback)"
    if not feed_items:
        print("ERROR: no YouTube source could be read. Nothing was changed.", file=sys.stderr)
        return 2

    short_ids = {i["id"] for i in shorts}
    long_ids = {i["id"] for i in longs}
    for it in feed_items:
        if it["id"] in short_ids and it["type"] != "short":
            it.update(make_item(it["id"], it["title"], it["published"], True, it.get("_description", "")))
        elif it["id"] in long_ids and it["type"] == "short":
            it.update(make_item(it["id"], it["title"], it["published"], False, it.get("_description", "")))

    feed_items, feed_dups = dedupe(feed_items)
    trailer_new, dropped_new, undecided_new = filter_mod_trailers(feed_items, keep_undecided=False)
    fresh_ids = {i["id"] for i in trailer_new}
    # Re-evaluate older stored entries so official/non-mod uploads are not kept,
    # but do not drop a previously listed trailer if its description cannot be fetched.
    kept_old = [i for i in old.get("items", []) if i.get("id") and i["id"] not in fresh_ids]
    trailer_old, dropped_old, undecided_old = filter_mod_trailers(kept_old, keep_undecided=True)
    merged, merge_dups = dedupe(trailer_new + trailer_old)
    merged.sort(key=lambda i: i.get("published") or "", reverse=True)
    merged = merged[:MAX_ITEMS]
    public_items = [public_item(i) for i in merged]

    payload = {
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "channel_id": CHANNEL_ID,
        "feed": used,
        "items": public_items,
    }
    old_ids = [i.get("id") for i in old.get("items", [])]
    new_ids = [i["id"] for i in public_items]
    dropped_ids = [i["id"] for i in dropped_new + dropped_old]
    summary = {
        "feed_used": used,
        "feed_count": len(feed_items),
        "shorts_feed_count": len(shorts),
        "long_feed_count": len(longs),
        "shorts_in_result": sum(1 for i in public_items if i["type"] == "short"),
        "duplicates_removed": feed_dups + merge_dups,
        "added": [i for i in new_ids if i not in old_ids],
        "dropped": [i for i in old_ids if i not in new_ids],
        "filtered_out": dropped_ids,
        "undecided_skipped": [i["id"] for i in undecided_new],
        "undecided_kept": [i["id"] for i in undecided_old],
        "result_count": len(public_items),
        "filter": "xenoverse-2-mod-trailers",
    }

    print(json.dumps(summary, indent=2))
    for it in public_items:
        print(f"  {it['id']}  {it['type']:5}  {it['published']}  {it['title']}")
    if dropped_ids:
        print("Filtered out (not mod trailers):")
        for it in dropped_new + dropped_old:
            print(f"  drop {it['id']}  {it.get('title')}")

    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.dry_run:
        rep = Path(args.report_dir)
        if not rep.is_absolute():
            rep = root / rep
        rep.mkdir(parents=True, exist_ok=True)
        (rep / "videos-auto.proposed.json").write_text(text, encoding="utf-8")
        (rep / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"Dry run: report written to {rep}. Site files unchanged.")
        return 0

    thumb_dir = root / "assets" / "yt"
    thumb_dir.mkdir(parents=True, exist_ok=True)
    for it in public_items:
        dest = thumb_dir / f"{it['id']}.jpg"
        if dest.exists():
            continue
        try:
            data = fetch(it["thumb_cdn"])
            if len(data) > 500:
                dest.write_bytes(data)
        except Exception as exc:  # the page falls back to the CDN thumbnail
            print(f"  thumb warning {it['id']}: {exc}", file=sys.stderr)
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {len(public_items)} videos to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

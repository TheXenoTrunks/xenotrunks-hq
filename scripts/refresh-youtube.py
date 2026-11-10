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
- Removes duplicates by video ID, newest first, and keeps older entries that are
  already in the file (so the list does not shrink) up to MAX_ITEMS.
- Thumbnails: https://i.ytimg.com/vi/<ID>/hqdefault.jpg (saved to assets/yt/<ID>.jpg).
- Links: https://www.youtube.com/shorts/<ID> for Shorts, https://www.youtube.com/watch?v=<ID> otherwise.

Used by .github/workflows/refresh-youtube.yml (manual runs only, never commits to main).
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
MAX_ITEMS = 12
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


def site_root() -> Path:
    return Path(__file__).resolve().parents[1]


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


def make_item(vid: str, title: str, published: str, is_short: bool) -> dict:
    return {
        "id": vid,
        "title": title,
        "published": published,
        "type": "short" if is_short else "video",
        "url": f"https://www.youtube.com/shorts/{vid}" if is_short else f"https://www.youtube.com/watch?v={vid}",
        "thumb": f"assets/yt/{vid}.jpg",
        "thumb_cdn": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
    }


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
        items.append(make_item(vid, title, published, "/shorts/" in href))
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


def watch_details(vid: str) -> tuple[str, str, str] | None:
    """Return (title, publish date, channel id) from the public watch page."""
    try:
        html = fetch(f"https://www.youtube.com/watch?v={vid}", browser=True).decode("utf-8", "replace")
    except Exception as exc:
        print(f"  watch page unavailable: {vid} ({exc})", file=sys.stderr)
        return None
    title = re.search(r'<meta name="title" content="([^"]*)"', html)
    date = re.search(r'"publishDate":"([^"]+)"', html) or re.search(r'<meta itemprop="datePublished" content="([^"]+)"', html)
    chan = re.search(r'"channelId":"(UC[A-Za-z0-9_-]{22})"', html)
    if not title:
        return None
    import html as _h
    return _h.unescape(title.group(1)).strip(), (date.group(1) if date else ""), (chan.group(1) if chan else "")


def from_channel_pages() -> list[dict]:
    items = []
    for tab, is_short in (("videos", False), ("shorts", True)):
        for vid in tab_ids(tab):
            det = watch_details(vid)
            if not det:
                continue
            title, published, chan = det
            if chan and chan != CHANNEL_ID:  # never import someone else's video
                print(f"  skipped {vid}: belongs to another channel", file=sys.stderr)
                continue
            items.append(make_item(vid, title, published, is_short))
    return items


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
            it.update(make_item(it["id"], it["title"], it["published"], True))
        elif it["id"] in long_ids and it["type"] == "short":
            it.update(make_item(it["id"], it["title"], it["published"], False))

    feed_items, feed_dups = dedupe(feed_items)
    fresh_ids = {i["id"] for i in feed_items}
    kept = [i for i in old.get("items", []) if i.get("id") and i["id"] not in fresh_ids]
    merged, merge_dups = dedupe(feed_items + kept)
    merged.sort(key=lambda i: i.get("published") or "", reverse=True)
    merged = merged[:MAX_ITEMS]

    payload = {
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "channel_id": CHANNEL_ID,
        "feed": used,
        "items": merged,
    }
    old_ids = [i.get("id") for i in old.get("items", [])]
    new_ids = [i["id"] for i in merged]
    summary = {
        "feed_used": used,
        "feed_count": len(feed_items),
        "shorts_feed_count": len(shorts),
        "long_feed_count": len(longs),
        "shorts_in_result": sum(1 for i in merged if i["type"] == "short"),
        "duplicates_removed": feed_dups + merge_dups,
        "added": [i for i in new_ids if i not in old_ids],
        "dropped": [i for i in old_ids if i not in new_ids],
        "result_count": len(merged),
    }

    print(json.dumps(summary, indent=2))
    for it in merged:
        print(f"  {it['id']}  {it['type']:5}  {it['published']}  {it['title']}")

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
    for it in merged:
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
    print(f"Wrote {len(merged)} videos to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

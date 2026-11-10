#!/usr/bin/env python3
"""Refresh content/videos-auto.json from Xeno Trunks' public YouTube RSS feeds.

No API key or secret is needed. Run from anywhere:

    python3 scripts/refresh-youtube.py            # update the files in place
    python3 scripts/refresh-youtube.py --dry-run  # change nothing; write a report to youtube-dry-run/

What it does
- Reads the channel uploads feed (latest ~15 videos and Shorts).
- Also reads the channel's Shorts playlist feed (UUSH...) when YouTube serves it,
  so Shorts are labelled even if the main feed links them as /watch.
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
ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def site_root() -> Path:
    return Path(__file__).resolve().parents[1]


def fetch(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; XenoTrunksHQ-RSS/4.0)",
            "Accept": "application/atom+xml, application/xml, text/xml, */*",
        },
    )
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
    if not feed_items:
        print("ERROR: no YouTube feed could be read. Nothing was changed.", file=sys.stderr)
        return 2

    shorts = fetch_feed(SHORTS_FEED) or []
    longs = fetch_feed(LONG_FEED) or []
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

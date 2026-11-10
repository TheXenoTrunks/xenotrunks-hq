#!/usr/bin/env python3
"""Rebuild content/fallback.js from the content JSON files (for file:// previews)."""
from __future__ import annotations

import json
from pathlib import Path

def main() -> None:
    root = Path(__file__).resolve().parents[1]
    content = root / "content"
    data = {}
    for name in ("settings", "news", "videos", "videos-auto", "mods", "fn", "work", "hire", "products"):
        path = content / f"{name}.json"
        data[name.replace("-", "_")] = json.loads(path.read_text(encoding="utf-8"))
    js = (
        "window.SITE_FALLBACK = "
        + json.dumps(data, ensure_ascii=False)
        + ";\n"
        + "window.NEWS_FALLBACK = window.SITE_FALLBACK.news;\n"
        + "window.YT_FALLBACK = window.SITE_FALLBACK.videos_auto;\n"
    )
    dest = content / "fallback.js"
    dest.write_text(js, encoding="utf-8")
    # keep a copy at the old path so older docs still work
    (root / "data" / "fallback.js").write_text(js, encoding="utf-8")
    print(f"Wrote {dest} ({len(js)} bytes)")

if __name__ == "__main__":
    main()

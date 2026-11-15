#!/usr/bin/env python3
"""Copy the home page's inline <style> into assets/css/base.css so quest.html shares the same look.
Run after editing styles in index.html:  python3 scripts/build-quest-css.py"""
import re
from pathlib import Path
root = Path(__file__).resolve().parents[1]
html = (root / "index.html").read_text(encoding="utf-8")
css = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
css = css.replace('url("assets/', 'url("../')
out = root / "assets" / "css" / "base.css"
out.write_text("/* Generated from index.html by scripts/build-quest-css.py. Do not edit by hand. */\n" + css.strip() + "\n", encoding="utf-8")
print(f"Wrote {out} ({out.stat().st_size} bytes)")

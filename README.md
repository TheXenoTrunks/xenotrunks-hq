# Xeno Trunks HQ — Xeno Trunks / Xeno Time Patrol (fan site)

Repo: https://github.com/TheXenoTrunks/xenotrunks-hq · Planned live URL: https://thexenotrunks.github.io/xenotrunks-hq/ · Phone guide: `UPDATING-ON-SAMSUNG.md`

Static one-page site for GitHub Pages. No build step is required to view it: open `index.html` or upload the folder as-is.

The v2 design is kept. All routine copy is in `content/` so the HTML does not need editing for news, videos, mods, Frieza’s Nightmare, the hero, or social links. See `content/README.md`.

## Editing without code

The recommended editor is [Pages CMS](https://app.pagescms.org) (free, GitHub login). Configuration is in `.pages.yml`. Full steps are in `PUBLISHING.md`. Long-term workflow (including how Xeno Bot and ChatGPT can keep adding features) is in `MAINTAINING.md`.

## News dates

Each raid or event in `content/news.json` should have `starts_at` and, if it expires, `ends_at` as ISO datetimes with a timezone, for example `2026-11-12T14:00:00+08:00`. The page, not the file’s old status field, decides **Live now** and **Upcoming**, and moves ended items into **Past events** automatically.

Do not invent live events. Link an official source on every item.

## Updating YouTube

Manual featured videos: edit `content/videos.json`.

Latest uploads: `content/videos-auto.json`, which can be refreshed with:

```bash
python3 scripts/refresh-youtube.py
python3 scripts/build-fallback.py
```

An optional GitHub Action in `.github/workflows/refresh-youtube.yml` is **manual only** (dry-run report, or a pull request into `preview`; never a commit to `main`). No API key is required.

## File:// previews

`content/fallback.js` is a snapshot of the JSON so the page still fills in when opened as a local file. After editing JSON on a computer, run `python3 scripts/build-fallback.py`. The live GitHub Pages site loads the JSON files over HTTPS, so this step is optional once the site is online.

## PayPal

`content/settings.json` → `paypal.enabled` must stay `false` until the Business account is verified. The page will not render a payment link while that flag is off.

## Credits

See `CREDITS.md` and `MISSING.md`.

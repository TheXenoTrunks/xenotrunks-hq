# Phase 4 (connect, test & launch prep), 10 Nov 2026

v3 design, artwork, content and features are unchanged. Launch-prep changes only:

- **URLs:** canonical, `og:url`, `og:image`, Twitter image, JSON-LD, `robots.txt` and `sitemap.xml` now use https://thexenotrunks.github.io/xenotrunks-hq/.
- **Past events archive:** ended raids/events now move automatically into a collapsible **Past events (N)** list under News (newest ended first). Live now / Upcoming / Announcements are unchanged.
- **Security:** the page script moved to `assets/js/site.js`, and a Content-Security-Policy meta tag allows only this site, YouTube thumbnails (i.ytimg.com) and the click-to-play youtube-nocookie player. CMS-entered links are filtered so only http(s) or site-relative URLs render (blocks `javascript:` links). A referrer policy was added.
- **PayPal:** still OFF (`paypal.enabled: false`). When it is switched on, it renders only a plain “Support Xeno Trunks on PayPal” link and only for an official `https://www.paypal.com/` or `https://paypal.me/` URL. No PayPal script ever loads. New CMS fields: `live_title`, `live_text`, `live_button_label`.
- **YouTube:** video titles now link to the correct YouTube page (`/shorts/ID` for Shorts, `/watch?v=ID` for videos); duplicates are removed by ID; thumbnails lazy-load and fall back to `i.ytimg.com/vi/ID/hqdefault.jpg` if a saved file is missing. `scripts/refresh-youtube.py` now dedupes, detects Shorts (link + UUSH Shorts playlist feed), keeps older entries, and has `--dry-run`. The workflow is manual-only with **dry-run** or **pr-to-preview** modes and never commits to `main`.
- **Mods / Frieza’s Nightmare:** optional `hidden` switch for mods and progress rows, and optional `video_url` for mods (CMS + page). No entries were added.
- **Performance:** WOFF2 fonts (about 565 KB → 200 KB, TTF kept as fallback), a 30 KB header/footer logo instead of the 200 KB original, hero image `fetchpriority=high`, Anton font preloaded.
- **file:// preview:** loads `content/fallback.js` only when opened as a local file, so there are no failed requests.
- **Docs:** `PUBLISHING.md` rewritten for the real repo, `UPDATING-ON-SAMSUNG.md` added, `.pages.yml` updated.

# What changed in v3 versus v2

The v2 design, palette, typography, custom Xeno Trunks artwork and section layout are kept. This is an upgrade of v2, not a rebuild.

- **Content is now data-driven.** Hero text and banner, buttons, social links, Patreon/PayPal, news, YouTube, workshop mods and Frieza’s Nightmare all live in `content/*.json`. The HTML renders from those files. Routine updates do not need HTML edits.
- **Pages CMS config added:** `.pages.yml` at the repo root, with collections for every content file and a media folder at `assets/uploads/`. Recommended editor: the hosted app at [app.pagescms.org](https://app.pagescms.org) (GitHub login, free). See `PUBLISHING.md` and `MAINTAINING.md`.
- **Automatic news expiry.** Every raid/event has `starts_at` and `ends_at` (ISO with timezone). The page shows **Live now** only between those times, **Upcoming** before the start, and moves the card to **Recent** after the end. Festival week chips (W1–W5) update the same way. Announcements with no end date stay under **Announcements**.
- **News re-checked on 10 Nov 2026 (Australia/Perth).** Broly Lite is still live. Festival Week 2 (Cross Versus, 9–15 Nov) is still the current Time Patrol week. Xbox raid times were corrected to the official Japanese clock (JST), not PT — see `MISSING.md` and the news card. A still-running official 10th-anniversary login bonus (ends 16 Nov 2026, 11:59 PM JST) was added from official information id1856. The official Japanese information post now lists the in-game Final Festival / Last World Tournament through 15 February 2027, 8:59 AM JST; the festival card uses that end date. The same official post states that the maximum Star Coins obtainable is about 25 times the previous tournament (previously treated as unverified because it was not on the English Bandai marketing page).
- **YouTube** is split into a manual featured list (`content/videos.json`) and an auto list (`content/videos-auto.json`). All eight current auto-list IDs were checked against YouTube oEmbed: each ID, title and thumbnail match the @Xeno_Trunks channel.
- **PayPal** is still inactive. It is now a CMS toggle (`paypal.enabled`). While that flag is off, no payment link is rendered, even if a URL is stored.
- **GitHub Action prepared but disabled:** `.github/workflows/refresh-youtube.yml` is `workflow_dispatch` only. The daily schedule is commented out. No secrets are required. It was not enabled.
- Docs added/updated: `PUBLISHING.md`, `MAINTAINING.md`, `content/README.md`, this file and `MISSING.md`.

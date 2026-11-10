# Update 2 (10 Nov 2026, preview branch)

- The YouTube section is now **Mod Trailers** and lists only Xenoverse 2 mod trailers and showcases from @Xeno_Trunks (newest first). Other uploads (official DLC trailers, Sparking Zero, Legends, memes, and the channel intro) are not shown.
- Featured entries are the Goku custom-transformation short and the Goku Day modded Parallel Quest trailer. “WHO IS FU?” was removed from featured because it is a Future Saga DLC promo, not a mod trailer.
- Video dates still show only the date (no “Australia/Perth” label).
- The manual YouTube importer (`scripts/refresh-youtube.py` and the Refresh YouTube list workflow) now filters to the same mod-trailer rule. The daily schedule stays off.

- The Community Discord card now uses the live Xeno Time Patrol Discord invite artwork (`assets/uploads/discord-invite-bg-web.jpg`, from `discord/perks/invite-bg-1920x1080.png`). The Facebook group card now uses the live dbxv2mods group cover v6.1 (`assets/uploads/fb-group-cover-v6-1-web.jpg`). Both are 1600×900 and under 300 KB.
- Xeno Trunks’ custom 7071 image was moved off the Discord card so the invite artwork can sit there. The original and `7071-web.jpg` are kept in `assets/uploads/`. Hero and workshop already use other custom Xeno Trunks shots, so 7071 is not shown on another card in this preview.

# Update 1b (10 Nov 2026, preview branch)

- The Festival, Broly Lite raid and 10th-anniversary login bonus news cards now use Xeno Time Patrol style images (theme tp_a: navy, cyan and magenta, TP logo watermark) instead of plain official Bandai stills. Official character art is kept inside our frame. Alt text and credits were updated. Image size is 1600×900 (WebP, under 250 KB).

# Update 1 (10 Nov 2026, preview branch)

- Video dates in the YouTube section now show only the date (e.g. “18 Oct 2026”), with no “Australia/Perth” label.
- News and raid cards can have an optional image (`image`, `image_alt`, `image_credit`; also in Pages CMS). On desktop the image sits on the left; on phones it sits on top. The Festival, Broly Lite raid and login bonus cards use official Bandai Namco images from the official information posts (see CREDITS.md).
- The Discord card now uses a 1600 px web copy of Xeno Trunks’ new upload (`7071-web.jpg`, 177 KB; the 2.4 MB original is kept). Alt texts were updated for the Discord card and the Frieza’s Nightmare image.
- The site keeps working when Pages CMS leaves out empty fields (PayPal URL, FN updates, trailer/download URLs, progress percent/note); this was tested.

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

## Update 3 (PREVIEW ONLY, 10 Nov 2026) — creator homepage restructure

Not live. Needs Xeno Trunks' approval before merging preview → main.

- Homepage reordered around Xeno Trunks as a creator: hero → Frieza's Nightmare (featured) → My quests (new `content/work.json`) → About → Commissions (new `content/hire.json`, enquiries only) → Patreon ranks → Mod Trailers → Community → Xenoverse 2 news (text-only, compact) → footer.
- Frieza's Nightmare now uses his own gameplay still `assets/fn-turles-slug.jpg` instead of the official trailer thumbnail; buttons for the free 1.7 trailer and download.
- Commissions: one service (Custom Parallel Quest). No prices, no booking, no payment. Status line "Enquiries only. Not yet open for bookings." Items marked [to confirm] show as a pink tag until decided.
- Patreon: rank cards copied from the 16 Oct 2026 tier copy (A$5 / A$10 / A$22). Must be re-checked against the live Patreon page before going live.
- Socials: the 8 big link tiles are gone; one compact Follow row in the footer. Hero/nav no longer push Discord first.
- News: moved to the bottom, images off (`news.json → show_images: false`).
- PayPal unchanged and still disabled.
- `.pages.yml`: new "My quests" and "Commissions" collections; About, Patreon ranks, news heading and FN buttons are editable.

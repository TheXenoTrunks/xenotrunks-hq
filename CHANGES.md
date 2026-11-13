# Update 10 (13 Nov 2026, preview branch)

Not live. Needs Xeno Trunks' approval before merging preview → main. The approved homepage layout is unchanged (news stays a secondary section). No prices, payments or release promises were added. No Perth times were added.

- **Added:** official Bandai Namco Europe news of 13 November 2026, [Festival Shop Item Lineup Update](https://en.bandainamcoent.eu/dragon-ball/news/dragon-ball-xenoverse-2-festival-shop-item-lineup-update). From Week 3 of the Final Festival, the Festival Shop expands with past items for Star Coins, rotating on a set schedule. The card uses a new Time Patrol (theme tp_a) 1600×900 WebP image. Rotation dates were read from the official lineup graphic (times in UTC). The graphic does not print the year; Week 3 starts 16 Nov 2026, and the January–March windows are 2027. Individual item names were not retyped. The shop rotation runs through Post-Final Period 3, ending 28 Mar 2027, 23:59 UTC. News card images stay on.

# Update 9 (13 Nov 2026, preview branch)

News card for the official themed World Tournament (id1854, 14–16 Nov 2026) now uses the approved English title **Dragon Ball Super Limited Tournament**, with the official Japanese name 「ドラゴンボール超限定一武道会」 as a small subtitle in the date line and on the card image. The top-5 Street Name is Exceed (「イクシード」). Times in the summary are shown in JST (from the official notice) and UTC, in line with the event-alert format; they are not shown in Perth time. The approved homepage layout is unchanged (news stays a secondary section). No prices, payments or release promises were added.

# Update 8 (12 Nov 2026, preview branch)

Not live. Needs Xeno Trunks' approval before merging preview → main. The approved homepage layout is unchanged (Frieza’s Nightmare and My quests stay first; news stays a secondary section at the bottom). No prices, payments or release promises were added.

- News was re-checked on 12 Nov 2026, Australia/Perth (UTC+8), against the official Japanese information listing and official @dbgame_official / @dragonballgames posts.
- **Still on:** Final Festival of Universes through 15 February 2027, 8:59 AM JST (7:59 AM Perth — the previous “9:59 AM Perth” conversion was corrected). Week 2, Cross Versus, is still the current Time Patrol week (9–15 November). The 10th-anniversary login bonus is still running, until 16 November 2026, 11:59 PM JST (10:59 PM Perth).
- **Ended:** the vs Broly (Full Power Super Saiyan) Lite raid (id1853). The last platform window closed at 12 November, 2:00 PM Perth. The card is kept and will sit in **Past events** automatically. The summary is now in the past tense. No newer official raid had been posted on the information listing when this was checked.
- **Added:** the 10th anniversary repost-campaign result (1,010 reposts reached; special loading screen for all Patrollers), announced 10 November 2026. Also added a short announcement that free Update #23 (the 10th-anniversary update and official trailer) has been out since 27 October 2026. FUTURE SAGA Chapter 4 and the Xenoverse 3 announcement are unchanged. The 3x EXP & Zeni boost (ended 5 November 2026, 2:59 PM UTC) was not added, because it has already ended.
- News card images are on again (`show_images: true`) so the Time Patrol raid picture and the other current news cards can show and fit the 16:9 slot on desktop and phone. Images are the existing tp_a 1600×900 WebP cards (navy, cyan and magenta), plus a new `repost-campaign-goal.webp` in the same style. Not plain official Bandai stills.

# Update 7 (10 Nov 2026, preview branch)

- Every card in **My quests** now has a picture, framed in a new **Xeno Time Patrol** card style: a cyan and magenta edge, a black-and-white grunge overlay, the TP logo in the corner, and the quest title on a coloured bar (CSS, not baked into the images). The approved homepage layout is unchanged.
- Frieza’s Nightmare 2.0 uses the pointing-pose frame from the 1.7 trailer (35.90s), file `assets/fn-frieza-trailer.jpg`, in the same frame. Alt text: “Frieza pointing, from Frieza’s Nightmare trailer.”
- Quest pictures (all 1600×900, under 250 KB) come from Xeno Trunks’ own trailers, except Couple’s Division, which uses a crop of his own 2023 poster (characters and TP logo only; official logos and legal line cropped off). Image paths are editable in Pages CMS (`content/work.json` `image` / `image_alt`).

# Update 6 (10 Nov 2026, preview branch)

- The Frieza’s Nightmare 2.0 featured card now uses a hype frame of Frieza from Xeno Trunks’ own 1.7 trailer (https://www.youtube.com/watch?v=KXJkr4EVsHo), instead of the Turles and Lord Slug still. The chosen frame is at 35.90s: Frieza pointing (picked by Xeno Trunks). File: `assets/fn-frieza-trailer.jpg` (1600×900, under 250 KB). Alt text: “Frieza in front of Namek, from Frieza’s Nightmare trailer.” The previous Turles/Slug image is kept in the repo but is no longer used on the page.

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

## Update 4 (PREVIEW ONLY, 10 Nov 2026) — functional pass (no redesign)

Not live. Needs Xeno Trunks' approval before merging preview → main. Layout and look of the approved "Rewrite the timeline" homepage are unchanged.

- **My quests:** every card now shows type, year, version, a short description taken from his own trailer descriptions/mod pages, "Needs" (game update) only where the download page states it, and existing credits. Each card has one **Free download** button (his own VGM mod pages, all HTTP 200 on 10 Nov 2026; Heroes Marvellous Show points to BBVenom's Ascended Warriors VGM page, which is the link in the trailer description) and one **Trailer** link (YouTube oEmbed OK, author Xeno Trunks). Downloads no longer point at Patreon, so no free quest sits behind Patreon wording, and the Nameless Namekian shop listing isn't linked anywhere. New CMS fields: `version`, `requirements`, `download_host`, `download_note`.
- **Work with me:** a working enquiry form (name/handle, contact method + detail, platform, idea, characters, release, deadline, budget "to discuss", rules checkbox). It validates, writes a formatted enquiry, and offers **Copy enquiry** (clipboard with a "Copied ✓" state, plus a manual-copy fallback) and **Open Discord to send it** (also copies). An **Email it instead** button appears only if `content/hire.json → form.contact_email` is filled in (empty by default). Nothing is sent from the site, there's no backend, and no price, booking or payment. 3-step "How it works".
- **Clutter:** removed the 2 disabled "coming when released" buttons on Frieza's Nightmare (now one text line, `fn.json → coming_note`), the disabled PayPal "Coming soon" button (now one text line), the duplicate "Commissions" nav link (the "Work with me" button stays) and the duplicate personal Facebook profile in the footer (`hidden: true`, can be switched back on in the CMS).
- **Phone:** section headings no longer sit under the sticky header (`scroll-margin-top`), the mobile menu also closes with Escape / tapping outside, tap targets are ≥ 44 px, small paragraph text is ≥ 16 px, form is single-column, no sideways scroll at 360 px.
- **Payments:** PayPal still `enabled: false`; no prices or booking added.

## Update 5 (PREVIEW ONLY, 10 Nov 2026) — creator business wording

Not live. Needs Xeno Trunks' approval before merging preview → main. Design unchanged; no prices added, no release dates, no payments (PayPal still `enabled: false`), no booking.

- **Released vs future quests:** My quests now says "Released quests: free to download for now", plus a line that future projects aren't promised as free releases and availability/distribution is decided per project (`work.json → download_note`, new `future_note`). Removed "Every quest I've released so far is free", "Every released quest stays a free download for everyone", "Every one is a free download", "Fan-made and free to play" and "Mods are fan-made and free to play". Frieza's Nightmare: "How 2.0 will be released is still being decided"; the default 2.0 button label is no longer "Download 2.0 free".
- **Commissions:** described as a paid service, quoted individually after reviewing scope and licensing/IP requirements. New "Why custom work takes time" note (`hire.json → time_note`). Step 2 is now "I review scope and licensing". Enquiry form option "Free public release" → "Public release, with credit to me". Still "Enquiries only. Not yet open for bookings."
- **Portfolio:** new "Past commission work" block inside Work with me (`hire.json → portfolio`). Shows title, client, what I did, year and trailer only; it never renders a download link. Only entries with `status: confirmed` show. Banana Blitz Showdown (commission for Simply Platano) is confirmed. Goku Day Pack and Corruption Crisis are `to_confirm` (hidden).
- **Quest cards:** new CMS flags `commission` (adds a Commission tag) and `show_download` (off hides the download button and Free tag). All current quests keep their downloads (`show_download: true`); only Banana Blitz has `commission: true`.
- **Patreon:** reworded as support for ongoing development. Perk wording no longer implies future public/free releases. Each perk has a `verified` flag; unverified perks are hidden publicly. Hero Society "1 small mod request a month" is `verified: false` (hidden) until checked against the live Patreon page.
- **Digital products:** new "Coming later" teaser section (`content/products.json`, toggle `enabled`) for original guides and scripting resources. No products, prices or buy buttons. Not in the nav.
- `.pages.yml`: new fields above + new "Digital products (coming later)" collection. `scripts/build-fallback.py` includes `products`.

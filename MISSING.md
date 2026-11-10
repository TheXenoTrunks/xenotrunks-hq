# Missing or unverified

## Custom-character attachments still missing

The rain/ruins sword-pose set, TP-logo OG, over-shoulder crop, square portrait, neon-ring portrait, in-game XV2 PNG and character video **still have not arrived** on the box under the requested hashes. v3 keeps the verified fallbacks from v2:

- Hero / workshop / OG: in-game close-up `cac-week2-host-closeup.jpg` (custom CaC: long lavender hair, scar and beard, purple armour, green undersuit, sword strap)
- Portrait: `avatar.jpg`

These are credited as “Xeno Trunks (custom character)”. Official DBH / generic Future Trunks art is not used as the brand character. Official XV2 Festival camaraderie art is only in the community cards.

## News notes (checked 10 Nov 2026, Australia/Perth)

- **Broly Lite (id1853) is still live.** Official PS/Switch/Steam window: 5 Nov 8:00 PM – 11 Nov 10:00 PM PT (= 6 Nov 12:00 PM – 12 Nov 2:00 PM Perth). Official Xbox window is published in JST: 6 Nov 4:00 AM – 12 Nov 6:00 AM JST (= 6 Nov 3:00 AM – 12 Nov 5:00 AM Perth). v2 had described the Xbox window as PT, which was incorrect; v3 uses the official Japanese clock. After the last platform window ends (12 Nov, 2:00 PM Perth) the card will move to Recent automatically.
- **Festival Week 2 (Cross Versus, 9–15 Nov)** is still current on the Time Patrol timetable. That week timetable is Time Patrol’s posted schedule, not a Bandai week-by-week table.
- The English Bandai marketing page still does not list a Festival end date. The official Japanese information post for the Last World Tournament (id1857) lists the main event through **15 February 2027, 8:59 AM JST**. v3 uses that official end date. If Bandai publishes a different end date in English, update `ends_at` in `content/news.json`.
- “About 25 times the previous tournament” Star Coins is now sourced to that same official Japanese information post, not the English marketing page. Wording follows the official JP text (maximum obtainable, not a generic “25× bonus”).
- Couple’s Division is still in development; no public download.
- Frieza’s Nightmare 2.0 still has no public trailer, download or percentage figures (percent fields are present but left empty so the site does not invent progress).
- PayPal Business is still not verified; `paypal.enabled` is false.
- Canonical URL, sitemap and robots now use `https://thexenotrunks.github.io/xenotrunks-hq/` (Phase 4). The site is not live until GitHub Pages is switched on.

## YouTube RSS from this build machine

The public RSS URL `https://www.youtube.com/feeds/videos.xml?channel_id=UCFpwz174y2HmOdL1DUCLjCw` returned **HTTP 404** from the build environment on 10 Nov 2026, so the live fetch could not be re-run here. The transform script was tested against a fixture built from the last successful feed (same morning) and all eight video IDs were re-checked with YouTube’s oEmbed API (titles, channel name “Xeno Trunks”, and `i.ytimg.com` thumbnails match). After publishing, run the Action once on GitHub’s runners (or `python3 scripts/refresh-youtube.py` on a normal network) to confirm the live feed.

## Pages CMS / automation not switched on

- Pages CMS is configured (`.pages.yml`) but **not installed** on a repo — that needs Xeno Trunks to sign in at app.pagescms.org and approve the GitHub App, after a repo exists.
- The YouTube GitHub Action is present but **not scheduled**. Raid PR automation and Discord bots were not set up (they would need a token later).

## Phase 4 notes (10 Nov 2026)

- **Instagram** `https://www.instagram.com/xeno_trunks_ig/` could not be verified (Instagram shows a login wall to automated checks). Xeno Trunks to confirm.
- **Facebook group** `https://www.facebook.com/groups/dbxv2mods` shows a login wall to automated checks. Xeno Trunks to confirm.
- Facebook Page `profile.php?id=61595489698900` resolves to “Xeno Time Patrol” and personal profile `profile.php?id=61566764950511` resolves to “Xeno Trunks”. The old Archive Page (61567187334380) is not used anywhere.
- GitHub Pages is **not enabled**. Pages CMS app is **not installed**. PayPal is **off**. The YouTube schedule is **off**.

## YouTube import test (10 Nov 2026)

- YouTube’s public RSS feeds returned **HTTP 404 for every channel** (also Google’s own channels) from both this machine and GitHub’s runners. The one manual GitHub run (dry-run) failed for that reason and changed nothing.
- `scripts/refresh-youtube.py` now falls back to the public channel pages (`/videos` and `/shorts`) plus each video’s public watch page. Local dry run: 12 items (8 Shorts, 4 videos), 0 duplicates, 4 new Shorts, all thumbnails and links return 200. It has **not** been re-run on GitHub yet; YouTube can show consent or bot-check pages to cloud runners, so the first GitHub run of the fallback still needs checking.
- `content/videos-auto.json` was **not** updated. Automatic publishing stays off.

# Editable content

All routine site copy lives in this folder. Edit these JSON files in [Pages CMS](https://app.pagescms.org) (recommended) or in the GitHub website/app. You should not need to edit `index.html` for news, videos, mods, Frieza’s Nightmare, hero text, or social links.

| File | What it controls |
|---|---|
| `settings.json` | Site name, hero banner/headline/buttons, ticker, social links, Patreon and PayPal (PayPal has an `enabled` flag — leave it off until the Business account is verified; only a public paypal.com / paypal.me link, never credentials) |
| `news.json` | Raids and events. Each item needs `starts_at` and (for things that expire) `ends_at` as ISO datetimes with a timezone. The page shows **Live now** or **Upcoming** from those dates and moves ended items into **Past events** automatically. Announcements can leave `ends_at` blank. |
| `videos.json` | Channel info, section title, and a manual **featured** list of Xenoverse 2 mod trailers (YouTube video IDs) |
| `videos-auto.json` | Xenoverse 2 mod trailers from the channel (optional GitHub Action filters to trailers only; you can also edit this list) |
| `mods.json` | Workshop items: title, image, description, download link, tutorial link, status |
| `fn.json` | Frieza’s Nightmare progress, optional percents, updates, trailer and download URLs (leave URLs blank until a release exists) |
| `fallback.js` | Copy of the JSON used when the page is opened as a local `file://` preview. Rebuild with `python3 scripts/build-fallback.py`. The live GitHub Pages site loads the JSON files directly, so this is optional once the site is online. |

Media uploaded through Pages CMS lands in `assets/uploads/`. Keep large mod downloads on Patreon, Google Drive or GitHub Releases — GitHub Pages has a 100 MB file limit and repos should stay well under ~1 GB.

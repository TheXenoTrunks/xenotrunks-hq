# Updating Xeno Trunks HQ from your Samsung phone

No coding needed. Use Chrome or Samsung Internet. Everything below is free.

- **Editor:** https://app.pagescms.org
- **Your website files:** https://github.com/TheXenoTrunks/xenotrunks-hq
- **Live site (after Pages is switched on):** https://thexenotrunks.github.io/xenotrunks-hq/

There are two branches (copies) of the site:

- **preview** = your workspace. Edits here are NOT live.
- **main** = the live website. Only change it by merging a pull request from preview.

---

## A. First time only: connect Pages CMS

1. Open **app.pagescms.org** and tap **Sign in with GitHub**.
2. GitHub asks you to authorise Pages CMS. Check it says **TheXenoTrunks**, then tap **Authorize**.
3. When asked to install the Pages CMS app, choose **Only select repositories** and pick **xenotrunks-hq** only. Tap **Install**.
4. You never type a password or token into the website files.

## B. Make a change (safe preview)

1. Open **app.pagescms.org** and tap **xenotrunks-hq**.
2. Tap the **branch** name at the top and choose **preview**. (Always check it says *preview* before editing.)
3. Pick what to edit from the menu:
   - **News & raids** – raids, events, announcements
   - **YouTube (featured)** / **YouTube (auto list)** – videos and Shorts
   - **Mod workshop** – mods, guides, downloads
   - **Frieza’s Nightmare** – progress, updates, trailer and download links
   - **Site settings** – homepage text and buttons, social links, Patreon, PayPal (off)
4. Make your change. To add an image, tap the image field → **Upload** → pick a photo. It is saved in `assets/uploads/`.
5. Tap **Save**. That saves to the preview branch only. The live site does not change.

### Dates for raids and events

- **Start** and **End** look like `2026-11-12T14:00:00+08:00` (date, `T`, time, then your time zone; `+08:00` is Perth, `+09:00` is Japan).
- The site shows **Live now** between start and end, **Upcoming** before, and moves the card into **Past events** by itself after the end.
- To hide something without deleting it, switch on **hidden**.

## C. Check it, then put it live

1. Open **github.com/TheXenoTrunks/xenotrunks-hq** in the browser (or the GitHub app).
2. You will see a yellow bar: **“preview had recent pushes” → Compare & pull request**. Tap it.
   - No bar? Tap **Pull requests → New pull request**, set **base: main** and **compare: preview**.
3. Tap **Files changed** to check exactly what changed.
4. Happy? Tap **Create pull request**, then **Merge pull request → Confirm merge**.
5. The live website updates in about 1–2 minutes.
6. Not happy? Go back to Pages CMS (still on preview), fix it and save again. The pull request updates by itself.

## D. Undo a mistake

**Undo something that already went live**

1. On GitHub, tap **Pull requests → Closed** and open the pull request you merged.
2. Scroll down and tap **Revert**. GitHub makes a new pull request that undoes it.
3. Tap **Merge pull request → Confirm merge**. The old version is back on the live site.

**Get back an old version of one file (e.g. a deleted news item)**

1. On GitHub open the file, e.g. `content/news.json`, and tap **History** (clock icon).
2. Tap the version from before the mistake and copy the part you need.
3. Paste it back in Pages CMS (on **preview**), save, then do section C.

Nothing is ever truly lost: every save is kept in the history.

## E. Keep the preview branch in step

After you merge, preview and main match. If preview ever gets messy, on GitHub open
**Pull requests → New pull request**, set **base: preview** and **compare: main**, and merge it to copy the live version back into preview.

## Safety rules

- Never paste passwords, PayPal details, API keys or Discord/GitHub tokens into any field. This repository is public.
- PayPal stays **off** until your Business account is verified and you have approved what supporters see.
- The YouTube auto-update only runs when you press **Run workflow** in GitHub **Actions**, and it never changes the live site by itself.

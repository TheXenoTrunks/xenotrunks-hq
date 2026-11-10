# Publishing Xeno Trunks HQ (GitHub Pages)

- Repository: https://github.com/TheXenoTrunks/xenotrunks-hq (public)
- Branches: `main` = live site once Pages is on · `preview` = workspace for edits
- Planned live URL: https://thexenotrunks.github.io/xenotrunks-hq/ (canonical, sitemap, robots and OG tags already use it)

Do not buy a domain, turn on PayPal or enable scheduled automation without Xeno Trunks’ approval.

## 1. Turn on GitHub Pages (only after Xeno Trunks approves the final review)

1. Repo **Settings → Pages**.
2. **Source:** Deploy from a branch. **Branch:** `main`, folder **/ (root)**. Save.
3. After 1–2 minutes the site is live at https://thexenotrunks.github.io/xenotrunks-hq/.
4. Tick **Enforce HTTPS** if it is not already ticked (github.io sites get HTTPS automatically).

Every merge into `main` republishes automatically in about a minute. `preview` is never published.

## 2. Connect Pages CMS (no-code editor)

1. Go to https://app.pagescms.org and **Sign in with GitHub**.
2. Install the Pages CMS GitHub App with **Only select repositories → xenotrunks-hq** (not “All repositories”).
3. Open **xenotrunks-hq**, switch the branch to **preview**, and edit.
4. Phone steps, pull requests and undo: see `UPDATING-ON-SAMSUNG.md`.

You are granting a third-party GitHub App read/write access to this one repository. No keys or passwords are stored in the site. You can remove it any time in GitHub **Settings → Applications → Installed GitHub Apps**.

## 3. Preview-and-approval workflow

1. Edit and save on `preview` (Pages CMS or GitHub).
2. Open a pull request **preview → main** and check **Files changed**.
3. Merge to go live. Undo with the **Revert** button on the merged pull request.

GitHub Pages only serves one branch, so `preview` is reviewed as a diff in the pull request (or locally), not as a second public website. Do not switch the Pages branch to `preview`; that would replace the live site.

## 4. YouTube list refresh (manual only)

**Actions → Refresh YouTube list → Run workflow**:

- `dry-run` (default): changes nothing and uploads a report (`youtube-dry-run` artifact) with the proposed list and a diff.
- `pr-to-preview`: commits the new list on a `youtube-refresh/<run>` branch and opens a pull request into `preview`. It never touches `main`. If GitHub’s “Allow GitHub Actions to create pull requests” setting is off (the default), the run prints a link to open the PR yourself.

The daily schedule is commented out until approved.

## 5. Optional later: custom domain

Only after approval: **Settings → Pages → Custom domain**, add the DNS records GitHub shows, wait for HTTPS, then update the canonical URL in `content/settings.json`, `index.html`, `robots.txt` and `sitemap.xml`.

## 6. Limits worth knowing

- GitHub Pages: 100 MB per file; keep the repo well under ~1 GB. Host big mod downloads on Patreon, Google Drive or GitHub Releases and only paste the link in `content/mods.json`.
- There is no `/admin` page and none should be added. Decap CMS was not used because it needs a separate login server.

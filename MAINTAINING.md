# Can Xeno Bot and ChatGPT keep improving the site?

Yes. Once Xeno Trunks HQ is on GitHub, nobody needs to rebuild the website from scratch to add news, change a banner, or ship a new feature. Everything lives in the GitHub repository, and Git keeps a full history. Any change can be reverted.

## Day-to-day content (Xeno Trunks, on a phone or computer)

Use Pages CMS (see `PUBLISHING.md`) or edit the JSON files in `content/`. Typical jobs:

- add, edit, expire or hide a raid (set `starts_at` / `ends_at`, or `hidden`)
- feature a YouTube video or Short
- upload a mod image and paste a download or tutorial link
- update Frieza’s Nightmare progress, and fill `trailer_url` / `download_url` only when a release exists
- change hero text, the banner image, social links, or the Patreon button
- leave PayPal `enabled` off until the Business account is verified

Save on the `preview` branch, then merge a pull request into `main`; once Pages is on, the live site updates in about a minute (see `UPDATING-ON-SAMSUNG.md`).

## Feature work (Xeno Bot)

Xeno Bot can keep editing the HTML, CSS, scripts and CMS config **on a branch**, then open a **pull request** for Xeno Trunks to approve. Nothing is overwritten in the dark, and merging a PR does not throw away earlier work.

For that to happen from this computer, Xeno Trunks would need to:

1. Approve giving the GitHub CLI (`gh`) access to the website repository (a GitHub login / device code he confirms).
2. Approve each pull request (or say in chat that a specific PR can be merged).

Xeno Bot will not create the repo, change Pages settings, or merge to `main` without that approval.

## Feature work (ChatGPT)

ChatGPT can:

- propose code for Xeno Trunks to paste or upload, or
- use its own GitHub connector, if he connects it to the same repo,

again through a branch and pull request whenever possible. Treat ChatGPT edits like any other contribution: review the diff, then merge.

## What is never stored in the repo

Passwords, PayPal secrets, Discord bot tokens and GitHub tokens must not be committed. Automation that needs a token later would use a GitHub Actions **secret**, and would stay off until approved.

## If something goes wrong

GitHub → the repository → **History** (or `git log`) shows every commit. You can restore a previous version of a file or revert a whole commit. Pages CMS changes are ordinary commits, so they revert the same way.

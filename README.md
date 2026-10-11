# Weekly Business Review

One static page for the weekly business review call: scorecard, pacing against plan, tasks, issues board, hires, inventory, customer service, creative, run of show and definitions.

Vercel serves `public/` as-is. There is no build step on Vercel.

## What is in this repository

| Path | What it is |
|---|---|
| `src/weekly-business-review.html` | The page source: styles, markup and script in one file, written in the Claude artifact format (no `<html>`, `<head>` or `<body>`). Edit this file. |
| `src/standalone-shim.js` | The data layer used outside Claude. It reads one JSON snapshot and serves it read-only. |
| `scripts/build_page.py` | Wraps the source in a normal HTML document, adds the shim, and writes `public/index.html`. |
| `scripts/build_snapshot.py` | Turns an export of the page database into `public/data/db.json`. |
| `public/index.html` | The built page. Commit it after every build; this is what Vercel serves. |
| `public/data/db.json` | The data snapshot the page displays. |
| `docs/data-model.md` | The collections and documents the page reads. |

**This repository is public and the snapshot is committed to it by choice.** `public/data/db.json` holds revenue, the cash plan, supplier payments and per-person numbers, and anyone can read it here and at the Vercel URL.

## Deploy on Vercel (one time)

1. Vercel → **Add New → Project → Import** this repository.
2. Framework Preset: **Other**. Leave Build Command empty. The output directory (`public`) comes from `vercel.json`.
3. Optional: **Settings → Deployment Protection** limits who can open the site. It does not hide the file in this repository.

Every push to `main` redeploys.

## Data

The page reads `public/data/db.json` at run time and shows the date of that snapshot in a banner at the top. To replace it with a newer export of the page database (one folder per collection, one JSON file per document):

```bash
python3 scripts/build_snapshot.py path/to/export 2026-10-11
git add public/data/db.json && git commit -m "Refresh data" && git push
```

Every push redeploys the site with the new numbers. Git keeps every earlier snapshot in the history.

To stop publishing the data, make the repository private (GitHub → Settings → Change visibility). Anything already pushed while it was public may have been copied.

## Read-only by design

On Vercel the page is a read-only copy. Tasks, targets, owner notes, stock counts and cash balances are edited on the Claude page, where they save to its shared database, and reach this copy with the next snapshot.

## Changing the page

```bash
# edit src/weekly-business-review.html, then
python3 scripts/build_page.py
git add -A && git commit -m "Describe the change" && git push
```

The same source file is what gets published as the Claude page, so the two stay identical. To preview locally:

```bash
python3 -m http.server 8000 --directory public
```

## Weeks

Every tab uses ISO calendar weeks, Monday to Sunday, labelled by week number (W40, W41).

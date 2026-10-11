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
| `docs/data-model.md` | The collections and documents the page reads. |

**No business data is in this repository.** The page reads `public/data/db.json` at run time, and that file is git-ignored.

## Deploy on Vercel (one time)

1. Vercel → **Add New → Project → Import** this repository.
2. Framework Preset: **Other**. Leave Build Command empty. The output directory (`public`) comes from `vercel.json`.
3. Turn on **Settings → Deployment Protection** before any data is added. The page shows revenue, cash and people's numbers.

Every push to `main` redeploys.

## Data

Without `public/data/db.json` the deployed page loads and says that no data file was found.

The snapshot holds revenue, cash, supplier payments and per-person numbers, so it must not be committed while this repository is public. Two ways to give the site its data:

- **Make the repository private**, remove the `public/data/*.json` line from `.gitignore`, and commit the snapshot. Each new export then redeploys the site.
- **Keep the repository public** and store the data somewhere private that the page can read after sign-in. That needs a small API and a login in front of it, which this version does not have.

To build a snapshot from an export of the page database (one folder per collection, one JSON file per document):

```bash
python3 scripts/build_snapshot.py path/to/export 2026-10-11
```

## Read-only by design

On Vercel the page is a read-only copy. Tasks, targets, owner notes, stock counts and cash balances are edited on the Claude page, where they save to its shared database. A banner at the top of the Vercel page shows the date of the snapshot it is displaying.

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

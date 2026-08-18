---
name: theme-dashboard
description: Rebuild and publish the ArxivWiki knowledge dashboard — a concept/tag frequency view over knowledge-extraction's kept ("Essential") papers. Use this skill when the user asks to update the theme dashboard, publish the knowledge dashboard, show dominant concepts or themes, or refresh the wiki's visual summary. Never judges a paper — it only counts and renders tags/concepts knowledge-extraction already assigned. Trigger on phrases like "update the dashboard", "publish the theme dashboard", "what are the dominant themes", "refresh the knowledge dashboard".
---

# Theme Dashboard

## Purpose

Give a single-glance view of what the ArxivWiki's durable knowledge (papers where [[knowledge-extraction]] set `keep: true`) is actually about — which concepts and tags recur, and which papers they trace back to. This is a read-only aggregation over knowledge-extraction's output, not a new judgment: it never scores, tags, or evaluates a paper itself.

## What it reads

- `../../papers/metadata/extractions/*.yaml` — filtered to records where `keep: true`. Each contributes its `tags` and `wiki_concepts_to_link` lists (see [[knowledge-extraction]]'s Section G).
- `../../papers/metadata/<arxiv_id>.json` — for title, `headline`, and `published` (to link back to the wiki page and to sort).

Papers that were extracted but not kept (`keep: false`, `status: "evaluated"`) are intentionally excluded — this dashboard is about durable knowledge, not everything that was read.

## What it writes

```bash
python skills/theme-dashboard/scripts/build_dashboard.py
```

Writes `../../ArxivWiki/dashboard.html` — a self-contained HTML **fragment** (deliberately no `<!DOCTYPE>`/`<html>`/`<head>`/`<body>`, so it can be handed to the Artifact tool without double-wrapping; it still renders acceptably if opened directly as a file). Contains two frequency clouds (concepts, tags — chip size and color scale with how many papers use them) and a table of the source papers with links back into `ArxivWiki/papers/`. Logs to `logs/build_dashboard-<timestamp>.log`, same convention as the other backend scripts.

The script is purely mechanical — it never needs an LLM in the loop to *run*, but publishing it does (see below), so it can't complete unattended any more than triage or extraction can.

## Publishing

After running the script, publish `ArxivWiki/dashboard.html` with the Artifact tool so there's a live, shareable link, not just a repo file:

1. Check whether `ArxivWiki/.dashboard-artifact.json` exists and has a `url` field.
2. If it does, call Artifact with `file_path: ArxivWiki/dashboard.html` and `url: <that url>` so the redeploy updates the *same* link instead of minting a new one. Pass `favicon: "🏷️"` (keep this stable across redeploys — only change it on a hard pivot, not a routine refresh) and a `title`/`description`.
3. If no state file exists yet (first-ever publish), call Artifact without `url`, then write the returned URL into `ArxivWiki/.dashboard-artifact.json` as `{"url": "...", "last_published": "<timestamp>"}` so future runs can find it.

This state file is bookkeeping, not wiki content — don't list it in `index.md` or treat it as a paper record.

## Process

1. Run `build_dashboard.py`.
2. Publish per the steps above.
3. Report a short summary: how many concepts/tags, the top 3-5 by frequency, and the artifact link.

## What this skill does not do

No scoring, no tagging, no summarizing a paper — that's [[knowledge-extraction]]'s job. This skill only aggregates and visualizes what extraction already decided.

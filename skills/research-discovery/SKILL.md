---
name: research-discovery
description: Discover newly published arXiv papers relevant to enterprise AI, and download PDFs only for the top-scoring papers each week. Use this skill when the user asks to check for new papers, run the research pipeline, discover this week's arXiv papers, refresh the paper queue, or download PDFs for the top papers. Retrieval only — it never judges paper quality, that is editorial-triage's job. Trigger on phrases like "check arXiv", "find new papers", "run discovery", "what's new this week", "download the top papers", "pull the latest research".
---

# Research Discovery

## Purpose

Continuously discover newly published arXiv papers that may be relevant to enterprise AI. This skill is responsible only for retrieval. It never attempts to judge quality — that is [[editorial-triage]].

## Two phases

Discovery is split into two scripts because PDF download is now gated by score, not automatic:

1. **`fetch.py`** — query arXiv, dedupe, write metadata only (title, abstract, authors, dates, categories). No PDF. Hands off to [[editorial-triage]].
2. **`download_top.py`** — runs *after* triage has scored the queue. Downloads PDFs only for the highest-scoring papers, capped at `download_top_n` (default 5) per week. Everyone below the cap stays undownloaded but not forgotten — they roll over and re-compete by score on the next run.

This ordering matters: **fetch, then triage, then download_top** — not fetch-and-download-everything. Running `download_top.py` before triage has scored anything will find zero eligible candidates (nothing has an `overall_score` yet).

## Phase 1: fetch.py

```bash
python skills/research-discovery/scripts/fetch.py
```

Useful overrides:

```bash
# Different categories or window for a one-off check
python skills/research-discovery/scripts/fetch.py --categories cs.AI,cs.CL --lookback-days 3

# Preview what would be discovered without writing anything
python skills/research-discovery/scripts/fetch.py --dry-run

# Skip the score gate and download PDFs immediately for everything found
# (bypasses download_top.py entirely — use sparingly, defeats the point of scoring first)
python skills/research-discovery/scripts/fetch.py --download
```

Read the stdout summary line (`Done. seen=... new=... duplicates=... out_of_lookback=... download_failures=...`) and report it in plain language: how many new papers were queued, how many were already known. Newly written metadata carries `"status": "queued"` — the handoff to [[editorial-triage]].

## Phase 2: download_top.py

Run this after triage has scored the current batch:

```bash
python skills/research-discovery/scripts/download_top.py
```

It looks at every `reviewed`, not-yet-downloaded paper whose `recommendation` is `download_eligible` (per `screening.recommendations` in the config — currently `Review fully` and `Priority review`), ranks by recommendation tier then `overall_score`, and downloads up to `download_top_n` minus however many were already downloaded this calendar week (Monday–Sunday). Report the summary: how many downloaded, how many deferred (still eligible, just outranked this week — they carry forward, not lost).

```bash
# See what would download without touching the network
python skills/research-discovery/scripts/download_top.py --dry-run

# Override the weekly cap for a one-off catch-up run
python skills/research-discovery/scripts/download_top.py --top-n 10
```

Downloaded papers get `"downloaded": true` and `"downloaded_at"` in their metadata — that timestamp is what the weekly budget counts against, so a paper downloaded outside the normal cadence (e.g. via `fetch.py --download`) still counts toward that week's cap.

## What gets written

```
papers/metadata/<arxiv_id>.json           — title, authors, abstract, categories, dates, pdf_url, status: "queued"
papers/pdf/<year-week>/<arxiv_id>.pdf     — PDF, written only by download_top.py (or fetch.py --download)
                                             grouped by the ISO year-week it was downloaded in (e.g. 2026-W31)
logs/fetch-<timestamp>.log                — fetch.py run log
logs/download_top-<timestamp>.log         — download_top.py run log
```

Every metadata record also carries `"discovery_date"` in the same `<year-week>` format (e.g. `"2026-W31"`), stamped once at discovery time — this is a fixed record of *when the paper was found*, independent of when (or whether) its PDF later gets downloaded, which can land in a later week if it's deferred by the `download_top_n` cap.

## Guarantees

- **Never downloads duplicates.** `already_known()` checks for an existing `papers/metadata/<arxiv_id>.json` before touching the network for that paper.
- **Never loses an eligible paper.** `download_top.py`'s deferred candidates aren't discarded — they're just outranked this week, and are reconsidered every run until downloaded or overtaken indefinitely.
- **Resumable and idempotent.** Interrupting either script and re-running is always safe — already-written metadata and already-downloaded PDFs are skipped, not redone.
- **Configurable.** Categories, lookback window, `download_top_n`, and the `screening.recommendations` eligibility gate all come from `config/editorial-profile.yaml` and can be overridden per run via flags (except the gate, which editorial-strategist proposes changes to). `max_results` is also configurable but hard-capped at 100 papers/week regardless of config or override — `fetch.py` clamps it (`min(..., 100)`).

## Requirements

Both scripts need PyYAML (`pip install pyyaml`) and network access to `export.arxiv.org`. No API key is required — arXiv's API is public.

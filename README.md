# signal2insights

A personal research intelligence system: it turns new arXiv papers into a curated, searchable knowledge base (the **ArxivWiki**), and produces a queue of high-value papers ready to become thought leadership content via Claude Co-work.

```
Research (arXiv) → Knowledge (ArxivWiki) → Content queue (papers.csv)
```

Everything for this system lives in this repository. Nothing outside it is read or written by any of these skills.

## The 6 skills

All 6 skill folders live under `skills/`, separate from the config, papers, and wiki data they operate on.

| Skill | Judges papers? | Backing script |
|---|---|---|
| [research-discovery](skills/research-discovery/SKILL.md) | No — retrieval only | `scripts/fetch.py`, `scripts/download_top.py` |
| [editorial-triage](skills/editorial-triage/SKILL.md) | Yes — scores against the editorial profile | `scripts/apply_scores.py`, `scripts/reassess_fulltext.py` (write-out helpers; the judgment itself is unscripted) |
| [knowledge-extraction](skills/knowledge-extraction/SKILL.md) | Yes — a second, full-text gate (`keep`) on papers that already passed triage | `scripts/apply_extraction.py` (write-out helper; also renders the wiki page) |
| [research-librarian](skills/research-librarian/SKILL.md) | No — aggregates and indexes | `scripts/build_index.py` |
| [pipeline-builder](skills/pipeline-builder/SKILL.md) | No — scaffolding, scheduling, health checks | none |
| [editorial-strategist](skills/editorial-strategist/SKILL.md) | No — analyzes past judgments, proposes profile changes | none |

Deterministic, mechanical steps (arXiv API calls, dedup, CSV/index rebuilding) run as real Python scripts. Anything requiring judgment (does this paper matter, what does it mean, is the model calibrated) is reasoned through by the skill directly at run time — there is no way to script "is this worth an enterprise AI builder's time."

## Data flow

Papers are screened on their abstract *before* a PDF is ever downloaded — PDF download is a separate, later gate capped at `download_top_n` per week, not an automatic side effect of discovery.

```
research-discovery                editorial-triage             research-discovery              knowledge-extraction                    research-librarian
(fetch.py)                        (judgment)                   (download_top.py)               (judgment)                              (build_index.py)
     |                                  |                              |                              |                                      |
     v                                  v                              v                              v                                      v
papers/metadata/<id>.json  --> papers/metadata/scores/<id>.yaml --> papers/pdf/<wk>/<id>.pdf --> papers/metadata/extractions/<id>.yaml --> papers/papers.csv
status: queued                  status: queued -> ignored          downloaded: true                (always written) --keep:true--> ArxivWiki/papers/<yr>/<id>.md
discovery_date: <wk>                       or triaged              (top N by score only,             status: extracted, or                  ArxivWiki/index.md
                                                                     grouped by download week)         evaluated if keep:false                ArxivWiki/tags/*.md, concepts/*.md
```

`<wk>` is an ISO year-week, e.g. `2026-W31` — see "Weekly grouping" below. `editorial-strategist` sits outside this main flow — it reads feedback (`logs/feedback.jsonl`) plus the outputs above, and writes proposals (`logs/strategist-proposal-<date>.md`) that a human applies to `config/editorial-profile.yaml` by hand.

## Paper status lifecycle

Every `papers/metadata/<arxiv_id>.json` carries a `status` field, set by [editorial-triage](skills/editorial-triage/SKILL.md)'s `recommendation` via `screening.recommendations` in the config:

| Status | Set when recommendation is | Meaning |
|---|---|---|
| `queued` | (not yet screened) | Discovered, not yet triaged |
| `ignored` | `Ignore` or `Archive` | Terminal — doesn't deserve attention, or on-topic but not worth acting on now |
| `triaged` | `Read later` | Screened, but not eligible for download or extraction yet |
| `triaged` | `Review fully` or `Priority review` | Screened, eligible for download and extraction |
| `evaluated` | (knowledge-extraction ran, `keep: false`) | Terminal — full text was read and judged, but it isn't durable-knowledge-worthy. No wiki page. |
| `extracted` | (knowledge-extraction ran, `keep: true`) | Wiki page written |

`download_eligible` and `extract_eligible` are separate booleans on the same record, also read straight from the recommendation's config entry — [research-discovery](skills/research-discovery/SKILL.md)'s `download_top.py` and [knowledge-extraction](skills/knowledge-extraction/SKILL.md) gate on those flags directly, not on `status` or a numeric threshold. `keep` is knowledge-extraction's own gate, a full-text second opinion on editorial-triage's abstract-only recommendation — a paper marked `extract_eligible` can still land `status: "evaluated"` instead of `"extracted"` if the full paper doesn't hold up.

`papers/papers.csv` (maintained by research-librarian) derives `Summarised` and `LinkedIn written` from the wiki file's existence and a manually-tracked field respectively — those are read state, not part of the status enum.

`downloaded` / `downloaded_at` are a separate boolean+timestamp on the same record, independent of `status` — a paper can be `triaged` and `download_eligible` with `downloaded: false` for weeks if it never ranks in `download_top_n`. Extraction requires `status == "triaged"`, `extract_eligible == true`, *and* `downloaded == true`.

`overall_score` is the sum of editorial-triage's seventeen 1-5 quantitative screening dimensions (max 85) — a single sortable number for `papers.csv` and for ranking within `download_top_n`, but never the gate itself. The `recommendation` (Ignore/Archive/Read later/Review fully/Priority review) is a reasoned judgment informed by the full 25-question screening, not a mechanical cutoff on that sum — see [editorial-triage](skills/editorial-triage/SKILL.md) for the full rubric. research-librarian's archiving step keys off the recommendation's `download_eligible` flag, so a paper that's been screened is never archived on stale logic disagreeing with its own recorded judgment.

## Weekly grouping

Two independent week tags exist, both in ISO year-week format (`YYYY-Www`, e.g. `2026-W31`), and they can differ for the same paper:

- **`discovery_date`** on the metadata record — stamped once, permanently, the week `fetch.py` first found the paper. Never changes.
- **The PDF's folder** — `papers/pdf/<year-week>/<arxiv_id>.pdf` — is the week the PDF was actually *downloaded*, which can be later than `discovery_date` if the paper was deferred by the `download_top_n` cap and only cleared it in a subsequent week's run. `research-discovery/scripts/fetch.py`'s `iso_week_str()` computes both.

`fetch.py` also hard-caps `max_results` at 100 papers per run regardless of config or `--max-results` override — search volume never exceeds 100/week.

## Folder map

```
signal2insights/
├── README.md                        this file
├── config/
│   └── editorial-profile.yaml       shared config — mission, topics, screening rubric + recommendation gates, discovery scope
├── papers/
│   ├── pdf/<year-week>/<id>.pdf     downloaded PDFs, grouped by ISO year-week of download (e.g. 2026-W31/)
│   ├── metadata/
│   │   ├── <arxiv_id>.json          one record per paper, lifecycle status + discovery_date live here
│   │   ├── scores/<arxiv_id>.yaml   editorial-triage's full screening record (Sections A-F, see its SKILL.md)
│   │   └── extractions/<id>.yaml    knowledge-extraction's full worksheet record (Sections A-H + Final Assessment) — always written once read, regardless of keep
│   └── papers.csv                   generated by research-librarian — the queue for Claude Co-work
├── logs/                            timestamped run logs, feedback.jsonl, strategist proposals
├── archive/pdf/<year-week>/         PDFs archived by research-librarian (recommendation no longer download_eligible, week preserved) or superseded versions
├── ArxivWiki/
│   ├── index.md                     generated entry point, grouped by recommendation tier
│   ├── papers/<year>/<arxiv_id>.md  one knowledge asset per paper
│   ├── tags/<tag>.md                generated, one page per topic tag
│   └── concepts/<concept>.md        generated, one page per named idea/technique
└── skills/
    ├── research-discovery/
    │   ├── SKILL.md
    │   └── scripts/
    │       ├── fetch.py                 phase 1: metadata only
    │       └── download_top.py          phase 2: PDFs for the top download_top_n by score
    ├── editorial-triage/
    │   ├── SKILL.md
    │   └── scripts/
    │       ├── apply_scores.py          write-out helper for triage judgments
    │       └── reassess_fulltext.py     write-out helper for post-download full-text reassessment
    ├── knowledge-extraction/
    │   ├── SKILL.md
    │   └── scripts/apply_extraction.py  write-out helper for extraction judgments; also renders the wiki page from the structured record
    ├── research-librarian/
    │   ├── SKILL.md
    │   └── scripts/build_index.py
    ├── pipeline-builder/SKILL.md
    └── editorial-strategist/SKILL.md
```

## Running the full pipeline

See [pipeline-builder](skills/pipeline-builder/SKILL.md) for the end-to-end sequence, folder repair, and scheduling. Short version:

```bash
python skills/research-discovery/scripts/fetch.py
# then: triage the queue (reasoning step, invoked as a skill) -- writes via apply_scores.py
python skills/research-discovery/scripts/download_top.py
# then: extract what's downloaded and extract_eligible (reasoning step, invoked as a skill)
python skills/research-librarian/scripts/build_index.py
```

## Requirements

Python 3 with PyYAML (`pip install pyyaml`) for the backend scripts. No API keys — arXiv's API is public. Everything else (scoring, extraction, indexing judgment calls, proposals) runs through Claude Code directly.

## Scope note

Writing the actual LinkedIn post or other thought-leadership content from a queued paper is intentionally outside this system — `papers/papers.csv`'s `LinkedIn written = False` rows, sorted by score, are the handoff point to Claude Co-work, one paper at a time.

# signal2insights

A personal research intelligence system: it turns new arXiv papers into a curated, searchable knowledge base (the **ArxivWiki**), and produces a queue of high-value papers ready to become thought leadership content via Claude Co-work.

```
Research (arXiv) → Knowledge (ArxivWiki) → Content queue (papers.csv)
```

Everything for this system lives in this repository, and nothing outside it is written by any of these skills. One deliberate read exception: [carousel-production](skills/carousel-production/SKILL.md) may search the web, and only to source or verify a figure that the paper does not supply. Any figure it takes from outside is cited on the slide with its publisher and year. External sources set the scene around a paper; they never support a claim about what the research found.

## The 9 skills

All 9 skill folders live under `skills/`, separate from the config, papers, and wiki data they operate on.

| Skill | Judges papers? | Backing script |
|---|---|---|
| [research-discovery](skills/research-discovery/SKILL.md) | No — retrieval only | `scripts/fetch.py`, `scripts/download_top.py` |
| [editorial-triage](skills/editorial-triage/SKILL.md) | Yes — scores against the editorial profile | `scripts/apply_scores.py`, `scripts/reassess_fulltext.py` (write-out helpers; the judgment itself is unscripted) |
| [editorial-review](skills/editorial-review/SKILL.md) | Human reviews, not a new score — approves or overrides a Priority-review call before extraction | `scripts/build_summary.py`, `scripts/apply_human_review.py` (write-out helpers; the decision is a human, via an interactive widget) |
| [knowledge-extraction](skills/knowledge-extraction/SKILL.md) | Yes — a second, full-text gate (`keep`) on papers that already passed triage | `scripts/build_fulltext.py` + `scripts/pdftext.py` (PDF → `output/<wk>/<wk>_<id>.md`), `scripts/apply_extraction.py` (write-out helper; also renders the wiki page) |
| [research-librarian](skills/research-librarian/SKILL.md) | No — aggregates and indexes | `scripts/build_index.py` |
| [theme-dashboard](skills/theme-dashboard/SKILL.md) | No — visualizes what knowledge-extraction already decided | `scripts/build_dashboard.py` (write-out; publishing the result is a manual Artifact-tool step) |
| [pipeline-builder](skills/pipeline-builder/SKILL.md) | No — scaffolding, scheduling, health checks | none |
| [editorial-strategist](skills/editorial-strategist/SKILL.md) | No — analyzes past judgments, proposes profile changes | none |
| [carousel-production](skills/carousel-production/SKILL.md) | No — turns an already-summarised paper into LinkedIn carousel copy, via four subagents | `scripts/check_standards.py` (lints copy against `writing-standards.md`; the writing and the review are subagent judgment) |

Deterministic, mechanical steps (arXiv API calls, dedup, CSV/index rebuilding) run as real Python scripts. Anything requiring judgment (does this paper matter, what does it mean, is the model calibrated) is reasoned through by the skill directly at run time — there is no way to script "is this worth an enterprise AI builder's time."

## Data flow

Papers are screened on their abstract *before* a PDF is ever downloaded — PDF download is a separate, later gate capped at `download_top_n` per week, not an automatic side effect of discovery.

Discovery, triage, and human review are also **interleaved per batch**, not sequential phases over the whole week's results: `fetch.py --batch-size N` writes a batch of metadata, editorial-triage scores those abstracts immediately, [editorial-review](skills/editorial-review/SKILL.md) puts them in front of the user, and the user's decisions recalibrate the scoring standard before the next batch is pulled. The loop ends when `download_top_n` papers have been **approved** — not merely scored as viable. Results are deliberately left unfetched at that point, and any fetched-but-unscreened paper stays `status: "queued"` for a later run.

The human review gate is mandatory and it gates `download_top.py`: no PDF is downloaded for a paper the user has not approved. `screening.viable_target` (default 10) only caps how many candidates get put in front of the reviewer at a time.

```
research-discovery                editorial-triage             research-discovery                knowledge-extraction                    research-librarian                    theme-dashboard
(fetch.py)                        (judgment)                   (download_top.py)                 (judgment)                              (build_index.py)                      (build_dashboard.py)
     |                                  |                              |                                |                                      |                                      |
     v                                  v                              v                                v                                      v                                      v
papers/metadata/<id>.json  --> papers/metadata/scores/<id>.yaml --> output/<wk>/<wk>_<id>.pdf --> papers/metadata/extractions/<id>.yaml --> papers/papers.csv                    ArxivWiki/dashboard.html
status: queued                  status: queued -> ignored          downloaded: true                  (always written) --keep:true--> ArxivWiki/papers/<yr>/<id>.md               --> published as a Claude Artifact
discovery_date: <wk>                       or triaged              (top N by score only,               status: extracted, or                  ArxivWiki/index.md                    (concept/tag frequency over
                                                                     grouped by download week)           evaluated if keep:false                ArxivWiki/tags/*.md, concepts/*.md      kept papers only)
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

`overall_score` is the sum of editorial-triage's five 1-5 quantitative screening dimensions (max 25) — a single sortable number for `papers.csv` and for ranking within `download_top_n`, but never the gate itself. The `recommendation` (Ignore/Archive/Read later/Review fully/Priority review) is a reasoned judgment informed by the full 13-question screening, not a mechanical cutoff on that sum — see [editorial-triage](skills/editorial-triage/SKILL.md) for the full rubric. research-librarian's archiving step keys off the recommendation's `download_eligible` flag, so a paper that's been screened is never archived on stale logic disagreeing with its own recorded judgment.

## Weekly grouping

Two independent week tags exist, both in ISO year-week format (`YYYY-Www`, e.g. `2026-W31`), and they can differ for the same paper:

- **`discovery_date`** on the metadata record — stamped once, permanently, the week `fetch.py` first found the paper. Never changes.
- **The PDF's folder** — `output/<year-week>/<year-week>_<arxiv_id>.pdf` — is the week the PDF was actually *downloaded*, which can be later than `discovery_date` if the paper was deferred by the `download_top_n` cap and only cleared it in a subsequent week's run. `research-discovery/scripts/fetch.py`'s `iso_week_str()` computes both.

`fetch.py` also hard-caps `max_results` at 100 papers per run regardless of config or `--max-results` override — search volume never exceeds 100/week.

## Folder map

```
signal2insights/
├── README.md                        this file
├── config/
│   └── editorial-profile.yaml       shared config — mission, topics, screening rubric + recommendation gates, discovery scope
├── output/<year-week>/               everything produced for a paper once it's selected, grouped by ISO year-week of download (e.g. 2026-W31/), filenames prefixed <year-week>_<arxiv_id>
│   ├── <wk>_<id>.pdf                 downloaded PDF
│   ├── <wk>_<id>.md                  cleaned body text extracted from the PDF — references, acknowledgements and appendices removed. What every skill actually reads; the Read tool cannot open PDFs here
│   ├── <wk>_<id>_carousel-draft.md   carousel-production's deliverable — slide copy, then design direction appended
│   ├── <wk>_<id>_review-business.md  carousel-reviewer-business findings, persisted by the orchestrator
│   ├── <wk>_<id>_review-technical.md carousel-reviewer-technical findings, persisted by the orchestrator
│   ├── <wk>_<id>_review-log.md       one row per review pass, appended by the orchestrator
│   └── <wk>_<id>_history/rev-NN.md   draft snapshot before each revision pass
├── papers/
│   ├── metadata/
│   │   ├── <arxiv_id>.json          one record per paper, lifecycle status + discovery_date live here
│   │   ├── scores/<arxiv_id>.yaml   editorial-triage's full screening record (Sections A-D, see its SKILL.md)
│   │   └── extractions/<id>.yaml    knowledge-extraction's full worksheet record (Sections A-H + Final Assessment) — always written once read, regardless of keep
│   └── papers.csv                   generated by research-librarian — the queue for Claude Co-work
├── logs/                            timestamped run logs, feedback.jsonl, strategist proposals
├── archive/pdf/<year-week>/<id>.pdf  PDFs archived by research-librarian (recommendation no longer download_eligible, week preserved) or superseded versions — keeps its own older, unprefixed filename convention, untouched by the output/ restructure
├── ArxivWiki/
│   ├── index.md                     generated entry point, grouped by recommendation tier
│   ├── papers/<year>/<arxiv_id>.md  one knowledge asset per paper
│   ├── tags/<tag>.md                generated, one page per topic tag
│   ├── concepts/<concept>.md        generated, one page per named idea/technique
│   ├── dashboard.html               generated concept/tag frequency dashboard over kept papers (HTML fragment, publishable as a Claude Artifact)
│   ├── .dashboard-artifact.json     bookkeeping only — last-published Artifact URL, so redeploys update the same link
│   └── summaries/<arxiv_id>.md      one-pagers for Priority-review papers awaiting human review (editorial-review), pre-extraction
├── .claude/agents/                  the four carousel subagent definitions (writer, 2 reviewers, designer)
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
    ├── editorial-review/
    │   ├── SKILL.md
    │   └── scripts/
    │       ├── build_summary.py         write-out helper: renders a one-pager for a pre-extraction Priority-review paper
    │       └── apply_human_review.py    write-out helper: applies an approve/archive/ignore decision, logs to logs/feedback.jsonl
    ├── knowledge-extraction/
    │   ├── SKILL.md
    │   └── scripts/
    │       ├── apply_extraction.py      write-out helper for extraction judgments; also renders the wiki page from the structured record
    │       ├── build_fulltext.py        PDF -> output/<wk>/<wk>_<id>.md, body only (drops references, acknowledgements, appendices)
    │       └── pdftext.py               dependency-free PDF text extractor; no PDF library is installable on this machine
    ├── research-librarian/
    │   ├── SKILL.md
    │   └── scripts/build_index.py
    ├── theme-dashboard/
    │   ├── SKILL.md
    │   └── scripts/build_dashboard.py   write-out helper; publishing the result via the Artifact tool is a manual step
    ├── carousel-production/
    │   ├── SKILL.md
    │   ├── writing-standards.md        canonical copy standard for carousels; the agents read it, the script enforces it
    │   └── scripts/check_standards.py  lints a draft: dashes, banned phrases, attribution, title case, verbatim quotes
    ├── pipeline-builder/SKILL.md
    └── editorial-strategist/SKILL.md
```

## Running the full pipeline

See [pipeline-builder](skills/pipeline-builder/SKILL.md) for the end-to-end sequence, folder repair, and scheduling. Short version:

```bash
# loop until download_top_n papers are human-approved (or arXiv runs out):
python skills/research-discovery/scripts/fetch.py --batch-size 20
# then, per batch: read logs/feedback.jsonl, triage that batch (reasoning step, invoked
#   as a skill, writes via apply_scores.py), run editorial-review with the user
#   (mandatory), recalibrate from their corrections, then re-run the same fetch
#   command for the next batch if still short of the approval gate
python skills/research-discovery/scripts/download_top.py   # approved papers only
python skills/knowledge-extraction/scripts/build_fulltext.py --all   # PDF -> output/<wk>/<wk>_<id>.md
# then: extract what's downloaded and extract_eligible (reasoning step, invoked as a skill)
python skills/research-librarian/scripts/build_index.py
python skills/theme-dashboard/scripts/build_dashboard.py
# then: publish ArxivWiki/dashboard.html via the Artifact tool (manual step, needs Claude in the loop)
```

## Requirements

Python 3 with PyYAML (`pip install pyyaml`) for the backend scripts. On Windows, the bare `python`/`python3` commands may resolve to the Microsoft Store alias stub instead of a real interpreter — a conda installation (e.g. `conda activate <env>`, or invoking `<conda-env-path>\python.exe` directly) satisfies the requirement instead. No API keys — arXiv's API is public. Everything else (scoring, extraction, indexing judgment calls, proposals) runs through Claude Code directly.

## Scope note

Carousel copy is now produced inside this system by [carousel-production](skills/carousel-production/SKILL.md), which takes a paper that already has an `ArxivWiki/summaries/<id>.md` one-pager and drafts, reviews and revises the slides. `papers/papers.csv`'s `LinkedIn written = False` rows, sorted by score, remain the queue that selects which paper to draft next.

Two things stay outside it. **Rendering** a draft to HTML, PDF or images is a separate action requiring its own explicit instruction, and no skill or agent here performs it. **Other content formats** (long-form posts, articles, talks) have no skill yet.

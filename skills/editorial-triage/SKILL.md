---
name: editorial-triage
description: Screen queued arXiv papers against the enterprise-AI editorial profile and decide whether each deserves a full review. Use this skill when the user asks to triage, score, review, or screen newly discovered papers, or asks "what's worth reading from this batch". This is the heart of the system — it judges relevance to enterprise AI builders, not academic importance. Trigger on phrases like "triage the queue", "score these papers", "screen this batch", "what's worth reading", "review new papers".
---

# Editorial Triage

## Purpose

Determine whether a paper deserves a full review, based solely on its metadata and abstract.

The objective is not to identify the "best research." The objective is to identify research that matters to people building enterprise AI systems. Screen against [[../../config/editorial-profile.yaml]]'s mission and topic lists, not against academic prestige signals (venue, citation count, author fame).

The judgment itself is unscripted — you reason over each paper directly and answer the questions below. `scripts/apply_scores.py` and `scripts/reassess_fulltext.py` are write-out helpers only: they take your already-decided answers and fan them out to the two files a screening record touches (see "Output" below). Neither script scores anything.

## Input

For each paper with `"status": "queued"` in `../../papers/metadata/<arxiv_id>.json`: title, abstract, categories. Full PDF text is not needed at this stage — that level of depth belongs to [[knowledge-extraction]], or to the optional "Full-text reassessment" pass below, both of which only run for papers that already passed this screen.

## The screening questions

Four sections, thirteen questions. Answer all of them for every candidate — this is a fixed worksheet, not a menu. The fixed checklists (business functions, themes, primary type, adoption horizon) and the valid recommendation labels all live in `../../config/editorial-profile.yaml`'s `screening` block — read them from there rather than hardcoding, in case [[editorial-strategist]] later proposes a change.

Condensed 2026-07-28 from the original 6-section/25-question worksheet after feedback analysis showed the old Editorial Value section let research novelty halo into business-value scores for papers that were technically deep but not enterprise-actionable (see `../../logs/strategist-proposal-2026-07-28.md`). Every one of the old 17 dimensions still has a home in the 5 below — none were dropped, only merged.

### Section A — Relevance

| # | Question | Answer as |
|---|---|---|
| A1 | What enterprise problem does this paper attempt to solve? | free text |
| A2 | Which business functions would care about this research? | multi-select from `screening.business_functions` (CIO/CTO, Chief AI Officer, Engineering, Data Science, Security, Compliance, Product, Operations, Other) |
| A3 | Which enterprise AI themes does this paper relate to? | multi-select from `screening.enterprise_ai_themes` (Agentic AI, RAG, Memory, Evaluation, LLMOps, Observability, Governance, Security, Reliability, Cost Optimization, Infrastructure, Fine-tuning, Other) |
| A4 | Is this primarily scientific research, an engineering technique, a system architecture, an evaluation methodology, a framework, a benchmark, or operational guidance? | single-select from `screening.primary_types` |

### Section B — Substance (each 1-5)

| # | Question | Field |
|---|---|---|
| B5 | Does it challenge an existing best practice or introduce a genuinely new concept, and how transformational (vs. incremental) is the innovation? | `novelty` |
| B6 | Is it convincingly *and* honestly demonstrated — validation strength, evaluation clarity, and acknowledged limitations, taken together? | `evidence_quality` |

### Section C — Business Fit

| # | Question | Field | Answer as |
|---|---|---|---|
| C7 | Could an enterprise implement this today, and does a real business function — including platform/engineering teams, but as an adoption signal, not as the target audience — have a reason to act on it? | `enterprise_readiness` | 1-5 |
| C8 | Does this map to a decision an **executive or business leader (CDO/CTO/CIO, business leadership)** is *already* asking about — not a platform team's technical curiosity, and not something requiring a research background to connect to a business outcome? | `business_translatability` | 1-5 |
| C9 | Is there a quotable, narrative-worthy story here for that *same* executive/business-leader audience — not something merely surprising to an engineer or ML researcher? | `story_potential` | 1-5 |
| C10 | What adoption horizon best fits? | `adoption_horizon` | single-select from `screening.adoption_horizons` (Immediate, `<12 months`, 1-3 years, Long-term research) |

**C8 and C9 are where this rubric most often goes wrong if you're not careful.** A paper can legitimately score high on `novelty`/`evidence_quality` (B5/B6) while scoring low on `business_translatability`/`story_potential` (C8/C9) — a technically deep, rigorous finding that requires several inferential steps to connect to an enterprise decision does NOT automatically earn a high C8/C9. If you can't state the business implication without first explaining an ML-research concept the target reader doesn't already know (e.g. conformal calibration, counterfactual memorization, KV-cache eviction theory), that's a sign C8/C9 should be lower, not that the explanation is still owed. Score these on the translation as it stands, for an executive/business-leader reader specifically — not on the paper's intrinsic research merit, and not on whether a platform or engineering team would find it interesting (that's `enterprise_readiness`, C7).

### Section D — Decision

| # | Question | Field | Answer as |
|---|---|---|---|
| D11 | What is the single best business headline for this paper? | `headline` | free text, e.g. *"Memory — not bigger models — is becoming the next competitive advantage."* |
| D12 | Overall recommendation | `recommendation` | single-select from `screening.recommendation_order`: **Ignore**, **Archive**, **Read later**, **Review fully**, **Priority review** |
| D13 | Explain your recommendation | `recommendation_reasoning` | free text, ≤150 words |

**D12 is the actual gate** — not a mechanical sum of the five 1-5 fields. Weigh all of Sections A-C as a human editor would, the same way `priority_topics` outweighs `secondary_topics` and `ignore_topics` is a strong-but-not-absolute down-weight (a robotics paper with major enterprise-agent implications can still score well). `Ignore` and `Archive` are both terminal and behave identically downstream, but mean different things: `Ignore` doesn't deserve attention; `Archive` is on-topic but not worth acting on right now (weak evidence, superseded, or already well-covered).

## Output

`overall_score` (the sum of the five 1-5 fields, max 25) is computed by `apply_scores.py` from your answers — it is a sortable, legacy-compatible number for `papers.csv` and ranking, never the gate itself.

Write your answers to a batch JSON matching `apply_scores.py`'s docstring, one object per paper, then run:

```bash
python skills/editorial-triage/scripts/apply_scores.py <batch.json>
```

This writes `../../papers/metadata/scores/<arxiv_id>.yaml`:

```yaml
enterprise_problem: "..."
headline: "..."
recommendation_reasoning: "..."
business_functions: [Engineering, Security]
enterprise_ai_themes: [Agentic AI, Governance]
primary_type: Engineering technique
adoption_horizon: <12 months
novelty: 4
evidence_quality: 4
enterprise_readiness: 3
business_translatability: 4
story_potential: 3
overall_score: 18
recommendation: Review fully
fulltext_reassessed: false
```

And updates `../../papers/metadata/<arxiv_id>.json`:
- `"reviewed": true`, `"reviewed_at"`
- `"overall_score"` and `"recommendation"` copied in for quick lookup without opening the score file
- `"status"`, `"download_eligible"`, `"extract_eligible"` — read straight from `screening.recommendations.<recommendation>` in the config, not decided by this skill directly

## Process

1. List candidates: `papers/metadata/*.json` where `status == "queued"` — normally the batch [[research-discovery]] just wrote, per "Batched screening loop" below.
2. Answer all 13 questions per paper, in the same pass reasoning briefly about *why* for D13 — that field should let future-you (or [[editorial-strategist]]) understand the call without re-reading the abstract.
3. Run `apply_scores.py` on the batch.
4. Report a short summary table to the user: arXiv ID, title, headline, overall score, recommendation. Group by recommendation so Priority review / Review fully stand out.
5. Do not download anything, do not extract anything, do not write to the wiki. That is [[knowledge-extraction]]'s job, gated on the screening this skill produces.

## Read the feedback log before scoring anything

**Start every screening session by reading `../../logs/feedback.jsonl`.** It is the accumulated record of the user's own corrections — every discard reason and every score adjustment from past [[editorial-review]] cycles — and it is the only calibration signal this skill has. Scoring a batch without reading it means repeating a mistake the user has already corrected, in writing, in this repo. Recurring notes there ("too technical", "no audience beyond IT", "scope is very narrow", `business_implication 2->1`) are instructions about where this rubric drifts, not history.

This has gone wrong for real: on 2026-07-29, 42 papers were screened with `business_translatability` and `story_potential` inflated on every single viable candidate, because the ten prior feedback entries saying exactly that were never opened.

## Batched screening loop

Screening is interleaved with discovery, not run once over a full 100-paper pull. Each paper is scored on its abstract right after its metadata is written, in batches, and each batch is reviewed and recalibrated before the next one is pulled:

1. `python skills/research-discovery/scripts/fetch.py --batch-size 20` — see [[research-discovery]] phase 1.
2. Screen every `status == "queued"` paper from that batch (the full 13 questions each), and apply via `apply_scores.py`.
3. Hand this batch's viable candidates — recommendation `extract_eligible` in `screening.recommendations`, currently `Review fully` and `Priority review` — to [[editorial-review]] for the user's decisions. This is not optional and it happens per batch, not once at the end.
4. **Recalibrate before pulling the next batch.** Fold the review's decisions and score corrections into the standard, and re-score any already-screened paper the corrected standard would move — a demotion is written with `apply_scores.py`, and the pre-existing records should be snapshotted to `../../logs/` first, since `apply_scores.py` keeps no history and `reassess_fulltext.py` would falsely mark the record as full-text reassessed.
5. If fewer than `download_top_n` papers are approved, return to step 1 for another batch. Otherwise stop — hand off to [[research-discovery]]'s phase 2.

`screening.viable_target` (default 10) caps how many candidates to put in front of the reviewer before pausing; `download_top_n` (default 5) is the number of *approved* papers that actually releases the download step. The second is the real gate.

Two consequences worth being explicit about:

- **A stopped loop leaves papers unfetched and unscored, deliberately.** Reaching the approval gate means the rest of the week's arXiv results are never pulled, and any already-fetched paper not yet screened stays `status: "queued"`. That is not a gap to backfill — `queued` means *not yet screened*, and those records re-compete on the next run.
- **Never let the target bend a judgment.** If a batch is weak, the right outcome is another batch, not inflating a borderline paper to `Review fully` to close out the count. The stop condition is a budget on effort, never an input to Section D. This cuts both ways: when recalibration drops the viable count below the gate, pull another batch — do not rescue a paper the corrected standard just demoted.

## Weekly limit

`weekly_limit` in the config caps how many papers get promoted through extraction per week, not how many get screened. Within a batch, screen every queued paper the batch contains regardless of volume — the early stop above operates between batches, never mid-batch. If more papers are `extract_eligible` in a week than `weekly_limit` allows, [[knowledge-extraction]] and [[research-librarian]] are responsible for picking the top subset (recommendation tier first, `overall_score` as tiebreaker), not this skill.

## Full-text reassessment (optional, after PDF download)

The screening above is abstract-only when first written. If a paper gets downloaded (`skills/research-discovery/scripts/download_top.py`), re-read the full PDF and reassess the record against what the full text actually says — abstracts routinely omit qualifying results, ablations, or scope limits that change several answers, most often `evidence_quality`, `enterprise_readiness`, and the recommendation itself.

1. Read the downloaded PDF in full.
2. Re-answer the full 13-question worksheet — not just the recommendation — against what the paper actually shows, not what the abstract claimed.
3. Run `python skills/editorial-triage/scripts/reassess_fulltext.py <batch.json>` (same record shape as `apply_scores.py`) — it diffs the new `overall_score` and `recommendation` against whatever screening record already exists, logs the delta per paper, and writes the updated record with `fulltext_reassessed: true`.
4. Report the delta table to the user: which recommendations moved, by how much, and why (usually: an abstract oversold or undersold a finding the full text qualifies).

This is the step that makes a downloaded paper's recommendation trustworthy enough for [[research-librarian]]'s housekeeping to treat a downward revision as deliberate rather than archive it on stale abstract-only judgment — see that skill's archiving behavior.

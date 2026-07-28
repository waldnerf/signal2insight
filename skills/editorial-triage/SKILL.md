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

Six sections, twenty-five questions. Answer all of them for every candidate — this is a fixed worksheet, not a menu. The fixed checklists (business functions, themes, primary type, adoption horizon) and the valid recommendation labels all live in `../../config/editorial-profile.yaml`'s `screening` block — read them from there rather than hardcoding, in case [[editorial-strategist]] later proposes a change.

### Section A — Relevance

| # | Question | Answer as |
|---|---|---|
| A1 | What enterprise problem does this paper attempt to solve? | free text |
| A2 | Which business functions would care about this research? | multi-select from `screening.business_functions` (CIO/CTO, Chief AI Officer, Engineering, Data Science, Security, Compliance, Product, Operations, Other) |
| A3 | Which enterprise AI themes does this paper relate to? | multi-select from `screening.enterprise_ai_themes` (Agentic AI, RAG, Memory, Evaluation, LLMOps, Observability, Governance, Security, Reliability, Cost Optimization, Infrastructure, Fine-tuning, Other) |
| A4 | Is this primarily scientific research, an engineering technique, a system architecture, an evaluation methodology, a framework, a benchmark, or operational guidance? | single-select from `screening.primary_types` |

### Section B — Strategic Importance (each 1-5)

| # | Question | Field |
|---|---|---|
| B5 | If validated, how much could this influence enterprise AI architectures? | `architectural_influence` |
| B6 | Does it challenge an existing best practice? (1 = no, 5 = fundamentally) | `challenges_best_practice` |
| B7 | Does it introduce a genuinely new concept? | `novelty` |
| B8 | Does it improve how enterprise AI systems are built, evaluated, deployed, or governed? | `enterprise_improvement` |
| B9 | Is the innovation incremental (1) or transformational (5)? | `innovation_scale` |

### Section C — Practicality

| # | Question | Field | Answer as |
|---|---|---|---|
| C10 | Could an enterprise implement ideas from this paper today? | `implementable_today` | 1-5 |
| C11 | What adoption horizon best fits? | `adoption_horizon` | single-select from `screening.adoption_horizons` (Immediate, `<12 months`, 1-3 years, Long-term research) |
| C12 | Are there obvious implementation barriers? (1 = none, 5 = severe) | `implementation_barriers` | 1-5 |
| C13 | Does the abstract mention production deployment, or only lab evaluation? (1 = lab only, 5 = production-validated) | `deployment_evidence` | 1-5 |

### Section D — Evidence (each 1-5)

| # | Question | Field |
|---|---|---|
| D14 | Does the abstract describe convincing experimental validation? | `validation_strength` |
| D15 | Are the evaluation methods clearly explained? | `evaluation_clarity` |
| D16 | Are limitations honestly acknowledged? | `limitations_acknowledged` |
| D17 | Does the paper appear rigorous overall? | `rigor` |

### Section E — Editorial Value

| # | Question | Field | Answer as |
|---|---|---|---|
| E18 | Would an enterprise executive care? | `executive_interest` | 1-5 |
| E19 | Would an AI platform team care? | `platform_team_interest` | 1-5 |
| E20 | Is there an obvious business implication? | `business_implication` | 1-5 |
| E21 | Is there an interesting or surprising idea? | `surprise_factor` | 1-5 |
| E22 | Could this become a strong LinkedIn article? | `linkedin_potential` | 1-5 |
| E23 | What is the single best business headline for this paper? | `headline` | free text, e.g. *"Memory — not bigger models — is becoming the next competitive advantage."* |

### Section F — Decision

| # | Question | Field | Answer as |
|---|---|---|---|
| F24 | Overall recommendation | `recommendation` | single-select from `screening.recommendation_order`: **Ignore**, **Archive**, **Read later**, **Review fully**, **Priority review** |
| F25 | Explain your recommendation | `recommendation_reasoning` | free text, ≤150 words |

**F24 is the actual gate** — not a mechanical sum of the seventeen 1-5 fields. Weigh all of Sections A-E as a human editor would, the same way `priority_topics` outweighs `secondary_topics` and `ignore_topics` is a strong-but-not-absolute down-weight (a robotics paper with major enterprise-agent implications can still score well). `Ignore` and `Archive` are both terminal and behave identically downstream, but mean different things: `Ignore` doesn't deserve attention; `Archive` is on-topic but not worth acting on right now (weak evidence, superseded, or already well-covered).

## Output

`overall_score` (the sum of the seventeen 1-5 fields, max 85) is computed by `apply_scores.py` from your answers — it is a sortable, legacy-compatible number for `papers.csv` and ranking, never the gate itself.

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
architectural_influence: 4
challenges_best_practice: 2
novelty: 4
enterprise_improvement: 5
innovation_scale: 3
implementable_today: 3
implementation_barriers: 2
deployment_evidence: 2
validation_strength: 4
evaluation_clarity: 4
limitations_acknowledged: 3
rigor: 4
executive_interest: 3
platform_team_interest: 5
business_implication: 4
surprise_factor: 3
linkedin_potential: 4
overall_score: 59
recommendation: Review fully
fulltext_reassessed: false
```

And updates `../../papers/metadata/<arxiv_id>.json`:
- `"reviewed": true`, `"reviewed_at"`
- `"overall_score"` and `"recommendation"` copied in for quick lookup without opening the score file
- `"status"`, `"download_eligible"`, `"extract_eligible"` — read straight from `screening.recommendations.<recommendation>` in the config, not decided by this skill directly

## Process

1. List candidates: `papers/metadata/*.json` where `status == "queued"`.
2. Answer all 25 questions per paper, in the same pass reasoning briefly about *why* for F25 — that field should let future-you (or [[editorial-strategist]]) understand the call without re-reading the abstract.
3. Run `apply_scores.py` on the batch.
4. Report a short summary table to the user: arXiv ID, title, headline, overall score, recommendation. Group by recommendation so Priority review / Review fully stand out.
5. Do not download anything, do not extract anything, do not write to the wiki. That is [[knowledge-extraction]]'s job, gated on the screening this skill produces.

## Weekly limit

`weekly_limit` in the config caps how many papers get promoted through extraction per week, not how many get screened — screen everything in the queue regardless of volume. If more papers are `extract_eligible` in a week than `weekly_limit` allows, [[knowledge-extraction]] and [[research-librarian]] are responsible for picking the top subset (recommendation tier first, `overall_score` as tiebreaker), not this skill.

## Full-text reassessment (optional, after PDF download)

The screening above is abstract-only when first written. If a paper gets downloaded (`skills/research-discovery/scripts/download_top.py`), re-read the full PDF and reassess the record against what the full text actually says — abstracts routinely omit qualifying results, ablations, or scope limits that change several answers, most often Sections B, D, and E and the recommendation itself.

1. Read the downloaded PDF in full.
2. Re-answer the full 25-question worksheet — not just the recommendation — against what the paper actually shows, not what the abstract claimed.
3. Run `python skills/editorial-triage/scripts/reassess_fulltext.py <batch.json>` (same record shape as `apply_scores.py`) — it diffs the new `overall_score` and `recommendation` against whatever screening record already exists, logs the delta per paper, and writes the updated record with `fulltext_reassessed: true`.
4. Report the delta table to the user: which recommendations moved, by how much, and why (usually: an abstract oversold or undersold a finding the full text qualifies).

This is the step that makes a downloaded paper's recommendation trustworthy enough for [[research-librarian]]'s housekeeping to treat a downward revision as deliberate rather than archive it on stale abstract-only judgment — see that skill's archiving behavior.

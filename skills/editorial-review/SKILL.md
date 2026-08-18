---
name: editorial-review
description: Run a human review cycle over Priority-review papers before they're downloaded or extracted, using an interactive widget for the approve/discard decision, and feed discards into editorial-strategist's existing feedback loop. Use this skill when the user asks to review Priority-review papers, run the review cycle, approve or discard a paper before extraction, or generate a one-pager summary. Trigger on phrases like "review the priority papers", "run the review cycle", "let me approve these before extraction".
---

# Editorial Review

## Purpose

A **mandatory** human checkpoint between [[editorial-triage]] and download/[[knowledge-extraction]]: before spending download and full-text-extraction effort on a Priority-review paper, the user confirms the abstract-only call was right, or discards it while it's still cheap to do so. `download_top.py` must not run on papers that have not been through this cycle — see [[pipeline-builder]] step 2. This runs **once per triage batch**, not once per week: its decisions are what recalibrate the next batch's scoring, so deferring it until the end of a run wastes every batch after the first. This is not a second scoring pass — it never re-derives a score, it only asks a human to confirm or override editorial-triage's own recommendation for one specific paper.

## Scope

Applies to papers where `recommendation` is `Priority review` or `Review fully` (the only two tiers with `download_eligible`/`extract_eligible: true` — Read later/Archive/Ignore are already terminal, nothing downstream to protect) **and** no `papers/metadata/extractions/<id>.yaml` exists yet — i.e. triaged but not yet past the extraction checkpoint. Papers already fully extracted (with a published wiki page) are out of scope for this cycle; re-litigating a paper after full-text reading and a wiki page already exist is a different, heavier decision than this lightweight pre-extraction check. Ranked by `overall_score` descending, capped at 20 papers per run.

## Process

1. **Author the narrative, then generate one-pagers.** Five fields — a high-level summary, 2-4 key highlights, why it matters for enterprise AI, recommended industries (company domains, not internal roles — editorial-triage's `business_functions` already covers roles like Engineering/Compliance, so don't duplicate that list here), and 2-3 concrete business applications — require actually reading the paper's abstract and reasoning about it; none of these are derivable from editorial-triage's structured scoring fields, so write them yourself (the same judgment split as editorial-triage: you reason, the script only renders) into a small JSON keyed by arxiv_id, then run:
   ```bash
   python skills/editorial-review/scripts/build_summary.py --narrative <narrative.json>
   ```
   With no `arxiv_id` arguments this selects every in-scope paper (up to 20). The output `ArxivWiki/summaries/<arxiv_id>.md` leads with your authored sections, then the mechanical triage detail (headline, why triage flagged it, enterprise relevance metadata, top-scoring dimensions) pulled straight from `papers/metadata/scores/<id>.yaml` — no new judgment in that half.

   The provenance line under the title tracks the score record rather than being fixed text: a paper screened abstract-only carries the pre-extraction caveat, while one whose record came from [[editorial-triage]]'s `reassess_fulltext.py` is labelled full-text reassessed. Note that the script keeps no copy of the narrative JSON you pass it — regenerating a summary (after a rescore, say) without supplying the narrative again silently drops the authored half, so recover it from the existing markdown first.

   **Write in business language, not restated abstract-ese.** The person reading this is deciding whether to spend attention on the paper, not grading its methodology. Translate every finding into what it changes about how a team builds, deploys, evaluates, or governs an AI system — name the specific practice, tool, decision, or trade-off affected. Avoid fluff: banned phrases include "could transform how enterprises think about X", "promising direction", "valuable insights", "opens up possibilities" — anything that would still be true if you deleted it. If, after trying, you can't name a concrete change a business would make because of this paper, say that plainly (e.g. "primarily a methodology contribution, no direct operational change") rather than papering over the gap with generic enthusiasm. Every "why it matters" and "business application" line should pass this test: could a reader repeat it back as a specific decision or action, not a mood.

2. **Review one paper at a time.** For each paper: put everything the reviewer needs into a single widget (via the `visualize` elicitation pattern) — the summary content (title, headline, key highlights, why it matters, business applications, recommended audience) *and* the decision controls together in one card, not split between response text and widget. Include:
   - All 5 quantitative dimension scores from `papers/metadata/scores/<id>.yaml` (grouped by rubric section — Substance, Business Fit — matching [[editorial-triage]]'s Sections B-C), each as an adjustable control pre-filled with its current 1-5 value, so the reviewer can correct a specific dimension without needing to re-litigate the whole recommendation
   - A single-select choice: **Approve** / **Archive** / **Ignore** (Archive = on-topic but not worth acting on now; Ignore = doesn't deserve attention — same distinction editorial-triage already uses, never default one silently over the other)
   - An optional free-text field for a reason, especially useful on Archive/Ignore or on any dimension adjustment

   Wait for the response before moving to the next paper — don't queue multiple widgets at once.

3. **Apply the batch.** Once you have a decision (optional note, optional score adjustments) for each paper reviewed this session, write a batch JSON and run:
   ```bash
   python skills/editorial-review/scripts/apply_human_review.py <batch.json>
   ```
   - `approve`: marks `human_reviewed: true` on the paper's metadata; changes nothing about its recommendation, status, or eligibility unless `score_adjustments` are also given.
   - `archive` / `ignore`: overwrites the paper's `recommendation` to `Archive`/`Ignore`, recomputes `status`/`download_eligible`/`extract_eligible` from `config/editorial-profile.yaml`'s `screening.recommendations` (same logic `apply_scores.py` uses), and preserves the original call as `pre_override_recommendation` on the score record so the override is traceable, not silent.
   - `score_adjustments` (optional on any decision): a `{dimension: new_value}` map correcting specific 1-5 scores. Every adjustment is recorded as a from/to pair under `human_score_adjustments` on the score record (cumulative history, never overwritten), and `overall_score` is recomputed as the sum of all 5 dimensions, exactly as `apply_scores.py` computes it.
   - Every decision logs an entry to `logs/feedback.jsonl` (rated `Good` for approve, `Ignore` for archive/ignore), with any score adjustments folded into the note so a recurring pattern ("humans keep correcting `business_translatability` upward") is visible to [[editorial-strategist]]'s later analysis.

4. Report which papers were approved, archived, or ignored, and remind the user that [[editorial-strategist]] can analyze the accumulated `logs/feedback.jsonl` entries later to propose profile changes — this skill only feeds that pipeline, it never edits `config/editorial-profile.yaml` itself.

5. Optionally re-run `python skills/research-librarian/scripts/build_index.py` afterward so `papers.csv` reflects any overrides immediately rather than waiting for the next scheduled run.

## Why feedback goes through editorial-strategist, not a direct config edit

Per this repo's editorial-profile change-control rule, only [[editorial-strategist]] proposes changes to `config/editorial-profile.yaml`, and only a human applies them by hand. A discard here is a data point (one paper, one reason) — it is not, by itself, evidence that a scoring dimension or topic list needs to change. Appending to `logs/feedback.jsonl` in editorial-strategist's existing schema lets that skill aggregate patterns across many discards before proposing anything, rather than one disagreement silently reshaping the model.

## What this skill does not do

No new scoring, no full-text reading, no editing `config/editorial-profile.yaml`. It does not touch papers that are past the extraction checkpoint — see [[knowledge-extraction]] and [[editorial-strategist]] for those.

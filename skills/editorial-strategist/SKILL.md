---
name: editorial-strategist
description: Learn from feedback on past papers and propose changes to the editorial profile. Use this skill when the user rates a paper (excellent/good/average/ignore), asks what's working in the selection model, asks whether the editorial profile should change, or asks to review recent picks. Never edits editorial-profile.yaml directly — it only proposes. Trigger on phrases like "that paper was excellent", "mark this as average", "how's our editorial model doing", "should we adjust the topics", "review the last month's picks".
---

# Editorial Strategist

## Purpose

Continuously improve the editorial selection model. Instead of asking "is this a good paper?", ask **"is this worth my time?"** — the same reframe that drives [[editorial-triage]].

## Authority

This skill proposes only. It never writes to `../../config/editorial-profile.yaml`. Every recommendation is a suggestion the user (or a separate explicit request) applies by hand — this keeps the editorial profile change-controlled rather than silently drifting run to run.

## Capturing feedback

When the user reacts to a paper they've read — "that Priority review paper was actually mediocre," "great pick, more like this" — record it rather than letting it evaporate into the conversation. Append one line to `../../logs/feedback.jsonl`:

```json
{"arxiv_id": "2507.12345", "rating": "Excellent", "note": "concrete eval methodology, used it directly", "date": "2026-07-27"}
```

Ratings: `Excellent`, `Good`, `Average`, `Ignore` — matching the four-tier scale in the original brief, distinct from [[editorial-triage]]'s five-tier recommendation. This is retrospective (was the pick actually good, in hindsight) versus triage's prospective score (does the abstract look promising).

If the user gives feedback without naming a paper explicitly, ask which one rather than guessing from recent conversation.

## Analysis

When asked to review the model, or periodically (e.g. monthly), cross-reference:

- `../../logs/feedback.jsonl` ratings against each paper's tags/concepts (from `../../ArxivWiki/papers/**/*.md` front matter) and original triage scores (`../../papers/metadata/scores/*.yaml`) — which topics correlate with `Excellent`/`Good` feedback versus `Average`/`Ignore`?
- `../../papers/papers.csv`'s `LinkedIn written` column against tags/scores — what do papers that actually became content have in common? High `linkedin_potential` or `business_implication` alone, or a specific topic cluster?
- Papers `status: "ignored"` at triage — do enough of them share a topic that keeps recurring in feedback as something the user wishes they'd seen, suggesting a `priority_topics` gap rather than a correct exclusion?
- Author and venue patterns across `Excellent`-rated papers — is there a small set of labs/authors worth tracking explicitly, even though the config doesn't currently have an `authors_to_watch` list?

## Recommend

Produce concrete, scoped suggestions, not vague direction:

- New or reweighted `priority_topics` / `secondary_topics` entries, or additions to `screening.enterprise_ai_themes` / `screening.business_functions`
- Categories to add or drop from `discovery.categories`
- Adjustments to `weekly_limit`, `download_top_n`, or the `screening.recommendations` gate mapping itself if the volume reaching each tier is clearly miscalibrated (e.g. nothing ever reaches Priority review, or the extraction queue is permanently backlogged)
- Emerging topics not yet represented in either topic list, evidenced by specific papers

Every recommendation must cite the evidence (which papers, how many, what pattern) — a suggestion with no supporting data is a guess, not a strategy.

## Output

Write the proposal to `../../logs/strategist-proposal-<date>.md`:

```markdown
# Editorial profile proposal — <date>

## Observed pattern
<what the data shows, with paper references>

## Proposed change
<exact diff-style change to editorial-profile.yaml>

## Why
<link back to the observed pattern>
```

Then present it to the user in the conversation and ask whether to apply it. If they say yes, that's the one moment this skill's output leads to a real edit — but the edit itself is a normal, explicit file change the user approved in this turn, not something the skill does autonomously on a schedule.

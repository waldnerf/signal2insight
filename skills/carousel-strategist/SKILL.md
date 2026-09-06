---
name: carousel-strategist
description: Learn from accumulated carousel review and revision feedback, and propose changes to writing-standards.md. Use when the user asks whether the carousel process is improving, what keeps getting corrected across decks, or whether writing-standards.md should change. Never edits writing-standards.md directly, it only proposes. Trigger on phrases like "how's the carousel process doing", "what keeps getting corrected", "should we update the writing standards", "review the last few decks".
---

# Carousel Strategist

## Purpose

Continuously improve `../carousel-production/writing-standards.md`, the same reframe [[editorial-strategist]] applies to the editorial profile: not "was this deck good," but "is the standard producing decks that don't need this correction again."

This is deliberately the only place in `carousel-production` that looks across decks instead of at one. `carousel-writer`, both reviewers, and `carousel-designer` all work within a single run; this skill is what turns a pattern repeating across several runs into a standing rule, instead of a correction that has to be relearned by hand every time.

## Authority

This skill proposes only. It never writes to `../carousel-production/writing-standards.md`. Every recommendation is a suggestion the user applies by hand, or approves explicitly in the conversation, the same change control [[editorial-strategist]] holds `editorial-profile.yaml` to, and for the same reason: writing-standards.md is what `carousel-writer`, both reviewers, and `check_standards.py` all read, so a silent drift there would silently reshape every future deck.

## Where the feedback comes from

`../../logs/carousel-feedback.jsonl`, one entry per revision or approval decision on a draft, written by `../carousel-production/scripts/log_carousel_feedback.py`:

```json
{"arxiv_id": "2608.23642", "revision": 1, "decision": "revise", "note": "Franz: slide bodies read as analyst-memo paragraphs, not carousel copy; wanted short declarative lines, one idea per line, minimal connective tissue.", "date": "2026-09-04"}
```

`decision` is `approve`, `revise`, or `reject`. Every forced revision pass gets logged, not only the final outcome, because a correction that recurs across decks is the actual signal, a single revised deck is not.

## A sample-size floor before this runs for real

A strategist proposal is only as good as the pattern behind it. One deck's feedback is a single data point, not a pattern, the same caution [[editorial-strategist]] would apply with too few `logs/feedback.jsonl` entries. Do not produce a proposal from fewer than **five decks' worth of decisions** in `carousel-feedback.jsonl`. Below that floor, if asked to review the process, say so directly and summarise what's been logged so far rather than manufacturing a rule from one correction.

## Analysis

When asked to review the process, or once the floor above is cleared:

- Group `carousel-feedback.jsonl` entries by the kind of correction (voice/register, content selection, sourcing, structure, framework choice), not just by arxiv_id. A correction that recurs across unrelated decks is a standing-rule candidate; a correction that shows up once is that deck's problem, not the standard's.
- Cross-reference against `check_standards.py` and `check_brief.py` output where available: if a correction is something the linter already catches (an em dash, a banned phrase), that is a writer-compliance problem, not a standards gap, and does not belong in a proposal here.
- Read the actual before/after on a few decks where the correction landed (`_history/rev-NN.md` against the approved draft) so the proposal can cite the specific change, not just paraphrase the note.

## Recommend

Produce concrete, scoped suggestions, not vague direction:

- A new rule or worked example added to `writing-standards.md`, in its own voice and format, not a summary of the feedback
- A tightening or loosening of an existing rule (word ceiling, depth pattern guidance, the negation rule) where decks keep landing on one side of it
- A default changed (which depth pattern gets suggested first, the default slide count) where one option keeps winning
- Removal of a rule nothing has ever corrected against, if one has clearly stopped mattering

Every recommendation must cite the evidence, which decks, how many times, in what words, the same evidentiary bar [[editorial-strategist]] holds itself to.

## Output

Write the proposal to `../../logs/carousel-strategist-proposal-<date>.md`:

```markdown
# Writing standards proposal — <date>

## Observed pattern
<what the feedback log shows, with deck references>

## Proposed change
<exact diff-style change to writing-standards.md>

## Why
<link back to the observed pattern>
```

Then present it to the user in the conversation and ask whether to apply it. If they say yes, that is the one moment this skill's output leads to a real edit, and the edit itself is a normal, explicit change the user approved in that turn, not something applied on a schedule.

## What this skill does not do

No per-deck judgment about a specific carousel's copy, structure, or framework choice, that is `carousel-writer`'s job within a run. No editing of `writing-standards.md`. No involvement in the LinkedIn post caption's content, that is [[carousel-production]]'s post-writer step, a per-deck authoring job, not a cross-deck calibration one.

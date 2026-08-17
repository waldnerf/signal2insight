# Review log · 2607.29433

One row per review pass. Scores are 1-5 per dimension. Primary dimensions are
`B1 so-what` and `T1 mechanism`, gated at 4; every other dimension floors at 3;
each subtotal bars at 19/25. See "The loop" in `skills/carousel-production/SKILL.md`.

| pass | rev | B1 | B2 | B3 | B4 | B5 | Bsub | T1 | T2 | T3 | T4 | T5 | Tsub | blk | wrong | maj | over | unver | min | gate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 4 | 3 | 3 | 5 | 4 | 19 | 5 | 3 | 4 | 3 | 4 | 19 | 0 | 0 | 3 | 3 | 1 | 5 | PROCEED |
| 2 | 3 | 5 | 5 | 3 | 5 | 4 | 22 | 4 | 2 | 3 | 2 | 3 | 14 | 0 | 2 | 1 | 1 | 2 | 5 | PROCEED (cap) |
| 3 | 4 | 5 | 5 | 4 | 5 | 4 | 23 | 5 | 4 | 4 | 3 | 5 | 21 | 0 | 2 | 2 | 2 | 0 | 5 | LOOP |
| 4 | 5 | 5 | 4 | 4 | 5 | 4 | 22 | 5 | 4 | 5 | 3 | 3 | 20 | 0 | 1 | 3 | 0 | 0 | 3 | LOOP |
| 5 | 6 | 5 | 4 | 4 | 5 | 5 | 23 | 5 | 4 | 3 | 4 | 5 | 21 | 0 | 1 | 2 | 1 | 0 | 8 | PROCEED (cap) |

## Pass 1 notes

Both subtotals landed exactly on the 19/25 bar, so the gate passes on its
margin rather than comfortably. Worth remembering when the thresholds get
recalibrated: this deck is the first data point, and "exactly at the bar"
described a deck with a real scope-slippage problem on slide 9.

Revision 1 was never reviewed. It was written from a truncated source file,
before the extractor bug that dropped introductions and related-work sections
was found and fixed. Reviewing it would have scored the bug rather than the deck.

Highest-value finding: `carousel-reviewer-technical` on slide 9, where a
Mem0-only failure decomposition is restated without the scope caveat that
slide 8 carries, next to a pull-quote drawn from a different analysis using a
different definition of "storage failure". Neither reviewer could have found
this from the summary alone; it needed the paper's own section structure, which
is the argument for `papers/text/` existing.

Both reviewers independently flagged slide 4's "at three levels of expression
strength" and the deck's handling of scope, from opposite directions:
accessibility (term undefined until slide 7) and precision (the outlier system
is not flagged). That convergence is the roster working as intended.

## Revision 3 · accuracy fixes, written in the main thread

**Deviation from the roster, recorded deliberately.** `carousel-writer` was
spawned for this pass and died on a session limit before writing anything. The
four fixes were made in the main thread instead. That breaks the rule that the
writer owns copy, and the copy therefore did not pass through the writer's
brief. Revision 3 has been linted clean but **has not been reviewed**, so its
scores are unknown and the 19/25 in the row above describes revision 2.

Fixed, all from the technical review:

1. Slide 10, the fabricated category. "Lifestyle preferences fare best" was
   removed entirely. Verified against the source: the paper's five types are
   stereotypical, anti-stereotypical, neutral, health/medical and
   therapy/emotional, and "lifestyle" occurs exactly once, in a passing
   contrast, never as a scored category. The paper ranks the two worst and
   never names a best, so no replacement ranking was substituted. The
   reasoning contrast (domain knowledge versus common sense) survives in the
   paragraph below the bullets, where it rests on no score claim.
2. Slide 9, scope. The failure decomposition now opens by stating it came from
   a single system on its own recall-passed cases.
3. Slide 9, the misplaced quote. The expression-strength finding is now framed
   as a separate benchmark-wide analysis, and the quote's attribution line says
   so, rather than sitting where it read as a summary of the single-system
   table above it.
4. Synthetic data. Now stated plainly in both layers: in the business list at
   point 2, where it bears on whether the numbers transfer, and in the
   technical note as the limitation the measurement states about itself.

**This severity call is the one to revisit.** Finding 1 was filed `overstated`
and it reads as `wrong`: a category that does not exist in the paper was
presented with a result attached. Had it been filed `wrong`, the gate would
have looped and this deck would not have reached the user. The gate behaved
correctly given its input; the input was graded a notch too kindly.

## Pass 2 · blind re-review of revision 3

Fresh reviewer instances. Prior scores, prior findings and the list of what had
been changed were all withheld, so the comparison measures the deck rather than
measuring agreement with an earlier pass.

Business **19 to 22**. Arc 3 to 5 and so-what 4 to 5. Removing the fabricated
category and adding the synthetic-data caveat visibly helped the commercial read.

Technical **19 to 14**, with two `wrong`. **The repair introduced a worse defect
than the one it fixed.**

Slide 9's original problem was a real scope slippage. The fix asserted that the
expression-strength breakdown was "a separate analysis, run across the whole
benchmark rather than on one system." That is false. Table 2 is captioned as
Mem0's Know-Pass x Act-Fail cases (n=722); the expression rows are the same
single-system oracle study sliced differently. No whole-benchmark
retrieval/comprehension analysis exists in the paper at all. The fix took a
slide that under-scoped a result and turned it into one that over-scoped the
same result, then attached a correctly-sourced quote from a genuinely different
analysis as though it corroborated the invented one.

Pass 1 had also missed slide 4's "about two-thirds", which is framed as the
Explicit-condition figure but is actually the macro-average across all three
conditions, off by roughly 17 points against Table 1.

**What this run establishes, and it is the useful output of the whole exercise:**

1. **Blind re-review works and is worth its cost.** Handing the reviewer a list
   of fixes would have produced confirmation. Withholding it produced a caught
   regression.
2. **A reviewer is not a substitute for the writer.** The repair was made in the
   main thread because `carousel-writer` had died on a session limit. It was
   linted clean and it was wrong. The linter cannot see a claim that misstates
   the paper, which is the entire argument for the roster.
3. **Scores move for real reasons.** 19/19 to 22/14 on one revision is a wide
   swing in opposite directions, which is evidence the dimensions discriminate
   rather than drifting upward with familiarity.
4. **The pass cap is the binding constraint, not the score bar.** The gate
   reports PROCEED only because three passes are spent. On its merits this deck
   fails four ways.

## Budget reset, granted by the user

`pass_reset_at: 3` set in the draft frontmatter, granting three fresh writer
passes from revision 4. `revision` is left untouched.

Granted because the deck fails on **defects introduced by the repair, not on
the source material**. The cap exists to surface a paper or a depth pattern
that cannot carry a deck, and that is not the situation here: the business axis
scores 22/25, and both `wrong` findings name an exact sentence and an exact
table. This is a fixable deck that lost a pass to a main-thread repair made
while `carousel-writer` was unavailable.

Alongside the reset, the severity boundary that let pass 1 through was tightened
in `.claude/agents/carousel-reviewer-technical.md`, and the matching writing
rule was added to `writing-standards.md` as "Scope travels with the number".
A misstated population and an invented category are now both `wrong` by
definition rather than by a reviewer's judgment. Under the old wording this
deck's two most serious findings could each have been filed `overstated`,
which is exactly how it reached the user the first time.

## Pass 3 · blind re-review of revision 4

Business **22 to 23**, technical **14 to 21**. Both revision-3 `wrong` findings
are repaired and verified gone. `T5 depth-pattern` reached 5 once the ratio
language left the technical notes, and `T2 fidelity` recovered 2 to 4.

Still LOOP, on two `wrong` and nothing else. Every dimension clears its floor
and both subtotals clear the bar comfortably.

**The tightened severity rule is doing exactly what it was added for.** Both new
`wrong` findings are far finer than the ones it caught last pass, and the
reviewer cites the new rule by name for one of them ("Per the standard's 'scope
travels with the number' rule, this is treated as wrong rather than
overstated"). Under the old wording both would have been `overstated` and the
deck would have shipped. They are:

1. Slide 7's quote attributed "across all 16 systems" where section 4.3 says
   "architectures", which is the five-category taxonomy in Figure 3 rather than
   the 16 rows of Table 1. A widened attribution, not a widened number.
2. Slide 9 using "stated outright" twice, three lines apart, for two different
   populations: the oracle-preference bypass condition, and Table 2's Explicit
   expression subgroup. Same phrase, same slide, different referents.

Both are wording collisions rather than false claims. That is a different and
much cheaper class of defect than pass 2's inverted scope, and it is the shape
a deck takes when it is nearly right.

**Open standards question, raised by the business reviewer and not adjudicated.**
The deck's load-bearing figure, "about two-thirds", is structurally identical
to the example `writing-standards.md` gives for the outcome-figures rule. The
standard bars outcome figures without distinguishing a vendor's ROI claim from
a benchmark's critical finding. The reviewer correctly declined to decide it.
This is a real gap in the standard rather than a defect in the deck, and it
needs a human ruling before the next deck inherits the same ambiguity.

Resolved before pass 4. The outcome-figures rule was rewritten: promotional
figures stay out, a source's own headline finding stays in. Test is what the
figure does, not whether it is a number. "About two-thirds" stays.

## Pass 4 · blind re-review of revision 5

Business **23 to 22**, technical **21 to 20**. Both dipped, and the two causes
are worth separating because only one is a defect in the deck.

**The new sourcing rule fixed one problem and created another.** Requiring a
source for slide 2's unsourced magnitude claim did what it should: the writer
searched, found NBER working paper 34255, and verified publisher, number, year,
sample and both figures. Every one checks out. But the source measures **one
product**, and the deck's prose widened it to "consumer assistant
conversations", which is the whole category. That is a `wrong` under the very
scope rule added two passes earlier: a citation makes the sentence look
rigorous while the population it supports is narrower than the claim.

It also produced a second-order defect the business reviewer caught. Slide 7's
"what your customers reveal in passing is the bulk of what they reveal" now
quietly borrows weight from those NBER figures, which measure a different
population entirely. An external figure introduced to fix one slide leaked
support into an unrelated claim two slides later.

**T5 fell 5 to 3 on an ambiguity in the standard, not on the deck.** The
dual-track row's column header says "Numeric thresholds" and its cell says
"keep numbers out". Those are different rules. The reviewer applied the cell
literally and flagged counts like "1,000 recall questions", "three human
annotators" and "722 cases" as leakage. Under the header reading, none of those
is a threshold and none is a defect. Two points of the drop trace to wording I
wrote, and a ruling is needed before another deck inherits it.

**Method note.** Churn checking was added this pass and reports honestly that
it has no baseline. Revision 5 is the first snapshot, so from revision 6 it can
show which slides changed without a finding behind them, and which findings
drew no change.

## Engine change, before pass 5

`dual-track` was redefined. Every resolution slide previously carried a
labelled *For the business* note and a labelled *Under the hood* note; that
visible seam is gone. Slides now write one blended passage, mechanism and
consequence sharing a paragraph with no header marking the switch, ending on
the takeaway. `writing-standards.md`, `SKILL.md`, `carousel-writer.md` and
both reviewer briefs were updated to match, and `check_standards.py` now
lints a 100-word target / 120-word hard ceiling per slide body under this
pattern. None of this touched the draft itself; it changed what the next
writer pass would be asked to do.

## Pass 5 · combined format rewrite and blind re-review of revision 6

`carousel-writer` rewrote all eleven resolution slides to the blended format
in the same pass as the six accuracy and wording fixes queued from pass 4
(slide 2's NBER scope, slide 7's unearned "bulk" claim, slide 8's jargon
title, the "memory layer" terminology seam, and two minor clarity fixes).
Doing both together in one pass was deliberate: the format change touches
every slide's body regardless, so a second full pass to apply fixes
separately would have cost a pass for no isolation benefit. Slide 12 was
left untouched, correctly: it never carried the split and drew no finding.

Business **22 to 23**, technical **20 to 21**. Both subtotals hold or
improve. The `wrong` count is unchanged at 1, but it is a **new** defect, not
the same one carried forward: slide 2's population scope (ChatGPT-only vs.
"consumer assistant conversations") is fixed, and in fixing it the writer
introduced a different error in the same sentence, the "about one in ten"
personal-expression figure, which independent accounts of the same NBER
source put at roughly 2.4-5.3 percent rather than the ~10 percent the slide
states. The citation is correctly named and dated; the number under it is
wrong. This is the same failure shape as pass 2's slide 9 regression: a
targeted fix on one axis (scope) introduced a defect on another (magnitude)
in the same sentence.

The business reviewer's "seam" check, added to the brief specifically to
catch leftover visible splits, found one real instance on slide 6: a run of
pure test-methodology sentences followed by a consequence sentence that does
not follow from what precedes it. Slide 7 was flagged separately for closing
on a restated finding rather than a stated business consequence. Neither is
a seam in the literal for-business/under-the-hood sense; both are the softer
version the new rule was written to catch, a passage that reads as two ideas
stitched together even without headers.

**Gate result: PROCEED (cap), not LOOP.** The `wrong` finding would mandate
another pass on its own, but this is the third pass since the last budget
reset (`pass_reset_at: 3`, revision now 6), so the cap binds first. Per
`SKILL.md`, that means taking the deck to the user with the open finding and
a read on the cause, not spending a fourth pass. The underlying cause here
is not the source or the depth pattern (both score well: T1 mechanism 5/5,
T5 depth-pattern 5/5) — it is that this pass asked the writer to do two
different things in the same slide bodies (reformat and re-verify a figure)
under a tight word ceiling, and the figure-level check did not fully hold
under that combined load.

**Open, for the user:** slide 2's personal-expression figure needs a
correction or removal before this deck ships. Everything else scored this
pass is a minor or a majors count below the loop threshold on its own.

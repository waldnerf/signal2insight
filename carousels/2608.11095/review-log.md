# Review log · 2608.11095

One row per review pass. Scores are 1-5 per dimension. Primary dimensions are
`B1 so-what` and `T1 mechanism`, gated at 4; every other dimension floors at
3; each subtotal bars at 19/25. See "The loop" in `skills/carousel-production/SKILL.md`.

| pass | rev | B1 | B2 | B3 | B4 | B5 | Bsub | T1 | T2 | T3 | T4 | T5 | Tsub | blk | wrong | maj | over | unver | min | gate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 3 | 3 | 2 | 4 | 15 | 3 | 2 | 3 | 2 | 4 | 14 | 1 | 5 | 7 | 7 | 0 | 4 | LOOP |
| 2 | 1 | 4 | 4 | 2 | 3 | 4 | 17 | 5 | 3 | 4 | 4 | 4 | 20 | 1 | 1 | 4 | 2 | 0 | 4 | LOOP |

## Pass 1 notes (revision 0, first review)

First review of the deck I wrote directly with Franz through the storyline and
copy iteration in the main thread, rather than a fresh carousel-writer draft.
The business reviewer's first attempt failed on an API/SSL error and was
relaunched cleanly at Franz's request; the retry completed normally.

Both reviewers failed the gate hard, on different grounds. Technical found
five `wrong` findings, all overstatement of what the paper's numbers actually
measure:

1. Slide 2, wrong. "A maintainer deletes everything in one pass" overstates
   a rewrite, which the paper defines as killing >=50% of live instructions
   (median: kills 46, births 14 in the same commit); only 24.4% of rewrites
   empty the file.
2. Slide 7, wrong. The title's >99% figure (T=51, 1 seed, 184 worlds) and the
   body's "60% or more... over the same steps" (T=15, 3 seeds, 552
   histories) are two different experimental conditions presented as one
   measurement.
3. Slides 1 and 8, wrong. The 23% real-world performance figure is a
   recovery from artificially seeded distractor instructions (D=16), not a
   general real-world gain. The paper states explicitly that a prompt with
   no extraneous instructions is "outside the scope of this experiment,"
   and both slides omit that scoping entirely.
4. Slide 9, wrong. "Roughly quadruples" (Haiku 4.5 to Opus 5) uses the raw
   size ratio (1.68 to 6.72, exactly 4x) rather than the paper's own
   excess-size definition (ratio minus one, as a percentage), which gives
   roughly 8.4x, not 4x.

Technical also filed seven `overstated` findings, several a repeat of the
same pattern: instruction *count* growth (+226%) described as *size* growth
(the paper separately tracks total size at +140% specifically to rule out
that conflation); "247,694 instructions" for what the source calls
"247,694 instruction lifetimes" (a derived, matched object, not a raw
count); "299,440 tracked file versions" for what the source calls
"299,440 version-to-version transitions"; a redundancy mechanism (two
instructions independently covering one constraint) described as a
dependency ("no other instruction quietly depends on it"); Cursor named
as covered when the paper's corpus and Limitations section scope only to
CLAUDE.md/AGENTS.md/copilot-instructions.md repositories; and the >99%
headline given without its single-seed caveat, next to a result (T=15)
the paper does replicate across three seeds.

One thing technical confirmed rather than flagged: slide 10's pull quote
is verbatim. The linter's WARN is a false positive caused by a PDF
line-wrap artifact (a missing space in "nothingand") consistent with two
other missing spaces in the same source paragraph.

Business found no wrong/overstated findings but filed a blocker and seven
majors, mostly structural: the closing slide (11) ends on an instruction
rather than a question, which the standard requires; slides 6, 7 and 8
each end their body on a mechanism or evidence detail rather than a stated
business consequence, three resolution slides in a row; slides 2 and 3's
titles read as fragment lists rather than single claims; slides 1, 7 and 8
restate the same two headline numbers as titles, which the business
reviewer read as flattening the arc's momentum; and slide 1's "tripling...
across 1,867 repositories" appeared to conflict with slide 2's figure note
citing a six-repository illustration, which the reviewer flagged as an
apparent population mismatch for the technical pass to adjudicate (folded
into the count-vs-size overstatement above).

Fixes queued for pass 2:

1. Slide 1 and 8, wrong. Scope the 23% figure to what it actually measures:
   recovery of instruction-following on prompts seeded with distractor
   instructions, not a general real-world performance claim.
2. Slide 2, wrong. Replace "deletes everything in one pass" with language
   matching the paper's >=50% rewrite definition and its own median
   (46 killed, 14 born), not a full wipe.
3. Slide 7, wrong. Separate the T=15 (60.4% to -5.8%, 3 seeds) and T=51
   (211.3% to 1.4%, 1 seed) results rather than presenting them as one
   measurement "over the same steps." Keep the T=51 figure as the >99%
   headline but caveat the single seed, and use the T=15 figure (with its
   three-seed replication) for the body's comparison claim.
4. Slide 9, wrong. Recompute the capability-compounding claim against the
   paper's own excess-size definition (ratio minus one), or state plainly
   that the raw size ratio is what is being quoted.
5. Slide 1 and 2, overstated. Distinguish instruction count (+226%) from
   total prompt size (+140%) throughout; do not call count growth "size."
6. Slide 3, overstated. "Instruction lifetimes," not "instructions"; "version-
   to-version transitions," not "file versions."
7. Slide 5, overstated. Redundant coverage, not dependency, is the
   mechanism; reword away from "depends on it."
8. Slide 11, overstated. Drop Cursor, the paper's corpus is CLAUDE.md/
   AGENTS.md/copilot-instructions.md repositories only.
9. Slide 4, minor (both reviewers). Replace "the paper tests" with named
   attribution per house style.
10. Slide 11, blocker. Close on a question the reader can answer from their
    own situation, not an instruction.
11. Slides 6, 7, 8, major. Land each resolution-stage body on a stated
    business consequence, not a mechanism step or an evidence number.
12. Slides 2, 3, major. Rewrite as single asserted claims rather than
    fragment lists.
13. Slides 1, 7, 8, major. Consider whether restating the same two headline
    numbers as later titles still serves the arc now that slide 1 states
    them upfront by design (pyramid structure, Franz's explicit choice);
    if kept, make clear each later slide adds evidence rather than just
    repeating the number.
14. Slide 1, minor. Gloss "CLAUDE.md" faster for a reader meeting it cold.

## Pass 2 notes (revision 1, after a mechanical word-count trim)

After pass 1's rework, every slide body was trimmed by hand (not via
carousel-writer) from 100-122 words down to 40-80, to hit Franz's explicit
40-50/80 word budget that pass 1's accuracy fixes had blown past. Two
regressions caught before review: the trim had cut slide 7's and slide 9's
closing consequence sentences, which pass 1 added specifically to fix a
business "ends on evidence, not a takeaway" finding. Both were restored
before this review round, so `revision` stayed at 1 rather than
incrementing, since no new writer pass occurred, only compression plus
those two restorations.

The technical reviewer's first attempt at this pass stalled (no progress
for 600s) and was relaunched with an instruction to keep the read
efficient, which completed cleanly.

Both reviewers improved on pass 1 (business 15 to 17/25, technical 14 to
20/25) but the gate still says LOOP. Business filed one new blocker
concentrated entirely on slide 1: the trim left "record why an instruction
was added, when it is added" reading as a stutter, and left three
undefined terms (51-step run, excess instructions, 16 distractors) landing
in the deck's very first slide with no prior context to anchor them. That
is a direct cost of the trim itself, not a fact-accuracy problem: pass 1's
untrimmed slide 1 did not have this issue.

Technical filed one new `wrong`: slide 2's "77.3%" is the paper's combined
rewrite-plus-migration figure, not the wholesale-rewrite-only figure the
slide's own sentence names, which is 76.8%. This survived pass 1 and the
trim untouched, so it was not introduced by either fix pass, it was wrong
from the first draft and neither review caught it until now. Two
`overstated` findings are new: slide 8's "confirmed by a second judge"
overstates what Appendix D.3 actually shows (the second judge confirmed
direction and significance at a smaller point estimate, 7.8pp vs 11.6pp,
not the specific magnitude); and slide 7's "at equal satisfaction" omits
that the comments arm empties the prompt entirely on 12.1% of worlds and
scores worst of the three arms specifically on those emptied worlds
(Appendix C.5) -- the same finding the business reviewer flagged from the
readability side, confirmed here as a real scoping gap, not just an
awkward sentence.

Fixes queued for pass 3:

1. Slide 1, blocker. Fix "added, when it is added" and give the 51-step
   run / excess instructions / 16 distractors enough of a gloss that a
   cold reader can judge whether 99.3%/23.1% are impressive, without
   reintroducing the word-count blowout pass 1 caused. This is the
   highest-priority fix: it is the deck's first blocker on the opening
   slide.
2. Slide 2, wrong. Change 77.3% to 76.8% (wholesale rewrites alone), or
   reword to "rewrites and migrations combined" if 77.3% is kept.
3. Slide 7, overstated. Either drop "at equal satisfaction" or qualify it:
   parity holds where the protocol keeps instructions, and the protocol's
   own emptied-prompt worlds (12.1% of them) are where it scores worst of
   the three arms, not best. This is the same finding business raised as a
   comprehension problem and technical confirmed as a real gap.
4. Slide 8, overstated. "Confirmed by a second judge" should say what was
   actually confirmed: the direction and significance, at a smaller point
   estimate (7.8pp vs. 11.6pp), not the 11.6pp/23.1% figure itself.
5. Slide 3, minor. Note that 4.9 net instructions/commit excludes mass
   rewrites, or drop "on average" since it is not an unconditional average.
6. Slide 3, major (business). Seven figures in ~70 words reads as a table
   in prose; cut to the two or three numbers the slide actually needs.
7. Slide 4, major (business). Define "fragility" in-line, at least as
   briefly as "staleness" already is.
8. Slide 1 vs 9, major (business). The deck's two headline numbers
   (99.3%, 23.1%) get no hedge on slide 1, while a comparable single-run
   result gets an explicit hedge on slide 9. Consider whether slide 1
   needs a light caveat, or whether the asymmetry is acceptable because
   slide 9 is a different (capability-scaling) result.
9. Slide 2, minor (business). Six figures in ~65 words; not blocking, but
   tighten if slide 3's rework leaves a pattern to match.
10. Slide 9, minor (business). "The raw ratio rather than excess above
    minimum" reads as an orphaned footnote after the trim; restore a
    clause that frames why the distinction matters, or cut it if slide 7
    no longer needs the contrast once its own wording changes.
11. Slide 10, minor (business). "safety relevant" needs a hyphen.

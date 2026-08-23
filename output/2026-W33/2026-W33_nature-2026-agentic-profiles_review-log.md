# Review log · nature-2026-agentic-profiles

One row per review pass. Scores are 1-5 per dimension. Primary dimensions are
`B1 so-what` and `T1 mechanism`, gated at 4; every other dimension floors at 3;
each subtotal bars at 19/25. See "The loop" in `skills/carousel-production/SKILL.md`.

| pass | rev | B1 | B2 | B3 | B4 | B5 | Bsub | T1 | T2 | T3 | T4 | T5 | Tsub | blk | wrong | maj | over | unver | min | gate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 4 | 4 | 3 | 5 | 5 | 21 | 5 | 4 | 4 | 3 | 5 | 21 | 0 | 1 | 4 | 1 | 0 | 3 | REWORK |
| 2 | 1 | 4 | 4 | 3 | 5 | 5 | 21 | 5 | 3 | 4 | 4 | 5 | 21 | 0 | 0 | 4 | 2 | 0 | 6 | SUPERSEDED |

## Pass 2 notes

Business re-review of revision 1 landed clean: no blockers, no wrong, no
overstated -- both pass-1 accuracy fixes (slide 2's scope, slide 10's caveat
sequencing) held. Remaining friction was readability, concentrated on slide
10 (dense multi-system comparison, one unparseable phrase) and a weak close
on slide 7. Technical re-review of revision 1 was still running when Franz
read the deck directly and gave structural feedback: stay closer to the
paper, one dedicated slide per dimension, a dedicated framework slide, and
multiple dedicated governance-implication slides (rather than compressing
framework, four dimensions, and governance implications into the same
~12-slide dual-track budget). That supersedes the dual-track structure this
review pass was scoring, so the technical re-review is not being waited on
and this row's technical columns are left blank. Revision 2 is a structural
rewrite per that direction, not a fix pass on revision 1 -- see the writer's
brief for what carries forward from both review rounds.

Technical re-review of revision 1 landed after the structural redirect was
already confirmed. Both reports are persisted for the record (see
`review-technical.md`). Two findings carry forward regardless of structure:
slide 4's "more agentic... more governance" pull-quote should not float
isolated (the negating lead-in is real -- confirmed against the raw
pre-cleanup extraction -- but severed from the quote by the page-order
artifact, so the rejection needs to be unmistakable in prose rather than
implied by an isolated fragment); and slide 10's "the four scores move
independently" overstates what the paper itself hedges ("dimensions can
correlate or compound," goal complexity and generality "often coincide").

| 3 | 2 | 5 | 5 | 3 | 5 | 5 | 23 | 5 | 3 | 4 | 4 | 3 | 19 | 0 | 1 | 3 | 1 | 2 | 6 | REWORK |

## Pass 3 notes (revision 2, first review of the restructure)

Both reviewers treated this as a first pass on new material (13 slides,
`depth_pattern: spec-cards`), full reads rather than churn-scoped. The
technical reviewer's agent stalled once and was relaunched cleanly.

Business landed strong: 23/25, no blockers/wrong/overstated, and named the
restructure's core strength explicitly -- every resolution slide lands an
explicit governance so-what, which the dual-track version didn't consistently
do. Three majors, all readability: slide 7's efficacy grid asserts E.0-E.5
without showing the rule that crosses the two axes; slide 11's table row 2
is the only row with no dimension label; slide 5 (the framework thesis slide)
stacks five sub-topics into one slide and will cost real reading time.

Technical found one `wrong`: slide 5 claims three properties (not two)
appear in all seven surveyed definitions. The paper is precise per-property --
autonomy "a key property of all definitions", efficacy "found in each
definition", but goal complexity only "a third common element across
different definitions", never "all"/"each", and the paper's own supporting
quotes for goal-directedness skip D.1 (Russell and Norvig). The deck's own
generality clause two slides later gets this kind of distinction right,
which makes the slide 5 error harder to excuse. One `overstated`: slide 12
contradicts itself within two sentences -- opens by saying the framework
"stops short of saying who signs" then closes by claiming the profile
"makes that answerable" on the same open liability question. Two
`unverifiable`: slide 10's inter-rater-reliability claim and slide 11's
reward-hacking/specification-gaming equivalence are both plausible but not
actually stated in the paper.

Fixes queued for pass 4:

1. Slide 5, wrong. Rewrite the "three properties appear in all of them"
   claim to match what the paper actually asserts per property -- autonomy
   and efficacy as near-universal, goal complexity as merely common across
   several definitions, not all seven.
2. Slide 12, overstated. Remove the internal contradiction -- don't claim
   the profile "makes [liability] answerable" when the same slide already
   says the framework stops short of assigning responsibility. Keep the
   Waymo red-light example as an open question, not a resolved one.
3. Slide 10, unverifiable. Drop or resource the inter-rater-reliability
   claim; the paper's actual caveats are no validated metric and standards
   not yet developed.
4. Slide 11, unverifiable. Drop or hedge the specification-gaming/reward-
   hacking equivalence -- plausible but not stated in the paper.
5. Slide 6, minor. Move the A.4/A.2 code comparison out of the governance
   paragraph and into the scale block, matching slides 7-9's clean pattern.
6. Slide 7, major (business). Show the rule that crosses the causal-power
   axis with the environment axis to produce E.0-E.5, not just the two
   spot examples.
7. Slide 11, major (business). Label table row 2 with its dimension, like
   every other row.
8. Slide 5, major (business). Consider splitting the thesis slide's five
   sub-topics -- comparing definitions, naming the four dimensions, defining
   the profile, what it gives governance, and the measurement caveat -- so
   it doesn't all land in one dense slide.
9. Minors from business (slide 4 stiff phrasing, slide 5's two two-clause
   sentences, slide 8's five-clause sentence) -- tighten if a pass touches
   those slides anyway, not worth a dedicated pass on their own.

| 4 | 3 | 4 | 5 | 3 | 5 | 4 | 21 | 5 | 4 | 4 | 5 | 4 | 22 | 0 | 1 | 6 | 0 | 1 | 3 | PROCEED (cap) |

## Pass 4 notes (revision 3) -- cap reached, brought to the user

Third writer pass since the last reset. `check_standards.py --gate` confirms
"writer passes: 3 of 3" and returns PROCEED (cap) despite one technical
`wrong` finding, per the loop cap in `skills/carousel-production/SKILL.md`.
No fifth pass spawned; this goes to Franz with both reports open.

All four fixes queued after pass 3 verified as landed correctly by the
technical reviewer: slide 5's per-property precision, slide 13's liability
question left open, slide 10 (now 11)'s dropped inter-rater claim, and the
dropped specification-gaming equivalence.

One new `wrong`, and it is the same failure shape as the one just fixed,
relocated: slide 12's governance-controls table pairs the chatbot's
classifier-models control with an "Efficacy" row label, but the source gives
no dimension code to that item at all (only the assistant's paired item
carries the source's own (E.3) code). The slide's closing line claims "each
control answers to a named dimension rather than to a general sense of
caution," which this one cell doesn't satisfy. The writer's own pass-3
report had already flagged this exact gap and left it unresolved while
fixing a different issue on the same slide.

Business majors (6) are entirely readability, no accuracy findings: slides
7, 9 and 10 each pack a six-point ordinal scale into one dense paragraph
(slide 8 solves the same problem with a table and reads cleanly by
contrast); slide 5 is the one resolution-stage slide with no stated
governance consequence; slide 12's table has "Goal complexity" as two
consecutive row labels, which reads as a copy error even though it isn't;
and "Google DeepMind and Carnegie Mellon" recurs as the sentence subject
across six slides, which the business reviewer reads as tilting the deck's
independent tone toward looking like the lab's own pitch.

**Read on the underlying cause, since the gate asks for one.** This is not
a source-material or depth-pattern problem -- T1 mechanism and T4 scope both
score at or near ceiling (5, 5), and every scale/table/quote checked traces
cleanly to the paper. The recurring failure is narrower: the deck keeps
reaching for one dimension-coded table row it cannot actually source (the
chatbot's classifier control), and each pass's fix has swapped which claim
sits in that unsourced spot rather than removing the unsourced pairing
itself. The clean fix is almost certainly to stop assigning that row a
dimension code at all -- state the two controls side by side without the
"Efficacy" label -- rather than finding a different plausible-sounding
pairing a fourth time.

## Pass 1 notes

Both subtotals clear the 19/25 bar comfortably and both primary dimensions
(B1 so-what, T1 mechanism) clear the 4 floor. The gate still mandates a pass
on `wrong: 1` alone (slide 2 widens the paper's two-framework critique -- EU
AI Act and NIST AI RMF -- into a three-framework one by folding in autonomous
vehicle regulation, which the paper actually treats as a foundation it builds
on rather than criticizes), independent of `majors + overstated = 5`, which
would also have triggered a revise pass on its own.

The technical reviewer's `overstated` finding on slide 10 is the more
structurally interesting one: the four scored tuples for AlphaGo, ChatGPT-3.5,
Claude 3.5 Sonnet and Waymo are individually verbatim-accurate, but they read
as settled fact from slide 5 through slide 11, and the deck only discloses on
slide 12 that none of the four dimensions has a validated measurement method
and that the worked examples are the authors' own unvalidated classifications.
Business reviewer flagged the same slides independently, from the opposite
direction: slide 10's bracket notation ("[A.3, E.1, GC.2, G.1]") is illegible
without decoding four abbreviations across four systems in one sentence, and
slide 2's "all three" claim reads as an internal inconsistency even before
the source-fidelity problem underneath it is visible. Both reviewers
converging on slide 2 and slide 10 from different angles is the roster
working as intended.

Fixes queued for pass 2, all from the technical review plus the business
readability findings on the same slides:

1. Slide 2, scope. Narrow "all three" back to the two frameworks the paper's
   critique actually names (EU AI Act, NIST AI RMF), and either drop or
   attribute the "sound foundations" characterization, since the paper does
   not use it. Separately identify Google DeepMind / Carnegie Mellon as the
   framework's own authors on this slide rather than first on slide 5, per
   the business reviewer's authority-appeal finding.
2. Slide 4, scope. Restore "general" before "high-autonomy agents" so the
   reduced-oversight claim stays tied to Park et al.'s example rather than
   reading as a claim about all highly autonomous simulated agents.
3. Slide 7, accessibility. Either name the efficacy matrix's rungs before
   using "constrained abilities" / "intermediate control" as comparison
   terms, or drop the direct comparison in favor of language already
   established earlier in the deck.
4. Slide 10, caveat sequencing. Move a short version of slide 12's "structured
   judgment, not measurement" caveat earlier, at or before slide 10, so the
   four tuples are never presented as settled fact ahead of that disclosure.
5. Slide 10/11, accessibility. Consider a lighter-weight rendering of the
   bracket tuples so a non-technical reader isn't decoding four abbreviations
   across four systems in one sentence.
6. Slide 11, minor. Translate or drop "interpretability checks on its internal
   goal representation" into something a commercial reader can act on.
7. Slide 12, minor. Source or soften "more than most governance registers
   hold today" -- flagged by the business reviewer as unattributed, not yet
   confirmed against the paper by the technical pass.

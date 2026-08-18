# Technical review — revision 1

PRIMARY TEST
pipeline sketch (from memory, after full read of both draft and paper):
1. Instrument the corpus at instruction level (not file level) across 1,867 repos, matching instructions across commit history -- needed because line diffs can't tell a deletion from a reword, and file size alone conflates growth mechanisms.
2. Characterize the ratchet: instructions grow steadily, then a wholesale-rewrite commit periodically clears roughly half the file, then growth resumes faster than before -- needed to establish that this is a self-reinforcing pattern (bulldoze, not prune) rather than simple accumulation.
3. Fit the deletion hazard curve and rule out rival mechanisms (staleness predicts hazard rising with age; content fragility, tested via gamma frailty, absorbs only part of the decline; the multi-author interaction confirms hazard falls faster on files more people have touched) -- needed to pin the root cause on lost rationale specifically, since the fix only follows from the correct cause.
4. Formalize why deletion becomes irrational once rationale is gone: two instructions can jointly cover one hidden requirement, so verifying either is safe to cut requires testing combinations, which is exponential in the number of instructions -- needed to explain the mechanism, not just assert it.
5. Propose the fix: a comment attached at write time, naming the failure that prompted the instruction, stripped before the executor ever sees it -- needed because it directly collapses the exponential audit back to a single question.
6. Build a testbed with a known ground truth by inverting IFEval -- needed because excess size is otherwise uncomputable without knowing the true minimum cover.
7. Run maintenance with vs. without comments over 15 and 51 rounds -- needed to show the comment protocol actually settles near/below the minimum while the uncommented arm balloons, at roughly matched satisfaction.
8. Seed real WildIFEval prompts with 16 distractor instructions and re-run the protocol -- needed to confirm the size reduction translates into recovered instruction-following on real prompts, confirmed under a second judge.
9. Swap in stronger maintainer models (Haiku vs Opus) -- needed to show the ratchet and the fix's payoff scale with agent capability.
10. Recommend keeping a human in the deletion path -- needed because writing a comment is provably safe but the automated pruning protocol overprunes on a meaningful share of worlds, so acting on a comment is where real risk sits.
gaps: none
had to reopen the deck to answer: no

SCORES
T1 mechanism: 5
T2 fidelity: 3
T3 traceability: 4
T4 scope: 4
T5 depth-pattern: 4
subtotal: 20/25

DEFECTS
blockers: 0
wrong: 1
majors: 0
overstated: 2
unverifiable: 0
minors: 1

The deck is largely defensible against the paper, and the twelve pass-1 fixes hold up under the trim: the >=50% rewrite definition (slide 2), the T=15/T=51 separation (slide 7), the raw-ratio framing (slide 9), and the seeded-distractor scoping of 23.1% (slides 1 and 8) are all still intact and accurate. The single biggest exposure is slide 2's "wholesale rewrites cause 77.3% of all instruction deaths," which attaches a combined figure (rewrites plus migrations) to a narrower category (rewrites alone) that the paper reports separately at 76.8%. It's a small numeric gap but a real category mismatch, and it forces another pass under the gate as written.

## Findings

SLIDE 2 · wrong · "Wholesale rewrites cause 77.3% of all instruction deaths."
  The paper reports two different figures here. The Introduction: "76.8% of instruction deaths arrive in one commit that bulldozes the file" -- that is the wholesale-rewrite-only figure. Section 3.2 and Appendix A.4 give 77.3% as rewrites and migrations combined: "77.3% of instruction deaths arrive in a wholesale rewrite or a migration to a sibling file" / "Together the two censor 77.3% of observed instruction deaths." The deck names the narrower category ("wholesale rewrites") but attaches the broader combined number to it. The correct figure for wholesale rewrites alone is 76.8%, not 77.3%.

SLIDE 8 · overstated · "confirmed by a second judge"
  The 11.6pp / 23.1% figure is judge 1's (claude-haiku-4-5) estimate for criterion (ii), "comments buy IF," per Table 14. The second judge (gpt-5.6-luna) found a smaller effect, 7.8pp, on the same criterion, not 11.6pp. Appendix D.3 is explicit that what survives under the second judge is the sign and statistical significance of the criterion, not the magnitude, and separately notes the 11.6pp vs 7.8pp spread "has no evidential support as a judge difference" given the sample size, which is a claim of insufficient power to detect a difference, not a claim that the magnitude itself was reproduced. Saying the specific 11.6-point/23.1% figure was "confirmed" overstates what the second judge showed; it confirmed the direction, at a materially smaller point estimate.

SLIDE 7 · overstated (missing caveat) · "with comments, 5.8% below it, at equal satisfaction"
  This is the point the business reviewer flagged, and on inspection there is a real technical issue underneath, not just an awkward juxtaposition. The pooled numbers are accurate (Table 2: TREATMENT at T=15 is -5.8% excess size, 38.2% satisfaction vs. CONTROL's 39.0%), and "parity" is the paper's own word for this. But the paper does not present that parity as unconditional. Appendix C.5 shows the informative-comments arm empties the prompt entirely in 12.1% of worlds (Table 12a), against 2.4% for the uncommented arm, and on exactly those emptied worlds satisfaction parity fails: the informative-comments arm scores lowest of the three arms on those worlds (Table 12b: 0.259 vs. 0.279 uncommented, 0.328 placebo). The Ethics Statement calls this "the main risk" of the recommendation: "Our protocol empties a non-trivial share of prompts, and the uncommented arm scores higher on exactly those worlds." Slide 10 does gesture at deletion risk generally, but slide 7 states "equal satisfaction" as if it holds everywhere, and nothing connects that recommendation back to this specific finding. This is the omission a reader could reasonably build a false belief from: that going below the minimum cover is costless. It is not costless on the subset where it happens.

SLIDE 3 · minor · "Each commit adds 4.9 net instructions on average."
  The paper's exact figure, "each commit adds a net +4.9 instructions across 19,267 commits," is stated as computed "excluding mass rewrites." The slide presents it as an unqualified per-commit average.

## Notes on things checked and cleared
- Slide 1's 226%/tripling figure, the 99.3%/T=51 single-run scoping, and the 23.1%/seeded-distractor scoping all trace cleanly.
- Slide 2's rewrite definition (>=50%), median 46 killed/14 born, and the 91.5%/10-commit recovery with 4.9% vs 4.1% growth rates all match Figure 4 and Table 4(a) exactly.
- Slide 4's 28,426 deletions, -0.032/commit slope, and the "under a third" (30.8%) fragility-absorption figure trace to Figure 5 and Section 3.4/Appendix A.7 as the paper's own body text frames them.
- Slide 9's raw-ratio framing (1.68/6.72 rounding to 1.7/6.7) and its explicit "one seed" caveat both trace to Table 9 and its footnote; the deck correctly avoids citing the flagged, non-compliant Sonnet 5 row.
- Slide 10's recommendation and pull-quote trace verbatim to the Ethics Statement.
- No separate labelled "for business" / "under the hood" notes appear anywhere; the dual-track pattern's blended-paragraph requirement is followed consistently.

Files reviewed: `carousels/2608.11095/draft-carousel.md`, `papers/text/2608.11095.md`, `skills/carousel-production/writing-standards.md`, `skills/carousel-production/SKILL.md`.

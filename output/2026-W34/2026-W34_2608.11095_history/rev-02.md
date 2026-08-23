---
title: "Catastrophic remembering in agentic coding, LinkedIn carousel"
type: carousel
status: in-review
source: papers/text/2608.11095.md
arxiv_id: "2608.11095"
depth_pattern: dual-track
slides: 11
revision: 2
---

## Slide 1 · Writing down why each instruction exists keeps an agent's rules file small enough to follow

*Stage: resolution*

Coding agents read a rules file, commonly CLAUDE.md, before each task. Instruction counts more than triple over a file's lifetime across 1,867 repositories. One habit reverses this: write the failure that prompted an instruction in a note beside it. In a 51-round simulation where the smallest workable rule set was known, those notes cut the surplus above it by 99.3%, and lifted instruction-following 23.1% on prompts padded with 16 needless rules.

## Slide 2 · Agent rules files grow until someone bulldozes half of them, and then they grow back faster

*Stage: situation*

Agent instruction files ratchet rather than grow steadily. Growth runs until one commit clears at least half the file, a median 46 killed against 14 added. Wholesale rewrites carry 76.8% of all instruction deaths. Files regain 91.5% of their prior count within ten commits, then grow faster than before, 4.9% per commit against 4.1%.

*Figure: reuse Figure 3, the six-repository sawtooth chart.*

## Slide 3 · The ratchet is the norm across public GitHub, and the median file has already grown past what models handle reliably

*Stage: situation*

The corpus spans 1,867 public GitHub repositories carrying CLAUDE.md, AGENTS.md or copilot-instructions.md, tracked instruction by instruction rather than by file size. Among multi-version repositories, 64.3% gain instructions against 26.6% that shed them. The median file ends at 39 instructions, well past where instruction-following degrades, so the typical file is already large enough to cost the agent accuracy.

## Slide 4 · The growth traces to one cause: reasoning that decays faster than the instructions it justifies

*Stage: complication*

Three explanations compete for why maintainers stop deleting: staleness, fragility, lost rationale. Staleness predicts deletion risk rising with an instruction's age. Across 28,426 deletions it falls instead, at 0.032 per commit. Fragility, where brittle instructions die young and leave sturdier ones behind, explains under a third of that decline. Only lost rationale predicts the rest: the decline steepens on files several people have edited, since rationale lives in whoever wrote it.

*Figure: reuse Figure 5, the deletion hazard curve.*

## Slide 5 · Losing that reasoning turns a cheap deletion into an exponentially expensive audit

*Stage: complication*

Adding an instruction costs one line. Removing one safely is harder: two instructions can cover the same hidden requirement, so each looks disposable alone, though deleting both breaks what they jointly covered. An honest check has to test combinations, doubling with every instruction in the file. Knowing why an instruction exists collapses that check to one question. Lose the reason, and the rational move is to leave it in place.

## Slide 6 · Software engineering solved this problem decades ago with a simple tool: the comment

*Stage: resolution*

Code comments exist for exactly this reason: they tell the next maintainer why a line is there, in a channel the machine never reads. Agent instruction files carry none of that. The fix: attach a short note to each instruction naming the failure it fixed, kept out of what the agent sees. One sentence at write time buys a file the next person can cut down safely.

## Slide 7 · Comments hold a maintained prompt at the smallest set that still does the job

*Stage: resolution*

Measuring bloat needs a known right answer. South Park Commons inverted IFEval, hiding the correct instruction list so a maintainer rebuilds it from feedback. Over 15 steps and 552 histories, maintainers without comments finished 60.4% above the minimum; with comments, 5.8% below it, at matched satisfaction where it left instructions in place. A longer 51-step run widened the gap to 211.3% against 1.4%. Instructions above the minimum earn nothing and cost on every call.

*Figure: reuse Figure 1(a), the excess-size curve comparing commented and uncommented arms.*

## Slide 8 · A pruned prompt wins back the instruction-following that clutter costs

*Stage: resolution*

A smaller file only matters if the agent behaves better. The same protocol ran on WildIFEval prompts seeded with 16 extraneous instructions, standing in for clutter. Maintainers writing comments pruned them and held satisfaction steady. Maintainers without comments finished 11.6 points lower, a 23.1% relative gap. A second judge confirmed the direction and its significance, at a smaller 7.8 points. The clutter was seeded, so the number prices what an overgrown file already costs.

## Slide 9 · The payoff compounds as agents grow more capable

*Stage: impact*

Swap a stronger model into the maintainer's seat, and the ratchet gets worse. Without comments, a prompt maintained by Haiku 4.5 ends at 1.7 times the minimum size it needed; by Opus 5, at 6.7 times. Comments remove a larger share from the stronger maintainer's file. This is one seed's worth of evidence, a direction rather than a settled magnitude. Capable agents write more, so the fix earns more over time.

## Slide 10 · The fix works best with a human still owning the deletion decision

*Stage: impact*

Writing a comment is safe: it adds information and removes nothing. Deleting is where the risk sits. The pruning protocol emptied the prompt entirely on 12.1% of test cases, and scored worst of the three arms on exactly those. The recommendation: keep a person in the deletion path, and hold safety-relevant instructions out of scope until the protocol is tested on them.

> "Writing a comment removes nothing and is therefore safe. Acting on one is not."

## Slide 11 · The cheapest version of this is one sentence per instruction, starting with the next one you add

*Stage: impact*

This works with the files a team already has. Next time an instruction goes into a CLAUDE.md, AGENTS.md or copilot-instructions.md, write one line beside it naming the failure that prompted it. That line is what makes the file prunable once the person who added it has moved on. The evidence covers only those three file types. Where does the reasoning behind your agents' instructions live today, and who on your team could reconstruct it?

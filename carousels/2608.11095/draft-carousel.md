---
title: "Catastrophic remembering in agentic coding, LinkedIn carousel"
type: carousel
status: in-review
source: papers/text/2608.11095.md
arxiv_id: "2608.11095"
depth_pattern: dual-track
slides: 11
revision: 1
---

## Slide 1 · Writing down why each instruction exists keeps an agent's rules file small enough to follow

*Stage: resolution*

Coding agents read a rules file, commonly CLAUDE.md, before touching a repository. Instruction counts more than triple over a file's lifetime across 1,867 repositories. One habit reverses this: record why an instruction was added, when it is added. A single 51-step run cut excess instructions 99.3%, and the same fix lifted instruction-following 23.1% on prompts seeded with 16 distractors.

## Slide 2 · Agent rules files grow until someone bulldozes half of them, and then they grow back faster

*Stage: situation*

Agent instruction files ratchet rather than grow steadily. Growth continues until one commit clears at least half the file, median 46 killed and 14 added at once. Wholesale rewrites cause 77.3% of all instruction deaths. Afterward, files recover to 91.5% of their prior count within ten commits, growing faster than before: 4.9% per commit versus 4.1%.

*Figure: reuse Figure 3, the six-repository sawtooth chart.*

## Slide 3 · The ratchet is the norm across public GitHub, and the median file has already grown past what models handle reliably

*Stage: situation*

The corpus spans 1,867 GitHub repositories carrying CLAUDE.md, AGENTS.md or copilot-instructions.md: 299,440 version-to-version transitions and 247,694 tracked instruction lifetimes. Among multi-version repositories, 64.3% gain instructions against 26.6% that lose them. Each commit adds 4.9 net instructions on average. The median file holds 39 instructions, the top tenth 131 or more, well past where instruction-following degrades.

## Slide 4 · The growth traces to one cause: reasoning that decays faster than the instructions it justifies

*Stage: complication*

Three explanations compete for why maintainers stop deleting: staleness, fragility, lost rationale. Staleness predicts deletion risk rising with age. Across 28,426 tracked deletions it falls instead, at 0.032 per commit. Fragility explains under a third of that decline. Only lost rationale predicts the rest: the decline is steeper on files several people have edited, since rationale lives in the people who wrote it.

*Figure: reuse Figure 5, the deletion hazard curve.*

## Slide 5 · Losing that reasoning turns a cheap deletion into an exponentially expensive audit

*Stage: complication*

Adding an instruction costs one line. Removing one safely is harder: two instructions can cover the same hidden requirement, so each looks disposable alone, though deleting both breaks what they jointly covered. An honest check has to test combinations, doubling with every instruction in the file. Knowing why an instruction exists collapses that check to one question. Lose the reason, and the rational move is to leave it in place.

## Slide 6 · Software engineering solved this problem decades ago with a simple tool: the comment

*Stage: resolution*

Code comments exist for exactly this reason: they tell the next maintainer why a line is there, in a channel the machine never reads. Agent instruction files carry none of that. The fix: attach a short note to each instruction naming the failure it fixed, kept out of what the agent sees. One sentence at write time buys a file the next person can cut down safely.

## Slide 7 · Comments hold a maintained prompt at the smallest set that still does the job

*Stage: resolution*

Measuring bloat needs a known right answer. South Park Commons inverted IFEval, hiding its correct instruction list so a fresh maintainer rebuilds it from feedback alone. Over 15 steps and 552 histories, maintainers without comments finished 60.4% above the minimum; with comments, 5.8% below it, at equal satisfaction. A longer 51-step run widened that gap to 211.3% against 1.4%. Every instruction above the minimum earns nothing, and still costs on every call.

*Figure: reuse Figure 1(a), the excess-size curve comparing commented and uncommented arms.*

## Slide 8 · A pruned prompt wins back the instruction-following that clutter costs

*Stage: resolution*

A smaller file only matters if the agent behaves better. The same protocol ran against WildIFEval, seeding 16 extraneous instructions into each prompt to stand in for clutter. Maintainers writing comments pruned them and held satisfaction steady. Maintainers without comments finished 11.6 points lower, a 23.1% relative gap, confirmed by a second judge. The clutter was seeded deliberately: the number prices what an overgrown file already costs.

## Slide 9 · The payoff compounds as agents grow more capable

*Stage: impact*

Swap a stronger model into the maintainer's seat, and the ratchet gets worse. Without comments, a prompt maintained by Haiku 4.5 ends at 1.7 times its minimum size; by Opus 5, at 6.7 times, the raw ratio rather than excess above minimum. Comments remove a larger share from the stronger maintainer's file. This is one seed's worth of evidence, a direction rather than a settled magnitude. Capable agents write more, so the fix earns more over time.

## Slide 10 · The fix works best with a human still owning the deletion decision

*Stage: impact*

Writing a comment is safe: it adds information and removes nothing. Deleting an instruction is where the real risk sits. The recommendation: keep a person in the deletion path, and hold safety relevant instructions out of scope until the protocol is tested on them.

> "Writing a comment removes nothing and is therefore safe. Acting on one is not."

## Slide 11 · The cheapest version of this is one sentence per instruction, starting with the next one you add

*Stage: impact*

This works with the files a team already has. Next time an instruction goes into a CLAUDE.md, AGENTS.md or copilot-instructions.md, write one line beside it naming the failure that prompted it. That line is what makes the file prunable once the person who added it has moved on. The evidence covers only those three file types. Where does the reasoning behind your agents' instructions live today, and who on your team could reconstruct it?

---
title: "Catastrophic remembering in agentic coding, LinkedIn carousel"
type: carousel
status: in-review
source: papers/text/2608.11095.md
arxiv_id: "2608.11095"
depth_pattern: dual-track
slides: 11
revision: 0
---

## Slide 1 · Capturing the reasoning behind every CLAUDE.md instruction lifts performance by up to 23%

*Stage: resolution*

Agent coding prompts like CLAUDE.md accumulate instructions and rarely lose any, tripling in size over their lifetime across 1,867 repositories. One practice reverses this: recording why an instruction exists, at the moment it is written. That habit cuts prompt bloat by over 99% and lifts real world performance by up to 23%.

## Slide 2 · CLAUDE.md files grow in a ratchet. 226% growth. A wholesale rewrite. Growth resumes.

*Stage: situation*

Left alone, agent instruction files do not grow steadily, they ratchet. Instructions build up for months, then a maintainer deletes everything in one pass. Growth resumes immediately after, and faster than before: files recover to 91.5% of their prior size within ten commits of a rewrite.

*Figure: reuse Figure 3, the six-repository sawtooth chart.*

## Slide 3 · The pattern holds at scale. 247,694 instructions. 1,867 repositories.

*Stage: situation*

This is not one team's habit. It shows up across 1,867 public GitHub repositories, 299,440 tracked file versions, and 247,694 individual instruction lifetimes. Growth averages plus 4.9 net instructions every commit, and the median file already carries 39 instructions.

## Slide 4 · The growth traces to one cause: reasoning that decays faster than the instructions it justifies

*Stage: situation*

The paper tests three explanations for why maintainers do not delete: instructions going stale, fragile instructions dying young, and lost rationale. Only lost rationale fits the data. Deletion hazard falls as an instruction ages, and falls faster the more people have edited the file.

*Figure: reuse Figure 5, the deletion hazard curve.*

## Slide 5 · Losing that reasoning turns a cheap deletion into an exponentially expensive audit

*Stage: situation*

Adding an instruction costs nothing. Removing one safely requires confirming no other instruction quietly depends on it, across every possible combination. That audit cost grows exponentially with file size. Once the reasoning is gone, deletion becomes too risky to attempt.

## Slide 6 · Software engineering solved this problem decades ago with a simple tool: the comment

*Stage: resolution*

Code comments exist for exactly this reason: to tell the next person why a line exists, separate from what it does. Agent instruction files have no equivalent yet. The fix, adapted to prompts: attach a short comment to every instruction, at write time.

## Slide 7 · Comments that capture the why cut prompt bloat by over 99%

*Stage: resolution*

In a controlled test, maintainers who wrote a comment with every instruction, naming the failure it fixed and the reasoning behind it, kept their prompts near the true minimum size. Maintainers without comments grew their prompts by 60% or more over the same steps.

*Figure: reuse Figure 1(a), the excess-size curve comparing commented and uncommented arms.*

## Slide 8 · The same fix lifts real world task performance by up to 23%

*Stage: resolution*

Smaller, more accurate prompts are also easier for a model to follow. Applying the same comment protocol to a real world instruction-following benchmark improved task completion by up to 23%, confirmed across two independent model judges scoring the same responses.

## Slide 9 · The payoff compounds as agents grow more capable

*Stage: resolution*

Stronger maintainer models ratchet harder when left uncommented: excess prompt size roughly quadruples moving from a smaller model to a larger one. The comment protocol's benefit grows right alongside that capability, so the fix matters more as agents improve.

## Slide 10 · The fix works best with a human still owning the deletion decision

*Stage: situation*

Writing a comment is safe: it adds information and removes nothing. Deleting an instruction is where the real risk sits. The recommendation: keep a person in the deletion path, and hold safety relevant instructions out of scope until the protocol is tested on them.

> "Writing a comment removes nothing and is therefore safe. Acting on one is not."

## Slide 11 · Write the reasoning into every prompt, alongside the instruction

*Stage: resolution*

Any org running Claude Code, Cursor, or a similar agent can start today: when you add an instruction to CLAUDE.md, add a short comment naming why. That one habit prevents years of accumulated debt, and keeps the prompt small enough for the agent to actually follow.

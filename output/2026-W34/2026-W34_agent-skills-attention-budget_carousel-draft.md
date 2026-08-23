---
title: "Agent skills, attention budget: consolidated storyline"
type: storyline
status: draft
depth_pattern: dual-track
sources:
  - arxiv_id: "2608.14036"
    role: "the why: skills drive real performance, and that performance is lost silently as the skill library grows"
  - arxiv_id: "2608.12610"
    role: "the recommendation: @skills manages the context window's limited slots directly, and what it solves"
slides: 9
---

Revision 8: pure pyramid, no situation-complication-resolution arc. Slide 1 states the full recommendation. Slides 2 to 4 are the reason why, grounded entirely in 2608.14036's performance evidence. Slides 5 to 8 return to @skills and what it solves, grounded in 2608.12610. Slide 9 closes on action. No stage carries a "situation" or "complication" label; support is reason, mechanism, and proof under one answer, not a separate narrative arc. MBB register, one sentence titles, no negation, no hype. Bodies target 50 words, ceiling 120.

## Slide 1 · Adopt @skills to manage the limited slots in your agent's context window

*Stage: answer (recommendation)*

Every agent has a limited number of slots that can stay loaded in its context window, and @skills manages that budget directly. Adopt it to decide, skill by skill, which capabilities are fetched on demand and which earn a permanent seat. Skip that discipline, and an agent's performance degrades exactly as its skill library grows, invisibly, on the one metric most teams track.

**Visual:** a stat card, 56,804 published skills against fewer than 100 that can occupy the context window at once. No figure in either paper states this exact contrast; build it fresh as the opening slide.

Sources: both papers, synthesis

## Slide 2 · Skills earn their value by guiding an agent's actions

*Stage: reason (2608.14036, what is at stake)*

Procedural anchoring, an agent following a clear sequence of steps, drives 65.7% of successful skill use, against 4.5% for injecting missing facts. Skills beat the closest alternative, direct workflow memory, by 6.06 points in matched comparisons. This is the performance a context-window budget is protecting, not a side benefit of installing more.

**Visual:** 2608.14036's Figure 2, the taxonomy label distribution across trajectory mixtures, or Table 11's mode breakdown.

Source: 2608.14036 (procedural anchoring, Section 5.1)

## Slide 3 · Retrieval precision collapses as a skill library grows past a few dozen entries

*Stage: reason (2608.14036, the performance lost)*

As a skill pool grows from 5 to 100 candidates, precision on picking the right one falls from 29.6% to 3.3%. Task success barely moves, holding near 36% to 39%, because a related skill often still helps. That gap between having a skill and finding it is exactly the performance loss active management is meant to prevent.

**Visual:** 2608.14036's Figure 3, the precision and downstream-success curves on SkillsBench.

Source: 2608.14036 (retrieval precision, RQ4)

## Slide 4 · Aggregate success rate hides where a skill program actually breaks

*Stage: reason (2608.14036, why the loss goes unnoticed)*

A skill can fail three ways: it is never retrieved, it is retrieved but misapplied, or it succeeds and the task still fails. Misapplication alone accounts for 10% of skill outcomes, a failure mode raw execution barely shows. A team watching only the aggregate number sees none of this coming.

**Visual:** 2608.14036's Table 11, the skill-use mode breakdown, showing skill_guidance_misapplied_or_ignored as a distinct category.

Source: 2608.14036 (misapplication, Section 5.3)

## Slide 5 · That loss traces to a hard ceiling: under a hundred skills can occupy the context window at once

*Stage: reason (2608.12610, the mechanical cause, pivot back to the recommendation)*

Three mechanical effects compound. A description loses influence the further it sits from the live task. Each one taxes every message, relevant or not. More descriptions dilute attention to all of them. Together they bound reliable capacity at under 100 skills, against a public catalogue of 56,804. This is the ceiling @skills is built to manage.

**Visual:** 2608.12610's Figure 5, left panel, the install-only side, showing attention decaying with distance from the task.

Source: 2608.12610 (the attention budget, Section 2)

## Slide 6 · @skills separates availability from permanence

*Stage: mechanism (2608.12610, what it solves)*

Installation currently bundles three decisions into one: whether to keep a copy, whether it fires automatically, and where the content lives. @skills splits them apart, so a skill can be reachable without ever costing a slot in the context window. Each decision now costs exactly what it needs, no more.

**Visual:** 2608.12610's Figure 2, the contribution in one picture, the two by two grid separating firing unprompted from owning a copy.

Source: 2608.12610 (the protocol, an open specification with a reference CLI)

## Slide 7 · Three tiers manage the budget directly: reference, save, install

*Stage: mechanism (2608.12610, detail)*

@skills:<path> fetches a skill at the moment of use, at zero standing cost. Adding :save vendors a copy into the project's git tracked .atskills/ folder, also at zero cost. Adding :install adds one line to .autotrigger, reserved for the small set that must fire unprompted. Sort an existing library into these three tiers before writing a single new skill.

**Visual:** 2608.12610's Figure 1, the three delivery tiers, sized by how many skills each is for.

Source: 2608.12610 (the three tiers: reference, save, install)

## Slide 8 · The right skill arrives exactly when needed

*Stage: proof (2608.12610, targeting the loss named in slide 3)*

A referenced skill loads at the end of the conversation, next to the current task, the position where an agent's attention is strongest. That design targets exactly the gap named earlier: it removes the standing cost that caps library size, and places content where attention is strongest rather than where installation happened to be easiest.

**Visual:** 2608.12610's Figure 5 again, this time the right panel, the reference-delivery side, completing the before and after split opened on slide 5.

Sources: both papers (2608.12610's point of use injection, 2608.14036's retrieval finding it targets)

## Slide 9 · How many of your agent's skills already claim a slot they don't need?

*Stage: close (action)*

Every enterprise agent program hits the same ceiling as its skill library grows: a fixed number of slots, and shrinking odds of finding the right one inside them. Count how many of your team's installed skills actually need a permanent slot, and manage the rest with @skills instead.

**Visual:** none needed, or a callback to 2608.12610's Figure 1 for a closing bookend with slide 7.

Sources: both papers, synthesis

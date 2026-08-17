---
title: "Agentic profiles for AI governance, LinkedIn carousel"
type: carousel
status: in-review
source: ArxivWiki/papers/2026/nature-2026-agentic-profiles.md
arxiv_id: "nature-2026-agentic-profiles"
depth_pattern: spec-cards
slides: 10
revision: 4
---

## Slide 1 · Your AI agents are arriving faster than the controls around them

*Stage: situation*

How much oversight does this specific agent require?

## Slide 2 · Existing AI governance measures the size of the risk, not the shape of the agent

*Stage: complication*

AI agents will power 40% of enterprise applications by end-2026. 

The EU AI Act and NIST's AI Risk Management Framework grade a system's overall risk, then size safeguards to that grade. Governance would benefit from further engagement with the new properties of AI agents. Autonomous vehicle regulation sets a precedent: autonomy graded on a scale, with guidance tailored to each level. A risk score signals potential cost. An agentic profile signals what is acting.

## Slide 3 · Four scores build an AI agent profile to ground governance requirements into

*Stage: resolution*

Each dimension, autonomy, efficacy, goal complexity, generality, carries its own score. 


| System | Autonomy | Efficacy | Goal complexity | Generality |
|---|---|---|---|---|
| ChatGPT-3.5, stand-alone chat completion | 2 | 2 | 3 | 3 |
| Claude 3.5 Sonnet with tool use | 3 | 3 | 4 | 3 |
| Waymo autonomous vehicle | 4 | 4 | 4 | 2 |



## Slide 4 · Autonomy decides how fast a small error becomes an expensive one

*Stage: resolution*

| Level | What it means |
|---|---|
| 0 No autonomy | Acts only as the principal directs |
| Restricted | One automated activity; everything else stays under direct control |
| 2 Partial | Several automated activities; principal stays ready to step in |
| 3 Intermediate | Most tasks run independently; principal decides on critical calls |
| 4 High | All tasks run independently within known circumstances; oversight held in reserve |
| 5 Full | All tasks, all circumstances, no oversight |

## Slide 5 · Efficacy separates a mistake you can reset from one you have to live with

*Stage: resolution*

| Causal power | Simulated | Mediated | Physical |
|---|---|---|---|
| Observation only | 0 | 0 | 0 |
| Constrained | 1 | 2 | 3 |
| Intermediate | 2 | 3 | 4 |
| Comprehensive | 3 | 4 | 5 |

Simulated environments reset. Mediated environments pass through a human before anything happens. Physical environments carry changes that persist and can be irreversible.

## Slide 6 · Goal complexity is where checking the output stops being enough

*Stage: resolution*

| Level | What it means |
|---|---|
| 0 No goal | Absence of a goal is absence of an agent |
| 1 Minimal | One goal, pursued directly |
| 2 Low | One goal, pursued through a more elaborate sequence |
| 3 Intermediate | Multifaceted goal, broken into subgoals, pursued fairly directly |
| 4 High | Multifaceted goal, many subgoals balanced and sequenced, themselves hard to fulfil |
| 5 Unbounded | Generates its own goal structures; interprets underspecified objectives |

## Slide 7 · Generality settles whether governance is a departmental job or a corporate one

*Stage: resolution*

| Level | What it means |
|---|---|
| 0 No application | No domain |
| 1 Single task | One task; capability does not transfer to related domains |
| 2 Task domain | A closely related set of tasks, such as board games |
| 3 Multiple domain | Different domains, drawing on different capabilities: linguistic, logical, creative |
| 4 Majority domain | Most human task domains |
| 5 Fully general | The entire suite of human cognitive tasks |


## Slide 9 · Different Agentic profiles deliver specific governance needs

*Stage: resolution*

A simple chatbot [A.1, E.1, GC.2, G.2] and an advanced assistant [A.3, E.3, GC.4, G.4] make a clean baseline for comparing standards, since the assistant ranks higher on every dimension:

| Dimension | Chatbot [A.1, E.1, GC.2, G.2] | Assistant [A.3, E.3, GC.4, G.4] |
|---|---|---|
| Autonomy | Direct oversight is sufficient at A.1. | Hard-coded stop conditions and automated circuit breakers are required at A.3. |
| Efficacy | Classifier models scan and block prohibited content. | Tool permissions are capped to the minimum needed, and time-bound, at E.3. |
| Goal complexity | Domain-specific evaluation benchmarks are largely sufficient at GC.2. | Interpretability tooling audits internal goal representation at GC.4. |
| Generality | Governance tailored to the known domain is sufficient at G.2. | System-level governance, including agent identification and gating protocols, is needed at G.4. |


## Slide 8 · Your agentic profile changes the moment you add a new tool


Agentic profiles are not fixed. Adding tool use, memory or reasoning shifts a system's scores. The practical version starts small: list the agents already running, score each across the four dimensions, and revisit whenever the scaffolding changes. How is your organization piloting governance for its AI agents? Share your approach below.


## Slide 10 · [closer, pending link]

*Stage: impact*

**PENDING:** awaiting the URL to link out to. Draft placeholder below.

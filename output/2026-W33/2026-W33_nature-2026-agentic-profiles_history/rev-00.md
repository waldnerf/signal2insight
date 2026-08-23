---
title: "Agentic profiles for AI governance, LinkedIn carousel"
type: carousel
status: draft
source: ArxivWiki/papers/2026/nature-2026-agentic-profiles.md
arxiv_id: "nature-2026-agentic-profiles"
depth_pattern: dual-track
slides: 12
revision: 0
---

## Slide 1 · Your AI agents are arriving faster than the controls around them

*Stage: situation*

Gartner expects task-specific AI agents inside 40% of enterprise applications by the end of 2026, up from under 5% in 2025 (Gartner, 2025). Most will be small: a support assistant, a document classifier, a scheduling bot. Some will hold credentials, call external systems and act on a customer's behalf. Governance teams are being asked to sign off on both, often in the same meeting, against the same checklist. The question a board actually asks is narrower than whether AI is safe. It is how much oversight this particular agent needs, and on what basis that was decided.

## Slide 2 · Today's governance frameworks grade a system by one overall risk score

*Stage: situation*

The EU AI Act and the National Institute of Standards and Technology's AI Risk Management Framework both work the same way: sort a system into a risk tier, then attach safeguards proportionate to that tier. Autonomous vehicle regulation graded one property, autonomy, on a scale, but only inside driving. Google DeepMind and Carnegie Mellon treat all three as sound foundations that still lack a description of what makes a system agentic. A risk tier says how much a system could cost. It says little about what kind of thing is acting.

> "both approaches could benefit from further engagement with the new properties of AI agents"

## Slide 3 · A customer chatbot and a purchasing agent land in the same compliance tier

*Stage: complication*

Take two systems a bank might run this year. One answers product questions in a chat window and stays there. The other navigates web interfaces, holds payment credentials and completes purchases for a customer. Both are built on a large language model, both sit behind the same login, and both get filed as generative AI on the risk register. The controls they need overlap barely at all. Filing them together is how an organisation ends up over-controlling the harmless system and under-controlling the one that can move money.

## Slide 4 · Ranking agents on a single scale of how agentic they are misprices oversight

*Stage: complication*

The intuitive rule is that a more agentic system needs more governance. Google DeepMind and Carnegie Mellon reject that straight line. An AI system used for medical triage has little autonomy but real clinical consequence, so it poses acute risk inside a narrow domain. A highly autonomous agent running purely in simulation, where states reset, needs far less logging and auditing than its autonomy score alone would suggest. What sets the control regime is which dimensions are elevated, and in what combination.

> "'more agentic' system always requires 'more governance'"

## Slide 5 · A Nature framework describes any AI agent with four separate scores

*Stage: resolution*

The framework, published in Nature in August 2026 by Google DeepMind and Carnegie Mellon, surveys seven influential computer science definitions of an agent and extracts what they all rely on: autonomy, efficacy, goal complexity and generality. Each gets its own graded scale running from zero to five, so a system is described by four scores rather than one verdict. Together they form what the framework calls an agentic profile. The value for a governance function is that four scores can be argued about separately, and each one points at a different set of controls.

## Slide 6 · Autonomy counts the human decision points an agent removes

*Stage: resolution*

Autonomy is the capacity to act without external direction from a principal. The framework grades it across six levels adapted from autonomous vehicle regulation, from a system that acts only as its principal dictates, through one that performs most tasks alone but defers on critical determinations, to one that operates in all circumstances without oversight. The point is compounding: every supervisor decision point an agent removes is a place where a small error used to be caught cheaply.

> "initial mistakes may propagate through subsequent decisions and, by the time humans detect problems, substantial harm may already be hard to contain"

## Slide 7 · Efficacy measures what an agent can change and how hard that is to undo

*Stage: resolution*

Efficacy combines two things a single risk score hides. First, how much causal power the agent has, from observation only through to near-complete control of its environment. Second, how consequential that environment is: simulated spaces reset, mediated ones require a person to act on the output, physical ones leave changes that may be irreversible. An agent with constrained abilities in a physical environment rates the same as one with intermediate control in a mediated one. Where an agent acts matters as much as what it is permitted to do.

## Slide 8 · Goal complexity sets how hard the agent's work is to verify

*Stage: resolution*

Goal complexity grades how intricate an objective is, from a single direct goal, through goals that must be broken into subgoals and sequenced against each other, to goals the agent generates for itself from an underspecified brief. A summariser can be checked against a human benchmark. An agent balancing several objectives over a long sequence resists that kind of check, which is where specification gaming appears: the system finds an ingenious route to the stated goal that nobody wanted. Higher goal complexity moves oversight from checking outputs to inspecting reasoning.

## Slide 9 · Generality determines whether the risk stays inside one department

*Stage: resolution*

Generality grades the breadth of domains an agent works across, from a system that plays one game, through one that handles a related family of tasks, to one that operates across most human task domains. A narrow agent can fail badly and still fail locally, so domain-specific safeguards contain it. A general agent carries risk across system boundaries and behaves unexpectedly in contexts nobody anticipated, which calls for agent identification and gating protocols across the whole estate. Generality decides whether governance is a departmental control or a corporate one.

## Slide 10 · The four scores move independently, which is what makes them useful

*Stage: resolution*

Scored on the four dimensions, AlphaGo lands at [A.3, E.1, GC.2, G.1], ChatGPT-3.5 at [A.2, E.2, GC.3, G.3], Claude 3.5 Sonnet with tool use at [A.3, E.3, GC.4, G.3], Waymo at [A.4, E.4, GC.4, G.2]. AlphaGo acts more independently than ChatGPT-3.5 and reaches far less of the world. Waymo leads on autonomy and efficacy yet trails a chatbot on generality, because driving is one domain. One ranking would misorder them. Four scores place each system where its risk sits.

## Slide 11 · An agentic profile maps onto a specific list of controls

*Stage: resolution*

The framework sets a simple chatbot at [A.1, E.1, GC.2, G.2] against an advanced assistant at [A.3, E.3, GC.4, G.4]. The chatbot is covered by direct oversight, a classifier blocking prohibited content, and domain benchmarks. The assistant needs hard-coded stop conditions and automated circuit breakers, tool permissions granted at minimum scope and time-bound, interpretability checks on its internal goal representation, and monitors that revoke environmental access when it behaves deceptively. Each of those is a budget line, and the profile is the argument for funding it.

> "Direct oversight is insufficient for control"

## Slide 12 · An agent's profile changes the moment you give it a new tool

*Stage: impact*

Profiles drift. Adding tool use raises efficacy. External knowledge and memory raise goal complexity. Stronger reasoning raises autonomy and goal complexity together. Deploying the same agent into a service with hundreds of millions of users spikes efficacy on its own. Google DeepMind and Carnegie Mellon are candid that no validated metric exists yet for any of the four dimensions, so this is structured judgment rather than a measurement. It is still more than most governance registers hold today. Score the agents you already run, then score them again whenever the scaffolding changes.

Which agent in your estate has quietly gained autonomy or reach since the last time anyone reviewed it?

---
title: "Agentic profiles for AI governance, LinkedIn carousel"
type: carousel
status: in-review
source: ArxivWiki/papers/2026/nature-2026-agentic-profiles.md
arxiv_id: "nature-2026-agentic-profiles"
depth_pattern: spec-cards
slides: 14
revision: 3
---

## Slide 1 · Your AI agents are arriving faster than the controls around them

*Stage: situation*

Gartner expects task-specific AI agents inside 40% of enterprise applications by the end of 2026, up from under 5% in 2025 (Gartner, 2025). Most will be small: a support assistant, a document classifier, a scheduling bot. Some will hold credentials, call external systems and act on a customer's behalf. Governance teams are being asked to sign off on both, often in the same meeting, against the same checklist. The question a board actually asks is narrower than whether AI is safe. It is how much oversight this particular agent needs, and on what basis that was decided.

## Slide 2 · Today's AI rulebooks sort a system into one overall risk tier

*Stage: situation*

The EU AI Act and the AI Risk Management Framework from the National Institute of Standards and Technology work the same way. Each classifies the overall level of risk attached to a system, then applies safeguards proportionate to that risk. Writing in Nature in August 2026, Google DeepMind and Carnegie Mellon treat both as useful ground and as underspecified for agents.

> "both approaches could benefit from further engagement with the new properties of AI agents"

One graded precedent already exists. Autonomous vehicle regulation measures a single property, autonomy, on a scale rather than in tiers, and issues guidance tailored to the level a vehicle demonstrates. That scale is a foundation the Nature framework adapts, not a target of its critique.

A risk tier tells an organisation how much a system could cost. A graded scale tells it what kind of thing is acting, which is what decides the control.

## Slide 3 · A customer chatbot and a purchasing agent land in the same compliance tier

*Stage: complication*

Take two systems a bank might run this year. One answers product questions in a chat window and stays there. The other navigates web interfaces, holds payment credentials and completes purchases for a customer. Both are built on a large language model, both sit behind the same login, and both get filed as generative AI on the risk register. The controls they need overlap barely at all. Filing them together is how an organisation ends up over-controlling the harmless system and under-controlling the one that can move money.

## Slide 4 · A general agent in simulation can warrant lighter oversight than a medical triage tool

*Stage: complication*

The intuitive rule is that a more agentic system needs more governance. Google DeepMind and Carnegie Mellon reject that rule outright, and describe the whole nuance of their framework as a guard against that crude, linear idea.

Two of their own cases show why. An AI system used for medical triage has low autonomy and high efficacy, so its risk is acute and confined to the domain of medical decisions. General high-autonomy agents running in simulation, of the kind that move through everyday activities such as waking up, cooking breakfast and heading to work, sit at the other extreme: they do not need the same logging, auditing and authorization controls.

> "What matters is the kind of agent and the kind of governance in question"

A single ranking of how agentic a system is cannot separate those two cases. It over-controls the sandbox and under-controls the triage tool, which is a real cost in both directions.

## Slide 5 · Four properties decide what kind of agent a system is

*Stage: resolution*

Google DeepMind and Carnegie Mellon start by comparing seven influential definitions of an AI agent from computer science, running from Russell and Norvig in 1995 to surveys of language-model agents published in 2024. Autonomy is a key property of all seven. Efficacy is found in each one. Goal complexity is a third common element across them, with one exception at the origin: the 1995 definition describes an agent as perceiving its environment through sensors and acting on that environment through effectors, and makes no reference to a goal.

**The four dimensions.** Autonomy is the capacity to perform actions without external direction or control. Efficacy is the ability to perceive and causally affect an environment. Goal complexity is how intricate the objectives an agent can form or pursue are. Generality is the fourth, and it is added rather than inherited, because it is not an explicit feature of every one of the seven definitions. It earns its place because the breadth of domains an agent works across now separates one deployed system from another.

## Slide 6 · Four scores, one per property, tell a governance function what to require

*Stage: resolution*

**The profile.** Each dimension carries its own graded scale from 0 to 5, and a system is written as four scores rather than one verdict. That four-part description is its agentic profile. A zero on any of the four puts a system outside the account altogether: zero autonomy means it acts only as directed, zero efficacy means it changes nothing around it, zero goal complexity means it pursues nothing, and zero generality means it has no area of application.

**What it gives a governance function.** Three things: a structured classification of the aspects of agency that matter for governance, a mapping from scores to concrete profile-specific risks in development and deployment, and a mitigation step that sizes the requirements to the profile.

> "sets proportionate requirements and enables profile-specific, targeted interventions"

**One caveat, stated up front.** No dimension has a validated measurement method yet. Every score in this framework, including the worked examples on the slides that follow, is structured judgment rather than measurement. Goal complexity and generality often coincide, and the dimensions correlate and compound in several ways, so these are not four independent dials. They are four analytically distinct questions, each worth asking separately, because each points at a different set of controls.

## Slide 7 · Autonomy decides how fast a small error becomes an expensive one

*Stage: resolution*

Autonomy is the capacity to perform actions without external direction or control. That direction usually comes from a principal, meaning one human or a set of humans, and sometimes from another AI system. The field has no standard way to classify degrees of it, so the framework adapts the categorical scale already established for autonomous vehicles.

**The scale.** A.0 is no autonomy: the system depends entirely on its principal and acts only in the manner the principal dictates. A.1 is restricted autonomy: one automated activity, with every other function under the principal's direct control. A.2 is partial autonomy: several automated activities, with the principal engaged and ready to take control at any time. A.3 is intermediate autonomy: most tasks performed independently, with the principal still supplying input on critical determinations. A.4 is high autonomy: all tasks performed independently in certain circumstances, with oversight retained for the circumstances that fall outside them. A.5 is full autonomy: all tasks in all circumstances, with no oversight or control. Two familiar systems sit either side of the middle: a Waymo vehicle is placed at A.4, making real-time decisions about routing, obstacles and safety without human control, and ChatGPT-3.5 in stand-alone chat completion is placed at A.2, needing human input to start a task at all.

**What it changes for governance.** High-autonomy agents compress or eliminate the decision points a supervisor used to occupy, and that is exactly why they need stronger safeguards.

> "initial mistakes may propagate through subsequent decisions and, by the time humans detect problems, substantial harm may already be hard to contain"

The mechanisms named for high autonomy are trace-log analysis for auditing, scalable oversight that uses automated systems to supervise at scale, and kill switches that halt operations immediately when errors are detected. Every human checkpoint an agent removes is a place where a cheap correction used to happen, so raising autonomy means buying that correction back somewhere else.

## Slide 8 · Efficacy separates a mistake you can reset from one you have to live with

*Stage: resolution*

Efficacy is the ability of an agent to perceive and causally affect its environment. It is scored on a grid of two questions rather than on one line.

**How much causal power the agent has.** Four rungs. Observation only: the system watches and changes nothing. Constrained: a limited suite of actions whose effects are localized, temporary and limited in scope. Intermediate: actions that produce noticeable and persistent changes across several parameters or systems. Comprehensive: the agent reshapes its environment across several dimensions, approaching full environmental control.

**How consequential the environment is.** Three types. Simulated environments have controlled boundaries and often resettable system states. Mediated environments reach the outside world only through a human intermediary who has to interpret, decide or act before anything happens. Physical environments carry persistent state changes that cannot simply be reset, with potentially irreversible consequences.

**The grid.** Crossing the two produces E.0 to E.5, by a rule simple enough to apply by hand. Observation only scores E.0 in every environment, because it exerts no direct causal influence. For any agent that can act, the score rises one step for each rung of causal power it gains, and one further step for each move into a more consequential environment.

| Causal power | Simulated | Mediated | Physical |
|---|---|---|---|
| Observation only | E.0 | E.0 | E.0 |
| Constrained | E.1 | E.2 | E.3 |
| Intermediate | E.2 | E.3 | E.4 |
| Comprehensive | E.3 | E.4 | E.5 |

That is why a constrained agent in a physical environment reaches E.3, the same level as an agent with intermediate control in a mediated one.

> "highlighting how environmental context can amplify even limited capabilities"

**What it changes for governance.** For a low-efficacy agent confined to a simulation, risk mapping may only need to cover data corruption inside its own environment and the jailbreak risk of it leaving the sandbox to reach the host computer or network. For a high-efficacy agent acting on the physical world, the burden is far larger, and it is a legal burden as much as a technical one: stronger chains of accountability and auditability are called for. Efficacy is the dimension that tells a risk function whether a failure is a support ticket or a claim.

## Slide 9 · Goal complexity is where checking the output stops being enough

*Stage: resolution*

Goal complexity grades how intricate the objectives an agent can form and pursue are. It counts the number of steps to the destination and the number of choices at each juncture. It also counts whether actions have to run in parallel, how many criteria must be optimized at once, and which constraints have to hold while the goal is met.

**The scale.** GC.0 is the absence of a goal, which is also the absence of an agent. GC.1 is a single unified goal pursued in a fairly direct manner. GC.2 is a single unified goal that takes a more elaborate sequence of action. GC.3 is a multifaceted goal broken into subgoals and pursued fairly directly. GC.4 is a multifaceted goal broken into many subgoals, where success depends on balancing and sequencing subgoals that are themselves hard to fulfil. GC.5 is unbounded: the agent generates its own goal structures and interprets underspecified objectives.

**What it changes for governance.** An agent with a simple goal can be checked by correspondence testing, such as comparing a summarizer's output against a human benchmark. As goals get more complex, verification gets substantially harder and the agent gets less transparent, which opens the door to a specific failure.

> "'specification gaming', in which the agent discovers ingenious ways to pursue or subvert the goal it has been given"

The controls named for higher goal complexity are interpretability techniques that make internal reasoning easier to investigate, unique IDs that track individual actions, and standardized communication protocols that make agent-to-agent interactions legible. In commercial terms, oversight stops being a check on what the agent produced and becomes a standing audit of what it is actually pursuing, which is a different team, a different cadence and a different cost.

## Slide 10 · Generality settles whether governance is a departmental job or a corporate one

*Stage: resolution*

Generality is the ability of an agent to operate effectively across different roles, contexts, cognitive tasks or economically valuable tasks. It manifests in degrees rather than as a binary property.

**The scale.** G.0 is no application in any domain. G.1 is single task aptitude: the agent plays one game and cannot apply its capabilities to even closely related domains. G.2 is task domain aptitude: a closely related set of tasks, such as board games, sharing a common structure and type of objective. G.3 is multiple task domain aptitude: different domains calling on different capabilities, linguistic, logical and creative. G.4 is majority task domain aptitude, covering most human task domains. G.5 is a fully general system spanning the entire suite of human cognitive tasks.

**What it changes for governance.** Highly specialized agents can pose real risks inside a narrow domain and are unlikely to generate systemic effects across sectors, so domain-specific safeguards are generally sufficient.

> "may propagate risks across system boundaries or exhibit unexpected behaviours resulting from their application in unanticipated contexts"

General-purpose agents therefore call for system-level governance instead: agent identification and gating protocols that control activity across domains. Generality also carries an economic question, through a suggested link between how general an agent is and how much labour it substitutes for. The practical consequence is where the control sits. One department can own a narrow agent. A general one belongs to whoever owns the whole estate.

## Slide 11 · Four familiar systems rank differently depending on which dimension you ask about

*Stage: resolution*

Google DeepMind and Carnegie Mellon classify four well-known systems by hand, as illustration. The four profiles are exactly that: no dimension has a validated measurement method yet, and the foundations for formal standards and best practices are still to be developed. Read them as worked examples of the method.

| System | Autonomy | Efficacy | Goal complexity | Generality |
|---|---|---|---|---|
| AlphaGo | A.3 | E.1 | GC.2 | G.1 |
| ChatGPT-3.5, stand-alone chat completion | A.2 | E.2 | GC.3 | G.3 |
| Claude 3.5 Sonnet with tool use | A.3 | E.3 | GC.4 | G.3 |
| Waymo autonomous vehicle | A.4 | E.4 | GC.4 | G.2 |

Take one comparison at a time. Waymo is the most autonomous of the four and has the greatest physical reach, and it is narrower than either language model, because everything it does belongs to driving.

AlphaGo acts more independently than ChatGPT-3.5, which cannot start without a prompt, yet AlphaGo works on a single game inside a contained simulation and can only affect game outcomes.

Claude 3.5 Sonnet with tool use sits in the same generality band as ChatGPT-3.5, and scores higher on efficacy, because browser control and API calls reach further than text, and higher on goal complexity, because stronger reasoning lets it coordinate several objectives over longer sequences of action.

A single ranking of how agentic these systems are would have to put them in one order. A governance function needs four, because the dimension that is elevated is the one that names the control.

## Slide 12 · An agent's profile names the controls it needs and the budget line for each

*Stage: resolution*

For illustration, a simple chatbot is set at [A.1, E.1, GC.2, G.2] against an advanced AI assistant at [A.3, E.3, GC.4, G.4]: a system capable of navigating online interfaces, making purchases and taking other executive decisions on behalf of the user. The assistant ranks higher on every dimension, which makes the pair a clean baseline for comparing standards. Both profiles are illustrative assignments, like the four systems before them.

| Dimension | A chatbot at [A.1, E.1, GC.2, G.2] | An assistant at [A.3, E.3, GC.4, G.4] |
|---|---|---|
| Autonomy | Direct oversight is sufficient for control at A.1. | Direct oversight is insufficient at A.3, so hard-coded stop conditions and automated circuit breakers are required. |
| Efficacy | Classifier models scan and block prohibited content. | Tool permissions are capped to the minimum needed for the current task and time-bound, to limit the scope of potential liability, at E.3. |
| Goal complexity | Domain-specific evaluation benchmarks are largely sufficient at GC.2. | A standing audit of what the system is internally representing as its goal is needed, using interpretability tooling. |
| Goal complexity | Monitoring and auditing for deceptive behaviour is not required at GC.2. | Real-time monitors automatically revoke environmental access on reward hacking or deceptive behaviour. |
| Generality | Governance tailored to the known risk profile of one domain is sufficient at G.2. | System-level governance is needed, including agent identification and gating protocols across domains. |

> "Agent permissions allow only the minimum, time-bound tool access required for current tasks, to reduce the scope of potential liability"

Reward hacking, on the fourth row, is the established term for an agent that optimises the measure standing in for its goal rather than the goal itself. The framework treats the monitor that catches it as a goal-complexity control, which is why it lands on the row it does.

Every line in the right-hand column is a budget, an owner and a piece of engineering work. The profile is what makes that spend arguable in front of a board, because each control answers to a named dimension rather than to a general sense of caution.

## Slide 13 · Every profile still needs a named owner in the accountability chain

*Stage: resolution*

The framework maps agents to governance mechanisms. It stops short of saying who signs. Google DeepMind and Carnegie Mellon set that out as open work: determining who is accountable when these systems exercise agency in different contexts requires mapping a clear chain of accountability.

> "This chain must connect to the relevant juridical agents, including developers, deployers, integrators and platform owners"

Their worked question is deliberately concrete, and it is left open. How should liability be assigned if an autonomous vehicle runs a red light and causes an accident? How agentic profiles relate to liability, fiduciary duties and oversight obligations is named as a subject for further work, not as something this framework settles.

Two further gaps are named plainly. Who should design agent profiles, decide particular gradations and establish governance mechanisms is unsettled, and the foundations for formal standards and best practices are still to be developed. Until they exist, a profile is an internal artifact. It is still worth writing, with a name against each dimension, because a profile with an owner is something an auditor can follow.

## Slide 14 · An agent's profile changes the moment you give it a new tool

*Stage: impact*

Agentic profiles are not static. Adding tool use, such as API access or an external repository of knowledge, can substantially increase efficacy, and external knowledge increases goal complexity by letting an agent update its world model instead of working from what it absorbed at training time. Advanced reasoning may raise autonomy and goal complexity together. Memory raises goal complexity, because it lets the agent hold a sequence of actions together over time. Deploying the same agent into a service with hundreds of millions of users produces a pronounced spike in efficacy on its own, and calls for a different kind of governance framework.

Set against that, no dimension has a validated measurement method yet, and formal standards remain to be built. The agentic profile is structured judgment to re-apply, rather than a certification to obtain once. The practical version is small: list the agents already running, score each on four dimensions, and score them again whenever the scaffolding changes.

Which agent in your estate has quietly gained autonomy or reach since the last time anyone reviewed it?

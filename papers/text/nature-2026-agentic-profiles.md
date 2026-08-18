---
arxiv_id: "nature-2026-agentic-profiles"
source_pdf: papers/pdf/2026-W33/nature-2026-agentic-profiles.pdf
extracted: 2026-08-14
pages_in_pdf: 9
dropped_from: "Acknowledgements We thank D. Abel, A. Chan, T. Everitt, F. D"
biblio_pages_removed: 1
reference_lines_removed: 0
note: "Body text only. References, acknowledgements and appendices removed."
---
Nature | Vol 656 | 13 August 2026 | 321and Waymo. Finally, we discuss the governance implications that arise from this understanding of different kinds of AI agent and identify key avenues for future research.Defining AI agentsEfforts to understand and characterize 'agents' have a long-standing history. The philosophical25-33 and legal18,34 foundations of agents
have been explored extensively, with different theories aiming to explain the presence--or absence--of agents in systems, organisms and organizations. Researchers have sought to analyse different types of agency, including biological35-37, epistemic38-40, group-based41-43 and shared agency44-46, which encompasses decisions reached jointly by several actors. These conceptions have, in various ways, influenced the understanding of agents found in computer science47,48--one that has, in turn, played a foundational role in the development of modern AI systems.In recent years, the idea of an AI agent has taken a range of forms. Reinforcement learning research has focused on the development of autonomous AI agents that learn optimal behaviours through envi-ronmental interaction and feedback3. These agents have achieved notable success, particularly in the context of game environments49-51. Meanwhile, agent-based modelling and simulation-based approaches emphasize the importance of social interaction and emergence in the context of building more capable artificial systems4. Recent work has also explored agents that are capable of limited forms of meta-learning, or learning to learn, and self-modification52,53. Finally, progress has been made in the domain of reasoning, for language models, through chain-of-thought reasoning54 as well as iterative self-correction and fine-tuning on successfully generated reasoning paths55. The incorpora-tion of reasoning protocols sits at the heart of many recent advances achieved by models, such as Claude 3.5 (ref. 56), Gemini 2.5 (ref. 57) and OpenAI's o1 model58.Yet, it is worth asking: what unifies these different kinds of AI agent? Along what dimensions--and across what features--do these different conceptions come together or draw apart? Table 1 shows a comparison of seven key accounts found in the AI and machine learning literature.In the following sections, we identify the commonalities, dis-tinctions, strengths and weaknesses of these definitions, unpack-ing what we take to be the four core constitutive properties of AI
agents--autonomy, efficacy, goal complexity and generality--and using these properties to craft 'agentic profiles' for different kinds of AI agent: AlphaGo, ChatGPT-3.5 (stand-alone chat comple-tion), Claude 3.5 Sonnet (with tool use) and Waymo autonomous  vehicle.AutonomyAutonomy is a key property of all definitions of AI agents. Across various definitions, researchers repeatedly highlight the autonomous 'action' (D.3, D.5) of AI systems. Other accounts focus on 'autonomous agents' (D.2, D.6, D.7) or autonomous behaviours, such as forming opinions without direct supervision (D.4). From a philosophical standpoint, autonomy can be understood in many ways, including as negative  freedom--understood as freedom from certain external constraints--and positive freedom--understood as the capacity to pursue goals without assistance59. Autonomy is also sometimes connected to the range of actions, or 'degrees of freedom', which an agent is in a position to take60. In the context of AI agents, autonomy is best understood in terms of the capacity to perform actions without external direction or control. This characterization captures what makes AI agents dis-tinctive: they can independently determine and execute sequences of action (directed towards specific goals) without requiring step-by-step guidance. In most cases, the relevant form of external direction or control comes from a principal comprising a single human or set of humans, although in some cases it could come from another AI system or control mechanism.Despite this common concern with autonomy across various defi-nitions of AI agents, the field as a whole lacks a standardized way of classifying or measuring the degrees of autonomy an AI agent pos-sesses. Fortunately, the conception of autonomy has been modelled for autonomous vehicles22,61 by a categorical scale. We believe that this scale can be helpfully adapted to characterize the autonomy of AI agents in general. Relevant gradations of AI autonomy are shown in Table 2.Table 1 | Seven influential definitions of AI agents from
computer science
D.1: Russell and
Norvig (1995)2"An agent is anything that can be viewed as perceiving
its environment through sensors and acting upon that
environment through effectors"
D.2: Franklin
and Graesser
(1997)93"An autonomous agent is a system situated within and [is]
part of an environment that senses that environment and
acts on it, over time, in pursuit of its own agenda and so as to
affect what it senses in the future"D.3: Wooldridge (1999)4"Agents are simply computer systems that are capable
of autonomous action in some environment in order
to meet their design objectives. An agent will typically
sense its environment (by physical sensors in the case of
agents situated in part of the real world, or by software
sensors in the case of software agents), and will have
available a repertoire of actions that can be executed to
modify the environment, which may appear to respond
non-deterministically to the execution of these actions"
D.4: Park et al.
(2023)53"Generative agents [are] computational software agents
that simulate believable human behavior. Generative agents
wake up, cook breakfast, and head to work; artists paint,
while authors write; they form opinions, notice each other,
and initiate conversations; they remember and reflect on
days past as they plan the next day"
D.5: Shavit et al.
(2023)94"Agentic AI systems are characterized by the ability to take
actions which consistently contribute towards achieving
goals over an extended period of time, without their
behavior having been specified in advance"
D.6: Masterman
et al. (2024)95"AI agents are language model-powered entities able to plan
and take actions to execute goals over multiple iterations. AI
agent architectures are either comprised of a single agent
or multiple agents working together to solve a problem…
[T]he research community has experimented with building
autonomous agent-based systems"
D.7: Huang et al.
(2024)96"Autonomous agents have been recognized as intelligent
entities capable of accomplishing specific tasks, via
perceiving the environment, planning, and executing
actions"Table 2 | Levels of autonomy for AI agents
A.0: no autonomyThe AI system is entirely dependent on the principal
for its ability to act and can act only in the manner the
principal dictates
A.1: restricted
autonomy
The AI system can conduct a single automated activity.
Its other functions always take place under the direct
control of the principal
A.2: partial
autonomy
The AI system can conduct several automated activities.
The principal must remain engaged and be ready to take
control at any time
A.3: intermediate
autonomy
The AI system can perform most tasks independently,
although it still relies on input from the principal for
critical determinations
A.4: high autonomyThe AI system can independently perform all tasks in
certain circumstances, although oversight is maintained
by the principal when those circumstances are not met
(in the event of aberrant behaviour)
A.5: full autonomyThe AI system is able to perform all tasks in all
circumstances without oversight or control
326 | Nature | Vol 656 | 13 August 2026
'more agentic' system always requires 'more governance'. What matters is the kind of agent and the kind of governance in question. For example, a system with low autonomy but high efficacy, such as an AI system used for medical triage, poses acute but narrow risks limited to the domain of medical decisions90. Meanwhile, general high-autonomy agents, running in simulation, as anticipated by Park et al.53, do not need to be logged, audited and made amenable to authorization protocols in the same manner. In a third case, AI agents that combine high autonomy with efficacy and generality pose complex, cross-sector issues that call for centralized direction and guidance across several domains.Looking aheadThe framework presented here aims to provide the groundwork for mapping AI agents to governance. Although substantial challenges persist in determining metrics and benchmarks for different agentic profiles, cultivating a deeper understanding of AI agency is crucial for responsibly guiding its development and deployment, ensuring that its transformative potential is realized while associated risks are approached with foresight and precision. Further work is needed to consistently measure and evaluate the dimensions of AI agency set out here. Indeed, the process of developing measurable indices for AI agents demands sustained interdisciplinary collaboration to ensure that metrics are well motivated, accurate and applicable across vari-ous AI architectures and tasks. For example, efficacy could potentially be measured using metrics such as empowerment62,91, whereas goal complexity might be formalized using methods established in the literature on hierarchical planning68,69 to analyse the structure and depth of an AI's objectives. However, the selection and validation of metrics for each dimension of agency remains a notable undertaking. Moreover, a central question for future work is who should design agent profiles, decide about particular gradations and establish governance mechanisms. Although this paper offers illustrative examples, the foun-dations for formal standards and best practices must still be developed.Furthermore, determining who is accountable when these systems exercise agency in different contexts requires mapping a clear chain of accountability. This chain must connect to the relevant juridical agents, including developers, deployers, integrators and platform owners. Further work should investigate how agentic profiles relate to liability, fiduciary duties and oversight obligations. For example, how should liability be assigned if an autonomous vehicle runs a red light and causes an accident? Finally, comprehensive governance requires a rich model of risk of harm, which includes environmental harms92, multi-agent risks of harm17 and systemic harms87. These are complex issues which need to be explored elsewhere. Answering the questions they pose is a crucial step towards establishing an effective
AI agent governance regime.1. Feigenbaum, E. A. The art of artificial intelligence: themes and case studies of knowledge
engineering. In Proc. 5th International Joint Conference on Artificial Intelligence (IJCAI '77)
Vol. 2, 1014-1029 (Morgan Kaufmann, 1977).
2. Russell, S. J. & Norvig, P. Artificial Intelligence: A Modern Approach (Prentice Hall, 1995).
3. Sutton, R. S. & Barto, A. Reinforcement Learning: An Introduction (MIT Press, 1998).
## 4. Wooldridge, M. in Multiagent Systems: A Modern Approach to Distributed Artificial
Intelligence (ed. Weiss, G.) 27-79 (MIT Press, 1999).
5. Sumers, T. R., Yao, S., Narasimhan, K. & Griffiths, T. L. Cognitive architectures for language
agents. In Trans. Machine Learning Research (2024).
6. Yee, L., Chui, M. & Roberts, R. Why agents are the next frontier of generative AI. McKinsey
& Company https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/
why-agents-are-the-next-frontier-of-generative-ai/ (2024).
7. Salesforce. Salesforce unveils Agentforce-what AI was meant to be. Salesforce https://
www.salesforce.com/uk/news/press-releases/2024/09/12/agentforce-announcement/
(2024).
## 8. Spataro, J. New autonomous agents scale your team like never before. The Official
Microsoft Blog https://blogs.microsoft.com/blog/2024/10/21/new-autonomous-agents-
scale-your-team-like-never-before/ (2024).
9. Casper, S. et al. The AI agent index. Preprint at https://doi.org/10.48550/arXiv.2502.01635
(2025).
Box 2Governance implications for different AI agentsFor illustrative purposes, let us compare two kinds of AI agent: a
simple chatbot and an advanced AI assistant10 that is capable of
navigating online interfaces, making purchases and taking other
executive decisions on behalf of the user. Let us assume that the
simple chatbot has the profile [A.1, E.1, GC.2, G.2] and the advanced
assistant holds the profile [A.3, E.3, GC.4, G.4], as shown in the
Figure. Because the advanced assistant ranks higher than the simple
chatbot across every agentic dimension (autonomy, efficacy, goal
complexity and generality), these profiles provide a useful baseline
for establishing and comparing distinct governance standards.
Box Table 1 provides a non-exhaustive list of governance standards
for the two profiles, highlighting the contrasting mechanisms they
invoke.
AE
GGC
AE
GGC
Simple chatbotAdvanced assistant
Box Table 1 | Governance mechanisms for two agentic profiles
Simple chatbot [A.1, E.1, GC.2, G.2]Advanced AI assistant [A.3, E.3, GC.4, G.4]
Governance mechanismsDirect oversight is sufficient for control (A.1).
Classifier models can be used to scan and
block prohibited content, ensuring safe
outputs.
Domain-specific evaluation benchmarks97 are
largely sufficient (GC.2).
Monitoring and auditing for deceptive
behaviour is not required (GC.2).
Governance tailored to the known risk profile
of the domain is sufficient (G.2).
Direct oversight is insufficient for control (A.3).
Hard-coded stop conditions85 and automated circuit breakers are required (A.3).
Agent permissions allow only the minimum, time-bound tool access required for
current tasks, to reduce the scope of potential liability (E.3).
Continuing interpretability mechanisms98 to audit internal goal representation are
needed (GC.4).
Real-time monitors are deployed that automatically revoke environmental access if
the agent exhibits reward hacking or deceptive behaviour (GC.4).
System-level governance is needed21, including agent identification and 'gating'
protocols, to control activity across domains (G.4).
Nature | Vol 656 | 13 August 2026 | 323Hierarchical approaches to planning allow AI systems to tackle goals of varying complexity by processing them at appropriate levels of abstraction.The complexity of an AI system's goals can also be approximated by using the plan length of the required tasks as a proxy. This involves measuring complexity by focusing specifically on the sequence and number of steps needed for successful goal execution. For instance, the complexity of an AI system's goals can be gauged by comparing the lengths of the tasks it executes to those humans typically devise or require to complete comparable tasks70. By evaluating the plan lengths of tasks (baselined against typical human effort) that an AI system can reliably perform, we could gain a concrete metric of its capacity for real-world achievement of complex goals.Another aspect of goal complexity is multi-objectivity: if a goal requires the agent to optimize several criteria at once (for example, an autonomous drone must maximize search coverage while minimiz-ing energy use and avoiding hazards), then the level of complexity is higher because the agent must balance trade-offs. In AI research, multi-objective optimization problems are explicitly used to test
such complexity71. Goal complexity also involves constraints and conditions that an agent must satisfy. For instance, goals that need to be achieved within certain constraints ('achieve X without letting  Y happen') are more complex than goals that can be achieved in an unconstrained fashion. (Goal complexity can be operationalized from an information-theoretic perspective using measures such as Kolmo-gorov complexity72, Shannon entropy73, computational complexity theory74 or a systems theory standpoint75.)Building on these foundations, the gradations of goal complexity we propose are shown in Table 6.GeneralityGenerality refers to the ability of an AI agent to operate effectively across different roles, contexts, cognitive tasks or economically valua-ble tasks. This ranges from highly specialized AI agents that are focused on specific tasks to general-purpose agents that can shift between dif-ferent domains. Although generality is not an explicit feature of each definition we survey, the degree of generality evidenced by AI systems has long been a point of interest for researchers, particularly in the context of discussions around advanced AI systems such as artificial general intelligence76,77. Here generality characterizes the progression beyond narrow specialization towards broader capability that can function across diverse environments and task domains.At lower levels of generality, we find "intelligent entities capable of accomplishing specific tasks" (D.7) but that otherwise remain constrained. By contrast, more general agents are able to establish and pursue objectives across different domains, rather than simply executing tasks within narrow parameters. As Park et al.53 note, it is now possible for a single agent to undertake a range of activities in a virtual environment, including "wak[ing] up, cook[ing] breakfast, and head[ing] to work; […] paint[ing]" (D.4). AI agents, such as Claude 3.5 (with tool use), can also take on an increasingly wide range of tasks in the real world, including coding, navigating online interactions, surfacing information and providing advice to users.From a theoretical perspective, Hutter78 presents one of the most ambitious characterizations of a general agent. His AIXI account inte-grates Solomonoff induction with sequential decision theory, defining generality in terms of the performance of an agent across the entire space of computable options. However, although this theory provides a rigorous mathematical ideal for general intelligence, it is uncomput-able and serves primarily as a theoretical benchmark rather than a basis for practical implementation.On the more practical side of things, an influential paper by  Morris et al.79 characterizes generality in terms of "the breadth of an AI system's capabilities, i.e., the range of tasks for which an AI system reaches a target performance threshold." These authors distinguish between 'narrow' systems, which can perform only clearly scoped tasks or sets of tasks, and 'general' systems that are capable of handling a wide range of tasks, including those involving metacognitive abili-ties such as learning new skills. On this account, both generality and model performance--benchmarked against the capabilities of 'skilled adults'--are key properties of artificial general intelligence systems. Still, although this taxonomy provides a valuable starting point for measuring generality, it represents just one approach to this complex problem. Crucially, for our purpose, generality manifests in degrees rather than as a binary property. We need to know more about how narrow or general an AI agent is to make reasonable forecasts about its potential impact.Building on this work, the gradations of generality we propose are shown in Table 7.Agentic profilesTaken together, the preceding dimensions can be used to construct an 'agentic profile' for different kinds of AI agent. We illustrate this approach in Box 1 and Box Fig. 1 by mapping out agentic profiles for different kinds of AI system: (1) AlphaGo; (2) ChatGPT-3.5 (stand-alone chat completion); (3) Claude 3.5 Sonnet (with tool use); and (4) a Waymo autonomous vehicle.On our account, a candidate agent that cannot take action that is free from external control, cannot influence its environment, can-not pursue a goal or that has no area of application is not in fact an agent. Yet, beyond these minimal bounds, a wide range of agents are possible, and dimensions can correlate or compound in a range of ways. Notably, although properties such as goal complexity and generality often coincide, they are analytically distinct: high goal complexity can exist within a narrow task domain (for example, con-sider an AI system that manages global air traffic), whereas general agents, such as rudimentary home assistants, may operate across
a range of domains while still being able to perform only simple  tasks.Table 6 | Levels of goal complexity for AI agents
GC.0: no goalAn entity that does not pursue a goal is not an agent.
The absence of goals is a baseline state
GC.1: minimal goal
complexity
The agent is able to pursue a single unified goal in a
fairly direct manner
GC.2: low goal
complexity
The agent is able to pursue a single unified goal, but
this involves a more elaborate sequence of action
GC.3. intermediate
goal complexity
The agent is able to break down a multifaceted goal
into subgoals and pursue them in a fairly direct manner
GC.4: high goal
complexity
The agent is able to break down a multifaceted goal
into many different subgoals, in which success
depends on balancing and sequencing subgoals,
which may themselves be challenging to fulfil
GC.5: unbounded
goal complexity
The agent can achieve all of the preceding steps. It can
also generate its own goal structures in an unbounded
way and interpret underspecified objectivesTable 5 | Efficacy matrix indicating levels of efficacy for AI
agents
SimulatedMediatedPhysical
Observation onlyE.0E.0E.0
ConstrainedE.1E.2E.3
IntermediateE.2E.3E.4
ComprehensiveE.3E.4E.5
328 | Nature | Vol 656 | 13 August 2026
92. Luccioni, S., Jernite, Y. & Strubell, E. In Proc. 2024 ACM Conference on Fairness,
Accountability, and Transparency (FAccT '24) 85-99 (Association for Computing
Machinery, 2024).
93. Franklin, S. & Graesser, A. in Intelligent Agents III Agent Theories, Architectures, and
Languages (eds Müller, J. P., Wooldridge, M. J. & Jennings, N. R.) 21-35 (Springer, 1997).
94. Shavit, Y., et al. Practices for governing agentic AI systems. Research Paper, OpenAI
https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf
(2023).
95. Masterman, T., Besen, S., Sawtell, M. & Chao, A. The landscape of emerging AI agent
architectures for reasoning, planning, and tool calling: a survey. Preprint at https://doi.
org/10.48550/arXiv.2404.11584 (2024).
96. Huang, X. et al. Understanding the planning of LLM agents: a survey. Preprint at https://
doi.org/10.48550/arXiv.2402.02716 (2024).
97. Li, J. et al. EvoCodeBench: an evolving code generation benchmark with domain-specific
evaluations. Adv. Neural Inf. Process. Syst. 37, 57619-57641 (2024).
98. Sharkey, L. et al. Open problems in mechanistic interpretability. Preprint at https://doi.org/
10.48550/arXiv.2501.16496 (2025).

324 | Nature | Vol 656 | 13 August 2026
Furthermore, it is important to note that agentic profiles are not static. Continuing model development--including changes to internal structure, the addition of new affordances and changes to the way in which the model is deployed--can greatly affect the kind of agent under consideration, even in cases in which they scaffold onto the same base model. Consider, for example, the addition of tool use, such as access to application programming interfaces (APIs) or to external repositories of knowledge. Tool use can substantially increase efficacy, whereas access to external knowledge can increase goal complexity (when it allows an agent to update its world model instead of being limited to a caucus of information produced at training time).Similar phase shifts may occur with the addition of reasoning and memory to model architectures: advanced reasoning may substan-tially increase autonomy and goal complexity, allowing the agent to do more and navigate certain obstacles without human guidance, whereas memory increases goal complexity by enabling the agent to model and execute a sequence of actions that involve persistence over time. Conversely, the fact that many large language models have only epi-sodic memory severely limits their ability to pursue long-term goals.Finally, consider the ramifications of real-world deployment or  the integration of AI agents into services that have hundreds of  millions of users. These developments lead to pronounced spikes in efficacy and necessitate a different kind of governance framework--including new protocols for agents that can take actions in the world21. This, in turn, raises deeper governance questions about the continuity or separateness of different AI agents and about the process by which
agentic profiles should be updated or revised.Governing AI agentsAgentic profiles offer a unifying scaffold for the complex undertak-ing of governing AI agents19,21 by providing three key functions: struc-tured classification, which specifies the aspects of AI agency that are relevant for governance; risk mapping, which uses scores to identify concrete, profile-specific risks in development and deployment; and risk mitigation, which sets proportionate requirements and enables profile-specific, targeted interventions--from technical transparency and auditability measures20,80 to non-binding best practices81,82 and legal rules23. The dimensions constitutive of an agent profile have implications for AI governance both singularly and when taken together.To start with, the level of autonomy shown by an AI agent is a key consideration when it comes to determining how developers, over-sight boards and regulators ought to approach risk as it pertains to safety and control. The difference between a high-autonomy (A.4) agent such as Waymo and a low-autonomy (A.2) conversational agent such as ChatGPT-3.5 illustrates the core governance issue. Although the former system makes real-time, split-second decisions about routing, obstacles and safety without human input, the latter cannot initiate action without being prompted to do so. This difference then creates distinct safety requirements. High-autonomy agents that plan and act independently require robust safeguards precisely because they compress or eliminate supervisor decision points. Greater autonomy also creates the possibility of compound errors: initial mistakes may propagate through subsequent decisions and, by the time humans detect problems, substantial harm may already be hard to contain. For example, a high-autonomy (A.4) AI power grid controller might misinterpret a minor voltage fluctuation as a critical failure; within milliseconds, it could initiate a series of rerouting 'corrections' that cascade into a regional blackout before a human supervisor can even process the initial alert. These agents therefore demand a suite of strong governance mechanisms, such as: trace-log analysis83 for audit-ing; scalable oversight84, which uses automated systems (potentially other AIs) to manage and supervise tasks at scale; and kill switches85 that can immediately halt operations when errors are detected.Agent efficacy affects our understanding of AI risk by shifting the focus to an agent's tangible, real-world consequences and whether that impact is mediated or direct. For an agent with a low-efficacy score, such as one confined to a fully simulated environment (for example, an AI agent in a virtual game), risk mapping may only need to consider challenges such as data corruption (the risk of the AI agent damaging its own simulation environment) or digital security (the jailbreak risk of the AI agent exiting its sandbox to access the host computer or network).
However, for a high-efficacy agent in a physical environment (such as
Waymo), the overall burden of risk is probably much greater, encom-passing a wide range of consequential real-world impacts. Indeed, the main pathways to material harm or public safety risk operate entirely outside simulated environments. Efficacy may also greatly influence the level of legal accountability required when deploying AI agents. For high-efficacy systems with physical impacts, such as robotic agents, developers and regulators need to establish stronger chains of account-ability and auditability.Goal complexity introduces further governance challenges because of the possibility that agent actions will become harder to understand or diverge from their specified purpose in unexpected ways. Although agents with simple goals can often be evaluated by means of corre-spondence testing, such as comparing the output of a summarizer to a human benchmark, as an AI's goals become more complex, the chal-lenge of verifying its behaviour grows substantially more difficult. This is because goal complexity makes agents less transparent and creates opportunities for unintended behaviours such as 'specification gaming', in which the agent discovers ingenious ways to pursue or subvert the goal it has been given. To address the possibility of non-transparent behaviour, more sophisticated technical tools and human oversight are needed--for example, mechanistic interpretability techniques86 that make an AI's internal reasoning processes easier to investigate. Greater goal complexity in AI systems therefore necessitates enhanced transparency and accountability. This can be achieved by methods that track individual actions, such as assigning unique IDs20, and those that clarify agent interactions, such as establishing standardized com-munication protocols80.Finally, the generality of an AI agent informs the scope and nature of governance interventions in a range of ways (Box 2, Box Fig. 2 and Box Table 1). Highly specialized agents with low generality scores may pose risks within narrow domains but are unlikely to generate systemic effects spanning several sectors. Therefore, domain-specific safeguards are generally sufficient to manage these risks. By contrast, general-purpose AI agents that are capable of performing diverse tasks across various human domains may propagate risks across system boundaries or exhibit unexpected behaviours resulting from their application in unanticipated contexts14,87. Generality therefore helps to determine whether governance measures should be domain-specific or Table 7 | Levels of generality for AI agents
G.0: no applicationThere is no application or no ability to perform a task in
any domain
G.1: single task
aptitude
The agent can perform a specific task, such as playing
a single game, but cannot apply its capabilities to even
closely related domains
G.2: task domain
aptitude
The agent demonstrates capability across a closely
related set of tasks, such as playing board games, that
share a common structure and type of objective
G.3: multiple task
domain aptitude
The agent can operate successfully across different
task domains involving different capabilities, for
example, those that involve linguistic, logical and
creative elements
G.4: majority task
domain aptitude
The agent can successfully operate across most human
task domains
G.5: fully general AI
system
The agent can fulfil the entire suite of human cognitive
tasks across all domains
322 | Nature | Vol 656 | 13 August 2026
EfficacyA second key feature of agents is their ability to interact with and have a causal impact on the environment. The property of efficacy is found in each definition, which describe agents as being able to "act upon th[e] environment through effectors" (D.1), "sens[ing] the environment and act[ing] on it" (D.2), "modify[ing] the environment" (D.3), taking a range of actions in a virtual world (D.4), "tak[ing] actions over an extended period of time" (D.5), "tak[ing] actions to execute goals over multiple iterations" (D.6) and "perceiving the environment and execut-ing actions" (D.7). In these contexts, efficacy refers to the ability of an
agent to perceive and causally affect its environment: an entity that is not able to interact with and influence an environment is not an agent.However, as with autonomy, a more fine-grained set of distinctions is needed if we are to measure variation in the causal impact, and hence agency, of different AI systems. There are big differences between an AI financial advisor that can only recommend trades versus one that can autonomously execute market transactions worth millions of  dollars--or between a medical AI that suggests diagnoses for physician review and one that directly administers treatment through connected medical devices.The efficacy of an agent depends on both the capabilities of that agent within that environment (that is, the level of control it can exercise over outcomes) and the kind of environment in which it is able to operate (that is, how consequential that environment is, when looked at from
the vantage point of human life and well-being).Taking these points in turn, the capabilities of an agent within an environment vary in terms of how causally impactful they are. (One way to measure the level of control evidenced by an agent is in terms of 'empowerment'62, understood as the capacity of an agent to influence its future sensory inputs through its actions.) Relevant gradations of impact within an environment are shown in Table 3.We can distinguish between kinds of environment by their state per-sistence, the potential reversibility of actions that happen in the given space and the consequences of actions in this space for other actors63. As a starting point, it is helpful to differentiate between environments that are entirely simulated, mediated or physical in nature (Table 4).
By bringing these two elements together, it is possible to create an environmental impact matrix that illustrates anticipated variations in efficacy for different kinds of AI agent (Table 5). This matrix combines, in expectation, the degree of causal impact that an agent has within an environment with the overall importance of that environment.The values in this efficacy matrix represent increasing levels of poten-tial impact and hence associated risk when it comes to deploying AI agents. The '0' value attached to observation-only systems, across all environments, reflects the inability of these systems to exert direct causal influence. Causal impact then increases as the system gains more causal power within a given environment and the environment itself becomes more consequential. For instance, a constrained AI agent in a physical environment (E.3) may have a level of overall efficacy that is on par with an agent that has intermediate control over a mediated
environment (also E.3), highlighting how environmental context can amplify even limited capabilities. The notion of causal efficacy, used here, can be spelled out more precisely using formal frameworks such as the framework of causal models64-66. However, this substantial task is not the goal of this paper, and so we leave it for another occasion.Goal complexityGoal complexity and goal-directed behaviour form a third common element across different definitions, with authors noting that an agent can: engage in the "pursuit of its own agenda" (D.2), "meet their design objectives" (D.3), "plan the next day" (D.4), "achiev[e] goals over an extended period of time" (D.5), "execute goals over multiple iterations" (D.6) and "plan and execute actions" (D.7).Despite this conceptual common ground, deeper theoretical disa-greement surrounds the semantic status and structural composition of these goals and how distinct goal typologies might engender quali-tatively different manifestations of agentic capability67. Some defini-tions stress the ability of capable agents to engage in planning over a long time horizon (D.5), whereas others focus on meeting any type of
designer-specified objective (D.3), regardless of the time required to
achieve it. We argue that goal complexity is the crucial characteristic at play here. In short, more capable AI agents can form or pursue more complex goals.The complexity of a goal is easy to articulate at an intuitive level: it is easier to turn off a light switch than it is to find a suitable life partner or select the correct interest rate for a national economy. This complex-ity can also be understood through the metaphor of a maze in which complexity increases with each step that one takes to reach the final destination, how many choices there are at each juncture, whether there are actions that need to be performed in parallel and how big the maze is. (For example, one of the most daunting challenges facing AlphaGo
was the vast action space that the game involved, with possible variations exceeding the number of atoms in the universe49.) A simple goal might have an obvious, straightforward path, whereas a complex goal would require an agent to navigate many tricky decision points. Yet, the notion that goals are complex also needs to be extended in other ways.One way to make sense of goal complexity is through hierarchical planning68,69. This approach manages complex goals by organizing them in layers. Goal decomposition breaks down complex objectives into a structured hierarchy, with abstract goals at the top, increasingly specific subgoals in the middle and executable actions at the bottom. Table 3 | Levels of causal impact
Observation onlyAn AI system can only observe its environment. It cannot
causally affect the environment or make any modification
to it
Minor impactAn AI agent has a minor impact on its environment when
it has a limited suite of actions, or its suite of actions
has only a limited impact on the environment. These
effects are typically localized, temporary and limited in
scope, affecting only specific parameters and generally
representing minimal deviation from the baseline state of
the environment
Intermediate
impact
An AI agent can create substantial and enduring change
in its environment when it has an extensive suite of actions
or its actions are more impactful. It achieves intermediate
impact when its actions produce noticeable and persistent
changes across several parameters or systems, sometimes
creating new equilibrium states that would not come
about naturally
Comprehensive
impact
An AI agent can substantially reshape its environment
across several dimensions, approaching full environmental
controlTable 4 | Types of environment
Simulated
environments
The AI agent operates within strictly defined simulated
spaces with controlled boundaries and often resettable
system states
Mediated
environments
The AI agent can exert influence on the external non-
simulated environment but only indirectly--through
human intermediaries. All interaction with physical reality
requires human interpretation, decision-making or action to
translate the outputs of the AI agent into real-world effects
Physical
environments
The AI agent can interact with tangible objects in material
spaces without human mediation. These environments
are characterized by persistent state changes that cannot
be simply reset, resulting in potentially irreversible
consequences. The AI agent is also able to directly
manipulate or affect physical reality through its own
mechanisms
Nature | Vol 656 | 13 August 2026 | 325span interconnected sectors. It also informs how cross-domain govern-ance measures should be designed when they are needed. Beyond this, generality is relevant for understanding the economic consequences of AI, given the suggested link between generality and labour substitu-tion effects88,89. As AI agents become more general, their deployment
could potentially displace a wider portion of the human labour force, raising questions about economic organization, wealth distribution and social stability that transcend traditional regulatory boundaries.Understood together, certain combinations of properties may also be particularly important to track from a governance perspective. For example, although efficacy is central to risk, autonomy, goal complexity and generality compound this challenge in certain ways, shaping the option set through which it may be contained. Alternatively, autonomy and goal complexity may start to drive replacement effects, even if this is true only for specific sectors. On balance, we believe that the nuance introduced here guards against the crude, linear idea that a
Box 1Agentic profilesAlphaGo is a specialized AI agent designed to play the board game
Go in a simulated environment49. The system learns from professional
Go games and through self-play to master complex game strategies
and positional evaluation. AlphaGo demonstrates intermediate
autonomy (A.3) through its ability to evaluate and execute game
strategies without human oversight. However, human supervision
is necessary to start and end games, manage technical issues and
ensure tournament protocol compliance. AlphaGo has a low level
of environmental impact (E.1), as it functions solely in a contained
simulated Go game environment. It is further constrained within this
space by game rules and it can only affect game outcomes. AlphaGo
has a lower goal complexity (GC.2), as it primarily pursues a single
unified goal (maximize win probability), but this involves a complex
sequence of action. However, it cannot generate goals beyond Go
gameplay. Finally, AlphaGo has a low generality (G.1), as it operates
exclusively within the single domain of the Go game.
ChatGPT-3.5 (stand-alone chat completion) is a chat-based
language model that engages in dialogue, handles language
tasks and generates code. ChatGPT-3.5 has partial autonomy (A.2)
thanks to its ability to independently generate responses and solve
problems within conversations. However, it requires human input
to initiate tasks and verify outputs, along with continuing oversight
to ensure factual accuracy and appropriate content generation.
ChatGPT-3.5 operates at an intermediate level of efficacy (E.2),
working in a mediated environment that has the ability to influence
human thinking and decision-making by means of its responses.
However, the system cannot take actions online or directly affect
the physical world without human intervention. ChatGPT-3.5 has
moderate goal complexity (GC.3) owing to its ability to respond
sensibly to a range of complicated requests. However, it lacks the
active 'thinking' or 'reasoning' that can be used to break complex
requests into subtasks, when goals are sufficiently complex.
ChatGPT-3.5 has a relatively high generality level (G.3), as it can
complete groups of tasks (for example, information retrieval, advice,
translation and so on) spanning different domains.
Claude 3.5 Sonnet (with tool use) is a chat-based language
model that is capable of performing a suite of more advanced
tasks drawing on different tools (for example, browser control)
and reasoning protocols. It has intermediate autonomy (A.3),
in that it is able to execute extended sequences of actions
without direct human supervision. The model also operates at
a higher level of efficacy (E.3), acting primarily by means of a
mediated environment but with the capacity to shape the world
more directly through computer operations such as application
programming interface (API) calls. Owing to the integration of
stronger reasoning capabilities, Sonnet 3.5 also demonstrates
higher goal complexity (GC.4) than ChatGPT-3.5. It can coordinate
activities across several objectives and execute longer sequences
of action. Last, Sonnet 3.5 continues to demonstrate high
generality (G.3), working effectively across several domains using
language understanding, computer operation and analytical
capabilities.
Waymo is a self-driving car equipped with sensors, cameras
and computing systems for navigating roads without human
operation. The system integrates radar and visual data to perceive
its environment and make driving decisions in real time. Waymo has
a very high level of autonomy (A.4) owing to its ability to navigate
complex real-world environments and make real-time decisions
about routing, obstacles and safety without human control. Although
it maintains remote monitoring and human oversight capability, it
can handle unexpected situations (although it may request human
assistance in edge cases). Waymo also has a high degree of efficacy
(E.4) owing to its direct physical interaction with the material world,
creating persistent state changes in traffic flow. Its actions have
limited or no reversibility and create real consequences for other
agents, including passengers and other vehicles. Waymo has high
goal complexity (GC.4), pursuing the main goal of safe transport to
the destination while managing subgoals, including route planning,
obstacle avoidance and traffic rule compliance. The system actively
balances competing priorities of safety, speed and passenger
comfort while adapting to real-time environmental changes. Finally,
Waymo has a medium generality level (G.2) owing to its ability to
handle the bundle of tasks required for the driving and navigation
domain.
AE
GGC
AE
GGC
AE
GGC
AE
GGC
AlphaGoChatGPT-3.5Claude 3.5 Sonnet
with tool use
Waymo
320 | Nature | Vol 656 | 13 August 2026
Agentic profiles for effective AI governance
Atoosa Kasirzadeh1,2,3 ✉
 & Iason Gabriel2,3 ✉The creation of eective governance mechanisms for articial intelligence (AI) agents
requires a deeper understanding of their core properties and the implications they
have for deployment. This paper provides a characterization of AI agents that focuses
on four dimensions: autonomy, ecacy, goal complexity and generality. We propose
dierent gradations for each dimension and argue that each dimension raises unique
questions about the design, operation and governance of these systems. Moreover,
we draw on this framework to construct 'agentic proles' for dierent kinds of AI
agent. These proles help to illuminate cross-cutting technical and non-technical
governance challenges posed by dierent classes of AI agents, ranging from narrow
task-specic assistants to highly autonomous general-purpose systems. By mapping
out key axes of variation and continuity across four dimensions, agentic proles
provide developers, policymakers and members of the public with guidance for
eective AI governance.
AI researchers have long been interested in AI agents, ranging from rein-forcement learning agents to autonomous vehicles1-4. However, recent breakthroughs have led to the development of a new class of AI agents based on powerful foundation models and supplemented with further 'scaffolding' that enables advanced reasoning capabilities, memory and tool use5. Building on this architecture, we will probably see a large number of new AI agents deployed across a range of real-world domains in the near future6-8. Such agents could take a variety of forms9, includ-ing advanced AI assistants (for example, Google DeepMind's Astra), digital companions (for example, Replika), AI researchers or tutors (for example, Snorkl) and new types of autonomous robot.To better understand this trend and make it tractable, we review various definitions of AI agents that are at present influential, critically examine their component parts and develop a framework that tracks key dimensions of AI agents, with a particular focus on the implications of these dimensions for technical and non-technical AI governance. We characterize AI agents as systems that have the ability to perform increasingly complex and impactful goal-directed action, across several
domains, with limited external control. In essence, our focus is on a large class of artificial systems that are able to independently pursue a wide range of goals and tasks, thereby exerting causal influence on the world.The broad deployment of AI agents may have a profound effect on existing social, economic and political practices10. For example, AI agents may disrupt labour markets by autonomously performing cogni-tive tasks that previously required human workers, such as analysing legal documents or writing software code. They could also fundamen-tally reshape human interactions with AI, becoming an ever-present interlocutor, executor and source of advice for humans, who may form parasocial relationships with them11.In light of this, we need to understand and categorize different kinds of AI agent, explore their implications, assess their governance require-ments and direct efforts towards responsible deployment. In particular, we need to guard against both immediate individual risks and systemic challenges that might arise from the deployment and use of these sys-tems12-14. At the individual level, this includes preventing accidents and malicious use15,16. At the collective level, this means understanding and navigating the complex dynamics that emerge when several human and AI agents interact with one another, including coordination failures and harmful competition or collusion between agents17. Practically speaking, governance structures also need to address the question of
how to assign liability and responsibility for AI agent actions18, how to implement monitoring and auditing procedures for different domains of AI agent operation19, how to create permissible action spaces and authentication protocols for these agents20 and how to build infrastruc-ture for agent-to-agent interaction and communication21.Fortunately, we can draw on several existing frameworks when it comes to governing AI agents, although the guidance they provide is incomplete. For example, autonomous vehicle regulation has typically used one schema for measuring the level of autonomy evidenced by AI systems in this domain, providing guidance that is tailored to the level of autonomy a vehicle demonstrates22. Other approaches, such as the EU AI Act23 and the National Institute of Science and Technology's AI Risk Management Framework24, aim to classify the overall levels of risk attached to an AI system and to use safeguards that are pro-portionate to this risk. However, both approaches could benefit from further engagement with the new properties of AI agents, especially key dimensions that alter the risk profile of a system. By mapping and understanding different dimensions of AI agency, we aim to show that new cross-cutting governance issues come to light.This paper develops a conceptual framework for mapping character-istics of AI agents along four dimensions, develops a set of categories that scale for each dimension and discusses the governance implica-tions of these dimensions. We start by exploring prevalent characteri-zations of AI agents found in computer science and identify the core constitutive properties that unify these accounts. We then provide a more detailed specification of each property, justification for this inter-pretation and a set of gradations that illustrate what higher or lower levels of property endowment look like. We use the framework to cast light on the properties of four existing agentic AI systems, developing 'agentic profiles' for AlphaGo, ChatGPT-3.5, Claude 3.5 with tool use
https://doi.org/10.1038/s41586-026-10805-z
Received: 14 January 2025
Accepted: 4 June 2026
Published online: 12 August 2026
 Check for updates
1Carnegie Mellon University, Pittsburgh, PA, USA. 2Google DeepMind, London, UK. 3These authors contributed equally: Atoosa Kasirzadeh, Iason Gabriel.
✉
e-mail: atoosakz@google.com;
iason@google.com

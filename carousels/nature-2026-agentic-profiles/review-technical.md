# Technical review — revision 3

PRIMARY TEST
pipeline sketch (from memory):
  1. Diagnose the gap -- existing frameworks (EU AI Act, NIST AI RMF) sort a whole system into one risk tier; AV regulation grades one property (autonomy) on a scale -- needed because a single tier can't tell a governance function what kind of thing is acting, only how much it could cost.
  2. Survey seven influential AI-agent definitions (Russell & Norvig 1995 through 2024 LLM-agent surveys) -- needed to ground the framework's dimensions in existing literature rather than inventing them from scratch.
  3. Extract four constitutive properties -- autonomy, efficacy, goal complexity (near-universal across the seven, with goal complexity absent only from the 1995 definition) and generality (added, not inherited) -- needed because a single "how agentic" score conflates risk types that call for different controls.
  4. Build a graded 0-5 scale per dimension: autonomy adapted from the AV categorical scale; efficacy as a grid crossing causal-power level against environment consequentiality; goal complexity from step count/branching/parallelism/multi-objective/constraints; generality from breadth of task domains -- needed because the field has no standardized way to measure any of these, so each needs its own operational rubric before it's usable.
  5. Compose the four scores into an "agentic profile" (a vector, not a verdict), with a zero on any axis putting the system outside "agent" territory -- needed so governance can target the dimension actually driving risk instead of applying one blanket rule.
  6. Apply the scales by hand to worked examples (AlphaGo, ChatGPT-3.5, Claude 3.5 Sonnet with tool use, Waymo) -- needed to show the four-axis view separates systems a single ranking would conflate, while being explicit that no dimension yet has a validated measurement method.
  7. Map profiles to governance mechanisms (structured classification, risk mapping, risk mitigation), illustrated with a chatbot-vs-assistant comparison and dimension-specific controls (kill switches for autonomy, tool-permission caps for efficacy, interpretability audits for goal complexity, cross-domain gating for generality) -- needed because the point of separating the dimensions is that each elevated one names a specific, proportionate control.
  8. Flag what the framework leaves open -- accountability chains, liability (e.g. the Waymo red-light question), who governs the standards themselves -- explicitly future work, not resolved by scoring -- needed because a classification scheme doesn't by itself assign legal responsibility.
  9. Note profiles are dynamic -- tool use, reasoning, memory, and scale of deployment shift a system's scores -- needed because a governance decision anchored to a stale profile is wrong the moment the scaffolding changes.
gaps: none material. The deck explains the "why" at every stage I could reconstruct, including the efficacy grid's crossing logic and why a single agentic ranking fails.
had to reopen the deck to answer: no

SCORES
T1 mechanism: 5
T2 fidelity: 4
T3 traceability: 4
T4 scope: 5
T5 depth-pattern: 4
subtotal: 22/25

DEFECTS
blockers: 0
wrong: 1
majors: 0
overstated: 0
unverifiable: 1
minors: 2

Verification of the four targeted fixes: all four landed correctly. (1) Slide 5 now states autonomy and efficacy as present in "all seven"/"each one" and correctly isolates goal complexity's single exception at "the origin" (the 1995 Russell & Norvig definition, which indeed carries no goal language in the source's Table 1 comparison) -- this is now precise. (2) Slide 13 now frames the Waymo red-light question as something the paper "names... as a subject for further work, not as something this framework settles," matching the source's "Further work should investigate..." framing exactly -- no longer implies the profile answers it. (3) Slide 11 no longer makes any inter-rater reliability claim. (4) Slide 12 no longer states the reward-hacking/specification-gaming equivalence as the paper's own claim.

SLIDE 12 · wrong · the "Efficacy" row pairs the chatbot's "Classifier models scan and block prohibited content" control with the assistant's E.3 tool-permission control
  Box Table 1 in the source gives the assistant's tool-permission item an explicit (E.3) code, but the chatbot's classifier-models item carries no dimension code anywhere in the source. The deck's table places it under an "Efficacy" row aligned against the assistant's coded E.3 item, presenting a categorization the paper never makes for that item, with no caveat that this pairing is the deck's own inference. The writer's own report flagged this exact gap; the fix from the previous pass addressed the reward-hacking/specification-gaming equivalence but left this pairing unaddressed. It also undercuts the slide's own closing sentence, "each control answers to a named dimension rather than to a general sense of caution," which is not true of this one cell. The defect is bounded to this single row/cell; every other row in the table (autonomy, both goal-complexity rows, generality) carries the source's own dimension codes correctly.

SLIDE 12 · unverifiable · "Reward hacking... is the established term for an agent that optimises the measure standing in for its goal rather than the goal itself"
  Papers/text uses the term "reward hacking" exactly once, inside Box Table 1's GC.4 governance item, and never defines it. This specific definition traces to neither the paper nor a named external source. It is a real AI-safety term, so the claim is plausibly true, but as written it has no citation and none is offered, which is what "unverifiable" is for. The second half of the sentence, attributing the GC.4 label to the framework's own table, is correctly sourced.

SLIDE 14 · missing caveat (minor) · "Memory raises goal complexity, because it lets the agent hold a sequence of actions together over time"
  The source states this and, in the very next sentence, adds "Conversely, the fact that many large language models have only episodic memory severely limits their ability to pursue long-term goals." The deck drops that qualifier, leaving memory's effect on goal complexity as a cleaner, more general claim than the paper makes in the same breath.

T5 · minor · depth_pattern is declared `spec-cards`, but the deck does not use the Inputs / Model / Calibration / Outputs card structure the standard specifies for that pattern
  Substantively the deck complies with the underlying rule (numeric codes and thresholds are consistently confined to bolded technical sub-sections and tables, kept out of "what it changes for governance" business-consequence prose), so this is a template-naming deviation rather than a numbers-leakage problem. Worth flagging since the pattern is supposed to be a literal, evidence-accumulating choice per the writing standard, not a loose label.

This deck is close to defensible in front of someone who has read the paper: every scale, every table value, every quote I checked (autonomy Table 2, efficacy Tables 3-5 and the reproduced grid, goal complexity Table 6, generality Table 7, all four worked-example profiles in Box 1, the governance-mapping paragraphs, and all seven verbatim quotes) traces exactly, and all four previously-flagged issues are now fixed correctly rather than just superficially. The single biggest exposure is Slide 12's "Efficacy" row: it dresses up the deck's own inference as if it were the paper's coding, in a slide whose whole rhetorical claim is that "each control answers to a named dimension" -- which is the same failure mode (an invented categorical pairing) that the previous pass had to fix once already on this exact slide, just relocated to a different cell.

Files reviewed: `carousels/nature-2026-agentic-profiles/draft-carousel.md`, `papers/text/nature-2026-agentic-profiles.md`, `skills/carousel-production/writing-standards.md`.

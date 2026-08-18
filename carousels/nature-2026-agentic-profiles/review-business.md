# Business review — revision 3

PRIMARY TEST
so-what (one sentence, from memory): "Because agentic AI systems now get scored on four separate properties (autonomy, efficacy, goal complexity, generality) instead of one overall risk tier, a business can size its governance controls, spend and ownership to each agent's actual profile, instead of over-controlling harmless agents and under-controlling risky ones under a single blanket rule."
had to reopen the deck to answer: no

SCORES
B1 so-what: 4
B2 arc: 5
B3 accessibility: 3
B4 hook-close: 5
B5 credibility: 4
subtotal: 21/25

DEFECTS
blockers: 0
wrong: 0
majors: 6
overstated: 0
unverifiable: 0
minors: 2

I would swipe through the whole thing. The arc is genuinely strong: two concrete illustrations of the problem (slides 3, 4), a clean four-dimension framework, one dimension per slide with a governance consequence stated plainly, worked examples on real systems, an honest slide on what the framework doesn't settle, and a closing question I could actually answer about my own AI estate. That is rare discipline for this kind of source material. The single biggest thing holding it back is that three of the four dimension-deep-dive slides (7, 9, 10) pack a six-point scale into one dense paragraph, which is exactly the place a busy reader stalls and has to reread, right in the middle of the deck's strongest material.

SLIDE 7 · major · "A.0 is no autonomy... A.5 is full autonomy: all tasks in all circumstances, with no oversight or control."
  Six scale points delivered as one run-on paragraph. I lost my place tracking which letter went with which description and had to go back to A.2 to check it against the Waymo/ChatGPT sentence that follows. Slide 8 solves the identical problem with a table and reads at pace; slides 7, 9, 10 don't get that treatment and pay for it.

SLIDE 9 · major · "GC.0 is the absence of a goal... GC.5 is unbounded: the agent generates its own goal structures and interprets underspecified objectives."
  Same density problem as slide 7. Six definitions in a row, no visual break, so the eye has nowhere to land before the paragraph moves on to what it means for governance.

SLIDE 10 · major · "G.0 is no application in any domain... G.5 is a fully general system spanning the entire suite of human cognitive tasks."
  Same again. Three slides in a row using this pattern reads as a template applied without checking whether it actually reads well, especially next to slide 8's table right before it.

SLIDE 5 · major · whole slide
  This is a resolution-stage slide and it has no business consequence sentence at all. It defines the four terms and explains why generality was added to a list of seven academic definitions, then stops. I finished it not knowing what any of this means for a governance decision until slide 6 answers that. The writing standard is explicit that every resolution slide carries this, and this is the one place in the deck it doesn't.

SLIDE 12 · major · table, "Goal complexity" row appearing twice
  The left-hand column of the table has "Goal complexity" listed twice in a row (once for the interpretability audit, once for the reward-hacking monitor). On a fast read this looks like a copy-paste error, not a deliberate design choice, and I had to stop and reread the two rows to confirm it wasn't a mistake before I trusted the table.

SLIDE 2, 4, 5, 11, 13 · major (one finding, cumulative) · "Google DeepMind and Carnegie Mellon"
  This phrase, or a variant of it, is the subject of the sentence in at least six slides ("Google DeepMind and Carnegie Mellon reject that rule outright," "Google DeepMind and Carnegie Mellon start by comparing," "Google DeepMind and Carnegie Mellon classify four well-known systems," "Google DeepMind and Carnegie Mellon set that out as open work"). Naming the organisation instead of "the authors" is the right call per the house style, but repeating a commercial AI lab's name this many times as the actor behind a governance framework starts to read like Google is positioning its own proposal, which undercuts the deck's otherwise careful, independent tone. I would not have flagged this once; I flag it because it recurs.

SLIDE 2 · minor · "Writing in Nature in August 2026, Google DeepMind and Carnegie Mellon treat both as useful ground and as underspecified for agents."
  Mildly awkward construction, two abstract nouns doing the work ("useful ground," "underspecified"). Not a stall, just not the deck's best sentence.

SLIDE 6 · minor · "That four-part description is its agentic profile."
  Fine on its own, but landing straight after the dense slide 5 means the reader meets the load-bearing term "agentic profile" for the first time right when attention is already stretched from the previous slide. Not a blocker, just poor sequencing given the slide 5 issue above.

Files reviewed: `carousels/nature-2026-agentic-profiles/draft-carousel.md`, `skills/carousel-production/writing-standards.md`.

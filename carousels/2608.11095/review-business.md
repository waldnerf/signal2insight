# Business review — revision 1

PRIMARY TEST
so-what (one sentence, from memory): "Teams running coding agents should require a one-line rationale comment on every rule added to CLAUDE.md-style instruction files, because that's what lets a bloated, unreliable file be safely pruned instead of left to grow until it degrades the agent."
had to reopen the deck to answer: no

SCORES
B1 so-what: 4
B2 arc: 4
B3 accessibility: 2
B4 hook-close: 3
B5 credibility: 4
subtotal: 17/25

DEFECTS
blockers: 1
wrong: 0
majors: 4
overstated: 0
unverifiable: 0
minors: 3

I would swipe through, but not without friction, and the friction is concentrated exactly where it costs most: the opening slide and the two densest data slides. The single biggest thing holding this deck back is that the trim kept every number and cut the connective explanation around them, so several slides now read as a stats printout rather than an argument. The arc is genuinely good (titles alone argue a real case, and the close is a strong, specific question), which makes the mid-deck density more frustrating, because the thesis is sound and mostly earns its claims, it just doesn't slow down enough on the numbers-heaviest slides to let a non-technical reader keep pace.

SLIDE 1 · blocker · "One habit reverses this: record why an instruction was added, when it is added."
  I had to reread this sentence to parse it; "added... when it is added" reads as a stutter rather than a clear instruction. This is the slide that decides whether I keep swiping, and it stalls on its second sentence.

SLIDE 1 · blocker · "A single 51-step run cut excess instructions 99.3%, and the same fix lifted instruction-following 23.1% on prompts seeded with 16 distractors."
  Three undefined terms land here at once: "51-step run," "excess instructions," and "16 distractors." None of them is explained anywhere before this point, and "excess instructions" specifically only gets a definition six slides later, on slide 7 (the minimum-instruction-set framing). A reader meeting this slide cold has no way to judge whether 99.3% is impressive or made up. The opening slide is the one place in the deck that cannot afford a forward reference like this.

SLIDE 3 · major · body
  "1,867 GitHub repositories carrying CLAUDE.md, AGENTS.md or copilot-instructions.md: 299,440 version-to-version transitions and 247,694 tracked instruction lifetimes. Among multi-version repositories, 64.3% gain instructions against 26.6% that lose them. Each commit adds 4.9 net instructions on average. The median file holds 39 instructions, the top tenth 131 or more..." Seven distinct figures in roughly 70 words, with no sentence doing anything but adding another number. At the pace I'd actually give this slide, I skim past it without retaining any of it, which defeats the point of including it. The title already carries the claim; the body should be doing something other than restating the underlying table in prose.

SLIDE 4 · major · "Fragility explains under a third of that decline."
  "Fragility" is introduced as one of three competing explanations in the first sentence and never defined at all, unlike "staleness," which the next sentence at least characterizes ("staleness predicts deletion risk rising with age"). I cannot evaluate a claim about a named hypothesis I was never told the content of. This is the complication slide that is supposed to establish the cause the rest of the deck builds on, so an undefined term here weakens everything downstream.

SLIDE 7 · major · "Over 15 steps and 552 histories, maintainers without comments finished 60.4% above the minimum; with comments, 5.8% below it, at equal satisfaction."
  "5.8% below it" (below the minimum) sits next to "at equal satisfaction" and I cannot reconcile the two: if the minimum is the correct, complete instruction set, finishing below it should mean something is missing, not that satisfaction held steady. I flag this as a comprehension problem for a business reader; I suspect it may also be a technical slip, but that call belongs to the technical review.

SLIDE 1 vs SLIDE 9 · major · credibility
  Slide 1 leads with two large, unhedged percentages (99.3%, 23.1%) as the deck's hook, drawn from what slide 9 later describes as "one seed's worth of evidence, a direction rather than a settled magnitude." The deck's most dramatic numbers get the least caveat and the most prominent placement, while a comparable single-run result later in the deck gets an explicit, honest hedge. That inconsistency reads as leading with the best number rather than the most representative one, which is the one place in an otherwise careful deck where the tone tips toward promotion.

SLIDE 2 · minor · body
  Six figures in about 65 words ("46 killed and 14 added," "77.3%," "91.5%," "4.9%... versus 4.1%"). Readable in one pass, but dense enough to slow the pace the title sets up.

SLIDE 9 · minor · "the raw ratio rather than excess above minimum"
  This clause reads as a stray footnote correcting the metric used on slide 7, dropped into a business-facing sentence without enough context to tell why the distinction matters here. Likely a trim artifact that removed the sentence that used to frame it.

SLIDE 10 · minor · "safety relevant instructions"
  Missing hyphen ("safety-relevant") causes a brief double-take; not load-bearing, just a small tax on read speed.

Files reviewed: `carousels/2608.11095/draft-carousel.md`, `skills/carousel-production/writing-standards.md`.

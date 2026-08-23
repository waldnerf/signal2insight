---
arxiv_id: "2607.29433"
reviewer: carousel-reviewer-business
draft_revision: 6
pass: 5
note: "Blind re-review of revision 6, the first pass under the blended dual-track format (labelled For the business / Under the hood notes removed) and the 100/120-word body cap."
---

PRIMARY TEST
so-what (one sentence, from memory): "A business running a memory-enabled AI assistant needs to test and buy on whether the system acts on a recalled customer preference, not just whether it recalls it, because even the best systems only act on about two-thirds of what they correctly remember, worst of all in high-stakes categories like health, so a utilisation figure belongs in every acceptance test and pilot on the company's own data."
had to reopen the deck to answer: no

SCORES
B1 so-what: 5
B2 arc: 4
B3 accessibility: 4
B4 hook-close: 5
B5 credibility: 5
subtotal: 23/25

DEFECTS
blockers: 0
wrong: 0
majors: 2
overstated: 0
unverifiable: 0
minors: 5

I would swipe through this whole deck. It opens on a concrete, high-stakes scenario, defines its two terms (recall vs. utilisation) before leaning on them, gives a buyer a metric and a four-item action list, and closes with a question I could actually answer from my own AI deployments. The single biggest thing holding it back is that two of the resolution/impact slides (6 and 7) let a run of pure test-mechanics sentences sit unconnected to any stated business stake, so the "so what" has to be inferred from the last sentence rather than earned across the passage the way slides 4, 8, 10 and 11 manage it.

SLIDE 7 · major · "Preferences mentioned in passing are the hardest for a system to store"
  The body explains the mechanism (explicit/incidental/inferential, why incidental scores lowest) and lands on "What customers mention in passing is what a system is likeliest never to hold." That sentence restates the finding, it doesn't say what changes for a business. This is a Resolution-stage slide, and the standard requires an explicit business consequence here. Compare to slide 10, three slides later, which does the same kind of finding and still lands on "every high-consequence category in your own domain needs a utilisation figure of its own." Slide 7 has no equivalent close.

SLIDE 6 · major · seam
  "Behaviour is scored by comparison: the same model answers the same request twice... a GPT-5 judge, checked against human annotators, decides only whether the memory-backed answer reflects the preference in a way the other misses. Every retrieval system shares GPT-4o-mini as backbone, so architecture is what varies." Two sentences of pure test-methodology detail, with nothing commercial in either, then "A buyer can put this number in an acceptance test." The consequence sentence doesn't follow from the sentence before it (backbone architecture) at all, it just arrives. I can point to that exact sentence as the switch. Each half is fine alone; together they read as a mechanism block with a consequence bolted on, not one blended passage.

SLIDE 1 · minor · "That scenario opens KnowAct, drawn as illustration rather than logged from a deployment."
  This is an honest and correct disclosure, but it lands in the middle of the hook, right where the deck most needs momentum, and I had to reread it to work out it was a sourcing caveat rather than part of the story. Worth relocating, not cutting.

SLIDE 9 · minor · "About three in ten were retrieval misses, and about one in six failed again with the preference handed over as a plain sentence, a proportion that holds steady however the preference was originally expressed."
  Three stats and a qualifying clause in one sentence, on top of "more than half" the sentence before. At the pace I'd actually give this slide, I had to stop and re-parse which number belonged to which condition.

SLIDE 5 · minor · title
  "Pairing a recall question with a behavioural scenario on the same preference makes the gap visible" describes the test method, not a business consequence. It reads fine as one line in the middle of an arc that's otherwise consequence-first (compare slide 6's "separates a memory problem from a behaviour problem" or slide 11's "belongs in every acceptance test"), but on its own it's a methods-section sentence.

SLIDE 9 · minor · title
  "Most failures happen with the right conversation already in front of the model" is a mechanism/location claim (where in the pipeline failures occur), not a stated consequence. It sets up the slide's real point, "better search addresses the smaller share," well, but that point belongs in the title per the standard, and isn't there.

SLIDE 8 · minor · "KnowAct ran this decomposition on one system, Mem0."
  Necessary scope disclosure, but it's dropped between the mechanism sentence and the closing consequence sentence ("A complaint about personalisation becomes a diagnosis with an owner."), interrupting the passage's flow right before it lands. Would read more smoothly earlier in the paragraph, alongside the rest of the method description.

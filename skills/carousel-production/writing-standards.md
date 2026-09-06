# Carousel writing standards

The copy standard for every LinkedIn carousel produced from this pipeline. `carousel-writer` writes against it, both reviewers judge against it, and `scripts/check_standards.py` enforces the mechanical half of it.

This file is canonical and self-contained. Nothing here reads from or defers to another repository.

## Objective and audience

Thought leadership on LinkedIn. The goal is to bring findings from current research to **business and technology leaders in accessible terms**.

Both audiences matter, and the deck fails if it serves only one. A commercial leader must be able to read the deck end to end and understand what changed and why it matters. A technical leader must find enough method detail to judge whether the approach is sound. Serving both is a layering problem, not a compromise: the narrative stays accessible throughout, and technical precision lives in designated places (see Technical depth below).

## Titles carry the argument

Titles are read as a standalone storyline. Someone who reads only the twelve titles, in order, and nothing else, should come away with the full argument.

- Every title is a **full sentence that asserts a claim**. Never a label. "Architecture", "Results", "The approach" and "Key findings" are all failures.
- Lead with the answer. The title states the conclusion; the body supplies the mechanism and the evidence.
- Titles follow a **Situation, Complication, Resolution, Impact** arc across the deck.
- The business consequence belongs in the title. The mechanism belongs in the body. Writing these the other way round produces a deck that reads as a methods section.

**The standalone test.** Extract the titles, read them in sequence with nothing else. If they do not argue a case on their own, the arc is wrong, and no amount of body copy will rescue it. `check_standards.py` prints this spine on every run so the test is unavoidable.

## Voice and tone

Confident, calm, analytical, practical.

Present a clear point of view. Explain reasoning. Connect every idea to application. Avoid urgency, avoid hype, avoid the register of an announcement.

The default register is impersonal and analytical. Direct second-person address is reserved for the opening hook and the closing call to action, where it earns its place.

## Mechanics

- **No em dashes. No en dashes.** Use a comma, a full stop, a colon, parentheses, or a middot.
- **Sentence case** in titles and labels. Capitalise the first word, proper nouns, and acronym expansions. Never title case.
- **Full sentences.** No fragment bullets. A bullet is still a sentence.
- Short sentences. Active voice. Precise terminology.

## Assert, do not negate

Describe what something **is**, rather than what it is not. A claim whose load-bearing word is "not", "no", "never", "without" or "cannot" reads as defensive and inverts the reader's effort.

| Avoid | Prefer |
|---|---|
| "Trust was the binding constraint, not accuracy." | "Trust set the ceiling on adoption." |
| "This is not a forecasting problem." | "This is a scheduling problem." |
| "The model cannot enter the solver directly." | "The solver needs straight lines, so the curve is approximated first." |

Negation inside an ordinary sentence is fine. The rule governs the claim a slide is built on, and titles most of all.

## Banned language

Filler, exaggerated claims, unnecessary adjectives, and marketing language without substance.

Specifically banned: transform, unlock, game changer, cutting edge, revolutionary, powerful, seamless, leverage AI, harness, supercharge, "in today's rapidly changing world", "opens up possibilities", "valuable insights", "promising direction", "could fundamentally change how".

**The deletion test.** If a sentence would remain equally true after deleting it, delete it.

## Attribution and quotes

- Never write "the authors", "the researchers", "the paper argues" or "the study finds". Name the organisation.
- Quoted text must be **verbatim**. `check_standards.py` matches every quoted string against the source and fails on a mismatch.
- Attribute quotes to the named organisation, not to individuals, unless the deck is specifically about a person.

## Numbers and technical naming

This rule is conditional on the deck's active **depth pattern**, which is recorded in the draft's frontmatter.

**In narrative copy, always:** no library names, no product names, no vendor names, no numeric acceptance thresholds. Name the method type and the general stack. "One machine learning model covers every product group" rather than the library that implements it.

**In a designated technical block:** what is permitted depends on the pattern.

| Pattern | Where technical depth lives | Library names | Numeric thresholds |
|---|---|---|---|
| `dual-track` | Blended into the same paragraph as the business consequence, no separate note or header | Yes, named plainly | No |
| `spec-cards` | One Inputs / Model / Calibration / Outputs card per system | Yes | Yes, in the Calibration line |

**Under `dual-track`, mechanism and consequence share one passage.** Earlier drafts of this pattern split every resolution slide into a labelled *For the business* note and a labelled *Under the hood* note. That visible seam is gone. Write one passage per slide where the mechanism explains itself and the business consequence follows from it in the same breath, with no header marking a switch between them. A reader should not be able to point to the sentence where the slide changes audience.

**End on the takeaway, not the mechanism.** Whatever order the passage introduces things in, the last sentence is the point: what this means, stated once and plainly, not set off by a label. A body that trails off in mechanism detail without landing on that sentence has failed even if every fact in it is correct. The title already carries the claim; the body's job is to earn it and then land it again, in the reader's own terms, at the close.

**Keep each slide body short.** A single blended passage does not need the room two labelled notes used to take. Target 100 words in the body, with 120 as a hard ceiling. If the mechanism needs more space than that to explain itself, the slide is carrying two ideas, and the fix is to split it into two slides, not to let the paragraph grow.

**"Numeric threshold" means an acceptance cutoff or a pass/fail bar**, the kind of number a team would hold a system to: a minimum accuracy, a maximum error, an optimality gap. Those are what `dual-track` keeps out of the blended passage.

It does **not** mean every number. Counts, sample sizes and structural figures belong in a technical note and make it concrete: how many systems were tested, how many preferences, how many annotators, how many cases in a breakdown. A practitioner judging whether a method is sound needs them, and stripping them leaves an assertion where the paper gave a measurement. They remain bound by the sourcing and scope rules like any other figure.

Neither pattern is settled as the house standard. The writer is told which to use and records it in frontmatter, so the choice accumulates as evidence rather than being decided once by guess.

**Promotional outcome figures stay out** under both patterns. Revenue lift, margin improvement, adoption and acceptance rates, ROI percentages: these are commercially sensitive, frequently unverifiable, and read as vendor marketing. Write "commercial teams accept and execute the large majority of recommendations" rather than a percentage. Scale and scope figures (portfolio size, market count, planning horizon) are descriptive rather than promotional, and are fine.

**A source's own headline finding is not a promotional figure, and it stays in.** The test is what the figure is doing, not whether it is a number. A figure that flatters the subject and cannot be checked comes out. A figure that *is* the finding, especially a critical or negative one the paper exists to report, is the deck's evidence, and stripping it into "a large share" leaves the reader with an assertion where the paper gave them a result. Keep it, carry its population with it, and hold it to the sourcing rule above like any other figure.

The distinction in one line: **a number that sells the subject comes out, a number that is the finding stays.** When a figure could be read either way, ask whether the paper would be diminished or flattered by it. Diminished means it is evidence.

## Every figure carries a source

A figure is any number, proportion, ranking, count or magnitude claim, whatever form it takes in the copy. "About two-thirds", "the second largest line", "most people" and "16 systems" are all figures.

Every one of them resolves to exactly one of three outcomes:

1. **Traceable to the paper.** Cite it the way the rest of the deck does, and carry its population with it.
2. **Traceable to a named external source**, found by search and verified. The slide names the publisher and the year, so a reader can check it. An industry benchmark, an official statistic, a named study.
3. **Removed.**

There is no fourth outcome. A figure that cannot reach 1 or 2 comes out of the deck.

**Do not launder an unsourced figure into vague prose.** Rewriting "roughly 40% of teams" as "many teams" keeps the claim and discards the accountability, which is worse than the number was. If the evidence is missing, the claim goes, not its precision.

**Search is a real option, not a formality.** Where a figure is genuinely load-bearing for the business framing and the paper does not supply it, look for one that is citable rather than dropping the point. Scene-setting figures about market size, industry cost structure or adoption rates usually do exist in citable form. What matters is that the reader can follow the citation to something real.

**External sources never support a claim about the paper.** They set the scene around it. Anything describing what the research found, measured or demonstrated traces to the paper and nothing else.

## Scope travels with the number

Every result carries the population it was measured on, and that scope moves with it to every slide that repeats it. A paper usually runs several analyses over different populations: the whole benchmark, one system, one condition, one subgroup. Those are different claims even when they share vocabulary and even when the figure is identical.

Three rules, and the reviewers treat a breach of any of them as `wrong` rather than as an overstatement:

- **State the population where the number appears**, not only where it was introduced. A caveat on slide 8 does not protect slide 9. A reader who sees one slide must not come away with a broader belief than the evidence supports.
- **Never widen a scope to make a claim land harder.** Over-scoping while sounding careful is the worst version of this, because the copy reads as rigorous while being false.
- **Name only categories the source reports.** If the deck attaches a result to a class of thing, that class must exist in the paper with a result of its own. A phrase borrowed from a passing contrast is not a category, and an aggregation the paper never performs is not a category.

Where two analyses share vocabulary with different meanings, keep them visibly apart, and attach each quotation to the analysis it actually came from. A correctly sourced quote placed beside a different finding implies corroboration that does not exist.

## Structure

- Twelve slides is the working default. Fourteen is the ceiling.
- Prefer frameworks, taxonomies, comparison tables and process flows over prose.
- Apply MECE thinking where it is natural. Clarity is the goal, not artificial symmetry.
- Every resolution slide carries an explicit business consequence, whatever the depth pattern.
- The closing slide asks a specific, open question that requires the reader to contribute real experience. "What do you think?" fails. "Where in your planning stack does a human still reconcile the model output by hand?" works.

## LinkedIn post caption

The short text post that sits above the carousel attachment, written by the post-writer step after the deck is approved (see [[SKILL]], "Post caption"). Everything above in this document applies to it (mechanics, banned language, attribution, assert-do-not-negate, the sourcing rule for every figure), plus:

- **One hook, one argument, one call to action.** LinkedIn truncates a post after roughly two to three lines before "see more," so the opening line has to work standalone, the same discipline the deck's titles are held to.
- **Argue the same case as the deck's brief**, its `key takeaway` and `framework choice`, not a second, independently invented framing. The caption and the deck should read as one argument continued across two surfaces.
- **Do not re-tell the deck slide by slide.** State the tension the deck resolves, in different words than the titles use, and stop. A caption that walks the reader through slide 1, then slide 2, then slide 3 gives away the deck before they swipe.
- **Close on the same open question the deck's closing slide asks**, or a tighter version of it, not a generic "thoughts?"
- **Length**: short enough to read before "see more" cuts it, roughly 40 to 80 words for the visible portion, with the rest of the post continuing past the fold if there's a genuine reason to.

## Final check

Before a draft goes to review:

1. Read the titles alone. Do they argue the case?
2. Does every resolution slide say what changes for the business?
3. Could a commercial leader read this without stalling on a sentence?
4. Could a technical leader tell whether the method is sound?
5. Is every quoted string verbatim, and every claim traceable to the source?

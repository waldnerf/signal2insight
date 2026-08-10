---
name: carousel-production
description: Produce a LinkedIn carousel draft from a paper this pipeline has already summarised, using a writer subagent, two review subagents, and a design-direction subagent. Use when the user asks for a carousel, slide copy, a LinkedIn deck, or a storyline from a paper, and when they ask to review or revise an existing carousel draft. Trigger on phrases like "make a carousel from this paper", "draft the slides", "write the LinkedIn deck", "review the carousel draft", "add design direction".
---

# Carousel production

## Purpose

Turn a paper that has already cleared [[editorial-review]] into a LinkedIn carousel draft, aimed at bringing current research to business and technology leaders in accessible terms.

This is the step that used to sit outside the system. It now lives here, because the constraints it runs on are the same constraints the rest of the pipeline enforces: canonical knowledge in the file the code reads, judgment separated from mechanical write-out, and a human gate before anything is published.

The output of this skill is **markdown only**. Rendering a deck to HTML, PDF or images is a separate action outside this skill, and it happens only on an explicit instruction.

## Scope

Applies to a paper with a downloaded PDF and cleaned body text at `papers/text/<arxiv_id>.md`. That file is the primary input: the deck is written from the paper, not from a summary of it.

If it is missing, build it first:

```bash
python skills/knowledge-extraction/scripts/build_fulltext.py <arxiv_id>
```

`ArxivWiki/summaries/<arxiv_id>.md` and `papers/metadata/extractions/<arxiv_id>.yaml` are secondary: useful for the business framing triage already reasoned through, but never a source for a quotation, because they paraphrase.

## Files

```
carousels/<arxiv_id>/
├── draft-carousel.md        the deliverable. Writer creates it, designer annotates it.
├── review-business.md       carousel-reviewer-business findings
└── review-technical.md      carousel-reviewer-technical findings
```

`draft-carousel.md` carries frontmatter recording `source`, `depth_pattern`, `slides` and `status`. The depth pattern is recorded because it is not yet settled (see below), and the record is what will eventually settle it.

## The two depth patterns

The deck serves business and technical leaders at once. Two patterns do that, and neither has been adopted as the house standard.

**`dual-track`.** Every resolution slide carries one blended passage: mechanism and business consequence share the same paragraph, with no labelled note marking a switch between them. The method is named plainly and numbers stay out of it. Depth is spread evenly across the deck rather than concentrated, and each slide body stays short, built to be read in a few seconds. Runs shorter, around 11 or 12 slides.

**`spec-cards`.** Narrative slides stay fully accessible, and each system gets one dedicated card with Inputs, Model, Calibration and Outputs carrying the real numbers and library names. Depth is concentrated; a technical reader gets two dense slides. Needs the length to afford them, around 14 slides.

**The choice is made in the main thread, by asking the user, before the writer is spawned.** A subagent starts cold and cannot ask a question mid-task. Record the answer in the draft's frontmatter. After several decks, whichever pattern keeps getting chosen becomes the standard, and that belongs in a short decision note rather than being guessed at now.

## The agents

Four subagent definitions live in `.claude/agents/`. They are workers; this file and [writing-standards.md](writing-standards.md) are the knowledge.

| Agent | Model | Writes? | Role |
|---|---|---|---|
| `carousel-writer` | Opus | Yes | Drafts and revises the slide copy |
| `carousel-reviewer-business` | Sonnet | No | Reads as a commercial leader |
| `carousel-reviewer-technical` | Sonnet | No | Traces every claim to the source |
| `carousel-designer` | Opus | Edits | Appends render notes and design direction |

Reviewers are deliberately **read-only**. A reviewer with write access rewrites the draft instead of reviewing it, and the separation the roster exists for is lost.

Reach and engagement are not reviewed here. That is a separate judgment about a specific post, and it belongs to whatever post-evaluation step the user runs at publication time.

## Process

1. **Confirm the source and the depth pattern.** Read `ArxivWiki/summaries/<id>.md` yourself before spawning anything, so you can tell the writer what the deck is about rather than making it guess. Ask the user which depth pattern to use. Ask nothing else at this stage.

2. **Spawn `carousel-writer`.** Pass the arxiv id, the depth pattern, the slide budget, and the paths to the source files. It writes `carousels/<id>/draft-carousel.md`.

3. **Run the linter.**
   ```bash
   python skills/carousel-production/scripts/check_standards.py <arxiv_id>
   ```
   Fix mechanical violations before spending a reviewer on them. The linter also prints the title spine, which is the standalone test from [writing-standards.md](writing-standards.md).

4. **Spawn both reviewers in parallel, in one message.** They are independent, and the friction between them is the point: the business reviewer pulls toward accessibility, the technical reviewer pulls toward precision. Neither wins automatically.

   The first review of a deck gets `carousel-reviewer-technical` a full read of `papers/text/<id>.md`. From the second review pass onward, tell it which slides changed since the last snapshot and which drew findings last time (from `--churn`, below); it greps the paper for those slides' claims instead of rereading the file in full, per its own agent definition.

   Reviewers are read-only, so they return findings rather than writing them. **You persist each report verbatim** to `carousels/<id>/review-business.md` and `review-technical.md`, because the writer reads those files on the revision run and a report that only exists in your context is lost the moment it is compacted.

5. **Persist both reports and apply the review gate.** Write each reviewer's report verbatim to `carousels/<id>/review-business.md` and `review-technical.md` (they have no write tools, so this is yours), and append a row to `review-log.md`. Then run the gate. See The loop below. It decides mechanically whether the draft goes back for another pass or forward to the user.

5b. **Snapshot before revising.**

   ```bash
   python skills/carousel-production/scripts/check_standards.py --snapshot <arxiv_id>
   ```

   Copies the draft to `history/rev-NN.md`. Do this on every pass without exception, because the next pass cannot be churn-checked without it.

6. **If the gate says revise:** spawn `carousel-writer` again straight away, **without consulting the user**. It reads its own previous draft and both review files, and increments `revision` in the frontmatter. The review files it reads are what scope its source reading too: from the second writer pass onward it greps `papers/text/<id>.md` for the claims on slides that drew findings, rather than rereading the file in full, per its own agent definition. **Return to step 3.** The linter and both reviewers run again on every pass; a fix on one slide routinely breaks the slide next to it. This is the loop, and interrupting it for approval on every pass defeats the point: the user's judgment is worth spending on a deck that has already cleared the bar, not on one the reviewers have already said is not ready.

7. **If the gate says ship, or the pass cap is reached:** bring the draft to the user, with both subtotals, the two primary-test answers, and any findings still open. Walk those findings one at a time; where the reviewers conflicted and both were right, that is the user's call, not yours. This approval gate is real: the designer edits the same file, so a copy revision after design direction has been added overwrites that direction.

8. **Spawn `carousel-designer`.** It appends a render note per slide. It changes no copy.

9. **Stop.** Rendering is not part of this skill and needs its own explicit instruction.

## The review gate

A draft that reviews badly gets another pass. That decision is mechanical, so it does not depend on how the reports happened to read or on what survived a context compaction.

**Both reviewers must open their report with this block.** A report without it is incomplete: send it back.

```
VERDICT
blockers: <n>      (business) reader stops or misunderstands
wrong: <n>         (technical) contradicts the source
majors: <n>        the point lands weakly
overstated: <n>    stronger than the source supports
unverifiable: <n>  no source found
minors: <n>
```

**The rule, applied to the two reports combined:**

| Condition | Outcome |
|---|---|
| `blockers > 0` or `wrong > 0` | **rework**, another pass is mandatory |
| `majors + overstated >= 3` | **revise**, another pass |
| otherwise | **ship**, go to the user |

You do not have discretion to skip a mandatory pass because the findings look minor to you. If you believe the gate is wrong, say so to the user and let them decide.

`unverifiable` findings never force a pass on their own, because they usually mean the source record is thin rather than the copy being wrong. They go to the user as questions.

**Loop cap: three writer passes.** If the gate still says rework after the third, stop and bring the whole thing to the user with both reports and your reading of why it will not converge. A loop that cannot converge is a signal about the source material or the brief, and spinning a fourth pass buries that signal instead of surfacing it.

**State lives in the frontmatter, not in your context.** Every pass updates `revision: <n>` and `status: draft | in-review | approved`. Context compaction will lose your memory of which pass you are on. The file will not.


## The loop

Both reviewers score five dimensions, 1 to 5, and each names one **primary** dimension: `B1 so-what` and `T1 mechanism`. Those two carry the deck's reason for existing, so they are gated harder than the rest.

Run another writer pass when **any** of these holds:

| # | Trigger | Why |
|---|---|---|
| 1 | Any `wrong` or any `blocker` | An inaccurate or unreadable deck never reaches the user for approval |
| 2 | `B1` or `T1` below **4** | The deck fails at the thing it exists to do |
| 3 | Any other dimension at **2 or below** | A floor, so a strong average cannot hide one bad dimension |
| 4 | Either subtotal below **19/25** | The general bar |

Rules 2 and 3 are why scores did not replace the defect counts. A composite alone would let a deck score 21 with a 2 in fidelity and pass.

**Cap: three writer passes.** At the cap the draft goes to the user with its scores and open findings regardless of the gate.

**Churn control.** Reviews are whole-deck, because arc and mechanism only exist across slides. Writing is not: a pass should touch the slides that drew findings and leave the rest alone, since every unrequested edit is a chance to break something already working. After each pass:

```bash
python skills/carousel-production/scripts/check_standards.py --churn <arxiv_id>
```

It compares the draft against the last snapshot and reports two things. **CHURN** is a slide that changed with no finding against it: confirm the edit was needed or revert it. **UNADDRESSED** is a slide that drew a finding and did not change: either the writer rejected the finding on the record, which is legitimate and must be stated, or it was missed.

Neither is automatically a failure, so this does not gate. It exists so an unrequested rewrite is visible instead of silent. Tell the writer in its brief which slides are scoring well and are not to be disturbed, and use this to check that it complied rather than taking its word.

This report is also what scopes the technical reviewer's next read (step 4): full rereads of `papers/text/<id>.md` happen once, on the first review, and after that it greps for the claims on the slides this report names, instead of rereading the file in full. The writer's own next-pass reading is scoped the same way but from the review findings directly, since churn on its last pass isn't available until after it writes (step 6).

**Resetting the budget.** Only the user grants a fresh three passes. Record it by setting `pass_reset_at: <current revision>` in the draft's frontmatter; the gate then counts `revision - pass_reset_at`. `revision` itself never rewinds, because it is the deck's history. A reset is a decision with a reason behind it, so the reason belongs in `review-log.md` next to the scores that prompted it. Never reset to escape a gate that keeps failing on the same finding: that is the signal the source or the depth pattern is wrong, which is what the cap exists to surface. A deck that cannot clear the bar in three passes has a problem in the source material or the chosen depth pattern, and further passes will not find it. Say which gate is still failing and what you think the underlying cause is.

Check the gate mechanically rather than by eye:

```bash
python skills/carousel-production/scripts/check_standards.py --gate <arxiv_id>
```

The thresholds above are a starting point, not a calibrated standard. They were set before any deck had been scored. After two or three runs, compare what a deck you consider good actually scores and adjust them, in this file, rather than letting the numbers drift by reinterpretation.

## Rules that bind every run

- **Never write outside this repository.** Everything this skill writes lives under `signal2insight/`.
- **Reading outside is limited to sourcing figures.** `carousel-writer` and `carousel-reviewer-technical` hold `WebSearch` and `WebFetch` for one purpose: to source a figure the paper does not supply, or to verify one the deck already cites. Every externally sourced figure names its publisher and year on the slide. A figure that reaches neither the paper nor a citable external source is removed, and it is never rewritten as vague prose to keep the claim without the accountability. Anything describing what the research found, measured or demonstrated traces to the paper alone.
- **The markdown is canonical.** Any rendered deck is a generated expression of it. If a copy decision exists only in a rendered artifact or in a conversation, it is not persisted.
- **The writer owns copy, the designer owns direction.** A designer that trims a sentence to make a slide fit has made a writing decision. It reports the problem instead.
- **Quotes are verbatim or they are not quotes.** The linter checks this against the source and it is not advisory.

## Known constraint

The Read tool cannot open PDFs in this environment and no PDF library is installed, which is why `build_fulltext.py` exists: it derives `papers/text/<id>.md` once, using a dependency-free extractor, and every skill reads that instead of the PDF.

Two limits carry through to review. **Appendices and references are removed**, so a claim resting on appendix material is unverifiable here even though it may be correct in the paper. And **page order in the extracted text does not always follow reading order**, so the body may not read start to finish. Neither affects quotation checking, which searches the whole file.

---
name: knowledge-extraction
description: Turn a triaged arXiv paper's PDF into a structured knowledge record, and — only if it's worth keeping — an ArxivWiki page. Use this skill when the user asks to extract, summarize, or write up a paper that has already been screened, or asks to process the extraction queue. Only runs on papers whose recommendation is extract_eligible (Review fully or Priority review). Trigger on phrases like "extract this paper", "write up the Priority review papers", "process the extraction queue", "summarize 2507.12345".
---

# Knowledge Extraction

## Purpose

Extract durable knowledge from a full paper, and decide whether it should become part of the knowledge base and eventually a public article. Editorial-triage judged the abstract; this skill judges the paper. A paper it thought promising can still come back `keep: false` here — full-text reading is a second, deeper gate, not a formality.

## Input

- `../../papers/pdf/<year-week>/<arxiv_id>.pdf` — PDFs are grouped by the ISO year-week they were downloaded in; if the exact week isn't already known, glob (`papers/pdf/*/<arxiv_id>.pdf`) rather than guess it
- `../../papers/metadata/<arxiv_id>.json` (title, authors, dates, categories, editorial-triage's `overall_score`/`recommendation`/`headline`)
- `../../papers/metadata/scores/<arxiv_id>.yaml` (from [[editorial-triage]])

## Candidate selection

1. Eligible: `status == "triaged"`, `downloaded == true`, and `extract_eligible == true` (set by [[editorial-triage]] from the paper's recommendation — currently true only for `Review fully` and `Priority review`, per `screening.recommendations` in `../../config/editorial-profile.yaml`).
2. **PDF must actually exist first.** A paper can be `extract_eligible` at triage and still not have a PDF yet if it wasn't ranked in that week's `download_top_n` cap — see [[research-discovery]]'s `download_top.py`. If a promising paper has no PDF, that's not a bug to work around; it means download_top hasn't gotten to it yet (or ever will, if consistently outranked). Don't extract from the abstract alone as a substitute.
3. Weekly budget: count papers already `extracted` whose `extracted_at` falls in the current calendar week (Monday–Sunday). Remaining budget = `weekly_limit` minus that count. A paper that gets read but comes back `keep: false` (`status: "evaluated"`) still counts against the budget — the read happened either way.
4. If eligible papers exceed the remaining budget, take the highest-ranked recommendation first (`Priority review` before `Review fully`, per `screening.recommendation_order`), `overall_score` as tiebreaker.
5. If the user names a specific paper directly and it has a PDF downloaded, extract it regardless of budget — the weekly limit throttles the *unattended* queue, not an explicit request. If it has no PDF yet, that's a [[research-discovery]] step first, not something this skill can work around.

## Reading the PDF

Use the Read tool on `../../papers/pdf/<year-week>/<arxiv_id>.pdf` (glob for the file if the week folder isn't already known — the metadata record's `downloaded_at` timestamp also tells you which week). For papers over ~20 pages, read in ranges via the `pages` parameter (e.g. `1-20`, then `21-40`) and synthesize across chunks — do not skip the back half of the paper, limitations and future work sections are frequently there.

## The worksheet

Eight sections, forty-seven questions, plus a Final Assessment. Answer all of them for every candidate. The fixed checklists and enums live in `../../config/editorial-profile.yaml`'s `extraction` block — read them from there rather than hardcoding.

### Section A — Executive Summary

| # | Question | Field |
|---|---|---|
| A1 | Summarize the paper in five sentences | `summary_five_sentences` |
| A2 | Explain it for an executive audience | `executive_explanation` |
| A3 | Explain it for an AI architect | `architect_explanation` |
| A4 | What is the central contribution? | `central_contribution` |

### Section B — Problem Analysis

| # | Question | Field |
|---|---|---|
| B5 | What industry problem motivated this work? | `industry_problem` |
| B6 | Why is the problem important? | `problem_importance` |
| B7 | What assumptions are challenged? | `assumptions_challenged` |
| B8 | What gaps in current approaches are identified? | `gaps_identified` |

### Section C — Technical Innovation

| # | Question | Field |
|---|---|---|
| C9 | Describe the proposed architecture | `proposed_architecture` |
| C10 | What makes it different? | `differentiation` |
| C11 | What are the novel concepts? | `novel_concepts` |
| C12 | Which existing approaches does it improve upon? | `improves_upon` |
| C13 | What trade-offs are introduced? | `tradeoffs` |

### Section D — Evidence

| # | Question | Field | Answer as |
|---|---|---|---|
| D14 | How was the approach evaluated? | `evaluation_method` | text |
| D15 | What datasets were used? | `datasets_used` | list |
| D16 | What benchmarks were used? | `benchmarks_used` | list |
| D17 | Are the results statistically convincing? | `statistically_convincing` | text |
| D18 | Are there weaknesses in the evaluation? | `evaluation_weaknesses` | text |
| D19 | What questions remain unanswered? | `open_questions` | text |

### Section E — Enterprise Translation

| # | Question | Field | Answer as |
|---|---|---|---|
| E20 | What does this mean for enterprises? | `enterprise_meaning` | text |
| E21 | Which industries benefit most? | `industries_benefiting` | list |
| E22 | Which enterprise AI patterns are affected? | `enterprise_patterns_affected` | text |
| E23 | Does this influence agent design / RAG / memory / evaluation / governance / security / LLMOps / infrastructure? | `influences` | multi-select from `extraction.enterprise_ai_patterns` |
| E24 | Could this reduce cost? | `reduces_cost` | text |
| E25 | Could this improve reliability? | `improves_reliability` | text |
| E26 | Could this improve governance? | `improves_governance` | text |
| E27 | Could this improve developer productivity? | `improves_developer_productivity` | text |
| E28 | What would a CIO change after reading this? | `cio_action` | text |
| E29 | What would an AI engineering team change? | `ai_team_action` | text |

### Section F — Editorial Analysis

| # | Question | Field | Answer as |
|---|---|---|---|
| F30 | What are the three most important insights? | `top_three_insights` | list, exactly 3 |
| F31 | Which claim is likely to surprise enterprise leaders? | `surprising_claim` | text |
| F32 | Which misconceptions does this paper challenge? | `misconceptions_challenged` | text |
| F33 | What are the strongest business implications? | `business_implications` | text |
| F34 | What future trends does this suggest? | `future_trends` | text |
| F35 | Which future research should be monitored? | `future_research_to_monitor` | text |

### Section G — Knowledge Capture

| # | Question | Field |
|---|---|---|
| G36 | List the new concepts introduced | `new_concepts` |
| G37 | List important terminology | `terminology` |
| G38 | List reusable architectural patterns | `architectural_patterns` |
| G39 | List evaluation methods worth remembering | `evaluation_methods` |
| G40 | Which papers should be read next? | `papers_to_read_next` |
| G41 | Which concepts should be linked into the ArxivWiki? | `wiki_concepts_to_link` |
| G42 | Which tags should be assigned? | `tags` |

All seven are lists. `wiki_concepts_to_link` becomes the wiki page's `concepts:` front matter, `tags` becomes `tags:` — use the same wording an earlier paper already used for the same idea (check `ArxivWiki/concepts/` first) so concepts actually cluster instead of fragmenting into near-duplicate slugs. Don't invent a tag or concept that won't recur — one with a single member forever is noise, not structure.

### Section H — Content Potential

| # | Question | Field | Answer as |
|---|---|---|---|
| H43 | Is this paper worth a LinkedIn post? | `worth_linkedin_post` | text |
| H44 | Is it worth a longer article? | `worth_long_article` | text |
| H45 | What is the single strongest narrative? | `strongest_narrative` | text |
| H46 | Suggest three executive-friendly titles | `candidate_titles` | list, exactly 3 |
| H47 | Identify the one key takeaway readers should remember | `key_takeaway` | text |

### Final Assessment

| Question | Field | Answer as |
|---|---|---|
| Keep? | `keep` | boolean |
| Knowledge Base Priority | `knowledge_base_priority` | single-select from `extraction.knowledge_base_priorities` (Low, Medium, High, Essential) |
| Executive Relevance | `executive_relevance` | 1-5 |
| Technical Novelty | `technical_novelty` | 1-5 |
| Practical Applicability | `practical_applicability` | 1-5 |
| Thought Leadership Potential | `thought_leadership_potential` | 1-5 |
| Recommended Next Action | `recommended_next_action` | single-select from `extraction.recommended_next_actions` (Archive, Monitor, Add to LLM Wiki, Write LinkedIn Post, Write Long-form Article) |

**`keep` is the real gate.** A paper editorial-triage marked `Review fully` or `Priority review` from its abstract can still turn out thin, derivative, or over-claimed once you've read the whole thing — say so. `keep: false` is a normal, expected outcome, not a failure of this skill.

## Output

Write your answers to a batch JSON matching `apply_extraction.py`'s docstring, one object per paper, then run:

```bash
python skills/knowledge-extraction/scripts/apply_extraction.py <batch.json>
```

This always writes the structured record to `../../papers/metadata/extractions/<arxiv_id>.yaml` — every answer above, verbatim. That record is what makes papers selectable later (by `knowledge_base_priority`, the four 1-5 scores, `recommended_next_action`) without re-reading anything, and it's what [[editorial-strategist]] can eventually cross-reference against feedback.

**Only if `keep: true`**, it also renders `../../ArxivWiki/papers/<year>/<arxiv_id>.md` directly from that same record — front matter (title, authors, published, arxiv, `overall_score`/`recommendation`/`headline` copied from editorial-triage, plus the Final Assessment fields, `tags`, `concepts`) and a body with one section per worksheet section (Executive Summary through Content Potential, ending in Final Assessment). The wiki page is generated, not hand-authored — never edit it directly once it exists; re-run extraction and regenerate it if something needs to change, so the page and the structured record can't drift apart.

And updates `../../papers/metadata/<arxiv_id>.json`:
- `keep`, `knowledge_base_priority`, `recommended_next_action`, and the four 1-5 scores — copied in for quick lookup without opening the extraction record
- `"status": "extracted"`, `"extracted_at"` — if `keep: true`
- `"status": "evaluated"`, `"evaluated_at"` — if `keep: false` (terminal: the paper was read and judged, but doesn't get a wiki page)

Extraction does not update `papers/papers.csv` or `ArxivWiki/index.md` — hand off to [[research-librarian]] (`build_index.py`) to refresh those after a batch of extractions.

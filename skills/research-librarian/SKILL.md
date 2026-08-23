---
name: research-librarian
description: Maintain the research database — papers.csv, the ArxivWiki index, tags, concepts, and backlinks. Use this skill when the user asks to rebuild the index, update papers.csv, find papers by tag or concept, check for duplicates, or asks "what have we covered on X". Also handles archiving superseded paper versions and low-scoring PDFs. Trigger on phrases like "rebuild the index", "update the library", "find papers tagged X", "what's in the wiki about Y", "check for duplicates".
---

# Research Librarian

## Purpose

Maintain a clean research knowledge base — the "database" layer on top of what [[research-discovery]], [[editorial-triage]], and [[knowledge-extraction]] have written.

## How it works

Aggregation across files is mechanical, so it lives in `scripts/build_index.py`. Your job is to run it, interpret its report, and handle the judgment calls it deliberately leaves to you (duplicate merges, stale tag cleanup).

```bash
python skills/research-librarian/scripts/build_index.py
```

Run this after any batch of discovery/triage/extraction, or whenever the user asks a question the index should answer (tag lookups, "have we covered X").

## What the script does for you

- Rebuilds `../../papers/papers.csv` from every `papers/metadata/*.json`: Paper ID, Title, Date, Authors, Categories, Scores, Recommendation, Downloaded, Reviewed, Summarised, LinkedIn written, Status.
- Rebuilds `../../ArxivWiki/tags/<tag>.md` and `../../ArxivWiki/concepts/<concept>.md` from every wiki page's front matter — one page per tag/concept, listing member papers newest-first.
- Rebuilds `../../ArxivWiki/index.md`, grouped by recommendation tier (Priority review / Review fully / Read later / Archive / Ignore, per `screening.recommendation_order` in the config), with links to the tag and concept browsers.
- Archives PDFs for papers whose current `recommendation` is no longer `download_eligible` (per `screening.recommendations` in the config), moving them from `../../output/<year-week>/<year-week>_<arxiv_id>.pdf` to `../../archive/pdf/<year-week>/<arxiv_id>.pdf` (week subfolder preserved, but the archive keeps its own older filename convention — no week prefix) to keep the live output folder focused on what's worth keeping. Marks `"archived": true` in metadata so it isn't repeated. A paper with no `recommendation` yet (not screened, or still on an older schema) is left alone rather than archived.
- Flags (does not merge) papers with near-identical normalized titles under different arXiv IDs — logs a `FLAG possible duplicate title` line.

## What you do after running it

1. **Duplicate flags**: for each `FLAG possible duplicate title`, look at both papers' metadata. If one is genuinely a duplicate (e.g. cross-listed, or a preprint later reissued under a new ID), decide with the user whether to merge notes and archive the older entry — do not silently delete either side.
2. **Updated versions**: arXiv IDs are stable across revisions, so a paper updated after extraction won't automatically re-trigger anything. If the user flags that a paper has a newer version worth re-reading, treat it as a fresh extraction pass on the same ID (overwrite the wiki page) rather than creating a second entry, and note the revision in the page body.
3. **Backlinks**: when [[knowledge-extraction]] leaves a paper's "Related papers" section thin (common for early entries before the wiki has much in it), revisit it once more papers exist on the same tag/concept and add the missing links both directions.
4. **Reporting**: when asked "what's in the wiki about X", check `../../ArxivWiki/tags/<slug>.md` and `../../ArxivWiki/concepts/<slug>.md` first rather than re-scanning every paper file — that's the index's entire purpose.

## Paper → content chain

The backlink chain this skill is responsible for keeping legible:

```
Paper (metadata/<id>.json)
  -> Markdown (ArxivWiki/papers/<year>/<id>.md)
    -> LinkedIn article (tracked via "LinkedIn written" in papers/papers.csv, written elsewhere with Claude Co-work)
      -> Future references (papers that cite or build on this one, via Related papers links)
```

This skill does not write LinkedIn content — it only tracks whether a paper has become one, so the queue for Claude Co-work (papers with `Summarised = True` and `LinkedIn written = False`, sorted by score) is always answerable from `papers/papers.csv`.

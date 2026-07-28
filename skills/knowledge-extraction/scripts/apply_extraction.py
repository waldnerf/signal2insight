#!/usr/bin/env python3
"""Apply knowledge-extraction's full-text worksheet to a structured record,
and, only if the paper is kept, render an ArxivWiki page from that record.

The judgment happens elsewhere (an LLM reading the full PDF and answering
the Section A-H questions in knowledge-extraction/SKILL.md). This script
takes that already-decided structured output and produces two things from
one source, per paper:

  1. papers/metadata/extractions/<arxiv_id>.yaml -- always written. The
     structured record: every answer, plus the Final Assessment. This is
     what makes papers selectable later (by knowledge_base_priority, the
     four 1-5 scores, recommended_next_action) without re-reading anything.
  2. ArxivWiki/papers/<year>/<arxiv_id>.md -- written only if the Final
     Assessment's "keep" is true. Rendered directly from the same record
     (front matter + body sections A-H), never hand-authored separately, so
     the wiki page and the structured record can't drift apart.

If keep is false, no wiki page is written -- the paper was read in full and
evaluated, but full-text reading revealed it isn't durable-knowledge-worthy
even though editorial-triage's abstract-only screen thought it might be.
That's a normal, expected outcome, not an error.

Usage:
    python apply_extraction.py <extractions_batch.json> [config_path]

extractions_batch.json: a JSON array of, per paper, "arxiv_id" plus all
Section A-H fields and the Final Assessment fields -- see SKILL.md for the
full field list, or TEXT_FIELDS / LIST_FIELDS / FINAL_ASSESSMENT_FIELDS
below for the exact names this script expects.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]  # repo root/
DEFAULT_CONFIG = ROOT / "config" / "editorial-profile.yaml"
METADATA_DIR = ROOT / "papers" / "metadata"
EXTRACTIONS_DIR = ROOT / "papers" / "metadata" / "extractions"
WIKI_PAPERS_DIR = ROOT / "ArxivWiki" / "papers"

TEXT_FIELDS = [
    # Section A -- Executive Summary
    "summary_five_sentences", "executive_explanation", "architect_explanation", "central_contribution",
    # Section B -- Problem Analysis
    "industry_problem", "problem_importance", "assumptions_challenged", "gaps_identified",
    # Section C -- Technical Innovation
    "proposed_architecture", "differentiation", "novel_concepts", "improves_upon", "tradeoffs",
    # Section D -- Evidence
    "evaluation_method", "statistically_convincing", "evaluation_weaknesses", "open_questions",
    # Section E -- Enterprise Translation
    "enterprise_meaning", "enterprise_patterns_affected", "reduces_cost", "improves_reliability",
    "improves_governance", "improves_developer_productivity", "cio_action", "ai_team_action",
    # Section F -- Editorial Analysis
    "surprising_claim", "misconceptions_challenged", "business_implications",
    "future_trends", "future_research_to_monitor",
    # Section H -- Content Potential
    "worth_linkedin_post", "worth_long_article", "strongest_narrative", "key_takeaway",
]
LIST_FIELDS = [
    "datasets_used", "benchmarks_used",                          # D15/D16
    "industries_benefiting",                                     # E21
    "influences",                                                # E23, from config extraction.enterprise_ai_patterns
    "top_three_insights",                                        # F30, exactly 3
    "new_concepts", "terminology", "architectural_patterns",      # G36-38
    "evaluation_methods", "papers_to_read_next", "wiki_concepts_to_link", "tags",  # G39-42
    "candidate_titles",                                            # H46, exactly 3
]
FINAL_ASSESSMENT_FIELDS = [
    "keep", "knowledge_base_priority",
    "executive_relevance", "technical_novelty", "practical_applicability", "thought_leadership_potential",
    "recommended_next_action",
]
ALL_FIELDS = TEXT_FIELDS + LIST_FIELDS + FINAL_ASSESSMENT_FIELDS


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def render_wiki_page(arxiv_id, record, meta):
    fm = {
        "title": meta.get("title", ""),
        "authors": meta.get("authors", []),
        "published": (meta.get("published") or "")[:10],
        "arxiv": arxiv_id,
        "overall_score": meta.get("overall_score"),
        "recommendation": meta.get("recommendation"),
        "headline": (meta.get("headline") or record.get("central_contribution", "")),
        "knowledge_base_priority": record["knowledge_base_priority"],
        "executive_relevance": record["executive_relevance"],
        "technical_novelty": record["technical_novelty"],
        "practical_applicability": record["practical_applicability"],
        "thought_leadership_potential": record["thought_leadership_potential"],
        "recommended_next_action": record["recommended_next_action"],
        "tags": record["tags"],
        "concepts": record["wiki_concepts_to_link"],
    }
    front_matter = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()

    def bullets(items):
        return "\n".join(f"- {item}" for item in items) if items else "_none_"

    body = f"""## Executive Summary

**Five-sentence summary:** {record['summary_five_sentences']}

**For executives:** {record['executive_explanation']}

**For AI architects:** {record['architect_explanation']}

**Central contribution:** {record['central_contribution']}

## Problem Analysis

**Industry problem:** {record['industry_problem']}

**Why it matters:** {record['problem_importance']}

**Assumptions challenged:** {record['assumptions_challenged']}

**Gaps identified:** {record['gaps_identified']}

## Technical Innovation

**Proposed architecture:** {record['proposed_architecture']}

**What makes it different:** {record['differentiation']}

**Novel concepts:** {record['novel_concepts']}

**Improves upon:** {record['improves_upon']}

**Trade-offs:** {record['tradeoffs']}

## Evidence

**Evaluation method:** {record['evaluation_method']}

**Datasets:**
{bullets(record['datasets_used'])}

**Benchmarks:**
{bullets(record['benchmarks_used'])}

**Statistically convincing?** {record['statistically_convincing']}

**Evaluation weaknesses:** {record['evaluation_weaknesses']}

**Open questions:** {record['open_questions']}

## Enterprise Translation

**What this means for enterprises:** {record['enterprise_meaning']}

**Industries that benefit most:**
{bullets(record['industries_benefiting'])}

**Enterprise AI patterns affected:** {record['enterprise_patterns_affected']}

**Influences:** {', '.join(record['influences']) if record['influences'] else '_none_'}

**Could reduce cost:** {record['reduces_cost']}

**Could improve reliability:** {record['improves_reliability']}

**Could improve governance:** {record['improves_governance']}

**Could improve developer productivity:** {record['improves_developer_productivity']}

**What a CIO would change:** {record['cio_action']}

**What an AI engineering team would change:** {record['ai_team_action']}

## Editorial Analysis

**Top three insights:**
{bullets(record['top_three_insights'])}

**Likely to surprise enterprise leaders:** {record['surprising_claim']}

**Misconceptions challenged:** {record['misconceptions_challenged']}

**Strongest business implications:** {record['business_implications']}

**Future trends suggested:** {record['future_trends']}

**Future research to monitor:** {record['future_research_to_monitor']}

## Knowledge Capture

**New concepts:**
{bullets(record['new_concepts'])}

**Terminology:**
{bullets(record['terminology'])}

**Reusable architectural patterns:**
{bullets(record['architectural_patterns'])}

**Evaluation methods worth remembering:**
{bullets(record['evaluation_methods'])}

**Read next:**
{bullets(record['papers_to_read_next'])}

## Content Potential

**Worth a LinkedIn post?** {record['worth_linkedin_post']}

**Worth a longer article?** {record['worth_long_article']}

**Strongest narrative:** {record['strongest_narrative']}

**Candidate titles:**
{bullets(record['candidate_titles'])}

**Key takeaway:** {record['key_takeaway']}

## Final Assessment

- **Keep:** Yes
- **Knowledge Base Priority:** {record['knowledge_base_priority']}
- **Executive Relevance:** {record['executive_relevance']}/5
- **Technical Novelty:** {record['technical_novelty']}/5
- **Practical Applicability:** {record['practical_applicability']}/5
- **Thought Leadership Potential:** {record['thought_leadership_potential']}/5
- **Recommended Next Action:** {record['recommended_next_action']}
"""
    return f"---\n{front_matter}\n---\n\n{body}"


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit("Usage: python apply_extraction.py <extractions_batch.json> [config_path]")
    batch_path = Path(sys.argv[1])
    config_path = Path(sys.argv[2]) if len(sys.argv) == 3 else DEFAULT_CONFIG
    config = load_config(config_path)
    extraction = config["extraction"]

    with open(batch_path, "r", encoding="utf-8") as f:
        batch = json.load(f)

    EXTRACTIONS_DIR.mkdir(parents=True, exist_ok=True)
    counts = {"kept": 0, "not_kept": 0}
    for item in batch:
        arxiv_id = item["arxiv_id"]
        missing = [f for f in ALL_FIELDS if f not in item]
        if missing:
            sys.exit(f"{arxiv_id}: missing field(s) {missing}")
        if item["knowledge_base_priority"] not in extraction["knowledge_base_priorities"]:
            sys.exit(f"{arxiv_id}: knowledge_base_priority {item['knowledge_base_priority']!r} invalid")
        if item["recommended_next_action"] not in extraction["recommended_next_actions"]:
            sys.exit(f"{arxiv_id}: recommended_next_action {item['recommended_next_action']!r} invalid")

        record = {f: item[f] for f in ALL_FIELDS}
        with open(EXTRACTIONS_DIR / f"{arxiv_id}.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(record, f, sort_keys=False, allow_unicode=True)

        meta_path = METADATA_DIR / f"{arxiv_id}.json"
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        meta["knowledge_base_priority"] = record["knowledge_base_priority"]
        meta["recommended_next_action"] = record["recommended_next_action"]
        meta["executive_relevance"] = record["executive_relevance"]
        meta["technical_novelty"] = record["technical_novelty"]
        meta["practical_applicability"] = record["practical_applicability"]
        meta["thought_leadership_potential"] = record["thought_leadership_potential"]
        meta["keep"] = record["keep"]

        if record["keep"]:
            year = (meta.get("published") or "")[:4] or "unknown"
            wiki_dir = WIKI_PAPERS_DIR / year
            wiki_dir.mkdir(parents=True, exist_ok=True)
            (wiki_dir / f"{arxiv_id}.md").write_text(render_wiki_page(arxiv_id, record, meta), encoding="utf-8")
            meta["status"] = "extracted"
            meta["extracted_at"] = datetime.now(timezone.utc).isoformat()
            counts["kept"] += 1
        else:
            meta["status"] = "evaluated"
            meta["evaluated_at"] = datetime.now(timezone.utc).isoformat()
            counts["not_kept"] += 1

        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"Applied {len(batch)} extraction(s) from {batch_path.name}: {counts}")


if __name__ == "__main__":
    main()

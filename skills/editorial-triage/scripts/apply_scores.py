#!/usr/bin/env python3
"""Apply editorial-triage screening judgments to metadata/scores/*.yaml and metadata/*.json.

This is a mechanical write-out helper for the triage skill: the actual
screening judgment happens elsewhere (an LLM reading title+abstract and
answering the Section A-F questions in editorial-triage/SKILL.md). This
script takes that already-decided structured output, computes overall_score,
derives status/eligibility from the recommendation, and fans it out to the
two files each screening record touches.

Usage:
    python apply_scores.py <scores_batch.json>

scores_batch.json: a JSON array of, per paper:
    {
      "arxiv_id": "...",
      # Section A -- Relevance
      "enterprise_problem": "...",                       # Q1, free text
      "business_functions": ["Engineering", "Security"], # Q2, from config screening.business_functions
      "enterprise_ai_themes": ["Agentic AI", "RAG"],      # Q3, from config screening.enterprise_ai_themes
      "primary_type": "Engineering technique",            # Q4, from config screening.primary_types
      # Section B -- Strategic Importance (1-5 each)
      "architectural_influence": 4, "challenges_best_practice": 2, "novelty": 4,
      "enterprise_improvement": 5, "innovation_scale": 3,
      # Section C -- Practicality
      "implementable_today": 3,                           # Q10, 1-5
      "adoption_horizon": "<12 months",                    # Q11, from config screening.adoption_horizons
      "implementation_barriers": 2, "deployment_evidence": 2,  # Q12/13, 1-5
      # Section D -- Evidence (1-5 each)
      "validation_strength": 4, "evaluation_clarity": 4,
      "limitations_acknowledged": 3, "rigor": 4,
      # Section E -- Editorial Value (1-5 each, headline is free text)
      "executive_interest": 3, "platform_team_interest": 5, "business_implication": 4,
      "surprise_factor": 3, "linkedin_potential": 4,
      "headline": "...",                                   # Q23, free text
      # Section F -- Decision
      "recommendation": "Review fully",                    # Q24, from config screening.recommendation_order
      "recommendation_reasoning": "..."                     # Q25, free text, <=150 words
    }

overall_score is computed here as the sum of the quantitative_dimensions
listed in config/editorial-profile.yaml (currently 17 dimensions, max 85) --
never trust a precomputed sum in the input. It is a sortable/legacy-compatible
number, not the gate: status and download/extract eligibility come from the
recommendation's entry in config screening.recommendations.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]  # repo root/
DEFAULT_CONFIG = ROOT / "config" / "editorial-profile.yaml"
METADATA_DIR = ROOT / "papers" / "metadata"
SCORES_DIR = ROOT / "papers" / "metadata" / "scores"

TEXT_FIELDS = ["enterprise_problem", "headline", "recommendation_reasoning"]
LIST_FIELDS = ["business_functions", "enterprise_ai_themes"]
ENUM_FIELDS = ["primary_type", "adoption_horizon"]


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit("Usage: python apply_scores.py <scores_batch.json> [config_path]")
    batch_path = Path(sys.argv[1])
    config_path = Path(sys.argv[2]) if len(sys.argv) == 3 else DEFAULT_CONFIG
    config = load_config(config_path)
    screening = config["screening"]
    dims = screening["quantitative_dimensions"]
    recommendations = screening["recommendations"]

    with open(batch_path, "r", encoding="utf-8") as f:
        batch = json.load(f)

    SCORES_DIR.mkdir(parents=True, exist_ok=True)
    counts = {}
    for item in batch:
        arxiv_id = item["arxiv_id"]
        recommendation = item["recommendation"]
        if recommendation not in recommendations:
            sys.exit(
                f"{arxiv_id}: recommendation {recommendation!r} is not one of "
                f"{list(recommendations)} (config screening.recommendations)"
            )
        missing = [d for d in dims if d not in item]
        if missing:
            sys.exit(f"{arxiv_id}: missing quantitative dimension(s) {missing}")
        overall_score = sum(item[d] for d in dims)
        gate = recommendations[recommendation]
        counts[recommendation] = counts.get(recommendation, 0) + 1

        score_record = {}
        for field in TEXT_FIELDS + LIST_FIELDS + ENUM_FIELDS + dims:
            score_record[field] = item[field]
        score_record["overall_score"] = overall_score
        score_record["recommendation"] = recommendation
        score_record["fulltext_reassessed"] = False
        with open(SCORES_DIR / f"{arxiv_id}.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(score_record, f, sort_keys=False, allow_unicode=True)

        meta_path = METADATA_DIR / f"{arxiv_id}.json"
        with open(meta_path, "r", encoding="utf-8") as f:
            rec = json.load(f)
        rec["reviewed"] = True
        rec["overall_score"] = overall_score
        rec["recommendation"] = recommendation
        rec["status"] = gate["status"]
        rec["download_eligible"] = gate["download_eligible"]
        rec["extract_eligible"] = gate["extract_eligible"]
        rec["reviewed_at"] = datetime.now(timezone.utc).isoformat()
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=2, ensure_ascii=False)

    print(f"Applied {len(batch)} screening(s) from {batch_path.name}: {counts}")


if __name__ == "__main__":
    main()

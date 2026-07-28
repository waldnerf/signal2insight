#!/usr/bin/env python3
"""Reassess a paper's screening record after a full-text read.

editorial-triage's screening (Sections A-F, see SKILL.md) is normally
answered abstract-only. Once a paper is downloaded and Claude has read the
full PDF, abstracts routinely turn out to have omitted qualifying results,
ablations, or scope limits that change several answers -- most often the
Section B/D/E quantitative dimensions and the Section F recommendation
itself. This script is the write-out half of that reassessment: it takes
the new full-record judgment, diffs it against whatever screening record
already exists, logs the delta, and persists the update.

It never re-derives a score itself -- the reasoning happens in the calling
conversation (an LLM reading the PDF), same division of labor as
apply_scores.py, and takes the exact same per-paper record shape (see that
script's docstring for the full field list).

Usage:
    python reassess_fulltext.py <reassessment_batch.json> [config_path]

Prints a delta table (old overall_score -> new, old recommendation -> new)
and writes:
  - metadata/scores/<arxiv_id>.yaml: full record replaced, with
    fulltext_reassessed: true, reassessed_at, previous_overall_score,
    previous_recommendation, delta
  - metadata/<arxiv_id>.json: overall_score, recommendation, status, and
    eligibility flags updated to match
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
        sys.exit("Usage: python reassess_fulltext.py <reassessment_batch.json> [config_path]")
    batch_path = Path(sys.argv[1])
    config_path = Path(sys.argv[2]) if len(sys.argv) == 3 else DEFAULT_CONFIG
    config = load_config(config_path)
    screening = config["screening"]
    dims = screening["quantitative_dimensions"]
    recommendations = screening["recommendations"]

    with open(batch_path, "r", encoding="utf-8") as f:
        batch = json.load(f)

    SCORES_DIR.mkdir(parents=True, exist_ok=True)
    deltas = []
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
        new_overall_score = sum(item[d] for d in dims)
        gate = recommendations[recommendation]

        score_path = SCORES_DIR / f"{arxiv_id}.yaml"
        prior = {}
        if score_path.exists():
            with open(score_path, "r", encoding="utf-8") as f:
                prior = yaml.safe_load(f) or {}
        previous_overall_score = prior.get("overall_score")
        previous_recommendation = prior.get("recommendation")

        score_record = {}
        for field in TEXT_FIELDS + LIST_FIELDS + ENUM_FIELDS + dims:
            score_record[field] = item[field]
        score_record["overall_score"] = new_overall_score
        score_record["recommendation"] = recommendation
        score_record["fulltext_reassessed"] = True
        score_record["reassessed_at"] = datetime.now(timezone.utc).isoformat()
        score_record["previous_overall_score"] = previous_overall_score
        score_record["previous_recommendation"] = previous_recommendation
        score_record["delta"] = (
            None if previous_overall_score is None else new_overall_score - previous_overall_score
        )
        with open(score_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(score_record, f, sort_keys=False, allow_unicode=True)

        meta_path = METADATA_DIR / f"{arxiv_id}.json"
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                rec = json.load(f)
            rec["overall_score"] = new_overall_score
            rec["recommendation"] = recommendation
            rec["status"] = gate["status"]
            rec["download_eligible"] = gate["download_eligible"]
            rec["extract_eligible"] = gate["extract_eligible"]
            rec["fulltext_reassessed"] = True
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(rec, f, indent=2, ensure_ascii=False)

        deltas.append((arxiv_id, previous_overall_score, new_overall_score, previous_recommendation, recommendation))

    print(f"Reassessed {len(batch)} paper(s) from {batch_path.name}:")
    print(f"{'arxiv_id':<16}{'old':>6}{'new':>6}{'delta':>7}  {'old rec.':<16} -> new rec.")
    for arxiv_id, old, new, old_rec, new_rec in deltas:
        old_disp = "-" if old is None else str(old)
        delta_disp = "-" if old is None else f"{new - old:+d}"
        old_rec_disp = old_rec or "-"
        print(f"{arxiv_id:<16}{old_disp:>6}{new:>6}{delta_disp:>7}  {old_rec_disp:<16} -> {new_rec}")


if __name__ == "__main__":
    sys.exit(main())

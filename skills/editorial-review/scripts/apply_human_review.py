#!/usr/bin/env python3
"""Apply human review decisions from the editorial-review cycle.

Mechanical write-out only, same split as apply_scores.py / apply_extraction.py:
the decision itself (approve, or discard as Archive/Ignore) is made by the user
during the review widget, not by this script. This script only fans it out.

Usage:
    python apply_human_review.py <decisions_batch.json> [config_path]

decisions_batch.json: a JSON array of:
    {
      "arxiv_id": "2607.24663",
      "decision": "approve" | "archive" | "ignore",
      "note": "...",                        # optional; the user's reason, especially for archive/ignore
      "score_adjustments": {"novelty": 5, ...}  # optional; dimension name -> new 1-5 value
    }

"approve" never changes the paper's recommendation/status/eligibility flags --
it only marks the paper as human-reviewed and logs positive feedback.

"archive" / "ignore" overwrite the paper's recommendation to "Archive" or
"Ignore" (title case, matching config screening.recommendation_order), and
recompute status/download_eligible/extract_eligible from
config screening.recommendations exactly as apply_scores.py does -- this is
an explicit, visible override of editorial-triage's original call, not a
silent downgrade, and the original recommendation is preserved as
pre_override_recommendation on the score record for traceability.

score_adjustments lets the reviewer correct specific 1-5 dimension scores
(the same 5 fields apply_scores.py writes, per
config screening.quantitative_dimensions) independently of the overall
decision -- a paper can be approved while still correcting a miscalibrated
dimension, or archived while noting which dimension misled triage. Every
adjusted dimension is recorded as a from/to pair under
human_score_adjustments on the score record (never silently overwritten),
and overall_score is recomputed as the sum of all 5 dimensions, exactly as
apply_scores.py computes it -- never trusting a precomputed sum.

Every decision appends one line to logs/feedback.jsonl in editorial-strategist's
existing format ({"arxiv_id", "rating", "note", "date"}), with any dimension
adjustments folded into the note so a pattern across many papers ("humans
keep correcting business_translatability upward") is visible to that skill's
analysis -- this feeds the same feedback -> strategist-proposal ->
human-applied-config-change pipeline the rest of the system already uses; it
never writes to config/editorial-profile.yaml directly.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[3]  # repo root/
DEFAULT_CONFIG = ROOT / "config" / "editorial-profile.yaml"
METADATA_DIR = ROOT / "papers" / "metadata"
SCORES_DIR = METADATA_DIR / "scores"
LOG_DIR = ROOT / "logs"
FEEDBACK_PATH = LOG_DIR / "feedback.jsonl"

DECISION_TO_RECOMMENDATION = {"archive": "Archive", "ignore": "Ignore"}
DECISION_TO_RATING = {"approve": "Good", "archive": "Ignore", "ignore": "Ignore"}


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def append_feedback(arxiv_id, rating, note):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "arxiv_id": arxiv_id,
        "rating": rating,
        "note": note or "",
        "date": datetime.now(timezone.utc).date().isoformat(),
    }
    with open(FEEDBACK_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit("Usage: python apply_human_review.py <decisions_batch.json> [config_path]")
    batch_path = Path(sys.argv[1])
    config_path = Path(sys.argv[2]) if len(sys.argv) == 3 else DEFAULT_CONFIG
    config = load_config(config_path)
    recommendations = config["screening"]["recommendations"]
    dims = config["screening"]["quantitative_dimensions"]

    with open(batch_path, "r", encoding="utf-8") as f:
        batch = json.load(f)

    counts = {}
    for item in batch:
        arxiv_id = item["arxiv_id"]
        decision = item["decision"]
        note = item.get("note", "")
        adjustments = item.get("score_adjustments") or {}
        if decision not in DECISION_TO_RATING:
            sys.exit(f"{arxiv_id}: decision {decision!r} must be one of approve/archive/ignore")
        bad_dims = [d for d in adjustments if d not in dims]
        if bad_dims:
            sys.exit(f"{arxiv_id}: score_adjustments has unknown dimension(s) {bad_dims}")
        counts[decision] = counts.get(decision, 0) + 1

        meta_path = METADATA_DIR / f"{arxiv_id}.json"
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        meta["human_reviewed"] = True
        meta["human_review_decision"] = decision
        meta["human_reviewed_at"] = datetime.now(timezone.utc).isoformat()

        needs_score_write = decision in DECISION_TO_RECOMMENDATION or adjustments
        if needs_score_write:
            score_path = SCORES_DIR / f"{arxiv_id}.yaml"
            with open(score_path, "r", encoding="utf-8") as f:
                score = yaml.safe_load(f)

            if decision in DECISION_TO_RECOMMENDATION:
                new_recommendation = DECISION_TO_RECOMMENDATION[decision]
                if new_recommendation not in recommendations:
                    sys.exit(f"{arxiv_id}: {new_recommendation!r} is not in config screening.recommendations")
                score.setdefault("pre_override_recommendation", score.get("recommendation"))
                score["recommendation"] = new_recommendation
                score["human_override"] = True
                score["human_override_reason"] = note

            this_run_deltas = {}
            if adjustments:
                history = score.setdefault("human_score_adjustments", {})
                for dim, new_value in adjustments.items():
                    this_run_deltas[dim] = {"from": score.get(dim), "to": new_value}
                    history[dim] = this_run_deltas[dim]
                    score[dim] = new_value
                score["overall_score"] = sum(score[d] for d in dims)

            with open(score_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(score, f, sort_keys=False, allow_unicode=True)

            if decision in DECISION_TO_RECOMMENDATION:
                gate = recommendations[score["recommendation"]]
                meta["recommendation"] = score["recommendation"]
                meta["status"] = gate["status"]
                meta["download_eligible"] = gate["download_eligible"]
                meta["extract_eligible"] = gate["extract_eligible"]
            if adjustments:
                meta["overall_score"] = score["overall_score"]

        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        feedback_note = note
        if adjustments:
            adj_summary = "; ".join(f"{dim}: {vals['from']}->{vals['to']}" for dim, vals in this_run_deltas.items())
            feedback_note = f"{note} [score adjustments: {adj_summary}]".strip()
        append_feedback(arxiv_id, DECISION_TO_RATING[decision], feedback_note)

    print(f"Applied {len(batch)} human review decision(s) from {batch_path.name}: {counts}")


if __name__ == "__main__":
    main()

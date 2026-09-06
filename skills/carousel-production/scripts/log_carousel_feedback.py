#!/usr/bin/env python3
"""Append carousel review/approval decisions to logs/carousel-feedback.jsonl.

Mechanical write-out only, same split as every apply_*.py script in this
repo: the decision (approve/revise/reject a specific revision of a specific
deck) is made elsewhere, by the review gate in check_standards.py or by the
user at final approval. This script only records it, one line per decision,
so the deck's actual revision history survives context compaction and
becomes [[carousel-strategist]]'s only calibration signal, the same way
logs/feedback.jsonl is editorial-triage's.

Usage:
    python log_carousel_feedback.py <decisions_batch.json>

decisions_batch.json: a JSON array of:
    {
      "arxiv_id": "2608.23642",
      "revision": 2,
      "decision": "approve" | "revise" | "reject",
      "note": "what changed and why, in the reviewer's or user's own terms"
    }

"revise" is logged for every pass the writer/review loop forces, not only
the final outcome, so a recurring correction is visible to the strategist
across many decks, not just the last thing that happened to one deck.
"reject" means the deck never shipped (three-pass cap hit with no
convergence, or the user declined it outright); the note should say why.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # repo root/
LOG_DIR = ROOT / "logs"
FEEDBACK_PATH = LOG_DIR / "carousel-feedback.jsonl"

VALID_DECISIONS = {"approve", "revise", "reject"}


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python log_carousel_feedback.py <decisions_batch.json>")
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        batch = json.load(f)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    counts = {}
    with open(FEEDBACK_PATH, "a", encoding="utf-8") as f:
        for item in batch:
            decision = item.get("decision")
            if decision not in VALID_DECISIONS:
                sys.exit("%s: decision %r must be one of %s"
                         % (item.get("arxiv_id"), decision, sorted(VALID_DECISIONS)))
            entry = {
                "arxiv_id": item["arxiv_id"],
                "revision": item.get("revision", 0),
                "decision": decision,
                "note": item.get("note", ""),
                "date": datetime.now(timezone.utc).date().isoformat(),
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            counts[decision] = counts.get(decision, 0) + 1

    print("Logged %d carousel decision(s) to %s: %s"
          % (len(batch), FEEDBACK_PATH.relative_to(ROOT), counts))


if __name__ == "__main__":
    main()

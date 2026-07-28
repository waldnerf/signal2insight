#!/usr/bin/env python3
"""Research Discovery backend, phase 2: download PDFs only for the
top-ranked triaged papers, capped at download_top_n per week.

fetch.py discovers metadata only. editorial-triage screens each paper from
its abstract and assigns a recommendation (Ignore/Archive/Read later/Review
fully/Priority review — see config screening.recommendations). This script
is the gate between "screened" and "worth the storage/bandwidth of an
actual PDF" — still retrieval, not judgment: the recommendation was already
decided elsewhere, this just applies a mechanical rank-and-cap rule to it.

A paper is eligible once: reviewed, not yet downloaded, and its
recommendation's download_eligible flag is true. Eligible papers are never
dropped — if the weekly budget is exhausted, they roll over and compete
again next run, ranked by recommendation tier (Priority review before
Review fully) then overall_score, until downloaded.

Usage:
    python download_top.py [--config PATH] [--top-n 5] [--dry-run]
"""
import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch  # noqa: E402  (reuse load_config, download_pdf, pdf_path, PDF_DIR, METADATA_DIR)

ROOT = fetch.ROOT
METADATA_DIR = fetch.METADATA_DIR
PDF_DIR = fetch.PDF_DIR
LOG_DIR = fetch.LOG_DIR
DEFAULT_CONFIG = fetch.DEFAULT_CONFIG


def load_all_metadata():
    records = {}
    for path in sorted(METADATA_DIR.glob("*.json")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                records[path.stem] = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"WARN could not read {path}: {e}")
    return records


def week_bounds(now):
    start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=7)
    return start, end


def parse_iso(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--top-n", type=int, help="Override download_top_n from config")
    parser.add_argument("--dry-run", action="store_true", help="Report what would download; write nothing")
    args = parser.parse_args()

    config = fetch.load_config(args.config)
    screening = config["screening"]
    recommendations = screening["recommendations"]
    recommendation_order = screening["recommendation_order"]
    tier_rank = {name: i for i, name in enumerate(recommendation_order)}
    top_n = args.top_n or config.get("download_top_n", 5)

    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_lines = []

    def log(msg):
        line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
        log_lines.append(line)
        print(line)

    now = datetime.now(timezone.utc)
    week_start, week_end = week_bounds(now)

    metadata = load_all_metadata()

    already_this_week = 0
    for rec in metadata.values():
        if not rec.get("downloaded"):
            continue
        dl_at = parse_iso(rec.get("downloaded_at"))
        if dl_at and week_start <= dl_at < week_end:
            already_this_week += 1

    budget = max(0, top_n - already_this_week)
    log(
        f"Week of {week_start.date()}: {already_this_week} already downloaded, "
        f"budget {top_n}, remaining {budget}"
    )

    candidates = []
    for arxiv_id, rec in metadata.items():
        if not rec.get("reviewed"):
            continue
        if rec.get("downloaded"):
            continue
        recommendation = rec.get("recommendation")
        gate = recommendations.get(recommendation)
        if gate is None or not gate.get("download_eligible"):
            continue
        candidates.append((arxiv_id, rec, recommendation, rec.get("overall_score", 0)))

    # best first: recommendation tier (Priority review before Review fully), then overall_score, then recency
    candidates.sort(
        key=lambda c: (-tier_rank.get(c[2], len(recommendation_order)), c[3], c[1].get("published", "")),
        reverse=True,
    )
    log(f"{len(candidates)} eligible undownloaded candidate(s) (download_eligible recommendation)")

    to_download = candidates[:budget]
    deferred = candidates[budget:]

    downloaded_count = 0
    failures = 0
    for arxiv_id, rec, recommendation, score in to_download:
        if args.dry_run:
            log(f"WOULD DOWNLOAD {arxiv_id} ({recommendation}, score={score}): {rec.get('title', '')}")
            continue
        ok = fetch.download_pdf(rec["pdf_url"], fetch.pdf_path(arxiv_id), log)
        if ok:
            rec["downloaded"] = True
            rec["downloaded_at"] = datetime.now(timezone.utc).isoformat()
            with open(METADATA_DIR / f"{arxiv_id}.json", "w", encoding="utf-8") as f:
                json.dump(rec, f, indent=2, ensure_ascii=False)
            log(f"DOWNLOADED {arxiv_id} ({recommendation}, score={score}): {rec.get('title', '')}")
            downloaded_count += 1
        else:
            log(f"FAILED {arxiv_id} ({recommendation}, score={score}): {rec.get('title', '')}")
            failures += 1

    for arxiv_id, rec, recommendation, score in deferred:
        log(f"DEFERRED {arxiv_id} ({recommendation}, score={score}): budget exhausted, rolls over to next run")

    log(
        f"Done. downloaded={downloaded_count} failed={failures} deferred={len(deferred)} "
        f"remaining_budget_after={budget - downloaded_count}"
    )

    if not args.dry_run:
        log_file = LOG_DIR / f"download_top-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines) + "\n")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

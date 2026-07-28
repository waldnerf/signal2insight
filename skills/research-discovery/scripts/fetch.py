#!/usr/bin/env python3
"""Research Discovery backend: query arXiv, dedupe against metadata/, and
queue new papers for editorial review.

This script performs retrieval only. It never judges quality — that is
editorial-triage's job. A paper it writes always gets status "queued".

By default it writes metadata only, no PDF. Papers are scored on their
abstract first (editorial-triage); only the top-scoring papers each week
get their PDF downloaded, by download_top.py. Pass --download to fetch
PDFs immediately instead, bypassing that gate.

Usage:
    python fetch.py [--config PATH] [--categories cs.AI,cs.CL] [--lookback-days 7]
                     [--max-results 100] [--download] [--dry-run]
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[3]  # repo root/ (.../repo root/skills/research-discovery/scripts/fetch.py)
DEFAULT_CONFIG = ROOT / "config" / "editorial-profile.yaml"
METADATA_DIR = ROOT / "papers" / "metadata"
PDF_DIR = ROOT / "papers" / "pdf"  # PDFs live under PDF_DIR/<ISO year-week>/<id>.pdf — see pdf_path()
LOG_DIR = ROOT / "logs"

ARXIV_API = "http://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
BATCH_SIZE = 100
NEW_ID_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?$")


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalize_id(raw_id):
    """'http://arxiv.org/abs/2507.12345v2' -> '2507.12345'."""
    m = NEW_ID_RE.search(raw_id)
    if m:
        return m.group(1)
    return raw_id.rstrip("/").rsplit("/", 1)[-1]


def build_query(categories):
    return " OR ".join(f"cat:{c}" for c in categories)


def fetch_page(search_query, start, batch_size, log):
    params = {
        "search_query": search_query,
        "start": start,
        "max_results": batch_size,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    last_error = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError) as e:
            last_error = e
            log(f"WARN fetch attempt {attempt} failed: {e}")
            time.sleep(3 * attempt)
    raise RuntimeError(f"Failed to fetch {url} after 3 attempts: {last_error}")


def parse_entries(xml_bytes):
    root = ET.fromstring(xml_bytes)
    entries = []
    for entry in root.findall("atom:entry", ATOM_NS):
        raw_id = entry.findtext("atom:id", default="", namespaces=ATOM_NS)
        arxiv_id = normalize_id(raw_id)
        title = " ".join(entry.findtext("atom:title", default="", namespaces=ATOM_NS).split())
        abstract = " ".join(entry.findtext("atom:summary", default="", namespaces=ATOM_NS).split())
        published = entry.findtext("atom:published", default="", namespaces=ATOM_NS)
        updated = entry.findtext("atom:updated", default="", namespaces=ATOM_NS)
        authors = [
            a.findtext("atom:name", default="", namespaces=ATOM_NS)
            for a in entry.findall("atom:author", ATOM_NS)
        ]
        categories = [c.get("term") for c in entry.findall("atom:category", ATOM_NS) if c.get("term")]
        pdf_url = ""
        for link in entry.findall("atom:link", ATOM_NS):
            if link.get("title") == "pdf" or link.get("type") == "application/pdf":
                pdf_url = link.get("href")
                break
        if not pdf_url:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
        entries.append(
            {
                "arxiv_id": arxiv_id,
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "categories": categories,
                "published": published,
                "updated": updated,
                "pdf_url": pdf_url,
            }
        )
    return entries


def within_lookback(entry, cutoff):
    try:
        pub = datetime.fromisoformat(entry["published"].replace("Z", "+00:00"))
    except ValueError:
        return True
    return pub >= cutoff


def iso_week_str(when=None):
    """ISO year-week, e.g. '2026-W31'. Used for both the discovery_date
    metadata tag and the PDF download folder grouping."""
    dt = when or datetime.now(timezone.utc)
    year, week, _ = dt.isocalendar()
    return f"{year}-W{week:02d}"


def metadata_path(arxiv_id):
    return METADATA_DIR / f"{arxiv_id}.json"


def pdf_path(arxiv_id, when=None):
    """PDFs are grouped by the ISO year-week they're downloaded in:
    papers/pdf/<YYYY-Www>/<arxiv_id>.pdf — `when` defaults to now (the
    moment of download), not the paper's discovery or publish date."""
    return PDF_DIR / iso_week_str(when) / f"{arxiv_id}.pdf"


def already_known(arxiv_id):
    return metadata_path(arxiv_id).exists()


def download_pdf(pdf_url, dest, log):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, 4):
        try:
            urllib.request.urlretrieve(pdf_url, dest)
            return True
        except (urllib.error.URLError, TimeoutError) as e:
            log(f"WARN pdf download attempt {attempt} failed for {pdf_url}: {e}")
            time.sleep(3 * attempt)
    return False


def write_metadata(entry, downloaded):
    record = dict(entry)
    record["downloaded"] = downloaded
    now = datetime.now(timezone.utc)
    if downloaded:
        record["downloaded_at"] = now.isoformat()
    record["reviewed"] = False
    record["status"] = "queued"
    record["discovered_at"] = now.isoformat()
    record["discovery_date"] = iso_week_str(now)  # e.g. "2026-W31" — the week this paper was discovered
    with open(metadata_path(entry["arxiv_id"]), "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--categories", help="Comma-separated override, e.g. cs.AI,cs.CL")
    parser.add_argument("--lookback-days", type=int)
    parser.add_argument("--max-results", type=int)
    parser.add_argument(
        "--download",
        action="store_true",
        help="Also download PDFs immediately (default: metadata only — PDFs are downloaded later, "
        "for the top-scoring papers only, by download_top.py)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Query and report; write nothing")
    args = parser.parse_args()

    config = load_config(args.config)
    discovery_cfg = config.get("discovery", {})
    categories = args.categories.split(",") if args.categories else discovery_cfg.get("categories", ["cs.AI"])
    lookback_days = args.lookback_days or discovery_cfg.get("lookback_days", 7)
    max_results = min(args.max_results or discovery_cfg.get("max_results", 100), 100)  # hard cap: 100/week

    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_lines = []

    def log(msg):
        line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
        log_lines.append(line)
        print(line)

    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    search_query = build_query(categories)
    log(f"Querying arXiv: categories={categories} lookback_days={lookback_days} max_results={max_results}")

    seen = 0
    new_count = 0
    skipped_duplicate = 0
    skipped_old = 0
    download_failures = 0
    fatal_error = None
    start = 0
    stop = False

    try:
        while seen < max_results and not stop:
            page_size = min(BATCH_SIZE, max_results - seen)
            try:
                xml_bytes = fetch_page(search_query, start, page_size, log)
            except RuntimeError as e:
                log(f"FATAL {e}")
                fatal_error = e
                break
            entries = parse_entries(xml_bytes)
            if not entries:
                break
            for entry in entries:
                seen += 1
                if not within_lookback(entry, cutoff):
                    skipped_old += 1
                    stop = True  # results are newest-first: once we hit one out of range, the rest are too
                    continue
                if already_known(entry["arxiv_id"]):
                    skipped_duplicate += 1
                    continue
                if args.dry_run:
                    log(f"NEW (dry-run) {entry['arxiv_id']}: {entry['title']}")
                    new_count += 1
                    continue
                downloaded = False
                if args.download:
                    downloaded = download_pdf(entry["pdf_url"], pdf_path(entry["arxiv_id"]), log)
                    if not downloaded:
                        download_failures += 1
                write_metadata(entry, downloaded)
                log(f"NEW {entry['arxiv_id']}: {entry['title']} (downloaded={downloaded})")
                new_count += 1
            start += len(entries)
            if len(entries) < page_size:
                break
            if not stop:
                time.sleep(3)  # be polite to the arXiv API between pages
    finally:
        log(
            f"Done. seen={seen} new={new_count} duplicates={skipped_duplicate} "
            f"out_of_lookback={skipped_old} download_failures={download_failures}"
        )
        if not args.dry_run:
            log_file = LOG_DIR / f"fetch-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
            with open(log_file, "w", encoding="utf-8") as f:
                f.write("\n".join(log_lines) + "\n")

    if fatal_error:
        return 2
    return 1 if download_failures else 0


if __name__ == "__main__":
    sys.exit(main())

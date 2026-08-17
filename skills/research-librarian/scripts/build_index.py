#!/usr/bin/env python3
"""Research Librarian backend: rebuild papers.csv, ArxivWiki/index.md,
ArxivWiki/tags/, and ArxivWiki/concepts/ from metadata/ and ArxivWiki/papers/.

Purely mechanical aggregation over files other skills already wrote — this
script never scores or summarizes a paper, it only indexes what exists.
It also does light housekeeping: archiving PDFs for papers whose current
recommendation is no longer download_eligible, and flagging (not merging)
likely duplicate titles for a human/Claude judgment call.

Usage:
    python build_index.py [--config PATH]
"""
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

# Paper titles, tags and concepts routinely contain non-Latin-1 characters, which
# raise UnicodeEncodeError on a cp1252 Windows console and abort the run mid-write.
# Degrade unprintable characters instead of failing; generated files stay UTF-8.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parents[3]  # repo root/
DEFAULT_CONFIG = ROOT / "config" / "editorial-profile.yaml"
METADATA_DIR = ROOT / "papers" / "metadata"
SCORES_DIR = ROOT / "papers" / "metadata" / "scores"
WIKI_DIR = ROOT / "ArxivWiki"
WIKI_PAPERS_DIR = WIKI_DIR / "papers"
TAGS_DIR = WIKI_DIR / "tags"
CONCEPTS_DIR = WIKI_DIR / "concepts"
PDF_DIR = ROOT / "papers" / "pdf"  # PDFs live under PDF_DIR/<ISO year-week>/<id>.pdf
ARCHIVE_DIR = ROOT / "archive"
LOG_DIR = ROOT / "logs"
CSV_PATH = ROOT / "papers" / "papers.csv"
INDEX_PATH = WIKI_DIR / "index.md"

CSV_COLUMNS = [
    "Paper ID", "Title", "Date", "Authors", "Categories", "Scores", "Recommendation",
    "Downloaded", "Reviewed", "Summarised", "Keep", "KB Priority", "Next Action",
    "LinkedIn written", "Status",
]
FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n(.*)$", re.DOTALL)


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled"


def load_metadata():
    records = {}
    for path in sorted(METADATA_DIR.glob("*.json")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                records[path.stem] = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"WARN could not read {path}: {e}")
    return records


def load_score(arxiv_id):
    path = SCORES_DIR / f"{arxiv_id}.yaml"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_wiki_file(arxiv_id):
    matches = list(WIKI_PAPERS_DIR.glob(f"*/{arxiv_id}.md"))
    return matches[0] if matches else None


def find_pdf(arxiv_id):
    """PDFs live under PDF_DIR/<ISO year-week>/<arxiv_id>.pdf — glob for it
    rather than assuming a flat layout, same pattern as find_wiki_file."""
    matches = list(PDF_DIR.glob(f"*/{arxiv_id}.pdf"))
    return matches[0] if matches else None


def parse_front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        print(f"WARN bad front matter in {path}: {e}")
        return {}, text
    return fm, m.group(2)


def build_papers_csv(metadata, log):
    rows = []
    for arxiv_id, rec in sorted(metadata.items()):
        wiki_file = find_wiki_file(arxiv_id)
        rows.append({
            "Paper ID": arxiv_id,
            "Title": rec.get("title", ""),
            "Date": (rec.get("published") or "")[:10],
            "Authors": "; ".join(rec.get("authors", [])),
            "Categories": ", ".join(rec.get("categories", [])),
            "Scores": rec.get("overall_score", ""),
            "Recommendation": rec.get("recommendation", ""),
            "Downloaded": rec.get("downloaded", False),
            "Reviewed": rec.get("reviewed", False),
            "Summarised": wiki_file is not None,
            "Keep": rec.get("keep", ""),
            "KB Priority": rec.get("knowledge_base_priority", ""),
            "Next Action": rec.get("recommended_next_action", ""),
            "LinkedIn written": rec.get("linkedin_written", False),
            "Status": rec.get("status", ""),
        })
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    log(f"papers.csv: {len(rows)} rows")
    return rows


def collect_wiki_entries(log):
    """Return list of (arxiv_id, front_matter, path) for every wiki page."""
    entries = []
    for path in sorted(WIKI_PAPERS_DIR.glob("*/*.md")):
        fm, _ = parse_front_matter(path)
        if not fm:
            log(f"WARN {path} has no parseable front matter, skipping")
            continue
        arxiv_id = path.stem
        entries.append((arxiv_id, fm, path))
    return entries


def build_tag_and_concept_pages(entries, log):
    by_tag = defaultdict(list)
    by_concept = defaultdict(list)
    for arxiv_id, fm, path in entries:
        rel = Path("..") / path.relative_to(WIKI_DIR)
        for tag in fm.get("tags") or []:
            by_tag[tag].append((arxiv_id, fm, rel))
        for concept in fm.get("concepts") or []:
            by_concept[concept].append((arxiv_id, fm, rel))

    for dir_path, groups, kind in ((TAGS_DIR, by_tag, "tag"), (CONCEPTS_DIR, by_concept, "concept")):
        existing = {p.stem for p in dir_path.glob("*.md")}
        current = set()
        for name, members in groups.items():
            slug = slugify(name)
            current.add(slug)
            lines = [f"# {kind.title()}: {name}", "", f"{len(members)} paper(s).", ""]
            for arxiv_id, fm, rel in sorted(members, key=lambda m: m[1].get("published", ""), reverse=True):
                title = fm.get("title", arxiv_id)
                lines.append(f"- [{title}]({rel.as_posix()}) — {fm.get('published', '')} — {fm.get('recommendation', '')}")
            (dir_path / f"{slug}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        stale = existing - current
        for slug in stale:
            log(f"NOTE stale {kind} page tags/{slug}.md has no current members (left in place, not deleted)")
        log(f"{kind}s: {len(current)} pages")
    return by_tag, by_concept


def detect_duplicate_titles(metadata, log):
    seen = {}
    dupes = []
    for arxiv_id, rec in metadata.items():
        key = re.sub(r"[^a-z0-9]+", "", rec.get("title", "").lower())
        if not key:
            continue
        if key in seen:
            dupes.append((seen[key], arxiv_id, rec.get("title", "")))
        else:
            seen[key] = arxiv_id
    for a, b, title in dupes:
        log(f"FLAG possible duplicate title between {a} and {b}: {title!r} (not merged automatically)")
    return dupes


def archive_non_eligible_pdfs(metadata, config, log):
    recommendations = config["screening"]["recommendations"]
    (ARCHIVE_DIR / "pdf").mkdir(parents=True, exist_ok=True)
    moved = 0
    for arxiv_id, rec in metadata.items():
        if rec.get("archived"):
            continue
        recommendation = rec.get("recommendation")
        if recommendation is None:
            continue  # not screened yet (or on the pre-screening-rubric schema) -- leave alone
        gate = recommendations.get(recommendation)
        if gate is None or gate.get("download_eligible"):
            continue  # unknown tier, or still eligible -- nothing to archive
        src = find_pdf(arxiv_id)
        if src is None:
            continue
        # preserve the week subfolder in the archive, same layout as the live PDF folder
        dest_dir = ARCHIVE_DIR / "pdf" / src.parent.name
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / src.name
        src.rename(dest)
        rec["archived"] = True
        with open(METADATA_DIR / f"{arxiv_id}.json", "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=2, ensure_ascii=False)
        log(f"ARCHIVE {arxiv_id}.pdf (recommendation {recommendation!r} is not download_eligible)")
        moved += 1
    log(f"archived {moved} non-eligible PDF(s)")
    return moved


def build_index_md(metadata, entries, config, log):
    by_tier = defaultdict(list)
    for arxiv_id, fm, path in entries:
        rel = path.relative_to(WIKI_DIR)
        by_tier[fm.get("recommendation", "Unscored")].append((arxiv_id, fm, rel))

    lines = ["# ArxivWiki Index", "", f"_Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}_", ""]
    lines.append(f"{len(entries)} paper(s) in the wiki. {len(metadata)} total tracked in `papers/papers.csv`.")
    lines.append("")
    for tier in config["screening"]["recommendation_order"]:
        members = by_tier.get(tier, [])
        if not members:
            continue
        lines.append(f"## {tier}")
        lines.append("")
        for arxiv_id, fm, rel in sorted(members, key=lambda m: m[1].get("published", ""), reverse=True):
            lines.append(f"- [{fm.get('title', arxiv_id)}]({rel.as_posix()}) — {fm.get('published', '')}")
        lines.append("")
    lines.append("## Browse")
    lines.append("")
    lines.append("- [Tags](tags/)")
    lines.append("- [Concepts](concepts/)")
    if (WIKI_DIR / "dashboard.html").exists():
        lines.append("- [Knowledge Dashboard](dashboard.html) — concept/tag frequency view, built by [[theme-dashboard]]")
    lines.append("")
    INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")
    log(f"index.md: {len(entries)} entries across {len(by_tier)} tiers")


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = parser.parse_args()

    config = load_config(args.config)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_lines = []

    def log(msg):
        line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
        log_lines.append(line)
        print(line)

    metadata = load_metadata()
    log(f"loaded {len(metadata)} metadata record(s)")

    build_papers_csv(metadata, log)
    entries = collect_wiki_entries(log)
    build_tag_and_concept_pages(entries, log)
    build_index_md(metadata, entries, config, log)
    detect_duplicate_titles(metadata, log)
    archive_non_eligible_pdfs(metadata, config, log)

    log_file = LOG_DIR / f"build_index-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

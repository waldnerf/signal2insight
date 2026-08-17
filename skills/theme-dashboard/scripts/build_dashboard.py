#!/usr/bin/env python3
"""Rebuild ArxivWiki/dashboard.html: a concept/tag frequency dashboard over
knowledge-extraction's kept ("Essential"-tier durable knowledge) papers.

Purely mechanical aggregation, same spirit as research-librarian/build_index.py
-- this script never judges a paper, it only counts and renders tags/concepts
that knowledge-extraction already assigned to papers where keep: true.

The output is an HTML *fragment* (no <!DOCTYPE>/<html>/<head>/<body>) so it can
be published as-is via the Artifact tool without double-wrapping, while still
rendering acceptably if opened directly as a file.

Usage:
    python build_dashboard.py [--config PATH]
"""
import json
import sys
from collections import defaultdict
from datetime import datetime
from html import escape
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
METADATA_DIR = ROOT / "papers" / "metadata"
EXTRACTIONS_DIR = METADATA_DIR / "extractions"
WIKI_DIR = ROOT / "ArxivWiki"
LOG_DIR = ROOT / "logs"
OUTPUT_PATH = WIKI_DIR / "dashboard.html"


def load_metadata():
    records = {}
    for path in sorted(METADATA_DIR.glob("*.json")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                records[path.stem] = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
    return records


def load_kept_extractions(log):
    """Return list of (arxiv_id, extraction_record) where keep is true."""
    kept = []
    for path in sorted(EXTRACTIONS_DIR.glob("*.yaml")):
        with open(path, "r", encoding="utf-8") as f:
            rec = yaml.safe_load(f) or {}
        if rec.get("keep"):
            kept.append((path.stem, rec))
    log(f"loaded {len(kept)} kept extraction record(s)")
    return kept


def wiki_relpath(arxiv_id, meta):
    year = (meta.get("published") or "")[:4] or "unknown"
    path = WIKI_DIR / "papers" / year / f"{arxiv_id}.md"
    if path.exists():
        return f"papers/{year}/{arxiv_id}.md"
    return None


def aggregate(kept, metadata):
    concept_papers = defaultdict(list)
    tag_papers = defaultdict(list)
    for arxiv_id, rec in kept:
        meta = metadata.get(arxiv_id, {})
        title = meta.get("title", arxiv_id)
        headline = meta.get("headline") or rec.get("central_contribution", "")
        rel = wiki_relpath(arxiv_id, meta)
        entry = {"arxiv_id": arxiv_id, "title": title, "headline": headline, "rel": rel,
                  "priority": rec.get("knowledge_base_priority", "")}
        for concept in rec.get("wiki_concepts_to_link") or []:
            concept_papers[concept].append(entry)
        for tag in rec.get("tags") or []:
            tag_papers[tag].append(entry)
    return concept_papers, tag_papers


def chip_scale(count, max_count):
    """Map a frequency count to a (font_size_rem, teal_tint) pair."""
    if max_count <= 1:
        ratio = 1.0
    else:
        ratio = count / max_count
    size = 0.85 + ratio * 0.95  # 0.85rem .. 1.8rem
    tint = 0.25 + ratio * 0.55  # opacity/tint of the accent fill
    return round(size, 2), round(tint, 2)


def render_cloud(groups, kind_label):
    if not groups:
        return f'<p class="empty">No {kind_label.lower()} yet.</p>'
    max_count = max(len(v) for v in groups.values())
    items = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0].lower()))
    chips = []
    for name, papers in items:
        size, tint = chip_scale(len(papers), max_count)
        title_attr = escape(" | ".join(p["title"] for p in papers[:6]))
        chips.append(
            f'<span class="chip" style="--size:{size}rem;--tint:{tint}" '
            f'title="{title_attr}">{escape(name)}'
            f'<span class="count">{len(papers)}</span></span>'
        )
    return f'<div class="cloud">{"".join(chips)}</div>'


def render_paper_rows(kept, metadata):
    rows = []
    for arxiv_id, rec in sorted(kept, key=lambda kv: (metadata.get(kv[0], {}).get("published") or ""), reverse=True):
        meta = metadata.get(arxiv_id, {})
        title = escape(meta.get("title", arxiv_id))
        headline = escape(meta.get("headline") or rec.get("central_contribution", ""))
        priority = escape(rec.get("knowledge_base_priority", ""))
        published = escape((meta.get("published") or "")[:10])
        rel = wiki_relpath(arxiv_id, meta)
        tags = ", ".join(escape(t) for t in (rec.get("tags") or []))
        title_cell = f'<a href="{escape(rel)}">{title}</a>' if rel else title
        rows.append(
            f"<tr><td>{title_cell}<div class=\"headline\">{headline}</div></td>"
            f'<td><span class="pill pill-{priority.lower()}">{priority}</span></td>'
            f"<td>{tags}</td><td class=\"num\">{published}</td></tr>"
        )
    return "\n".join(rows)


TEMPLATE = """<style>
  .s2i-dash {{
    --paper: #F3F4F2; --ink: #1B2321; --muted: #6B6F76; --border: #D8DAD5;
    --signal: #0E7C86; --signal-ink: #ffffff; --surface: #ffffff;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    color: var(--ink); background: var(--paper);
    max-width: 100%; box-sizing: border-box; line-height: 1.45;
  }}
  @media (prefers-color-scheme: dark) {{
    .s2i-dash {{ --paper: #12151A; --ink: #E7EAE7; --muted: #9AA09B; --border: #2A2F2C;
      --signal: #2FB8C4; --signal-ink: #06141a; --surface: #181C1F; }}
  }}
  :root[data-theme="dark"] .s2i-dash {{ --paper: #12151A; --ink: #E7EAE7; --muted: #9AA09B; --border: #2A2F2C;
    --signal: #2FB8C4; --signal-ink: #06141a; --surface: #181C1F; }}
  :root[data-theme="light"] .s2i-dash {{ --paper: #F3F4F2; --ink: #1B2321; --muted: #6B6F76; --border: #D8DAD5;
    --signal: #0E7C86; --signal-ink: #ffffff; --surface: #ffffff; }}
  .s2i-dash * {{ box-sizing: border-box; }}
  .s2i-mast {{
    background: var(--ink); color: var(--paper); padding: 1.5rem 1.75rem;
    border-radius: 10px 10px 0 0;
  }}
  @media (prefers-color-scheme: dark) {{ .s2i-mast {{ background: #06090c; }} }}
  :root[data-theme="dark"] .s2i-mast {{ background: #06090c; }}
  :root[data-theme="light"] .s2i-mast {{ background: var(--ink); }}
  .s2i-eyebrow {{
    font-family: ui-monospace, "SFMono-Regular", "JetBrains Mono", "Cascadia Code", Consolas, monospace;
    font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase; opacity: 0.7;
  }}
  .s2i-title {{
    font-family: ui-monospace, "SFMono-Regular", "JetBrains Mono", "Cascadia Code", Consolas, monospace;
    font-size: 1.4rem; font-weight: 700; letter-spacing: 0.01em; margin: 0.35rem 0 1rem;
    text-wrap: balance;
  }}
  .s2i-stats {{ display: flex; flex-wrap: wrap; gap: 1.75rem; }}
  .s2i-stat {{ font-family: ui-monospace, "SFMono-Regular", "JetBrains Mono", Consolas, monospace; }}
  .s2i-stat .num {{ font-size: 1.5rem; font-variant-numeric: tabular-nums; display: block; }}
  .s2i-stat .lbl {{ font-size: 0.7rem; opacity: 0.65; letter-spacing: 0.06em; text-transform: uppercase; }}
  .s2i-body {{ background: var(--surface); border: 1px solid var(--border); border-top: none;
    border-radius: 0 0 10px 10px; padding: 1.75rem; }}
  .s2i-section {{ margin-bottom: 2rem; }}
  .s2i-section h2 {{
    font-family: ui-monospace, "SFMono-Regular", "JetBrains Mono", Consolas, monospace;
    font-size: 0.85rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted);
    margin: 0 0 0.9rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border);
  }}
  .cloud {{ display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; }}
  .chip {{
    font-family: ui-monospace, "SFMono-Regular", "JetBrains Mono", Consolas, monospace;
    font-size: var(--size); line-height: 1; padding: 0.42em 0.7em; border-radius: 999px;
    background: color-mix(in srgb, var(--signal) calc(var(--tint) * 100%), var(--surface));
    color: color-mix(in srgb, var(--signal-ink) calc(var(--tint) * 100%), var(--ink));
    border: 1px solid color-mix(in srgb, var(--signal) 40%, var(--border));
    display: inline-flex; align-items: baseline; gap: 0.45em; cursor: default;
    transition: transform 0.12s ease;
  }}
  .chip:hover {{ transform: translateY(-1px); }}
  .chip .count {{
    font-size: 0.62em; opacity: 0.75; background: color-mix(in srgb, currentColor 18%, transparent);
    border-radius: 999px; padding: 0.15em 0.5em;
  }}
  .empty {{ color: var(--muted); font-style: italic; font-size: 0.9rem; }}
  .s2i-table-wrap {{ overflow-x: auto; }}
  table.s2i-table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; }}
  table.s2i-table th {{
    text-align: left; font-family: ui-monospace, "SFMono-Regular", "JetBrains Mono", Consolas, monospace;
    font-size: 0.68rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted);
    padding: 0.5rem 0.6rem; border-bottom: 1px solid var(--border);
  }}
  table.s2i-table td {{ padding: 0.65rem 0.6rem; border-bottom: 1px solid var(--border); vertical-align: top; }}
  table.s2i-table td.num {{ font-variant-numeric: tabular-nums; white-space: nowrap; color: var(--muted); }}
  table.s2i-table a {{ color: var(--signal); text-decoration: none; font-weight: 600; }}
  table.s2i-table a:hover {{ text-decoration: underline; }}
  .headline {{ color: var(--muted); font-size: 0.82rem; margin-top: 0.2rem; }}
  .pill {{
    display: inline-block; font-size: 0.72rem; font-weight: 600; padding: 0.2em 0.6em;
    border-radius: 999px; border: 1px solid var(--border); white-space: nowrap;
  }}
  .pill-essential {{ background: color-mix(in srgb, var(--signal) 22%, var(--surface)); color: var(--signal); border-color: var(--signal); }}
  .pill-high {{ background: color-mix(in srgb, var(--signal) 10%, var(--surface)); color: var(--ink); }}
  .s2i-footer {{ margin-top: 1.25rem; font-size: 0.75rem; color: var(--muted); }}
</style>
<div class="s2i-dash">
  <div class="s2i-mast">
    <div class="s2i-eyebrow">signal2insights &middot; knowledge dashboard</div>
    <div class="s2i-title">Dominant Concepts &amp; Tags in the ArxivWiki</div>
    <div class="s2i-stats">
      <div class="s2i-stat"><span class="num">{papers_tracked}</span><span class="lbl">Papers Tracked</span></div>
      <div class="s2i-stat"><span class="num">{papers_kept}</span><span class="lbl">Kept (Essential)</span></div>
      <div class="s2i-stat"><span class="num">{concept_count}</span><span class="lbl">Distinct Concepts</span></div>
      <div class="s2i-stat"><span class="num">{tag_count}</span><span class="lbl">Distinct Tags</span></div>
    </div>
  </div>
  <div class="s2i-body">
    <div class="s2i-section">
      <h2>Concepts</h2>
      {concept_cloud}
    </div>
    <div class="s2i-section">
      <h2>Themes / Tags</h2>
      {tag_cloud}
    </div>
    <div class="s2i-section">
      <h2>Source Papers</h2>
      <div class="s2i-table-wrap">
        <table class="s2i-table">
          <thead><tr><th>Paper</th><th>Priority</th><th>Tags</th><th>Published</th></tr></thead>
          <tbody>
{paper_rows}
          </tbody>
        </table>
      </div>
    </div>
    <div class="s2i-footer">Regenerated {generated_at} from {papers_kept} kept extraction record(s). Chip size and tint scale with frequency.</div>
  </div>
</div>
"""


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_lines = []

    def log(msg):
        line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
        log_lines.append(line)
        print(line)

    metadata = load_metadata()
    kept = load_kept_extractions(log)
    concept_papers, tag_papers = aggregate(kept, metadata)

    html = TEMPLATE.format(
        papers_tracked=len(metadata),
        papers_kept=len(kept),
        concept_count=len(concept_papers),
        tag_count=len(tag_papers),
        concept_cloud=render_cloud(concept_papers, "concepts"),
        tag_cloud=render_cloud(tag_papers, "tags"),
        paper_rows=render_paper_rows(kept, metadata),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    log(f"dashboard.html: {len(concept_papers)} concept(s), {len(tag_papers)} tag(s), {len(kept)} paper(s)")

    log_file = LOG_DIR / f"build_dashboard-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    log_file.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

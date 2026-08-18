#!/usr/bin/env python3
"""Render a one-pager summary for Priority-review papers still awaiting
full-text extraction, for the editorial-review human review cycle.

Mechanical write-out only: it never scores or judges a paper, it renders
already-decided triage (or, if present, extraction) fields into a short
markdown file. The judgment behind those fields belongs to editorial-triage
and knowledge-extraction -- with one exception (see --narrative below).

The provenance line under the title follows the score record: a paper whose
screening came from reassess_fulltext.py is labelled full-text reassessed,
everything else keeps the abstract-only pre-extraction caveat.

Usage:
    python build_summary.py [arxiv_id ...] [--config PATH] [--limit N] [--narrative PATH]

With no arxiv_id arguments, selects every paper where recommendation ==
"Priority review" and no extraction record exists yet (pre-extraction),
capped at --limit (default 20).

--narrative PATH: a JSON object keyed by arxiv_id, e.g.
    {
      "2607.24663": {
        "high_level_summary": "...",
        "key_highlights": ["...", "...", "..."],
        "why_it_matters": "...",
        "recommended_industries": ["...", "...", "..."],
        "business_applications": ["...", "...", "..."]
      }
    }
These fields require reading the abstract and reasoning about it -- they are
not derivable from editorial-triage's structured scoring fields (which only
capture internal business_functions, e.g. Engineering/Compliance, never
company domains or concrete use cases), so this script never invents them.
Author them the same way editorial-triage authors its own answers (an LLM
reasoning over the paper), then pass them in here; the script only renders
what it's given. Recommended Audience combines score.business_functions
(mechanical, always present) with narrative.recommended_industries (authored,
optional) so "who" spans both internal roles and company domains. A paper
with no narrative entry still gets a summary, just without the authored
sections.
"""
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[3]  # repo root/
DEFAULT_CONFIG = ROOT / "config" / "editorial-profile.yaml"
METADATA_DIR = ROOT / "papers" / "metadata"
SCORES_DIR = METADATA_DIR / "scores"
EXTRACTIONS_DIR = METADATA_DIR / "extractions"
SUMMARIES_DIR = ROOT / "ArxivWiki" / "summaries"


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


ELIGIBLE_TIERS = ("Priority review", "Review fully")


def select_pending(limit):
    """Every Priority-review or Review-fully paper not yet past the extraction
    checkpoint, ranked by overall_score descending, capped at limit."""
    candidates = []
    for path in sorted(METADATA_DIR.glob("*.json")):
        arxiv_id = path.stem
        with open(path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        if meta.get("recommendation") not in ELIGIBLE_TIERS:
            continue
        if (EXTRACTIONS_DIR / f"{arxiv_id}.yaml").exists():
            continue  # already past this checkpoint
        candidates.append((arxiv_id, meta.get("overall_score", 0)))
    candidates.sort(key=lambda kv: kv[1], reverse=True)
    return [arxiv_id for arxiv_id, _ in candidates[:limit]]


def render_summary(arxiv_id, meta, score, narrative=None, max_score=25, dims=None):
    narrative = narrative or {}
    # Rank the rubric's own 1-5 dimensions, named by config. Selecting every int
    # in the record instead would also pick up reassess_fulltext.py's bookkeeping
    # fields (previous_overall_score, delta) and render them as "/5" scores.
    dims = dims or [k for k, v in score.items() if isinstance(v, int) and k != "overall_score"]
    top_dims = sorted(
        ((k, score[k]) for k in dims if isinstance(score.get(k), int)),
        key=lambda kv: kv[1], reverse=True,
    )[:5]
    dim_lines = "\n".join(f"- **{k.replace('_', ' ')}**: {v}/5" for k, v in top_dims)
    # A paper reassessed by reassess_fulltext.py has been read in full, so the
    # pre-extraction caveat would be a false statement on its summary.
    if score.get("fulltext_reassessed"):
        provenance = (
            "_Full-text reassessed: screened on the complete PDF, not the abstract alone. "
            "Not yet through [[knowledge-extraction]]._"
        )
    else:
        provenance = "_Pre-extraction: this paper has only been screened on its abstract, not read in full yet._"
    lines = [
        f"# {meta.get('title', arxiv_id)}",
        "",
        f"arXiv: [{arxiv_id}]({meta.get('pdf_url', '')}) &middot; Published {meta.get('published', '')[:10]} &middot; "
        f"Recommendation: **{score.get('recommendation', '')}** (score {score.get('overall_score', '')}/{max_score})",
        "",
        provenance,
        "",
    ]
    if narrative.get("high_level_summary"):
        lines += ["## High-Level Summary", "", narrative["high_level_summary"], ""]
    if narrative.get("key_highlights"):
        lines += ["## Key Highlights", ""]
        lines += [f"- {h}" for h in narrative["key_highlights"]]
        lines += [""]
    if narrative.get("why_it_matters"):
        lines += ["## Why It Matters for Enterprise AI", "", narrative["why_it_matters"], ""]
    if narrative.get("business_applications"):
        lines += ["## Business Applications", ""]
        lines += [f"- {a}" for a in narrative["business_applications"]]
        lines += [""]
    if score.get("business_functions") or narrative.get("recommended_industries"):
        lines += ["## Recommended Audience", ""]
        if score.get("business_functions"):
            lines += [f"**Roles:** {', '.join(score['business_functions'])}", ""]
        if narrative.get("recommended_industries"):
            lines += [f"**Industries:** {', '.join(narrative['recommended_industries'])}", ""]
    lines += [
        "## Headline",
        "",
        score.get("headline", ""),
        "",
        "## Why triage flagged this",
        "",
        score.get("recommendation_reasoning", ""),
        "",
        "## Triage Detail",
        "",
        f"**Problem it addresses:** {score.get('enterprise_problem', '')}",
        "",
        f"**Enterprise AI themes:** {', '.join(score.get('enterprise_ai_themes', []))}",
        "",
        "**Top scoring dimensions:**",
        "",
        dim_lines,
        "",
    ]
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("arxiv_ids", nargs="*")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--narrative", default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    # Max possible overall_score = 5 points per quantitative dimension, derived from
    # config rather than hardcoded so a rubric change can't leave a stale denominator.
    dims = config["screening"]["quantitative_dimensions"]
    max_score = 5 * len(dims)
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

    all_narrative = {}
    if args.narrative:
        with open(args.narrative, "r", encoding="utf-8") as f:
            all_narrative = json.load(f)

    arxiv_ids = args.arxiv_ids or select_pending(args.limit)
    if not arxiv_ids:
        print("No Priority-review, pre-extraction papers found.")
        return 0

    written = []
    for arxiv_id in arxiv_ids:
        meta_path = METADATA_DIR / f"{arxiv_id}.json"
        score_path = SCORES_DIR / f"{arxiv_id}.yaml"
        if not meta_path.exists() or not score_path.exists():
            print(f"WARN skipping {arxiv_id}: missing metadata or score record")
            continue
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        with open(score_path, "r", encoding="utf-8") as f:
            score = yaml.safe_load(f)
        out_path = SUMMARIES_DIR / f"{arxiv_id}.md"
        out_path.write_text(
            render_summary(arxiv_id, meta, score, all_narrative.get(arxiv_id), max_score, dims),
            encoding="utf-8",
        )
        written.append(arxiv_id)
        print(f"wrote {out_path.relative_to(ROOT)}")

    print(f"Done. {len(written)} summary/summaries written: {', '.join(written)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

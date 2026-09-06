#!/usr/bin/env python3
"""Lint a carousel brief against skills/carousel-production/SKILL.md's brief gate.

A brief is authored before any writer subagent runs (see SKILL.md, "Brief
stage"): the key takeaway, the framework choice, the storyline, the
standalone-test self-certification, the supporting elements, and per-slide
visual notes. This script checks the mechanical half of that gate, the same
split as check_standards.py: deterministic checks live here, the standalone
verdict itself is a judgment the brief's author records, not something a
regex can decide.

Usage:
    python check_brief.py <arxiv_id> [--brief PATH]

Exit code is 1 if any ERROR was raised, otherwise 0.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_standards as cs  # noqa: E402  (reuse resolve_dir, load_source, squash, check_title, Report)

FM_RE = re.compile(r'\A---\n(.*?)\n---\n', re.S)
STORYLINE_RE = re.compile(r'^\s*(\d+)\.\s*(?:\[(\w[\w-]*)\]\s*)?(.+?)\s*$', re.M)
BULLET_RE = re.compile(r'^\s*-\s*(.+?)\s*$', re.M)
TAG_RE = re.compile(r'^\[(paper|external(?:,\s*[^,\]]+,\s*(\d{4}))?)\]\s*(.+)$', re.I)
VISUAL_RE = re.compile(r'^\s*-\s*slide\s+(\d+)\s*:\s*(.+?)\s*$', re.M | re.I)

DEPTH_DEFAULTS = {'dual-track': (11, 12), 'spec-cards': (13, 14)}  # (typical, ceiling-ish)


def brief_path_for(arxiv_id):
    return cs.paper_path(arxiv_id, '_carousel-brief.md')


def section(text, heading):
    """Body text under '## <heading>' up to the next '## ' or end of file."""
    m = re.search(r'^##\s+%s\s*$' % re.escape(heading), text, re.M | re.I)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r'^##\s+', rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def check(arxiv_id, brief_path):
    rep = cs.Report()
    text = brief_path.read_text(encoding='utf-8', errors='replace')

    fm = FM_RE.match(text)
    if not fm:
        rep.add('ERROR', 'frontmatter', 'no YAML frontmatter')
        return rep
    block = fm.group(1)

    def fm_field(name):
        m = re.search(r'^%s:\s*(.+)$' % name, block, re.M)
        return m.group(1).strip('"\' ') if m else None

    pattern = fm_field('depth_pattern')
    declared_slides = fm_field('slides')
    framework_fm = fm_field('framework')

    src, nparts = cs.load_source(arxiv_id)
    hay = cs.squash(src) if nparts else ''

    # ---- 1. key takeaway traces to the paper --------------------------
    takeaway = section(text, 'Key takeaway')
    if not takeaway or not takeaway.strip():
        rep.add('ERROR', 'key takeaway', 'missing or empty')
    elif nparts == 0:
        rep.add('WARN', 'key takeaway', 'no source files for %s, cannot verify it traces to the paper' % arxiv_id)
    else:
        needle = cs.squash(takeaway.strip().splitlines()[0])
        if needle and needle not in hay:
            rep.add('ERROR', 'key takeaway',
                    'does not appear in the paper (or any stored source); trace it or rewrite it',
                    takeaway.strip().splitlines()[0])

    # ---- 3. framework choice, stated with a reason --------------------
    framework = section(text, 'Framework choice')
    if not framework or not framework.strip():
        rep.add('ERROR', 'framework choice', 'missing or empty')
    elif not re.search(r'\b(scr|pyramid)\b', framework, re.I):
        rep.add('ERROR', 'framework choice', 'does not name scr or pyramid')
    elif len(framework.split()) < 6:
        rep.add('WARN', 'framework choice', 'no visible reason, just the label')

    # ---- 5. storyline titles, and 4. page count -----------------------
    storyline = section(text, 'Storyline')
    titles = []
    if not storyline:
        rep.add('ERROR', 'storyline', 'missing "## Storyline" section')
    else:
        for num, stage, title in STORYLINE_RE.findall(storyline):
            titles.append((int(num), stage, title))
            cs.check_title(rep, 'storyline %s' % num, title)
        if not titles:
            rep.add('ERROR', 'storyline', 'no numbered lines found ("1. [stage] Title")')

    n = len(titles)
    if declared_slides is None:
        rep.add('WARN', 'frontmatter', 'slides: not declared')
    elif declared_slides.isdigit() and int(declared_slides) != n:
        rep.add('ERROR', 'storyline',
                'frontmatter says slides: %s but storyline has %d numbered lines' % (declared_slides, n))
    if n > cs.SLIDE_CEILING:
        rep.add('ERROR', 'storyline', '%d slides exceeds the ceiling of %d' % (n, cs.SLIDE_CEILING))
    if pattern in DEPTH_DEFAULTS:
        typical, ceiling = DEPTH_DEFAULTS[pattern]
        if n and n > ceiling:
            rep.add('WARN', 'storyline',
                    '%d slides is above the usual range for %s (%d-%d); fine if deliberate' % (n, pattern, typical, ceiling))

    # ---- 6. standalone-test self-certification ------------------------
    standalone = section(text, 'Standalone test')
    if not standalone:
        rep.add('ERROR', 'standalone test', 'missing "## Standalone test" section')
    else:
        v = re.search(r'^\s*verdict:\s*(yes|no)\s*$', standalone, re.M | re.I)
        r = re.search(r'^\s*reason:\s*(.+)$', standalone, re.M | re.I)
        if not v:
            rep.add('ERROR', 'standalone test', 'no "verdict: yes|no" line')
        elif v.group(1).lower() == 'no':
            rep.add('ERROR', 'standalone test',
                    'verdict is no: the titles do not argue the case yet, revise the storyline before proceeding')
        if not r or not r.group(1).strip():
            rep.add('WARN', 'standalone test', 'verdict has no stated reason')

    # ---- 2. supporting elements, tagged and traceable ------------------
    elements = section(text, 'Supporting elements')
    if not elements or not elements.strip():
        rep.add('WARN', 'supporting elements', 'none listed')
    else:
        for line in BULLET_RE.findall(elements):
            m = TAG_RE.match(line)
            if not m:
                rep.add('ERROR', 'supporting elements',
                        'bullet has no [paper] or [external, publisher, year] tag', line[:80])
                continue
            tag, year, fact = m.group(1), m.group(2), m.group(3)
            if tag.lower() == 'paper':
                if nparts == 0:
                    rep.add('WARN', 'supporting elements', 'no source files, cannot verify a [paper] element', fact[:80])
                elif cs.squash(fact) and cs.squash(fact) not in hay:
                    rep.add('WARN', 'supporting elements',
                            '[paper] element not found verbatim in the source; check it is a paraphrase, not an invention',
                            fact[:80])
            elif year is None:
                rep.add('ERROR', 'supporting elements',
                        '[external] element missing a publisher and a year', fact[:80])

    # ---- 7. at least one visual note -----------------------------------
    visuals = section(text, 'Visuals')
    vlines = VISUAL_RE.findall(visuals) if visuals else []
    if not vlines:
        rep.add('ERROR', 'visuals', 'no "- Slide N: ..." visual notes found')
    elif titles and len(vlines) < max(1, n // 3):
        rep.add('WARN', 'visuals', 'only %d visual note(s) for %d slides, sparse' % (len(vlines), n))

    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('arxiv_id')
    ap.add_argument('--brief', help='override path to the brief file')
    args = ap.parse_args()

    brief_path = Path(args.brief) if args.brief else brief_path_for(args.arxiv_id)
    if brief_path is None or not brief_path.exists():
        sys.exit('no carousel-brief.md found for %s (looked under output/*/*_%s*)'
                  % (args.arxiv_id, args.arxiv_id))

    print('\n=== %s ===' % args.arxiv_id)
    print('brief: %s' % brief_path.relative_to(cs.ROOT))
    rep = check(args.arxiv_id, brief_path)
    print('\n-- findings --')
    rep.dump()
    nerr = len(rep.errors())
    print('\n%d error(s), %d warning(s)' % (nerr, len(rep.rows) - nerr))
    if nerr:
        print('\n  REVISE: the brief gate is not clear, fix the errors above and recheck')
    else:
        print('\n  PROCEED: brief gate clear, safe to spawn carousel-writer')
    return 1 if nerr else 0


if __name__ == '__main__':
    sys.exit(main())

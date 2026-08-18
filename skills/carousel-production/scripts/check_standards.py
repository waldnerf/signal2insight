#!/usr/bin/env python3
"""Lint a carousel draft against skills/carousel-production/writing-standards.md.

Mechanical checks only. Everything here is deterministic and decidable by a
script: dashes, banned phrases, attribution, title case, negation-led claims,
slide budget, slide body word count under dual-track, and whether quoted
strings appear verbatim in the source. The judgment calls (does the arc hold,
would a commercial leader stall, is a claim overstated) belong to the two
reviewer subagents, not to this file.

The script also prints the title spine, because the standalone test in
writing-standards.md is the single most useful check and it needs a human eye.

Usage:
    python check_standards.py <arxiv_id> [--draft PATH] [--quiet-spine]
    python check_standards.py --all

Exit code is 1 if any ERROR was raised, otherwise 0. Warnings never fail the
run: they are prompts for a human to look, not verdicts.
"""
import argparse
import io
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[3]
CAROUSELS = ROOT / 'carousels'
FULLTEXT = ROOT / 'papers' / 'text'
SUMMARIES = ROOT / 'ArxivWiki' / 'summaries'
WIKI = ROOT / 'ArxivWiki' / 'papers'
EXTRACTIONS = ROOT / 'papers' / 'metadata' / 'extractions'

SLIDE_CEILING = 14

# writing-standards.md: "Target 100 words in the body, with 120 as a hard
# ceiling." Applies to dual-track only; spec-cards' dedicated cards are a
# different, deliberately denser structure with no length rule of its own.
WORD_TARGET = 100
WORD_CEILING = 120

# Ligatures survive PDF text extraction and would otherwise turn a verbatim
# quote into a false mismatch (configuration vs con[fi]guration).
LIGATURES = {
    'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi',
    'ﬄ': 'ffl', 'ﬅ': 'st', 'ﬆ': 'st',
}

BANNED = [
    'transform', 'unlock', 'game changer', 'game-changer', 'cutting edge',
    'cutting-edge', 'revolutionary', 'powerful', 'seamless', 'leverage ai',
    'harness', 'supercharge', "in today's rapidly changing world",
    'opens up possibilities', 'valuable insights', 'promising direction',
    'could fundamentally change how', 'paradigm shift', 'best-in-class',
]

ATTRIBUTION = ['the authors', 'the researchers', 'the paper argues',
               'the study finds', 'the study shows']

NEGATION = [r"\bnot\b", r"\bnever\b", r"\bwithout\b", r"\bcannot\b", r"n't\b"]

# Tokens that legitimately carry capitals mid-title, so the title-case
# heuristic does not fire on every proper noun and acronym.
ALLOW_CAPS = {
    'ai', 'cpg', 'llm', 'api', 'mece', 'roi', 'pepsico', 'promoai', 'pricingai',
    'rgm', 'milp', 'lightgbm', 'gurobi', 'stan', 'scipy', 'databricks',
    'bayesian', 'gaussian', 'monte', 'carlo', 'linkedin', 'arxiv', 'informs',
    'christmas', 'europe', 'european', 'us', 'uk', 'eu',
}

SLIDE_RE = re.compile(r'^##\s+Slide\s+(\d+)\s*[·:.-]\s*(.+?)\s*$', re.M)
FM_RE = re.compile(r'\A---\n(.*?)\n---\n', re.S)

# Pull quotes live on blockquote lines and never span a newline. Scanning the
# whole document instead matches YAML string values and any stray apostrophe
# pair, which is how the first version of this script produced four false
# positives on a clean draft.
QUOTE_RE = re.compile(u'[“"]([^“”"\n]{25,})[”"]')
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['\-][A-Za-z0-9]+)*")


def slide_bodies(text):
    """{slide number: body text, heading line stripped} for one draft."""
    marks = list(SLIDE_RE.finditer(text))
    out = {}
    for i, m in enumerate(marks):
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[int(m.group(1))] = text[start:end]
    return out


def squash(s):
    """Normalise for verbatim comparison: fold ligatures, NFKC, unify quotes
    and dashes, collapse whitespace, lowercase."""
    for lig, rep in LIGATURES.items():
        s = s.replace(lig, rep)
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('’', "'").replace('‘', "'")
    s = s.replace('“', '"').replace('”', '"')
    s = s.replace('—', ' ').replace('–', ' ').replace('-', ' ')
    s = re.sub(r'[^a-z0-9 ]+', ' ', s.lower())
    return re.sub(r'\s+', ' ', s).strip()


class Report:
    def __init__(self):
        self.rows = []

    def add(self, sev, where, msg, detail=''):
        self.rows.append((sev, where, msg, detail))

    def errors(self):
        return [r for r in self.rows if r[0] == 'ERROR']

    def dump(self):
        if not self.rows:
            print('  no findings')
            return
        order = {'ERROR': 0, 'WARN': 1}
        for sev, where, msg, detail in sorted(self.rows, key=lambda r: (order[r[0]], r[1])):
            print('  %-5s %-10s %s' % (sev, where, msg))
            if detail:
                print('  %-5s %-10s   %s' % ('', '', detail))


def load_source(arxiv_id):
    """Everything the quotes could legitimately have come from.

    The cleaned full text comes first and is the one that matters: a quote
    lifted from the paper will not appear in a summary that paraphrases it,
    which is why quote checking was advisory before papers/text/ existed.
    """
    parts = []
    f = FULLTEXT / ('%s.md' % arxiv_id)
    if f.exists():
        parts.append(f.read_text(encoding='utf-8', errors='replace'))
    s = SUMMARIES / ('%s.md' % arxiv_id)
    if s.exists():
        parts.append(s.read_text(encoding='utf-8', errors='replace'))
    for p in WIKI.glob('*/%s.md' % arxiv_id):
        parts.append(p.read_text(encoding='utf-8', errors='replace'))
    e = EXTRACTIONS / ('%s.yaml' % arxiv_id)
    if e.exists():
        parts.append(e.read_text(encoding='utf-8', errors='replace'))
    return '\n'.join(parts), len(parts)


def check(arxiv_id, draft_path, show_spine=True):
    rep = Report()
    text = draft_path.read_text(encoding='utf-8', errors='replace')

    # ---- frontmatter -------------------------------------------------
    fm = FM_RE.match(text)
    if not fm:
        rep.add('WARN', 'frontmatter', 'no YAML frontmatter, so the depth pattern is unrecorded')
        pattern = None
    else:
        block = fm.group(1)
        m = re.search(r'^depth_pattern:\s*(\S+)', block, re.M)
        pattern = m.group(1).strip('"\'') if m else None
        if pattern is None:
            rep.add('WARN', 'frontmatter', 'depth_pattern missing; record it so the choice accumulates')
        elif pattern not in ('dual-track', 'spec-cards'):
            rep.add('WARN', 'frontmatter', 'unknown depth_pattern %r' % pattern)
        if not re.search(r'^source:', block, re.M):
            rep.add('ERROR', 'frontmatter', 'no source: pointer')

    # ---- slides ------------------------------------------------------
    slides = SLIDE_RE.findall(text)
    if not slides:
        rep.add('ERROR', 'structure', 'no "## Slide N · Title" headings found')
        return rep, [], pattern
    n = len(slides)
    if n > SLIDE_CEILING:
        rep.add('ERROR', 'structure', '%d slides exceeds the ceiling of %d' % (n, SLIDE_CEILING))

    nums = [int(a) for a, _ in slides]
    if nums != list(range(1, n + 1)):
        rep.add('WARN', 'structure', 'slide numbers are not a clean 1..%d run: %s' % (n, nums))

    # ---- whole-document mechanics ------------------------------------
    for ch, name in (('—', 'em dash'), ('–', 'en dash')):
        for m in re.finditer(re.escape(ch), text):
            line = text.count('\n', 0, m.start()) + 1
            ctx = text[max(0, m.start() - 40):m.start() + 40].replace('\n', ' ')
            rep.add('ERROR', 'line %d' % line, '%s' % name, '...%s...' % ctx.strip())

    low = text.lower()
    for phrase in BANNED:
        for m in re.finditer(re.escape(phrase), low):
            line = text.count('\n', 0, m.start()) + 1
            rep.add('ERROR', 'line %d' % line, 'banned phrase: %r' % phrase)
    for phrase in ATTRIBUTION:
        for m in re.finditer(re.escape(phrase), low):
            line = text.count('\n', 0, m.start()) + 1
            rep.add('ERROR', 'line %d' % line,
                    'attribution: %r, name the organisation instead' % phrase)

    # ---- titles ------------------------------------------------------
    titles = []
    for num, title in slides:
        titles.append((int(num), title))
        where = 'slide %s' % num

        if not re.search(r'[a-z]', title):
            rep.add('WARN', where, 'title has no lowercase, check it is a sentence')

        words = re.findall(r"[A-Za-z][A-Za-z'&]*", title)
        capped = [w for w in words[1:]
                  if w[:1].isupper() and w.lower() not in ALLOW_CAPS and not w.isupper()]
        if len(capped) >= 3:
            rep.add('WARN', where, 'looks like title case, use sentence case',
                    'capitalised: %s' % ', '.join(capped[:6]))

        for pat in NEGATION:
            if re.search(pat, title, re.I):
                rep.add('WARN', where, 'title claim is built on negation, assert the positive',
                        title)
                break

        if len(title.split()) < 5:
            rep.add('WARN', where, 'title may be a label rather than a claim', title)

    # ---- body word count (dual-track only) ----------------------------
    if pattern == 'dual-track':
        bodies = slide_bodies(text)
        for num, _ in slides:
            where = 'slide %s' % num
            wc = len(WORD_RE.findall(bodies.get(int(num), '')))
            if wc > WORD_CEILING:
                rep.add('ERROR', where,
                        'body is %d words, exceeds the %d-word ceiling' % (wc, WORD_CEILING))
            elif wc > WORD_TARGET:
                rep.add('WARN', where,
                        'body is %d words, over the %d-word target (ceiling %d)'
                        % (wc, WORD_TARGET, WORD_CEILING))

    # ---- quotes verbatim against source ------------------------------
    # Pull quotes only ever sit on blockquote lines, and the frontmatter is
    # excluded outright: scanning the whole document matches YAML string
    # values and reports them as failed quotes.
    body = text[fm.end():] if fm else text
    quotes = []
    for ln in body.splitlines():
        if ln.lstrip().startswith('>'):
            quotes.extend(QUOTE_RE.findall(ln))

    src, nparts = load_source(arxiv_id)
    if quotes:
        if nparts == 0:
            rep.add('WARN', 'quotes', 'no source files for %s, cannot verify %d quote(s)'
                    % (arxiv_id, len(quotes)))
        else:
            hay = squash(src)
            for q in quotes:
                needle = squash(q)
                if not needle or needle in hay:
                    continue
                # A misquote and an unverifiable quote are different problems.
                # If the opening words are present but the whole string is not,
                # the text was altered: that is an error. If the opening words
                # are absent too, the quote came from something this repo does
                # not hold (the PDF full text), which a human must resolve.
                prefix = ' '.join(needle.split()[:6])
                short = '"%s"' % (q[:90] + ('...' if len(q) > 90 else ''))
                if prefix and prefix in hay:
                    rep.add('ERROR', 'quotes', 'quote altered from the source wording', short)
                else:
                    rep.add('WARN', 'quotes',
                            'quote not present in any stored source, verify by hand', short)

    return rep, titles, pattern


def run(arxiv_id, draft_path, show_spine=True):
    print('\n=== %s ===' % arxiv_id)
    print('draft: %s' % draft_path.relative_to(ROOT))
    rep, titles, pattern = check(arxiv_id, draft_path, show_spine)

    if show_spine and titles:
        print('\n-- title spine (%d slides, depth_pattern=%s) --' % (len(titles), pattern))
        print('   read these alone. if they do not argue the case, the arc is wrong.\n')
        for num, t in titles:
            print('  %2d. %s' % (num, t))

    print('\n-- findings --')
    rep.dump()
    nerr = len(rep.errors())
    print('\n%d error(s), %d warning(s)' % (nerr, len(rep.rows) - nerr))
    return nerr


# ---------------------------------------------------------------- the gate
# Thresholds are a starting point, set before any deck had been scored. See
# "The loop" in SKILL.md: recalibrate them there after a few real runs rather
# than letting them drift by reinterpretation.
PRIMARY_MIN = 4      # B1 so-what, T1 mechanism
DIMENSION_MIN = 3    # every other dimension: 2 or below fails
SUBTOTAL_MIN = 19    # out of 25, per reviewer
MAX_PASSES = 3

PRIMARY = {'B1': 'so-what', 'T1': 'mechanism'}
SCORE_RE = re.compile(r'^\s*([BT][1-5])\s+([a-z-]+)\s*:\s*([1-5])\s*$', re.M)
DEFECT_RE = re.compile(r'^\s*(blockers|wrong|majors|overstated|unverifiable|minors)\s*:\s*(\d+)\s*$', re.M)
REOPEN_RE = re.compile(r'had to reopen the deck to answer\s*:\s*(yes|no)', re.I)


def read_review(path):
    if not path.exists():
        return None
    t = path.read_text(encoding='utf-8', errors='replace')
    return {
        'scores': {k: int(v) for k, _, v in SCORE_RE.findall(t)},
        'defects': {k: int(v) for k, v in DEFECT_RE.findall(t)},
        'reopened': (REOPEN_RE.search(t).group(1).lower() == 'yes'
                     if REOPEN_RE.search(t) else None),
    }


def gate(arxiv_id):
    d = CAROUSELS / arxiv_id
    reviews = {'business': read_review(d / 'review-business.md'),
               'technical': read_review(d / 'review-technical.md')}

    print('\n=== gate: %s ===' % arxiv_id)
    missing = [k for k, v in reviews.items() if v is None]
    if missing:
        print('  LOOP: no review file for %s' % ', '.join(missing))
        return 1

    reasons, total = [], {}
    for who, r in reviews.items():
        if not r['scores']:
            reasons.append('%s report has no SCORES block' % who)
            continue
        sub = sum(r['scores'].values())
        total[who] = sub
        for code, val in sorted(r['scores'].items()):
            label = PRIMARY.get(code)
            if label and val < PRIMARY_MIN:
                reasons.append('%s %s (%s) = %d, primary must be >= %d'
                               % (who, code, label, val, PRIMARY_MIN))
            elif not label and val < DIMENSION_MIN:
                reasons.append('%s %s = %d, floor is %d' % (who, code, val, DIMENSION_MIN))
        if sub < SUBTOTAL_MIN:
            reasons.append('%s subtotal %d/25, bar is %d' % (who, sub, SUBTOTAL_MIN))
        for k in ('blockers', 'wrong'):
            if r['defects'].get(k, 0):
                reasons.append('%s filed %d %s' % (who, r['defects'][k], k))
        if r['reopened']:
            reasons.append('%s had to reopen the deck for the primary test' % who)

    for who, sub in sorted(total.items()):
        print('  %-10s %d/25  %s' % (who, sub, ' '.join(
            '%s=%d' % (c, v) for c, v in sorted(reviews[who]['scores'].items()))))

    # `revision` is monotonic and is the deck's history; it never rewinds.
    # `pass_reset_at` is how a human grants a fresh budget without erasing that
    # history, and it stays in the file so the grant is auditable rather than
    # implied. Effective passes = revision - pass_reset_at.
    passes, revision, reset_at = 0, 0, 0
    draft = d / 'draft-carousel.md'
    if draft.exists():
        t = draft.read_text(encoding='utf-8', errors='replace')
        m = re.search(r'^revision:\s*(\d+)', t, re.M)
        revision = int(m.group(1)) if m else 0
        m = re.search(r'^pass_reset_at:\s*(\d+)', t, re.M)
        reset_at = int(m.group(1)) if m else 0
        passes = max(0, revision - reset_at)
    print('  writer passes: %d of %d%s' % (
        passes, MAX_PASSES,
        '  (revision %d, budget reset at %d)' % (revision, reset_at) if reset_at else ''))

    if not reasons:
        print('\n  PROCEED: every gate cleared, take it to the user')
        return 0
    print('\n  %d gate failure(s):' % len(reasons))
    for r in reasons:
        print('    - %s' % r)
    if passes >= MAX_PASSES:
        print('\n  PROCEED (cap): %d passes used. Take it to the user with the'
              ' failures above and say what you think the underlying cause is.' % passes)
        return 0
    print('\n  LOOP: revise without consulting the user, then re-run reviewers')
    return 1


# ------------------------------------------------------------------ churn
# A writer pass should touch the slides that drew findings and leave the rest
# alone. Every unrequested edit is a chance to break something that was
# already working, which has happened twice on this pipeline's first deck.
SLIDE_SPLIT_RE = re.compile(r'^##\s+Slide\s+(\d+)\s*[·:.-]', re.M)
FINDING_SLIDE_RE = re.compile(r'^\s*SLIDE\s+(\d+)', re.M | re.I)


def split_slides(text):
    """{slide number: body text} for one draft."""
    marks = list(SLIDE_SPLIT_RE.finditer(text))
    out = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[int(m.group(1))] = re.sub(r'\s+', ' ', text[m.start():end]).strip()
    return out


def snapshot(arxiv_id):
    d = CAROUSELS / arxiv_id
    draft = d / 'draft-carousel.md'
    if not draft.exists():
        print('  no draft at %s' % draft)
        return 1
    t = draft.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'^revision:\s*(\d+)', t, re.M)
    rev = int(m.group(1)) if m else 0
    hist = d / 'history'
    hist.mkdir(parents=True, exist_ok=True)
    dst = hist / ('rev-%02d.md' % rev)
    dst.write_text(t, encoding='utf-8')
    print('snapshot: %s' % dst.relative_to(ROOT))
    return 0


def churn(arxiv_id):
    """Which slides changed, and did each change have a finding behind it."""
    d = CAROUSELS / arxiv_id
    draft = d / 'draft-carousel.md'
    hist = sorted((d / 'history').glob('rev-*.md')) if (d / 'history').exists() else []
    print('\n=== churn: %s ===' % arxiv_id)
    if not draft.exists():
        print('  no draft')
        return 1
    cur_text = draft.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'^revision:\s*(\d+)', cur_text, re.M)
    cur_rev = int(m.group(1)) if m else 0
    prior = [p for p in hist if p.stem != 'rev-%02d' % cur_rev]
    if not prior:
        print('  no earlier snapshot to compare against.')
        print('  run --snapshot after each pass so the next one can be checked.')
        return 0
    base = prior[-1]
    print('  %s  ->  revision %d' % (base.name, cur_rev))

    old = split_slides(base.read_text(encoding='utf-8', errors='replace'))
    new = split_slides(cur_text)

    flagged = set()
    for f in ('review-business.md', 'review-technical.md'):
        p = d / f
        if p.exists():
            flagged |= {int(n) for n in
                        FINDING_SLIDE_RE.findall(p.read_text(encoding='utf-8', errors='replace'))}

    changed = {n for n in set(old) | set(new) if old.get(n) != new.get(n)}
    churned = sorted(changed - flagged)
    untouched = sorted(flagged - changed)

    print('  slides: %d  changed: %d  had findings: %d'
          % (len(new), len(changed), len(flagged)))
    if churned:
        print('\n  CHURN, changed with no finding against it: %s'
              % ', '.join(str(n) for n in churned))
        print('  Each one is an unrequested edit. Confirm it was needed, or revert it.')
    if untouched:
        print('\n  UNADDRESSED, had a finding and did not change: %s'
              % ', '.join(str(n) for n in untouched))
        print('  Either the finding was rejected on the record, or it was missed.')
    if not churned and not untouched:
        print('\n  CLEAN: every change had a finding, every finding drew a change.')
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('arxiv_id', nargs='?')
    ap.add_argument('--gate', action='store_true',
                    help='apply the review gate instead of linting the draft')
    ap.add_argument('--snapshot', action='store_true',
                    help='copy the current draft into history/ before the next pass')
    ap.add_argument('--churn', action='store_true',
                    help='compare against the last snapshot: what changed, and why')
    ap.add_argument('--draft', help='explicit path, overrides the default location')
    ap.add_argument('--all', action='store_true', help='every draft under carousels/')
    ap.add_argument('--quiet-spine', action='store_true')
    args = ap.parse_args()

    for flag, fn in (('gate', gate), ('snapshot', snapshot), ('churn', churn)):
        if getattr(args, flag):
            if not args.arxiv_id:
                ap.error('--%s needs an arxiv_id' % flag)
            return fn(args.arxiv_id)

    targets = []
    if args.all:
        for d in sorted(CAROUSELS.glob('*/draft-carousel.md')):
            targets.append((d.parent.name, d))
    elif args.arxiv_id:
        p = Path(args.draft) if args.draft else CAROUSELS / args.arxiv_id / 'draft-carousel.md'
        targets.append((args.arxiv_id, p))
    else:
        ap.error('give an arxiv_id or --all')

    if not targets:
        print('no drafts found under %s' % CAROUSELS)
        return 0

    total = 0
    for arxiv_id, path in targets:
        if not path.exists():
            print('\n=== %s ===\n  MISSING: %s' % (arxiv_id, path))
            total += 1
            continue
        total += run(arxiv_id, path, not args.quiet_spine)

    print('\nmechanical checks only. arc, accessibility and overstatement are')
    print('reviewer judgments, not lint findings.')
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())

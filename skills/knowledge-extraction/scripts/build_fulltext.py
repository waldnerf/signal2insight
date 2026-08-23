#!/usr/bin/env python3
"""Extract a downloaded PDF to cleaned markdown at
output/<year-week>/<year-week>_<arxiv_id>.md, beside its source PDF.

The body only: references, bibliography, acknowledgements and every appendix
are dropped. What remains is the argument of the paper, which is what the
downstream skills actually read.

Why this exists: nothing in this repository held the full text, so no
automated check could confirm that a quotation in a carousel matched what the
paper said. Deriving the text once, into a file the scripts can read, closes
that gap for every skill rather than one.

Mechanical write-out only. It makes no judgment about the paper.

Usage:
    python build_fulltext.py <arxiv_id> [<arxiv_id> ...]
    python build_fulltext.py --all          every downloaded PDF without a text file
    python build_fulltext.py --all --force  rebuild them all
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdftext  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / 'output'

PAGE_RE = re.compile(r'^=== page (\d+) ===$', re.M)

# A terminal heading ends the body. Matched at line start only, because
# "see Appendix A" appears mid-sentence constantly and must not cut a paper in
# half. The lookahead matters: text extraction frequently glues the heading to
# the first entry, producing "ReferencesYonas Atinafu and..." on one line, so
# requiring the heading to sit alone on its line misses most real papers.
TERMINAL_RE = re.compile(
    r'^\s*(?:'
    r'appendix\s+[a-z0-9]+\b'
    r'|appendices\b'
    r'|supplementary\s+material'
    r'|(?:references|bibliography|acknowledge?ments?|works\s+cited)'
    r'(?=\s*$|[A-Z\[])'
    r')',
    re.I | re.M)

# Markers that only cluster inside a bibliography. Used to confirm a candidate
# heading really opens one, which is more reliable than a position rule: some
# papers place references before their appendices, and extraction order does
# not always follow reading order.
BIBLIO_MARKERS = [
    r'https?://', r'arxiv:', r'\bdoi\b', r'\bpp\.\s*\d', r'\bvol\.\s*\d',
    r'in\s+proceedings', r'et\s+al\.', r'\[\d{1,3}\]', r'\bpreprint\b',
]
BIBLIO_RE = re.compile('|'.join(BIBLIO_MARKERS), re.I)

# How much text after a candidate heading to inspect, and how many marker hits
# it takes to call it a bibliography.
TAIL_WINDOW = 3000
TAIL_HITS = 4

# A line that is itself a reference entry, for the papers whose heading did not
# survive extraction at all.
ENTRY_RE = re.compile(r'^\s*\[\d{1,3}\]')

SECTION_RE = re.compile(r'^(\d+)\.\s+([A-Z][^\n]{2,80})$')
SUBSECTION_RE = re.compile(r'^(\d+\.\d+)\.?\s+([A-Z][^\n]{2,80})$')


def find_pdf(arxiv_id):
    """PDFs are grouped by ISO download week, which is not derivable from the
    id or from discovery_date, so glob rather than compute the path.
    Filename is <year-week>_<arxiv_id>.pdf, e.g. output/2026-W31/2026-W31_2607.25891.pdf."""
    hits = sorted(OUTPUT_DIR.glob('*/*_%s.pdf' % arxiv_id))
    return hits[0] if hits else None


def strip_running_lines(pages):
    """Drop headers and footers: short lines repeating across many pages."""
    if len(pages) < 4:
        return pages
    counts = {}
    for body in pages:
        for ln in set(l.strip() for l in body.splitlines() if l.strip()):
            if len(ln) <= 120:
                counts[ln] = counts.get(ln, 0) + 1
    threshold = max(3, int(len(pages) * 0.4))
    running = {ln for ln, n in counts.items() if n >= threshold}
    # A bare page number differs every page, so catch it by shape instead.
    out = []
    for body in pages:
        keep = []
        for ln in body.splitlines():
            s = ln.strip()
            if not s or s in running or re.fullmatch(r'\d{1,3}', s):
                continue
            keep.append(ln)
        out.append('\n'.join(keep))
    return out


# Function words carry prose and are nearly absent from a reference list,
# which is a list of names, titles and venues. Citation density alone cannot
# tell the two apart: a related-work section is every bit as citation-dense as
# a bibliography, and judging on density alone silently deletes it.
STOPWORDS = {
    'the', 'of', 'and', 'to', 'a', 'in', 'is', 'that', 'for', 'it', 'as',
    'we', 'this', 'are', 'with', 'be', 'on', 'by', 'not', 'or', 'but', 'they',
    'which', 'from', 'can', 'our', 'these', 'their', 'when', 'has', 'have',
    'was', 'were', 'an', 'if', 'than', 'then', 'because', 'while', 'each',
    'its', 'may', 'more', 'most', 'such', 'also', 'how', 'do', 'does',
}
WORD_RE = re.compile(r"[A-Za-z']+")
PROSE_STOPWORD_FLOOR = 0.20


def stopword_ratio(text):
    words = [w.lower() for w in WORD_RE.findall(text)]
    if len(words) < 40:
        return 1.0
    return sum(1 for w in words if w in STOPWORDS) / len(words)


def is_biblio_page(page):
    """A page that is mostly citations rather than prose about citations.

    Two conditions, both required. Dense citation markers, and prose-poor: a
    reference list runs about 10 to 15 percent function words where ordinary
    academic prose runs 30 to 45 percent. Dropping the second condition eats
    introductions and related-work sections, which is a silent and expensive
    failure, because the reader never learns the framing argument is missing.
    """
    body = page.strip()
    if len(body) < 200:
        return False
    hits = len(BIBLIO_RE.findall(body))
    if hits < 8 or hits / (len(body) / 400.0) < 1.0:
        return False
    return stopword_ratio(body) < PROSE_STOPWORD_FLOOR


def cut_pages(pages):
    """Drop terminal matter, working page by page.

    Extraction order does not reliably follow reading order, so truncating the
    concatenated stream at the first terminal heading can throw away body text
    that happens to be emitted later. Two rules avoid that:

      * An appendix heading really is terminal, so it truncates from there on.
      * References are identified by citation density per page, which holds
        regardless of where the page landed in the stream.

    Acknowledgements never truncate. They are short, they sit next to the
    conclusion, and treating them as terminal is what previously destroyed
    two thirds of a paper whose pages came out of order.
    """
    dropped_at = None

    # Appendices are genuinely terminal in reading order, so the first one
    # ends the paper. Everything from that point is discarded.
    for i, page in enumerate(pages):
        m = re.search(r'^\s*(appendix\s+[a-z0-9]+\b|appendices\b|supplementary\s+material)',
                      page, re.I | re.M)
        if m:
            dropped_at = page[m.start():m.start() + 90].splitlines()[0].strip()[:70]
            pages = pages[:i] + [page[:m.start()]]
            break

    kept, n_biblio = [], 0
    for page in pages:
        if is_biblio_page(page):
            n_biblio += 1
            if dropped_at is None:
                dropped_at = 'citation-dense page'
            continue
        # An acknowledgements or references heading inside an otherwise normal
        # page ends that page, and nothing more.
        m = re.search(r'^\s*(references|bibliography|acknowledge?ments?|works\s+cited)'
                      r'(?=\s*$|[A-Z\[])', page, re.I | re.M)
        if m:
            if dropped_at is None:
                dropped_at = page[m.start():m.start() + 60].splitlines()[0].strip()
            page = page[:m.start()]
        kept.append(page)
    return kept, dropped_at, n_biblio


def drop_entry_lines(text):
    """Remove numbered reference entries that survived because the paper's
    bibliography heading did not make it through extraction."""
    keep, dropped = [], 0
    for ln in text.splitlines():
        if ENTRY_RE.match(ln) and BIBLIO_RE.search(ln):
            dropped += 1
            continue
        keep.append(ln)
    return '\n'.join(keep), dropped


def to_markdown(text):
    """Light structure only: numbered section headings become real headings,
    hyphenation across a line break is rejoined, runs of blanks collapse."""
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    out = []
    for ln in text.splitlines():
        s = ln.rstrip()
        m = SUBSECTION_RE.match(s.strip())
        if m:
            out.append('### %s %s' % (m.group(1), m.group(2)))
            continue
        m = SECTION_RE.match(s.strip())
        if m:
            out.append('## %s. %s' % (m.group(1), m.group(2)))
            continue
        out.append(s)
    text = '\n'.join(out)
    return re.sub(r'\n{3,}', '\n\n', text).strip()


def build(arxiv_id, force=False):
    pdf = find_pdf(arxiv_id)
    if pdf is None:
        print('  %s: no PDF under output/*/ , skipped' % arxiv_id)
        return False
    dst = pdf.parent / ('%s_%s.md' % (pdf.parent.name, arxiv_id))
    if dst.exists() and not force:
        print('  %s: already built, use --force to rebuild' % arxiv_id)
        return False

    raw, n_pages = pdftext.extract(str(pdf))
    if not raw.strip():
        print('  %s: extractor returned nothing, PDF may be image-only' % arxiv_id)
        return False

    marks = list(PAGE_RE.finditer(raw))
    pages = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(raw)
        pages.append(raw[m.end():end])
    if not pages:
        pages = [raw]

    pages = strip_running_lines(pages)
    pages, dropped_at, n_biblio = cut_pages(pages)
    body, n_entries = drop_entry_lines('\n'.join(pages))
    md = to_markdown(body)

    fm = [
        '---',
        'arxiv_id: "%s"' % arxiv_id,
        'source_pdf: %s' % pdf.relative_to(ROOT).as_posix(),
        'extracted: %s' % dt.date.today().isoformat(),
        'pages_in_pdf: %d' % n_pages,
        'dropped_from: %s' % ('"%s"' % dropped_at if dropped_at else 'null'),
        'biblio_pages_removed: %d' % n_biblio,
        'reference_lines_removed: %d' % n_entries,
        'note: "Body text only. References, acknowledgements and appendices removed."',
        '---',
        '',
    ]
    dst.write_text('\n'.join(fm) + md + '\n', encoding='utf-8')
    detail = ', cut at %r' % dropped_at if dropped_at else ', NO terminal heading'
    if n_biblio:
        detail += ', %d biblio page(s)' % n_biblio
    if n_entries:
        detail += ', %d entry lines' % n_entries
    print('  %s: %d pages -> %s (%d chars)%s' % (
        arxiv_id, n_pages, dst.relative_to(ROOT), len(md), detail))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('arxiv_ids', nargs='*')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--force', action='store_true')
    args = ap.parse_args()

    ids = list(args.arxiv_ids)
    if args.all:
        # filename is <year-week>_<arxiv_id>.pdf; strip the week+underscore prefix
        ids = sorted({p.stem[len(p.parent.name) + 1:] for p in OUTPUT_DIR.glob('*/*.pdf')})
    if not ids:
        ap.error('give an arxiv_id or --all')

    print('building full text for %d paper(s)' % len(ids))
    n, failed = 0, []
    for i in ids:
        # One malformed PDF must not abort a batch of nine.
        try:
            if build(i, args.force):
                n += 1
        except Exception as exc:
            failed.append(i)
            print('  %s: FAILED, %s: %s' % (i, type(exc).__name__, exc))
    print('wrote %d file(s) to %s' % (n, OUTPUT_DIR.relative_to(ROOT)))
    if failed:
        print('%d failed: %s' % (len(failed), ', '.join(failed)))
    return 0


if __name__ == '__main__':
    sys.exit(main())

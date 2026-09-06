#!/usr/bin/env python3
"""Minimal dependency-free PDF text extractor.

Enough for arXiv/pdfTeX output: scans every object, inflates FlateDecode
streams, walks BT/ET text blocks in content streams, and decodes strings
through the font's ToUnicode CMap when one exists (Type1 subsets otherwise
come out near-ASCII already).

Usage: python pdftext.py <file.pdf> [start_page] [end_page]
"""
import re
import sys
import zlib

NUM = r"[-+]?[0-9]*\.?[0-9]+"


def inflate(data):
    try:
        return zlib.decompress(data)
    except zlib.error:
        for i in range(1, 12):
            try:
                return zlib.decompressobj().decompress(data[i:])
            except zlib.error:
                continue
    return b""


def objects(raw):
    """Yield (objnum, dict_bytes, stream_bytes|None) for every `N 0 obj`."""
    out = {}
    for m in re.finditer(rb"(\d+)\s+(\d+)\s+obj\b", raw):
        num = int(m.group(1))
        start = m.end()
        end = raw.find(b"endobj", start)
        if end < 0:
            continue
        body = raw[start:end]
        sm = re.search(rb"stream\r?\n", body)
        if sm:
            dic = body[: sm.start()]
            stream = body[sm.end():]
            stream = re.sub(rb"\s*endstream\s*$", b"", stream)
        else:
            dic, stream = body, None
        out[num] = (dic, stream)
    return out


def expand_objstm(objs):
    """Objects inside /ObjStm compressed streams (PDF 1.5+)."""
    extra = {}
    for num, (dic, stream) in list(objs.items()):
        if b"/ObjStm" not in dic or stream is None:
            continue
        data = inflate(stream) if b"/FlateDecode" in dic else stream
        n = re.search(rb"/N\s+(\d+)", dic)
        first = re.search(rb"/First\s+(\d+)", dic)
        if not (n and first and data):
            continue
        n, first = int(n.group(1)), int(first.group(1))
        header = data[:first].split()
        for i in range(n):
            try:
                onum = int(header[2 * i])
                off = int(header[2 * i + 1])
            except (IndexError, ValueError):
                break
            nxt = int(header[2 * i + 3]) + first if 2 * i + 3 < len(header) else len(data)
            extra[onum] = (data[first + off:nxt], None)
    objs.update(extra)
    return objs


def tounicode_maps(objs):
    """objnum -> {code: char} for every ToUnicode CMap in the file."""
    maps = {}
    for num, (dic, stream) in objs.items():
        if stream is None or b"beginbfchar" not in (stream[:20] + b""):
            pass
        data = inflate(stream) if (stream and b"/FlateDecode" in dic) else (stream or b"")
        if b"beginbfchar" not in data and b"beginbfrange" not in data:
            continue
        cmap = {}
        for blk in re.findall(rb"beginbfchar(.*?)endbfchar", data, re.S):
            for src, dst in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
                cmap[int(src, 16)] = hexstr(dst)
        for blk in re.findall(rb"beginbfrange(.*?)endbfrange", data, re.S):
            for lo, hi, dst in re.findall(
                rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk
            ):
                lo, hi, base = int(lo, 16), int(hi, 16), int(dst, 16)
                for k in range(lo, min(hi, lo + 512) + 1):
                    # A malformed or multi-char bfrange destination can exceed
                    # the Unicode range; skip those codes rather than aborting
                    # the whole document.
                    v = base + k - lo
                    if 0 <= v < 0x110000:
                        cmap[k] = chr(v)
        maps[num] = cmap
    return maps


def hexstr(h):
    b = bytes.fromhex(h.decode() if isinstance(h, bytes) else h)
    try:
        return b.decode("utf-16-be")
    except UnicodeDecodeError:
        return b.decode("latin-1")


def unescape(s):
    out, i = bytearray(), 0
    esc = {b"n": 10, b"r": 13, b"t": 9, b"b": 8, b"f": 12}
    while i < len(s):
        c = s[i:i + 1]
        if c == b"\\" and i + 1 < len(s):
            nxt = s[i + 1:i + 2]
            if nxt in esc:
                out.append(esc[nxt]); i += 2
            elif nxt.isdigit():
                m = re.match(rb"[0-7]{1,3}", s[i + 1:])
                out.append(int(m.group(0), 8) & 0xFF); i += 1 + m.end()
            else:
                out += nxt; i += 2
        else:
            out += c; i += 1
    return bytes(out)


def split_strings(chunk):
    """Split a (...) literal respecting balanced/escaped parens."""
    res, depth, buf, i = [], 0, bytearray(), 0
    while i < len(chunk):
        c = chunk[i:i + 1]
        if c == b"\\":
            buf += chunk[i:i + 2]; i += 2; continue
        if c == b"(":
            depth += 1
            if depth == 1:
                buf = bytearray(); i += 1; continue
        elif c == b")":
            depth -= 1
            if depth == 0:
                res.append(bytes(buf)); i += 1; continue
        if depth:
            buf += c
        i += 1
    return res


def tj_parts(arr, cmap):
    """Walk a TJ array left to right, turning big negative kerns into spaces."""
    out, i = [], 0
    while i < len(arr):
        c = arr[i:i + 1]
        if c == b"(":
            depth, buf = 1, bytearray()
            i += 1
            while i < len(arr) and depth:
                ch = arr[i:i + 1]
                if ch == b"\\":
                    buf += arr[i:i + 2]; i += 2; continue
                if ch == b"(":
                    depth += 1
                elif ch == b")":
                    depth -= 1
                    if not depth:
                        i += 1; break
                buf += ch; i += 1
            out.append(decode(unescape(bytes(buf)), cmap))
            continue
        m = re.match(NUM.encode(), arr[i:])
        if m:
            if float(m.group(0)) <= -120 and out and not out[-1].endswith(" "):
                out.append(" ")
            i += m.end()
            continue
        i += 1
    return "".join(out)


# Bold weight indicated in a font's BaseFont name. Covers the base-14 fonts
# (Times-Bold, Helvetica-Bold), LaTeX's Computer/Latin Modern bold families
# (CMBX*, CMBSY*), and the Nimbus substitutes pdfTeX emits for mathptmx/Times
# (NimbusRomNo9L-Medi, -MediItal), which is what arXiv PDFs commonly use for
# section headings and emphasised topic sentences.
BOLD_RE = re.compile(r"bold|black|semibold|heavy|-medi(?:ital)?$|cmbx|cmbsy", re.I)


def is_bold_font(basefont_name):
    return bool(BOLD_RE.search(basefont_name))


def flush_run(cur):
    """Join (text, is_bold) pieces into one string, wrapping contiguous bold
    runs in markdown emphasis so a paper's own bolded topic sentences survive
    extraction instead of flattening into plain prose. Whitespace at a run's
    edges stays outside the ** markers so spacing between words is untouched."""
    out, run_text, run_bold = [], "", None
    for text, bold in cur:
        if not text:
            continue
        if run_bold is None or bold == run_bold:
            run_text += text
        else:
            out.append(_wrap_bold(run_text, run_bold))
            run_text = text
        run_bold = bold
    if run_text:
        out.append(_wrap_bold(run_text, run_bold))
    return "".join(out)


def _wrap_bold(text, bold):
    if not bold or not text.strip():
        return text
    lead = text[:len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]
    return "%s**%s**%s" % (lead, text.strip(), trail)


def page_text(content, fontmaps):
    lines, cur, cmap, bold = [], [], {}, False
    for m in re.finditer(rb"BT(.*?)ET", content, re.S):
        blk = m.group(1)
        for op in re.finditer(
            rb"/([^\s/]+)\s+" + NUM.encode() + rb"\s+Tf"
            rb"|(\((?:\\.|[^\\()]|\((?:\\.|[^\\()])*\))*\))\s*Tj"
            rb"|\[((?:\((?:\\.|[^\\()])*\)|[^\]])*)\]\s*TJ"
            rb"|(" + NUM.encode() + rb")\s+(" + NUM.encode() + rb")\s+Td"
            rb"|T\*",
            blk,
            re.S,
        ):
            if op.group(1) is not None:
                cmap, bold = fontmaps.get(op.group(1).decode("latin-1"), ({}, False))
            elif op.group(2) is not None:
                cur.append((decode(unescape(op.group(2)[1:-1]), cmap), bold))
            elif op.group(3) is not None:
                cur.append((tj_parts(op.group(3), cmap), bold))
            elif op.group(4) is not None:
                if float(op.group(5)) != 0:
                    lines.append(flush_run(cur)); cur = []
            else:
                lines.append(flush_run(cur)); cur = []
        lines.append(flush_run(cur)); cur = []
    return "\n".join(l for l in lines if l.strip())


# TeX OT1/T1 ligature slots, used when a font ships no ToUnicode for them
TEX_SLOTS = {0x0B: "ff", 0x0C: "fi", 0x0D: "fl", 0x0E: "ffi", 0x0F: "ffl",
             0x16: "", 0x19: "ss", 0x1B: "ae", 0x1C: "oe"}


def decode(b, cmap):
    if cmap:
        wide = any(k > 0xFF for k in cmap)
        if wide:
            out = [cmap.get((b[i] << 8) | b[i + 1], "") for i in range(0, len(b) - 1, 2)]
            if "".join(out).strip():
                return "".join(out)
        else:
            out, hits = [], 0
            for c in b:
                if c in cmap:
                    out.append(cmap[c]); hits += 1
                else:
                    out.append(TEX_SLOTS.get(c, chr(c) if c >= 0x20 else ""))
            if hits >= len(b) * 0.6:
                return "".join(out)
    return "".join(TEX_SLOTS.get(c, chr(c) if c >= 0x20 else "") for c in b)


LIG = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl",
       "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-",
       "—": "--", " ": " ", "�": ""}


def extract(path, first=1, last=10**6):
    raw = open(path, "rb").read()
    objs = expand_objstm(objects(raw))
    maps = tounicode_maps(objs)
    # page objects, in file order
    pages = [(n, d) for n, (d, s) in objs.items() if re.search(rb"/Type\s*/Page[^s]", d)]
    pages.sort()
    chunks = []
    for idx, (num, dic) in enumerate(pages, 1):
        if idx < first or idx > last:
            continue
        # resource name -> that font's ToUnicode CMap
        res = re.search(rb"/Resources\s+(\d+)\s+0\s+R", dic)
        resdic = objs.get(int(res.group(1)), (b"", None))[0] if res else dic
        fontblk = re.search(rb"/Font\s*<<(.*?)>>", resdic, re.S)
        if not fontblk:
            fr = re.search(rb"/Font\s+(\d+)\s+0\s+R", resdic)
            src = objs.get(int(fr.group(1)), (b"", None))[0] if fr else b""
            fontblk = re.search(rb"<<(.*?)>>", src, re.S)
        fontmaps = {}
        if fontblk:
            for name, fnum in re.findall(rb"/([^\s/]+)\s+(\d+)\s+0\s+R", fontblk.group(1)):
                fd = objs.get(int(fnum), (b"", None))[0]
                cmap = {}
                tu = re.search(rb"/ToUnicode\s+(\d+)\s+0\s+R", fd)
                if tu and int(tu.group(1)) in maps:
                    cmap = maps[int(tu.group(1))]
                bf = re.search(rb"/BaseFont\s*/([^\s/>]+)", fd)
                basefont = bf.group(1).decode("latin-1", "replace") if bf else ""
                # Every font resource gets an entry, even with no ToUnicode map,
                # so boldness is tracked whether or not this font's text also
                # decodes through a CMap.
                fontmaps[name.decode("latin-1")] = (cmap, is_bold_font(basefont))
        body = b""
        for cnum in re.findall(rb"/Contents\s+(?:(\d+)\s+0\s+R|\[([^\]]*)\])", dic):
            refs = [cnum[0]] if cnum[0] else re.findall(rb"(\d+)\s+0\s+R", cnum[1])
            for r in refs:
                cd, cs = objs.get(int(r), (b"", None))
                if cs is None:
                    continue
                body += inflate(cs) if b"/FlateDecode" in cd else cs
        if not body:
            continue
        txt = page_text(body, fontmaps)
        for k, v in LIG.items():
            txt = txt.replace(k, v)
        chunks.append(f"\n=== page {idx} ===\n{txt}")
    return "".join(chunks), len(pages)


if __name__ == "__main__":
    path = sys.argv[1]
    a = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    b = int(sys.argv[3]) if len(sys.argv) > 3 else 10**6
    text, n = extract(path, a, b)
    print(f"[{n} pages total]")
    print(text)

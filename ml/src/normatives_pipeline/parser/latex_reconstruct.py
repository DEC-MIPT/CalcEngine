"""Детерминированная реконструкция LaTeX формулы из текстового слоя PDF.

Для PDF с текстовым слоем формулы собираются из геометрии символов ``pdfplumber``
(размер шрифта → ``_{...}``/``^{...}``, базовая линия, таблица Adobe Symbol PUA),
без OCR и без нейросетей. Кириллица берётся из PDF как есть — OCR-головки её не портят.

Используется как основной путь для текстовых PDF; для сканов остаётся pix2text
(``formulas.detect``). Выбор пути делает ``formulas.source`` по классификации
``parser.text_layer.classify``.
"""

from __future__ import annotations

import re
import unicodedata

import pdfplumber

from .symbols import CYR, GREEK

# Adobe Symbol font, PUA 0xF0xx (детерминированная таблица кодировки шрифта, не под СП).
_SYMBOL_PUA = {
    0xF0A3: "\\leq ",
    0xF0B3: "\\geq ",
    0xF0B4: "\\times ",
    0xF0B9: "\\neq ",
    0xF0BB: "\\approx ",
    0xF0D6: "\\sqrt ",
    0xF0D7: "\\cdot ",
    0xF0B1: "\\pm ",
    0xF0A2: "\\prime ",
    0xF0B0: "^{\\circ}",
    0xF0A5: "\\infty ",
    0xF0E5: "\\sum ",
    0xF0D5: "\\prod ",
    0xF0F2: "\\int ",
    0xF0CE: "\\in ",
    0xF0CC: "\\subset ",
    0xF0CD: "\\subseteq ",
    0xF0AE: "\\to ",
    0xF0AC: "\\leftarrow ",
    0xF0C8: "\\cup ",
    0xF0C7: "\\cap ",
}
_SYMBOL_DROP = set(range(0xF0E6, 0xF100))
_SYMBOL_GREEK = {
    0xF061: "\\alpha", 0xF062: "\\beta", 0xF063: "\\chi", 0xF064: "\\delta",
    0xF065: "\\epsilon", 0xF066: "\\phi", 0xF067: "\\gamma", 0xF068: "\\eta",
    0xF069: "\\iota", 0xF06B: "\\kappa", 0xF06C: "\\lambda", 0xF06D: "\\mu",
    0xF06E: "\\nu", 0xF06F: "o", 0xF070: "\\pi", 0xF071: "\\theta",
    0xF072: "\\rho", 0xF073: "\\sigma", 0xF074: "\\tau", 0xF075: "\\upsilon",
    0xF076: "\\omega", 0xF077: "\\omega", 0xF078: "\\xi", 0xF079: "\\psi",
    0xF07A: "\\zeta", 0xF044: "\\Delta", 0xF046: "\\Phi", 0xF047: "\\Gamma",
    0xF04C: "\\Lambda", 0xF050: "\\Pi", 0xF051: "\\Theta", 0xF053: "\\Sigma",
    0xF055: "\\Upsilon", 0xF057: "\\Omega", 0xF059: "\\Psi",
    0xF06A: "\\phi",
}
_SYMBOL_LATIN = {
    0xF041: "A", 0xF042: "B", 0xF043: "X", 0xF045: "E", 0xF048: "H",
    0xF049: "I", 0xF04B: "K", 0xF04D: "M", 0xF04E: "N", 0xF04F: "O",
    0xF052: "P", 0xF054: "T", 0xF05A: "Z",
}
_SCRIPT_RATIO = 0.85


def base_char(ch: str) -> str:
    code = ord(ch)
    if code == 0x00B4:
        return "^{\\prime}"
    if code in _SYMBOL_PUA:
        return _SYMBOL_PUA[code]
    if code in _SYMBOL_GREEK:
        return _SYMBOL_GREEK[code]
    if code in _SYMBOL_LATIN:
        return _SYMBOL_LATIN[code]
    if code in _SYMBOL_DROP:
        return ""
    normalized = unicodedata.normalize("NFKC", ch)
    return GREEK.get(normalized, normalized)


def transliterate(text: str) -> str:
    out: list[str] = []
    for ch in text:
        low = ch.lower()
        if low in CYR:
            translit = CYR[low]
            out.append(translit[:1].upper() + translit[1:] if ch.isupper() else translit)
        else:
            out.append(ch)
    return "".join(out)


_REL = {"=", "≥", "≤", "≠", "<", ">", "≈", "\uf0b3", "\uf0a3", "\uf0b9", "\uf0bb"}
_SUM_GLYPHS = {"\uf0e5", "∑", "Σ"}
_BIG_TOKENS = set("()[]{}|") | _SUM_GLYPHS


def _cluster(chars: list[dict], tol: float = 2.0) -> list[dict]:
    lines: list[dict] = []
    for c in sorted(chars, key=lambda c: c["top"]):
        for line in lines:
            if abs(line["top"] - c["top"]) <= tol:
                line["chars"].append(c)
                break
        else:
            lines.append({"top": c["top"], "chars": [c]})
    return lines


_LETTER_RE = re.compile(r"[A-Za-zА-Яа-яЁё]")


def _char_at(row: list[dict], idx: int) -> dict | None:
    acc = 0
    for c in row:
        if acc == idx:
            return c
        acc += len(c["text"])
    return None


def _marker(chars: list[dict], number: str) -> tuple[float, float] | None:
    target = f"({number})"
    groups: list[list[tuple[float, float]]] = [[], [], [], []]
    for line in _cluster(chars, tol=1.5):
        row = sorted(line["chars"], key=lambda c: c["x0"])
        text = "".join(c["text"] for c in row)
        idx = text.find(target)
        if idx < 0:
            continue
        c = _char_at(row, idx)
        if c is None:
            continue
        is_end = not _LETTER_RE.search(text[idx + len(target):])
        is_prose = _looks_like_prose(line)
        hit = (c["top"], c["x0"])
        groups[0 if (is_end and not is_prose) else 1 if not is_prose else 2 if is_end else 3].append(hit)
    for group in groups[:2]:
        if group:
            return max(group, key=lambda t: t[1])
    return None


def _base_size(chars: list[dict]) -> float:
    sizes = [
        c["size"]
        for c in chars
        if c["size"] > 0
        and c["text"] not in _BIG_TOKENS
        and not any(0xF0E6 <= ord(ch) <= 0xF0FF for ch in c["text"])
    ]
    if not sizes:
        sizes = [c["size"] for c in chars if c["size"] > 0]
    return max(sizes, default=0.0)


def _assemble(chars: list[dict]) -> str:
    keep = sorted((c for c in chars if c["text"].strip()), key=lambda c: c["x0"])
    if not keep:
        return ""
    base_size = _base_size(keep)
    top = min(
        (c["top"] for c in keep if c["size"] >= 0.9 * base_size), default=keep[0]["top"]
    )
    tokens: list[tuple[str, str]] = []
    for c in keep:
        if c["size"] / base_size <= _SCRIPT_RATIO:
            kind = "sub" if c["top"] >= top + 1 else "sup"
        else:
            kind = "base"
        frag = base_char(c["text"])
        if tokens and tokens[-1][0] == kind:
            tokens[-1] = (kind, tokens[-1][1] + frag)
        else:
            tokens.append((kind, frag))
    return "".join(
        ("_{" + t + "}" if k == "sub" else "^{" + t + "}" if k == "sup" else t)
        for k, t in tokens
    )


def _bars(page, y0: float, y1: float, x0: float, x1: float) -> list[dict]:
    out = []
    for seg in list(page.rects) + list(page.lines):
        if seg["height"] <= 2 and seg["width"] >= 6:
            center_y = seg["top"] + seg["height"] / 2
            if y0 <= center_y <= y1 and x0 <= seg["x0"] and seg["x1"] <= x1 + 2:
                out.append(seg)
    return out


def _slashes(page, y0: float, y1: float, x0: float, x1: float) -> list[dict]:
    out = []
    for seg in list(page.rects) + list(page.lines):
        w, h = seg["width"], seg["height"]
        if w <= 0 or not (2 <= w <= 12 and 6 <= h <= 25):
            continue
        if not (0.15 <= w / h <= 0.9):
            continue
        if y0 <= seg["top"] <= y1 and x0 <= seg["x0"] <= x1:
            out.append(seg)
    return out


def _radicals(page, band: list[dict], bars: list[dict]) -> list[dict]:
    segs = list(page.rects) + list(page.lines)
    out = []
    for bar in bars:
        strokes = [
            s
            for s in segs
            if s["width"] <= 8
            and s["x1"] <= bar["x0"] + 1.5
            and s["x0"] >= bar["x0"] - 8
            and s["bottom"] >= bar["top"] - 2
            and s["top"] <= bar["bottom"] + 20
        ]
        if not strokes:
            continue
        lo, hi = bar["x0"] - 1, bar["x1"] + 1

        def inside(c: dict, lo: float = lo, hi: float = hi) -> bool:
            return lo <= (c["x0"] + c["x1"]) / 2 <= hi

        below = [c for c in band if inside(c) and bar["top"] - 1 <= c["top"] <= bar["top"] + 16]
        above = [
            c
            for c in band
            if inside(c) and bar["top"] - 12 <= c["bottom"] <= bar["top"] - 0.5
        ]
        if below and not above:
            latex = "\\sqrt{" + _assemble(sorted(below, key=lambda c: c["x0"])) + "}"
            used = {id(bar)} | {id(s) for s in strokes} | {id(c) for c in below}
            out.append(
                {"bar": bar, "strokes": strokes,
                 "x": min(s["x0"] for s in strokes), "y": min(s["top"] for s in strokes),
                 "latex": latex, "used": used}
            )
    return out


def _frac(chars: list[dict], bar: dict) -> tuple[float, str, set[int]] | None:
    lo, hi = bar["x0"] - 1, bar["x1"] + 1
    bar_bottom = bar["top"] + bar["height"]

    def inside(c: dict) -> bool:
        return lo <= (c["x0"] + c["x1"]) / 2 <= hi

    num = [
        c
        for c in chars
        if inside(c) and bar["top"] - 12 <= c["bottom"] <= bar["top"] + 0.5
    ]
    den = [
        c
        for c in chars
        if inside(c) and bar_bottom - 0.5 <= c["top"] <= bar_bottom + 12
    ]
    if not num or not den:
        return None
    consumed = {id(c) for c in num + den}
    latex = "\\frac{" + _assemble(num) + "}{" + _assemble(den) + "}"
    return bar["x0"], latex, consumed


def _has_rel(chars: list[dict]) -> bool:
    return any(c["text"] in _REL for c in chars)


def _sum_groups(
    band: list[dict], consumed: set[int]
) -> list[tuple[float, float, str, set[int]]]:
    base_size = _base_size(band)
    out: list[tuple[float, float, str, set[int]]] = []
    for s in band:
        if s["text"] not in _SUM_GLYPHS or id(s) in consumed:
            continue
        lo, hi = s["x0"] - 1.5, s["x1"] + 1.5

        def small(c: dict, s: dict = s, lo: float = lo, hi: float = hi) -> bool:
            ctr = (c["x0"] + c["x1"]) / 2
            return (
                id(c) != id(s)
                and id(c) not in consumed
                and lo <= ctr <= hi
                and c["size"] < 0.8 * base_size
            )
        sup = [
            c
            for c in band
            if small(c) and s["top"] - 12 <= c["top"] and c["bottom"] <= s["top"] + 1.5
        ]
        sub = [
            c
            for c in band
            if small(c) and s["bottom"] - 1.5 <= c["top"] <= s["bottom"] + 12
        ]
        latex = "\\sum"
        if sub:
            latex += "_{" + _assemble(sorted(sub, key=lambda c: c["x0"])) + "}"
        if sup:
            latex += "^{" + _assemble(sorted(sup, key=lambda c: c["x0"])) + "}"
        used = {id(s)} | {id(c) for c in sup + sub}
        out.append((s["x0"], s["top"], latex, used))
    return out


def _has_brace(chars: list[dict]) -> bool:
    for c in chars:
        if c["text"] in "{}" or any(0xF0E6 <= ord(ch) <= 0xF0FF for ch in c["text"]):
            return True
    return False


_CYR_RE = re.compile(r"[а-яё]", re.IGNORECASE)


def _looks_like_prose(line: dict, run: int = 4) -> bool:
    base_size = max((c["size"] for c in line["chars"]), default=0.0)
    streak = 0
    for c in sorted(line["chars"], key=lambda c: c["x0"]):
        if base_size and c["size"] < 0.9 * base_size:
            streak = 0
            continue
        if _CYR_RE.fullmatch(c["text"]):
            streak += 1
            if streak >= run:
                return True
        else:
            streak = 0
    return False


def _line_latex(line: dict, rest: list[dict], fraction: list[tuple[float, float, str]]) -> str:
    inner = line["chars"]
    left = min(c["x0"] for c in inner)
    near = [(x, latex) for x, y, latex in fraction if line["top"] - 5 <= y <= line["top"] + 14]
    right = max([max(c["x1"] for c in inner)] + [x for x, _ in near])
    seg = sorted(
        (
            c
            for c in rest
            if line["top"] - 5 <= c["top"] <= line["top"] + 14
            and left - 1 <= c["x0"] <= right + 3
        ),
        key=lambda c: c["x0"],
    )
    inserted = sorted((x, latex) for x, latex in near if left - 1 <= x <= right + 3)
    rel = [c["size"] for c in line["chars"] if c["text"] in _REL and c["size"] > 0]
    base_size = max(rel) if rel else _base_size(line["chars"])
    is_prose = [
        c["size"] >= 0.9 * base_size and bool(_CYR_RE.fullmatch(c["text"])) for c in seg
    ]
    lead = 0
    while lead < len(seg) and is_prose[lead]:
        lead += 1
    if lead >= 3:
        seg, is_prose = seg[lead:], is_prose[lead:]
    run = 0
    cut_x = None
    for j, p in enumerate(is_prose):
        run = run + 1 if p else 0
        if run >= 3:
            seg = seg[: j - run + 1]
            cut_x = seg[-1]["x1"] if seg else None
            break
    if cut_x is not None:
        inserted = [t for t in inserted if t[0] <= cut_x + 3]
    tokens: list[tuple[str, str]] = []
    fi = 0
    for c in seg:
        while fi < len(inserted) and inserted[fi][0] <= c["x0"]:
            tokens.append(("frac", inserted[fi][1]))
            fi += 1
        if base_size and c["size"] > base_size * 1.15:
            continue
        if base_size and c["size"] / base_size <= _SCRIPT_RATIO:
            kind = "sub" if c["top"] >= line["top"] + 1 else "sup"
        else:
            kind = "base"
        frag = base_char(c["text"])
        if tokens and tokens[-1][0] == kind:
            tokens[-1] = (kind, tokens[-1][1] + frag)
        else:
            tokens.append((kind, frag))
    while fi < len(inserted):
        tokens.append(("frac", inserted[fi][1]))
        fi += 1
    frags = [
        "_{" + t + "}" if k == "sub" else "^{" + t + "}" if k == "sup" else t
        for k, t in tokens
    ]
    for i, frag in enumerate(frags):
        if frag.startswith("\\sum") and i + 1 < len(frags):
            frags = frags[: i + 1] + ["{" + "".join(frags[i + 1:]) + "}"]
            break
    return "".join(frags)


def reconstruct_latex(page, number: str) -> str | None:
    """Собирает LaTeX формулы ``(number)`` со страницы по геометрии символов."""
    chars = page.chars
    marker = _marker(chars, number)
    if marker is None:
        return None
    top, marker_x = marker
    bars = _bars(page, top - 25, top + 25, 60, marker_x - 2)
    y_lo = min([top - 25] + [b["top"] - 14 for b in bars])
    y_hi = max([top + 25] + [b["bottom"] + 14 for b in bars])
    band = [
        c
        for c in chars
        if c["text"].strip()
        and y_lo <= c["top"] <= y_hi
        and c["x0"] < marker_x - 2
        and c["x0"] > 60
        and c["size"] > 0
    ]
    if not band:
        return None
    prose_ids = {
        id(c) for ln in _cluster(band) if _looks_like_prose(ln) for c in ln["chars"]
    }
    band = [c for c in band if id(c) not in prose_ids]
    if not band:
        return None

    fraction: list[tuple[float, float, str]] = []
    consumed: set[int] = set()
    radicals = _radicals(page, band, bars)
    rad_bars = {id(r["bar"]) for r in radicals}
    rad_diags = {id(s) for r in radicals for s in r["strokes"]}
    for sl in _slashes(page, y_lo, y_hi, 60, marker_x - 2):
        if id(sl) in rad_diags:
            continue
        fraction.append((sl["x0"], sl["top"], "/"))
    for bar in bars:
        if id(bar) in rad_bars:
            continue
        result = _frac(band, bar)
        if result is None:
            continue
        x, latex, used = result
        fraction.append((x, bar["top"], latex))
        consumed |= used
    for r in radicals:
        fraction.append((r["x"], r["y"], r["latex"]))
        consumed |= r["used"]
    for x, y, latex, used in _sum_groups(band, consumed):
        fraction.append((x, y, latex))
        consumed |= used
    rest = [c for c in band if id(c) not in consumed]

    lines = _cluster(rest)
    if not lines:
        return None
    marker_i = min(range(len(lines)), key=lambda i: abs(lines[i]["top"] - top))
    block = [marker_i]
    i = marker_i - 1
    while i >= 0 and lines[i + 1]["top"] - lines[i]["top"] <= 22:
        block.append(i)
        i -= 1
    i = marker_i + 1
    while i < len(lines) and lines[i]["top"] - lines[i - 1]["top"] <= 22:
        block.append(i)
        i += 1
    block.sort()
    marker_base = _base_size(lines[marker_i]["chars"]) or _base_size(rest)
    math_lines = [
        lines[i]
        for i in block
        if any(c["size"] >= 0.9 * marker_base for c in lines[i]["chars"])
    ]
    if not math_lines:
        return None

    parts = [p for p in (_line_latex(ln, rest, fraction) for ln in math_lines) if p]
    if not parts:
        return None
    if _has_brace(band) and len(parts) > 1:
        body = "\\\\".join(parts)
        return "\\left.\\begin{aligned}" + body + "\\end{aligned}\\right\\}"
    body = " ".join(parts)
    body = re.sub(r"[,;]+\}\s*$", "}", body)
    return body.rstrip(" ,;.")


def reconstruct_document(path) -> dict[int, dict[str, str]]:
    """Все формулы документа: ``{page_no: {number: latex}}`` (открывает PDF один раз)."""
    out: dict[int, dict[str, str]] = {}
    with pdfplumber.open(str(path)) as doc:
        for page_no, page in enumerate(doc.pages, start=1):
            raw = "".join(c["text"] for c in page.chars)
            for number in sorted(set(re.findall(r"\((\d{1,2}(?:\.\d+)?)\)", raw))):
                latex = reconstruct_latex(page, number)
                if latex:
                    out.setdefault(page_no, {})[number] = latex
    return out

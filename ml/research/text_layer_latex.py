"""Детерминированная реконструкция LaTeX формулы из текстового слоя PDF.

Research-прототип (не в основном пайплайне). Решает главный блокер pix2text —
кириллические индексы: нейросетевой OCR читает ``h_зар`` как ``h_3arrom``, а текстовый
слой PDF хранит кириллицу корректно. Здесь подстрочные/надстрочные символы определяются
по геометрии (pdfplumber: размер шрифта и базовая линия), математические символы — по
NFKC и таблице Symbol-шрифта, а кириллица транслитерируется в латиницу только для парсинга
``latex2sympy2``. Никаких моделей/LLM — чистые библиотеки.

CLI::

    python -m research.text_layer_latex "../docs/normative-base/СП 31.13330.2021.pdf"

Результат на СП 31.13330.2021: 8/13 формул парсятся (pix2text — 10/21 = 48%); все
формулы с кириллическими индексами (7, 9, 10 и надстрочные 2, 3) парсятся, чего
pix2text не мог. Остаточные отказы — не про алфавит: дробь с горизонтальной чертой,
химия ``Fe^{2+}``, многоколоночная вёрстка.
"""

from __future__ import annotations

import argparse
import re
import unicodedata
from itertools import product
from pathlib import Path

import pdfplumber

from normatives_pipeline.formulas.validation import latex2sympy
from normatives_pipeline.parser.symbols import CYR, GREEK

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
# Растянутые скобки/рамки Symbol (0xF0E6..0xF0FF) — декоративные разделители, убираем.
# 0xF0F2 (∫) остаётся: _SYMBOL_PUA проверяется раньше.
_SYMBOL_DROP = set(range(0xF0E6, 0xF100))
# Буквы Adobe Symbol в PUA: 0xF000 + код Symbol (табличная кодировка шрифта, не под СП).
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
# Заглавные буквы Adobe Symbol в PUA, чей глиф совпадает с латинской заглавной
# (Iota→I, Rho→P): в формулах СП это «II», «I» и т.п. Табличная кодировка шрифта.
_SYMBOL_LATIN = {
    0xF041: "A", 0xF042: "B", 0xF043: "X", 0xF045: "E", 0xF048: "H",
    0xF049: "I", 0xF04B: "K", 0xF04D: "M", 0xF04E: "N", 0xF04F: "O",
    0xF052: "P", 0xF054: "T", 0xF05A: "Z",
}
_SCRIPT_RATIO = 0.85


def base_char(ch: str) -> str:
    """Один символ текстового слоя → фрагмент LaTeX (NFKC, греческий, Symbol PUA)."""
    code = ord(ch)
    if code == 0x00B4:
        # U+00B4 (spacing acute) — в СП это штрих у величины (`b´`); NFKC превратил бы
        # его в пробел+комбинирующий акут, поэтому обрабатываем до NFKC.
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
    """Кириллица → латиница (``cyr_map``) для sympy-идентификаторов."""
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

# N-ary суммирование: PUA Symbol 0xF0E5 + литеральные ∑/Σ.
_SUM_GLYPHS = {"\uf0e5", "∑", "Σ"}
# Крупные разделители/операторы: их размер завышен относительно переменных.
_BIG_TOKENS = set("()[]{}|") | _SUM_GLYPHS


def _cluster(chars: list[dict], tol: float = 2.0) -> list[dict]:
    """Группирует символы в строки по вертикали (``top``)."""
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
    """Позиция ``(`` из ``(number)`` в строке-номере формулы.

    ``(number)`` встречается на странице раньше самой формулы — как ссылка в прозе
    («вычисляемая по формуле (5.8)»). Номер уравнения стоит **последним** токеном своей
    строки, поэтому предпочитаем вхождения в конце строки и не в прозаической строке.
    """
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
    for group in groups:
        if group:
            return max(group, key=lambda t: t[1])
    return None
    return None


def _base_size(chars: list[dict]) -> float:
    """Размер базовой линии без крупных разделителей/операторов.

    ``(` ``)`` и ``Σ`` в формулах крупнее переменных (18.6 против 11.9 при базе 11.9);
    если брать максимум по всем, переменные ошибочно уезжают в подстрочные.
    """
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
    """Собирает символы одной строки в LaTeX: ``size``/``top`` → base/sub/sup."""
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
    """Горизонтальные отрезки (дробные черты) в окне формулы."""
    out = []
    for seg in list(page.rects) + list(page.lines):
        if seg["height"] <= 2 and seg["width"] >= 6:
            center_y = seg["top"] + seg["height"] / 2
            if y0 <= center_y <= y1 and x0 <= seg["x0"] and seg["x1"] <= x1 + 2:
                out.append(seg)
    return out


def _frac(chars: list[dict], bar: dict) -> tuple[float, str, set[int]] | None:
    """Делит символы на числитель/знаменатель по черте → (x, ``\\frac``, consumed)."""
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
    """Σ-группы ``\\sum_{...}^{...}``: глиф плюс мелкие пределы над/под ним.

    Пределы ``n`` (сверху) и ``i=1`` (снизу) вёрстаны отдельными строками и по центру
    колонки Σ. ``i=1`` содержит ``=`` и без выделения читается как отдельная формула.
    """
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
    """Фигурная скобка системы уравнений (литеральная или PUA Symbol 0xF0E6..0xF0FF)."""
    for c in chars:
        if c["text"] in "{}" or any(0xF0E6 <= ord(ch) <= 0xF0FF for ch in c["text"]):
            return True
    return False


_CYR_RE = re.compile(r"[а-яё]", re.IGNORECASE)


def _looks_like_prose(line: dict, run: int = 4) -> bool:
    """Слой распознавания шума: длинное кириллическое слово базового размера — это текст.

    В формуле кириллица стоит либо одиночной базовой буквой-переменной (``Д``, ``щ``),
    либо в индексе (мелкий размер, другая строка). ``run`` идущих подряд базовых букв —
    признак фразы, попавшей в полосу из-за расширенного окна.
    """
    base_size = max((c["size"] for c in line["chars"]), default=0.0)
    streak = 0
    for c in sorted(line["chars"], key=lambda c: c["x0"]):
        if base_size and c["size"] < 0.9 * base_size:
            streak = 0  # кириллица в индексе (F_{макс}) — не проза
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
    # Атомы (дроби/Σ), вертикально принадлежащие строке, расширяют её правую границу:
    # в «стопке» (5.19) базовая линия `s=β` короче дроби, стоящей справа.
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
    return "".join(
        "_{" + t + "}" if k == "sub" else "^{" + t + "}" if k == "sup" else t
        for k, t in tokens
    )


def reconstruct_latex(page, number: str) -> str | None:
    """Собирает LaTeX формулы ``(number)`` со страницы по геометрии символов."""
    chars = page.chars
    marker = _marker(chars, number)
    if marker is None:
        return None
    top, marker_x = marker
    bars = _bars(page, top - 25, top + 25, 60, marker_x - 2)
    # Пробелы не несут смысла и тянут в полосу соседнюю строку текста, ломая base_size.
    # Базовое окно ±25 накрывает системы из двух строк; запас ±14 вокруг дробных черт
    # удерживает подстрочные знаменателя, сидящие ниже окна (``E_i`` при маркере 183.5).
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

    fraction: list[tuple[float, float, str]] = []
    consumed: set[int] = set()
    for bar in bars:
        result = _frac(band, bar)
        if result is None:
            continue
        x, latex, used = result
        fraction.append((x, bar["top"], latex))
        consumed |= used
    for x, y, latex, used in _sum_groups(band, consumed):
        fraction.append((x, y, latex))
        consumed |= used
    rest = [c for c in band if id(c) not in consumed]

    lines = _cluster(rest)
    math_lines = [
        ln
        for ln in lines
        if _has_rel(ln["chars"]) and not _looks_like_prose(ln)
    ]
    if not math_lines:
        return None

    parts = [p for p in (_line_latex(ln, rest, fraction) for ln in math_lines) if p]
    if not parts:
        return None
    if _has_brace(band) and len(parts) > 1:
        body = "\\\\".join(parts)
        return "\\left.\\begin{aligned}" + body + "\\end{aligned}\\right\\}"
    return "; ".join(parts)


_KNOWN_CMDS = sorted(
    {v.strip() for v in (*GREEK.values(), *_SYMBOL_PUA.values(), *_SYMBOL_GREEK.values()) if v.strip()},
    key=len,
    reverse=True,
)


def _space_commands(s: str) -> str:
    """Вставляет пробел между командой и следующей буквой (``\\etac`` → ``\\eta c``).

    Только настоящие команды (с обратным слэшем): одиночные буквы-значения Symbol
    (например ``o`` = omicron) не команды и иначе рвут ``\\cdot``/``\\epsilon``.
    """
    for cmd in _KNOWN_CMDS:
        if not cmd.startswith("\\"):
            continue
        s = re.sub(re.escape(cmd) + r"(?=[A-Za-z])", lambda m, c=cmd: c + " ", s)
    return s


def _frac_to_div(s: str) -> str:
    """``\\frac{A}{B}`` → ``((A)/(B))``: ``latex2sympy2`` не парсит индексы в \\frac."""
    out: list[str] = []
    i = 0
    while True:
        j = s.find("\\frac", i)
        if j < 0:
            out.append(s[i:])
            break
        out.append(s[i:j])

        def group(k: int) -> tuple[str, int]:
            depth = 0
            m = k
            while m < len(s):
                if s[m] == "{":
                    depth += 1
                elif s[m] == "}":
                    depth -= 1
                    if depth == 0:
                        return s[k + 1 : m], m + 1
                m += 1
            return s[k + 1 :], len(s)

        k1 = j + 5
        if k1 >= len(s) or s[k1] != "{":
            out.append(s[j:k1])
            i = k1
            continue
        g1, n1 = group(k1)
        if n1 >= len(s) or s[n1] != "{":
            out.append(s[j:n1])
            i = n1
            continue
        g2, n2 = group(n1)
        out.append("((" + _frac_to_div(g1) + ")/(" + _frac_to_div(g2) + "))")
        i = n2
    return "".join(out)


def to_parseable(display: str) -> str:
    """Отображаемый LaTeX → строка, парсимая ``latex2sympy2`` (транслит кириллицы)."""
    s = display
    for src, dst in (
        ("−", "-"), ("–", "-"), ("≥", "\\geq "), ("≤", "\\leq "), ("·", "\\cdot "),
        ("⋅", "\\cdot "), ("×", "\\times "), ("≠", "\\neq "), ("∑", "\\sum "),
        ("∏", "\\prod "), ("∫", "\\int "), ("∞", "\\infty "), ("≈", "\\approx "),
        ("′", "\\prime "), ("″", "\\prime \\prime "),
    ):
        s = s.replace(src, dst)
    s = re.sub(r"(\\leq|\\geq|\\neq)\s*=", r"\1", s)
    s = re.sub(r"=(\\leq|\\geq|\\neq)", r"\1", s)
    s = re.sub(r"√([A-Za-z0-9]+(?:_\{[^{}]*\})?)", r"\\sqrt{\1}", s)
    s = re.sub(r"(\d),(\d)", r"\1.\2", s)
    s = re.sub(r"\s+", "", s)
    s = _frac_to_div(s)
    s = _space_commands(s)
    s = re.sub(r"(?<![A-Za-z])ctg(?![A-Za-z])", r"\\cot ", s)
    s = re.sub(r"(?<![A-Za-z])tg(?![A-Za-z])", r"\\tan ", s)
    s = re.sub(
        r"([_^])\{([^{}]*)\}", lambda m: m.group(1) + "{" + m.group(2).replace(".", "") + "}", s
    )
    s = re.sub(r"\\(sum|prod|int)", "", s)
    s = s.strip(" ,;.:")
    return re.sub(r"[а-яёА-ЯЁ]+", lambda m: transliterate(m.group(0)), s)


def split_juxtaposed(s: str) -> str:
    """Соседние голые буквы (вне индексов/команд) → явное ``*``.

    ``latex2sympy2`` падает с ``TypeError`` на триграмме ``dlb`` (и подобных), хотя
    математически это ``d·l·b``. Явное ``*`` (в отличие от ``\\cdot``) парсится.
    """
    out: list[str] = []
    depth = i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if ch == "\\":
            out.append(ch)
            i += 1
            while i < n and s[i].isalpha():
                out.append(s[i])
                i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth = max(0, depth - 1)
        out.append(ch)
        if depth == 0 and ch.isalpha() and i + 1 < n and s[i + 1].isalpha():
            out.append("*")
        i += 1
    return "".join(out)


_ALONE_E = re.compile(r"(?<![A-Za-z\\])E(?![A-Za-z0-9])")


def mathtt_E(s: str) -> str:
    """Голую ``E`` оборачивает в ``\\mathit{E}``: грамматика latex2sympy2 резервирует ``E``.

    Токен ``LETTER_NO_E`` исключает ``E`` (экспонента ``1E10``), поэтому как символ
    (модуль деформации) ``E`` не парсится; ``\\mathit{E}`` даёт ``Symbol('E')``.
    """
    return _ALONE_E.sub(r"\\mathit{E}", s)


_SIGN_RE = re.compile(r"(±|∓|\\pm|\\mp)")


def sign_variants(parseable: str, limit: int = 16) -> list[str]:
    """Разворачивает ``±``/``∓`` в конкретные знаки (все комбинации).

    Формула с ``±`` — это семейство выражений, а не одно. Проверяем каждую ветвь
    отдельно, а не подменяем знак: ``N=N_d/n±M_x y/Σy_i²±…`` даёт 2² ветви.
    """
    tokens = _SIGN_RE.split(parseable)
    positions = [i for i, t in enumerate(tokens) if _SIGN_RE.fullmatch(t)]
    if not positions or 2 ** len(positions) > limit:
        return [parseable]
    out: list[str] = []
    for combo in product("+-", repeat=len(positions)):
        row = list(tokens)
        for i, sign in zip(positions, combo):
            row[i] = sign
        out.append("".join(row))
    return out


_TRAIL_NUM = re.compile(r"\((?:\d+\.\d+|\d+)\)\s*$")
_REF_CUE = re.compile(r"(формул|услови|выражен|зависимост|см\.)", re.IGNORECASE)


def is_prose_reference(line: str) -> bool:
    """Строка-ссылка на формулу в прозе, а не уравнение.

    ``extract_formulas`` считает формулой любую строку, кончающуюся ``(N)``; но так же
    выглядит ссылка «…вычисляют по формуле (9.7)». Отличаем по длинной кириллической фразе
    или служебному слову перед номером.
    """
    if not _TRAIL_NUM.search(line):
        return False
    body = _TRAIL_NUM.sub("", line)
    return len(re.findall(r"[а-яёА-ЯЁ]{3,}", body)) >= 2 or bool(_REF_CUE.search(body))


def _numbers(chars: list[dict]) -> list[str]:
    raw = "".join(c["text"] for c in chars)
    return sorted(
        {m.group(1) for m in re.finditer(r"\((\d{1,2}(?:\.\d+)?)\)", raw)},
        key=lambda n: tuple(int(p) for p in n.split(".")),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    total = parsed = 0
    with pdfplumber.open(args.pdf) as doc:
        for page_no, page in enumerate(doc.pages, start=1):
            for number in _numbers(page.chars):
                display = reconstruct_latex(page, number)
                if not display or len(display) < 4:
                    continue
                if not any(op in display for op in ("=", "≥", "≤", "≠")):
                    continue
                total += 1
                if "\\begin{aligned}" in display:
                    body = display.split("\\begin{aligned}", 1)[1]
                    body = body.split("\\end{aligned}", 1)[0]
                    equations = [e for e in body.split("\\\\") if e.strip()]
                else:
                    equations = [display]
                parseable = " ; ".join(to_parseable(e) for e in equations)
                try:
                    for equation in equations:
                        latex2sympy(to_parseable(equation))
                    status = "OK "
                    parsed += 1
                except Exception:  # noqa: BLE001 — latex2sympy бросает разнородные ошибки
                    status = "ERR"
                print(f"({number}) p{page_no} {status} | {display}  ->  {parseable}")
    print(f"== {parsed}/{total} parsed")


if __name__ == "__main__":
    main()

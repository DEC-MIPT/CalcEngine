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
# Растянутые скобки/рамки Symbol (0xF0E6..0xF0FB) — декоративные разделители, убираем.
_SYMBOL_DROP = set(range(0xF0E6, 0xF0FC))
_SCRIPT_RATIO = 0.85


def base_char(ch: str) -> str:
    """Один символ текстового слоя → фрагмент LaTeX (NFKC, греческий, Symbol PUA)."""
    code = ord(ch)
    if code in _SYMBOL_PUA:
        return _SYMBOL_PUA[code]
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


def _marker(chars: list[dict], number: str) -> tuple[float, float] | None:
    candidates = [c for c in chars if c["text"] == "("]
    seen: set[int] = set()
    for c in sorted(candidates, key=lambda c: c["top"]):
        top = round(c["top"])
        if top in seen:
            continue
        seen.add(top)
        tail = "".join(
            x["text"] for x in chars if abs(x["top"] - top) < 1.5 and x["x0"] >= c["x0"]
        )
        if f"({number})" in tail:
            return c["top"], c["x0"]
    return None


def reconstruct_latex(page, number: str) -> str | None:
    """Собирает LaTeX формулы ``(number)`` со страницы по геометрии символов."""
    chars = page.chars
    marker = _marker(chars, number)
    if marker is None:
        return None
    top, marker_x = marker
    band = [
        c
        for c in chars
        if top - 4 <= c["top"] <= top + 16
        and c["x0"] < marker_x - 2
        and c["x0"] > 60
        and c["size"] > 0
    ]
    if not band:
        return None
    band.sort(key=lambda c: c["x0"])
    base_size = max(c["size"] for c in band)
    tokens: list[tuple[str, str]] = []
    i, n = 0, len(band)
    while i < n:
        c = band[i]
        if not c["text"].strip():
            i += 1
            continue
        if c["size"] / base_size <= _SCRIPT_RATIO:
            kind = "sub" if c["top"] >= top + 1 else "sup"
            run = base_char(c["text"])
            j = i + 1
            while j < n:
                d = band[j]
                if not d["text"].strip():
                    j += 1
                    continue
                if d["size"] / base_size <= _SCRIPT_RATIO:
                    dkind = "sub" if d["top"] >= top + 1 else "sup"
                    if dkind != kind:
                        break
                    run += base_char(d["text"])
                    j += 1
                else:
                    break
            if tokens and tokens[-1][0] == kind:
                tokens[-1] = (kind, tokens[-1][1] + run)
            else:
                tokens.append((kind, run))
            i = j
        else:
            if tokens and tokens[-1][0] == "base":
                tokens[-1] = ("base", tokens[-1][1] + base_char(c["text"]))
            else:
                tokens.append(("base", base_char(c["text"])))
            i += 1
    return "".join(
        ("_{" + t + "}" if k == "sub" else "^{" + t + "}" if k == "sup" else t)
        for k, t in tokens
    )


def to_parseable(display: str) -> str:
    """Отображаемый LaTeX → строка, парсимая ``latex2sympy2`` (транслит кириллицы)."""
    s = display
    for src, dst in (("−", "-"), ("–", "-"), ("≥", "\\geq "), ("≤", "\\leq "), ("·", "\\cdot ")):
        s = s.replace(src, dst)
    s = re.sub(r"√([A-Za-z0-9]+(?:_\{[^{}]*\})?)", r"\\sqrt{\1}", s)
    s = re.sub(r"(\d),(\d)", r"\1.\2", s)
    s = re.sub(r"\s+", "", s)
    s = re.sub(
        r"([_^])\{([^{}]*)\}", lambda m: m.group(1) + "{" + m.group(2).replace(".", "") + "}", s
    )
    s = re.sub(r"\\sum", "", s)
    s = s.strip(" ,;.:")
    return re.sub(r"[а-яёА-ЯЁ]+", lambda m: transliterate(m.group(0)), s)


def _numbers(chars: list[dict]) -> list[str]:
    raw = "".join(c["text"] for c in chars)
    return sorted({m.group(1) for m in re.finditer(r"\((\d{1,2})\)", raw)}, key=int)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    total = parsed = 0
    with pdfplumber.open(args.pdf) as doc:
        for page_no, page in enumerate(doc.pages, start=1):
            for number in _numbers(page.chars):
                display = reconstruct_latex(page, number)
                if not display or ("=" not in display and "≥" not in display) or len(display) < 4:
                    continue
                total += 1
                parseable = to_parseable(display)
                try:
                    latex2sympy(parseable)
                    status = "OK "
                    parsed += 1
                except Exception:  # noqa: BLE001 — latex2sympy бросает разнородные ошибки
                    status = "ERR"
                print(f"({number}) p{page_no} {status} | {display}  ->  {parseable}")
    print(f"== {parsed}/{total} parsed")


if __name__ == "__main__":
    main()

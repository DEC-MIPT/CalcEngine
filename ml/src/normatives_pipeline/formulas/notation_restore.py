"""Восстановление индексов формулы по словарю обозначений (вариант A).

pix2text не обучен на кириллице и выдаёт индексы-обозначения побуквенной латиницей
с путаницей букв/цифр (``раб`` → ``pa6``, ``з`` → ``3``). Словарь обозначений
(``extract_formula_notation``) содержит авторитетные символы в юникоде; их транслит
подставляем вместо мусора. Кириллическое отображение остаётся в словаре отдельно —
`latex2sympy2` не парсит кириллицу в индексах и требует латинский идентификатор.
"""

from __future__ import annotations

import re
import unicodedata

from ..parser.symbols import CYR
from .validation import normalize_latex

_OMOGLYPHS = {
    "6": "b",  # б
    "3": "z",  # з
    "0": "o",  # о
    "4": "ch",  # ч
    "2": "g",  # г
}

_PRIME_CHARS = ("'", "´", "\u02b9", "\u2032", "\u2033", "\u2034")


def _canon(text: str) -> str:
    """Латинский канон для сравнения (устойчив к OCR-омографам)."""
    s = unicodedata.normalize("NFKC", text).lower()
    out: list[str] = []
    for ch in s:
        if ch in CYR:
            out.append(CYR[ch])
        elif ch in _OMOGLYPHS:
            out.append(_OMOGLYPHS[ch])
        elif ch.isascii() and ch.isalnum():
            out.append(ch)
    return "".join(out)


def _symbol_sub_canon(symbol: str) -> str:
    """Латинский транслит подстрочной части символа (``Рраб`` → ``rab``)."""
    s = unicodedata.normalize("NFKC", symbol).split("=", 1)[0].strip()
    chars = [ch for ch in s if ch not in _PRIME_CHARS]
    if len(chars) < 2:
        return ""
    return _canon("".join(chars[1:]))


def _close(a: str, b: str) -> bool:
    if not a or not b:
        return False
    if a == b:
        return True
    if len(a) == len(b):
        return sum(1 for x, y in zip(a, b) if x != y) <= 1
    return False


def restore_indices(latex: str, symbols: list[str]) -> str:
    """Подставляет латинский транслит обозначений вместо транслит-индексов pix2text.

    Сопоставление — по канону (транслит + омографы) с допуском в одну ошибку.
    ``P_{pa6}`` → ``P_{rab}`` (парсится `latex2sympy2`).
    """
    if not symbols:
        return latex
    out = normalize_latex(latex)
    for symbol in symbols:
        target = _symbol_sub_canon(symbol)
        if not target:
            continue
        for m in re.finditer(r"_\{([^{}]*)\}", out):
            idx = m.group(1)
            if _close(_canon(idx), target):
                out = out.replace("_{" + idx + "}", "_{" + target + "}")
                break
    return out

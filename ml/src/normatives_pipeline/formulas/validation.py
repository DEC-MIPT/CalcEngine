"""Семантическое сравнение LaTeX формул: канонизация и равенство выражений."""

from __future__ import annotations

import re
from typing import Any

from latex2sympy2 import latex2sympy  # type: ignore[import-untyped]


def normalize_latex(latex: str) -> str:
    """Снимает косметические различия LaTeX (не семантику)."""
    s = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", latex)
    s = re.sub(r"\\operatorname\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\left|\\right|\\,|\\!|\\;|~", "", s)
    s = re.sub(r"\\[bB]igg?[lrm]?", "", s)
    s = s.replace("\\prime", "'")
    s = s.replace("^{'}", "'")
    s = re.sub(r"'(_\{[^{}]*\})", r"\1'", s)
    for _ in range(3):
        s2 = re.sub(r"_\{\s*_\{([^{}]*)\}\s*\}", r"_{\1}", s)
        s2 = re.sub(r"\^\{\s*\^\{([^{}]*)\}\s*\}", r"^{\1}", s2)
        if s2 == s:
            break
        s = s2
    return re.sub(r"\s+", "", s)


def canonical_latex(latex: str) -> Any:
    """Приводит LaTeX к каноничной форме: SymPy-выражение или нормализованная строка."""
    s = normalize_latex(latex)
    try:
        return latex2sympy(s)
    except Exception:  # noqa: BLE001 — парсер бросает разнородные ошибки на непарном LaTeX
        return s


def formulas_equal(a: str, b: str) -> bool:
    """Семантическое равенство двух LaTeX формул."""
    return canonical_latex(a) == canonical_latex(b)

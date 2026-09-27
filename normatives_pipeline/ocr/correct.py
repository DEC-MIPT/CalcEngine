"""Стадия 3 — пост-коррекция известных искажений OCR (config-карта)."""

from __future__ import annotations

import re

from ..config import ocr_config

_MATH_CHARS = "=+-/()\\<>≤≥·"


def _pick_formula_line(lines: list[str]) -> str:
    best = ""
    best_score = -1
    for line in lines:
        score = sum(line.count(c) for c in _MATH_CHARS)
        if score > best_score:
            best = line
            best_score = score
    return best


def _strip_array(latex: str) -> str:
    latex = re.sub(r"\\begin\{array\}\s*\{[^{}]*\}", "", latex)
    latex = re.sub(r"\\end\{array\}", "", latex)
    lines = [p.strip().strip("{}").strip() for p in latex.split("\\\\")]
    lines = [line for line in lines if line]
    return _pick_formula_line(lines) if lines else latex


def correct_latex(latex: str) -> str:
    for wrong, right in ocr_config()["correct"].get("replacements", []):
        latex = latex.replace(wrong, right)
    if "\\begin{array}" in latex:
        latex = _strip_array(latex)
    latex = re.sub(r"\\mathrm\{\s*\}", "", latex)
    latex = re.sub(r"\\qquad|\\quad", "", latex)
    for spacing in ("~", "\\,", "\\;"):
        latex = latex.replace(spacing, " ")
    latex = re.sub(r"\s+", " ", latex).strip()
    return latex.rstrip(" ,;.:")

"""Стадия 3 — пост-коррекция известных искажений OCR (config-карта)."""

from __future__ import annotations

from ..config import ocr_config


def correct_latex(latex: str) -> str:
    for wrong, right in ocr_config()["correct"].get("replacements", []):
        latex = latex.replace(wrong, right)
    return latex

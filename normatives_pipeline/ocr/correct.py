"""Стадия 3 — пост-коррекция известных искажений OCR (config-карта)."""

from __future__ import annotations

import re

from ..config import ocr_config


def correct_latex(latex: str) -> str:
    for wrong, right in ocr_config()["correct"].get("replacements", []):
        latex = latex.replace(wrong, right)
    for spacing in ("~", "\\,", "\\;"):
        latex = latex.replace(spacing, " ")
    latex = re.sub(r"\s+", " ", latex).strip()
    return latex.rstrip(" ,;.:")

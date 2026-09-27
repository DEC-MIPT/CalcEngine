"""Двухстадийное чтение формулы: детекция области + распознавание (OCR)."""

from __future__ import annotations

from . import correct, detect, recognize


def read_formula(page, formula_number: str) -> str:
    bbox = detect.detect_formula_bbox(page.chars, formula_number)
    if bbox is None:
        return ""
    image = recognize.render_crop(page, bbox)
    return correct.correct_latex(recognize.recognize_latex(image))

"""Единый источник LaTeX формулы: текстовый слой или OCR — по типу PDF.

Правило выбора зашито в типе PDF, а не в вызывающем коде: ``text_layer.classify``
возвращает ``"text"`` (есть текстовый слой) или ``"scan"``. Для текстовых PDF LaTeX
собирается детерминированно из геометрии (``latex_reconstruct``); для сканов —
отложенный OCR-шаг (``detect``/``enrich``), здесь LaTeX остаётся пустым.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from ..parser import latex_reconstruct, text_layer
from ..parser.models import Formula


def classify_pdf(pages: list[str]) -> str:
    return text_layer.classify(pages)


def fill_latex(path: Path, formulas: list[Formula], pages: list[str]) -> list[Formula]:
    """Заполняет ``latex`` у формул текстового PDF; у скана оставляет как есть (OCR отложен)."""
    if classify_pdf(pages) != "text":
        return formulas
    reconstructed = latex_reconstruct.reconstruct_document(path)
    out: list[Formula] = []
    for f in formulas:
        latex = reconstructed.get(f.page, {}).get(f.number, "")
        out.append(replace(f, latex=latex) if latex else f)
    return out

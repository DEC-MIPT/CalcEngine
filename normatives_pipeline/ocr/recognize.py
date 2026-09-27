"""Стадия 2 — распознавание LaTeX из изображения (pix2tex, ViT)."""

from __future__ import annotations

from ..config import ocr_config

_model = None


def _get_model():
    global _model
    if _model is None:
        from pix2tex.cli import LatexOCR  # type: ignore[import-untyped]

        _model = LatexOCR()
    return _model


def render_crop(page, bbox: tuple):
    resolution = int(ocr_config()["recognize"]["resolution"])
    return page.crop(bbox).to_image(resolution=resolution).original


def recognize_latex(image) -> str:
    return _get_model()(image)

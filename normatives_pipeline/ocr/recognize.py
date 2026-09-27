"""Стадия 2 — распознавание LaTeX из изображения (pix2text LatexOCR, ONNX)."""

from __future__ import annotations

import importlib
import importlib.util
import sys
import types

from ..config import ocr_config

_model = None


def _load_latex_ocr():
    # Импорт LatexOCR напрямую, минуя pix2text/__init__.py: он тянет text-OCR
    # (cnocr/cnstd → pytorch-lightning → omegaconf), а нам нужен только latex_ocr.
    spec = importlib.util.find_spec("pix2text")
    if spec is None or not spec.submodule_search_locations:
        raise ImportError("pix2text не найден")
    pkg = types.ModuleType("pix2text")
    pkg.__path__ = list(spec.submodule_search_locations)
    pkg.__package__ = "pix2text"
    sys.modules["pix2text"] = pkg
    importlib.import_module("pix2text.consts")
    importlib.import_module("pix2text.utils")
    importlib.import_module("pix2text.latex_ocr")
    return sys.modules["pix2text.latex_ocr"].LatexOCR


def _get_model():
    global _model
    if _model is None:
        _model = _load_latex_ocr()(device="cpu")
    return _model


def render_crop(page, bbox: tuple):
    resolution = int(ocr_config()["recognize"]["resolution"])
    return page.crop(bbox).to_image(resolution=resolution).original


def recognize_latex(image) -> str:
    return _get_model().recognize(image)["text"]

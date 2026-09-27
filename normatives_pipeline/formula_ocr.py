"""Формульный пайплайн: детекция (DocLayout-YOLO) + распознавание (pix2text)."""

from __future__ import annotations

import importlib
import importlib.util
import re
import sys
import types

from PIL import Image

from .config import formula_ocr_config

_detector = None
_recognizer = None


def _import_latex_ocr():
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


def _get_detector():
    global _detector
    if _detector is None:
        from doclayout_yolo import YOLOv10  # type: ignore[import-untyped]
        from huggingface_hub import hf_hub_download

        weights = hf_hub_download(
            "juliozhao/DocLayout-YOLO-DocStructBench",
            "doclayout_yolo_docstructbench_imgsz1024.pt",
        )
        _detector = YOLOv10(weights)
    return _detector


def _get_recognizer():
    global _recognizer
    if _recognizer is None:
        _recognizer = _import_latex_ocr()(device="cpu")
    return _recognizer


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


def correct_latex(latex: str) -> str:
    if "\\begin{array}" in latex:
        latex = re.sub(r"\\begin\{array\}\s*\{[^{}]*\}", "", latex)
        latex = re.sub(r"\\end\{array\}", "", latex)
        lines = [p.strip().strip("{}").strip() for p in latex.split("\\\\")]
        lines = [line for line in lines if line]
        latex = _pick_formula_line(lines) if lines else latex
    latex = re.sub(r"\\mathrm\{\s*\}", "", latex)
    latex = re.sub(r"\\qquad|\\quad", "", latex)
    for spacing in ("~", "\\,", "\\;"):
        latex = latex.replace(spacing, " ")
    latex = re.sub(r"\s+", " ", latex).strip()
    return latex.rstrip(" ,;.:")


def detect_formulas(img) -> list[tuple]:
    cfg = formula_ocr_config()
    crops: list[tuple] = []
    for r in _get_detector().predict(img, conf=float(cfg["conf"]), imgsz=int(cfg["imgsz"])):
        for box, cls in zip(r.boxes.xyxy, r.boxes.cls):
            if r.names[int(cls)] == "isolate_formula":
                x1, y1, x2, y2 = [int(v) for v in box]
                crops.append(((x1, y1, x2, y2), img[y1:y2, x1:x2]))
    crops.sort(key=lambda item: item[0][1])
    return crops


def recognize_crop(crop) -> str:
    return correct_latex(_get_recognizer().recognize(Image.fromarray(crop[..., ::-1]))["text"])


def warm_up() -> None:
    """Прогрев моделей при старте сервиса: грузит детектор и распознаватель заранее."""
    _get_detector()
    _get_recognizer()

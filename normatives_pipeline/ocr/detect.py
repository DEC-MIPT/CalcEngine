"""Стадия 1 — детекция областей формул (по координатам и DocLayout-YOLO)."""

from __future__ import annotations

from ..config import ocr_config


def detect_formula_bbox(chars: list[dict], formula_number: str) -> tuple | None:
    """Прецизионная детекция по номеру формулы (для обогащения известных формул)."""
    cfg = ocr_config()["detect"]
    seq = list(f"({formula_number})")
    idx: int | None = None
    for i in range(len(chars) - len(seq) + 1):
        if [chars[j]["text"] for j in range(i, i + len(seq))] == seq:
            idx = i
            break
    if idx is None:
        return None

    marker = chars[idx : idx + len(seq)]
    y_center = sum(c["top"] for c in marker) / len(marker)
    marker_x0 = min(c["x0"] for c in marker)

    up = float(cfg["up_margin"])
    down = float(cfg["down_margin"])
    left = float(cfg["left_indent"])

    cands = [
        c
        for c in chars
        if c["x1"] <= marker_x0 - 2
        and c["x0"] >= left
        and y_center - up <= c["top"] <= y_center + down
    ]
    if not cands:
        return None

    pad = float(cfg["pad"])
    x0 = min(c["x0"] for c in cands) - pad
    top = min(c["top"] for c in cands) - pad
    x1 = max(c["x1"] for c in cands) + pad
    bottom = max(c["bottom"] for c in cands) + pad
    return (x0, top, x1, bottom)


_yolo = None


def _get_yolo():
    global _yolo
    if _yolo is None:
        from doclayout_yolo import YOLOv10  # type: ignore[import-untyped]
        from huggingface_hub import hf_hub_download

        weights = hf_hub_download(
            "juliozhao/DocLayout-YOLO-DocStructBench",
            "doclayout_yolo_docstructbench_imgsz1024.pt",
        )
        _yolo = YOLOv10(weights)
    return _yolo


def detect_formula_bboxes(image) -> list[tuple]:
    """Детекция всех областей формул на изображении страницы (DocLayout-YOLO)."""
    bboxes: list[tuple] = []
    for r in _get_yolo().predict(image, conf=0.25, imgsz=1024):
        for box, cls in zip(r.boxes.xyxy, r.boxes.cls):
            if r.names[int(cls)] == "isolate_formula":
                bboxes.append(tuple(int(v) for v in box))
    return bboxes

"""Обогащение формул: детекция + распознавание → latex + expression (кандидат)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pdfplumber

from .. import db
from ..config import detect_config
from . import detect
from .validation import canonical_latex

DEFAULT_PILOT = Path("docs/normative-base/СП 22.13330.2016.pdf")


def enrich(path: Path) -> int:
    if not path.exists():
        print(f"нет файла: {path}")
        return 1
    designation = path.stem

    conn = db.connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM document WHERE designation = %s", (designation,))
            row = cur.fetchone()
        if row is None:
            print(f"[skip] {designation} не в хранилище — сначала ingest")
            return 1
        doc_id = int(row["id"])

        formulas = db.fetch_formulas(conn, doc_id)
        by_page: dict[int, list[dict]] = {}
        for f in formulas:
            by_page.setdefault(f["page"], []).append(f)

        filled = 0
        dpi = int(detect_config()["dpi"])
        with pdfplumber.open(path) as pdf:
            for page_no, page_formulas in by_page.items():
                page = pdf.pages[page_no - 1]
                img_rgb = np.array(page.to_image(resolution=dpi).original)
                img_bgr = img_rgb[..., ::-1]
                crops = detect.detect_formulas(img_bgr)
                for i, (_, crop) in enumerate(crops):
                    if i >= len(page_formulas):
                        break
                    latex = detect.recognize_crop(crop)
                    if not latex:
                        continue
                    expression = str(canonical_latex(latex))
                    db.update_formula(conn, int(page_formulas[i]["id"]), latex, expression)
                    filled += 1
        print(f"[enriched] {designation}: заполнено {filled}/{len(formulas)} формул")
        return 0
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    path = Path(args[0]) if args else DEFAULT_PILOT
    return enrich(path)


if __name__ == "__main__":
    sys.exit(main())

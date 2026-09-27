"""Обогащение формул: OCR → latex + expression (машиночитаемый кандидат)."""

from __future__ import annotations

import sys
from pathlib import Path

import pdfplumber

from . import db
from .ocr import correct, detect, recognize
from .validation import canonical_latex

DEFAULT_PILOT = Path("norm-docs/СП 22.13330.2016.pdf")


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
        filled = 0
        with pdfplumber.open(path) as pdf:
            for f in formulas:
                page = pdf.pages[f["page"] - 1]
                bbox = detect.detect_formula_bbox(page.chars, f["number"])
                if bbox is None:
                    continue
                image = recognize.render_crop(page, bbox)
                latex = correct.correct_latex(recognize.recognize_latex(image))
                if not latex:
                    continue
                expression = str(canonical_latex(latex))
                db.update_formula(conn, int(f["id"]), latex, expression)
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

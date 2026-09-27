"""Точка входа парсера: разбор пилотного СП и валидация формулы (H6)."""

from __future__ import annotations

import sys
from pathlib import Path

from . import extractors, formula_code, text_layer
from .models import ParsedDocument

PILOT = Path("norm-docs/СП 22.13330.2016.pdf")


def main() -> int:
    if not PILOT.exists():
        print(f"нет пилотного файла: {PILOT}")
        return 1

    pages = text_layer.read_pages(PILOT)
    layer = text_layer.classify(pages)
    doc = ParsedDocument(
        designation="СП 22.13330.2016",
        layer=layer,
        clauses=tuple(extractors.extract_clauses(pages)),
        formulas=tuple(extractors.extract_formulas(pages)),
        notation=tuple(extractors.extract_notation(pages)),
        tables=tuple(extractors.extract_tables(PILOT, max_pages=15)),
    )

    print(f"[layer] {doc.layer}")
    print(f"[clauses] {len(doc.clauses)} (пример: {doc.clauses[3].number} {doc.clauses[3].text[:40]})")
    print(f"[formulas] {len(doc.formulas)} номеров (пример: {', '.join(f.number for f in doc.formulas[:8])})")
    print(f"[notation] {len(doc.notation)} записей")
    print(f"[tables] {len(doc.tables)} таблиц")

    print("\n=== Формула (5.7) → исполняемый код ===")
    bound = formula_code.demo_formula_5_7()
    f = bound.as_callable()
    values = [1.25, 1.0, 1.1, 0.5, 1.0, 2.0, 18.0, 3.0, 1.5, 9.0, 1.0, 2.0, 25.0]
    print(f"надёжное: R = {round(f(*values), 2)} кПа (символы: {', '.join(s.name for s in bound.symbols)})")

    naive = formula_code.alternative_parse_latex(bound.latex.split("=")[1].strip())
    print(f"parse_latex (менее валидно): {naive}")

    print(f"latex-only (менее валидно): {formula_code.alternative_latex_only(bound.latex)[:60]}...")
    print(f"codegen (менее валидно): {formula_code.alternative_codegen(bound.expr)[:60]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())

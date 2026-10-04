"""Офлайн-ingestion: обработать PDF один раз и сохранить в хранилище."""

from __future__ import annotations

import sys
from pathlib import Path

from . import db
from .config import formula_manifest, output_config, parser_config
from .parser import extractors, symbols, text_layer
from .retrieval import normalize_text

DEFAULT_PILOT = Path("docs/normative-base/СП 22.13330.2016.pdf")


def ingest(path: Path, force: bool = False) -> int:
    if not path.exists():
        print(f"нет файла: {path}")
        return 1

    pages = text_layer.read_pages(path)
    designation = text_layer.extract_designation(pages)
    if not designation:
        raise RuntimeError("не удалось извлечь обозначение документа с титульной страницы")
    edition = text_layer.extract_edition_year(designation)
    if not edition:
        raise RuntimeError(f"не удалось извлечь год издания из обозначения {designation!r}")
    year = int(edition)

    conn = db.connect()
    try:
        db.init_schema(conn)
        if not force and db.document_exists(conn, designation):
            print(f"[skip] {designation} уже в хранилище")
            return 0
        if force:
            db.delete_document(conn, designation)

        clauses = extractors.extract_clauses(pages)

        numbered = extractors.associate_formulas_to_clauses(
            clauses, extractors.extract_formulas(pages)
        )
        unnumbered, unnumbered_notation = extractors.extract_unnumbered_formulas(
            pages, clauses
        )
        formulas = numbered + unnumbered

        seen: set[str] = set()
        deduped = []
        for f in formulas:
            if f.number in seen:
                continue
            seen.add(f.number)
            deduped.append(f)
        formulas = deduped

        formula_notation = extractors.extract_formula_notation(pages, numbered)
        formula_notation.update(unnumbered_notation)
        cross_refs = extractors.extract_cross_refs(pages, clauses)

        heading = {c.number: c.text for c in clauses}
        label = parser_config()["formula_label"]
        doc_id = db.upsert_document(conn, designation, edition=edition, year=year)

        clause_rows = [
            (c.number, c.text, c.page, normalize_text(c.text)) for c in clauses
        ]
        db.insert_clauses(conn, doc_id, clause_rows)

        manifest = {
            (m["designation"], m["number"]): m for m in formula_manifest()
        }

        formula_rows = []
        notation_rows = []
        for f in formulas:
            m = manifest.get((designation, f.number))
            f_latex = m["latex"] if m else f.latex
            f_expression = m["expression"] if m else ""

            meanings = [n.meaning for n in formula_notation.get(f.number, [])]
            search = normalize_text(
                f"{label} {f.number} {heading.get(f.clause, '')} "
                + " ".join(meanings)
                + f" {f_latex}"
            )
            if m:
                status, provenance = "verified", "human-verified"
            else:
                status, provenance = "unverified", "machine-extracted"
            formula_rows.append(
                (
                    f.number, f.clause, f_latex, f_expression, f.raw_text, f.page,
                    search, status, provenance,
                )
            )

            if m:
                for s in m["symbols"]:
                    notation_rows.append(
                        (f.number, s["id"], s["latex"], s["meaning"], s["unit"], s["kind"])
                    )
            else:
                for n in formula_notation.get(f.number, []):
                    for sym in symbols.split_symbols(n.symbol):
                        norm = symbols.normalize_symbol(sym)
                        if norm is None:
                            continue
                        ident, sym_latex = norm
                        notation_rows.append(
                            (f.number, ident, sym_latex, n.meaning, n.unit, "input")
                        )
        db.insert_formulas(conn, doc_id, formula_rows)
        db.insert_notation(conn, doc_id, notation_rows)

        ref_rows = [(r.clause, r.ref_type, r.value, r.url) for r in cross_refs]
        db.insert_cross_refs(conn, doc_id, ref_rows)

        table_prefix = output_config()["table_prefix"]
        tables = extractors.extract_tables(path)
        coeff_rows = [
            (
                t.number, t.page, ri, ci, value,
                "unverified",
                f"{table_prefix} {t.number}" if t.number else "unverified",
                "unverified",
                "machine-extracted",
            )
            for t in tables
            for ri, row in enumerate(t.rows)
            for ci, value in enumerate(row)
            if value
        ]
        db.insert_coefficients(conn, doc_id, coeff_rows)

        print(
            f"[ingested] {designation}: пунктов {len(clauses)}, формул {len(formulas)} "
            f"({len(numbered)} нумерованных, {len(unnumbered)} синтетических), "
            f"обозначений {len(notation_rows)}, ссылок {len(ref_rows)}, "
            f"таблиц {len(tables)}, ячеек {len(coeff_rows)}"
        )
        return 0
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    force = False
    if "--force" in args:
        force = True
        args = [a for a in args if a != "--force"]
    path = Path(args[0]) if args else DEFAULT_PILOT
    return ingest(path, force=force)


if __name__ == "__main__":
    sys.exit(main())

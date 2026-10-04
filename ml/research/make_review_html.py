r"""HTML для визуальной сверки: слева скриншот из PDF, справа то же из БД.

Для одного документа строит страницу с двумя разделами (формула и таблица). В каждом
разделе две колонки:
  * слева — вырезка из PDF (PyMuPDF, bbox берётся через pdfplumber) ;
  * справа — то, что отдаём Акиму (payload / NormRef как JSON) и визуальная форма
    (формула — MathJax, таблица — HTML-таблица из сохранённых ячеек).

Только библиотеки: pdfplumber (bbox), pymupdf (растр), psycopg2 (чтение БД). LLM нет.
Ничего в рабочем коде не меняется.

Запуск (из каталога ml/):

    DEC_DATABASE_URL=postgresql://dec:dec@localhost:5433/dec_e2e \
      python -m research.make_review_html ../docs/normative-base/СП\ 22.13330.2016.pdf \
        --formula 5.7 --table 5.5 --out research/review/sp22.html
"""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter
from pathlib import Path

import pdfplumber
import pymupdf as fitz

from normatives_pipeline import db
from normatives_pipeline.ingest import ingest

ZOOM = 3.0


def _esc(value: object) -> str:
    return html.escape(str(value)).replace("\n", "<br>")


def _safe(name: str) -> str:
    return re.sub(r"[^0-9A-Za-zА-Яа-я._-]", "_", name)


def _cell_map(cells: list[dict]) -> dict[tuple[int, int], str]:
    return {(c["row_index"], c["col_index"]): c["value"] for c in cells}


def _overlap(a: dict, b: dict) -> int:
    return sum((Counter(a.values()) & Counter(b.values())).values())


def _render_clip(pdf_path: Path, page_no: int, rect: tuple, out: Path) -> None:
    doc = fitz.open(pdf_path)
    page = doc[page_no - 1]
    clip = fitz.Rect(*rect)
    pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=clip, alpha=False)
    out.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out)
    doc.close()


def _formula_clip(pdf_path: Path, page_no: int, number: str, out: Path) -> None:
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_no - 1]
        matches = page.search(r"\(\s*" + re.escape(number) + r"\s*\)", regex=True)
        if matches:
            bottom = max(m["bottom"] for m in matches)
        else:
            bottom = page.height * 0.6
        x0 = 30
        x1 = page.width - 30
        y0 = max(0, bottom - 260)
        y1 = min(page.height, bottom + 25)
    _render_clip(pdf_path, page_no, (x0, y0, x1, y1), out)


def _table_clip(
    pdf_path: Path, page_no: int, db_cells: dict, out: Path
) -> None:
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_no - 1]
        tables = page.find_tables()
        if not tables:
            _render_clip(pdf_path, page_no, (0, 0, page.width, page.height), out)
            return
        best = max(
            tables, key=lambda t: _overlap(_cell_map_of(t), db_cells)
        )
        x0, top, x1, bottom = best.bbox
        rect = (max(0, x0 - 6), max(0, top - 46), min(page.width, x1 + 6), min(page.height, bottom + 6))
    _render_clip(pdf_path, page_no, rect, out)


def _cell_map_of(tbl) -> dict[tuple[int, int], str]:
    out: dict[tuple[int, int], str] = {}
    for ri, row in enumerate(tbl.extract()):
        for ci, cell in enumerate(row):
            value = "" if cell is None else str(cell).strip()
            if value:
                out[(ri, ci)] = value
    return out


def _pick_formula(conn, doc_id: int) -> dict | None:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT f.number, f.clause_number, f.latex, f.expression, f.raw_text,
                   f.page, f.status, f.provenance
            FROM formula f WHERE f.document_id = %s
            ORDER BY (f.latex <> '') DESC, (f.number NOT LIKE '%%#%%') DESC,
                     length(f.raw_text) DESC, f.id
            LIMIT 1
            """,
            (doc_id,),
        )
        row = cur.fetchone()
    return dict(row) if row else None


def _pick_table(conn, doc_id: int, requested: str | None) -> str | None:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_number FROM coefficient
            WHERE document_id = %s AND table_number <> ''
            GROUP BY table_number
            ORDER BY count(*) DESC, table_number LIMIT 1
            """,
            (doc_id,),
        )
        largest = cur.fetchone()
    if requested:
        return requested
    return largest["table_number"] if largest else None


def _payload_table(conn, doc_id: int, table_number: str) -> str:
    rows = db.fetch_coefficients(conn, doc_id, table_number)
    if not rows:
        return "<p>нет данных</p>"
    data = next(
        (r for r in rows if re.search(r"\d", r["value"]) and r["value"] not in ("", "0")),
        rows[0],
    )
    ref = db.build_coefficient_norm_ref(rows[0])
    payload = db.build_coefficient_payload(data)
    return (
        "<h4>NormRef</h4><pre>"
        + _esc(json.dumps(ref, ensure_ascii=False, indent=2))
        + "</pre><h4>payload одной ячейки (как отдаём Акиму)</h4><pre>"
        + _esc(json.dumps(payload, ensure_ascii=False, indent=2))
        + "</pre>"
    )


def _grid_html(cells: list[dict], page: int) -> str:
    on_page = [c for c in cells if c["page"] == page]
    if not on_page:
        return "<p>нет данных на странице</p>"
    max_r = max(c["row_index"] for c in on_page)
    max_c = max(c["col_index"] for c in on_page)
    grid = [["" for _ in range(max_c + 1)] for _ in range(max_r + 1)]
    for c in on_page:
        grid[c["row_index"]][c["col_index"]] = _esc(c["value"])
    head = "".join(f"<th>{ci}</th>" for ci in range(max_c + 1))
    body = "".join(
        "<tr><th>" + str(ri) + "</th>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>"
        for ri, row in enumerate(grid)
    )
    return f'<table class="data"><tr><th></th>{head}</tr>{body}</table>'


def _symbols_html(conn, doc_id: int, number: str) -> str:
    symbols = db.fetch_notation(conn, doc_id, number)
    if not symbols:
        return "<p>обозначения не найдены</p>"
    rows = "".join(
        "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            _esc(s["symbol"]), _esc(s["latex"]), _esc(s["meaning"]),
            _esc(s["unit"]), _esc(s["kind"]),
        )
        for s in symbols
    )
    return (
        '<table class="data"><tr><th>id</th><th>latex</th><th>meaning</th>'
        "<th>unit</th><th>kind</th></tr>" + rows + "</table>"
    )


def build_html(pdf_path: Path, out: Path, formula_no: str | None, table_no: str | None) -> int:
    print("[ingest] ...")
    if ingest(pdf_path, force=True) != 0:
        print("ingest вернул ошибку")
        return 1

    conn = db.connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT d.id, d.designation, d.edition, d.year,
                       (SELECT count(*) FROM clause c WHERE c.document_id=d.id) clauses,
                       (SELECT count(*) FROM formula f WHERE f.document_id=d.id) formulas,
                       (SELECT count(*) FROM coefficient k WHERE k.document_id=d.id) coeffs
                FROM document d
                WHERE d.designation = (
                    SELECT designation FROM document ORDER BY id DESC LIMIT 1
                )
                """
            )
            doc = dict(cur.fetchone())
        doc_id = doc["id"]

        formula = None
        if formula_no:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT f.number, f.clause_number, f.latex, f.expression, f.raw_text,
                           f.page, f.status, f.provenance
                    FROM formula f WHERE f.document_id = %s AND f.number = %s
                    """,
                    (doc_id, formula_no),
                )
                row = cur.fetchone()
                formula = dict(row) if row else None
        if formula is None:
            formula = _pick_formula(conn, doc_id)

        table_number = _pick_table(conn, doc_id, table_no)
        table_cells = (
            db.fetch_coefficients(conn, doc_id, table_number) if table_number else []
        )

        assets = out.parent / (out.stem + "_assets")
        assets.mkdir(parents=True, exist_ok=True)

        formula_left = ""
        formula_right = ""
        if formula:
            fimg = assets / f"formula_{_safe(formula['number'])}.png"
            _formula_clip(pdf_path, formula["page"], formula["number"], fimg)
            formula_left = (
                f'<figure><img src="{fimg.name}" alt="formula from pdf">'
                f"<figcaption>PDF, стр. {formula['page']}</figcaption></figure>"
            )
            with conn.cursor() as cur:
                cur.execute("SELECT edition FROM document WHERE id = %s", (doc_id,))
                edition = cur.fetchone()["edition"]
            payload = db.build_formula_payload(
                conn,
                {
                    "document_id": doc_id,
                    "designation": doc["designation"],
                    "number": formula["number"],
                    "clause_number": formula["clause_number"],
                    "latex": formula["latex"],
                    "expression": formula["expression"],
                    "edition": edition,
                    "status": formula["status"],
                    "provenance": formula["provenance"],
                },
            )
            latex = formula["latex"]
            if latex:
                rendered = f'<div class="math">\\[{html.escape(latex)}\\]</div>'
            else:
                rendered = (
                    '<p class="note">latex пуст: формула распознана детектором и хранится '
                    "как machine-extracted; OCR-путь (pix2text) отложен (design decision 4).</p>"
                    f'<pre>{_esc(formula["raw_text"])}</pre>'
                )
            formula_right = (
                "<h4>payload (как отдаём Акиму)</h4><pre>"
                + _esc(json.dumps(payload, ensure_ascii=False, indent=2))
                + "</pre><h4>визуально (MathJax)</h4>"
                + rendered
                + "<h4>обозначения</h4>"
                + _symbols_html(conn, doc_id, formula["number"])
            )

        table_left = ""
        table_right = ""
        if table_number and table_cells:
            first_page = min(c["page"] for c in table_cells)
            timg = assets / f"table_{_safe(table_number)}.png"
            _table_clip(
                pdf_path, first_page, _cell_map(
                    [c for c in table_cells if c["page"] == first_page]
                ), timg
            )
            table_left = (
                f'<figure><img src="{timg.name}" alt="table from pdf">'
                f"<figcaption>PDF, табл. {table_number}, стр. {first_page}</figcaption></figure>"
            )
            other = sorted({c["page"] for c in table_cells if c["page"] != first_page})
            note = (
                f'<p class="note">таблица продолжается на стр. {other}</p>' if other else ""
            )
            table_right = (
                _payload_table(conn, doc_id, table_number)
                + note
                + "<h4>визуально (сохранённые ячейки, строка/колонка)</h4>"
                + _grid_html(table_cells, first_page)
            )
    finally:
        conn.close()

    document_html = f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<title>Сверка PDF и БД — {_esc(doc['designation'])}</title>
<script>window.MathJax={{tex:{{displayMath:[['\\\\[','\\\\]'],['$$','$$']]}}}};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
 body{{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:24px;color:#1b1f23}}
 h1{{font-size:20px}} h2{{font-size:17px;margin-top:28px;border-top:2px solid #ddd;padding-top:12px}}
 h4{{margin:14px 0 4px;font-size:13px;color:#444}}
 .grid{{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}}
 .card{{border:1px solid #d0d7de;border-radius:8px;padding:12px;background:#fff}}
 .pdf{{background:#fafafa}}
 figure{{margin:0}} img{{max-width:100%;border:1px solid #ccc;border-radius:4px}}
 figcaption{{font-size:12px;color:#666;margin-top:4px}}
 pre{{background:#f6f8fa;border:1px solid #e1e4e8;border-radius:6px;padding:10px;
      overflow:auto;font-size:12px;white-space:pre-wrap}}
 table.data{{border-collapse:collapse;font-size:11px;margin-top:6px}}
 table.data th,table.data td{{border:1px solid #c8c8c8;padding:3px 6px;vertical-align:top;max-width:260px}}
 table.data th{{background:#eef1f4}}
 .math{{font-size:18px;overflow-x:auto;padding:6px 0}}
 .note{{font-size:12px;color:#8a6d00;background:#fff8e1;border:1px solid #ffe08a;
        border-radius:6px;padding:6px 8px}}
 .meta{{color:#555;font-size:13px}}
</style></head><body>
<h1>Сверка «PDF ↔ БД» — {_esc(doc['designation'])}</h1>
<p class="meta">издание {_esc(doc['edition'])}, год {_esc(doc['year'])} ·
 пунктов {doc['clauses']} · формул {doc['formulas']} · ячеек {doc['coeffs']}</p>
<h2>Формула {_esc(formula['number']) if formula else ''}</h2>
<div class="grid">
 <div class="card pdf">{formula_left}</div>
 <div class="card">{formula_right}</div>
</div>
<h2>Таблица {_esc(table_number) if table_number else ''}</h2>
<div class="grid">
 <div class="card pdf">{table_left}</div>
 <div class="card">{table_right}</div>
</div>
</body></html>
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(document_html, encoding="utf-8")
    print(f"[written] {out} (+ assets {assets})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--formula", default=None)
    parser.add_argument("--table", default=None)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if not args.pdf.exists():
        print(f"нет файла: {args.pdf}")
        return 2
    return build_html(args.pdf, args.out, args.formula, args.table)


if __name__ == "__main__":
    raise SystemExit(main())

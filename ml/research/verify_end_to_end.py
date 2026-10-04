"""End-to-end проверка нормативного пайплайна: PDF -> парсинг -> БД -> чтение -> сверка.

Только детерминированные Python-библиотеки: pdftotext, pdfplumber, psycopg2. LLM не
используется. Рабочий код пайплайна не изменяется — скрипт только читает и сравнивает.

Что делает для одного PDF:
  1. извлекает обозначение и год издания с титульной страницы (text_layer);
  2. загружает документ в БД штатным ingest (python -m normatives_pipeline.ingest);
  3. проверяет инварианты NormRef по всем формулам и коэффициентам документа;
  4. читает из БД то, что ждёт потребитель (search.query + build_formula_payload,
     fetch_coefficients + build_coefficient_payload);
  5. точная сверка «экстрактор -> БД -> чтение»: набор ячеек, который вернул
     pdfplumber-экстрактор (extractors.extract_tables), сравнивается с тем, что лежит в
     БД, как multiset (Counter). Ловит потерю ячеек, порчу значений и дубликаты;
  6. независимая сверка одной выбранной таблицы: она заново извлекается из PDF прямым
     вызовом pdfplumber (не через extractors) и сверяется с БД по строкам/колонкам.

Шаги 5 и 6 дополняют друг друга: 5 покрывает весь документ и гарантирует, что хранилище
и чтение ничего не теряют; 6 подтверждает содержимое таблицы прямо из PDF.

Запуск (из каталога ml/, с поднятым Postgres):

    DEC_DATABASE_URL=postgresql://dec:dec@localhost:5433/dec \
      python -m research.verify_end_to_end "../docs/normative-base/СП 22.13330.2016.pdf"

    # независимо сверить конкретную таблицу (по умолчанию 5.5, иначе первую)
    ... python -m research.verify_end_to_end --table 5.5 <pdf>
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import pdfplumber

from normatives_pipeline import db
from normatives_pipeline.config import output_config
from normatives_pipeline.ingest import ingest
from normatives_pipeline.parser import extractors, text_layer
from normatives_pipeline.search import query

CellMap = dict[tuple[int, int], str]


def _cells(rows: list[list[str | None]]) -> CellMap:
    out: CellMap = {}
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row):
            value = "" if cell is None else str(cell).strip()
            if value:
                out[(ri, ci)] = value
    return out


def _caption_regex(table_number: str) -> re.Pattern[str]:
    number = "".join(
        r"\s*\.\s*" if ch == "." else re.escape(ch) for ch in table_number
    )
    return re.compile(r"[Тт]\s*а\s*б\s*л\s*и\s*ц\s*а\s*" + number)


def independent_table(
    pdf, pages: list[str], table_number: str, page_hint: int | None
) -> tuple[int | None, CellMap]:
    """Прямое извлечение таблицы из PDF по подписи; возвращает страницу и ячейки.

    Среди страниц, где подпись встречается, берётся та, что совпадает с page_hint
    (страницей из БД), иначе первая, где таблица начинается сразу под подписью.
    """
    pattern = _caption_regex(table_number)
    candidates = [i for i, text in enumerate(pages, start=1) if pattern.search(text)]
    if page_hint in candidates:
        candidates = [page_hint] + [c for c in candidates if c != page_hint]

    for page_no in candidates:
        if not (1 <= page_no <= len(pdf.pages)):
            continue
        page = pdf.pages[page_no - 1]
        matches = page.search(pattern.pattern, regex=True)
        tables = page.find_tables()
        if not tables:
            continue
        anchors = sorted(m.get("bottom", 0) for m in matches)
        for anchor in anchors:
            below = [t for t in tables if t.bbox[1] >= anchor - 1]
            if not below:
                continue
            chosen = min(below, key=lambda t: t.bbox[1])
            if chosen.bbox[1] - anchor <= 250:
                return page_no, _cells(chosen.extract())
    return None, {}


def audit_norm_refs(conn, document_id: int) -> list[str]:
    violations: list[str] = []
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT f.number, f.status, f.provenance, d.edition
            FROM formula f JOIN document d ON d.id = f.document_id
            WHERE f.document_id = %s
            """,
            (document_id,),
        )
        for r in cur.fetchall():
            if not r["edition"]:
                violations.append(f"formula {r['number']}: пустой edition")
            if r["status"] not in ("verified", "unverified"):
                violations.append(f"formula {r['number']}: status={r['status']!r}")
            if r["provenance"] not in ("human-verified", "machine-extracted"):
                violations.append(f"formula {r['number']}: provenance={r['provenance']!r}")
            if r["status"] == "verified" and r["provenance"] != "human-verified":
                violations.append(
                    f"formula {r['number']}: verified, но provenance={r['provenance']!r}"
                )

        cur.execute(
            """
            SELECT table_number, row_index, col_index, document_id,
                   edition, clause, status, provenance
            FROM coefficient WHERE document_id = %s
            """,
            (document_id,),
        )
        for r in cur.fetchall():
            where = f"coefficient {r['table_number']}[{r['row_index']},{r['col_index']}]"
            if not r["document_id"]:
                violations.append(f"{where}: нет document_id")
            if not r["clause"]:
                violations.append(f"{where}: пустой clause")
            if r["status"] not in ("verified", "unverified"):
                violations.append(f"{where}: status={r['status']!r}")
            if r["status"] == "verified" and (
                r["edition"] == "unverified" or r["clause"] == "unverified"
            ):
                violations.append(f"{where}: verified, но ссылка не конкретна")
    return violations


def verify_coefficient_roundtrip(path: Path, conn, doc_id: int) -> list[str]:
    """Точная сверка ячеек extractors.extract_tables с тем, что лежит в БД (Counter)."""
    expected: Counter = Counter(
        (t.number, t.page, ri, ci, value)
        for t in extractors.extract_tables(path)
        for ri, row in enumerate(t.rows)
        for ci, value in enumerate(row)
        if value
    )
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_number, page, row_index, col_index, value
            FROM coefficient WHERE document_id = %s
            """,
            (doc_id,),
        )
        actual: Counter = Counter(
            (
                r["table_number"],
                r["page"],
                r["row_index"],
                r["col_index"],
                r["value"],
            )
            for r in cur.fetchall()
        )

    print(f"[roundtrip] экстрактор={sum(expected.values())} БД={sum(actual.values())}")
    failures: list[str] = []
    if expected == actual:
        return failures
    for row in list((expected - actual).items())[:10]:
        failures.append(f"roundtrip: нет в БД {row[0]}")
    for row in list((actual - expected).items())[:10]:
        failures.append(f"roundtrip: лишнее в БД {row[0]}")
    return failures


def verify_independent_table(
    path: Path, pages: list[str], conn, doc_id: int, table_number: str
) -> list[str]:
    """Независимая сверка одной таблицы: прямой pdfplumber vs БД, по строкам/колонкам."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT page, row_index, col_index, value FROM coefficient
            WHERE document_id = %s AND table_number = %s
            ORDER BY page, row_index, col_index
            """,
            (doc_id, table_number),
        )
        rows = [dict(r) for r in cur.fetchall()]
    if not rows:
        return [f"таблица {table_number} не найдена в БД"]

    page_hint = min(r["page"] for r in rows)
    db_cells: CellMap = {}
    db_pages: set[int] = set()
    for r in rows:
        db_pages.add(r["page"])
        if r["page"] == page_hint:
            db_cells[(r["row_index"], r["col_index"])] = r["value"]

    with pdfplumber.open(path) as pdf:
        found_page, pdf_cells = independent_table(pdf, pages, table_number, page_hint)

    failures: list[str] = []
    if found_page is None:
        return [f"таблица {table_number}: подпись не найдена в PDF"]
    for key, value in sorted(pdf_cells.items()):
        dbv = db_cells.get(key)
        if dbv is None:
            failures.append(f"таблица {table_number} стр.{found_page}: нет в БД {key}={value!r}")
        elif dbv != value:
            failures.append(
                f"таблица {table_number} стр.{found_page}: {key} pdf={value!r} db={dbv!r}"
            )
    for key, value in sorted(db_cells.items()):
        if key not in pdf_cells:
            failures.append(
                f"таблица {table_number} стр.{found_page}: лишнее в БД {key}={value!r}"
            )
    status = "ok" if not failures else "MISMATCH"
    print(
        f"[independent] табл. {table_number} стр.{found_page}: "
        f"pdf={len(pdf_cells)} db={len(db_cells)} {status}"
        + (f" | БД на стр. {sorted(db_pages)}" if len(db_pages) > 1 else "")
    )
    return failures


def verify(path: Path, only_table: str | None) -> int:
    pages = text_layer.read_pages(path)
    designation = text_layer.extract_designation(pages)
    edition = text_layer.extract_edition_year(designation)
    print(f"[title] designation={designation!r} edition={edition!r}")

    failures: list[str] = []
    if not designation or not edition:
        failures.append("не извлечены обозначение/год с титульной страницы")

    print("[ingest] ...")
    if ingest(path, force=True) != 0:
        print("FAIL: ingest вернул ошибку")
        return 1

    conn = db.connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, designation, edition, year FROM document WHERE designation = %s",
                (designation,),
            )
            doc = dict(cur.fetchone())
        doc_id = doc["id"]
        print(f"[db] document id={doc_id} edition={doc['edition']!r} year={doc['year']}")

        if doc["edition"] != edition or doc["year"] != int(edition):
            failures.append("edition/year в БД не совпали с титульной страницей")

        violations = audit_norm_refs(conn, doc_id)
        print(f"[normref] нарушений: {len(violations)}")
        failures.extend(violations)

        formula = _pick_formula(conn, doc_id)
        if formula is not None:
            payload = db.build_formula_payload(conn, formula)
            print(f"[payload] формула {formula['number']} -> {payload['norm_ref']}")
            if list(payload.keys()) != output_config()["formula_keys"]:
                failures.append("formula payload не совпал с [output] formula_keys")

        search_text = _search_query(conn, doc_id)
        result = query(search_text)
        print(f"[search] запрос={search_text!r} формул в выдаче={len(result['formulas'])}")
        for p in result["formulas"]:
            if list(p.keys()) != output_config()["formula_keys"]:
                failures.append("search.query вернул payload с чужими ключами")

        failures.extend(verify_coefficient_roundtrip(path, conn, doc_id))

        target = only_table or _largest_numbered_table(conn, doc_id)
        if target is None:
            print("[independent] нумерованных таблиц нет — независимая сверка пропущена")
        else:
            failures.extend(verify_independent_table(path, pages, conn, doc_id, target))
    finally:
        conn.close()

    print("\n=== ИТОГ ===")
    if failures:
        print(f"FAIL ({len(failures)}):")
        for f in failures[:40]:
            print("  -", f)
        return 1
    print("PASS: PDF -> БД -> чтение совпадают, инварианты NormRef соблюдены")
    return 0


def _pick_formula(conn, doc_id: int) -> dict | None:
    """Любая формула документа (без привязки к пилоту); предпочитаем с expression."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT d.id AS document_id, d.designation, f.number, f.clause_number,
                   f.latex, f.expression, f.raw_text, f.page,
                   d.edition, f.status, f.provenance
            FROM formula f JOIN document d ON d.id = f.document_id
            WHERE f.document_id = %s
            ORDER BY (f.expression <> '') DESC, (f.latex <> '') DESC, f.id
            LIMIT 1
            """,
            (doc_id,),
        )
        row = cur.fetchone()
    return dict(row) if row else None


def _search_query(conn, doc_id: int) -> str:
    """Запрос строится из первого пункта документа, а не зашит под пилот."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT title FROM clause WHERE document_id = %s ORDER BY id LIMIT 1",
            (doc_id,),
        )
        row = cur.fetchone()
    if not row:
        return ""
    words = re.findall(r"[А-Яа-яЁёA-Za-z0-9]+", row["title"])
    return " ".join(words[:5])


def _largest_numbered_table(conn, doc_id: int) -> str | None:
    """Самая крупная нумерованная таблица документа — обобщённый выбор, без пилота."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_number FROM coefficient
            WHERE document_id = %s AND table_number <> ''
            GROUP BY table_number ORDER BY count(*) DESC, table_number
            LIMIT 1
            """,
            (doc_id,),
        )
        row = cur.fetchone()
    return row["table_number"] if row else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--table", default=None, help="независимо сверить одну таблицу")
    args = parser.parse_args(argv)

    if not args.pdf.exists():
        print(f"нет файла: {args.pdf}")
        return 2
    return verify(args.pdf, args.table)


if __name__ == "__main__":
    sys.exit(main())

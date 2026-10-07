"""Хранилище PostgreSQL: схема, низкоуровневые операции и поиск."""

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import Any

import psycopg2  # type: ignore[import-untyped]
from psycopg2.extras import (  # type: ignore[import-untyped]
    Json,
    RealDictCursor,
    execute_values,
)

from .config import output_config, search_config

SCHEMA = """
CREATE TABLE IF NOT EXISTS document (
    id SERIAL PRIMARY KEY,
    designation TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    edition TEXT NOT NULL DEFAULT '',
    year INT,
    source_url TEXT NOT NULL DEFAULT '',
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS clause (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    number TEXT NOT NULL,
    title TEXT NOT NULL,
    page INT,
    search_text TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS formula (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    number TEXT NOT NULL,
    clause_number TEXT NOT NULL DEFAULT '',
    latex TEXT NOT NULL DEFAULT '',
    expression TEXT NOT NULL DEFAULT '',
    raw_text TEXT NOT NULL DEFAULT '',
    page INT,
    search_text TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'unverified',
    provenance TEXT NOT NULL DEFAULT 'machine-extracted'
);
ALTER TABLE formula ADD COLUMN IF NOT EXISTS expression TEXT NOT NULL DEFAULT '';
ALTER TABLE formula ADD COLUMN IF NOT EXISTS status TEXT NOT NULL DEFAULT 'unverified';
ALTER TABLE formula ADD COLUMN IF NOT EXISTS provenance TEXT NOT NULL DEFAULT 'machine-extracted';

CREATE TABLE IF NOT EXISTS notation_entry (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    formula_number TEXT NOT NULL DEFAULT '',
    symbol TEXT NOT NULL,
    latex TEXT NOT NULL DEFAULT '',
    meaning TEXT NOT NULL,
    unit TEXT NOT NULL DEFAULT '',
    kind TEXT NOT NULL DEFAULT 'input'
);
ALTER TABLE notation_entry ADD COLUMN IF NOT EXISTS latex TEXT NOT NULL DEFAULT '';
ALTER TABLE notation_entry ADD COLUMN IF NOT EXISTS kind TEXT NOT NULL DEFAULT 'input';

CREATE TABLE IF NOT EXISTS cross_ref (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    clause_number TEXT NOT NULL DEFAULT '',
    ref_type TEXT NOT NULL,
    ref_value TEXT NOT NULL,
    url TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS condition (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    clause_number TEXT NOT NULL DEFAULT '',
    text TEXT NOT NULL,
    page INT,
    line INT,
    kind TEXT NOT NULL DEFAULT 'condition',
    status TEXT NOT NULL DEFAULT 'unverified',
    provenance TEXT NOT NULL DEFAULT 'machine-extracted'
);
ALTER TABLE condition ADD COLUMN IF NOT EXISTS line INT;

CREATE TABLE IF NOT EXISTS coefficient (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    table_number TEXT NOT NULL DEFAULT '',
    page INT,
    row_index INT NOT NULL,
    col_index INT NOT NULL,
    value TEXT NOT NULL,
    edition TEXT NOT NULL DEFAULT 'unverified',
    clause TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'unverified',
    provenance TEXT NOT NULL DEFAULT 'machine-extracted'
);
ALTER TABLE coefficient ADD COLUMN IF NOT EXISTS edition TEXT NOT NULL DEFAULT 'unverified';
ALTER TABLE coefficient ADD COLUMN IF NOT EXISTS clause TEXT NOT NULL DEFAULT '';
ALTER TABLE coefficient ADD COLUMN IF NOT EXISTS status TEXT NOT NULL DEFAULT 'unverified';
ALTER TABLE coefficient ADD COLUMN IF NOT EXISTS provenance TEXT NOT NULL DEFAULT 'machine-extracted';

CREATE INDEX IF NOT EXISTS idx_clause_doc ON clause(document_id);
CREATE INDEX IF NOT EXISTS idx_formula_doc ON formula(document_id);
CREATE INDEX IF NOT EXISTS idx_notation_doc ON notation_entry(document_id);
CREATE INDEX IF NOT EXISTS idx_crossref_doc ON cross_ref(document_id);
CREATE INDEX IF NOT EXISTS idx_coefficient_doc ON coefficient(document_id);
CREATE INDEX IF NOT EXISTS idx_coefficient_table ON coefficient(document_id, table_number);

CREATE EXTENSION IF NOT EXISTS pg_trgm;
DROP INDEX IF EXISTS idx_clause_search;
DROP INDEX IF EXISTS idx_formula_search;
CREATE INDEX IF NOT EXISTS idx_clause_search ON clause
    USING gin (search_text gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_formula_search ON formula
    USING gin (search_text gin_trgm_ops);

ALTER TABLE formula ADD COLUMN IF NOT EXISTS result_symbol TEXT NOT NULL DEFAULT '';
ALTER TABLE formula ADD COLUMN IF NOT EXISTS tree JSONB;
ALTER TABLE formula ADD COLUMN IF NOT EXISTS units JSONB;

CREATE TABLE IF NOT EXISTS catalog_binding (
    id SERIAL PRIMARY KEY,
    calculation_type TEXT NOT NULL,
    parameter TEXT NOT NULL,
    kind TEXT NOT NULL,
    document_id INT NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    formula_number TEXT NOT NULL DEFAULT '',
    table_number TEXT NOT NULL DEFAULT '',
    heading_symbol TEXT NOT NULL DEFAULT '',
    source_key TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'unverified',
    provenance TEXT NOT NULL DEFAULT 'machine-extracted',
    UNIQUE (calculation_type, parameter)
);
CREATE INDEX IF NOT EXISTS idx_binding_type ON catalog_binding(calculation_type);

CREATE TABLE IF NOT EXISTS table_value (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    calculation_type TEXT NOT NULL DEFAULT '',
    parameter TEXT NOT NULL,
    clause TEXT NOT NULL DEFAULT '',
    symbol TEXT NOT NULL DEFAULT '',
    latex TEXT NOT NULL DEFAULT '',
    value NUMERIC NOT NULL,
    unit TEXT NOT NULL DEFAULT '1',
    heading_symbol TEXT NOT NULL DEFAULT '',
    heading_value NUMERIC,
    heading_unit TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'unverified',
    provenance TEXT NOT NULL DEFAULT 'machine-extracted'
);
CREATE INDEX IF NOT EXISTS idx_table_value_param ON table_value(calculation_type, parameter);

CREATE TABLE IF NOT EXISTS threshold_value (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    calculation_type TEXT NOT NULL,
    parameter TEXT NOT NULL,
    clause TEXT NOT NULL DEFAULT '',
    latex TEXT NOT NULL DEFAULT '',
    value NUMERIC NOT NULL,
    unit TEXT NOT NULL DEFAULT '1',
    status TEXT NOT NULL DEFAULT 'unverified',
    provenance TEXT NOT NULL DEFAULT 'machine-extracted',
    UNIQUE (calculation_type, parameter)
);

CREATE TABLE IF NOT EXISTS check_ref (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    calculation_type TEXT NOT NULL,
    parameter TEXT NOT NULL,
    clause TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'unverified',
    provenance TEXT NOT NULL DEFAULT 'machine-extracted',
    UNIQUE (calculation_type, parameter)
);

CREATE TABLE IF NOT EXISTS method_bound (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    calculation_type TEXT NOT NULL,
    quantity TEXT NOT NULL,
    clause TEXT NOT NULL DEFAULT '',
    kind TEXT NOT NULL,
    value NUMERIC NOT NULL,
    unit TEXT NOT NULL DEFAULT '1',
    inclusive BOOLEAN NOT NULL DEFAULT TRUE,
    status TEXT NOT NULL DEFAULT 'unverified',
    provenance TEXT NOT NULL DEFAULT 'machine-extracted'
);
CREATE INDEX IF NOT EXISTS idx_method_bound_type ON method_bound(calculation_type);
"""


def connect(url: str | None = None) -> Any:
    _url = url or os.environ.get("DEC_DATABASE_URL")
    if not _url:
        raise RuntimeError("DEC_DATABASE_URL не задан")
    return psycopg2.connect(_url, cursor_factory=RealDictCursor)


def init_schema(conn: Any) -> None:
    with conn.cursor() as cur:
        cur.execute(SCHEMA)
    conn.commit()


def document_exists(conn: Any, designation: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM document WHERE designation = %s", (designation,))
        return cur.fetchone() is not None


def fetch_document_id(conn: Any, designation: str) -> int | None:
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM document WHERE designation = %s", (designation,))
        row = cur.fetchone()
        return int(row["id"]) if row else None


def delete_document(conn: Any, designation: str) -> None:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM document WHERE designation = %s", (designation,))
    conn.commit()


def upsert_document(
    conn: Any,
    designation: str,
    title: str = "",
    edition: str = "",
    year: int | None = None,
    source_url: str = "",
) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO document (designation, title, edition, year, source_url)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (designation) DO UPDATE SET title = EXCLUDED.title
            RETURNING id
            """,
            (designation, title, edition, year, source_url),
        )
        doc_id = cur.fetchone()["id"]
    conn.commit()
    return int(doc_id)


def insert_clauses(conn: Any, doc_id: int, rows: Sequence[tuple[Any, ...]]) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO clause (document_id, number, title, page, search_text) VALUES %s",
            [(doc_id, *row) for row in rows],
        )
    conn.commit()


def insert_formulas(conn: Any, doc_id: int, rows: Sequence[tuple[Any, ...]]) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO formula
                (document_id, number, clause_number, latex, expression, raw_text, page,
                 search_text, status, provenance)
            VALUES %s
            """,
            [(doc_id, *row) for row in rows],
        )
    conn.commit()


def insert_notation(conn: Any, doc_id: int, rows: Sequence[tuple[Any, ...]]) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO notation_entry
                (document_id, formula_number, symbol, latex, meaning, unit, kind)
            VALUES %s
            """,
            [(doc_id, *row) for row in rows],
        )
    conn.commit()


def insert_cross_refs(conn: Any, doc_id: int, rows: Sequence[tuple[Any, ...]]) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO cross_ref (document_id, clause_number, ref_type, ref_value, url)
            VALUES %s
            """,
            [(doc_id, *row) for row in rows],
        )
    conn.commit()


def insert_conditions(conn: Any, doc_id: int, rows: Sequence[tuple[Any, ...]]) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO condition
                (document_id, clause_number, text, page, line, kind, status, provenance)
            VALUES %s
            """,
            [(doc_id, *row) for row in rows],
        )
    conn.commit()


def insert_coefficients(conn: Any, doc_id: int, rows: Sequence[tuple[Any, ...]]) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO coefficient
                (document_id, table_number, page, row_index, col_index, value,
                 edition, clause, status, provenance)
            VALUES %s
            """,
            [(doc_id, *row) for row in rows],
        )
    conn.commit()


def fetch_coefficients(conn: Any, doc_id: int, table_number: str) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT d.designation, c.table_number, c.page, c.row_index, c.col_index,
                   c.value, c.edition, c.clause, c.status, c.provenance
            FROM coefficient c
            JOIN document d ON d.id = c.document_id
            WHERE c.document_id = %s AND c.table_number = %s
            ORDER BY c.row_index, c.col_index
            """,
            (doc_id, table_number),
        )
        return [dict(row) for row in cur.fetchall()]


def fetch_formulas(conn: Any, doc_id: int) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, number, clause_number, page, status, provenance
            FROM formula
            WHERE document_id = %s
            ORDER BY id
            """,
            (doc_id,),
        )
        return [dict(row) for row in cur.fetchall()]


def update_formula(conn: Any, formula_id: int, latex: str, expression: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE formula SET latex = %s, expression = %s WHERE id = %s",
            (latex, expression, formula_id),
        )
    conn.commit()


def _trgm_search(
    conn: Any, table: str, alias: str, cols: str, query: str, k: int
) -> list[dict]:
    threshold = search_config()["similarity_threshold"]
    sql = f"""
        SELECT d.id AS document_id, d.designation, {cols},
               similarity({alias}.search_text, %s) AS rank
        FROM {table} {alias}
        JOIN document d ON d.id = {alias}.document_id
        WHERE similarity({alias}.search_text, %s) > %s
        ORDER BY rank DESC
        LIMIT %s
    """
    with conn.cursor() as cur:
        cur.execute(sql, (query, query, threshold, k))
        return [dict(row) for row in cur.fetchall()]


def search_formulas(conn: Any, lemmas: str, k: int = 5) -> list[dict]:
    cols = (
        "f.number, f.clause_number, f.latex, f.expression, f.raw_text, f.page, "
        "d.edition, f.status, f.provenance"
    )
    return _trgm_search(conn, "formula", "f", cols, lemmas, k)


def search_clauses(conn: Any, lemmas: str, k: int = 5) -> list[dict]:
    cols = "c.number, c.title, c.page"
    return _trgm_search(conn, "clause", "c", cols, lemmas, k)


def fetch_notation(conn: Any, doc_id: int, formula_number: str) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT symbol, latex, meaning, unit, kind
            FROM notation_entry
            WHERE document_id = %s AND formula_number = %s
            ORDER BY id
            """,
            (doc_id, formula_number),
        )
        return [dict(row) for row in cur.fetchall()]


def fetch_cross_refs(conn: Any, doc_id: int, clause_number: str) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT ref_type, ref_value, url
            FROM cross_ref
            WHERE document_id = %s AND clause_number = %s
            ORDER BY id
            """,
            (doc_id, clause_number),
        )
        return [dict(row) for row in cur.fetchall()]


def _formula_locator(formula: dict) -> str:
    cfg = output_config()
    number = formula.get("number") or ""
    clause = formula.get("clause_number") or ""
    if "#" in number or not number:
        return f"{cfg['clause_prefix']} {clause}" if clause else "unverified"
    return f"{cfg['formula_prefix']} ({number})"


def build_formula_payload(conn: Any, formula: dict) -> dict:
    cfg = output_config()

    document = formula.get("designation") or ""
    if not document:
        raise RuntimeError("формула без документа: payload не строится")

    norm_ref = {
        "document": document,
        "edition": formula.get("edition") or "unverified",
        "clause": _formula_locator(formula),
        "status": formula.get("status") or "unverified",
        "provenance": formula.get("provenance") or "machine-extracted",
    }
    for key in cfg["norm_ref_keys"]:
        if key not in norm_ref and key in formula:  # pragma: no cover
            norm_ref[key] = formula[key]

    symbols = []
    for n in fetch_notation(conn, formula["document_id"], formula["number"]):
        s = {
            "id": n["symbol"],
            "latex": n["latex"],
            "meaning": n["meaning"],
            "unit": n["unit"],
            "kind": n.get("kind") or cfg["default_symbol_kind"],
        }
        symbols.append({k: s[k] for k in cfg["symbol_keys"]})

    cross_refs = fetch_cross_refs(
        conn, formula["document_id"], formula.get("clause_number") or ""
    )

    payload = {
        "norm_ref": norm_ref,
        "formula_id": formula.get("number", ""),
        "latex": formula.get("latex") or "",
        "symbols": symbols,
        "expression": formula.get("expression", ""),
        "cross_refs": cross_refs,
    }
    return {k: payload[k] for k in cfg["formula_keys"]}


def build_coefficient_norm_ref(coefficient: dict) -> dict:
    document = coefficient.get("designation") or ""
    if not document:
        raise RuntimeError("коэффициент без документа: NormRef не строится")
    return {
        "document": document,
        "edition": coefficient.get("edition") or "unverified",
        "clause": coefficient.get("clause") or "unverified",
        "status": coefficient.get("status") or "unverified",
        "provenance": coefficient.get("provenance") or "machine-extracted",
    }


def build_coefficient_payload(coefficient: dict) -> dict:
    return {
        "table_number": coefficient.get("table_number", ""),
        "page": coefficient.get("page"),
        "row_index": coefficient["row_index"],
        "col_index": coefficient["col_index"],
        "value": coefficient["value"],
        "norm_ref": build_coefficient_norm_ref(coefficient),
    }


def fetch_formula_by_number(conn: Any, doc_id: int, number: str) -> dict | None:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, number, clause_number, latex, expression, result_symbol, page,
                   status, provenance
            FROM formula
            WHERE document_id = %s AND number = %s
            ORDER BY id
            LIMIT 1
            """,
            (doc_id, number),
        )
        row = cur.fetchone()
        return dict(row) if row else None


def set_formula_catalog(
    conn: Any,
    formula_id: int,
    result_symbol: str,
    tree: Any,
    units: Any,
    commit: bool = True,
) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE formula SET result_symbol = %s, tree = %s, units = %s,"
            " status = 'unverified', provenance = 'machine-extracted' WHERE id = %s",
            (result_symbol, Json(tree), Json(units), formula_id),
        )
    if commit:
        conn.commit()


def replace_catalog_formula(
    conn: Any,
    doc_id: int,
    number: str,
    clause_number: str,
    latex: str,
    expression: str,
    result_symbol: str,
    tree: Any,
    units: Any,
    commit: bool = True,
) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM formula WHERE document_id = %s AND number = %s",
            (doc_id, number),
        )
        cur.execute(
            """
            INSERT INTO formula
                (document_id, number, clause_number, latex, expression, result_symbol,
                 tree, units, status, provenance)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'unverified', 'machine-extracted')
            """,
            (
                doc_id, number, clause_number, latex, expression, result_symbol,
                Json(tree), Json(units),
            ),
        )
    if commit:
        conn.commit()


def delete_catalog_rows(conn: Any, calculation_type: str, commit: bool = True) -> None:
    with conn.cursor() as cur:
        for table in (
            "catalog_binding",
            "table_value",
            "threshold_value",
            "check_ref",
            "method_bound",
        ):
            cur.execute(
                f"DELETE FROM {table} WHERE calculation_type = %s", (calculation_type,)
            )
    if commit:
        conn.commit()


def insert_catalog_bindings(conn: Any, doc_id: int, rows: list[tuple], commit: bool = True) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO catalog_binding
                (calculation_type, parameter, kind, document_id, formula_number,
                 table_number, heading_symbol, source_key, status, provenance)
            VALUES %s
            """,
            [
                (
                    calculation_type, parameter, kind, doc_id, formula_number,
                    table_number, heading_symbol, source_key,
                    "unverified", "machine-extracted",
                )
                for (
                    calculation_type, parameter, kind, formula_number,
                    table_number, heading_symbol, source_key,
                ) in rows
            ],
        )
    if commit:
        conn.commit()


def insert_table_values(conn: Any, doc_id: int, rows: list[tuple], commit: bool = True) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO table_value
                (document_id, calculation_type, parameter, clause, symbol, latex, value,
                 unit, heading_symbol, heading_value, heading_unit, status, provenance)
            VALUES %s
            """,
            [(doc_id, *row, "unverified", "machine-extracted") for row in rows],
        )
    if commit:
        conn.commit()


def insert_threshold_values(conn: Any, doc_id: int, rows: list[tuple], commit: bool = True) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO threshold_value
                (document_id, calculation_type, parameter, clause, latex, value, unit,
                 status, provenance)
            VALUES %s
            """,
            [(doc_id, *row, "unverified", "machine-extracted") for row in rows],
        )
    if commit:
        conn.commit()


def insert_check_refs(conn: Any, doc_id: int, rows: list[tuple], commit: bool = True) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO check_ref
                (document_id, calculation_type, parameter, clause, status, provenance)
            VALUES %s
            """,
            [(doc_id, *row, "unverified", "machine-extracted") for row in rows],
        )
    if commit:
        conn.commit()


def insert_method_bounds(conn: Any, doc_id: int, rows: list[tuple], commit: bool = True) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO method_bound
                (document_id, calculation_type, quantity, clause, kind, value, unit,
                 inclusive, status, provenance)
            VALUES %s
            """,
            [(doc_id, *row, "unverified", "machine-extracted") for row in rows],
        )
    if commit:
        conn.commit()

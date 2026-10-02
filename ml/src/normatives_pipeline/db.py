"""Хранилище PostgreSQL: схема, низкоуровневые операции и поиск."""

from __future__ import annotations

import os
from typing import Any

import psycopg2  # type: ignore[import-untyped]
from psycopg2.extras import (  # type: ignore[import-untyped]
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
    search_text TEXT NOT NULL DEFAULT ''
);
ALTER TABLE formula ADD COLUMN IF NOT EXISTS expression TEXT NOT NULL DEFAULT '';

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

CREATE TABLE IF NOT EXISTS coefficient (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    table_number TEXT NOT NULL DEFAULT '',
    page INT,
    row_index INT NOT NULL,
    col_index INT NOT NULL,
    value TEXT NOT NULL
);

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
"""


def connect() -> Any:
    url = os.environ.get("DEC_DATABASE_URL")
    if not url:
        raise RuntimeError("DEC_DATABASE_URL не задан")
    return psycopg2.connect(url, cursor_factory=RealDictCursor)


def init_schema(conn: Any) -> None:
    with conn.cursor() as cur:
        cur.execute(SCHEMA)
    conn.commit()


def document_exists(conn: Any, designation: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM document WHERE designation = %s", (designation,))
        return cur.fetchone() is not None


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


def insert_clauses(conn: Any, doc_id: int, rows: list[tuple]) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO clause (document_id, number, title, page, search_text) VALUES %s",
            [(doc_id, *row) for row in rows],
        )
    conn.commit()


def insert_formulas(conn: Any, doc_id: int, rows: list[tuple]) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO formula
                (document_id, number, clause_number, latex, expression, raw_text, page, search_text)
            VALUES %s
            """,
            [(doc_id, *row) for row in rows],
        )
    conn.commit()


def insert_notation(conn: Any, doc_id: int, rows: list[tuple]) -> None:
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


def insert_cross_refs(conn: Any, doc_id: int, rows: list[tuple]) -> None:
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


def insert_coefficients(conn: Any, doc_id: int, rows: list[tuple]) -> None:
    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO coefficient
                (document_id, table_number, page, row_index, col_index, value)
            VALUES %s
            """,
            [(doc_id, *row) for row in rows],
        )
    conn.commit()


def fetch_coefficients(conn: Any, doc_id: int, table_number: str) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_number, page, row_index, col_index, value
            FROM coefficient
            WHERE document_id = %s AND table_number = %s
            ORDER BY row_index, col_index
            """,
            (doc_id, table_number),
        )
        return [dict(row) for row in cur.fetchall()]


def fetch_formulas(conn: Any, doc_id: int) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, number, clause_number, page
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
    cols = "f.number, f.clause_number, f.latex, f.expression, f.raw_text, f.page, d.edition"
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

    norm_ref = {
        "document": formula.get("designation", ""),
        "edition": formula.get("edition") or "unverified",
        "clause": _formula_locator(formula),
        "status": "unverified",
        "provenance": "machine-extracted",
    }
    norm_ref = {k: norm_ref[k] for k in cfg["norm_ref_keys"]}

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

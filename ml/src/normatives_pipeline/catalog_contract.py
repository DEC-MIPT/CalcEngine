"""Контракт чтения `catalog_read` (WP9, решение 1-2 design).

Схема с фиксированным набором представлений и одной функцией поиска — это единственный
способ, которым backend Акима читает `dec_normatives`. Пайплайн создаёт схему, роли и
права идемпотентно, при ingestion. Представления выполняются от владельца таблиц, поэтому
читателю достаточно `SELECT` на представления.
"""

from __future__ import annotations

import os
from typing import Any

READER_ROLE = "dec_normatives_reader"
READER_PASSWORD_VAR = "DEC_NORMATIVES_READER_PASSWORD"  # pragma: allowlist secret

_NORM_REF = """jsonb_build_array(jsonb_build_object(
        'document', d.designation,
        'edition', COALESCE(NULLIF(d.edition, ''), 'unverified'),
        'clause', COALESCE(NULLIF({clause}, ''), 'unverified'),
        'status', {status},
        'provenance', {provenance}))"""

VIEWS_SQL = f"""
CREATE SCHEMA IF NOT EXISTS catalog_read;
REVOKE ALL ON SCHEMA catalog_read FROM PUBLIC;

CREATE OR REPLACE VIEW catalog_read.documents AS
SELECT d.id AS document_id, d.designation, d.title, d.edition, d.year,
       NULLIF(d.source_url, '') AS source_url
FROM document d;

CREATE OR REPLACE VIEW catalog_read.clauses AS
SELECT c.document_id,
       (row_number() OVER (
           PARTITION BY c.document_id ORDER BY c.page NULLS FIRST, c.id))::int - 1
           AS position,
       c.number, NULLIF(c.title, '') AS title, c.page
FROM clause c;

CREATE OR REPLACE FUNCTION catalog_read.search(query text, max_rows int)
RETURNS TABLE(kind text, document_id int, designation text, edition text,
              number text, title text, rank real)
LANGUAGE sql STABLE SECURITY DEFINER SET search_path = pg_catalog, public AS $$
    SELECT h.kind, h.document_id, h.designation, h.edition, h.number, h.title, h.rank
    FROM (
        SELECT 'clause'::text AS kind, d.id AS document_id, d.designation, d.edition,
               c.number AS number, NULLIF(c.title, '') AS title,
               similarity(c.search_text, query) AS rank
        FROM clause c JOIN document d ON d.id = c.document_id
        WHERE similarity(c.search_text, query) > 0.1
        UNION ALL
        SELECT 'formula'::text, d.id, d.designation, d.edition,
               f.number, NULL::text, similarity(f.search_text, query)
        FROM formula f JOIN document d ON d.id = f.document_id
        WHERE similarity(f.search_text, query) > 0.1
        UNION ALL
        SELECT 'document'::text, d.id, d.designation, d.edition,
               NULL::text, NULLIF(d.title, ''), similarity(d.designation, query)
        FROM document d
        WHERE similarity(d.designation, query) > 0.1
    ) h
    ORDER BY h.rank DESC, h.designation COLLATE "C",
             h.number COLLATE "C" NULLS FIRST
    LIMIT max_rows
$$;

CREATE OR REPLACE VIEW catalog_read.type_formulas AS
SELECT b.calculation_type, b.parameter, f.result_symbol, f.latex, f.tree, f.units,
       {_NORM_REF.format(clause="f.clause_number", status="f.status", provenance="f.provenance")}
           AS norm_refs
FROM catalog_binding b
JOIN document d ON d.id = b.document_id
JOIN formula f ON f.document_id = b.document_id AND f.number = b.formula_number
WHERE b.kind = 'formula';

CREATE OR REPLACE VIEW catalog_read.type_table_values AS
SELECT v.calculation_type, v.parameter, v.symbol, v.latex, v.value, v.unit,
       NULLIF(v.heading_symbol, '') AS heading_symbol, v.heading_value,
       NULLIF(v.heading_unit, '') AS heading_unit,
       {_NORM_REF.format(clause="v.clause", status="v.status", provenance="v.provenance")}
           AS norm_refs
FROM table_value v JOIN document d ON d.id = v.document_id;

CREATE OR REPLACE VIEW catalog_read.type_thresholds AS
SELECT t.calculation_type, t.parameter, t.latex, t.value, t.unit,
       {_NORM_REF.format(clause="t.clause", status="t.status", provenance="t.provenance")}
           AS norm_refs
FROM threshold_value t JOIN document d ON d.id = t.document_id;

CREATE OR REPLACE VIEW catalog_read.type_checks AS
SELECT k.calculation_type, k.parameter,
       {_NORM_REF.format(clause="k.clause", status="k.status", provenance="k.provenance")}
           AS norm_refs
FROM check_ref k JOIN document d ON d.id = k.document_id;

CREATE OR REPLACE VIEW catalog_read.type_method_bounds AS
SELECT m.calculation_type, m.quantity, m.kind, m.value, m.unit, m.inclusive,
       {_NORM_REF.format(clause="m.clause", status="m.status", provenance="m.provenance")}
           AS norm_refs
FROM method_bound m JOIN document d ON d.id = m.document_id;
"""


def reader_password() -> str | None:
    """Пароль читателя из окружения (нигде не логируется)."""
    return os.environ.get(READER_PASSWORD_VAR) or None


def ensure_catalog_read(conn: Any, password: str | None = None) -> bool:
    """Создаёт схему, представления, функцию поиска и роль читателя идемпотентно.

    Args:
        conn: соединение владельца (ingestion).
        password: пароль роли читателя; при ``None`` берётся из окружения. Если пароль
            не задан, роль и права не создаются (представления создаются всегда).

    Returns:
        ``True``, если роль читателя обеспечена; иначе ``False``.
    """
    with conn.cursor() as cur:
        cur.execute(VIEWS_SQL)

    password = password if password is not None else reader_password()
    if not password:
        conn.commit()
        return False

    with conn.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM pg_roles WHERE rolname = %s", (READER_ROLE,)
        )
        if cur.fetchone() is None:
            cur.execute(f'CREATE ROLE "{READER_ROLE}" LOGIN')
        cur.execute(
            f'ALTER ROLE "{READER_ROLE}" PASSWORD %s',
            (password,),
        )
        cur.execute(f'REVOKE ALL ON SCHEMA catalog_read FROM "{READER_ROLE}"')
        cur.execute(f'GRANT USAGE ON SCHEMA catalog_read TO "{READER_ROLE}"')
        cur.execute(
            f'GRANT SELECT ON ALL TABLES IN SCHEMA catalog_read TO "{READER_ROLE}"'
        )
        cur.execute(
            f'GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA catalog_read TO "{READER_ROLE}"'
        )
        cur.execute(f'REVOKE ALL ON ALL TABLES IN SCHEMA public FROM "{READER_ROLE}"')
        cur.execute(f'REVOKE ALL ON SCHEMA public FROM "{READER_ROLE}"')
        cur.execute("REVOKE CREATE ON SCHEMA public FROM PUBLIC")
        cur.execute("REVOKE TEMP ON DATABASE dec FROM PUBLIC")
    conn.commit()
    return True

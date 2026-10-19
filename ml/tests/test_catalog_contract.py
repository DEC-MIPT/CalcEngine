"""Тесты контракта чтения `catalog_read` (WP9 2.6)."""

from __future__ import annotations

from urllib.parse import urlsplit

import psycopg2  # type: ignore[import-untyped]
import pytest
from conftest import require_test_db_url

from normatives_pipeline import catalog_contract, db

pytestmark = pytest.mark.postgres

URL = require_test_db_url()

PASSWORD = "test-reader"  # pragma: allowlist secret
TEST_READER_ROLE = "dec_catalog_test_reader"

EXPECTED = {
    "documents": [
        "document_id", "designation", "title", "edition", "year", "source_url",
    ],
    "clauses": ["document_id", "position", "number", "title", "page"],
    "type_formulas": [
        "calculation_type", "parameter", "result_symbol", "latex", "tree", "units",
        "norm_refs",
    ],
    "type_table_values": [
        "calculation_type", "parameter", "symbol", "latex", "value", "unit",
        "heading_symbol", "heading_value", "heading_unit", "norm_refs",
    ],
    "type_thresholds": [
        "calculation_type", "parameter", "latex", "value", "unit", "norm_refs",
    ],
    "type_checks": ["calculation_type", "parameter", "norm_refs"],
    "type_method_bounds": [
        "calculation_type", "quantity", "kind", "value", "unit", "inclusive",
        "norm_refs",
    ],
}


@pytest.fixture()
def conn():
    require_test_db_url()
    connection = db.connect()
    db.init_schema(connection)
    catalog_contract.ensure_catalog_read(
        connection, password=PASSWORD, role_name=TEST_READER_ROLE
    )
    yield connection
    connection.close()


def _columns(connection, name: str) -> list[str]:
    with connection.cursor() as cur:
        cur.execute(
            """
            SELECT column_name FROM information_schema.columns
            WHERE table_schema = 'catalog_read' AND table_name = %s
            ORDER BY ordinal_position
            """,
            (name,),
        )
        return [row["column_name"] for row in cur.fetchall()]


@pytest.mark.parametrize("view,columns", list(EXPECTED.items()))
def test_view_columns(conn, view: str, columns: list[str]) -> None:
    assert _columns(conn, view) == columns


def test_ingestion_twice_is_idempotent(conn) -> None:
    assert catalog_contract.ensure_catalog_read(conn, password=PASSWORD) is True
    assert _columns(conn, "type_formulas") == EXPECTED["type_formulas"]


def test_reader_password_is_not_logged(conn, caplog, capsys) -> None:
    import logging

    with caplog.at_level(logging.DEBUG):
        assert catalog_contract.ensure_catalog_read(conn, password=PASSWORD) is True
    captured = capsys.readouterr()
    assert PASSWORD not in caplog.text
    assert PASSWORD not in captured.out
    assert PASSWORD not in captured.err


def _reader_url() -> str:
    parts = urlsplit(URL)
    host = parts.hostname or "localhost"
    port = parts.port or 5432
    dbname = (parts.path or "/dec").lstrip("/")
    return f"postgresql://{TEST_READER_ROLE}:{PASSWORD}@{host}:{port}/{dbname}"


def test_search_finds_inflected_word(conn) -> None:
    """FTS with 'russian' config finds morphological variants of clause title words.

    The assertion on word_similarity proves the old trigram condition (> 0.3) would
    miss this query, so the test holds the switch to FTS.
    """
    with conn.cursor() as cur:
        cur.execute("DELETE FROM document WHERE designation = 'TEST-SEARCH-FTS'")
        cur.execute(
            "INSERT INTO document (designation, title, edition, year) "
            "VALUES ('TEST-SEARCH-FTS', 'test', '2024', 2024) RETURNING id"
        )
        doc_id = cur.fetchone()["id"]
        cur.execute(
            "INSERT INTO clause (document_id, number, title, page, search_text) "
            "VALUES (%s, '5.1', 'грунтовое основание', 1, 'грунтовый основание')",
            (doc_id,),
        )
    conn.commit()

    with conn.cursor() as cur:
        cur.execute(
            "SELECT word_similarity(%s, %s)", ("оснований", "грунтовое основание")
        )
        ws = cur.fetchone()[0]
    assert ws < 0.5, (
        f"word_similarity={ws:.3f} is too high; old code at threshold 0.3 would already "
        "find this clause — pick a word pair that better demonstrates the FTS improvement"
    )

    with conn.cursor() as cur:
        cur.execute(
            "SELECT number FROM catalog_read.search(%s, %s)", ("оснований", 50)
        )
        found = [r["number"] for r in cur.fetchall()]

    with conn.cursor() as cur:
        cur.execute(
            "SELECT number FROM catalog_read.search(%s, %s)", ("электромагнетизм", 50)
        )
        noise = [r["number"] for r in cur.fetchall()]

    with conn.cursor() as cur:
        cur.execute("DELETE FROM document WHERE designation = 'TEST-SEARCH-FTS'")
    conn.commit()

    assert "5.1" in found, "FTS must find clause by inflected form of its title word"
    assert "5.1" not in noise, "FTS must not return clause for an unrelated query"


def test_reader_role_refusals(conn) -> None:
    reader = psycopg2.connect(_reader_url())
    try:
        with reader.cursor() as cur, pytest.raises(psycopg2.Error):
            cur.execute("INSERT INTO catalog_read.documents (designation) VALUES ('x')")
        reader.rollback()
        with reader.cursor() as cur, pytest.raises(psycopg2.Error):
            cur.execute("CREATE TABLE public.hack (id int)")
        reader.rollback()
        with reader.cursor() as cur, pytest.raises(psycopg2.Error):
            cur.execute("SELECT 1 FROM public.document")
        reader.rollback()
        with reader.cursor() as cur, pytest.raises(psycopg2.Error):
            cur.execute("CREATE TEMP TABLE tmp_hack (id int)")
        reader.rollback()
        with reader.cursor() as cur:
            cur.execute("SELECT count(*) FROM catalog_read.documents")
            assert cur.fetchone()[0] >= 0
        with reader.cursor() as cur:
            cur.execute("SELECT * FROM catalog_read.search(%s, %s)", ("б", 5))
    finally:
        reader.close()

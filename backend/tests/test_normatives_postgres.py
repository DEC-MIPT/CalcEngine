import os
from collections.abc import Iterator
from typing import Any, Literal

import pytest
from catalog_fixture import (
    PLACEHOLDER_CLAUSES,
    PLACEHOLDER_DOCUMENTS,
    TEST_ROLE,
    contract_differences,
)
from fastapi.testclient import TestClient
from sqlalchemy import Engine, event, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session, sessionmaker

from app.db.catalog import CatalogSessions
from app.engine.registry import CalculatorRegistry
from app.main import create_app
from app.repositories.normatives import NormativesRepository
from app.schemas.normatives import SearchHit

pytestmark = pytest.mark.postgres

URL = os.environ.get("DEC_TEST_NORMATIVES_DATABASE_URL")

if URL is None:
    pytest.skip("DEC_TEST_NORMATIVES_DATABASE_URL is not set", allow_module_level=True)

INSUFFICIENT_PRIVILEGE = "42501"
READ_ONLY_TRANSACTION = "25006"


@pytest.fixture
def repository(catalog_postgres: Engine) -> Iterator[NormativesRepository]:
    with Session(catalog_postgres) as session:
        yield NormativesRepository(session)


@pytest.fixture
def as_reader(catalog_postgres: Engine) -> Iterator[Any]:
    """Соединение владельца, переключённое на роль-читателя синтетического контракта."""
    with catalog_postgres.connect() as connection:
        connection.execute(text(f"SET ROLE {TEST_ROLE}"))
        yield connection
        connection.rollback()


def sqlstate(error: DBAPIError) -> str | None:
    return getattr(error.orig, "sqlstate", None)


def hit(kind: Literal["document", "clause"], document: int, number: str | None, title: str | None) -> SearchHit:
    return SearchHit(
        kind=kind,
        document_id=document,
        designation=PLACEHOLDER_DOCUMENTS[document - 1],
        edition="unverified",
        number=number,
        title=title,
    )


def test_the_search_ranks_documents_before_clauses(repository: NormativesRepository) -> None:
    hits = repository.search("Синтетический", 10)

    assert hits == (
        hit("document", 2, None, "Второй синтетический документ"),
        hit("document", 1, None, "Синтетический документ об основаниях"),
        hit("clause", 2, PLACEHOLDER_CLAUSES[1], "Синтетический пункт о грунтах"),
        hit("clause", 1, PLACEHOLDER_CLAUSES[1], "Синтетический пункт об основаниях"),
        hit("clause", 1, PLACEHOLDER_CLAUSES[2], "Синтетический пункт о фундаментах"),
    )


def test_the_search_is_capped_at_max_rows(repository: NormativesRepository) -> None:
    hits = repository.search("Синтетический", 2)

    assert [found.kind for found in hits] == ["document", "document"]


def test_a_russian_word_finds_its_clause(repository: NormativesRepository) -> None:
    assert repository.search("грунтах", 10) == (hit("clause", 2, PLACEHOLDER_CLAUSES[1], "Синтетический пункт о грунтах"),)


def test_no_match_gives_no_hit(repository: NormativesRepository) -> None:
    assert repository.search("бетон", 10) == ()


def test_a_query_with_sql_syntax_is_one_statement_with_a_bound_text(
    catalog_postgres: Engine, repository: NormativesRepository
) -> None:
    hostile = "x'); DROP TABLE catalog_read.documents; --"
    statements: list[tuple[str, Any]] = []

    def capture(conn: Any, cursor: Any, statement: str, parameters: Any, context: Any, executemany: bool) -> None:
        statements.append((statement, parameters))

    event.listen(catalog_postgres, "before_cursor_execute", capture)
    try:
        hits = repository.search(hostile, 10)
    finally:
        event.remove(catalog_postgres, "before_cursor_execute", capture)

    ((statement, parameters),) = statements
    assert hits == ()
    assert hostile not in statement and "DROP" not in statement
    assert parameters == {"query": hostile, "max_rows": 10}
    assert repository.document(1) is not None


def test_the_repository_reads_numbers_and_json_from_postgres(repository: NormativesRepository) -> None:
    rows = repository.table_values("foundations_shallow_r")

    assert all(isinstance(row.value, float) for row in rows)
    assert [row.heading_value for row in rows if row.parameter == "m_q"] == [10.0, 20.0, 30.0]
    assert isinstance(repository.formulas("foundations_shallow_r")[0].tree, dict)


def test_a_write_through_the_catalog_session_is_refused(
    catalog_postgres: Engine, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert URL is not None
    monkeypatch.setenv("DEC_NORMATIVES_DATABASE_URL", URL)
    sessions = CatalogSessions()
    try:
        with sessions.factory()() as session, pytest.raises(DBAPIError) as exc_info:
            session.execute(text("DELETE FROM catalog_read.documents"))
    finally:
        sessions.dispose()

    assert sqlstate(exc_info.value) == READ_ONLY_TRANSACTION
    with catalog_postgres.connect() as connection:
        assert connection.execute(text("SELECT count(*) FROM catalog_read.documents")).scalar_one() == 2


def test_the_reader_reads_the_contract_and_calls_the_search(as_reader: Any) -> None:
    count = as_reader.execute(text("SELECT count(*) FROM catalog_read.type_formulas")).scalar_one()
    hits = as_reader.execute(text("SELECT count(*) FROM catalog_read.search('грунтах', 10)")).scalar_one()

    assert (count, hits) == (4, 1)


@pytest.mark.parametrize(
    "statement",
    [
        "SELECT * FROM public.catalog_contract_private",
        "CREATE TABLE public.catalog_contract_intruder (x integer)",
        "INSERT INTO catalog_read.documents (document_id, designation, title, edition) VALUES (9, 'x', 'x', 'x')",
        "CREATE TABLE catalog_read.intruder (x integer)",
    ],
)
def test_the_reader_is_refused_outside_its_privileges(as_reader: Any, statement: str) -> None:
    with pytest.raises(DBAPIError) as exc_info:
        as_reader.execute(text(statement))

    assert sqlstate(exc_info.value) == INSUFFICIENT_PRIVILEGE


def test_the_contract_columns_match_the_design(as_reader: Any) -> None:
    assert contract_differences(as_reader) == []


@pytest.mark.parametrize(
    ("change", "difference"),
    [
        (
            "ALTER TABLE catalog_read.type_table_values RENAME COLUMN heading_unit TO heading_units",
            ["type_table_values: missing heading_unit text", "type_table_values: unexpected heading_units text"],
        ),
        (
            "ALTER TABLE catalog_read.type_thresholds ALTER COLUMN value TYPE double precision",
            ["type_thresholds: missing value numeric", "type_thresholds: unexpected value double precision"],
        ),
        (
            "ALTER TABLE catalog_read.type_checks RENAME TO type_check",
            [
                "unexpected view type_check",
                "type_checks: missing calculation_type text",
                "type_checks: missing norm_refs jsonb",
                "type_checks: missing parameter text",
            ],
        ),
    ],
)
def test_a_changed_contract_is_reported(catalog_postgres: Engine, change: str, difference: list[str]) -> None:
    with catalog_postgres.connect() as connection:
        connection.execute(text(change))
        found = contract_differences(connection)
        connection.rollback()

    assert found == difference


def test_a_changed_search_function_is_reported(catalog_postgres: Engine) -> None:
    with catalog_postgres.connect() as connection:
        connection.execute(text("ALTER FUNCTION catalog_read.search(text, integer) RENAME TO search_all"))
        found = contract_differences(connection)
        connection.rollback()

    assert found == ["search: arguments (), results ()"]


def test_the_search_endpoint_ranks_caps_and_finds_russian_words(
    catalog_postgres: Engine, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)
    app = create_app(registry=CalculatorRegistry(), catalog_session_factory=sessionmaker(bind=catalog_postgres))

    with TestClient(app) as client:
        capped = client.get("/normatives/search", params={"q": "Синтетический", "limit": 3})
        russian = client.get("/normatives/search", params={"q": "  грунтах "})
        hostile = client.get("/normatives/search", params={"q": "x'); DROP TABLE catalog_read.documents; --"})
        document = client.get("/normatives/documents/1")

    assert [(hit["kind"], hit["document_id"], hit["number"]) for hit in capped.json()["hits"]] == [
        ("document", 2, None),
        ("document", 1, None),
        ("clause", 1, PLACEHOLDER_CLAUSES[1]),
    ]
    assert russian.json()["hits"] == [hit("clause", 2, PLACEHOLDER_CLAUSES[1], "Синтетический пункт о грунтах").model_dump()]
    assert (hostile.status_code, hostile.json()) == (200, {"hits": []})
    assert [clause["page"] for clause in document.json()["clauses"]] == [1, 2, None]

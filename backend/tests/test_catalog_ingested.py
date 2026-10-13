import os
import re
import uuid
from collections import Counter
from collections.abc import Iterator
from decimal import Decimal

import pytest
from catalog_fixture import contract_differences
from fastapi.testclient import TestClient
from sqlalchemy import Connection, Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from test_engine_foundations_shallow_r import inputs

from app.db.session import as_psycopg_url
from app.main import create_app
from app.models import Base
from app.repositories.calculation_result import CalculationResultRepository
from app.schemas.calculation import NormRef
from app.schemas.normatives import parse_norm_refs

pytestmark = pytest.mark.postgres

URL = os.environ.get("DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL")
PILOT = "foundations_shallow_r"
VIEWS = ("type_formulas", "type_table_values", "type_thresholds", "type_checks", "type_method_bounds")
WORD = re.compile(r"[А-Яа-яЁё]{6,}")
LIMIT = 50
KNOWN_MISSES = [("6.10.9", "одного")]
"""Слова, которые поиск каталога не находит, хотя выдача не заполнена.

Находка R5 третьего ревью (``normative-catalog-backend-readiness.md``, 2026-10-13):
``word_similarity > 0.3`` не связывает «одного» с леммой «один». Когда R5 исправят,
список станет пустым, и тест потребует его убрать.
"""

if URL is None:
    pytest.skip("DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL is not set", allow_module_level=True)


@pytest.fixture(scope="module")
def reader() -> Iterator[Connection]:
    """Соединение с ингестированным каталогом Егора под ролью-читателем, только для чтения.

    ``normative-catalog-backend`` tasks.md, задача 7.1: модуль ничего не пишет в каталог,
    в отличие от ``test_normatives_postgres.py``, который пересоздаёт ``catalog_read``.
    """
    assert URL is not None
    engine = create_engine(as_psycopg_url(URL))
    with engine.connect() as connection:
        yield connection
        connection.rollback()
    engine.dispose()


@pytest.fixture(scope="module")
def results() -> Iterator[Engine]:
    """База результатов в SQLite в памяти; путь ``dec_app`` в PostgreSQL проверяют тесты WP8."""
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="module")
def client(results: Engine) -> Iterator[TestClient]:
    """Клиент приложения, собранного как в работе: каталог из ``DEC_NORMATIVES_DATABASE_URL``.

    Реестр и диапазоны читаются из файлов параметров, источник параметров — каталог норм.
    """
    assert URL is not None
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("DEC_NORMATIVES_DATABASE_URL", URL)
        patch.delenv("DEC_APP_DATABASE_URL", raising=False)
        with TestClient(create_app(session_factory=sessionmaker(bind=results))) as test_client:
            yield test_client


def catalog_refs(reader: Connection) -> set[NormRef]:
    """Все ссылки, которые каталог даёт пилоту во всех своих представлениях."""
    found: set[NormRef] = set()
    for view in VIEWS:
        rows = reader.execute(
            text(f"SELECT norm_refs FROM catalog_read.{view} WHERE calculation_type = :type"), {"type": PILOT}
        )
        for (raw,) in rows:
            found.update(parse_norm_refs(raw))
    return found


def catalog_editions(reader: Connection) -> set[tuple[str, str]]:
    """Пары обозначения и редакции документов каталога."""
    rows = reader.execute(text("SELECT designation, edition FROM catalog_read.documents"))
    return {(designation, edition) for designation, edition in rows}


def test_the_ingested_catalog_matches_the_contract(reader: Connection) -> None:
    assert contract_differences(reader) == []


def test_the_pilot_runs_end_to_end_on_the_catalog(reader: Connection, client: TestClient, results: Engine) -> None:
    refs = catalog_refs(reader)
    headings: list[Decimal] = list(
        reader.execute(
            text(
                "SELECT DISTINCT heading_value FROM catalog_read.type_table_values"
                " WHERE calculation_type = :type AND heading_symbol = 'phi_II'"
            ),
            {"type": PILOT},
        ).scalars()
    )
    given = {name: value.model_dump() for name, value in inputs().items()}
    phi = min(headings, key=lambda heading: (abs(float(heading) - given["phi_II"]["value"]), heading))
    given["phi_II"] = {"value": float(phi), "unit": "deg"}

    created = client.post("/calculations", json={"calculation_type": PILOT, "inputs": given})
    envelope = created.json()
    stored = client.get(f"/calculations/{envelope['result_id']}")

    trace = envelope["trace"]
    assert created.status_code == 201
    assert {step["kind"] for step in trace} == {"formula", "table", "check"}
    assert all(set(parse_norm_refs(step["norm_refs"])) <= refs for step in trace)
    assert set(parse_norm_refs(envelope["norm_refs"])) <= refs
    with Session(results) as session:
        row = CalculationResultRepository(session).get(uuid.UUID(envelope["result_id"]))
    assert row is not None
    sources = {(source["document"], source["edition"]) for source in row.norm_sources}
    assert (stored.status_code, stored.json()) == (200, envelope)
    assert sources and sources <= catalog_editions(reader)


def found(client: TestClient, word: str) -> list[tuple[str, int, str | None]]:
    """Совпадения поиска по слову в порядке ранга: вид, документ и номер, не больше ``LIMIT``."""
    response = client.get("/normatives/search", params={"q": word, "limit": LIMIT})
    assert response.status_code == 200
    return [(hit["kind"], hit["document_id"], hit["number"]) for hit in response.json()["hits"]]


def missed(client: TestClient, document_id: int, number: str, word: str) -> bool:
    """Промах: пункта нет среди совпадений, и выдача не заполнена до ``LIMIT``.

    При заполненной выдаче частая основа («основан», «сооружен») находит больше пунктов,
    чем помещается в ответ, и пункт может стоять ниже ``LIMIT``; это не промах поиска.
    """
    hits = found(client, word)
    return ("clause", document_id, number) not in hits and len(hits) < LIMIT


def test_every_russian_word_of_a_clause_title_finds_its_clause(reader: Connection, client: TestClient) -> None:
    clauses = reader.execute(
        text("SELECT document_id, number, title FROM catalog_read.clauses WHERE title IS NOT NULL ORDER BY document_id, position")
    ).all()
    counts = Counter(word.lower() for _, _, title in clauses for word in set(WORD.findall(title)))
    words = [
        (document_id, number, word)
        for document_id, number, title in clauses
        for word in dict.fromkeys(WORD.findall(title))
        if counts[word.lower()] == 1
    ]

    misses = [(number, word) for document_id, number, word in words if missed(client, document_id, number, word)]

    assert words
    assert misses == KNOWN_MISSES, f"{len(misses)} of {len(words)} words miss their clause, first: {misses[:10]}"

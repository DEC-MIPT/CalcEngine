from collections.abc import Iterator
from typing import Any

import pytest
from catalog_fixture import (
    OTHER,
    PILOT,
    PLACEHOLDER_CLAUSES,
    PLACEHOLDER_DOCUMENTS,
    REFS,
    ROWS,
)
from pydantic import ValidationError
from sqlalchemy import Engine, event
from sqlalchemy.orm import Session

from app.repositories.normatives import NormativesRepository
from app.schemas.calculation import NormRef
from app.schemas.normatives import (
    CheckRow,
    ClauseView,
    DocumentView,
    FormulaRow,
    MethodBoundRow,
    SearchHit,
    TableValueRow,
    ThresholdRow,
    parse_norm_refs,
)

VIEWS: dict[str, tuple[str, type[Any], tuple[str, ...]]] = {
    "formulas": ("type_formulas", FormulaRow, ("parameter",)),
    "table_values": ("type_table_values", TableValueRow, ("parameter", "heading_value")),
    "thresholds": ("type_thresholds", ThresholdRow, ("parameter",)),
    "checks": ("type_checks", CheckRow, ("parameter",)),
    "method_bounds": ("type_method_bounds", MethodBoundRow, ("quantity", "kind")),
}
"""Метод репозитория → (представление, класс строки, порядок строк)."""


@pytest.fixture
def repository(catalog_sqlite: Engine) -> Iterator[NormativesRepository]:
    with Session(catalog_sqlite) as session:
        yield NormativesRepository(session)


def expected(method: str, calculation_type: str) -> list[Any]:
    view, row_class, order = VIEWS[method]
    fields = row_class.__dataclass_fields__
    rows = [
        row_class(**{key: value for key, value in row.items() if key in fields})
        for row in ROWS[view]
        if row["calculation_type"] == calculation_type
    ]
    return sorted(rows, key=lambda row: tuple(getattr(row, key) or 0 for key in order))


@pytest.mark.parametrize("method", VIEWS)
@pytest.mark.parametrize("calculation_type", [PILOT, OTHER])
def test_each_view_gives_the_rows_of_one_type(
    repository: NormativesRepository, method: str, calculation_type: str
) -> None:
    rows = getattr(repository, method)(calculation_type)

    assert list(rows) == expected(method, calculation_type)
    assert rows


@pytest.mark.parametrize("method", VIEWS)
def test_an_unknown_type_has_no_rows(repository: NormativesRepository, method: str) -> None:
    assert getattr(repository, method)("unknown_type") == ()


def test_numbers_are_floats_and_json_is_decoded(repository: NormativesRepository) -> None:
    (row, *_) = repository.table_values(PILOT)
    formula = repository.formulas(PILOT)[0]

    assert isinstance(row.value, float)
    assert row.norm_refs == REFS
    assert isinstance(formula.tree, dict) and isinstance(formula.units, dict)


def test_a_document_has_its_clauses_in_document_order(repository: NormativesRepository) -> None:
    document = repository.document(1)

    assert document == DocumentView(
        document_id=1,
        designation=PLACEHOLDER_DOCUMENTS[0],
        title="Синтетический документ об основаниях",
        edition="unverified",
        year=None,
        source_url=None,
        clauses=(
            ClauseView(number=PLACEHOLDER_CLAUSES[1], title="Синтетический пункт об основаниях", page=1),
            ClauseView(number=PLACEHOLDER_CLAUSES[2], title="Синтетический пункт о фундаментах", page=2),
            ClauseView(number=PLACEHOLDER_CLAUSES[3], title=None, page=None),
        ),
    )


def test_a_document_has_only_its_own_clauses(repository: NormativesRepository) -> None:
    document = repository.document(2)

    assert document is not None
    assert [clause.title for clause in document.clauses] == ["Синтетический пункт о грунтах"]


def test_an_unknown_document_is_none(repository: NormativesRepository) -> None:
    assert repository.document(99) is None


def test_client_values_reach_the_database_as_bound_parameters(
    catalog_sqlite: Engine, repository: NormativesRepository
) -> None:
    hostile = "x' OR '1'='1"
    statements: list[tuple[str, Any]] = []

    def capture(conn: Any, cursor: Any, statement: str, parameters: Any, context: Any, executemany: bool) -> None:
        statements.append((statement, parameters))

    event.listen(catalog_sqlite, "before_cursor_execute", capture)
    try:
        for method in VIEWS:
            assert getattr(repository, method)(hostile) == ()
        assert repository.document(-1) is None
    finally:
        event.remove(catalog_sqlite, "before_cursor_execute", capture)

    assert len(statements) == len(VIEWS) + 1
    for statement, parameters in statements:
        assert hostile not in statement and "-1" not in statement
    assert [parameters for _, parameters in statements] == [(hostile,)] * len(VIEWS) + [(-1,)]


def test_norm_refs_parse_into_references() -> None:
    assert parse_norm_refs(REFS) == (NormRef.model_validate(REFS[0]),)


@pytest.mark.parametrize(
    "raw",
    [
        [],
        None,
        "<NORM-DOC-PLACEHOLDER>",
        [{**REFS[0], "status": "verified"}],
        [{**REFS[0], "extra": "x"}],
        [{key: value for key, value in REFS[0].items() if key != "clause"}],
    ],
)
def test_invalid_norm_refs_are_refused(raw: object) -> None:
    with pytest.raises(ValidationError):
        parse_norm_refs(raw)


def test_a_search_hit_has_a_known_kind() -> None:
    hit = SearchHit(
        kind="clause", document_id=1, designation=PLACEHOLDER_DOCUMENTS[0], edition="unverified", number="1", title=None
    )

    assert hit.kind == "clause"
    with pytest.raises(ValidationError):
        SearchHit.model_validate(hit.model_dump() | {"kind": "table"})

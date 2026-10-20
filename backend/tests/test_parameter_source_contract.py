"""Одна батарея контрактных тестов для обоих источников (``interim-normatives`` "Interim parameter source contract").

Оба источника получают одни и те же данные — синтетику ``catalog_fixture.ROWS``, не
норматив: каталог — через SQLite, временный источник — теми же строками в YAML-файлах.
Тесты, которые есть только у каталога (запросы SQL, недоступное соединение), остаются в
своих модулях.
"""

from collections.abc import Callable, Iterator, Mapping, Sequence
from datetime import date
from pathlib import Path
from typing import Any

import pytest
from catalog_fixture import PILOT, REFS, ROWS, SELECTED, load_sqlite
from interim_fixture import from_catalog, manifest, write
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from test_engine_foundations_shallow_r import inputs, parameters
from test_services_catalog_source import bound, registry, with_phi

from app.core.exceptions import InputValidationError, ParameterSourceUnavailableError
from app.db.catalog import CatalogSessions
from app.engine.pipeline import calculate
from app.schemas.api import FieldError
from app.schemas.calculation import NormRef, QuantityValue
from app.services.catalog_source import CatalogParameterSource
from app.services.interim_source import interim_sources
from app.services.parameter_assembly import NO_ROW
from app.services.parameter_source import ParameterSource

Rows = Mapping[str, Sequence[Mapping[str, Any]]]
Build = Callable[[Rows], ParameterSource]
TODAY = date(2026, 10, 21)
SOURCE = (NormRef.model_validate(REFS[0]),)
KINDS = ("catalog", "interim")


@pytest.fixture(params=KINDS)
def build(request: pytest.FixtureRequest, tmp_path: Path) -> Iterator[Build]:
    """Строит источник одного вида из строк представлений каталога."""
    engines: list[Engine] = []
    roots = iter(tmp_path / f"interim-{index}" for index in range(100))

    def make(rows: Rows = ROWS) -> ParameterSource:
        if request.param == "catalog":
            engine = create_engine("sqlite://", poolclass=StaticPool)
            engines.append(engine)
            load_sqlite(engine, rows)
            return CatalogParameterSource(CatalogSessions(sessionmaker(bind=engine)), registry())
        root = next(roots)
        write(root / "doc" / "manifest.yaml", manifest())
        write(root / "doc" / f"{PILOT}.yaml", from_catalog(PILOT, rows))
        return interim_sources(registry(), root, "strict", TODAY)[PILOT]

    yield make
    for engine in engines:
        engine.dispose()


def changed(view: str, keep: Callable[[Mapping[str, Any]], bool] = lambda _: True, *extra: Mapping[str, Any]) -> Rows:
    return dict(ROWS) | {view: (*(row for row in ROWS[view] if keep(row)), *extra)}


def test_the_same_data_give_the_same_parameters_and_method_range(build: Build) -> None:
    resolved = build(ROWS).resolve(PILOT, inputs())

    assert resolved.parameters == parameters()
    assert resolved.method_range == (
        bound("b", "max", 10.0),
        bound("b", "min", 1.0),
        bound("phi_II", "max", 30.0),
        bound("phi_II", "min", 10.0),
    )


def test_both_sources_resolve_one_data_set_to_equal_results(tmp_path: Path) -> None:
    engine = create_engine("sqlite://", poolclass=StaticPool)
    load_sqlite(engine)
    write(tmp_path / "doc" / "manifest.yaml", manifest())
    write(tmp_path / "doc" / f"{PILOT}.yaml", from_catalog(PILOT))
    catalog = CatalogParameterSource(CatalogSessions(sessionmaker(bind=engine)), registry())
    interim = interim_sources(registry(), tmp_path, "strict", TODAY)[PILOT]

    for given in (inputs(), *(with_phi(phi) for phi in SELECTED), with_phi(40.0)):
        first, second = catalog.resolve(PILOT, given), interim.resolve(PILOT, given)
        assert (first.parameters, first.method_range) == (second.parameters, second.method_range)
    engine.dispose()


@pytest.mark.parametrize("phi", sorted(SELECTED))
def test_a_table_row_is_chosen_by_its_input_with_its_selector(build: Build, phi: float) -> None:
    selected: Any = build(ROWS).resolve(PILOT, with_phi(phi)).parameters

    for entry, value in zip((selected.m_gamma, selected.m_q, selected.m_c), SELECTED[phi], strict=True):
        assert entry.value == QuantityValue(value=value, unit="1")
        assert [(s.symbol, s.value) for s in entry.selectors] == [("phi_II", QuantityValue(value=phi, unit="deg"))]
        assert entry.norm_refs == SOURCE
    assert selected.gamma_c1.selectors == ()


def test_an_input_off_every_row_raises_the_same_error_without_its_value(build: Build) -> None:
    with pytest.raises(InputValidationError) as exc_info:
        build(ROWS).resolve(PILOT, with_phi(15.0))

    assert exc_info.value.fields == (FieldError(location=("body", "inputs", "phi_II"), message=NO_ROW),)
    assert "15" not in str(exc_info.value)


def test_an_input_outside_the_method_range_leads_the_engine_to_refuse_with_that_bound(build: Build) -> None:
    given = with_phi(40.0)
    resolved = build(ROWS).resolve(PILOT, given)

    result = calculate(
        registry().contract(PILOT), registry().get(PILOT), given, resolved.parameters, method_range=resolved.method_range
    )

    reason = result.model_dump()["verdict_reason"]
    assert result.verdict == "refused"
    assert (reason["kind"], reason["bound"]["quantity"], reason["bound"]["kind"]) == ("bound", "phi_II", "max")


@pytest.mark.parametrize(
    "rows",
    [
        changed("type_table_values", lambda row: row["parameter"] != "gamma_c1"),
        changed("type_thresholds", lambda _: True, ROWS["type_thresholds"][0]),
        changed("type_checks", lambda row: row["calculation_type"] != PILOT),
        changed("type_formulas", lambda _: True, {**ROWS["type_formulas"][0], "parameter": "not_in_the_model"}),
    ],
    ids=["no record", "two records", "no check", "unknown parameter"],
)
def test_a_broken_binding_makes_the_type_unavailable(build: Build, rows: Rows) -> None:
    with pytest.raises(ParameterSourceUnavailableError):
        build(rows).resolve(PILOT, inputs())

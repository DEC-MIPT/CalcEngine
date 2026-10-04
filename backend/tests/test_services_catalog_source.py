from typing import Any, Literal

import pytest
from catalog_fixture import PILOT, PLACEHOLDER_DOCUMENTS, REFS, SELECTED
from sqlalchemy import Engine, event, text
from sqlalchemy.orm import Session, sessionmaker
from test_engine_foundations_shallow_r import ROUNDING, RULE, inputs, parameters

from app.core.exceptions import InputValidationError
from app.db.catalog import CatalogSessions
from app.engine import foundations_shallow_r as pilot
from app.engine.boundary import convert
from app.engine.registry import CalculatorRegistry
from app.repositories.calculation_result import CalculationResultRepository
from app.schemas.api import FieldError
from app.schemas.calculation import (
    CalculationRequest,
    MethodBound,
    NormRef,
    QuantityValue,
)
from app.services.calculation import CalculationService
from app.services.catalog_source import NO_ROW, CatalogParameterSource

SOURCE = (NormRef.model_validate(REFS[0]),)


def registry() -> CalculatorRegistry:
    found = CalculatorRegistry()
    pilot.register(found, ROUNDING, RULE)
    return found


def make_source(engine: Engine) -> CatalogParameterSource:
    return CatalogParameterSource(CatalogSessions(sessionmaker(bind=engine)), registry())


def with_phi(value: float, unit: str = "deg") -> dict[str, QuantityValue]:
    return inputs() | {"phi_II": QuantityValue(value=value, unit=unit)}


def change(engine: Engine, statement: str) -> None:
    with engine.begin() as connection:
        connection.execute(text(statement))


def bound(quantity: str, kind: Literal["min", "max"], value: float) -> MethodBound:
    return MethodBound(quantity=quantity, kind=kind, value=value, inclusive=True, source=SOURCE)


def test_the_pilot_parameters_come_from_the_catalog(catalog_sqlite: Engine) -> None:
    resolved = make_source(catalog_sqlite).resolve(PILOT, inputs())

    assert resolved.parameters == parameters()
    assert resolved.method_range == (
        bound("b", "max", 10.0),
        bound("b", "min", 1.0),
        bound("phi_II", "max", 30.0),
        bound("phi_II", "min", 10.0),
    )


@pytest.mark.parametrize("phi", sorted(SELECTED))
def test_the_row_whose_heading_equals_the_input_is_selected(catalog_sqlite: Engine, phi: float) -> None:
    resolved = make_source(catalog_sqlite).resolve(PILOT, with_phi(phi))
    selected: Any = resolved.parameters

    for entry, value in zip((selected.m_gamma, selected.m_q, selected.m_c), SELECTED[phi], strict=True):
        assert entry.value == QuantityValue(value=value, unit="1")
        assert [(s.symbol, s.value) for s in entry.selectors] == [("phi_II", QuantityValue(value=phi, unit="deg"))]
        assert entry.norm_refs == SOURCE
    assert selected.gamma_c1.selectors == ()


def test_an_input_off_every_row_is_rejected_without_its_value(catalog_sqlite: Engine) -> None:
    with pytest.raises(InputValidationError) as exc_info:
        make_source(catalog_sqlite).resolve(PILOT, with_phi(15.0))

    assert exc_info.value.fields == (FieldError(location=("body", "inputs", "phi_II"), message=NO_ROW),)
    assert "15" not in str(exc_info.value)


def test_bounds_in_other_units_arrive_in_the_base_unit_of_their_input(catalog_sqlite: Engine) -> None:
    change(catalog_sqlite, "UPDATE catalog_read.type_method_bounds SET value = 100, unit = 'cm' WHERE quantity = 'b' AND kind = 'min'")
    change(catalog_sqlite, "UPDATE catalog_read.type_method_bounds SET value = 0.5, unit = 'rad' WHERE quantity = 'phi_II' AND kind = 'max'")

    method_range = make_source(catalog_sqlite).resolve(PILOT, inputs()).method_range

    by_side = {(found.quantity, found.kind): found.value for found in method_range}
    assert by_side[("b", "min")] == 1.0
    assert by_side[("phi_II", "max")] == convert(QuantityValue(value=0.5, unit="rad"), "deg").value


def test_a_heading_in_another_unit_selects_its_row_for_an_input_in_that_unit(catalog_sqlite: Engine) -> None:
    change(catalog_sqlite, "UPDATE catalog_read.type_table_values SET heading_value = 0.3, heading_unit = 'rad' WHERE heading_value = 20")

    selected: Any = make_source(catalog_sqlite).resolve(PILOT, with_phi(0.3, "rad")).parameters

    assert selected.m_q.value == QuantityValue(value=5.0, unit="1")
    assert selected.m_q.selectors[0].value == QuantityValue(value=0.3, unit="rad")


def test_one_resolution_reads_each_view_once(catalog_sqlite: Engine) -> None:
    statements: list[str] = []

    def capture(conn: Any, cursor: Any, statement: str, *rest: Any) -> None:
        statements.append(statement)

    event.listen(catalog_sqlite, "before_cursor_execute", capture)
    try:
        make_source(catalog_sqlite).resolve(PILOT, inputs())
    finally:
        event.remove(catalog_sqlite, "before_cursor_execute", capture)

    views = ["type_formulas", "type_table_values", "type_thresholds", "type_checks", "type_method_bounds"]
    assert len(statements) == 5
    assert [next(view for view in views if f"catalog_read.{view}" in statement) for statement in statements] == views


def test_the_service_runs_the_pilot_on_catalog_data(catalog_sqlite: Engine, sqlite_session: Session) -> None:
    service = CalculationService(
        registry(),
        sources={PILOT: make_source(catalog_sqlite)},
        results=CalculationResultRepository(sqlite_session),
    )

    envelope = service.submit(CalculationRequest(calculation_type=PILOT, inputs=inputs()))

    assert envelope.verdict == "pass"
    assert envelope.outputs[0].value == 172.5
    assert {ref.document for step in envelope.trace for ref in step.norm_refs} == {PLACEHOLDER_DOCUMENTS[0]}
    assert [(s.symbol, s.value) for s in envelope.trace[4].substitutions] == [("phi_II", 20.0)]

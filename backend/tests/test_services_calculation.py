from collections.abc import Iterator, Mapping
from itertools import count
from typing import Any
from uuid import UUID

import pytest
from pydantic import BaseModel

from app.core.exceptions import CalculationError, NotFoundError
from app.engine.base import Calculator
from app.engine.pipeline import CalculatorOutput, calculate
from app.engine.registry import CalculatorRegistry
from app.engine.steps import check_step, formula_step
from app.schemas.calculation import (
    CalculationResult,
    CalculationTypeContract,
    MethodBound,
    NormRef,
    OutputDeclaration,
    QuantityDeclaration,
    QuantityValue,
    RoundingRule,
)
from app.schemas.expression import parse_expression
from app.schemas.parameters import EngineerRule
from app.schemas.resolved import Formula
from app.services.calculation import CalculationService

REF = NormRef(
    document="<NORM-DOC-PLACEHOLDER>",
    edition="unverified",
    clause="<CLAUSE-PLACEHOLDER>",
    status="unverified",
    provenance="machine-extracted",
)
RULE = EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>")

CONTRACT = CalculationTypeContract(
    name="synthetic",
    inputs=(QuantityDeclaration(name="b", base_unit="m"),),
    outputs=(
        OutputDeclaration(
            name="y", base_unit="m", rounding_rule=RoundingRule(decimals=2, mode="half_up"), rounding_source=RULE
        ),
    ),
    checks=("check",),
)


class SyntheticParameters(BaseModel):
    formula: Formula
    limit: QuantityValue


PARAMETERS = SyntheticParameters(
    formula=Formula(
        latex=r"y = 2 b",
        tree=parse_expression(
            {"kind": "mul", "left": {"kind": "number", "value": 2}, "right": {"kind": "symbol", "name": "b"}}
        ),
        result_symbol="y",
        units={"b": "m", "y": "m"},
        norm_refs=(REF,),
    ),
    limit=QuantityValue(value=10.0, unit="m"),
)


class SyntheticCalculator(Calculator[Mapping[str, QuantityValue], SyntheticParameters, CalculatorOutput]):
    def calculate(
        self, inputs: Mapping[str, QuantityValue], parameters: SyntheticParameters
    ) -> CalculatorOutput:
        y = formula_step("y", parameters.formula, inputs)
        check = check_step("check", ("y", y.result), "le", ("y_{max}", parameters.limit), (REF,))
        return CalculatorOutput(trace=(y, check), outputs={"y": y.result})


class WrongCalculator(Calculator[Mapping[str, QuantityValue], Any, Any]):
    def calculate(self, inputs: Mapping[str, QuantityValue], parameters: Any) -> Any:
        return "not an output"


def ids() -> Iterator[UUID]:
    for number in count(1):
        yield UUID(int=number)


@pytest.fixture
def service() -> CalculationService:
    registry = CalculatorRegistry()
    registry.register(CONTRACT, SyntheticCalculator())
    registry.register(CONTRACT.model_copy(update={"name": "wrong"}), WrongCalculator())
    return CalculationService(registry, new_id=ids().__next__)


def b(value: float, unit: str = "m") -> dict[str, QuantityValue]:
    return {"b": QuantityValue(value=value, unit=unit)}


def test_two_envelopes_from_identical_results_differ_only_in_result_id(
    service: CalculationService,
) -> None:
    result = calculate(CONTRACT, SyntheticCalculator(), b(1.2345), PARAMETERS)

    first, second = service.envelope(result), service.envelope(result)

    assert first.result_id != second.result_id
    for envelope in (first, second):
        assert CalculationResult.model_validate(envelope.model_dump(exclude={"result_id"})) == result


def test_the_service_runs_a_registered_type_and_assigns_a_result_id(
    service: CalculationService,
) -> None:
    envelope = service.run("synthetic", b(1234.5, "mm"), PARAMETERS)

    assert envelope.result_id == UUID(int=1)
    assert envelope.verdict == "pass"
    assert [(o.quantity, o.value, o.unit) for o in envelope.outputs] == [("y", 2.47, "m")]
    assert envelope.trace[0].substitutions[0].value == 1.2345
    assert len(envelope.input_hash) == 64


def test_the_service_returns_a_refusal_as_an_envelope(service: CalculationService) -> None:
    bound = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(REF,))

    envelope = service.run("synthetic", b(2.0), PARAMETERS, method_range=(bound,))

    assert envelope.verdict == "refused"
    assert (envelope.trace, envelope.outputs) == ((), ())
    assert envelope.result_id == UUID(int=1)


def test_identical_runs_give_envelopes_equal_except_result_id(
    service: CalculationService,
) -> None:
    first = service.run("synthetic", b(1.2345), PARAMETERS)
    second = service.run("synthetic", b(1.2345), PARAMETERS)

    assert first.result_id != second.result_id
    assert first.model_dump(exclude={"result_id"}) == second.model_dump(exclude={"result_id"})


def test_an_unknown_calculation_type_fails(service: CalculationService) -> None:
    with pytest.raises(NotFoundError):
        service.run("missing", b(1.0), PARAMETERS)


def test_a_calculator_that_does_not_return_its_output_fails(service: CalculationService) -> None:
    with pytest.raises(CalculationError, match="not a CalculatorOutput"):
        service.run("wrong", b(1.0), PARAMETERS)

from collections.abc import Mapping
from typing import Any

import pytest
from pydantic import BaseModel
from test_verification_models import example_data

from app.core.exceptions import ParameterSourceUnavailableError
from app.engine.base import Calculator
from app.engine.pipeline import CalculatorOutput
from app.engine.registry import CalculatorRegistry
from app.engine.steps import check_step, formula_step
from app.schemas.calculation import (
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
from app.schemas.text import LocalizedText
from app.verification.models import ExpectedOutput, ReferenceExample
from app.verification.runner import ExampleParameters, run_suite, within_tolerance

TYPE = "synthetic_verification_type"
REF = NormRef(
    document="<NORM-DOC-PLACEHOLDER>",
    edition="unverified",
    clause="<CLAUSE-PLACEHOLDER>",
    status="unverified",
    provenance="machine-extracted",
)
RULE = EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>")
CONTRACT = CalculationTypeContract(
    name=TYPE,
    inputs=(
        QuantityDeclaration(name="b", label=LocalizedText(ru="b"), symbol="b", base_unit="m"),
        QuantityDeclaration(name="q", label=LocalizedText(ru="q"), symbol="q", base_unit="1"),
    ),
    outputs=(
        OutputDeclaration(
            name="y",
            label=LocalizedText(ru="y"),
            symbol="y",
            base_unit="m",
            rounding_rule=RoundingRule(decimals=3, mode="half_even"),
            rounding_source=RULE,
        ),
    ),
    checks=("check",),
)


class Parameters(BaseModel):
    formula: Formula
    limit: QuantityValue


PARAMETERS = Parameters(
    formula=Formula(
        latex="y = b q",
        tree=parse_expression(
            {"kind": "mul", "left": {"kind": "symbol", "name": "b"}, "right": {"kind": "symbol", "name": "q"}}
        ),
        result_symbol="y",
        units={"b": "m", "q": "1", "y": "m"},
        norm_refs=(REF,),
    ),
    limit=QuantityValue(value=100.0, unit="m"),
)
METHOD = (MethodBound(quantity="b", kind="max", value=50.0, inclusive=True, source=(REF,)),)


class SyntheticCalculator(Calculator[Mapping[str, QuantityValue], Parameters, CalculatorOutput]):
    def calculate(self, inputs: Mapping[str, QuantityValue], parameters: Parameters) -> CalculatorOutput:
        y = formula_step("y", parameters.formula, {"b": inputs["b"], "q": inputs["q"]})
        check = check_step("check", ("y", y.result), "le", ("y_{max}", parameters.limit), (REF,))
        return CalculatorOutput(trace=(y, check), outputs={"y": y.result})


def registry() -> CalculatorRegistry:
    built = CalculatorRegistry()
    built.register(CONTRACT, SyntheticCalculator())
    return built


def resolve(example: ReferenceExample) -> ExampleParameters:
    return ExampleParameters(parameters=PARAMETERS, method_range=METHOD)


def output(value: float, unit: str = "m", tolerance: float = 0.01, kind: str = "absolute") -> dict[str, Any]:
    return {
        "value": value,
        "unit": unit,
        "tolerance": tolerance,
        "tolerance_kind": kind,
        "tolerance_source": {"engineer": "<ENGINEER>", "rationale": "<RATIONALE>"},
    }


def example(example_id: str = "ex", b: float = 2.0, q: float = 3.0, **outputs: dict[str, Any]) -> ReferenceExample:
    return ReferenceExample.model_validate(
        example_data(
            example_id=example_id,
            inputs={"b": {"value": b, "unit": "m"}, "q": {"value": q, "unit": "1"}},
            expected_outputs=outputs or {"y": output(6.0)},
        )
    )


def test_every_output_within_its_tolerance_gives_go() -> None:
    report = run_suite([example("ex1"), example("ex2", b=4.0, y=output(12.0))], registry(), resolve)

    assert report.verdict == "GO"
    assert [(run.example_id, run.outcome) for run in report.runs] == [("ex1", "passed"), ("ex2", "passed")]
    assert report.failures == ()
    check = report.runs[0].checks[0]
    assert (check.quantity, check.computed, check.outcome) == ("y", QuantityValue(value=6.0, unit="m"), "within")


def test_an_output_outside_its_tolerance_gives_no_go_naming_the_example_and_the_quantity() -> None:
    report = run_suite([example("ex1"), example("ex2", y=output(6.5, tolerance=0.25))], registry(), resolve)

    assert report.verdict == "NO-GO"
    assert [run.outcome for run in report.runs] == ["passed", "failed"]
    ((example_id, check),) = report.failures
    assert (example_id, check.quantity, check.outcome) == ("ex2", "y", "outside")
    assert check.computed == QuantityValue(value=6.0, unit="m")
    assert (check.expected.value, check.expected.unit, check.expected.tolerance) == (6.5, "m", 0.25)


@pytest.mark.parametrize(
    ("expected", "within"),
    [
        (output(6.5, tolerance=0.5), True),
        (output(5.5, tolerance=0.5), True),
        (output(6.5, tolerance=0.25), False),
        (output(5.0, tolerance=0.2, kind="relative"), True),
        (output(5.0, tolerance=0.1, kind="relative"), False),
        (output(6.0, tolerance=0.0), True),
    ],
    ids=["absolute at the upper edge", "absolute at the lower edge", "absolute outside", "relative at the edge", "relative outside", "exact"],
)
def test_the_tolerance_rule_of_the_requirement_includes_its_edge(expected: dict[str, Any], within: bool) -> None:
    report = run_suite([example(y=expected)], registry(), resolve)

    assert (report.verdict == "GO") is within


def test_an_absolute_tolerance_applies_in_the_unit_of_the_expected_value() -> None:
    inside = run_suite([example(y=output(6001.0, unit="mm", tolerance=1.0))], registry(), resolve)
    outside = run_suite([example(y=output(6001.0, unit="mm", tolerance=0.5))], registry(), resolve)

    assert inside.verdict == "GO"
    assert inside.runs[0].checks[0].computed == QuantityValue(value=6000.0, unit="mm")
    assert outside.verdict == "NO-GO"


def test_a_relative_tolerance_uses_the_absolute_expected_value() -> None:
    expected = ExpectedOutput.model_validate(output(-10.0, tolerance=0.1, kind="relative"))

    assert within_tolerance(-9.0, expected)
    assert not within_tolerance(-8.5, expected)


def test_an_expected_quantity_the_result_does_not_hold_fails_the_example() -> None:
    report = run_suite([example(y=output(6.0), z=output(1.0))], registry(), resolve)

    assert report.verdict == "NO-GO"
    assert [(check.quantity, check.outcome) for check in report.runs[0].checks] == [("y", "within"), ("z", "missing")]
    ((_, missing),) = report.failures
    assert missing.computed is None


def test_an_expected_value_in_a_unit_of_another_dimension_fails_the_example() -> None:
    report = run_suite([example(y=output(6.0, unit="kPa"))], registry(), resolve)

    assert report.verdict == "NO-GO"
    check = report.runs[0].checks[0]
    assert (check.outcome, check.computed) == ("incompatible_unit", None)


def test_a_refused_calculation_fails_the_example() -> None:
    report = run_suite([example("far", b=60.0, y=output(180.0))], registry(), resolve)

    assert report.verdict == "NO-GO"
    run = report.runs[0]
    assert run.outcome == "refused"
    assert [check.outcome for check in run.checks] == ["missing"]


def test_an_unregistered_calculation_type_fails_the_example_as_an_error() -> None:
    unknown = example().model_copy(update={"calculation_type": "not_registered"})

    report = run_suite([unknown], registry(), resolve)

    assert report.verdict == "NO-GO"
    run = report.runs[0]
    assert (run.outcome, run.error, run.checks) == ("error", "NotFoundError", ())


def test_a_parameter_source_error_fails_the_example_as_an_error() -> None:
    def unavailable(example: ReferenceExample) -> ExampleParameters:
        raise ParameterSourceUnavailableError("no source")

    report = run_suite([example()], registry(), unavailable)

    assert (report.verdict, report.runs[0].outcome, report.runs[0].error) == (
        "NO-GO",
        "error",
        "ParameterSourceUnavailableError",
    )


def test_the_resolver_receives_each_example() -> None:
    seen: list[str] = []

    def recording(example: ReferenceExample) -> ExampleParameters:
        seen.append(example.example_id)
        return resolve(example)

    run_suite([example("a"), example("b")], registry(), recording)

    assert seen == ["a", "b"]

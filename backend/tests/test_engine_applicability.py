from collections.abc import Mapping
from typing import Any

import pytest

from app.core.exceptions import CalculationError
from app.engine.applicability import check_applicability, is_inside
from app.engine.base import Calculator
from app.engine.boundary import run
from app.engine.result import assemble_result
from app.schemas.calculation import (
    CalculationTypeContract,
    MethodBound,
    NormRef,
    OutputDeclaration,
    QuantityDeclaration,
    QuantityValue,
    RoundingRule,
    ValidatedBound,
)
from app.schemas.parameters import EngineerRule
from app.schemas.text import LocalizedText


def ref(clause: str) -> NormRef:
    return NormRef(
        document="<NORM-DOC-PLACEHOLDER>",
        edition="unverified",
        clause=clause,
        status="unverified",
        provenance="machine-extracted",
    )


A, B = ref("<CLAUSE-A>"), ref("<CLAUSE-B>")
RULE = EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>")

CONTRACT = CalculationTypeContract(
    name="synthetic",
    inputs=(
        QuantityDeclaration(name="b", label=LocalizedText(ru="b"), symbol="b", base_unit="m"),
        QuantityDeclaration(name="p", label=LocalizedText(ru="p"), symbol="p", base_unit="kPa"),
    ),
    outputs=(
        OutputDeclaration(
            name="y",
            label=LocalizedText(ru="y"),
            symbol="y",
            base_unit="m",
            rounding_rule=RoundingRule(decimals=2, mode="half_up"),
            rounding_source=RULE,
        ),
    ),
    checks=("check",),
)


def method(quantity: str, kind: str, value: float, *, inclusive: bool = True, source: Any = (A,)) -> MethodBound:
    return MethodBound.model_validate(
        {"quantity": quantity, "kind": kind, "value": value, "inclusive": inclusive, "source": source}
    )


def validated(quantity: str, kind: str, value: float, *, inclusive: bool = True) -> ValidatedBound:
    return ValidatedBound.model_validate(
        {"quantity": quantity, "kind": kind, "value": value, "inclusive": inclusive, "source": RULE}
    )


METHOD = (method("b", "max", 10.0),)
VALIDATED = (validated("b", "max", 5.0),)


class SpyCalculator(Calculator[Mapping[str, QuantityValue], None, str]):
    def __init__(self) -> None:
        self.calls = 0

    def calculate(self, inputs: Mapping[str, QuantityValue], parameters: None) -> str:
        self.calls += 1
        return "ran"


def q(value: float, unit: str) -> QuantityValue:
    return QuantityValue(value=value, unit=unit)


def inputs(b: float, p: float = 100.0, b_unit: str = "m") -> dict[str, QuantityValue]:
    return {"b": q(b, b_unit), "p": q(p, "kPa")}


def test_inside_both_ranges_the_calculation_runs_without_a_warning() -> None:
    calculator = SpyCalculator()

    outcome = run(
        CONTRACT, calculator, inputs(3.0), None, method_range=METHOD, validated_range=VALIDATED
    )

    assert (outcome.result, outcome.refusal, outcome.warnings) == ("ran", None, ())
    assert calculator.calls == 1


def test_outside_the_method_range_the_calculation_is_refused_naming_the_bound() -> None:
    calculator = SpyCalculator()

    outcome = run(
        CONTRACT, calculator, inputs(12.0), None, method_range=METHOD, validated_range=VALIDATED
    )

    assert outcome.result is None
    assert outcome.refusal is not None
    assert outcome.refusal.bound == METHOD[0]
    assert outcome.refusal.bound.source == (A,)
    assert outcome.refusal.value == q(12.0, "m")
    assert calculator.calls == 0


def test_outside_the_validated_range_the_calculation_runs_with_a_warning() -> None:
    calculator = SpyCalculator()

    outcome = run(
        CONTRACT, calculator, inputs(7.0), None, method_range=METHOD, validated_range=VALIDATED
    )

    assert (outcome.result, outcome.refusal) == ("ran", None)
    (warning,) = outcome.warnings
    assert (warning.value, warning.bound, warning.bound.source) == (q(7.0, "m"), VALIDATED[0], RULE)
    assert calculator.calls == 1


def test_a_refusal_keeps_the_validated_range_warnings() -> None:
    outcome = run(
        CONTRACT, SpyCalculator(), inputs(12.0), None, method_range=METHOD, validated_range=VALIDATED
    )

    assert [warning.bound for warning in outcome.warnings] == [VALIDATED[0]]


def test_the_check_reads_inputs_in_their_base_units() -> None:
    outcome = run(CONTRACT, SpyCalculator(), inputs(12_000.0, b_unit="mm"), None, method_range=METHOD)

    assert outcome.refusal is not None
    assert outcome.refusal.value == q(12.0, "m")


@pytest.mark.parametrize(
    "kind,inclusive,inside",
    [("max", True, True), ("max", False, False), ("min", True, True), ("min", False, False)],
)
def test_an_input_equal_to_a_bound_is_inside_only_if_the_bound_includes_it(
    kind: str, inclusive: bool, inside: bool
) -> None:
    assert is_inside(10.0, method("b", kind, 10.0, inclusive=inclusive)) is inside
    assert is_inside(10.0, validated("b", kind, 10.0, inclusive=inclusive)) is inside


@pytest.mark.parametrize("inclusive,refused", [(True, False), (False, True)])
def test_an_input_equal_to_a_bound_of_the_method_range(inclusive: bool, refused: bool) -> None:
    outcome = run(
        CONTRACT,
        SpyCalculator(),
        inputs(10.0),
        None,
        method_range=(method("b", "max", 10.0, inclusive=inclusive),),
    )

    assert (outcome.refusal is not None) is refused


@pytest.mark.parametrize("inclusive,warned", [(True, False), (False, True)])
def test_an_input_equal_to_a_bound_of_the_validated_range(inclusive: bool, warned: bool) -> None:
    outcome = run(
        CONTRACT,
        SpyCalculator(),
        inputs(5.0),
        None,
        validated_range=(validated("b", "min", 5.0, inclusive=inclusive),),
    )

    assert bool(outcome.warnings) is warned


def test_two_violated_bounds_are_refused_by_the_one_declared_first() -> None:
    on_b, on_p = method("b", "max", 10.0, source=(A,)), method("p", "max", 100.0, source=(B,))
    values = {"b": q(12.0, "m"), "p": q(150.0, "kPa")}

    first, _ = check_applicability(values, (on_b, on_p), ())
    second, _ = check_applicability(values, (on_p, on_b), ())

    assert first is not None and first.bound == on_b
    assert second is not None and second.bound == on_p


def test_warnings_follow_the_declared_order_of_the_validated_range() -> None:
    on_p, on_b = validated("p", "max", 50.0), validated("b", "max", 5.0)

    _, warnings = check_applicability({"b": q(7.0, "m"), "p": q(60.0, "kPa")}, (), (on_p, on_b))

    assert [warning.bound for warning in warnings] == [on_p, on_b]


def test_a_refused_outcome_becomes_a_refused_envelope() -> None:
    outcome = run(
        CONTRACT, SpyCalculator(), inputs(12.0), None, method_range=METHOD, validated_range=VALIDATED
    )
    assert outcome.refusal is not None

    result = assemble_result(
        CONTRACT,
        input_hash="0" * 64,
        trace=(),
        outputs=(),
        warnings=outcome.warnings,
        validated_range=VALIDATED,
        refusal=outcome.refusal,
    )

    assert result.verdict == "refused"
    assert result.norm_refs == (A,)
    assert result.engineer_rules == (RULE,)


@pytest.mark.parametrize(
    "method_range,validated_range,match",
    [
        ((method("z", "max", 1.0),), (), "not an input"),
        ((), (validated("z", "max", 1.0),), "not an input"),
        ((method("b", "min", 5.0), method("b", "max", 1.0)), (), "is empty"),
        ((), (validated("b", "max", 5.0), validated("b", "max", 6.0)), "two max bounds"),
    ],
)
def test_a_range_that_does_not_fit_the_inputs_fails(
    method_range: tuple[MethodBound, ...], validated_range: tuple[ValidatedBound, ...], match: str
) -> None:
    with pytest.raises(CalculationError, match=match):
        check_applicability(inputs(1.0), method_range, validated_range)

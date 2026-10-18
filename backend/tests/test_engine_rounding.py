import sys

import pytest
from pydantic import ValidationError

from app.engine.boundary import make_outputs
from app.engine.result import assemble_result
from app.engine.steps import check_step, formula_step
from app.schemas.calculation import (
    MAX_DECIMALS,
    CalculationTypeContract,
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

REF = NormRef(
    document="<NORM-DOC-PLACEHOLDER>",
    edition="unverified",
    clause="<CLAUSE-PLACEHOLDER>",
    status="unverified",
    provenance="machine-extracted",
)
RULE = EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>")


def rule(decimals: int, mode: str) -> RoundingRule:
    return RoundingRule.model_validate({"decimals": decimals, "mode": mode})


@pytest.mark.parametrize(
    "value,decimals,half_up,half_even",
    [(2.5, 0, 3.0, 2.0), (0.125, 2, 0.13, 0.12), (1.2345, 3, 1.235, 1.234), (-2.5, 0, -3.0, -2.0)],
)
def test_a_tie_rounds_differently_in_half_up_and_half_even(
    value: float, decimals: int, half_up: float, half_even: float
) -> None:
    assert rule(decimals, "half_up").apply(value) == half_up
    assert rule(decimals, "half_even").apply(value) == half_even


def test_rounding_reads_the_shortest_decimal_of_the_float() -> None:
    assert round(2.675, 2) == 2.67
    assert rule(2, "half_up").apply(2.675) == 2.68


@pytest.mark.parametrize("mode", ["half_up", "half_even"])
def test_a_value_that_is_not_a_tie_rounds_to_the_nearest(mode: str) -> None:
    assert rule(1, mode).apply(7.46) == 7.5
    assert rule(0, mode).apply(7.44) == 7.0


def test_a_check_whose_outcome_would_change_on_the_rounded_value_uses_the_unrounded_value() -> None:
    contract = CalculationTypeContract(
        name="synthetic",
        inputs=(QuantityDeclaration(name="a", label=LocalizedText(ru="a"), symbol="a", base_unit="kPa"),),
        outputs=(
            OutputDeclaration(
                name="y",
                label=LocalizedText(ru="y"),
                symbol="y", base_unit="kPa", rounding_rule=rule(2, "half_up"), rounding_source=RULE
            ),
        ),
        checks=("check",),
    )
    formula = Formula(
        latex=r"y = a",
        tree=parse_expression({"kind": "symbol", "name": "a"}),
        result_symbol="y",
        units={"a": "kPa", "y": "kPa"},
        norm_refs=(REF,),
    )
    y = formula_step("y", formula, {"a": QuantityValue(value=4.996, unit="kPa")})
    limit = QuantityValue(value=4.999, unit="kPa")
    check = check_step("check", ("y", y.result), "le", ("y_{lim}", limit), (REF,))

    result = assemble_result(
        contract,
        input_hash="0" * 64,
        trace=(y, check),
        outputs=make_outputs(contract, {"y": y.result}),
        warnings=(),
        validated_range=(),
    )

    assert result.outputs[0].value == 5.0
    assert result.outputs[0].value > limit.value
    assert check.result.value == 4.996
    assert (check.passed, result.verdict) == (True, "pass")


def test_the_decimals_are_bounded_at_an_implementation_limit() -> None:
    assert rule(MAX_DECIMALS, "half_up").decimals == 15

    with pytest.raises(ValidationError):
        rule(MAX_DECIMALS + 1, "half_up")


@pytest.mark.parametrize(
    ("value", "decimals", "expected"),
    [
        (1e30, 2, 1e30),
        (-1e30, 2, -1e30),
        (1e300, 0, 1e300),
        (sys.float_info.max, MAX_DECIMALS, sys.float_info.max),
        (-sys.float_info.max, 0, -sys.float_info.max),
        (1.5, MAX_DECIMALS, 1.5),
        (1e-300, MAX_DECIMALS, 0.0),
    ],
)
def test_any_finite_value_is_rounded_without_an_invalid_operation(
    value: float, decimals: int, expected: float
) -> None:
    assert rule(decimals, "half_up").apply(value) == expected


def test_a_large_value_keeps_its_rounding() -> None:
    assert rule(1, "half_up").apply(123456789012345.67) == 123456789012345.7

import pytest

from app.reporting.format import (
    UNIT_DESIGNATIONS,
    check_rounding,
    format_norm_ref,
    format_number,
    latex_number,
    latex_quantity,
)
from app.schemas.calculation import (
    CheckStep,
    NormRef,
    QuantityValue,
    RoundingRule,
    Substitution,
)
from app.schemas.units import UNITS


@pytest.mark.parametrize(
    ("value", "text"),
    [
        (172.5, "172,5"),
        (1e-07, "0,0000001"),
        (2.0, "2"),
        (100.0, "100"),
        (1e20, "100000000000000000000"),
        (0.1 + 0.2, "0,30000000000000004"),
        (-3.25, "-3,25"),
        (-0.0, "0"),
    ],
)
def test_a_number_is_the_shortest_decimal_without_an_exponent_with_a_comma(value: float, text: str) -> None:
    assert format_number(value) == text


HUNDREDTHS = RoundingRule(decimals=2, mode="half_up")


@pytest.mark.parametrize(
    ("value", "decimals", "text"),
    [(172.5, 2, "172,50"), (168.29, 2, "168,29"), (0.0, 2, "0,00"), (-0.0, 1, "0,0"), (2.0, 0, "2"), (0.125, 1, "0,125")],
)
def test_a_number_is_padded_to_the_given_decimals(value: float, decimals: int, text: str) -> None:
    assert format_number(value, decimals) == text


@pytest.mark.parametrize(("value", "text"), [(172.5, "172{,}5"), (2.0, "2"), (-3.25, "-3{,}25")])
def test_a_latex_number_keeps_its_comma_in_braces(value: float, text: str) -> None:
    assert latex_number(value) == text


@pytest.mark.parametrize(
    ("value", "unit", "text"),
    [
        (172.5, "kPa", r"172{,}5\ \text{кПа}"),
        (1e-07, "m", r"0{,}0000001\ \text{м}"),
        (2.0, "1", "2"),
        (20.0, "deg", r"20^{\circ}"),
    ],
)
def test_a_latex_quantity_prints_with_the_russian_designation_of_its_unit(value: float, unit: str, text: str) -> None:
    assert latex_quantity(QuantityValue(value=value, unit=unit)) == text


@pytest.mark.parametrize(
    ("value", "text"), [(168.28900000000002, r"168{,}29\ \text{кПа}"), (172.5, r"172{,}50\ \text{кПа}")]
)
def test_an_output_value_prints_rounded_with_exactly_its_decimals(value: float, text: str) -> None:
    assert latex_quantity(QuantityValue(value=value, unit="kPa"), HUNDREDTHS) == text


UNVERIFIED = NormRef(
    document="<DOC>", edition="unverified", clause="<CLAUSE>", status="unverified", provenance="machine-extracted"
)


def check(result: float, right: float, passed: bool) -> CheckStep:
    return CheckStep(
        step_id="check",
        expression=r"y \le y_{lim}",
        substitutions=(
            Substitution(symbol="y", value=result, unit="kPa"),
            Substitution(symbol="y_lim", value=right, unit="kPa"),
        ),
        result=QuantityValue(value=result, unit="kPa"),
        operator="le",
        right=QuantityValue(value=right, unit="kPa"),
        passed=passed,
        norm_refs=(UNVERIFIED,),
    )


def test_a_check_side_that_is_an_output_follows_its_rule() -> None:
    assert check_rounding(check(100.0, 168.289, True), {"y_lim": HUNDREDTHS}) == (None, HUNDREDTHS)
    assert check_rounding(check(100.0, 168.289, True), {}) == (None, None)


def test_a_check_prints_unrounded_when_rounding_would_contradict_its_outcome() -> None:
    assert check_rounding(check(4.996, 4.999, True), {"y": HUNDREDTHS}) == (None, None)


def test_every_unit_of_the_vocabulary_has_a_russian_designation() -> None:
    assert set(UNIT_DESIGNATIONS) == set(UNITS)
    assert [unit for unit, designation in UNIT_DESIGNATIONS.items() if not designation] == ["1"]


def test_a_norm_ref_prints_with_its_status_and_unverified_parts() -> None:
    unverified = NormRef(
        document="<DOC>", edition="unverified", clause="<CLAUSE>", status="unverified", provenance="machine-extracted"
    )
    verified = NormRef(document="<DOC>", edition="<ED>", clause="<CLAUSE>", status="verified", provenance="human-verified")

    assert format_norm_ref(unverified) == "<DOC>, редакция: не проверено, пункт: <CLAUSE> (статус: не проверено)"
    assert format_norm_ref(verified) == "<DOC>, редакция: <ED>, пункт: <CLAUSE> (статус: проверено)"
    assert format_norm_ref(unverified, status=False) == "<DOC>, редакция: не проверено, пункт: <CLAUSE>"

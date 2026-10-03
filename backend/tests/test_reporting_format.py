import pytest

from app.reporting.format import (
    UNIT_DESIGNATIONS,
    format_norm_ref,
    format_number,
    format_quantity,
)
from app.schemas.calculation import NormRef, QuantityValue
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


@pytest.mark.parametrize(
    ("value", "unit", "text"),
    [(172.5, "kPa", "172,5 кПа"), (1e-07, "m", "0,0000001 м"), (2.0, "1", "2"), (20.0, "deg", "20°")],
)
def test_a_quantity_prints_with_the_russian_designation_of_its_unit(value: float, unit: str, text: str) -> None:
    assert format_quantity(QuantityValue(value=value, unit=unit)) == text


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

from typing import Any

import pytest
from pydantic import ValidationError

from app.schemas.calculation import NormRef, QuantityValue
from app.schemas.parameters import EngineerRule
from app.verification.models import ExpectedOutput, ReferenceExample, SourceCitation

SYNTHETIC_TYPE = "synthetic_verification_type"
REF = {
    "document": "<NORM-DOC-PLACEHOLDER>",
    "edition": "unverified",
    "clause": "<CLAUSE-PLACEHOLDER>",
    "status": "unverified",
    "provenance": "machine-extracted",
}
RULE = {"engineer": "<ENGINEER>", "rationale": "<RATIONALE>"}


def example_data(**changes: Any) -> dict[str, Any]:
    """Синтетический эталонный пример в том виде, в каком его прочитали бы из файла.

    Args:
        changes: поля, которые заменяют значения по умолчанию.

    Returns:
        Словарь полей примера.
    """
    data: dict[str, Any] = {
        "example_id": "synthetic-ex1",
        "calculation_type": SYNTHETIC_TYPE,
        "inputs": {"a": {"value": 2.0, "unit": "m"}, "q": {"value": 3.0, "unit": "kPa"}},
        "expected_outputs": {
            "y": {
                "value": 6.0,
                "unit": "kN",
                "tolerance": 0.01,
                "tolerance_kind": "absolute",
                "tolerance_source": RULE,
            }
        },
        "origin": "textbook",
        "citation": {"document": "<GUIDE-PLACEHOLDER>", "year": 2000, "locator": "p. 1, example 1"},
        "source_norm_edition": "unverified",
    }
    return data | changes


def test_a_complete_example_keeps_every_field_of_the_requirement() -> None:
    example = ReferenceExample.model_validate(example_data())

    assert example.example_id == "synthetic-ex1"
    assert example.calculation_type == SYNTHETIC_TYPE
    assert example.inputs == {
        "a": QuantityValue(value=2.0, unit="m"),
        "q": QuantityValue(value=3.0, unit="kPa"),
    }
    expected = example.expected_outputs["y"]
    assert isinstance(expected, ExpectedOutput)
    assert (expected.value, expected.unit, expected.tolerance, expected.tolerance_kind) == (6.0, "kN", 0.01, "absolute")
    assert expected.tolerance_source == EngineerRule(**RULE)
    assert example.origin == "textbook"
    assert example.citation == SourceCitation(document="<GUIDE-PLACEHOLDER>", year=2000, locator="p. 1, example 1")
    assert example.source_norm_edition == "unverified"


def test_a_tolerance_source_may_be_norm_references() -> None:
    output = example_data()["expected_outputs"]["y"] | {"tolerance_kind": "relative", "tolerance_source": [REF]}

    example = ReferenceExample.model_validate(example_data(expected_outputs={"y": output}))

    expected = example.expected_outputs["y"]
    assert expected.tolerance_kind == "relative"
    assert expected.tolerance_source == (NormRef.model_validate(REF),)


@pytest.mark.parametrize("origin", ["manual calculation", "textbook", "norm application"])
def test_each_origin_of_the_requirement_is_accepted(origin: str) -> None:
    assert ReferenceExample.model_validate(example_data(origin=origin)).origin == origin


def test_a_zero_tolerance_is_allowed() -> None:
    output = example_data()["expected_outputs"]["y"] | {"tolerance": 0.0}

    example = ReferenceExample.model_validate(example_data(expected_outputs={"y": output}))

    assert example.expected_outputs["y"].tolerance == 0.0


def test_an_example_is_immutable() -> None:
    example = ReferenceExample.model_validate(example_data())

    with pytest.raises(ValidationError):
        example.example_id = "other"

from typing import Any

import pytest
from pydantic import ValidationError

from app.parameters.param_schemas import ParameterFileSchema
from app.schemas.calculation import MethodBound, NormRef, check_bounds

SOURCE = {"engineer": "И. И. Иванов", "rationale": "..."}


def bound(kind: str, value: float, inclusive: bool = True, quantity: str = "depth") -> dict[str, Any]:
    return {
        "quantity": quantity,
        "kind": kind,
        "value": value,
        "inclusive": inclusive,
        "source": SOURCE,
    }


def schema(*bounds: dict[str, Any]) -> ParameterFileSchema:
    return ParameterFileSchema.model_validate({"validated_range": list(bounds)})


def test_validated_range_accepts_min_only() -> None:
    (lower,) = schema(bound("min", 0.5)).validated_range
    assert (lower.kind, lower.value) == ("min", 0.5)


def test_validated_range_accepts_max_only() -> None:
    (upper,) = schema(bound("max", 5.0)).validated_range
    assert (upper.kind, upper.value) == ("max", 5.0)


def test_no_validated_range_at_all_is_an_empty_list() -> None:
    assert ParameterFileSchema.model_validate({}).validated_range == ()


def test_validated_range_keeps_its_declared_order() -> None:
    bounds = schema(bound("max", 5.0), bound("min", 0.5), bound("min", 1.0, quantity="width"))

    assert [(b.quantity, b.kind) for b in bounds.validated_range] == [
        ("depth", "max"),
        ("depth", "min"),
        ("width", "min"),
    ]


def test_validated_range_rejects_min_greater_than_max() -> None:
    with pytest.raises(ValidationError, match="is empty"):
        schema(bound("min", 5.0), bound("max", 0.5))


def test_a_single_point_range_needs_both_bounds_inclusive() -> None:
    assert len(schema(bound("min", 1.0), bound("max", 1.0)).validated_range) == 2
    with pytest.raises(ValidationError, match="is empty"):
        schema(bound("min", 1.0, inclusive=False), bound("max", 1.0))


def test_a_quantity_has_one_bound_of_each_kind() -> None:
    with pytest.raises(ValidationError, match="two min bounds"):
        schema(bound("min", 0.5), bound("min", 1.0))


def test_bounds_of_different_quantities_are_independent() -> None:
    bounds = schema(bound("min", 5.0), bound("max", 0.5, quantity="width"))

    assert len(bounds.validated_range) == 2


@pytest.mark.parametrize("missing", ["engineer", "rationale"])
def test_a_bound_in_the_file_names_its_engineer_and_rationale(missing: str) -> None:
    source = dict(SOURCE)
    del source[missing]

    with pytest.raises(ValidationError):
        schema(bound("min", 0.5) | {"source": source})


def test_a_bound_from_the_norm_does_not_belong_in_the_file() -> None:
    reference = {
        "document": "<NORM-DOC-PLACEHOLDER>",
        "edition": "unverified",
        "clause": "<CLAUSE-PLACEHOLDER>",
        "status": "unverified",
        "provenance": "machine-extracted",
    }

    with pytest.raises(ValidationError):
        schema(bound("min", 0.5) | {"source": [reference]})


def test_the_old_validated_ranges_key_is_rejected() -> None:
    with pytest.raises(ValidationError):
        ParameterFileSchema.model_validate(
            {"validated_ranges": {"depth": {"min_value": 0.5, **SOURCE}}}
        )


def test_check_bounds_applies_to_the_method_range_too() -> None:
    reference = NormRef(
        document="<NORM-DOC-PLACEHOLDER>",
        edition="unverified",
        clause="<CLAUSE-PLACEHOLDER>",
        status="unverified",
        provenance="machine-extracted",
    )
    lower = MethodBound(quantity="b", kind="min", value=2.0, inclusive=True, source=(reference,))
    upper = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(reference,))

    check_bounds((lower,))
    with pytest.raises(ValueError, match="is empty"):
        check_bounds((lower, upper))

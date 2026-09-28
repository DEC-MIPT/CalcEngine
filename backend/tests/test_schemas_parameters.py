import pytest
from pydantic import ValidationError

from app.schemas.parameters import ValidatedRange

ENGINEER = "И. И. Иванов"
RATIONALE = "..."


def test_validated_range_accepts_min_only() -> None:
    value = ValidatedRange(engineer=ENGINEER, rationale=RATIONALE, min_value=0.5)
    assert value.min_value == 0.5
    assert value.max_value is None


def test_validated_range_accepts_max_only() -> None:
    value = ValidatedRange(engineer=ENGINEER, rationale=RATIONALE, max_value=5.0)
    assert value.max_value == 5.0
    assert value.min_value is None


def test_validated_range_rejects_no_bound_at_all() -> None:
    with pytest.raises(ValidationError, match="needs min_value, max_value, or both"):
        ValidatedRange(engineer=ENGINEER, rationale=RATIONALE)


def test_validated_range_rejects_min_greater_than_max() -> None:
    with pytest.raises(ValidationError, match="min_value must not be greater than max_value"):
        ValidatedRange(
            engineer=ENGINEER, rationale=RATIONALE, min_value=5.0, max_value=0.5
        )

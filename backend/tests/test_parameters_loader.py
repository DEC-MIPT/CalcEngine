from pathlib import Path

import pytest

from app.core.exceptions import DECError
from app.parameters.loader import load_parameters
from app.schemas.parameters import RoundingRule, ValidatedRange

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "params"


def test_load_parameters_returns_typed_values() -> None:
    parameters = load_parameters("foundations_r", FIXTURES_DIR)

    rounding_rule = parameters.rounding_rules["R"]
    assert isinstance(rounding_rule, RoundingRule)
    assert rounding_rule.decimals == 2
    assert rounding_rule.engineer == "И. И. Иванов"

    validated_range = parameters.validated_ranges["depth"]
    assert isinstance(validated_range, ValidatedRange)
    assert validated_range.min_value == 0.5
    assert validated_range.max_value == 5.0


def test_unknown_key_is_rejected_with_a_dec_error() -> None:
    with pytest.raises(DECError):
        load_parameters("unknown_key", FIXTURES_DIR)


def test_missing_engineer_fields_are_rejected_with_a_dec_error() -> None:
    with pytest.raises(DECError):
        load_parameters("missing_rationale", FIXTURES_DIR)


def test_missing_file_raises_a_dec_error() -> None:
    with pytest.raises(DECError):
        load_parameters("does_not_exist", FIXTURES_DIR)

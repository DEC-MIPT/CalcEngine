from pathlib import Path

import pytest

from app.core.exceptions import DECError, ParameterValidationError
from app.parameters.loader import load_parameters
from app.parameters.param_schemas import EngineerBound, RoundingEntry

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "params"


def test_load_parameters_returns_typed_values() -> None:
    parameters = load_parameters("foundations_r", FIXTURES_DIR)

    rounding = parameters.rounding_rules["R"]
    assert isinstance(rounding, RoundingEntry)
    assert (rounding.rule.decimals, rounding.rule.mode) == (2, "half_up")
    assert rounding.source.engineer == "И. И. Иванов"

    lower, upper = parameters.validated_range
    assert isinstance(lower, EngineerBound)
    assert (lower.quantity, lower.kind, lower.value, lower.inclusive) == ("depth", "min", 0.5, True)
    assert (upper.kind, upper.value) == ("max", 5.0)
    assert upper.source.engineer == "И. И. Иванов"


def test_unknown_key_is_rejected_with_a_dec_error() -> None:
    with pytest.raises(DECError):
        load_parameters("unknown_key", FIXTURES_DIR)


@pytest.mark.parametrize("calculation_type", ["missing_rationale", "missing_engineer"])
def test_missing_engineer_fields_are_rejected_with_a_dec_error(
    calculation_type: str,
) -> None:
    with pytest.raises(ParameterValidationError):
        load_parameters(calculation_type, FIXTURES_DIR)


@pytest.mark.parametrize("calculation_type", ["missing_mode", "flat_rounding"])
def test_a_rounding_rule_without_its_mode_or_separate_source_is_rejected(
    calculation_type: str,
) -> None:
    with pytest.raises(ParameterValidationError):
        load_parameters(calculation_type, FIXTURES_DIR)


def test_malformed_yaml_is_rejected_with_a_dec_error() -> None:
    with pytest.raises(ParameterValidationError):
        load_parameters("malformed", FIXTURES_DIR)


def test_missing_file_raises_a_dec_error() -> None:
    with pytest.raises(DECError):
        load_parameters("does_not_exist", FIXTURES_DIR)

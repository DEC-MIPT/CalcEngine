from pathlib import Path
from typing import Any

import pytest
import yaml

from app.parameters.loader import load_parameters

PARAMS_ROOT = Path(__file__).resolve().parents[1] / "params"

ALLOWED_KEYS = {
    "rounding_rules",
    "validated_range",
    "rule",
    "source",
    "decimals",
    "mode",
    "engineer",
    "rationale",
    "quantity",
    "kind",
    "value",
    "inclusive",
}


FORBIDDEN_WORDS = ("formula", "coefficient", "tree", "latex", "expression")


def format_keys(data: Any, quantity_names: bool = False) -> set[str]:
    """Все ключи формата файла; имена выходов под ``rounding_rules`` пропускаются."""
    if isinstance(data, dict):
        found: set[str] = set()
        for key, value in data.items():
            if not quantity_names:
                found.add(key)
            found |= format_keys(value, quantity_names=key == "rounding_rules")
        return found
    if isinstance(data, list):
        return set().union(*(format_keys(item) for item in data))
    return set()


@pytest.mark.parametrize(
    "calculation_type", sorted(path.stem for path in PARAMS_ROOT.glob("*.yaml"))
)
def test_every_parameter_file_validates_against_the_engineer_set_schema(
    calculation_type: str,
) -> None:
    load_parameters(calculation_type, PARAMS_ROOT)


def test_the_pilot_file_validates() -> None:
    parameters = load_parameters("foundations_shallow_r", PARAMS_ROOT)

    rounding = parameters.rounding_rules["R"]
    assert (rounding.rule.decimals, rounding.rule.mode) == (2, "half_up")
    assert rounding.source.engineer and rounding.source.rationale
    assert parameters.validated_range == ()


def test_the_pilot_file_contains_no_formula_or_coefficient_key() -> None:
    raw = yaml.safe_load((PARAMS_ROOT / "foundations_shallow_r.yaml").read_text(encoding="utf-8"))

    found = format_keys(raw)

    assert found <= ALLOWED_KEYS
    assert not [key for key in found if any(word in key.lower() for word in FORBIDDEN_WORDS)]


def test_format_keys_reads_nested_keys_and_skips_output_names() -> None:
    raw = {"rounding_rules": {"R": {"rule": {"formula": 1}}}, "validated_range": [{"kind": "min"}]}

    assert format_keys(raw) == {"rounding_rules", "rule", "formula", "validated_range", "kind"}

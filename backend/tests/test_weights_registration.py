import json
from datetime import date
from pathlib import Path

import pytest
import yaml

from app.core.config import INTERIM_ROOT, PARAMS_ROOT
from app.core.exceptions import (
    CalculationError,
    ParameterSourceUnavailableError,
    ParameterValidationError,
)
from app.engine import foundations_shallow_loads as loads
from app.engine import foundations_shallow_weights as weights
from app.engine.legacy_module import LegacyOptions
from app.engine.registry import CalculatorRegistry
from app.parameters.loader import load_parameters
from app.services.catalog import build_registry
from app.services.interim_source import interim_sources

FIXTURE = Path(__file__).parent / "fixtures" / "foundations_weights_references.json"


def given() -> dict:
    from app.schemas.calculation import QuantityValue

    return {name: QuantityValue.model_validate(value) for name, value in json.loads(FIXTURE.read_text())[0]["inputs"].items()}


def test_default_registry_and_strict_prepared_source_execute_new_type_without_a_weight_thickness() -> None:
    registry = build_registry(PARAMS_ROOT)
    source = interim_sources(registry, INTERIM_ROOT, "strict", date(2026, 11, 22))[weights.NAME]
    resolved = source.resolve(weights.NAME, given())
    outcome = registry.module(weights.NAME).execute_public(given(), resolved.parameters, LegacyOptions(method_range=resolved.method_range))
    assert next(output.value for output in outcome.outputs if output.quantity == "p") == 120
    assert len(registry.contract(weights.NAME).inputs) == 19
    assert resolved.source is not None and resolved.source.kind == "interim"
    assert all(reference.status == "unverified" for reference in outcome.norm_refs)


def test_weight_source_missing_components_fail_closed(tmp_path: Path) -> None:
    registry = build_registry(PARAMS_ROOT)
    source = interim_sources(registry, tmp_path, "strict", date(2026, 11, 22))[weights.NAME]
    with pytest.raises(ParameterSourceUnavailableError):
        source.resolve(weights.NAME, given())


def test_registration_requires_rounding_for_every_output(tmp_path: Path) -> None:
    for path in PARAMS_ROOT.glob("*.yaml"):
        (tmp_path / path.name).write_bytes(path.read_bytes())
    path = tmp_path / f"{weights.NAME}.yaml"
    content = yaml.safe_load(path.read_text())
    del content["rounding_rules"]["p_corner_mm"]
    path.write_text(yaml.safe_dump(content, allow_unicode=True))
    with pytest.raises(ParameterValidationError, match="p_corner_mm"):
        build_registry(tmp_path)


def test_module_registration_rejects_wrong_registry_or_partial_output_configuration() -> None:
    entries = load_parameters(weights.NAME, PARAMS_ROOT).rounding_rules
    with pytest.raises(CalculationError, match="registry"):
        weights.register(object(), entries)
    with pytest.raises(CalculationError, match="rounding entry"):
        weights.register(CalculatorRegistry(), {"R": entries["R"]})


def test_new_input_symbols_are_valid_grouped_tex_and_the_transfer_hint_names_no_removed_field() -> None:
    inputs = {item.name: item for item in weights.INPUTS}
    assert inputs["G_fund"].symbol == "G_{fund}"
    assert inputs["Mx_add_base"].symbol == "M_{x,add,base}"
    assert inputs["My_add_base"].symbol == "M_{y,add,base}"
    assert inputs["h"].hint is not None and "d и" not in inputs["h"].hint.ru
    assert "d" not in inputs
    assert "d" in {item.name for item in loads.INPUTS}


def test_new_type_obeys_loaded_method_bound_before_pressure_steps() -> None:
    from app.schemas.calculation import QuantityValue

    registry = build_registry(PARAMS_ROOT)
    source = interim_sources(registry, INTERIM_ROOT, "strict", date(2026, 11, 22))[weights.NAME]
    inputs = given() | {"d_b": QuantityValue(value=3, unit="m")}
    resolved = source.resolve(weights.NAME, inputs)
    outcome = registry.module(weights.NAME).execute_public(inputs, resolved.parameters, LegacyOptions(method_range=resolved.method_range))
    assert outcome.verdict == "refused"
    assert outcome.verdict_reason.kind == "bound"
    assert outcome.verdict_reason.bound.quantity == "d_b"
    assert outcome.trace == () and outcome.outputs == ()

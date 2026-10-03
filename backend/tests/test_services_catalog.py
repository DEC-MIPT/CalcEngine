from pathlib import Path

import pytest

from app.core.exceptions import DECError
from app.engine import foundations_shallow_r
from app.engine.base import Calculator
from app.engine.registry import CalculatorRegistry
from app.parameters.loader import load_parameters
from app.schemas.api import CalculationTypeView, InputView, OutputView
from app.schemas.calculation import (
    CalculationTypeContract,
    OutputDeclaration,
    QuantityDeclaration,
    RoundingRule,
)
from app.schemas.parameters import EngineerRule
from app.schemas.units import Dimension
from app.services.catalog import build_registry, calculation_types

PARAMS_ROOT = Path(__file__).resolve().parents[1] / "params"
FILE_NAME = f"{foundations_shallow_r.NAME}.yaml"

VALID_RULE = """\
rounding_rules:
  R:
    rule:
      decimals: 1
      mode: half_up
    source:
      engineer: "<ENGINEER>"
      rationale: "<RATIONALE>"
"""


class IdentityCalculator(Calculator[float, float, float]):
    def calculate(self, inputs: float, parameters: float) -> float:
        return inputs


def synthetic_contract(name: str) -> CalculationTypeContract:
    return CalculationTypeContract(
        name=name,
        inputs=(QuantityDeclaration(name="x", base_unit="m"),),
        outputs=(
            OutputDeclaration(
                name="y",
                base_unit="m",
                rounding_rule=RoundingRule(decimals=2, mode="half_up"),
                rounding_source=EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>"),
            ),
        ),
        checks=("c",),
    )


def write_params(root: Path, text: str) -> Path:
    path = root / FILE_NAME
    path.write_text(text, encoding="utf-8")
    return path


def test_the_pilot_is_registered_with_the_rounding_of_its_parameter_file() -> None:
    expected = load_parameters(foundations_shallow_r.NAME, PARAMS_ROOT).rounding_rules["R"]

    contract = build_registry(PARAMS_ROOT).contract(foundations_shallow_r.NAME)

    (output,) = contract.outputs
    assert output.name == "R"
    assert output.rounding_rule == expected.rule
    assert isinstance(output.rounding_source, EngineerRule)
    assert output.rounding_source == expected.source
    assert output.rounding_source.engineer
    assert output.rounding_source.rationale


def test_a_missing_parameter_file_names_the_file(tmp_path: Path) -> None:
    with pytest.raises(DECError, match=FILE_NAME):
        build_registry(tmp_path)


def test_a_file_that_is_not_yaml_names_the_file(tmp_path: Path) -> None:
    write_params(tmp_path, "rounding_rules: [unclosed\n")

    with pytest.raises(DECError, match=FILE_NAME):
        build_registry(tmp_path)


@pytest.mark.parametrize("missing", ["engineer", "rationale"])
def test_a_rounding_rule_without_its_source_names_the_file_and_the_output(
    tmp_path: Path, missing: str
) -> None:
    text = "\n".join(line for line in VALID_RULE.splitlines() if missing not in line)
    write_params(tmp_path, text)

    with pytest.raises(DECError) as raised:
        build_registry(tmp_path)

    assert FILE_NAME in str(raised.value)
    assert f"rounding_rules.R.source.{missing}" in str(raised.value)


def test_a_file_without_a_rule_for_r_names_the_file_and_the_output(tmp_path: Path) -> None:
    write_params(tmp_path, VALID_RULE.replace("  R:", "  X:"))

    with pytest.raises(DECError) as raised:
        build_registry(tmp_path)

    assert FILE_NAME in str(raised.value)
    assert "'R'" in str(raised.value)


def test_a_valid_file_in_another_root_is_used(tmp_path: Path) -> None:
    write_params(tmp_path, VALID_RULE)

    contract = build_registry(tmp_path).contract(foundations_shallow_r.NAME)

    assert contract.outputs[0].rounding_source == EngineerRule(
        engineer="<ENGINEER>", rationale="<RATIONALE>"
    )


def test_the_pilot_view_lists_inputs_and_outputs_in_contract_order() -> None:
    (view,) = calculation_types(build_registry(PARAMS_ROOT))

    assert view.name == foundations_shallow_r.NAME
    assert [item.name for item in view.inputs] == [q.name for q in foundations_shallow_r.INPUTS]
    assert [item.base_unit for item in view.inputs] == [
        q.base_unit for q in foundations_shallow_r.INPUTS
    ]
    assert view.outputs == (OutputView(name="R", base_unit="kPa"),)


def test_the_view_takes_each_dimension_from_the_unit_vocabulary() -> None:
    (view,) = calculation_types(build_registry(PARAMS_ROOT))

    dimensions = {item.name: item.dimension for item in view.inputs}
    assert dimensions["b"] is Dimension.LENGTH
    assert dimensions["gamma_II"] is Dimension.SPECIFIC_WEIGHT
    assert dimensions["c_II"] is Dimension.PRESSURE
    assert dimensions["phi_II"] is Dimension.ANGLE


def test_the_view_leaves_out_rounding_checks_and_sources() -> None:
    (view,) = calculation_types(build_registry(PARAMS_ROOT))

    assert set(view.model_dump()) == {"name", "inputs", "outputs"}
    assert set(view.outputs[0].model_dump()) == {"name", "base_unit"}


def test_an_empty_registry_has_no_types() -> None:
    assert calculation_types(CalculatorRegistry()) == ()


def test_types_are_listed_in_registration_order() -> None:
    registry = CalculatorRegistry()
    registry.register(synthetic_contract("second"), IdentityCalculator())
    registry.register(synthetic_contract("first"), IdentityCalculator())

    views = calculation_types(registry)

    assert [view.name for view in views] == ["second", "first"]
    assert views[0] == CalculationTypeView(
        name="second",
        inputs=(InputView(name="x", base_unit="m", dimension=Dimension.LENGTH),),
        outputs=(OutputView(name="y", base_unit="m"),),
    )

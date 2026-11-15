from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from app.core.exceptions import ContractMetadataError
from app.engine import foundations_shallow_r as pilot
from app.engine.base import Calculator
from app.engine.registry import CalculatorRegistry
from app.main import create_app
from app.schemas.calculation import (
    CalculationTypeContract,
    OutputDeclaration,
    QuantityDeclaration,
    RoundingRule,
)
from app.schemas.parameters import EngineerRule
from app.schemas.text import LocalizedText
from app.services.catalog import build_registry, calculation_types

PARAMS_ROOT = Path(__file__).resolve().parents[1] / "params"
ROUNDING = RoundingRule(decimals=2, mode="half_up")
RULE = EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>")


class IdentityCalculator(Calculator[float, float, float]):
    def calculate(self, inputs: float, parameters: float) -> float:
        return inputs


def contract(
    input_changes: dict[str, Any] | None = None, output_changes: dict[str, Any] | None = None
) -> CalculationTypeContract:
    quantity: dict[str, Any] = {"label": LocalizedText(ru="x"), "symbol": "x"}
    result: dict[str, Any] = {"label": LocalizedText(ru="y"), "symbol": "y"}
    return CalculationTypeContract(
        name="t",
        inputs=(QuantityDeclaration(name="x", base_unit="m", **(quantity | (input_changes or {}))),),
        outputs=(
            OutputDeclaration(
                name="y",
                base_unit="m",
                rounding_rule=ROUNDING,
                rounding_source=RULE,
                **(result | (output_changes or {})),
            ),
        ),
        checks=("c",),
    )


@pytest.mark.parametrize(
    ("input_changes", "output_changes", "problem"),
    [
        ({"label": None}, None, "input 'x' has no label.ru"),
        ({"label": LocalizedText(ru="")}, None, "input 'x' has no label.ru"),
        ({"label": LocalizedText(ru="  ")}, None, "input 'x' has no label.ru"),
        ({"symbol": None}, None, "input 'x' has no symbol"),
        ({"symbol": ""}, None, "input 'x' has no symbol"),
        ({"hint": LocalizedText(ru="")}, None, "input 'x' has a hint without hint.ru"),
        (None, {"label": None}, "output 'y' has no label.ru"),
        (None, {"symbol": " "}, "output 'y' has no symbol"),
    ],
    ids=[
        "no-label",
        "empty-label-ru",
        "blank-label-ru",
        "no-symbol",
        "empty-symbol",
        "empty-hint-ru",
        "output-no-label",
        "output-blank-symbol",
    ],
)
def test_a_type_without_label_or_symbol_is_not_registered_and_the_quantity_is_named(
    input_changes: dict[str, Any] | None, output_changes: dict[str, Any] | None, problem: str
) -> None:
    registry = CalculatorRegistry()

    with pytest.raises(ContractMetadataError, match=problem):
        registry.register(contract(input_changes, output_changes), IdentityCalculator())

    assert registry.contracts() == ()


def test_every_problem_of_a_type_is_named_at_once() -> None:
    with pytest.raises(ContractMetadataError) as caught:
        CalculatorRegistry().register(
            contract({"label": None, "symbol": None}, {"label": None}), IdentityCalculator()
        )

    assert [part.strip() for part in str(caught.value).split(":", 1)[1].split(";")] == [
        "input 'x' has no label.ru",
        "input 'x' has no symbol",
        "output 'y' has no label.ru",
    ]


def test_hint_and_english_text_are_optional() -> None:
    registry = CalculatorRegistry()

    registry.register(contract(), IdentityCalculator())

    (declared,) = registry.contract("t").inputs
    assert declared.hint is None
    assert declared.label is not None and declared.label.en is None
    assert declared.whole_values_only is False


def test_an_english_text_may_not_be_empty() -> None:
    with pytest.raises(ValidationError):
        LocalizedText(ru="x", en="")


def test_an_output_has_no_hint_and_no_whole_values_flag() -> None:
    with pytest.raises(ValidationError, match="may not have a hint or whole_values_only"):
        contract(output_changes={"hint": LocalizedText(ru="y")})
    with pytest.raises(ValidationError, match="may not have a hint or whole_values_only"):
        contract(output_changes={"whole_values_only": True})


def test_a_bare_declaration_cannot_describe_itself() -> None:
    with pytest.raises(ContractMetadataError, match="'x'"):
        QuantityDeclaration(name="x", base_unit="m").described()


def test_every_quantity_of_the_pilot_has_a_russian_label_and_a_symbol() -> None:
    registry = build_registry(PARAMS_ROOT)
    declared = registry.contract(pilot.NAME)

    assert declared.metadata_problems() == ()
    for quantity in (*declared.inputs, *declared.outputs):
        label, symbol = quantity.described()
        assert label.ru and symbol


def test_only_phi_ii_takes_whole_values() -> None:
    declared = build_registry(PARAMS_ROOT).contract(pilot.NAME)

    assert {quantity.name for quantity in declared.inputs if quantity.whole_values_only} == {"phi_II"}


def test_the_listing_carries_the_metadata_in_the_declared_order() -> None:
    view = calculation_types(build_registry(PARAMS_ROOT))[0]

    by_name = {item.name: item for item in view.inputs}
    assert [item.name for item in view.inputs] == [quantity.name for quantity in pilot.INPUTS]
    assert by_name["phi_II"].whole_values_only is True
    assert by_name["b"].whole_values_only is False
    assert by_name["phi_II"].symbol == r"\varphi_{II}"
    assert by_name["phi_II"].hint is not None and by_name["b"].hint is None
    assert [item.name for item in view.outputs] == ["R"]


def test_the_openapi_description_documents_the_metadata() -> None:
    schemas = create_app(registry=build_registry(PARAMS_ROOT)).openapi()["components"]["schemas"]

    assert {"label", "symbol", "hint", "whole_values_only"} <= set(schemas["InputView"]["properties"])
    assert {"label", "symbol"} <= set(schemas["OutputView"]["properties"])
    assert "whole_values_only" not in schemas["OutputView"]["properties"]

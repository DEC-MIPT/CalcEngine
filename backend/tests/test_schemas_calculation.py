import pytest
from pydantic import ValidationError

from app.schemas.calculation import CalculationTypeContract, QuantityDeclaration


def quantity(name: str, unit: str = "m") -> QuantityDeclaration:
    return QuantityDeclaration(name=name, base_unit=unit)


def test_contract_holds_quantities_with_base_units() -> None:
    contract = CalculationTypeContract(
        name="t", inputs=(quantity("b"), quantity("d", "kPa")), outputs=(quantity("r"),)
    )

    assert [(q.name, q.base_unit) for q in contract.inputs] == [("b", "m"), ("d", "kPa")]


@pytest.mark.parametrize("field", ["inputs", "outputs"])
def test_contract_needs_at_least_one_quantity_on_each_side(field: str) -> None:
    sides: dict[str, tuple[QuantityDeclaration, ...]] = {
        "inputs": (quantity("a"),),
        "outputs": (quantity("b"),),
    }
    sides[field] = ()

    with pytest.raises(ValidationError):
        CalculationTypeContract(name="t", **sides)


@pytest.mark.parametrize("field", ["inputs", "outputs"])
def test_quantity_names_must_be_unique_within_a_side(field: str) -> None:
    sides: dict[str, tuple[QuantityDeclaration, ...]] = {
        "inputs": (quantity("a"),),
        "outputs": (quantity("b"),),
    }
    sides[field] = (quantity("x"), quantity("x", "kPa"))

    with pytest.raises(ValidationError):
        CalculationTypeContract(name="t", **sides)


def test_same_name_on_both_sides_is_allowed() -> None:
    contract = CalculationTypeContract(
        name="t", inputs=(quantity("x"),), outputs=(quantity("x"),)
    )

    assert contract.inputs[0].name == contract.outputs[0].name


@pytest.mark.parametrize("name,unit", [("", "m"), ("x", "")])
def test_quantity_needs_a_name_and_a_base_unit(name: str, unit: str) -> None:
    with pytest.raises(ValidationError):
        QuantityDeclaration(name=name, base_unit=unit)


def test_contract_is_immutable() -> None:
    contract = CalculationTypeContract(
        name="t", inputs=(quantity("a"),), outputs=(quantity("b"),)
    )

    with pytest.raises(ValidationError):
        contract.name = "other"

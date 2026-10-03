import pytest
from pydantic import ValidationError

from app.core.exceptions import AlreadyRegisteredError, DECError
from app.engine.base import Calculator
from app.engine.registry import CalculatorRegistry
from app.schemas.calculation import (
    CalculationTypeContract,
    OutputDeclaration,
    QuantityDeclaration,
    RoundingRule,
)
from app.schemas.parameters import EngineerRule


class DoublingCalculator(Calculator[float, float, float]):
    def calculate(self, inputs: float, parameters: float) -> float:
        return inputs * parameters


def doubling_contract(name: str = "doubling") -> CalculationTypeContract:
    return CalculationTypeContract(
        checks=("c",),
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
    )


def test_registered_calculator_is_found_by_name() -> None:
    registry = CalculatorRegistry()
    calculator = DoublingCalculator()

    registry.register(doubling_contract(), calculator)

    assert registry.get("doubling") is calculator
    assert registry.get("doubling").calculate(3.0, 2.0) == 6.0


def test_registry_holds_the_contract_of_the_type() -> None:
    registry = CalculatorRegistry()
    contract = doubling_contract()

    registry.register(contract, DoublingCalculator())

    assert registry.contract("doubling") is contract


def test_unregistered_name_raises_a_dec_error() -> None:
    registry = CalculatorRegistry()

    with pytest.raises(DECError):
        registry.get("missing")
    with pytest.raises(DECError):
        registry.contract("missing")


def test_registering_a_name_twice_raises_a_dec_error() -> None:
    registry = CalculatorRegistry()
    first = DoublingCalculator()
    registry.register(doubling_contract(), first)

    with pytest.raises(AlreadyRegisteredError):
        registry.register(doubling_contract(), DoublingCalculator())

    assert registry.get("doubling") is first


def test_calculator_interface_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        Calculator()  # type: ignore[abstract]


@pytest.mark.parametrize("missing", ["rounding_rule", "rounding_source"])
def test_a_type_whose_output_lacks_rounding_cannot_be_registered(missing: str) -> None:
    output = {
        "name": "y",
        "base_unit": "m",
        "rounding_rule": {"decimals": 2, "mode": "half_even"},
        "rounding_source": {"engineer": "<ENGINEER>", "rationale": "<RATIONALE>"},
    }
    del output[missing]
    registry = CalculatorRegistry()

    with pytest.raises(ValidationError, match=missing):
        registry.register(
            CalculationTypeContract.model_validate(
                {
                    "name": "doubling",
                    "inputs": [{"name": "x", "base_unit": "m"}],
                    "outputs": [output],
                    "checks": ["c"],
                }
            ),
            DoublingCalculator(),
        )

    with pytest.raises(DECError):
        registry.get("doubling")


def test_contracts_are_listed_in_registration_order() -> None:
    registry = CalculatorRegistry()
    registry.register(doubling_contract("b"), DoublingCalculator())
    registry.register(doubling_contract("a"), DoublingCalculator())

    assert [contract.name for contract in registry.contracts()] == ["b", "a"]
    assert CalculatorRegistry().contracts() == ()

import pytest

from app.core.exceptions import DECError
from app.engine.base import Calculator
from app.engine.registry import CalculatorRegistry


class DoublingCalculator(Calculator[float, float, float]):
    def calculate(self, inputs: float, parameters: float) -> float:
        return inputs * parameters


def test_registered_calculator_is_found_by_name() -> None:
    registry = CalculatorRegistry()
    calculator = DoublingCalculator()

    registry.register("doubling", calculator)

    assert registry.get("doubling") is calculator
    assert registry.get("doubling").calculate(3.0, 2.0) == 6.0


def test_unregistered_name_raises_a_dec_error() -> None:
    registry = CalculatorRegistry()

    with pytest.raises(DECError):
        registry.get("missing")


def test_calculator_interface_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        Calculator()  # type: ignore[abstract]

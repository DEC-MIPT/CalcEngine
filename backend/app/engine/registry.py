from typing import Any

from app.core.exceptions import AlreadyRegisteredError, NotFoundError
from app.engine.base import Calculator
from app.schemas.calculation import CalculationTypeContract


class CalculatorRegistry:
    def __init__(self) -> None:
        self._entries: dict[
            str, tuple[CalculationTypeContract, Calculator[Any, Any, Any]]
        ] = {}

    def register(
        self, contract: CalculationTypeContract, calculator: Calculator[Any, Any, Any]
    ) -> None:
        if contract.name in self._entries:
            raise AlreadyRegisteredError(
                f"calculation type {contract.name!r} is already registered"
            )
        self._entries[contract.name] = (contract, calculator)

    def get(self, calculation_type: str) -> Calculator[Any, Any, Any]:
        return self._entry(calculation_type)[1]

    def contract(self, calculation_type: str) -> CalculationTypeContract:
        return self._entry(calculation_type)[0]

    def _entry(
        self, calculation_type: str
    ) -> tuple[CalculationTypeContract, Calculator[Any, Any, Any]]:
        try:
            return self._entries[calculation_type]
        except KeyError:
            raise NotFoundError(
                f"no calculator registered for calculation type {calculation_type!r}"
            ) from None

from typing import Any

from app.core.exceptions import AlreadyRegisteredError, NotFoundError
from app.engine.base import Calculator


class CalculatorRegistry:
    def __init__(self) -> None:
        self._calculators: dict[str, Calculator[Any, Any, Any]] = {}

    def register(
        self, calculation_type: str, calculator: Calculator[Any, Any, Any]
    ) -> None:
        if calculation_type in self._calculators:
            raise AlreadyRegisteredError(
                f"calculation type {calculation_type!r} is already registered"
            )
        self._calculators[calculation_type] = calculator

    def get(self, calculation_type: str) -> Calculator[Any, Any, Any]:
        try:
            return self._calculators[calculation_type]
        except KeyError:
            raise NotFoundError(
                f"no calculator registered for calculation type {calculation_type!r}"
            ) from None

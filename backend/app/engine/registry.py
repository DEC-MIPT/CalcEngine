from typing import Any

from pydantic import TypeAdapter

from app.core.exceptions import (
    AlreadyRegisteredError,
    ContractMetadataError,
    NotFoundError,
)
from app.engine.base import Calculator
from app.engine.legacy_module import LegacyQuantityModule
from app.schemas.calculation import CalculationTypeContract


class CalculatorRegistry:
    def __init__(self) -> None:
        self._entries: dict[
            str, tuple[CalculationTypeContract, Calculator[Any, Any, Any]]
        ] = {}
        self._modules: dict[str, LegacyQuantityModule[Any]] = {}

    def register(
        self, contract: CalculationTypeContract, calculator: Calculator[Any, Any, Any],
        *, parameter_schema: type[Any] | None = None,
    ) -> None:
        if contract.name in self._entries:
            raise AlreadyRegisteredError(
                f"calculation type {contract.name!r} is already registered"
            )
        problems = contract.metadata_problems()
        if problems:
            raise ContractMetadataError(
                f"calculation type {contract.name!r} is not registered: {'; '.join(problems)}"
            )
        module = LegacyQuantityModule(
            contract, calculator, TypeAdapter(parameter_schema or object),
            infer_data_schema=parameter_schema is None,
        )
        self._entries[contract.name] = (contract, calculator)
        self._modules[contract.name] = module

    def get(self, calculation_type: str) -> Calculator[Any, Any, Any]:
        return self._entry(calculation_type)[1]

    def module(self, calculation_type: str) -> LegacyQuantityModule[Any]:
        """Возвращает совместимый модуль зарегистрированного калькулятора."""
        self._entry(calculation_type)
        return self._modules[calculation_type]

    def contract(self, calculation_type: str) -> CalculationTypeContract:
        return self._entry(calculation_type)[0]

    def contracts(self) -> tuple[CalculationTypeContract, ...]:
        """Возвращает контракты всех зарегистрированных типов расчёта.

        Returns:
            Контракты в порядке регистрации.
        """
        return tuple(contract for contract, _ in self._entries.values())

    def _entry(
        self, calculation_type: str
    ) -> tuple[CalculationTypeContract, Calculator[Any, Any, Any]]:
        try:
            return self._entries[calculation_type]
        except KeyError:
            raise NotFoundError(
                f"no calculator registered for calculation type {calculation_type!r}"
            ) from None

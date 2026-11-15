from collections.abc import Mapping, Sequence
from dataclasses import replace
from typing import Any

from app.engine.base import Calculator
from app.engine.legacy_module import (
    CalculatorOutput,
    LegacyOptions,
    LegacyQuantityModule,
    parameter_adapter,
)
from app.engine.module import execute_module
from app.engine.module_adapter import ModuleCalculator
from app.schemas.calculation import (
    BoundViolation,
    CalculationResult,
    CalculationTypeContract,
    MethodBound,
    QuantityValue,
    ValidatedBound,
)
from app.schemas.module import ModuleExecution
from app.schemas.normatives import CatalogSnapshot

__all__ = ["CalculatorOutput", "calculate"]


def calculate[ParametersT](
    contract: CalculationTypeContract,
    calculator: Calculator[Mapping[str, QuantityValue], ParametersT, Any],
    inputs: Mapping[str, QuantityValue],
    parameters: ParametersT,
    *,
    method_range: Sequence[MethodBound] = (),
    validated_range: Sequence[ValidatedBound] = (),
    module: Any | None = None,
) -> CalculationResult:
    """Чистая функция расчёта: на входе типизированные входы и разрешённые параметры, на выходе результат.

    Единицы переводятся и применимость проверяется на границе; отказ — это результат,
    а не исключение (design.md, решения 1–3). ``result_id`` в результат не входит: его
    назначает слой сервисов (решение 12).

    Args:
        contract: контракт типа расчёта.
        calculator: калькулятор типа.
        inputs: входы со своими единицами.
        parameters: разрешённые параметры калькулятора.
        method_range: границы диапазона метода.
        validated_range: границы проверенного диапазона.
        module: совместимый модуль, зарегистрированный при запуске приложения.

    Returns:
        Результат расчёта без ``result_id``.

    Raises:
        CalculationError: если калькулятор вернул не ``CalculatorOutput`` или его
            части не складываются в корректный результат.
        UnitError: если единицу входа нельзя перевести в базовую.
    """
    if module is None and isinstance(calculator, ModuleCalculator):
        module = calculator.module
    if module is not None and not isinstance(module, LegacyQuantityModule):
        return module.execute_public(inputs, parameters, LegacyOptions(
            method_range=tuple(method_range), validated_range=tuple(validated_range)))
    adapter = module or LegacyQuantityModule(contract, calculator, parameter_adapter(parameters))
    if adapter.infer_data_schema or isinstance(parameters, CatalogSnapshot):
        adapter = replace(adapter, data_schema=parameter_adapter(parameters), infer_data_schema=False)
    execution: ModuleExecution[Mapping[str, QuantityValue], BoundViolation] = execute_module(
        adapter,
        inputs,
        parameters,
        LegacyOptions(method_range=tuple(method_range), validated_range=tuple(validated_range)),
    )
    return adapter.adapt_result(execution)

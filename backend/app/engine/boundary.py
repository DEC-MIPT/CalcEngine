import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from app.core.exceptions import CalculationError, UnitError
from app.engine.applicability import check_applicability
from app.engine.base import Calculator
from app.engine.hashing import input_hash
from app.schemas.calculation import (
    ApplicabilityWarning,
    BoundViolation,
    CalculationTypeContract,
    MethodBound,
    OutputValue,
    QuantityValue,
    ValidatedBound,
)
from app.schemas.units import UNITS, Unit


def _unit(symbol: str) -> Unit:
    if symbol not in UNITS:
        raise UnitError(f"unit {symbol!r} is not in the unit vocabulary")
    return UNITS[symbol]


def _converted(value: float, source: str, target: str) -> float:
    source_unit, target_unit = _unit(source), _unit(target)
    if source_unit.dimension != target_unit.dimension:
        raise UnitError(
            f"cannot convert {source!r} ({source_unit.dimension}) to {target!r}"
            f" ({target_unit.dimension})"
        )
    if source == target:
        return value
    result = value * source_unit.factor / target_unit.factor
    if not math.isfinite(result):
        raise UnitError(f"{value} {source} is not a finite number in {target!r}")
    return result


def convert(value: QuantityValue, unit: str) -> QuantityValue:
    """Выражает величину в другой единице той же размерности.

    Args:
        value: величина со своей единицей.
        unit: целевая единица из словаря.

    Returns:
        Ту же величину в целевой единице.

    Raises:
        UnitError: если единицы нет в словаре, у неё другая размерность или
            результат не конечное число.
    """
    return QuantityValue(value=_converted(value.value, value.unit, unit), unit=unit)


def inputs_to_base_units(
    contract: CalculationTypeContract, inputs: Mapping[str, QuantityValue]
) -> dict[str, QuantityValue]:
    """Переводит каждый объявленный вход в его базовую единицу.

    Args:
        contract: контракт типа расчёта.
        inputs: входы запроса со своими единицами.

    Returns:
        Входы в базовых единицах в порядке контракта.

    Raises:
        CalculationError: если набор входов не совпадает с объявленным.
        UnitError: если единицу входа нельзя перевести в базовую.
    """
    declared = [quantity.name for quantity in contract.inputs]
    if set(inputs) != set(declared):
        raise CalculationError(
            f"inputs {sorted(inputs)} do not match the declared inputs {declared}"
        )
    return {
        quantity.name: convert(inputs[quantity.name], quantity.base_unit)
        for quantity in contract.inputs
    }


def make_outputs(
    contract: CalculationTypeContract, values: Mapping[str, QuantityValue]
) -> tuple[OutputValue, ...]:
    """Собирает объявленные выходы в том виде, в каком они покидают движок.

    Каждое неокруглённое значение переводится в базовую единицу и округляется по
    правилу, объявленному в контракте; запись несёт это правило и его источник. Шаги
    трассы и проверки сохраняют неокруглённые значения.

    Args:
        contract: контракт типа расчёта.
        values: неокруглённые выходы калькулятора.

    Returns:
        Выходы в порядке контракта.

    Raises:
        CalculationError: если набор выходов не совпадает с объявленным.
    """
    declared = [quantity.name for quantity in contract.outputs]
    if set(values) != set(declared):
        raise CalculationError(
            f"outputs {sorted(values)} do not match the declared outputs {declared}"
        )
    return tuple(
        OutputValue(
            quantity=quantity.name,
            value=quantity.rounding_rule.apply(convert(values[quantity.name], quantity.base_unit).value),
            unit=quantity.base_unit,
            rounding_rule=quantity.rounding_rule,
            rounding_source=quantity.rounding_source,
        )
        for quantity in contract.outputs
    )


@dataclass(frozen=True)
class Outcome[ResultT]:
    """Что возвращает граница движка: результат калькулятора или отказ.

    Attributes:
        input_hash: идентичность запуска по типу расчёта, входам в базовых единицах и
            разрешённым параметрам, включая оба диапазона (design.md, решение 6).
        result: результат калькулятора; ``None`` ровно тогда, когда задан ``refusal``.
        refusal: нарушенная граница диапазона метода или ``None``.
        warnings: предупреждения проверенного диапазона, в обоих случаях.
    """

    input_hash: str
    result: ResultT | None
    refusal: BoundViolation | None
    warnings: tuple[ApplicabilityWarning, ...]


def run[ParametersT, ResultT](
    contract: CalculationTypeContract,
    calculator: Calculator[Mapping[str, QuantityValue], ParametersT, ResultT],
    inputs: Mapping[str, QuantityValue],
    parameters: ParametersT,
    *,
    method_range: Sequence[MethodBound] = (),
    validated_range: Sequence[ValidatedBound] = (),
) -> Outcome[ResultT]:
    """Переводит входы, проверяет применимость и запускает совместимый legacy-калькулятор.

    Типизированные модули исполняются через ``pipeline.calculate`` или ``execute_module``;
    этот адаптер сохраняет legacy-контракт Outcome и отклоняет их до обработки входов.

    Единица вне словаря или другой размерности приводит к ``DECError`` до первого
    шага. Вход вне диапазона метода даёт отказ, и калькулятор не запускается
    (design.md, решения 2 и 3).

    Args:
        contract: контракт типа расчёта.
        calculator: калькулятор типа.
        inputs: входы со своими единицами.
        parameters: разрешённые параметры калькулятора.
        method_range: границы диапазона метода.
        validated_range: границы проверенного диапазона.

    Returns:
        Исход запуска: результат или отказ, предупреждения и ``input_hash``.

    Raises:
        CalculationError: если передан типизированный модуль, набор входов не совпадает
            с объявленным или диапазон противоречив.
        UnitError: если единицу входа нельзя перевести в базовую.
    """
    from app.engine.module_adapter import ModuleCalculator

    if isinstance(calculator, ModuleCalculator):
        raise CalculationError("typed quantity modules must execute through pipeline.calculate")
    converted = inputs_to_base_units(contract, inputs)
    identity = input_hash(
        contract.name,
        converted,
        {
            "parameters": parameters,
            "method_range": method_range,
            "validated_range": validated_range,
        },
    )
    refusal, warnings = check_applicability(converted, method_range, validated_range)
    if refusal is not None:
        return Outcome(input_hash=identity, result=None, refusal=refusal, warnings=warnings)
    return Outcome(
        input_hash=identity,
        result=calculator.calculate(converted, parameters),
        refusal=None,
        warnings=warnings,
    )

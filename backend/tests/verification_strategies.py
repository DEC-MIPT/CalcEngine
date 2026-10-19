import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from hypothesis import strategies as st

from app.engine.base import Calculator
from app.engine.boundary import convert
from app.schemas.calculation import CalculationTypeContract, MethodBound, QuantityValue
from app.schemas.units import UNITS, units_of
from app.verification.invariants import InputRange, InvariantPlan


@dataclass(frozen=True)
class Subject:
    """Тип расчёта, на котором проверяются общие инварианты.

    Attributes:
        contract: контракт типа.
        calculator: калькулятор типа.
        parameters: разрешённые параметры для данных входов (табличная строка зависит от входа).
        method_range: границы диапазона метода.
        plan: план инвариантов типа с допустимым диапазоном входов.
    """

    contract: CalculationTypeContract
    calculator: Calculator[Mapping[str, QuantityValue], Any, Any]
    parameters: Callable[[Mapping[str, QuantityValue]], object]
    method_range: tuple[MethodBound, ...]
    plan: InvariantPlan


def _input(item: InputRange) -> st.SearchStrategy[QuantityValue]:
    """Значение внутри диапазона, выраженное в любой единице той же размерности.

    Целые значения (``whole``) остаются в единице диапазона: в другой единице они
    перестали бы совпадать со строкой таблицы.

    Args:
        item: допустимый диапазон входа.

    Returns:
        Стратегия значений входа.
    """
    if item.whole:
        whole = st.integers(min_value=math.ceil(item.lower), max_value=math.floor(item.upper))
        return whole.map(lambda value: QuantityValue(value=float(value), unit=item.unit))
    values = st.floats(min_value=item.lower, max_value=item.upper, allow_nan=False, allow_infinity=False)
    units = st.sampled_from(units_of(UNITS[item.unit].dimension))
    return st.builds(lambda value, unit: convert(QuantityValue(value=value, unit=item.unit), unit), values, units)


def inputs_in_range(plan: InvariantPlan) -> st.SearchStrategy[dict[str, QuantityValue]]:
    """Входы типа внутри его допустимого диапазона (design.md, решение 17).

    Args:
        plan: план инвариантов типа.

    Returns:
        Стратегия словарей входов, каждый в случайной единице своей размерности.
    """
    return st.fixed_dictionaries({item.quantity: _input(item) for item in plan.valid_range})

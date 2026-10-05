from collections.abc import Mapping, Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.exceptions import UnitError
from app.engine.base import Calculator
from app.engine.boundary import convert, inputs_to_base_units
from app.engine.pipeline import calculate
from app.schemas.calculation import CalculationTypeContract, MethodBound, QuantityValue
from app.schemas.units import UNITS, UnitSymbol

DETERMINISM = "determinism"
"""Идентификатор общего инварианта: требование "Pure calculation function"."""

UNIT_CHANGE = "unit-change-consistency"
"""Идентификатор общего инварианта: требование "Explicit units at the boundary"."""


class Invariant(BaseModel):
    """Инвариант типа расчёта, верный при любой норме (`calculation-verification` "Invariant tests").

    Attributes:
        identifier: идентификатор инварианта, уникальный в плане типа.
        statement: утверждение инварианта.
        quantities: имена входов и выходов типа, которые в нём участвуют.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    identifier: str = Field(pattern=r"\S")
    statement: str = Field(pattern=r"\S")
    quantities: tuple[str, ...] = Field(min_length=1)


class InputRange(BaseModel):
    """Допустимый диапазон одного входа, из которого генератор берёт значения.

    Это данные типа, как его эталонные примеры, а не значение нормы и не диапазон
    применимости метода (design.md, решение 17). Границы входят.

    Attributes:
        quantity: имя входа типа.
        lower: нижняя граница.
        upper: верхняя граница, не меньше нижней.
        unit: единица обеих границ.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    quantity: str = Field(pattern=r"\S")
    lower: float
    upper: float
    unit: UnitSymbol

    @model_validator(mode="after")
    def _ordered(self) -> "InputRange":
        if self.lower > self.upper:
            raise ValueError("lower must not exceed upper")
        return self


class InvariantPlan(BaseModel):
    """Инварианты типа расчёта и допустимый диапазон его входов.

    Attributes:
        calculation_type: зарегистрированное имя типа расчёта.
        valid_range: по одному диапазону на каждый вход типа.
        invariants: инварианты типа; общие (детерминизм, смена единицы) входят всегда.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    calculation_type: str = Field(pattern=r"\S")
    valid_range: tuple[InputRange, ...] = Field(min_length=1)
    invariants: tuple[Invariant, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _unique(self) -> "InvariantPlan":
        quantities = [item.quantity for item in self.valid_range]
        if len(set(quantities)) != len(quantities):
            raise ValueError("each input has at most one range")
        identifiers = [invariant.identifier for invariant in self.invariants]
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("invariant identifiers must be unique")
        return self


def shared_invariants(contract: CalculationTypeContract) -> tuple[Invariant, Invariant]:
    """Строит два общих инварианта для типа расчёта (design.md, решение 17).

    Args:
        contract: контракт типа расчёта.

    Returns:
        Детерминизм и согласованность при смене единицы, со всеми величинами типа.
    """
    inputs = tuple(quantity.name for quantity in contract.inputs)
    outputs = tuple(quantity.name for quantity in contract.outputs)
    return (
        Invariant(
            identifier=DETERMINISM,
            statement="Two calls of the pure function with the same inputs and resolved parameters give equal results.",
            quantities=inputs + outputs,
        ),
        Invariant(
            identifier=UNIT_CHANGE,
            statement=(
                "An input given in another unit gives the same result as that input converted"
                " to its base unit by the engine and given in the base unit."
            ),
            quantities=inputs + outputs,
        ),
    )


def plan_problems(plan: InvariantPlan, contract: CalculationTypeContract) -> tuple[str, ...]:
    """Сверяет план инвариантов с контрактом типа расчёта.

    План годится, когда он для этого типа, у каждого входа ровно один диапазон в единице
    его размерности, конечный после перевода в базовую единицу, в нём есть оба общих
    инварианта и каждый инвариант называет только величины типа.

    Args:
        plan: план инвариантов.
        contract: контракт того же типа.

    Returns:
        Описания нарушений; пусто, если план годится.
    """
    problems: list[str] = []
    if plan.calculation_type != contract.name:
        problems.append(f"plan is for {plan.calculation_type!r}, contract is {contract.name!r}")
    inputs = {quantity.name: quantity.base_unit for quantity in contract.inputs}
    ranged = {item.quantity: item for item in plan.valid_range}
    problems.extend(f"input {name!r} has no range" for name in inputs if name not in ranged)
    for name, item in ranged.items():
        if name not in inputs:
            problems.append(f"range of {name!r} names no input")
        elif UNITS[item.unit].dimension is not UNITS[inputs[name]].dimension:
            problems.append(f"range of {name!r} is in a unit of another dimension")
        else:
            try:
                for bound in (item.lower, item.upper):
                    convert(QuantityValue(value=bound, unit=item.unit), inputs[name])
            except UnitError:
                problems.append(f"range of {name!r} overflows in the base unit")
    identifiers = {invariant.identifier for invariant in plan.invariants}
    problems.extend(
        f"shared invariant {identifier!r} is missing" for identifier in (DETERMINISM, UNIT_CHANGE) if identifier not in identifiers
    )
    known = set(inputs) | {quantity.name for quantity in contract.outputs}
    for invariant in plan.invariants:
        problems.extend(
            f"invariant {invariant.identifier!r} names unknown quantity {name!r}"
            for name in invariant.quantities
            if name not in known
        )
    return tuple(problems)


def determinism_holds(
    contract: CalculationTypeContract,
    calculator: Calculator[Mapping[str, QuantityValue], Any, Any],
    inputs: Mapping[str, QuantityValue],
    parameters: object,
    method_range: Sequence[MethodBound] = (),
) -> bool:
    """Проверяет детерминизм: два одинаковых вызова чистой функции дают равные результаты.

    Требование "Pure calculation function" `calculation-core-contract`, задача 2.10.

    Args:
        contract: контракт типа расчёта.
        calculator: калькулятор типа.
        inputs: входы со своими единицами.
        parameters: разрешённые параметры.
        method_range: границы диапазона метода.

    Returns:
        ``True``, если результаты равны поле в поле.
    """
    first = calculate(contract, calculator, inputs, parameters, method_range=method_range)
    second = calculate(contract, calculator, inputs, parameters, method_range=method_range)
    return first == second


def unit_change_holds(
    contract: CalculationTypeContract,
    calculator: Calculator[Mapping[str, QuantityValue], Any, Any],
    inputs: Mapping[str, QuantityValue],
    parameters: object,
    method_range: Sequence[MethodBound] = (),
) -> bool:
    """Проверяет согласованность при смене единицы (design.md, решение 17; задача 2.9).

    Входы в своих единицах дают тот же результат, поле в поле и без допуска, что те же
    входы, переведённые в базовые единицы собственным переводом движка и поданные в
    базовых единицах (требование "Explicit units at the boundary"
    `calculation-core-contract`).

    Args:
        contract: контракт типа расчёта.
        calculator: калькулятор типа.
        inputs: входы в любых единицах их размерностей.
        parameters: разрешённые параметры.
        method_range: границы диапазона метода.

    Returns:
        ``True``, если оба результата равны.
    """
    given = calculate(contract, calculator, inputs, parameters, method_range=method_range)
    in_base = inputs_to_base_units(contract, inputs)
    converted = calculate(contract, calculator, in_base, parameters, method_range=method_range)
    return given == converted

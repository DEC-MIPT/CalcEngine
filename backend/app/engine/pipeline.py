from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from app.core.exceptions import CalculationError
from app.engine.base import Calculator
from app.engine.boundary import make_outputs, run
from app.engine.result import assemble_result
from app.schemas.calculation import (
    CalculationResult,
    CalculationTypeContract,
    CheckStep,
    FormulaStep,
    MethodBound,
    QuantityValue,
    TableStep,
    ValidatedBound,
)


@dataclass(frozen=True)
class CalculatorOutput:
    """Что вычисляет тип расчёта: трассу и неокруглённые выходы.

    Attributes:
        trace: шаги трассы по порядку.
        outputs: неокруглённые выходы по именам величин.
    """

    trace: tuple[FormulaStep | TableStep | CheckStep, ...]
    outputs: Mapping[str, QuantityValue]


def calculate[ParametersT](
    contract: CalculationTypeContract,
    calculator: Calculator[Mapping[str, QuantityValue], ParametersT, CalculatorOutput],
    inputs: Mapping[str, QuantityValue],
    parameters: ParametersT,
    *,
    method_range: Sequence[MethodBound] = (),
    validated_range: Sequence[ValidatedBound] = (),
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

    Returns:
        Результат расчёта без ``result_id``.

    Raises:
        CalculationError: если калькулятор вернул не ``CalculatorOutput`` или его
            части не складываются в корректный результат.
        UnitError: если единицу входа нельзя перевести в базовую.
    """
    outcome = run(
        contract,
        calculator,
        inputs,
        parameters,
        method_range=method_range,
        validated_range=validated_range,
    )
    if outcome.result is None:
        return assemble_result(
            contract,
            input_hash=outcome.input_hash,
            trace=(),
            outputs=(),
            warnings=outcome.warnings,
            validated_range=validated_range,
            refusal=outcome.refusal,
        )
    if not isinstance(outcome.result, CalculatorOutput):
        raise CalculationError(
            f"calculator of {contract.name!r} returned {type(outcome.result).__name__},"
            " not a CalculatorOutput"
        )
    return assemble_result(
        contract,
        input_hash=outcome.input_hash,
        trace=outcome.result.trace,
        outputs=make_outputs(contract, outcome.result.outputs),
        warnings=outcome.warnings,
        validated_range=validated_range,
    )

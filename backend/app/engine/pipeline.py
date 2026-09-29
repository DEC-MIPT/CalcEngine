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
    """What a calculation type computes: its trace and its unrounded outputs."""

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
    """The pure calculation function: typed inputs and resolved parameters in, a result out.

    Units are converted and applicability is checked at the boundary; a refusal is a
    result, not an exception (design.md decisions 1-3). ``result_id`` is not part of
    it: the service layer assigns it (decision 12).
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

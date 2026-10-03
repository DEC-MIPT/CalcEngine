import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from app.core.exceptions import CalculationError, UnitError
from app.engine.applicability import check_applicability
from app.engine.base import Calculator
from app.engine.hashing import input_hash
from app.engine.rounding import round_value
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
    """The same quantity in another unit of its dimension."""
    return QuantityValue(value=_converted(value.value, value.unit, unit), unit=unit)


def inputs_to_base_units(
    contract: CalculationTypeContract, inputs: Mapping[str, QuantityValue]
) -> dict[str, QuantityValue]:
    """Every declared input in its base unit, in the contract's order."""
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
    """The declared outputs as they leave the engine, in the contract's order.

    Each unrounded value is converted to its base unit and rounded by the rule its
    contract declares; the entry carries that rule and its source. Trace steps and
    checks keep the unrounded values.
    """
    declared = [quantity.name for quantity in contract.outputs]
    if set(values) != set(declared):
        raise CalculationError(
            f"outputs {sorted(values)} do not match the declared outputs {declared}"
        )
    return tuple(
        OutputValue(
            quantity=quantity.name,
            value=round_value(
                convert(values[quantity.name], quantity.base_unit).value, quantity.rounding_rule
            ),
            unit=quantity.base_unit,
            rounding_rule=quantity.rounding_rule,
            rounding_source=quantity.rounding_source,
        )
        for quantity in contract.outputs
    )


@dataclass(frozen=True)
class Outcome[ResultT]:
    """What the engine boundary gives back: the calculator's result, or a refusal.

    ``result`` is ``None`` exactly when ``refusal`` is set; ``warnings`` hold the
    validated-range warnings in either case. ``input_hash`` identifies the run by
    its calculation type, inputs in base units, and resolved parameters, including
    both ranges (design.md decision 6).
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
    """Convert the inputs to base units, check applicability, then run the calculator.

    A unit outside the vocabulary or of another dimension fails with a ``DECError``
    before any step runs. An input outside the method's range refuses the
    calculation, and the calculator does not run (design.md decisions 2 and 3).
    """
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

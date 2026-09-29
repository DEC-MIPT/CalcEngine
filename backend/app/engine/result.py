from collections.abc import Sequence
from typing import Literal

from pydantic import ValidationError

from app.core.exceptions import CalculationError, UnitError
from app.schemas.calculation import (
    ApplicabilityWarning,
    BoundViolation,
    CalculationResult,
    CalculationTypeContract,
    CheckReason,
    CheckStep,
    FormulaStep,
    OutputValue,
    TableStep,
    ValidatedBound,
    ordered_sources,
    unverified_steps,
    verdict_of,
)

Step = FormulaStep | TableStep | CheckStep


def _ordered_outputs(
    contract: CalculationTypeContract, outputs: Sequence[OutputValue]
) -> tuple[OutputValue, ...]:
    by_name: dict[str, OutputValue] = {}
    for output in outputs:
        if output.quantity in by_name:
            raise CalculationError(f"output {output.quantity!r} is given twice")
        by_name[output.quantity] = output
    declared = [quantity.name for quantity in contract.outputs]
    if set(by_name) != set(declared):
        raise CalculationError(
            f"outputs {sorted(by_name)} do not match the declared outputs {declared}"
        )
    for quantity in contract.outputs:
        output = by_name[quantity.name]
        if output.unit != quantity.base_unit:
            raise UnitError(
                f"output {quantity.name!r} is in {output.unit!r},"
                f" its base unit is {quantity.base_unit!r}"
            )
        if (output.rounding_rule, output.rounding_source) != (
            quantity.rounding_rule,
            quantity.rounding_source,
        ):
            raise CalculationError(
                f"output {quantity.name!r} is not rounded by the rule its contract declares"
            )
    return tuple(by_name[name] for name in declared)


def _ordered_warnings(
    warnings: Sequence[ApplicabilityWarning], validated_range: Sequence[ValidatedBound]
) -> tuple[ApplicabilityWarning, ...]:
    positions = []
    for warning in warnings:
        if warning.bound not in validated_range:
            raise CalculationError("a warning names a bound outside the validated range")
        positions.append((validated_range.index(warning.bound), warning))
    return tuple(warning for _, warning in sorted(positions, key=lambda item: item[0]))


def _check_steps_are_declared(contract: CalculationTypeContract, trace: Sequence[Step]) -> None:
    for step in trace:
        if isinstance(step, CheckStep) and step.step_id not in contract.checks:
            raise CalculationError(
                f"check {step.step_id!r} is not declared by calculation type {contract.name!r}"
            )


def assemble_result(
    contract: CalculationTypeContract,
    *,
    engine_version: str,
    input_hash: str,
    trace: Sequence[Step],
    outputs: Sequence[OutputValue],
    warnings: Sequence[ApplicabilityWarning],
    validated_range: Sequence[ValidatedBound],
    refusal: BoundViolation | None = None,
) -> CalculationResult:
    """Build a calculation result with its lists ordered (design.md decision 17).

    ``outputs`` follow the contract's declared order, ``warnings`` the declared order
    of ``validated_range``; ``norm_refs`` and ``engineer_rules`` hold each source
    once, in the order of first use. A refused calculation has no trace or outputs.
    """
    ordered_warnings = _ordered_warnings(warnings, validated_range)
    verdict: Literal["pass", "fail", "refused"]
    reason: BoundViolation | CheckReason
    ordered_outputs: tuple[OutputValue, ...]
    if refusal is not None:
        if trace or outputs:
            raise CalculationError("a refused calculation has no trace and no outputs")
        verdict, reason, ordered_outputs = "refused", refusal, ()
    else:
        _check_steps_are_declared(contract, trace)
        ordered_outputs = _ordered_outputs(contract, outputs)
        try:
            verdict, step_id = verdict_of(trace)
        except ValueError as exc:
            raise CalculationError(str(exc)) from exc
        reason = CheckReason(step_id=step_id)
    norm_refs, engineer_rules = ordered_sources(
        trace, refusal, ordered_outputs, ordered_warnings
    )
    try:
        return CalculationResult(
            engine_version=engine_version,
            input_hash=input_hash,
            outputs=ordered_outputs,
            norm_refs=norm_refs,
            engineer_rules=engineer_rules,
            verdict=verdict,
            verdict_reason=reason,
            warnings=ordered_warnings,
            trace=tuple(trace),
            unverified_step_count=unverified_steps(trace),
        )
    except ValidationError as exc:
        raise CalculationError(f"the calculation result is not valid: {exc}") from exc

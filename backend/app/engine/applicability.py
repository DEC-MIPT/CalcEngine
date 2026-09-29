from collections.abc import Mapping, Sequence

from app.core.exceptions import CalculationError
from app.schemas.calculation import (
    ApplicabilityWarning,
    BoundViolation,
    MethodBound,
    QuantityValue,
    ValidatedBound,
    check_bounds,
)


def is_inside(value: float, bound: MethodBound | ValidatedBound) -> bool:
    """Whether a value in its base unit is on the allowed side of a bound."""
    if value == bound.value:
        return bound.inclusive
    return value > bound.value if bound.kind == "min" else value < bound.value


def _checked(
    inputs: Mapping[str, QuantityValue], bounds: Sequence[MethodBound | ValidatedBound]
) -> None:
    try:
        check_bounds(bounds)
    except ValueError as exc:
        raise CalculationError(str(exc)) from exc
    for bound in bounds:
        if bound.quantity not in inputs:
            raise CalculationError(f"bound on {bound.quantity!r}, which is not an input")


def check_applicability(
    inputs: Mapping[str, QuantityValue],
    method_range: Sequence[MethodBound],
    validated_range: Sequence[ValidatedBound],
) -> tuple[BoundViolation | None, tuple[ApplicabilityWarning, ...]]:
    """The three outcomes of "Applicability check with three outcomes".

    Inputs are in their base units. Returns the first violated bound of the method's
    range in declared order (a refusal), or none; and a warning for every violated
    bound of the validated range, in declared order.
    """
    _checked(inputs, method_range)
    _checked(inputs, validated_range)
    refusal = next(
        (
            BoundViolation(value=inputs[bound.quantity], bound=bound)
            for bound in method_range
            if not is_inside(inputs[bound.quantity].value, bound)
        ),
        None,
    )
    warnings = tuple(
        ApplicabilityWarning(value=inputs[bound.quantity], bound=bound)
        for bound in validated_range
        if not is_inside(inputs[bound.quantity].value, bound)
    )
    return refusal, warnings

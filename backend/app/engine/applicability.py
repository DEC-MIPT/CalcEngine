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
    """Проверяет, лежит ли значение по разрешённую сторону границы.

    Args:
        value: значение в базовой единице.
        bound: граница диапазона метода или проверенного диапазона.

    Returns:
        ``True``, если значение допустимо; при равенстве решает ``inclusive``.
    """
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
    """Проверяет применимость с тремя исходами ("Applicability check with three outcomes").

    Args:
        inputs: входы в базовых единицах.
        method_range: границы диапазона метода в объявленном порядке.
        validated_range: границы проверенного диапазона в объявленном порядке.

    Returns:
        Первую нарушенную границу диапазона метода в объявленном порядке (отказ) или
        ``None``, и предупреждение для каждой нарушенной границы проверенного
        диапазона в объявленном порядке.

    Raises:
        CalculationError: если диапазон противоречив или граница стоит на величине,
            которой нет среди входов.
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

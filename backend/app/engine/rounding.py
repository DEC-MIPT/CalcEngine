from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal

from app.schemas.calculation import RoundingRule

_MODES = {"half_up": ROUND_HALF_UP, "half_even": ROUND_HALF_EVEN}


def round_value(value: float, rule: RoundingRule) -> float:
    """Round an output value by its rule (design.md decision 14).

    The float becomes the shortest decimal that reads back to it, so ``2.675`` is
    rounded as ``2.675`` and not as its binary neighbour. ``half_up`` rounds a tie
    away from zero.
    """
    exponent = Decimal(1).scaleb(-rule.decimals)
    return float(Decimal(repr(value)).quantize(exponent, rounding=_MODES[rule.mode]))

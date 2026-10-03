from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal

from app.schemas.calculation import RoundingRule

_MODES = {"half_up": ROUND_HALF_UP, "half_even": ROUND_HALF_EVEN}


def round_value(value: float, rule: RoundingRule) -> float:
    """Округляет значение выхода по его правилу (design.md, решение 14).

    Число с плавающей точкой превращается в самую короткую десятичную запись, которая
    читается обратно в то же значение, поэтому ``2.675`` округляется как ``2.675``, а
    не как его двоичный сосед. ``half_up`` округляет половину от нуля.

    Args:
        value: неокруглённое значение.
        rule: число знаков после запятой и режим округления.

    Returns:
        Округлённое значение.
    """
    exponent = Decimal(1).scaleb(-rule.decimals)
    return float(Decimal(repr(value)).quantize(exponent, rounding=_MODES[rule.mode]))

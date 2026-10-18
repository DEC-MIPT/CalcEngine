import datetime
import operator
from collections.abc import Callable, Mapping
from decimal import Decimal
from types import MappingProxyType

from app.reporting.formula import Line, Math
from app.schemas.calculation import (
    CheckStep,
    MethodBound,
    NormRef,
    QuantityValue,
    RoundingRule,
    Source,
    ValidatedBound,
)
from app.schemas.parameters import EngineerRule

UNIT_DESIGNATIONS: MappingProxyType[str, str] = MappingProxyType(
    {
        "1": "",
        "m": "м",
        "cm": "см",
        "mm": "мм",
        "m2": "м²",
        "N": "Н",
        "kN": "кН",
        "MN": "МН",
        "Pa": "Па",
        "kPa": "кПа",
        "MPa": "МПа",
        "N/m3": "Н/м³",
        "kN/m3": "кН/м³",
        "rad": "рад",
        "deg": "°",
    }
)
"""Русские обозначения единиц словаря в том виде, в каком они печатаются в отчёте (source: unverified)."""

LATEX_ATTACHED: MappingProxyType[str, str] = MappingProxyType({"°": r"^{\circ}"})
"""Обозначения, которые пишутся вплотную к числу, и их запись в LaTeX."""

LATEX_OPERATORS: MappingProxyType[str, str] = MappingProxyType(
    {"le": r"\le", "lt": "<", "ge": r"\ge", "gt": ">"}
)

_HOLDS: MappingProxyType[str, Callable[[float, float], bool]] = MappingProxyType(
    {"le": operator.le, "lt": operator.lt, "ge": operator.ge, "gt": operator.gt}
)

UNVERIFIED_TEXT = "не проверено"

VERDICT_TEXTS: MappingProxyType[str, tuple[str, str]] = MappingProxyType(
    {
        "pass": ("выполнено", "Все проверки выполнены."),
        "fail": ("не выполнено", "Проверка не выполнена."),
        "refused": ("расчёт отклонён", "Расчёт отклонён: входное значение вне области применения метода."),
    }
)
"""Тексты каждого вердикта: короткое имя для блока подотчётности и фраза заключения."""


def format_number(value: float, decimals: int = 0) -> str:
    """Форматирует число самой короткой десятичной записью без экспоненты и с запятой.

    Запись читается обратно в то же значение float. Дробная часть дополняется нулями
    до ``decimals`` знаков, как у округлённого значения выхода на экране результата.

    Args:
        value: число.
        decimals: наименьшее число знаков после запятой.

    Returns:
        Число в виде строки, например ``172,5``, ``172,50`` или ``0,0000001``.
    """
    text = "0" if value == 0 else format(Decimal(repr(value)).normalize(), "f")
    whole, _, fraction = text.partition(".")
    fraction = fraction.ljust(decimals, "0")
    return f"{whole},{fraction}" if fraction else whole


def latex_number(value: float, decimals: int = 0) -> str:
    """Записывает число в LaTeX так же, как ``format_number``.

    Запятая заключена в фигурные скобки, чтобы после неё не было пробела.

    Args:
        value: число.
        decimals: наименьшее число знаков после запятой.

    Returns:
        Число в LaTeX, например ``172{,}5``.
    """
    return format_number(value, decimals).replace(",", "{,}")


def latex_quantity(value: QuantityValue, rule: RoundingRule | None = None) -> str:
    """Записывает значение в LaTeX с русским обозначением его единицы.

    У безразмерного значения обозначения нет. С правилом округления выхода значение
    печатается округлённым и ровно с его числом знаков после запятой.

    Args:
        value: значение с единицей.
        rule: правило округления выхода, если значение относится к выходу.

    Returns:
        Выражение LaTeX, например ``172{,}5\\ \\text{кПа}``.
    """
    number = (
        latex_number(value.value) if rule is None else latex_number(rule.apply(value.value), rule.decimals)
    )
    unit = UNIT_DESIGNATIONS[value.unit]
    if not unit:
        return number
    if unit in LATEX_ATTACHED:
        return number + LATEX_ATTACHED[unit]
    return rf"{number}\ \text{{{unit}}}"


def check_rounding(
    step: CheckStep, rounding: Mapping[str, RoundingRule]
) -> tuple[RoundingRule | None, RoundingRule | None]:
    """Находит правила округления, по которым печатаются стороны проверки.

    Сторона, чья величина — выход, печатается по его правилу. Если округлённые стороны
    противоречили бы исходу проверки, обе печатаются без округления, как на экране
    результата.

    Args:
        step: шаг проверки; его подстановки называют левую и правую величины.
        rounding: правила округления выходов по имени.

    Returns:
        Правила левой и правой сторон или ``None`` для стороны без округления.
    """
    left, right = (rounding.get(substitution.symbol) for substitution in step.substitutions[:2])

    def shown(value: float, rule: RoundingRule | None) -> float:
        return value if rule is None else rule.apply(value)

    agrees = _HOLDS[step.operator](shown(step.result.value, left), shown(step.right.value, right)) == step.passed
    return (left, right) if agrees else (None, None)


def format_norm_ref(reference: NormRef, *, status: bool = True) -> str:
    """Форматирует ссылку на норму, по умолчанию с её статусом.

    Редакция или пункт со значением ``unverified`` печатаются как непроверенные.

    Args:
        reference: ссылка на норму.
        status: печатать ли статус проверки ссылки.

    Returns:
        Строка ссылки.
    """
    edition, clause = (
        UNVERIFIED_TEXT if part == "unverified" else part
        for part in (reference.edition, reference.clause)
    )
    text = f"{reference.document}, редакция: {edition}, пункт: {clause}"
    if not status:
        return text
    checked = "проверено" if reference.status == "verified" else UNVERIFIED_TEXT
    return f"{text} (статус: {checked})"


BOUND_WORDS: MappingProxyType[tuple[str, bool], str] = MappingProxyType(
    {("min", True): "не менее", ("min", False): "более", ("max", True): "не более", ("max", False): "менее"}
)

ROUNDING_MODES: MappingProxyType[str, str] = MappingProxyType(
    {"half_up": "половина — от нуля", "half_even": "половина — к чётному"}
)


def format_bound(bound: MethodBound | ValidatedBound, unit: str) -> Line:
    """Описывает, что допускает граница, в единице входа, который она ограничивает.

    Args:
        bound: граница диапазона метода или проверенного диапазона.
        unit: базовая единица входа.

    Returns:
        Строка вида «допускается не более 1 м», где предел — формула.
    """
    limit = latex_quantity(QuantityValue(value=bound.value, unit=unit))
    return (f"допускается {BOUND_WORDS[(bound.kind, bound.inclusive)]} ", Math(limit))


def format_engineer_rule(rule: EngineerRule) -> str:
    return f"решение инженера {rule.engineer}: {rule.rationale}"


def format_source(source: Source) -> str:
    """Форматирует источник: правило инженера или ссылки на нормы со статусом.

    Args:
        source: правило инженера или список ссылок на нормы.

    Returns:
        Строка источника.
    """
    if isinstance(source, EngineerRule):
        return format_engineer_rule(source)
    return "; ".join(format_norm_ref(reference) for reference in source)


def format_rounding(rule: RoundingRule) -> str:
    return f"{rule.decimals} знак(а) после запятой, {ROUNDING_MODES[rule.mode]}"


def format_date(day: datetime.date) -> str:
    """Форматирует дату как ``ДД.ММ.ГГ`` с двумя последними цифрами года.

    Формат по GOST R 21.101-2026 (edition unverified), приложение Е, примечание 2.

    Args:
        day: дата.

    Returns:
        Строка вида ``30.09.26``.
    """
    return day.strftime("%d.%m.%y")

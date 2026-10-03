import datetime
from decimal import Decimal
from types import MappingProxyType

from app.schemas.calculation import (
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

_ATTACHED = frozenset({"°"})

OPERATORS: MappingProxyType[str, str] = MappingProxyType(
    {"le": "≤", "lt": "<", "ge": "≥", "gt": ">"}
)

UNVERIFIED_TEXT = "не проверено"


def format_number(value: float) -> str:
    """Форматирует число самой короткой десятичной записью без экспоненты и с запятой.

    Запись читается обратно в то же значение float.

    Args:
        value: число.

    Returns:
        Число в виде строки, например ``172,5`` или ``0,0000001``.
    """
    if value == 0:
        return "0"
    text = format(Decimal(repr(value)).normalize(), "f")
    return text.replace(".", ",")


def format_quantity(value: QuantityValue) -> str:
    """Форматирует значение с русским обозначением его единицы.

    У безразмерного значения обозначения нет.

    Args:
        value: значение с единицей.

    Returns:
        Строка вида ``172,5 кПа``.
    """
    number, unit = format_number(value.value), UNIT_DESIGNATIONS[value.unit]
    if not unit:
        return number
    return f"{number}{unit}" if unit in _ATTACHED else f"{number} {unit}"


def format_norm_ref(reference: NormRef) -> str:
    """Форматирует ссылку на норму с её статусом.

    Редакция или пункт со значением ``unverified`` печатаются как непроверенные.

    Args:
        reference: ссылка на норму.

    Returns:
        Строка ссылки со статусом.
    """
    edition, clause = (
        UNVERIFIED_TEXT if part == "unverified" else part
        for part in (reference.edition, reference.clause)
    )
    status = "проверено" if reference.status == "verified" else UNVERIFIED_TEXT
    return f"{reference.document}, редакция: {edition}, пункт: {clause} (статус: {status})"


BOUND_WORDS: MappingProxyType[tuple[str, bool], str] = MappingProxyType(
    {("min", True): "не менее", ("min", False): "более", ("max", True): "не более", ("max", False): "менее"}
)

ROUNDING_MODES: MappingProxyType[str, str] = MappingProxyType(
    {"half_up": "половина — от нуля", "half_even": "половина — к чётному"}
)


def format_bound(bound: MethodBound | ValidatedBound, unit: str) -> str:
    """Описывает, что допускает граница, в единице входа, который она ограничивает.

    Args:
        bound: граница диапазона метода или проверенного диапазона.
        unit: базовая единица входа.

    Returns:
        Строка вида «допускается не более 1 м».
    """
    limit = format_quantity(QuantityValue(value=bound.value, unit=unit))
    return f"допускается {BOUND_WORDS[(bound.kind, bound.inclusive)]} {limit}"


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

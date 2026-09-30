from decimal import Decimal
from types import MappingProxyType

from app.schemas.calculation import NormRef, QuantityValue

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
"""Russian designations of the unit vocabulary as printed in a report (source: unverified)."""

_ATTACHED = frozenset({"°"})

OPERATORS: MappingProxyType[str, str] = MappingProxyType(
    {"le": "≤", "lt": "<", "ge": "≥", "gt": ">"}
)

UNVERIFIED_TEXT = "не проверено"


def format_number(value: float) -> str:
    """The shortest decimal that reads back to the same float, without an exponent, with a comma."""
    if value == 0:
        return "0"
    text = format(Decimal(repr(value)).normalize(), "f")
    return text.replace(".", ",")


def format_quantity(value: QuantityValue) -> str:
    """A value followed by the Russian designation of its unit; a dimensionless value has none."""
    number, unit = format_number(value.value), UNIT_DESIGNATIONS[value.unit]
    if not unit:
        return number
    return f"{number}{unit}" if unit in _ATTACHED else f"{number} {unit}"


def format_norm_ref(reference: NormRef) -> str:
    """A reference with its status; an ``unverified`` edition or clause is printed as unverified."""
    edition, clause = (
        UNVERIFIED_TEXT if part == "unverified" else part
        for part in (reference.edition, reference.clause)
    )
    status = "проверено" if reference.status == "verified" else UNVERIFIED_TEXT
    return f"{reference.document}, редакция: {edition}, пункт: {clause} (статус: {status})"

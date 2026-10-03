import math
from enum import StrEnum
from types import MappingProxyType
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field


class Dimension(StrEnum):
    DIMENSIONLESS = "dimensionless"
    LENGTH = "length"
    AREA = "area"
    FORCE = "force"
    PRESSURE = "pressure"
    SPECIFIC_WEIGHT = "specific_weight"
    ANGLE = "angle"


class Unit(BaseModel):
    """Обозначение единицы, её размерность и множитель к единице СИ этой размерности.

    Это определения единиц, а не значения норм (design.md, решение 13).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    symbol: str = Field(min_length=1)
    dimension: Dimension
    factor: float = Field(gt=0)


UNITS: MappingProxyType[str, Unit] = MappingProxyType(
    {
        unit.symbol: unit
        for unit in (
            Unit(symbol="1", dimension=Dimension.DIMENSIONLESS, factor=1.0),
            Unit(symbol="m", dimension=Dimension.LENGTH, factor=1.0),
            Unit(symbol="cm", dimension=Dimension.LENGTH, factor=1e-2),
            Unit(symbol="mm", dimension=Dimension.LENGTH, factor=1e-3),
            Unit(symbol="m2", dimension=Dimension.AREA, factor=1.0),
            Unit(symbol="N", dimension=Dimension.FORCE, factor=1.0),
            Unit(symbol="kN", dimension=Dimension.FORCE, factor=1e3),
            Unit(symbol="MN", dimension=Dimension.FORCE, factor=1e6),
            Unit(symbol="Pa", dimension=Dimension.PRESSURE, factor=1.0),
            Unit(symbol="kPa", dimension=Dimension.PRESSURE, factor=1e3),
            Unit(symbol="MPa", dimension=Dimension.PRESSURE, factor=1e6),
            Unit(symbol="N/m3", dimension=Dimension.SPECIFIC_WEIGHT, factor=1.0),
            Unit(symbol="kN/m3", dimension=Dimension.SPECIFIC_WEIGHT, factor=1e3),
            Unit(symbol="rad", dimension=Dimension.ANGLE, factor=1.0),
            Unit(symbol="deg", dimension=Dimension.ANGLE, factor=math.pi / 180),
        )
    }
)


def _in_vocabulary(symbol: str) -> str:
    if symbol not in UNITS:
        raise ValueError(f"unit {symbol!r} is not in the unit vocabulary")
    return symbol


UnitSymbol = Annotated[str, AfterValidator(_in_vocabulary)]


def units_of(dimension: Dimension) -> tuple[str, ...]:
    """Перечисляет единицы словаря одной размерности.

    Args:
        dimension: размерность.

    Returns:
        Обозначения единиц этой размерности в порядке словаря.
    """
    return tuple(symbol for symbol, unit in UNITS.items() if unit.dimension is dimension)

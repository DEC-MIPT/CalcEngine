from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from app.schemas.calculation import MethodBound, QuantityValue


@dataclass(frozen=True)
class ResolvedParameters:
    """Нормативные параметры одного расчёта.

    Это типизированные параметры калькулятора и диапазон применимости метода
    (``calculation-api`` design.md, решение 3).

    Attributes:
        parameters: разрешённые параметры калькулятора.
        method_range: границы диапазона метода.
    """

    parameters: object
    method_range: tuple[MethodBound, ...]


class ParameterSource(Protocol):
    """Откуда берутся нормативные параметры типа расчёта: из нормативного каталога.

    Источник получает входы, потому что табличное значение может зависеть от входа.
    """

    def resolve(
        self, calculation_type: str, inputs: Mapping[str, QuantityValue]
    ) -> ResolvedParameters: ...

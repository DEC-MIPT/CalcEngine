from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from app.schemas.calculation import MethodBound, ParameterSourceInfo, QuantityValue


@dataclass(frozen=True)
class ResolvedParameters:
    """Нормативные параметры одного расчёта.

    Это типизированные параметры калькулятора и диапазон применимости метода
    (``calculation-api`` design.md, решение 3).

    Attributes:
        parameters: разрешённые параметры калькулятора.
        method_range: границы диапазона метода.
        source: откуда пришли параметры; ``None`` у источника без описания (тестовый
            дублёр), тогда у конверта нет ``parameter_source`` (``interim-normatives-source``
            design.md, решение 5).
    """

    parameters: object
    method_range: tuple[MethodBound, ...]
    source: ParameterSourceInfo | None = None


class ParameterSource(Protocol):
    """Откуда берутся нормативные параметры типа расчёта: из нормативного каталога.

    Источник получает входы, потому что табличное значение может зависеть от входа.
    """

    def resolve(
        self, calculation_type: str, inputs: Mapping[str, QuantityValue]
    ) -> ResolvedParameters: ...

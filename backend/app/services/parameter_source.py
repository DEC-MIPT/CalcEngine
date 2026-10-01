from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from app.schemas.calculation import MethodBound, QuantityValue


@dataclass(frozen=True)
class ResolvedParameters:
    """The norm-given parameters of one calculation: the calculator's typed parameters and
    the method's range of application (``calculation-api`` design.md decision 3)."""

    parameters: object
    method_range: tuple[MethodBound, ...]


class ParameterSource(Protocol):
    """Where a calculation type's norm-given parameters come from: the normative catalog.

    It receives the inputs, since a table value can depend on an input.
    """

    def resolve(
        self, calculation_type: str, inputs: Mapping[str, QuantityValue]
    ) -> ResolvedParameters: ...

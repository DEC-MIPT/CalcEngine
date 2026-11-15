from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from app.engine.base import Calculator
from app.engine.legacy_module import LegacyOptions
from app.schemas.calculation import CalculationResult, QuantityValue


class PublicQuantityModule[ParametersT](Protocol):
    def execute_public(
        self, inputs: Mapping[str, QuantityValue], data: ParametersT, options: LegacyOptions,
    ) -> CalculationResult: ...


@dataclass(frozen=True)
class ModuleCalculator[ParametersT](Calculator[Mapping[str, QuantityValue], ParametersT, CalculationResult]):
    module: PublicQuantityModule[ParametersT]

    def calculate(self, inputs: Mapping[str, QuantityValue], parameters: ParametersT) -> CalculationResult:
        return self.module.execute_public(inputs, parameters, LegacyOptions())

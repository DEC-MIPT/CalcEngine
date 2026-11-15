from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ConfigDict, TypeAdapter

from app.core.exceptions import CalculationError
from app.engine.applicability import check_applicability
from app.engine.base import Calculator
from app.engine.boundary import inputs_to_base_units, make_outputs
from app.engine.hashing import input_hash
from app.engine.result import assemble_result
from app.schemas.calculation import (
    BoundViolation,
    CalculationResult,
    CalculationTypeContract,
    CheckStep,
    MethodBound,
    QuantityValue,
    Step,
    ValidatedBound,
)
from app.schemas.module import (
    EngineerFormulaStep,
    ModuleDiagnostic,
    ModuleExecution,
    ModuleMetadata,
    ModuleOutcome,
    ModuleStep,
)
from app.schemas.normatives import CatalogSnapshot


@dataclass(frozen=True)
class CalculatorOutput:
    """Что вычисляет тип расчёта: трассу и неокруглённые выходы.

    Attributes:
        trace: шаги трассы по порядку.
        outputs: неокруглённые выходы по именам величин.
    """

    trace: tuple[Step, ...]
    outputs: Mapping[str, QuantityValue]


class LegacyOptions(BaseModel):
    """Явные диапазоны существующего контракта величин."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    method_range: tuple[MethodBound, ...] = ()
    validated_range: tuple[ValidatedBound, ...] = ()


@dataclass(frozen=True)
class LegacyQuantityModule[ParametersT]:
    """Адаптирует существующий калькулятор без изменения его методики и хеша.

    Args:
        contract: внешний контракт величин и проверок.
        calculator: зарегистрированный чистый калькулятор.
        data_schema: схема разрешённых параметров калькулятора.
    """

    contract: CalculationTypeContract
    calculator: Calculator[Mapping[str, QuantityValue], ParametersT, CalculatorOutput]
    data_schema: TypeAdapter[ParametersT]
    infer_data_schema: bool = False

    @property
    def metadata(self) -> ModuleMetadata:
        return ModuleMetadata(
            identifier=self.contract.name,
            methodology_version="legacy-calculator-v1",
            input_schema_version="legacy-quantities-v1",
            data_schema_version="legacy-parameters-v1",
            options_schema_version="legacy-ranges-v1",
            output_schema_version="legacy-quantities-v1",
            diagnostic_schema_version="legacy-bound-v1",
            identity_policy="legacy",
        )

    @property
    def input_schema(self) -> TypeAdapter[Mapping[str, QuantityValue]]:
        return TypeAdapter(Mapping[str, QuantityValue])

    @property
    def options_schema(self) -> TypeAdapter[LegacyOptions]:
        return TypeAdapter(LegacyOptions)

    @property
    def output_schema(self) -> TypeAdapter[Mapping[str, QuantityValue]]:
        return TypeAdapter(Mapping[str, QuantityValue])

    @property
    def diagnostic_schema(self) -> TypeAdapter[BoundViolation]:
        return TypeAdapter(BoundViolation)

    def normalize(self, inputs: Mapping[str, QuantityValue]) -> Mapping[str, QuantityValue]:
        return inputs_to_base_units(self.contract, inputs)

    def validate(
        self, inputs: Mapping[str, QuantityValue], data: ParametersT, options: LegacyOptions
    ) -> None:
        refusal, _ = check_applicability(inputs, options.method_range, options.validated_range)
        if isinstance(data, CatalogSnapshot) and refusal is None:
            raise CalculationError("a catalog snapshot is valid only for a preflight refusal")

    def identity(
        self, inputs: Mapping[str, QuantityValue], data: ParametersT, options: LegacyOptions
    ) -> str:
        return input_hash(
            self.contract.name,
            inputs,
            {
                "parameters": data,
                "method_range": options.method_range,
                "validated_range": options.validated_range,
            },
        )

    def calculate(
        self, inputs: Mapping[str, QuantityValue], data: ParametersT, options: LegacyOptions
    ) -> ModuleOutcome[Mapping[str, QuantityValue], BoundViolation]:
        refusal, warnings = check_applicability(
            inputs, options.method_range, options.validated_range
        )
        if refusal is not None:
            return ModuleOutcome(
                execution="stopped",
                applicability="not_applicable",
                warnings=warnings,
                diagnostic=ModuleDiagnostic(
                    code="method_bound", source=refusal.bound.source, details=refusal
                ),
                stop_stage="before_calculation",
            )
        result = self.calculator.calculate(inputs, data)
        if not isinstance(result, CalculatorOutput):
            raise CalculationError(
                f"calculator of {self.contract.name!r} returned {type(result).__name__},"
                " not a CalculatorOutput"
            )
        return ModuleOutcome(
            execution="completed",
            applicability="outside_validated_range" if warnings else "applicable",
            outputs=result.outputs,
            trace=result.trace,
            checks=tuple(step for step in result.trace if isinstance(step, CheckStep)),
            warnings=warnings,
        )

    def validate_diagnostic(
        self,
        diagnostic: ModuleDiagnostic[BoundViolation],
        trace: tuple[ModuleStep, ...],
        inputs: Mapping[str, QuantityValue],
        data: ParametersT,
        options: LegacyOptions,
    ) -> None:
        refusal, _ = check_applicability(inputs, options.method_range, options.validated_range)
        if (
            diagnostic.code != "method_bound"
            or diagnostic.details != refusal
            or diagnostic.source != diagnostic.details.bound.source
            or trace
        ):
            raise CalculationError("legacy diagnostic does not match input applicability")

    def adapt_result(
        self, execution: ModuleExecution[Mapping[str, QuantityValue], BoundViolation]
    ) -> CalculationResult:
        outcome = execution.outcome
        refusal = outcome.diagnostic.details if outcome.diagnostic is not None else None
        if any(isinstance(step, EngineerFormulaStep) for step in outcome.trace):
            raise CalculationError("legacy result cannot expose an engineer_formula step")
        trace = tuple(step for step in outcome.trace if not isinstance(step, EngineerFormulaStep))
        return assemble_result(
            self.contract,
            input_hash=execution.input_hash,
            trace=trace,
            outputs=make_outputs(self.contract, outcome.outputs) if outcome.outputs is not None else (),
            warnings=outcome.warnings,
            validated_range=tuple(warning.bound for warning in outcome.warnings),
            refusal=refusal,
        )


def parameter_adapter(parameters: Any) -> TypeAdapter[Any]:
    """Выбирает конкретную схему для совместимого низкоуровневого вызова."""
    return TypeAdapter(type(parameters))

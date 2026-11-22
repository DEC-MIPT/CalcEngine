from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ConfigDict, TypeAdapter

from app.core.exceptions import CalculationError
from app.engine import foundations_shallow_loads as loads
from app.engine.applicability import check_applicability
from app.engine.boundary import inputs_to_base_units
from app.engine.legacy_module import LegacyOptions
from app.engine.module import execute_module, module_run_identity
from app.schemas.calculation import (
    WEIGHTS_CONTACT_INPUTS,
    CalculationResult,
    CalculationTypeContract,
    QuantityValue,
    RoundingRule,
    Source,
    validate_loads_domains,
)
from app.schemas.module import (
    ModuleDiagnostic,
    ModuleExecution,
    ModuleMetadata,
    ModuleOutcome,
    ModuleStep,
)
from app.schemas.parameters import EngineerRule

NAME = "foundations_shallow_weights"
OUTPUT_NAMES = loads.OUTPUT_NAMES
Parameters = loads.Parameters
Outputs = loads.Outputs
Details = loads.Details
ASSEMBLY_RULE = EngineerRule(
    engineer="Аким",
    rationale="Явные веса: V=N+G_fund+G_soil+G_other; M_base=M+Q*h+M_add_base. Нагрузки конструкции на обрезе, дополнительные моменты на подошве; решение инженера 2026-11-22.",
)

INPUTS = tuple(
    loads._input("h", "m", "Расстояние от сечения нагрузок до подошвы", "Независимо от d_1; структурные моменты переносятся по M+Q*h")
    if item.name == "h" else item
    for item in loads.INPUTS if item.name != "d"
) + (
    loads._input("G_fund", "kN", "Вес фундамента", "Вниз, неотрицательный; не включать повторно в N"),
    loads._input("G_soil", "kN", "Вес грунта над подошвой", "Вниз, неотрицательный; для заданной геометрии"),
    loads._input("G_other", "kN", "Прочие добавленные веса", "Вниз, неотрицательные; не включать повторно в N"),
    loads._input("Mx_add_base", "kN*m", "Дополнительный момент на подошве для давления вдоль x=b", "Подписанный; повторно через h не переносится"),
    loads._input("My_add_base", "kN*m", "Дополнительный момент на подошве для давления вдоль y=l", "Подписанный; повторно через h не переносится"),
)

_SYMBOLS = {"G_fund": "G_{fund}", "G_soil": "G_{soil}", "G_other": "G_{other}",
            "Mx_add_base": "M_{x,add,base}", "My_add_base": "M_{y,add,base}"}
INPUTS = tuple(item.model_copy(update={"symbol": _SYMBOLS[item.name]}) if item.name in _SYMBOLS else item for item in INPUTS)


class Inputs(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    b: QuantityValue
    d_1: QuantityValue
    d_b: QuantityValue
    gamma_II: QuantityValue
    gamma_II_prime: QuantityValue
    c_II: QuantityValue
    phi_II: QuantityValue
    l: QuantityValue
    h: QuantityValue
    N: QuantityValue
    Mx: QuantityValue
    My: QuantityValue
    Qx: QuantityValue
    Qy: QuantityValue
    G_fund: QuantityValue
    G_soil: QuantityValue
    G_other: QuantityValue
    Mx_add_base: QuantityValue
    My_add_base: QuantityValue

    def quantities(self) -> dict[str, QuantityValue]:
        return {name: getattr(self, name) for name in type(self).model_fields}


def contract(rounding_rule: RoundingRule, rounding_source: Source) -> CalculationTypeContract:
    return loads.contract(rounding_rule, rounding_source).model_copy(update={"name": NAME, "inputs": INPUTS})


@dataclass(frozen=True)
class FoundationsWeightsModule:
    contract: CalculationTypeContract

    @property
    def metadata(self) -> ModuleMetadata:
        return ModuleMetadata(identifier=NAME, methodology_version="rectangular-explicit-weights-v1",
                              input_schema_version="weights-quantities-v1", data_schema_version="loads-resolved-v1",
                              options_schema_version="loads-ranges-v1", output_schema_version="loads-pressures-v1",
                              diagnostic_schema_version="weights-contact-v1")

    @property
    def input_schema(self) -> TypeAdapter[Inputs]:
        return TypeAdapter(Inputs)

    @property
    def data_schema(self) -> TypeAdapter[Parameters]:
        return TypeAdapter(Parameters)

    @property
    def options_schema(self) -> TypeAdapter[LegacyOptions]:
        return TypeAdapter(LegacyOptions)

    @property
    def output_schema(self) -> TypeAdapter[Outputs]:
        return TypeAdapter(Outputs)

    @property
    def diagnostic_schema(self) -> TypeAdapter[Details]:
        return TypeAdapter(Details)

    def normalize(self, inputs: Inputs) -> Inputs:
        return Inputs(**inputs_to_base_units(self.contract, inputs.quantities()))

    def validate(self, inputs: Inputs, data: Parameters, options: LegacyOptions) -> None:
        validate_loads_domains(inputs.quantities(), explicit_weights=True)
        if options.validated_range:
            raise CalculationError("weights validated range has no engineer admission")

    def identity(self, inputs: Inputs, data: Parameters, options: LegacyOptions) -> str:
        return module_run_identity(self.metadata, inputs, data, options)

    def calculate(self, inputs: Inputs, data: Parameters, options: LegacyOptions) -> ModuleOutcome[Outputs, Details]:
        refusal, warnings = check_applicability(inputs.quantities(), options.method_range, options.validated_range)
        if refusal is not None:
            return ModuleOutcome(execution="stopped", applicability="not_applicable", warnings=warnings,
                                 diagnostic=ModuleDiagnostic(code="method_bound", source=refusal.bound.source, details=refusal),
                                 stop_stage="before_calculation")
        trace, values, corner = loads.pressure_steps(inputs.quantities(), data, assembly_rule=ASSEMBLY_RULE)
        return loads.pressure_outcome(trace, values, corner, data, WEIGHTS_CONTACT_INPUTS)

    def validate_diagnostic(self, diagnostic: ModuleDiagnostic[Details], trace: tuple[ModuleStep, ...], inputs: Inputs,
                            data: Parameters, options: LegacyOptions) -> None:
        expected = self.calculate(inputs, data, options)
        if diagnostic != expected.diagnostic or trace != expected.trace:
            raise CalculationError("weights diagnostic differs from the domain calculation")

    def adapt_result(self, execution: ModuleExecution[Outputs, Details]) -> CalculationResult:
        return loads.FoundationsLoadsModule(self.contract).adapt_result(execution)

    def execute_public(self, inputs: Mapping[str, QuantityValue], data: Parameters, options: LegacyOptions) -> CalculationResult:
        execution = execute_module(self, Inputs(**inputs), data, options)
        return self.adapt_result(execution)


def register(registry: Any, entries: Mapping[str, Any]) -> None:
    from app.engine.registry import CalculatorRegistry

    if not isinstance(registry, CalculatorRegistry):
        raise CalculationError("weights registry is not a calculator registry")
    typed = dict(entries)
    if set(typed) != set(OUTPUT_NAMES):
        raise CalculationError("weights requires a rounding entry for every output")
    first = typed["R"]
    declared = contract(first.rule, first.source)
    declared = declared.model_copy(update={"outputs": tuple(output.model_copy(update={
        "rounding_rule": typed[output.name].rule, "rounding_source": typed[output.name].source}) for output in declared.outputs)})
    registry.register_module(declared, FoundationsWeightsModule(declared))

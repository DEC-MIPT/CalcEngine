import math
from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, TypeAdapter, model_validator

from app.core.exceptions import CalculationError, ExpressionError
from app.engine import ENGINE_VERSION
from app.engine.applicability import check_applicability
from app.engine.boundary import inputs_to_base_units, make_outputs
from app.engine.foundations_shallow_r import INPUTS as R_INPUTS
from app.engine.foundations_shallow_r import Parameters as ResistanceParameters
from app.engine.foundations_shallow_r import resistance_steps
from app.engine.legacy_module import LegacyOptions
from app.engine.module import execute_module, module_run_identity, module_sources
from app.engine.steps import check_step, formula_step, table_step
from app.schemas.calculation import (
    CONTACT_INPUTS,
    CONTACT_RULE,
    BoundViolation,
    CalculationResult,
    CalculationTypeContract,
    CheckReason,
    DerivedViolation,
    FormulaStep,
    OutputDeclaration,
    QuantityDeclaration,
    QuantityValue,
    RoundingRule,
    Source,
    Substitution,
    unverified_steps,
    validate_loads_domains,
    verdict_of,
)
from app.schemas.calculation import (
    EngineerFormulaStep as PublicEngineerFormulaStep,
)
from app.schemas.module import (
    EngineerFormulaStep,
    ModuleDiagnostic,
    ModuleExecution,
    ModuleMetadata,
    ModuleOutcome,
    ModuleStep,
)
from app.schemas.parameters import EngineerRule
from app.schemas.resolved import (
    ApplicabilityCondition,
    DiagramCases,
    Formula,
    TableValue,
)
from app.schemas.text import LocalizedText

NAME = "foundations_shallow_loads"
CHECKS = ("p_le_R", "p_x_max_le_limit", "p_y_max_le_limit", "p_corner_max_le_limit")
OUTPUTS = ("R", "p", "p_x_min", "p_x_max", "p_y_min", "p_y_max",
           "p_corner_pp", "p_corner_pm", "p_corner_mp", "p_corner_mm")
GEOMETRY_RULE = EngineerRule(engineer="Аким", rationale="Геометрия прямоугольной подошвы: A=b*l, Wx=l*b²/6, Wy=b*l²/6; инженерный контракт 2026-11-08.")
TRANSFER_RULE = EngineerRule(engineer="Аким", rationale="Подписанный перенос нагрузок к подошве M_base=M+Q*h; оси x=b и y=l; инженерный контракт 2026-11-08.")
CORNER_RULE = EngineerRule(engineer="Аким", rationale="Подписанные угловые давления из нормативных компонент и выбор экстремумов в порядке pp, pm, mp, mm; инженерный контракт 2026-11-08.")


def _input(name: str, unit: str, label: str, hint: str | None = None) -> QuantityDeclaration:
    return QuantityDeclaration(name=name, base_unit=unit, symbol={"Mx": "M_x", "My": "M_y", "Qx": "Q_x", "Qy": "Q_y"}.get(name, name), label=LocalizedText(ru=label),
                               hint=LocalizedText(ru=hint) if hint else None)


INPUTS = (*R_INPUTS[:7],
          _input("l", "m", "Длина подошвы по оси y", "l ≥ b; стороны и нагрузки автоматически не переставляются"),
          _input("h", "m", "Расстояние от сечения нагрузок до подошвы", "Независимо от d и d_1; моменты переносятся по M+Q*h"),
          _input("d", "m", "Толщина в весовом слагаемом", "Независима от h и d_1; вес учитывается через γ_mt*d"),
          _input("N", "kN", "Вертикальная нагрузка", "Без собственного веса фундамента и грунта над подошвой; вес добавляется один раз"),
          _input("Mx", "kN*m", "Подписанный момент для давления вдоль x=b"),
          _input("My", "kN*m", "Подписанный момент для давления вдоль y=l"),
          _input("Qx", "kN", "Подписанная поперечная сила вдоль x=b"),
          _input("Qy", "kN", "Подписанная поперечная сила вдоль y=l"))


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
    d: QuantityValue
    N: QuantityValue
    Mx: QuantityValue
    My: QuantityValue
    Qx: QuantityValue
    Qy: QuantityValue

    def quantities(self) -> dict[str, QuantityValue]:
        return {name: getattr(self, name) for name in type(self).model_fields}


class Outputs(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    R: QuantityValue
    p: QuantityValue
    p_x_min: QuantityValue
    p_x_max: QuantityValue
    p_y_min: QuantityValue
    p_y_max: QuantityValue
    p_corner_pp: QuantityValue
    p_corner_pm: QuantityValue
    p_corner_mp: QuantityValue
    p_corner_mm: QuantityValue

    @model_validator(mode="after")
    def _pressure_units(self) -> "Outputs":
        if any(value.unit != "kPa" for value in self.quantities().values()):
            raise ValueError("loads outputs must use the kPa base unit")
        return self

    def quantities(self) -> dict[str, QuantityValue]:
        return {name: getattr(self, name) for name in type(self).model_fields}


class Parameters(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    resistance: ResistanceParameters
    p_edge_plus: Formula
    p_edge_minus: Formula
    p_corner: Formula
    gamma_mt: TableValue
    edge_pressure_limit_multiplier: TableValue
    corner_pressure_limit_multiplier: TableValue
    edge_limit: Formula
    corner_limit: Formula
    applicability_condition: ApplicabilityCondition
    diagram_cases: DiagramCases


Details = BoundViolation | DerivedViolation


def contract(rounding_rule: RoundingRule, rounding_source: Source) -> CalculationTypeContract:
    labels = ("Расчётное сопротивление грунта", "Среднее давление", "Минимальное давление по x",
              "Максимальное давление по x", "Минимальное давление по y", "Максимальное давление по y",
              "Угловое давление (+x,+y)", "Угловое давление (+x,-y)",
              "Угловое давление (-x,+y)", "Угловое давление (-x,-y)")
    symbols = ("R", "p", "p_{x,min}", "p_{x,max}", "p_{y,min}", "p_{y,max}", "p_{++}", "p_{+-}", "p_{-+}", "p_{--}")
    return CalculationTypeContract(name=NAME, inputs=INPUTS, outputs=tuple(
        OutputDeclaration(name=name, base_unit="kPa", label=LocalizedText(ru=label), symbol=symbol,
                          rounding_rule=rounding_rule, rounding_source=rounding_source)
        for name, label, symbol in zip(OUTPUTS, labels, symbols, strict=True)), checks=CHECKS)


def _quantity(value: float, unit: str) -> QuantityValue:
    if not math.isfinite(value):
        raise ExpressionError("non-finite loads intermediate")
    return QuantityValue(value=value, unit=unit)


def pressure_steps(inputs: Mapping[str, QuantityValue], data: Parameters) -> tuple[tuple[ModuleStep, ...], dict[str, QuantityValue], str]:
    values = dict(inputs)
    prefix, resistance = resistance_steps(inputs, data.resistance)
    trace: list[ModuleStep] = list(prefix)
    values["R"] = resistance.result

    def engineer(name: str, expression: str, value: float, unit: str, used: tuple[str, ...], rule: EngineerRule) -> None:
        result = _quantity(value, unit)
        trace.append(EngineerFormulaStep(step_id=name, expression=expression, substitutions=tuple(
            Substitution(symbol=key, value=values[key].value, unit=values[key].unit) for key in used),
            result=result, source=rule))
        values[name] = result

    b, length, height = (inputs[name].value for name in ("b", "l", "h"))
    try:
        engineer("A", "A=b l", b * length, "m2", ("b", "l"), GEOMETRY_RULE)
        engineer("Wx", "W_x=l b^2/6", length * b * b / 6, "m3", ("b", "l"), GEOMETRY_RULE)
        engineer("Wy", "W_y=b l^2/6", b * length * length / 6, "m3", ("b", "l"), GEOMETRY_RULE)
        for axis in ("x", "y"):
            moment, shear = f"M{axis}", f"Q{axis}"
            engineer(f"M{axis}_base", f"M_{{{axis},base}}=M_{axis}+Q_{axis} h",
                     inputs[moment].value + inputs[shear].value * height, "kN*m",
                     (moment, shear, "h"), TRANSFER_RULE)
        gamma = table_step("gamma_mt", data.gamma_mt, {})
        trace.append(gamma)
        values["gamma_mt"] = gamma.result
        mean_values = values | {"M": _quantity(0, "kN*m"), "W": values["Wx"]}
        mean = formula_step("p", data.p_edge_plus, mean_values)
        trace.append(mean)
        values["p"] = mean.result
        engineer("V", "V=N+\\gamma_{mt} d A", inputs["N"].value + gamma.result.value * inputs["d"].value * values["A"].value,
                 "kN", ("N", "gamma_mt", "d", "A"), CORNER_RULE)
        for axis in ("x", "y"):
            moment_value = values[f"M{axis}_base"]
            modulus = values[f"W{axis}"]
            for suffix, expression in (("min", data.p_edge_minus), ("max", data.p_edge_plus)):
                step = formula_step(f"p_{axis}_{suffix}", expression, values | {"M": _quantity(abs(moment_value.value), "kN*m"), "W": modulus})
                trace.append(step)
                values[step.step_id] = step.result
            engineer(f"e_{axis}", f"e_{axis}=|M_{{{axis},base}}|/V", abs(moment_value.value) / values["V"].value,
                     "m", (f"M{axis}_base", "V"), CORNER_RULE)
            ratio = values[f"e_{axis}"].value / inputs["b" if axis == "x" else "l"].value
            condition = data.applicability_condition
            fraction = Fraction(condition.value_fraction.numerator, condition.value_fraction.denominator)
            exact_ratio = Fraction(abs(moment_value.value)) / (Fraction(values["V"].value) * Fraction(inputs["b" if axis == "x" else "l"].value))
            relations = {"lt": exact_ratio < fraction, "le": exact_ratio <= fraction, "eq": exact_ratio == fraction,
                         "ge": exact_ratio >= fraction, "gt": exact_ratio > fraction}
            trace.append(FormulaStep(step_id=f"relative_eccentricity_{axis}", expression=condition.latex,
                substitutions=(Substitution(symbol="e/L", value=ratio, unit="1"),
                               Substitution(symbol="numerator", value=condition.value_fraction.numerator, unit="1"),
                               Substitution(symbol="denominator", value=condition.value_fraction.denominator, unit="1")),
                result=_quantity(float(relations[condition.relation]), "1"), norm_refs=condition.norm_refs))
            if len(data.diagram_cases.cases) != 3:
                raise CalculationError("loads pressure diagram requires its three prepared cases")
            if exact_ratio <= fraction:
                case = data.diagram_cases.cases[0 if exact_ratio < fraction else 1]
                trace.append(FormulaStep(step_id=f"pressure_diagram_{axis}", expression=case.condition_latex,
                    substitutions=(Substitution(symbol="e", value=values[f"e_{axis}"].value, unit="m"),
                                   Substitution(symbol="l", value=inputs["b" if axis == "x" else "l"].value, unit="m")),
                    result=values[f"e_{axis}"], norm_refs=data.diagram_cases.norm_refs))
        for suffix, sign_x, sign_y in (("pp", 1, 1), ("pm", 1, -1), ("mp", -1, 1), ("mm", -1, -1)):
            component = formula_step(f"corner_component_{suffix}", data.p_corner, values | {
                "M_x": _quantity(sign_x * values["Mx_base"].value, "kN*m"),
                "M_y": _quantity(sign_y * values["My_base"].value, "kN*m"),
                "W_x": values["Wx"], "W_y": values["Wy"]})
            trace.append(component)
            values[component.step_id] = component.result
            values[f"sign_x_{suffix}"] = _quantity(sign_x, "1")
            values[f"sign_y_{suffix}"] = _quantity(sign_y, "1")
            engineer(f"p_corner_{suffix}", f"p_{{{suffix}}}=p+s_x M_{{x,base}}/W_x+s_y M_{{y,base}}/W_y", component.result.value,
                     "kPa", ("p", "Mx_base", "Wx", "My_base", "Wy", f"sign_x_{suffix}", f"sign_y_{suffix}", component.step_id), CORNER_RULE)
        corners = tuple(f"p_corner_{suffix}" for suffix in ("pp", "pm", "mp", "mm"))
        minimum = min(corners, key=lambda name: values[name].value)
        engineer("p_corner_min", "p_{corner,min}=\\min(p_{++},p_{+-},p_{-+},p_{--})", values[minimum].value,
                 "kPa", corners, CONTACT_RULE)
        engineer("p_corner_max", "p_{corner,max}=\\max(p_{++},p_{+-},p_{-+},p_{--})", max(values[name].value for name in corners),
                 "kPa", corners, CORNER_RULE)
    except (ZeroDivisionError, OverflowError) as exc:
        raise ExpressionError("invalid loads intermediate arithmetic") from exc
    return tuple(trace), values, minimum.removeprefix("p_corner_")



@dataclass(frozen=True)
class FoundationsLoadsModule:
    contract: CalculationTypeContract

    @property
    def metadata(self) -> ModuleMetadata:
        return ModuleMetadata(identifier=NAME, methodology_version="rectangular-full-contact-v1",
            input_schema_version="loads-quantities-v1", data_schema_version="loads-resolved-v1",
            options_schema_version="loads-ranges-v1", output_schema_version="loads-pressures-v1",
            diagnostic_schema_version="loads-contact-v1")

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
        validate_loads_domains(inputs.quantities())
        if options.validated_range:
            raise CalculationError("loads validated range has no engineer admission")

    def identity(self, inputs: Inputs, data: Parameters, options: LegacyOptions) -> str:
        return module_run_identity(self.metadata, inputs, data, options)

    def calculate(self, inputs: Inputs, data: Parameters, options: LegacyOptions) -> ModuleOutcome[Outputs, Details]:
        refusal, warnings = check_applicability(inputs.quantities(), options.method_range, options.validated_range)
        if refusal is not None:
            return ModuleOutcome(execution="stopped", applicability="not_applicable", warnings=warnings,
                diagnostic=ModuleDiagnostic(code="method_bound", source=refusal.bound.source, details=refusal), stop_stage="before_calculation")
        trace, values, corner = pressure_steps(inputs.quantities(), data)
        if values["p_corner_min"].value < 0:
            reason = DerivedViolation(value=values["p_corner_min"], limit=QuantityValue(value=0, unit="kPa"), source=CONTACT_RULE,
                                      related_inputs=CONTACT_INPUTS, limiting_corner=cast(Literal["pp", "pm", "mp", "mm"], corner))
            return ModuleOutcome(execution="stopped", applicability="not_applicable", trace=trace,
                diagnostic=ModuleDiagnostic(code="full_contact", step_id=reason.step_id, source=reason.source, details=reason), stop_stage="after_start")
        edge_factor = table_step("edge_limit_multiplier", data.edge_pressure_limit_multiplier, {})
        edge_limit = formula_step("edge_limit", data.edge_limit, values | {data.edge_pressure_limit_multiplier.symbol: edge_factor.result})
        corner_factor = table_step("corner_limit_multiplier", data.corner_pressure_limit_multiplier, {})
        corner_limit = formula_step("corner_limit", data.corner_limit, values | {data.corner_pressure_limit_multiplier.symbol: corner_factor.result})
        checks = (
            check_step(CHECKS[0], ("p", values["p"]), "le", ("R", values["R"]), data.resistance.check_norm_refs),
            check_step(CHECKS[1], ("p_x_max", values["p_x_max"]), "le", ("edge_limit", edge_limit.result), data.edge_pressure_limit_multiplier.norm_refs),
            check_step(CHECKS[2], ("p_y_max", values["p_y_max"]), "le", ("edge_limit", edge_limit.result), data.edge_pressure_limit_multiplier.norm_refs),
            check_step(CHECKS[3], ("p_corner_max", values["p_corner_max"]), "le", ("corner_limit", corner_limit.result), data.corner_pressure_limit_multiplier.norm_refs))
        return ModuleOutcome(execution="completed", applicability="applicable", outputs=Outputs(**{key: values[key] for key in OUTPUTS}),
            trace=(*trace, edge_factor, edge_limit, corner_factor, corner_limit, *checks), checks=checks)

    def validate_diagnostic(self, diagnostic: ModuleDiagnostic[Details], trace: tuple[ModuleStep, ...], inputs: Inputs,
                            data: Parameters, options: LegacyOptions) -> None:
        expected = self.calculate(inputs, data, options)
        if diagnostic != expected.diagnostic or trace != expected.trace:
            raise CalculationError("loads diagnostic differs from the domain calculation")

    def adapt_result(self, execution: ModuleExecution[Outputs, Details]) -> CalculationResult:
        outcome = execution.outcome
        public_trace = tuple(PublicEngineerFormulaStep.model_validate(step.model_dump()) if isinstance(step, EngineerFormulaStep) else step for step in outcome.trace)
        verdict: Literal["pass", "fail", "refused"]
        if outcome.diagnostic is None:
            if outcome.outputs is None:
                raise CalculationError("completed loads result lacks outputs")
            outputs = make_outputs(self.contract, outcome.outputs.quantities())
            verdict, deciding = verdict_of(public_trace)
            reason: CheckReason | Details = CheckReason(step_id=deciding)
        else:
            outputs = ()
            verdict = "refused"
            reason = outcome.diagnostic.details
        norms, rules = module_sources(outcome, [output.rounding_source for output in outputs])
        return CalculationResult(engine_version=ENGINE_VERSION, input_hash=execution.input_hash, outputs=outputs,
            norm_refs=norms, engineer_rules=rules, verdict=verdict, verdict_reason=reason,
            warnings=outcome.warnings, trace=public_trace, unverified_step_count=unverified_steps(public_trace))

    def execute_public(self, inputs: Mapping[str, QuantityValue], data: Parameters, options: LegacyOptions) -> CalculationResult:
        execution = execute_module(self, Inputs(**inputs), data, options)
        return self.adapt_result(execution)


OUTPUT_NAMES = OUTPUTS


def register(registry: Any, entries: Mapping[str, Any]) -> None:
    from app.engine.registry import CalculatorRegistry

    if not isinstance(registry, CalculatorRegistry):
        raise CalculationError("loads registry is not a calculator registry")
    typed = dict(entries)
    if set(typed) != set(OUTPUTS):
        raise CalculationError("loads requires a rounding entry for every output")
    first = typed["R"]
    declared = contract(first.rule, first.source)
    declared = declared.model_copy(update={"outputs": tuple(output.model_copy(update={
        "rounding_rule": typed[output.name].rule, "rounding_source": typed[output.name].source}) for output in declared.outputs)})
    registry.register_module(declared, FoundationsLoadsModule(declared))

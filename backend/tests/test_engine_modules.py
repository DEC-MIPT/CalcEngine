from dataclasses import dataclass
from typing import Any, Literal

import pytest
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    TypeAdapter,
    ValidationError,
)
from test_engine_purity import sealed  # noqa: F401

from app.core.exceptions import CalculationError, DECError
from app.engine.boundary import convert
from app.engine.module import (
    ModuleRegistry,
    execute_module,
    module_canonical_json,
    module_run_identity,
    module_sources,
    module_traceability,
)
from app.engine.steps import check_step
from app.schemas.calculation import (
    ApplicabilityWarning,
    FormulaStep,
    NormRef,
    QuantityValue,
    Substitution,
    ValidatedBound,
)
from app.schemas.module import (
    EngineerFormulaStep,
    ModuleDiagnostic,
    ModuleExecution,
    ModuleMetadata,
    ModuleOutcome,
)
from app.schemas.parameters import EngineerRule

RULE = EngineerRule(engineer="<ENGINEER>", rationale="<SYNTHETIC-RULE>")
OTHER_RULE = EngineerRule(engineer="<OTHER-ENGINEER>", rationale="<OTHER-RULE>")
REF = NormRef(
    document="<SYNTHETIC-DOCUMENT>",
    edition="unverified",
    clause="<SYNTHETIC-CLAUSE>",
    status="unverified",
    provenance="machine-extracted",
)
VERIFIED = REF.model_copy(update={"edition": "<EDITION>", "status": "verified", "provenance": "human-verified"})


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False, strict=True)


class Inputs(StrictModel):
    lengths: list[QuantityValue]
    serial: int = 2**53 + 1


class Data(StrictModel):
    factor: float = 2.0
    reference: NormRef = REF


class Options(StrictModel):
    mode: Literal["complete", "before", "after"] = "complete"
    limit: float = 10.0
    warn: bool = False


class Outputs(StrictModel):
    total: QuantityValue


class Details(StrictModel):
    observed: QuantityValue
    input_name: Literal["lengths"] = "lengths"


def metadata(**changes: Any) -> ModuleMetadata:
    return ModuleMetadata.model_validate({
        "identifier": "synthetic-structured",
        "methodology_version": "1",
        "input_schema_version": "1",
        "data_schema_version": "1",
        "options_schema_version": "1",
        "output_schema_version": "1",
        "diagnostic_schema_version": "1",
        "identity_policy": "v1",
    } | changes)


def engineer_step(step_id: str = "total", source: EngineerRule = RULE) -> EngineerFormulaStep:
    return EngineerFormulaStep(
        step_id=step_id, expression="t=x", substitutions=(),
        result=QuantityValue(value=4.0, unit="m"), source=source,
    )


class StructuredModule:
    metadata = metadata()
    input_schema = TypeAdapter(Inputs)
    data_schema = TypeAdapter(Data)
    options_schema = TypeAdapter(Options)
    output_schema = TypeAdapter(Outputs)
    diagnostic_schema = TypeAdapter(Details)

    def normalize(self, inputs: Inputs) -> Inputs:
        return Inputs(lengths=[convert(value, "m") for value in inputs.lengths], serial=inputs.serial)

    def validate(self, inputs: Inputs, data: Data, options: Options) -> None:
        if not inputs.lengths or data.factor <= 0:
            raise CalculationError("synthetic domain validation failed")

    def calculate(self, inputs: Inputs, data: Data, options: Options) -> ModuleOutcome[Outputs, Details]:
        if options.mode == "before":
            return ModuleOutcome[Outputs, Details](
                execution="stopped", applicability="not_applicable", stop_stage="before_calculation",
                diagnostic=ModuleDiagnostic[Details](
                    code="synthetic_preflight", source=RULE, details=Details(observed=inputs.lengths[0]),
                ),
            )
        total = QuantityValue(value=sum(value.value for value in inputs.lengths) * data.factor, unit="m")
        step = engineer_step().model_copy(update={"result": total})
        if options.mode == "after":
            return ModuleOutcome[Outputs, Details](
                execution="stopped", applicability="not_applicable", stop_stage="after_start", trace=(step,),
                diagnostic=ModuleDiagnostic[Details](
                    code="synthetic_derived", source=RULE, step_id="total", details=Details(observed=total),
                ),
            )
        norm = FormulaStep(
            step_id="copy", expression="y=t", substitutions=(), result=total, norm_refs=(data.reference,),
        )
        check = check_step("limit", ("y", total), "le", ("limit", QuantityValue(value=options.limit, unit="m")), (data.reference,))
        warnings = () if not options.warn else (
            ApplicabilityWarning(value=inputs.lengths[0], bound=ValidatedBound(
                quantity="lengths", kind="max", value=1.0, inclusive=True, source=OTHER_RULE,
            )),
        )
        return ModuleOutcome[Outputs, Details](
            execution="completed", applicability="outside_validated_range" if options.warn else "applicable",
            outputs=Outputs(total=total), trace=(step, norm, check), checks=(check,), warnings=warnings,
        )

    def validate_diagnostic(self, diagnostic: ModuleDiagnostic[Details], trace: Any, inputs: Inputs, data: Data, options: Options) -> None:
        if diagnostic.code == "synthetic_derived" and diagnostic.details.observed != trace[-1].result:
            raise CalculationError("synthetic diagnostic disagrees with trace")

    def identity(self, inputs: Inputs, data: Data, options: Options) -> str:
        return module_run_identity(self.metadata, inputs, data, options)

    def adapt_result(self, execution: ModuleExecution[Outputs, Details]) -> str:
        return execution.outcome.execution


def run(module: Any = None, *, inputs: Any = None, data: Any = None, options: Any = None) -> ModuleExecution[Outputs, Details]:
    return execute_module(
        StructuredModule() if module is None else module,
        Inputs(lengths=[QuantityValue(value=2.0, unit="m")]) if inputs is None else inputs,
        Data() if data is None else data,
        Options() if options is None else options,
    )


def test_structured_module_executes_without_flattening_and_adapts_explicitly() -> None:
    module = StructuredModule()
    result = run(module)

    assert result.metadata == module.metadata
    assert result.outcome.outputs == Outputs(total=QuantityValue(value=4.0, unit="m"))
    assert [step.step_id for step in result.outcome.trace] == ["total", "copy", "limit"]
    assert module.adapt_result(result) == "completed"


def test_engineering_failure_is_a_completed_applicable_execution() -> None:
    result = run(options=Options(limit=3.0)).outcome

    assert (result.execution, result.applicability) == ("completed", "applicable")
    assert result.checks[0].passed is False
    assert result.diagnostic is None


@pytest.mark.parametrize("mode,stage,ids", [("before", "before_calculation", []), ("after", "after_start", ["total"])])
def test_stops_preserve_only_completed_diagnostics(mode: str, stage: str, ids: list[str]) -> None:
    outcome = run(options=Options.model_validate({"mode": mode})).outcome

    assert (outcome.execution, outcome.applicability, outcome.stop_stage) == ("stopped", "not_applicable", stage)
    assert outcome.outputs is None
    assert outcome.checks == ()
    assert [step.step_id for step in outcome.trace] == ids
    assert outcome.diagnostic is not None
    assert outcome.diagnostic.step_id == (ids[-1] if ids else None)


def test_completed_validated_range_warning_is_independent_of_check_result() -> None:
    outcome = run(options=Options(warn=True, limit=3.0)).outcome

    assert outcome.applicability == "outside_validated_range"
    assert len(outcome.warnings) == 1
    assert outcome.checks[0].passed is False


@pytest.mark.usefixtures("sealed")
def test_module_executor_works_without_io_clock_or_randomness() -> None:
    assert run().outcome.execution == "completed"


def test_repeated_interleaved_calls_normalize_units_and_preserve_caller_objects() -> None:
    module = StructuredModule()
    inputs = Inputs(lengths=[QuantityValue(value=2000.0, unit="mm")])
    data, options = Data(), Options()
    before = (inputs.model_dump_json(), data.model_dump_json(), options.model_dump_json())

    first = run(module, inputs=inputs, data=data, options=options)
    run(inputs=Inputs(lengths=[QuantityValue(value=3.0, unit="m")]))
    second = run(module, inputs=inputs, data=data, options=options)

    assert first == second == run()
    assert first.model_dump_json() == second.model_dump_json()
    assert (inputs.model_dump_json(), data.model_dump_json(), options.model_dump_json()) == before


def test_defective_callback_cannot_mutate_caller_nested_input() -> None:
    class MutatingModule(StructuredModule):
        def normalize(self, inputs: Inputs) -> Inputs:
            inputs.lengths.append(QuantityValue(value=1.0, unit="m"))
            return super().normalize(inputs)

    inputs = Inputs(lengths=[QuantityValue(value=2.0, unit="m")])
    result = run(MutatingModule(), inputs=inputs)

    assert len(inputs.lengths) == 1
    assert result.outcome.outputs == Outputs(total=QuantityValue(value=6.0, unit="m"))


@pytest.mark.parametrize("field,value", [
    ("inputs", {"lengths": [], "unknown": 1}),
    ("inputs", {"lengths": [{"value": float("inf"), "unit": "m"}]}),
    ("inputs", Inputs.model_construct(lengths=[QuantityValue.model_construct(value=float("nan"), unit="m")])),
    ("inputs", {"lengths": [{"value": 1.0, "unit": "m"}], "serial": "4"}),
    ("data", {"factor": float("nan")}),
    ("data", Data.model_construct(factor=float("inf"), reference=REF)),
    ("options", {"limit": float("inf")}),
    ("options", {"limit": 1.0, "extra": True}),
])
def test_invalid_typed_payloads_fail_before_computation(field: str, value: Any) -> None:
    class UnreachableModule(StructuredModule):
        def calculate(self, inputs: Inputs, data: Data, options: Options) -> Any:
            pytest.fail("invalid input reached computation")

    with pytest.raises((DECError, ValidationError)):
        run(UnreachableModule(), **{field: value})


def test_domain_errors_remain_errors_rather_than_refusals() -> None:
    with pytest.raises(CalculationError, match="domain validation"):
        run(inputs=Inputs(lengths=[]))


def test_dataclass_payload_is_checked_against_the_declared_model_schema() -> None:
    @dataclass(frozen=True)
    class ResolvedRecord:
        factor: float
        reference: NormRef

    assert run(data=ResolvedRecord(2.0, REF)) == run()


def test_normalizer_result_is_revalidated_before_domain_computation() -> None:
    class InvalidNormalizer(StructuredModule):
        def normalize(self, inputs: Inputs) -> Inputs:
            return inputs.model_copy(update={"serial": "not an integer"})

    with pytest.raises((DECError, ValidationError)):
        run(InvalidNormalizer())


@pytest.mark.parametrize("change", [
    {"execution": "completed", "applicability": "not_applicable"},
    {"outputs": None},
    {"stop_stage": "after_start"},
    {"applicability": "outside_validated_range"},
    {"checks": ()},
    {"trace": (engineer_step(), engineer_step())},
    {"outputs": {"wrong": 3}},
    {"outputs": Outputs.model_construct(total=QuantityValue.model_construct(value=float("inf"), unit="m"))},
    {"unrecognized": True},
])
def test_executor_revalidates_module_outcome_including_bypassed_models(change: dict[str, Any]) -> None:
    class InvalidOutcome(StructuredModule):
        def calculate(self, inputs: Inputs, data: Data, options: Options) -> Any:
            return super().calculate(inputs, data, options).model_copy(update=change)

    with pytest.raises(CalculationError):
        run(InvalidOutcome())


@pytest.mark.parametrize("carrier", [
    "check_passed", "trace_result", "substitution_value", "check_right",
    "warning_value", "warning_bound_inclusive", "normative_source_shape",
])
def test_shared_outcome_rejects_bypassed_wrong_primitive_types_before_adaptation(carrier: str) -> None:
    class WrongSharedPrimitive(StructuredModule):
        def calculate(self, inputs: Inputs, data: Data, options: Options) -> Any:
            outcome = super().calculate(inputs, data, options)
            trace = list(outcome.trace)
            changes: dict[str, Any] = {}
            if carrier == "check_passed":
                check = outcome.checks[0].model_copy(update={"passed": "false"})
                trace[-1] = check
                changes["checks"] = (check,)
            elif carrier == "trace_result":
                trace[0] = trace[0].model_copy(update={
                    "result": QuantityValue.model_construct(value=True, unit="m"),
                })
            elif carrier == "substitution_value":
                trace[0] = trace[0].model_copy(update={
                    "substitutions": (Substitution.model_construct(symbol="x", value=True, unit="m"),),
                })
            elif carrier == "check_right":
                check = outcome.checks[0].model_copy(update={
                    "right": QuantityValue.model_construct(value=True, unit="m"),
                })
                trace[-1] = check
                changes["checks"] = (check,)
            elif carrier == "warning_value":
                changes["warnings"] = (outcome.warnings[0].model_copy(update={
                    "value": QuantityValue.model_construct(value=True, unit="m"),
                }),)
            elif carrier == "warning_bound_inclusive":
                warning = outcome.warnings[0]
                changes["warnings"] = (warning.model_copy(update={
                    "bound": warning.bound.model_copy(update={"inclusive": "false"}),
                }),)
            else:
                trace[1] = trace[1].model_copy(update={"norm_refs": [data.reference]})
            return outcome.model_copy(update=changes | {"trace": tuple(trace)})

        def adapt_result(self, execution: ModuleExecution[Outputs, Details]) -> str:
            pytest.fail("malformed shared outcome reached result adaptation")

    module = WrongSharedPrimitive()
    with pytest.raises(CalculationError):
        module.adapt_result(run(module, options=Options(warn=True)))


def test_non_outcome_result_is_a_calculation_error() -> None:
    class WrongReturn(StructuredModule):
        def calculate(self, inputs: Inputs, data: Data, options: Options) -> Any:
            return "not an outcome"

    with pytest.raises(CalculationError):
        run(WrongReturn())


@pytest.mark.parametrize("change", [
    {"outputs": Outputs(total=QuantityValue(value=1.0, unit="m"))},
    {"diagnostic": None},
    {"stop_stage": None},
    {"stop_stage": "before_calculation"},
    {"trace": ()},
    {"applicability": "applicable"},
])
def test_stopped_outcome_rejects_contradictions(change: dict[str, Any]) -> None:
    class InvalidStop(StructuredModule):
        def calculate(self, inputs: Inputs, data: Data, options: Options) -> Any:
            return super().calculate(inputs, data, options).model_copy(update=change)

    with pytest.raises(CalculationError):
        run(InvalidStop(), options=Options(mode="after"))


@pytest.mark.parametrize("change", [
    {"step_id": "missing"},
    {"step_id": None},
    {"details": {"limiting_corner": "injected"}},
    {"details": Details(observed=QuantityValue(value=999.0, unit="m"))},
    {"source": ()},
    {"code": ""},
])
def test_module_diagnostics_validate_schema_reference_and_domain_details(change: dict[str, Any]) -> None:
    class InvalidDiagnostic(StructuredModule):
        def calculate(self, inputs: Inputs, data: Data, options: Options) -> Any:
            outcome = super().calculate(inputs, data, options)
            assert outcome.diagnostic is not None
            return outcome.model_copy(update={"diagnostic": outcome.diagnostic.model_copy(update=change)})

    with pytest.raises(CalculationError):
        run(InvalidDiagnostic(), options=Options(mode="after"))


def test_completed_generic_module_can_have_no_engineering_checks() -> None:
    outcome = ModuleOutcome[Outputs, Details](
        execution="completed", applicability="applicable", outputs=Outputs(total=QuantityValue(value=2.0, unit="m")),
    )

    assert outcome.checks == ()


def test_registry_uses_trusted_objects_and_rejects_duplicate_unknown_or_invalid_entries() -> None:
    registry = ModuleRegistry()
    module = StructuredModule()
    registry.register(module)

    assert registry.get(module.metadata.identifier) is module
    with pytest.raises(DECError):
        registry.register(StructuredModule())
    with pytest.raises(DECError):
        registry.get("missing")
    for field in ("identifier", "methodology_version", "input_schema_version", "data_schema_version", "options_schema_version", "output_schema_version", "diagnostic_schema_version"):
        invalid = StructuredModule()
        invalid.metadata = metadata().model_copy(update={field: ""})
        with pytest.raises(DECError):
            ModuleRegistry().register(invalid)
    missing = StructuredModule()
    missing.output_schema = None  # type: ignore[assignment]
    with pytest.raises(DECError):
        ModuleRegistry().register(missing)
    invalid_callback = StructuredModule()
    invalid_callback.adapt_result = None  # type: ignore[assignment]
    with pytest.raises(DECError):
        ModuleRegistry().register(invalid_callback)


def test_new_module_registration_needs_no_executor_edit() -> None:
    class AnotherModule(StructuredModule):
        metadata = metadata(identifier="another-structured")

    registry = ModuleRegistry()
    registry.register(StructuredModule())
    registry.register(AnotherModule())

    result = run(registry.get("another-structured"))
    assert result.metadata.identifier == "another-structured"
    assert result.input_hash != run().input_hash


@pytest.mark.parametrize("field", ["identifier", "methodology_version", "input_schema_version", "data_schema_version", "options_schema_version", "output_schema_version", "diagnostic_schema_version"])
def test_new_identity_covers_each_metadata_version(field: str) -> None:
    inputs, data, options = Inputs(lengths=[]), Data(), Options()
    assert module_run_identity(metadata(), inputs, data, options) != module_run_identity(metadata(**{field: "changed"}), inputs, data, options)


def test_new_identity_covers_resolved_sources_and_all_execution_settings() -> None:
    inputs, data, options = Inputs(lengths=[]), Data(), Options()
    original = module_run_identity(metadata(), inputs, data, options)

    for changed in (data.model_copy(update={"factor": 3.0}), data.model_copy(update={"reference": VERIFIED})):
        assert module_run_identity(metadata(), inputs, changed, options) != original
    assert module_run_identity(metadata(), inputs, data, Options(limit=11.0)) != original
    assert module_run_identity(metadata(), inputs.model_copy(update={"serial": 2**53}), data, options) != original


def test_versioned_identity_cannot_silently_replace_legacy_policy() -> None:
    with pytest.raises(CalculationError, match="v1 policy"):
        module_run_identity(metadata(identity_policy="legacy"), {}, {}, {})


def test_new_module_cannot_override_versioned_identity_with_a_constant_hash() -> None:
    class ConstantIdentity(StructuredModule):
        def identity(self, inputs: Inputs, data: Data, options: Options) -> str:
            return "0" * 64

        def calculate(self, inputs: Inputs, data: Data, options: Options) -> Any:
            pytest.fail("computation ran with an invalid identity")

    with pytest.raises(CalculationError, match="identity"):
        run(ConstantIdentity())


def test_legacy_module_identity_still_has_to_be_a_sha256_value() -> None:
    class MalformedLegacyIdentity(StructuredModule):
        metadata = metadata(identity_policy="legacy")

        def identity(self, inputs: Inputs, data: Data, options: Options) -> str:
            return "not-a-hash"

    with pytest.raises(CalculationError):
        run(MalformedLegacyIdentity())


def test_v1_json_preserves_large_integers_types_keys_and_sequence_order() -> None:
    assert module_canonical_json({"x": 2**53 + 1}) != module_canonical_json({"x": 2**53})
    assert module_canonical_json({"x": 1}) != module_canonical_json({"x": 1.0})
    assert module_canonical_json({"b": 2, "a": 1}) == module_canonical_json({"a": 1, "b": 2})
    assert module_canonical_json([1, 2]) != module_canonical_json([2, 1])
    assert module_canonical_json({"x": True, "y": None, "z": "тест"}) == '{"x":true,"y":null,"z":"тест"}'


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), {1: "collision"}, {"x": object()}, {"x": {1, 2}}])
def test_v1_json_rejects_unsupported_or_nonfinite_identity_values(value: Any) -> None:
    with pytest.raises(CalculationError):
        module_canonical_json(value)


def test_engineer_steps_cannot_claim_norm_references_or_normative_verification() -> None:
    data = engineer_step().model_dump()
    with pytest.raises(ValidationError):
        EngineerFormulaStep.model_validate(data | {"norm_refs": (REF,)})

    stats = module_traceability((engineer_step(),))
    assert (stats.normative_steps, stats.verified_steps, stats.unverified_steps, stats.engineer_steps) == (0, 0, 0, 1)
    assert stats.completeness is None


def test_normative_traceability_counts_only_normative_steps() -> None:
    outcome = run(data=Data(reference=VERIFIED)).outcome
    stats = module_traceability(outcome.trace)

    assert (stats.normative_steps, stats.verified_steps, stats.unverified_steps, stats.engineer_steps) == (2, 2, 0, 1)
    assert stats.completeness == 1.0
    unverified = module_traceability(run().outcome.trace)
    assert (unverified.normative_steps, unverified.verified_steps, unverified.unverified_steps) == (2, 0, 2)
    assert unverified.completeness == 0.0


def test_sources_are_deduplicated_in_first_use_order_across_all_carriers() -> None:
    outcome = run(options=Options(warn=True)).outcome
    norms, engineers = module_sources(outcome, output_sources=((REF,), RULE, OTHER_RULE))

    assert norms == (REF,)
    assert engineers == (RULE, OTHER_RULE)
    stopped = run(options=Options(mode="after")).outcome
    assert module_sources(stopped) == ((), (RULE,))
    assert module_traceability(()).completeness is None


def test_boundary_rejects_nested_unknown_fields_even_with_pydantic_default_ignore() -> None:
    class Child(BaseModel):
        value: float

    class Nested(BaseModel):
        node: Child

    class NestedModule(StructuredModule):
        input_schema = TypeAdapter[Any](Nested)

    with pytest.raises(CalculationError):
        run(NestedModule(), inputs={"node": {"value": 2.0, "unrecognized": True}})


def test_alias_models_accept_valid_alias_and_field_name_data_at_the_boundary() -> None:
    class Aliased(BaseModel):
        amount: float = Field(alias="external_amount")

    class AliasedModule(StructuredModule):
        input_schema = TypeAdapter[Any](Aliased)

        def normalize(self, inputs: Any) -> Any:
            return inputs

        def validate(self, inputs: Any, data: Data, options: Options) -> None:
            pass

        def calculate(self, inputs: Any, data: Data, options: Options) -> ModuleOutcome[Outputs, Details]:
            return ModuleOutcome[Outputs, Details](
                execution="completed", applicability="applicable",
                outputs=Outputs(total=QuantityValue(value=inputs.amount, unit="m")),
            )

    module = AliasedModule()
    result = run(module, inputs=Aliased(external_amount=2.0))
    assert result == run(module, inputs={"external_amount": 2.0})
    assert result == run(module, inputs={"amount": 2.0})
    assert result.outcome.outputs == Outputs(total=QuantityValue(value=2.0, unit="m"))


def test_root_models_execute_and_reject_injected_model_attributes() -> None:
    class Values(RootModel[list[int]]):
        pass

    class RootModule(StructuredModule):
        input_schema = TypeAdapter[Any](Values)

        def normalize(self, inputs: Any) -> Any:
            return inputs

        def validate(self, inputs: Any, data: Data, options: Options) -> None:
            pass

        def calculate(self, inputs: Any, data: Data, options: Options) -> ModuleOutcome[Outputs, Details]:
            return ModuleOutcome[Outputs, Details](
                execution="completed", applicability="applicable",
                outputs=Outputs(total=QuantityValue(value=sum(inputs.root), unit="m")),
            )

    inputs = Values([1, 2])
    result = run(RootModule(), inputs=inputs)
    assert result.outcome.outputs == Outputs(total=QuantityValue(value=3.0, unit="m"))
    assert inputs.root == [1, 2]
    with pytest.raises(CalculationError, match="root model"):
        run(RootModule(), inputs=inputs.model_copy(update={"unrecognized": True}))


def test_excluded_model_fields_still_affect_computation_identity() -> None:
    class ExcludedOptions(Options):
        factor: float = Field(default=1.0, exclude=True)

    first, second = ExcludedOptions(factor=1.0), ExcludedOptions(factor=2.0)
    assert first.model_dump() == second.model_dump()
    assert module_run_identity(metadata(), {}, {}, first) != module_run_identity(metadata(), {}, {}, second)

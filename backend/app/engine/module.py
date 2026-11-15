import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Protocol

from pydantic import BaseModel, TypeAdapter, ValidationError

from app.core.exceptions import (
    AlreadyRegisteredError,
    CalculationError,
    ContractMetadataError,
    NotFoundError,
)
from app.schemas.calculation import NormRef, Source
from app.schemas.module import (
    AnyModuleOutcome,
    EngineerFormulaStep,
    ModuleDiagnostic,
    ModuleExecution,
    ModuleMetadata,
    ModuleOutcome,
    ModuleStep,
)
from app.schemas.parameters import EngineerRule


class CalculationModule[InputsT, DataT, OptionsT, OutputsT, DetailsT, ExternalT](Protocol):
    @property
    def metadata(self) -> ModuleMetadata: ...
    @property
    def input_schema(self) -> TypeAdapter[InputsT]: ...
    @property
    def data_schema(self) -> TypeAdapter[DataT]: ...
    @property
    def options_schema(self) -> TypeAdapter[OptionsT]: ...
    @property
    def output_schema(self) -> TypeAdapter[OutputsT]: ...
    @property
    def diagnostic_schema(self) -> TypeAdapter[DetailsT]: ...

    def normalize(self, inputs: InputsT) -> InputsT: ...
    def validate(self, inputs: InputsT, data: DataT, options: OptionsT) -> None: ...
    def calculate(
        self, inputs: InputsT, data: DataT, options: OptionsT
    ) -> ModuleOutcome[OutputsT, DetailsT]: ...
    def validate_diagnostic(
        self, diagnostic: ModuleDiagnostic[DetailsT], trace: tuple[ModuleStep, ...],
        inputs: InputsT, data: DataT, options: OptionsT,
    ) -> None: ...
    def identity(self, inputs: InputsT, data: DataT, options: OptionsT) -> str: ...
    def adapt_result(self, execution: ModuleExecution[OutputsT, DetailsT]) -> ExternalT: ...


def _contents(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        raise CalculationError("module payloads require finite numbers")
    if isinstance(value, BaseModel):
        if value.__pydantic_root_model__:
            if set(vars(value)) != {"root"} or value.model_extra:
                raise CalculationError("unexpected fields on a module root model")
            return _contents(vars(value)["root"])
        return _contents(vars(value) | (value.model_extra or {}))
    if is_dataclass(value) and not isinstance(value, type):
        return _contents(asdict(value))
    if isinstance(value, Mapping):
        return {key: _contents(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return tuple(_contents(item) for item in value)
    if isinstance(value, list):
        return [_contents(item) for item in value]
    return deepcopy(value)


def _validated[T](schema: TypeAdapter[T], value: object) -> T:
    return schema.validate_python(
        _contents(value), strict=True, extra="forbid", by_alias=True, by_name=True,
    )


def execute_module[I, D, S, O, E, X](
    module: CalculationModule[I, D, S, O, E, X], inputs: I, data: D, options: S,
) -> ModuleExecution[O, E]:
    """Выполняет модуль на изолированных данных и проверяет его результат."""
    try:
        metadata = ModuleMetadata.model_validate(_contents(module.metadata))
        normalized = _validated(module.input_schema, inputs)
        resolved = _validated(module.data_schema, data)
        settings = _validated(module.options_schema, options)
        normalized = _validated(module.input_schema, module.normalize(normalized))
        module.validate(deepcopy(normalized), deepcopy(resolved), deepcopy(settings))
        identity = module.identity(deepcopy(normalized), deepcopy(resolved), deepcopy(settings))
        if metadata.identity_policy == "v1" and identity != module_run_identity(
            metadata, normalized, resolved, settings,
        ):
            raise CalculationError("module identity does not match its declared v1 policy")
        raw = module.calculate(deepcopy(normalized), deepcopy(resolved), deepcopy(settings))
        outcome = _validated(TypeAdapter(AnyModuleOutcome), raw)
        if outcome.execution == "completed":
            output = _validated(module.output_schema, outcome.outputs)
            outcome = outcome.model_copy(update={"outputs": output})
        if outcome.diagnostic is not None:
            details = _validated(module.diagnostic_schema, outcome.diagnostic.details)
            diagnostic = outcome.diagnostic.model_copy(update={"details": details})
            outcome = outcome.model_copy(update={"diagnostic": diagnostic})
            module.validate_diagnostic(
                deepcopy(diagnostic), deepcopy(outcome.trace),
                deepcopy(normalized), deepcopy(resolved), deepcopy(settings),
            )
        return ModuleExecution(metadata=metadata, input_hash=identity, outcome=outcome)
    except (ValidationError, ValueError, TypeError) as exc:
        raise CalculationError(f"invalid calculation module execution: {exc}") from exc


class ModuleRegistry:
    def __init__(self) -> None:
        self._modules: dict[str, CalculationModule[Any, Any, Any, Any, Any, Any]] = {}

    def register(self, module: CalculationModule[Any, Any, Any, Any, Any, Any]) -> None:
        try:
            metadata = ModuleMetadata.model_validate(_contents(module.metadata))
            for name in (
                "input_schema", "data_schema", "options_schema", "output_schema", "diagnostic_schema",
            ):
                if not isinstance(getattr(module, name), TypeAdapter):
                    raise TypeError(f"module {name} must be a TypeAdapter")
            for name in (
                "normalize", "validate", "calculate", "validate_diagnostic", "identity", "adapt_result",
            ):
                if not callable(getattr(module, name)):
                    raise TypeError(f"module {name} must be callable")
        except (AttributeError, ValueError, TypeError) as exc:
            raise ContractMetadataError(f"invalid calculation module registration: {exc}") from exc
        if metadata.identifier in self._modules:
            raise AlreadyRegisteredError(f"module {metadata.identifier!r} is already registered")
        self._modules[metadata.identifier] = module

    def get(self, identifier: str) -> CalculationModule[Any, Any, Any, Any, Any, Any]:
        try:
            return self._modules[identifier]
        except KeyError:
            raise NotFoundError(f"no calculation module registered for {identifier!r}") from None


def _identity_value(value: object) -> object:
    if isinstance(value, BaseModel):
        return _identity_value(_contents(value))
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise CalculationError("module identity requires string object keys")
        return {key: _identity_value(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_identity_value(item) for item in value]
    if value is None or isinstance(value, str | bool | int):
        return value
    if isinstance(value, float):
        if math.isfinite(value):
            return value
        raise CalculationError("module identity requires finite numbers")
    raise CalculationError(f"{type(value).__name__} cannot be part of a module identity")


def module_canonical_json(data: object) -> str:
    return json.dumps(
        _identity_value(data), sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    )


def module_run_identity(metadata: ModuleMetadata, inputs: object, data: object, options: object) -> str:
    if metadata.identity_policy != "v1":
        raise CalculationError("versioned module identity requires the v1 policy")
    payload = {
        "format": "calculation-module-run-v1",
        "module": metadata,
        "inputs": inputs,
        "data": data,
        "options": options,
    }
    return hashlib.sha256(module_canonical_json(payload).encode("utf-8")).hexdigest()


def module_sources(
    outcome: ModuleOutcome[Any, Any], output_sources: Sequence[Source] = (),
) -> tuple[tuple[NormRef, ...], tuple[EngineerRule, ...]]:
    sources: list[Source] = [
        step.source if isinstance(step, EngineerFormulaStep) else step.norm_refs
        for step in outcome.trace
    ]
    if outcome.diagnostic is not None:
        sources.append(outcome.diagnostic.source)
    sources.extend(output_sources)
    sources.extend(warning.bound.source for warning in outcome.warnings)
    norms: list[NormRef] = []
    rules: list[EngineerRule] = []
    for source in sources:
        if isinstance(source, EngineerRule):
            if source not in rules:
                rules.append(source)
        else:
            for reference in source:
                if reference not in norms:
                    norms.append(reference)
    return tuple(norms), tuple(rules)


@dataclass(frozen=True)
class ModuleTraceability:
    normative_steps: int
    verified_steps: int
    unverified_steps: int
    engineer_steps: int

    @property
    def completeness(self) -> float | None:
        return None if not self.normative_steps else self.verified_steps / self.normative_steps


def module_traceability(trace: Sequence[ModuleStep]) -> ModuleTraceability:
    normative = [step for step in trace if not isinstance(step, EngineerFormulaStep)]
    verified = sum(step.verified for step in normative)
    return ModuleTraceability(
        normative_steps=len(normative), verified_steps=verified,
        unverified_steps=len(normative) - verified, engineer_steps=len(trace) - len(normative),
    )

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.calculation import (
    ApplicabilityWarning,
    CheckStep,
    FormulaStep,
    QuantityValue,
    Source,
    Substitution,
    TableStep,
)
from app.schemas.parameters import EngineerRule


class ModuleMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    identifier: str = Field(min_length=1)
    methodology_version: str = Field(min_length=1)
    input_schema_version: str = Field(min_length=1)
    data_schema_version: str = Field(min_length=1)
    options_schema_version: str = Field(min_length=1)
    output_schema_version: str = Field(min_length=1)
    diagnostic_schema_version: str = Field(min_length=1)
    identity_policy: Literal["v1", "legacy"] = "v1"


class EngineerFormulaStep(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["engineer_formula"] = "engineer_formula"
    step_id: str = Field(min_length=1)
    expression: str = Field(min_length=1)
    substitutions: tuple[Substitution, ...]
    result: QuantityValue
    source: EngineerRule


ModuleStep = Annotated[
    FormulaStep | TableStep | CheckStep | EngineerFormulaStep, Field(discriminator="kind")
]


class ModuleDiagnostic[DetailsT](BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    code: str = Field(min_length=1)
    source: Source
    step_id: str | None = Field(default=None, min_length=1)
    details: DetailsT


class ModuleOutcome[OutputsT, DetailsT](BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    execution: Literal["completed", "stopped"]
    applicability: Literal["applicable", "outside_validated_range", "not_applicable"]
    outputs: OutputsT | None = None
    trace: tuple[ModuleStep, ...] = ()
    checks: tuple[CheckStep, ...] = ()
    warnings: tuple[ApplicabilityWarning, ...] = ()
    diagnostic: ModuleDiagnostic[DetailsT] | None = None
    stop_stage: Literal["before_calculation", "after_start"] | None = None

    @model_validator(mode="after")
    def _consistent(self) -> "ModuleOutcome[OutputsT, DetailsT]":
        names = [step.step_id for step in self.trace]
        if len(names) != len(set(names)):
            raise ValueError("trace step identifiers must be unique")
        if self.checks != tuple(step for step in self.trace if isinstance(step, CheckStep)):
            raise ValueError("checks must equal the ordered check steps in the trace")
        if self.execution == "completed":
            if self.applicability == "not_applicable" or self.outputs is None:
                raise ValueError("completed execution needs applicable final outputs")
            if self.diagnostic is not None or self.stop_stage is not None:
                raise ValueError("completed execution cannot have a stop diagnostic or stage")
            if (self.applicability == "outside_validated_range") != bool(self.warnings):
                raise ValueError("completed applicability must agree with warnings")
        else:
            if self.applicability != "not_applicable" or self.outputs is not None:
                raise ValueError("stopped execution is not applicable and has no final outputs")
            if self.diagnostic is None or self.stop_stage is None:
                raise ValueError("stopped execution needs a diagnostic and stop stage")
            if self.stop_stage == "before_calculation":
                if self.trace or self.diagnostic.step_id is not None:
                    raise ValueError("a preflight stop has no trace or step reference")
            elif not self.trace or self.diagnostic.step_id not in names:
                raise ValueError("a later stop must reference a retained trace step")
        return self


class ModuleExecution[OutputsT, DetailsT](BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    metadata: ModuleMetadata
    input_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    outcome: ModuleOutcome[OutputsT, DetailsT]


AnyModuleOutcome = ModuleOutcome[Any, Any]

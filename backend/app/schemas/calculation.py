from collections.abc import Sequence
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.exceptions import InputValidationError
from app.schemas.parameters import EngineerRule
from app.schemas.units import UNITS, UnitSymbol

UNVERIFIED: Literal["unverified"] = "unverified"


class QuantityDeclaration(BaseModel):
    """A quantity of a calculation type and the base unit it is held in."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    base_unit: UnitSymbol


class QuantityValue(BaseModel):
    """A finite value with its unit from the unit vocabulary."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    value: float
    unit: UnitSymbol


class Substitution(QuantityValue):
    """The value with its unit substituted for one symbol of a step."""

    symbol: str = Field(min_length=1)


class NormRef(BaseModel):
    """A reference to one locator of a norm document (design.md, section "NormRef").

    ``edition`` and ``clause`` are a concrete string or the reserved literal
    ``unverified``; ``document`` is always concrete.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    document: str = Field(min_length=1)
    edition: Literal["unverified"] | str = Field(min_length=1)
    clause: Literal["unverified"] | str = Field(min_length=1)
    status: Literal["verified", "unverified"]
    provenance: Literal["human-verified", "machine-extracted"]

    @model_validator(mode="after")
    def _invariants_hold(self) -> "NormRef":
        if self.document == UNVERIFIED:
            raise ValueError("document must be a concrete designation, never 'unverified'")
        if self.status == "verified" and UNVERIFIED in (self.edition, self.clause):
            raise ValueError("a verified reference needs a concrete edition and clause")
        if self.provenance == "machine-extracted" and self.status == "verified":
            raise ValueError("a machine-extracted reference is always unverified")
        return self


NormRefs = Annotated[tuple[NormRef, ...], Field(min_length=1)]

Source = NormRefs | EngineerRule


class _TraceStep(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    step_id: str = Field(min_length=1)
    expression: str = Field(min_length=1)
    substitutions: tuple[Substitution, ...]
    result: QuantityValue
    norm_refs: NormRefs

    @property
    def verified(self) -> bool:
        """A step counts as verified only when every one of its references is verified."""
        return all(reference.status == "verified" for reference in self.norm_refs)


class FormulaStep(_TraceStep):
    """A step that evaluates a formula; ``expression`` is the formula's LaTeX."""

    kind: Literal["formula"] = "formula"


class TableStep(_TraceStep):
    """A step that takes one entry of a norm's table, selected by its substitutions."""

    kind: Literal["table"] = "table"


class CheckStep(_TraceStep):
    """A comparison of ``result`` (the left value) with ``right``."""

    kind: Literal["check"] = "check"
    operator: Literal["le", "lt", "ge", "gt"]
    right: QuantityValue
    passed: bool


TraceStep = Annotated[FormulaStep | TableStep | CheckStep, Field(discriminator="kind")]


def unverified_steps(trace: Sequence[FormulaStep | TableStep | CheckStep]) -> int:
    """The number of steps that do not count as verified; none is dropped."""
    return sum(not step.verified for step in trace)


def verdict_of(
    trace: Sequence[FormulaStep | TableStep | CheckStep],
) -> tuple[Literal["pass", "fail"], str]:
    """The verdict of a calculation that ran, and the ``step_id`` of its deciding check.

    ``fail`` is decided by the first check step that did not pass, ``pass`` by the
    last check step ("Automatic correctness validation").
    """
    checks = [step for step in trace if isinstance(step, CheckStep)]
    if not checks:
        raise ValueError("a calculation that ran has at least one check step")
    failed = next((step for step in checks if not step.passed), None)
    if failed is not None:
        return "fail", failed.step_id
    return "pass", checks[-1].step_id


class RoundingRule(BaseModel):
    """How an output value is rounded; the rule and its mode come from its source."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    decimals: int = Field(ge=0)
    mode: Literal["half_up", "half_even"]


class OutputDeclaration(QuantityDeclaration):
    """An output quantity with the rule it is rounded by and the source of that rule."""

    rounding_rule: RoundingRule
    rounding_source: Source


class CalculationTypeContract(BaseModel):
    """What the registry holds for a calculation type besides its calculator.

    Base units and quantity names are data the engineer fills, never values of a
    norm. ``checks`` names the check steps of the type; at least one is required,
    so a result that is not refused always has a deciding check. Every output
    declares its rounding rule and its source, so a type without them cannot be
    registered.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    inputs: tuple[QuantityDeclaration, ...] = Field(min_length=1)
    outputs: tuple[OutputDeclaration, ...] = Field(min_length=1)
    checks: tuple[Annotated[str, Field(min_length=1)], ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _quantity_names_are_unique(self) -> "CalculationTypeContract":
        for group in (self.inputs, self.outputs):
            names = [quantity.name for quantity in group]
            if len(names) != len(set(names)):
                raise ValueError("quantity names must be unique within inputs and within outputs")
        if len(self.checks) != len(set(self.checks)):
            raise ValueError("check names must be unique")
        return self


class _Bound(BaseModel):
    """A lower (``min``) or upper (``max``) bound of one input, in its base unit."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    quantity: str = Field(min_length=1)
    kind: Literal["min", "max"]
    value: float
    inclusive: bool


class MethodBound(_Bound):
    """A bound of the method's range; its source is always the norm."""

    source: NormRefs


class ValidatedBound(_Bound):
    """A bound of the validated range, from the norm or set by the engineer."""

    source: Source


def check_bounds(bounds: Sequence[MethodBound | ValidatedBound]) -> None:
    """A range has at most one lower and one upper bound per quantity, and is not empty."""
    sides: dict[tuple[str, str], MethodBound | ValidatedBound] = {}
    for bound in bounds:
        key = (bound.quantity, bound.kind)
        if key in sides:
            raise ValueError(f"quantity {bound.quantity!r} has two {bound.kind} bounds")
        sides[key] = bound
    for (quantity, kind), lower in sides.items():
        upper = sides.get((quantity, "max"))
        if kind != "min" or upper is None:
            continue
        empty = lower.value > upper.value or (
            lower.value == upper.value and not (lower.inclusive and upper.inclusive)
        )
        if empty:
            raise ValueError(f"the range of {quantity!r} is empty: its min is above its max")


class OutputValue(QuantityValue):
    """An output quantity in its base unit, rounded by its rule."""

    quantity: str = Field(min_length=1)
    rounding_rule: RoundingRule
    rounding_source: Source


class ApplicabilityWarning(BaseModel):
    """An input inside the method's range but outside the validated range."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    value: QuantityValue
    bound: ValidatedBound


class CheckReason(BaseModel):
    """The check step that decided a ``pass`` or ``fail`` verdict."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["check"] = "check"
    step_id: str = Field(min_length=1)


class BoundViolation(BaseModel):
    """The bound of the method's range that refused the calculation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["bound"] = "bound"
    value: QuantityValue
    bound: MethodBound


VerdictReason = Annotated[CheckReason | BoundViolation, Field(discriminator="kind")]


def ordered_sources(
    trace: Sequence[FormulaStep | TableStep | CheckStep],
    refusal: BoundViolation | None,
    outputs: Sequence[OutputValue],
    warnings: Sequence[ApplicabilityWarning],
) -> tuple[tuple[NormRef, ...], tuple[EngineerRule, ...]]:
    """Every source used, each once, in the order of first use (design.md decision 17).

    Trace steps in order, then the bound that refused the calculation, then the
    rounding sources in the order of ``outputs``, then the warnings.
    """
    sources: list[NormRefs | EngineerRule] = [step.norm_refs for step in trace]
    if refusal is not None:
        sources.append(refusal.bound.source)
    sources.extend(output.rounding_source for output in outputs)
    sources.extend(warning.bound.source for warning in warnings)
    norm_refs: list[NormRef] = []
    engineer_rules: list[EngineerRule] = []
    for source in sources:
        if isinstance(source, EngineerRule):
            if source not in engineer_rules:
                engineer_rules.append(source)
            continue
        for reference in source:
            if reference not in norm_refs:
                norm_refs.append(reference)
    return tuple(norm_refs), tuple(engineer_rules)


class CalculationResult(BaseModel):
    """What the pure calculation function returns: the envelope without ``result_id``."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    engine_version: str = Field(min_length=1)
    input_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    outputs: tuple[OutputValue, ...]
    norm_refs: tuple[NormRef, ...]
    engineer_rules: tuple[EngineerRule, ...]
    verdict: Literal["pass", "fail", "refused"]
    verdict_reason: VerdictReason
    warnings: tuple[ApplicabilityWarning, ...]
    trace: tuple[TraceStep, ...]
    unverified_step_count: int = Field(ge=0)

    @model_validator(mode="after")
    def _is_consistent(self) -> "CalculationResult":
        if self.verdict == "refused":
            self._check_refusal()
        else:
            self._check_deciding_step()
        self._check_sources_are_listed()
        if self.unverified_step_count != unverified_steps(self.trace):
            raise ValueError("unverified_step_count must equal the number of unverified steps")
        return self

    def _check_refusal(self) -> None:
        if self.verdict_reason.kind != "bound":
            raise ValueError("a refused calculation names the violated bound")
        if self.trace or self.outputs or self.unverified_step_count:
            raise ValueError(
                "a refused calculation has an empty trace and outputs and no unverified step"
            )

    def _check_deciding_step(self) -> None:
        reason = self.verdict_reason
        if reason.kind != "check":
            raise ValueError("a pass or fail verdict names its deciding check")
        checks = {step.step_id for step in self.trace if step.kind == "check"}
        if reason.step_id not in checks:
            raise ValueError(f"deciding check {reason.step_id!r} is not a check step of the trace")
        if (self.verdict, reason.step_id) != verdict_of(self.trace):
            raise ValueError(
                "the verdict and its deciding check do not follow from the check steps"
            )

    def _check_sources_are_listed(self) -> None:
        refusal = self.verdict_reason if isinstance(self.verdict_reason, BoundViolation) else None
        norm_refs, engineer_rules = ordered_sources(
            self.trace, refusal, self.outputs, self.warnings
        )
        if any(rule not in self.engineer_rules for rule in engineer_rules):
            raise ValueError("every engineer rule used is listed in engineer_rules")
        if any(reference not in self.norm_refs for reference in norm_refs):
            raise ValueError("every norm reference used is listed in norm_refs")
        if (self.norm_refs, self.engineer_rules) != (norm_refs, engineer_rules):
            raise ValueError(
                "norm_refs and engineer_rules list each source used once, in the order of first use"
            )


class ResultEnvelope(CalculationResult):
    """A calculation result with the ``result_id`` the service layer assigns."""

    result_id: UUID


class CalculationRequest(BaseModel):
    """A request to run a calculation type, validated before the engine runs.

    The schema rejects a malformed request, a non-finite value and a unit outside
    the vocabulary; ``check_against`` rejects inputs that do not fit the type's
    contract (``security`` "Input validation", design.md decisions 12 and 13).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    calculation_type: str = Field(min_length=1)
    inputs: dict[str, QuantityValue]

    def check_against(self, contract: CalculationTypeContract) -> None:
        declared = {quantity.name: quantity.base_unit for quantity in contract.inputs}
        if set(self.inputs) != set(declared):
            raise InputValidationError(
                f"inputs {sorted(self.inputs)} do not match the declared inputs {sorted(declared)}"
            )
        for name, value in self.inputs.items():
            given, base = UNITS[value.unit].dimension, UNITS[declared[name]].dimension
            if given != base:
                raise InputValidationError(
                    f"input {name!r} is in {value.unit!r} ({given}), not a unit of {base}"
                )

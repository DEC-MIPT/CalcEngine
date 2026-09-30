from collections.abc import Mapping
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.core.exceptions import InputValidationError
from app.schemas.calculation import (
    BoundViolation,
    CalculationTypeContract,
    CheckStep,
    QuantityValue,
    ResultEnvelope,
    TraceStep,
)
from app.schemas.report import ReportRequest


class _Section(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class InputRow(_Section):
    """One input as the request gave it, before conversion to its base unit."""

    quantity: str = Field(min_length=1)
    value: QuantityValue


class InputSection(_Section):
    kind: Literal["inputs"] = "inputs"
    rows: tuple[InputRow, ...]


class TraceSection(_Section):
    """The trace steps in run order, each with its ``norm_refs``; empty when refused."""

    kind: Literal["trace"] = "trace"
    refused: bool
    steps: tuple[TraceStep, ...]


class ConclusionSection(_Section):
    """The verdict and what decided it: the deciding check step, or the violated bound."""

    kind: Literal["conclusion"] = "conclusion"
    verdict: Literal["pass", "fail", "refused"]
    deciding_check: CheckStep | None
    violation: BoundViolation | None


BodySection = Annotated[
    InputSection | TraceSection | ConclusionSection, Field(discriminator="kind")
]


class Report(_Section):
    """What a renderer writes: the request (title block, signatures) and the body sections."""

    request: ReportRequest
    body: tuple[BodySection, ...]


def _input_rows(
    contract: CalculationTypeContract, inputs: Mapping[str, QuantityValue]
) -> tuple[InputRow, ...]:
    declared = [quantity.name for quantity in contract.inputs]
    if set(inputs) != set(declared):
        raise InputValidationError(
            f"inputs {sorted(inputs)} do not match the declared inputs {declared}"
        )
    return tuple(InputRow(quantity=name, value=inputs[name]) for name in declared)


def _conclusion(envelope: ResultEnvelope) -> ConclusionSection:
    reason = envelope.verdict_reason
    if isinstance(reason, BoundViolation):
        return ConclusionSection(verdict=envelope.verdict, deciding_check=None, violation=reason)
    deciding = next(
        step
        for step in envelope.trace
        if isinstance(step, CheckStep) and step.step_id == reason.step_id
    )
    return ConclusionSection(verdict=envelope.verdict, deciding_check=deciding, violation=None)


def build_report(
    contract: CalculationTypeContract,
    inputs: Mapping[str, QuantityValue],
    envelope: ResultEnvelope,
    request: ReportRequest,
) -> Report:
    """The report model of one result (``calculation-core-contract`` design.md decision 18).

    The body holds the input-data table in the contract's order of inputs, the trace,
    and the conclusion. A refused calculation keeps every section: its trace section
    holds no step, and its conclusion names the violated bound.
    """
    return Report(
        request=request,
        body=(
            InputSection(rows=_input_rows(contract, inputs)),
            TraceSection(refused=envelope.verdict == "refused", steps=envelope.trace),
            _conclusion(envelope),
        ),
    )

from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.calculation import QuantityValue, ResultEnvelope
from app.schemas.units import UNITS

SearchStopReason = Literal["parameter_source_unavailable", "calculation_error", "time_budget", "cancelled"]


class DesignModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class FoundationCandidate(DesignModel):
    b: QuantityValue
    l: QuantityValue

    def area_m2(self) -> Decimal:
        return (Decimal(str(self.b.value)) * Decimal(str(UNITS[self.b.unit].factor))
                * Decimal(str(self.l.value)) * Decimal(str(UNITS[self.l.unit].factor)))


class FoundationSelectionRequest(DesignModel):
    schema_version: Literal["foundation-selection-request-v1"] = "foundation-selection-request-v1"
    calculation_type: Literal["foundations_shallow_loads"] = "foundations_shallow_loads"
    policy_version: Literal["foundation-min-area-v1"] = "foundation-min-area-v1"
    common_inputs: dict[str, QuantityValue]
    candidates: tuple[FoundationCandidate, ...] = Field(min_length=1, max_length=256)


class PressureCorner(DesignModel):
    name: Literal["pp", "pm", "mp", "mm"]
    x: QuantityValue
    y: QuantityValue
    pressure: QuantityValue
    step_id: str


class FoundationContext(DesignModel):
    schema_version: Literal["foundation-result-context-v1"] = "foundation-result-context-v1"
    result_id: UUID
    calculation_type: Literal["foundations_shallow_loads", "foundations_shallow_weights"]
    methodology_version: str
    input_hash: str
    load_level: Literal["upper_cut"] = "upper_cut"
    weight_mode: Literal["averaged", "explicit"]
    inputs: dict[str, QuantityValue]
    geometry: dict[str, QuantityValue]
    trace_values: dict[str, QuantityValue]
    pressure_state: Literal["full_contact", "diagnostic", "unavailable"]
    corners: tuple[PressureCorner, ...] = ()

    @model_validator(mode="after")
    def _corner_contract(self) -> "FoundationContext":
        expected_mode = "explicit" if self.calculation_type == "foundations_shallow_weights" else "averaged"
        if self.weight_mode != expected_mode:
            raise ValueError("weight mode differs from its registered type")
        if set(self.geometry) - {"b", "l", "A", "Wx", "Wy"} or not {"b", "l"}.issubset(self.geometry):
            raise ValueError("geometry needs the declared footing dimensions")
        units = {"b": "m", "l": "m", "A": "m2", "Wx": "m3", "Wy": "m3"}
        if any(value.unit != units[name] or value.value <= 0 for name, value in self.geometry.items()):
            raise ValueError("geometry needs positive values with declared base units")
        if any(corner.x.unit != "m" or corner.y.unit != "m" for corner in self.corners):
            raise ValueError("corner coordinates need metres")
        if any(corner.step_id != f"p_corner_{corner.name}" or self.trace_values.get(corner.step_id) != corner.pressure for corner in self.corners):
            raise ValueError("corner values must match their stored trace origins")
        if any(corner.pressure.unit != "kPa" for corner in self.corners):
            raise ValueError("corner pressures need kPa")
        if self.pressure_state == "unavailable":
            if self.corners:
                raise ValueError("unavailable pressures cannot contain a pressure diagram")
        elif tuple(corner.name for corner in self.corners) != ("pp", "pm", "mp", "mm"):
            raise ValueError("pressure context needs four ordered corners")
        return self


class FoundationContextResponse(DesignModel):
    status: Literal["available", "unavailable"]
    context: FoundationContext | None = None

    @model_validator(mode="after")
    def _available(self) -> "FoundationContextResponse":
        if (self.status == "available") != (self.context is not None):
            raise ValueError("context availability and payload differ")
        return self


class CandidateOutcome(DesignModel):
    index: int = Field(ge=0, le=255)
    candidate: FoundationCandidate
    status: Literal["evaluated", "error", "skipped"]
    envelope: ResultEnvelope | None = None
    reason: Literal["parameter_source_unavailable", "calculation_error", "time_budget", "cancelled", "not_evaluated"] | None = None

    @model_validator(mode="after")
    def _evidence(self) -> "CandidateOutcome":
        if self.status == "evaluated":
            if self.envelope is None or self.reason is not None:
                raise ValueError("evaluated candidate needs only its envelope")
        elif self.envelope is not None or self.reason is None:
            raise ValueError("unevaluated candidate needs only its reason")
        return self


class FoundationSelectionResult(DesignModel):
    schema_version: Literal["foundation-selection-result-v1"] = "foundation-selection-result-v1"
    selection_id: UUID
    input_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    request: FoundationSelectionRequest
    status: Literal["selected", "no_acceptable_candidate", "incomplete"]
    outcomes: tuple[CandidateOutcome, ...]
    stop_reason: SearchStopReason | None = None
    selected_candidate_index: int | None = None
    selected_result_id: UUID | None = None

    @model_validator(mode="after")
    def _selection(self) -> "FoundationSelectionResult":
        if len(self.outcomes) != len(self.request.candidates):
            raise ValueError("every submitted candidate needs retained evidence")
        for index, outcome in enumerate(self.outcomes):
            if outcome.index != index or outcome.candidate != self.request.candidates[index]:
                raise ValueError("candidate evidence must preserve input order")
        passing = [index for index, item in enumerate(self.outcomes) if item.status == "evaluated" and item.envelope is not None and item.envelope.verdict == "pass"]
        if self.status == "selected" and self.selected_candidate_index is not None:
            areas = [(self.request.candidates[index].area_m2(), index) for index in passing]
            best = min(areas) if areas else None
            if best is None or best[1] != self.selected_candidate_index:
                raise ValueError("selected candidate does not follow minimum-area policy")
        if self.status == "selected":
            if self.selected_candidate_index is None or not 0 <= self.selected_candidate_index < len(self.outcomes):
                raise ValueError("selected candidate index is absent or invalid")
            if any(item.status != "evaluated" for item in self.outcomes):
                raise ValueError("an incomplete search cannot select a winner")
            selected = self.outcomes[self.selected_candidate_index].envelope
            if selected is None or selected.verdict != "pass" or selected.result_id != self.selected_result_id:
                raise ValueError("selected result must match a passing candidate")
        elif self.selected_candidate_index is not None or self.selected_result_id is not None:
            raise ValueError("unselected search cannot name a winner")
        if self.status == "no_acceptable_candidate" and any(
            item.status != "evaluated" or (item.envelope is not None and item.envelope.verdict == "pass")
            for item in self.outcomes
        ):
            raise ValueError("exhaustion requires a complete set without passing candidates")
        if (self.status == "incomplete") != (self.stop_reason is not None):
            raise ValueError("interrupted search must retain its stop reason")
        return self

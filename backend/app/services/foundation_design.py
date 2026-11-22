import hashlib
import json
from collections.abc import Callable, Mapping, Sequence
from decimal import Decimal
from time import monotonic
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.core.exceptions import (
    FoundationContextUnavailableError,
    InputValidationError,
    NotFoundError,
    ParameterSourceUnavailableError,
    UnitError,
)
from app.engine.boundary import inputs_to_base_units
from app.engine.registry import CalculatorRegistry
from app.reporting.foundation_design import render_selection_docx
from app.repositories.foundation_design import FoundationDesignRepository
from app.schemas.api import FieldError
from app.schemas.calculation import CalculationRequest, ValidatedBound
from app.schemas.foundation_design import (
    CandidateOutcome,
    FoundationContextResponse,
    FoundationSelectionRequest,
    FoundationSelectionResult,
    SearchStopReason,
)
from app.schemas.report import ReportRequest
from app.services.calculation import CalculationService, calculation_service
from app.services.parameter_source import ParameterSource


class FoundationDesignService:
    def __init__(
        self, registry: CalculatorRegistry, calculations: CalculationService,
        repository: FoundationDesignRepository, *,
        clock: Callable[[], float] = monotonic, budget: float = 10.0,
        new_id: Callable[[], UUID] = uuid4,
    ) -> None:
        self._registry = registry
        self._calculations = calculations
        self._repository = repository
        self._clock = clock
        self._budget = budget
        self._new_id = new_id

    def select(
        self, request: FoundationSelectionRequest,
        cancelled: Callable[[], bool] = lambda: False,
    ) -> FoundationSelectionResult:
        contract = self._registry.contract(request.calculation_type)
        prepared: list[CalculationRequest] = []
        areas: list[Decimal] = []
        problems: list[FieldError] = []
        if "b" in request.common_inputs or "l" in request.common_inputs:
            raise InputValidationError("Candidate dimensions belong in candidates.", tuple(
                FieldError(location=("body", "common_inputs", name), message="Dimension belongs in candidates.")
                for name in ("b", "l") if name in request.common_inputs
            ))
        for index, candidate in enumerate(request.candidates):
            given = CalculationRequest(calculation_type=request.calculation_type,
                inputs=request.common_inputs | {"b": candidate.b, "l": candidate.l})
            try:
                given.check_against(contract)
                inputs_to_base_units(contract, given.inputs)
            except (InputValidationError, UnitError) as exc:
                fields = exc.fields if isinstance(exc, InputValidationError) else ()
                for field in fields:
                    if isinstance(field, FieldError):
                        location = field.location
                        name = location[-1]
                        target = ("body", "candidates", index, name) if name in ("b", "l") else ("body", "common_inputs", name)
                        problems.append(FieldError(location=target, message=field.message))
                if not fields:
                    problems.append(FieldError(location=("body", "candidates", index), message="Invalid candidate inputs."))
                continue
            prepared.append(given)
            areas.append(request.candidates[index].area_m2())
        if problems:
            raise InputValidationError("The candidate inputs do not fit the calculation type.", tuple(problems))
        start = self._clock()
        outcomes: list[CandidateOutcome] = []
        interrupted: SearchStopReason | None = None
        for index, given in enumerate(prepared):
            if interrupted is None:
                if cancelled():
                    interrupted = "cancelled"
                elif self._clock() - start >= self._budget:
                    interrupted = "time_budget"
            if interrupted is not None:
                outcomes.append(CandidateOutcome(index=index, candidate=request.candidates[index],
                    status="skipped", reason=interrupted))
                continue
            try:
                envelope = self._calculations.evaluate(given)
            except ParameterSourceUnavailableError:
                interrupted = "parameter_source_unavailable"
                outcomes.append(CandidateOutcome(index=index, candidate=request.candidates[index],
                    status="error", reason=interrupted))
            except Exception:  # noqa: BLE001 - retain incomplete evidence for any failed candidate evaluation
                interrupted = "calculation_error"
                outcomes.append(CandidateOutcome(index=index, candidate=request.candidates[index],
                    status="error", reason=interrupted))
            else:
                outcomes.append(CandidateOutcome(index=index, candidate=request.candidates[index],
                    status="evaluated", envelope=envelope))
        if interrupted is None:
            if cancelled():
                interrupted = "cancelled"
            elif self._clock() - start >= self._budget:
                interrupted = "time_budget"
        incomplete = interrupted is not None
        passing = [] if incomplete else [i for i, item in enumerate(outcomes) if item.envelope is not None and item.envelope.verdict == "pass"]
        selected_candidate_index = min(passing, key=lambda i: (areas[i], i)) if passing else None
        selected = None if selected_candidate_index is None else outcomes[selected_candidate_index].envelope
        digest = hashlib.sha256(json.dumps({
            "request": request.model_dump(mode="json"),
            "methodology": self._registry.module(request.calculation_type).metadata.model_dump(mode="json"),
            "candidate_identity": [{"input_hash": item.envelope.input_hash, "source": None if item.envelope.parameter_source is None else item.envelope.parameter_source.model_dump(mode="json")} if item.envelope is not None else {"reason": item.reason} for item in outcomes],
        }, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        result = FoundationSelectionResult(
            selection_id=self._new_id(), input_hash=digest, request=request,
            status="incomplete" if incomplete else "selected" if selected is not None else "no_acceptable_candidate",
            outcomes=tuple(outcomes), stop_reason=interrupted, selected_candidate_index=selected_candidate_index,
            selected_result_id=None if selected is None else selected.result_id,
        )
        if selected is not None and selected_candidate_index is not None:
            self._calculations.persist(prepared[selected_candidate_index], selected)
        self._repository.add_selection(result)
        return result

    def get(self, selection_id: UUID) -> FoundationSelectionResult:
        result = self._repository.selection(selection_id)
        if result is None:
            raise NotFoundError("The requested foundation selection does not exist.")
        return result

    def context(self, result_id: UUID) -> FoundationContextResponse:
        self._calculations.get(result_id)
        result = self._repository.context(result_id)
        if result is None:
            raise FoundationContextUnavailableError("Stored foundation visualization context is unavailable.")
        return FoundationContextResponse(status="available", context=result)

    def report(self, selection_id: UUID, request: ReportRequest) -> bytes:
        selection = self.get(selection_id)
        context = None if selection.selected_result_id is None else self._repository.context(selection.selected_result_id)
        return render_selection_docx(selection, request, self._registry.contract(selection.request.calculation_type), context)


def foundation_design_service(
    session: Session, registry: CalculatorRegistry, *,
    sources: Mapping[str, ParameterSource], validated_ranges: Mapping[str, Sequence[ValidatedBound]],
) -> FoundationDesignService:
    return FoundationDesignService(registry, calculation_service(session, registry,
        sources=sources, validated_ranges=validated_ranges), FoundationDesignRepository(session))

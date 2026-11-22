from threading import Event
from typing import Annotated
from uuid import UUID

import anyio
from fastapi import APIRouter, Depends, Request, Response
from starlette.concurrency import run_in_threadpool

from app.api.calculations import DOCX, error_responses
from app.api.dependencies import get_foundation_design_service
from app.schemas.foundation_design import (
    FoundationContextResponse,
    FoundationSelectionRequest,
    FoundationSelectionResult,
)
from app.schemas.report import ReportRequest
from app.services.foundation_design import FoundationDesignService

router = APIRouter()


@router.post('/foundation-selections', status_code=201, response_model=FoundationSelectionResult, responses=error_responses(413, 422, 503))
async def create_selection(body: FoundationSelectionRequest, request: Request, service: Annotated[FoundationDesignService, Depends(get_foundation_design_service)], response: Response) -> FoundationSelectionResult:
    disconnected = Event()

    async def observe_disconnect() -> None:
        while True:
            message = await request.receive()
            if message["type"] == "http.disconnect":
                disconnected.set()
                return

    failure: Exception | None = None
    result: FoundationSelectionResult | None = None
    async with anyio.create_task_group() as group:
        group.start_soon(observe_disconnect)
        try:
            result = await run_in_threadpool(service.select, body, disconnected.is_set)
        except Exception as exc:  # noqa: BLE001 - rethrow outside task group preserves API error mapping
            failure = exc
        finally:
            disconnected.set()
            group.cancel_scope.cancel()
    if failure is not None:
        raise failure
    assert result is not None
    response.headers['Location'] = f'/foundation-selections/{result.selection_id}'
    return result


@router.get('/foundation-selections/{selection_id}', response_model=FoundationSelectionResult, responses=error_responses(404, 503))
def get_selection(selection_id: UUID, service: Annotated[FoundationDesignService, Depends(get_foundation_design_service)]) -> FoundationSelectionResult:
    return service.get(selection_id)


@router.post('/foundation-selections/{selection_id}/report', response_class=Response, responses=error_responses(404, 413, 422, 503))
def selection_report(selection_id: UUID, body: ReportRequest, service: Annotated[FoundationDesignService, Depends(get_foundation_design_service)]) -> Response:
    return Response(service.report(selection_id, body), media_type=DOCX, headers={'Content-Disposition': 'attachment; filename="foundation-selection-report.docx"'})


@router.get('/foundation-calculations/{result_id}/context', response_model=FoundationContextResponse, responses=error_responses(404, 503))
def calculation_context(result_id: UUID, service: Annotated[FoundationDesignService, Depends(get_foundation_design_service)]) -> FoundationContextResponse:
    return service.context(result_id)

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Response

from app.api.dependencies import get_registry, get_service
from app.engine.registry import CalculatorRegistry
from app.schemas.api import CalculationTypeView, ErrorBody
from app.schemas.calculation import CalculationRequest, ResultEnvelope
from app.schemas.report import ReportRequest
from app.services.calculation import CalculationService
from app.services.catalog import calculation_types

router = APIRouter()

DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

ERROR_DESCRIPTIONS = {
    404: "`not_found`: the calculation type or the stored result does not exist.",
    409: "`calculation_type_not_registered`: the stored result's type is no longer registered.",
    413: "`payload_too_large`: the request body is larger than 1 MiB.",
    422: "`validation_error` or `invalid_input`, with one entry in `fields` per offending field.",
    503: "`parameter_source_unavailable` or `database_unavailable`.",
}


def error_responses(*statuses: int) -> dict[int | str, dict[str, Any]]:
    """Описывает ответы об ошибках маршрута для OpenAPI.

    Свой ``422`` заменяет ответ, который FastAPI добавляет сам, так что у всех
    ошибок одна схема тела, ``ErrorBody`` (``calculation-api`` «API documentation»).

    Args:
        statuses: коды ошибок, которые маршрут может вернуть по спеке.

    Returns:
        Значение аргумента ``responses`` декоратора маршрута.
    """
    return {status: {"model": ErrorBody, "description": ERROR_DESCRIPTIONS[status]} for status in statuses}


@router.get("/calculation-types", response_model=list[CalculationTypeView])
def list_calculation_types(
    registry: Annotated[CalculatorRegistry, Depends(get_registry)],
) -> list[CalculationTypeView]:
    """Перечисляет зарегистрированные типы расчёта с входами и выходами.

    Маршрут не открывает базу: список строится из реестра (``calculation-api``
    «Calculation types listing»).

    Args:
        registry: реестр типов расчёта.

    Returns:
        По одному описанию на тип; пустой список, если типов нет.
    """
    return list(calculation_types(registry))


@router.post(
    "/calculations",
    status_code=201,
    response_model=ResultEnvelope,
    responses=error_responses(404, 413, 422, 503),
)
def create_calculation(
    body: CalculationRequest,
    service: Annotated[CalculationService, Depends(get_service)],
    response: Response,
) -> ResultEnvelope:
    """Запускает расчёт, сохраняет результат и возвращает его конверт.

    Порядок проверок — решение 3 дизайна: схема (FastAPI), тип, контракт, источник,
    затем запуск и запись. Отказ по диапазону метода — тоже ``201``, с вердиктом
    ``refused`` (``calculation-api`` «Run a calculation»).

    Args:
        body: запрос на расчёт: тип и входы со своими единицами.
        service: сервис расчётов этого запроса.
        response: ответ, в который ставится заголовок ``Location``.

    Returns:
        Сохранённый конверт результата.
    """
    envelope = service.submit(body)
    response.headers["Location"] = f"/calculations/{envelope.result_id}"
    return envelope


@router.get(
    "/calculations/{result_id}",
    response_model=ResultEnvelope,
    responses=error_responses(404, 422, 503),
)
def read_calculation(
    result_id: UUID,
    service: Annotated[CalculationService, Depends(get_service)],
) -> ResultEnvelope:
    """Возвращает сохранённый конверт результата без изменений.

    Других методов у ресурса нет: ``PUT``, ``PATCH`` и ``DELETE`` получают ``405``
    от маршрутизатора (``calculation-api`` «Stored result retrieval»).

    Args:
        result_id: идентификатор результата; не UUID — ``422``.
        service: сервис расчётов этого запроса.

    Returns:
        Конверт, равный телу ответа ``201``, создавшего результат.
    """
    return service.get(result_id).envelope


@router.post(
    "/calculations/{result_id}/report",
    response_class=Response,
    responses={
        200: {"content": {DOCX: {}}, "description": "The `.docx` report."},
        **error_responses(404, 409, 413, 422, 503),
    },
)
def download_report(
    result_id: UUID,
    body: ReportRequest,
    service: Annotated[CalculationService, Depends(get_service)],
) -> Response:
    """Отдаёт отчёт ``.docx`` по сохранённому результату.

    Отчёт строится только из сохранённых входов и конверта, расчёт клиент заново не
    присылает (``calculation-api`` «Report download», design.md, решение 9). Имя
    файла — ``dec-report-<result_id>.docx``, только ASCII, поэтому кодировать
    заголовок не нужно.

    Args:
        result_id: идентификатор сохранённого результата.
        body: данные основной надписи, настройка блока подписей и подписанты.
        service: сервис расчётов этого запроса.

    Returns:
        Ответ ``200`` с файлом ``.docx`` как вложением.
    """
    return Response(
        content=service.report(result_id, body),
        media_type=DOCX,
        headers={"Content-Disposition": f'attachment; filename="dec-report-{result_id}.docx"'},
    )

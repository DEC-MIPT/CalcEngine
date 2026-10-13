from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from pydantic import StringConstraints

from app.api.calculations import error_responses
from app.api.dependencies import get_normatives_service
from app.schemas.normatives import DocumentView, SearchResults
from app.services.normatives import NormativesService

router = APIRouter(prefix="/normatives")

ERROR_DESCRIPTIONS = {
    404: "`not_found`: the catalog holds no document with this id.",
    422: "`validation_error`: a query or path parameter is outside its limits.",
    503: "`catalog_unavailable`: the normative catalog is not configured or cannot be reached.",
}

SearchText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=200)]
"""Текст поиска: от 2 до 200 символов после обрезки пробелов — предел API, не нормы (design.md, решение 8)."""


@router.get(
    "/search",
    response_model=SearchResults,
    responses=error_responses(422, 503, descriptions=ERROR_DESCRIPTIONS),
)
def search_normatives(
    q: Annotated[SearchText, Query()],
    service: Annotated[NormativesService, Depends(get_normatives_service)],
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> SearchResults:
    """Ищет документы, пункты и формулы каталога (``normatives-catalog`` "Normative search endpoint").

    Текст уходит в базу связанным параметром как есть, без транслитерации; ни ответ, ни
    строка лога его не повторяют.

    Args:
        q: текст поиска.
        service: сервис каталога норм.
        limit: наибольшее число совпадений, от 1 до 50.

    Returns:
        Совпадения в порядке ранга каталога; ``{"hits": []}``, если их нет.
    """
    return service.search(q, limit)


@router.get(
    "/documents/{document_id}",
    response_model=DocumentView,
    responses=error_responses(404, 422, 503, descriptions=ERROR_DESCRIPTIONS),
)
def read_normative_document(
    document_id: Annotated[int, Path(gt=0)],
    service: Annotated[NormativesService, Depends(get_normatives_service)],
) -> DocumentView:
    """Возвращает документ каталога с пунктами (``normatives-catalog`` "Normative document endpoint").

    Args:
        document_id: положительный идентификатор документа.
        service: сервис каталога норм.

    Returns:
        Документ с пунктами в порядке документа.
    """
    return service.document(document_id)

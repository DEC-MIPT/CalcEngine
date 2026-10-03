from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Request
from pydantic import ValidationError
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.core.exceptions import DatabaseUnavailableError
from app.db.session import get_engine, get_session_factory
from app.engine.registry import CalculatorRegistry
from app.services.calculation import CalculationService, calculation_service


def _session_factory(request: Request) -> sessionmaker[Session]:
    """The application's session factory, built at the first request that needs ``dec_app``.

    A missing or malformed ``DEC_APP_DATABASE_URL`` becomes ``DatabaseUnavailableError``;
    its text is not carried on, since it can hold the URL (design.md decision 7).
    """
    state = request.app.state
    if state.session_factory is None:
        try:
            state.session_factory = get_session_factory(get_engine(Settings()))  # type: ignore[call-arg]
        except (ValidationError, ArgumentError):
            raise DatabaseUnavailableError("the application database is not configured") from None
    factory: sessionmaker[Session] = state.session_factory
    return factory


def get_session(request: Request) -> Iterator[Session]:
    """One session per request, committed when the route returns without an error."""
    with _session_factory(request)() as session:
        yield session
        session.commit()


def get_registry(request: Request) -> CalculatorRegistry:
    """Реестр типов расчёта, собранный при старте приложения."""
    registry: CalculatorRegistry = request.app.state.registry
    return registry


def get_service(
    request: Request, session: Annotated[Session, Depends(get_session, scope="function")]
) -> CalculationService:
    """Сервис расчётов для одного запроса.

    Зависит от сессии, поэтому базу открывают только маршруты, которым нужен
    сервис; ``GET /calculation-types`` и ``/health`` её не трогают. Сессия
    закрывается с ``scope="function"``: фиксация выполняется до отправки ответа,
    так что ошибка записи даёт ответ об ошибке, а не ``201`` без сохранённого
    результата.

    Args:
        request: текущий запрос; из него берутся реестр, источники и диапазоны.
        session: сессия ``dec_app`` этого запроса.

    Returns:
        Сервис с репозиторием на сессии запроса.
    """
    state = request.app.state
    return calculation_service(
        session,
        state.registry,
        sources=state.sources,
        validated_ranges=state.validated_ranges,
    )

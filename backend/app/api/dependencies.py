import threading
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
from app.services.foundation_design import (
    FoundationDesignService,
    foundation_design_service,
)
from app.services.normatives import NormativesService

_FACTORY_LOCK = threading.Lock()


def _session_factory(request: Request) -> sessionmaker[Session]:
    """Возвращает фабрику сессий приложения, построенную при первом запросе к ``dec_app``.

    Синхронные зависимости выполняются в пуле потоков, поэтому построение защищено
    блокировкой: два первых одновременных запроса строят один движок. Построенный здесь
    движок принадлежит приложению и освобождается при его остановке.

    Args:
        request: текущий запрос; фабрика кэшируется в ``app.state``.

    Returns:
        Фабрика сессий ``dec_app``.

    Raises:
        DatabaseUnavailableError: если ``DEC_APP_DATABASE_URL`` не задан или неверен;
            текст исходной ошибки не передаётся дальше, потому что в нём может быть
            URL (design.md, решение 7).
    """
    state = request.app.state
    if state.session_factory is None:
        with _FACTORY_LOCK:
            if state.session_factory is None:
                try:
                    state.session_factory = get_session_factory(get_engine(Settings()))  # type: ignore[call-arg]
                except (ValidationError, ArgumentError):
                    raise DatabaseUnavailableError("the application database is not configured") from None
                state.owns_session_factory = True
    factory: sessionmaker[Session] = state.session_factory
    return factory


def get_session(request: Request) -> Iterator[Session]:
    """Открывает одну сессию на запрос и фиксирует её, если маршрут завершился без ошибки.

    Args:
        request: текущий запрос.

    Yields:
        Сессия ``dec_app`` этого запроса.

    Raises:
        DatabaseUnavailableError: если база не настроена.
    """
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


def get_normatives_service(request: Request) -> NormativesService:
    """Сервис каталога норм на фабрике сессий каталога приложения.

    Базу ``dec_app`` не открывает: эндпоинтам ``/normatives`` она не нужна.

    Args:
        request: текущий запрос; из него берётся фабрика сессий каталога.

    Returns:
        Сервис поиска и чтения документов каталога.
    """
    return NormativesService(request.app.state.catalog)


def get_foundation_design_service(
    request: Request, session: Annotated[Session, Depends(get_session, scope="function")]
) -> FoundationDesignService:
    state = request.app.state
    return foundation_design_service(
        session, state.registry, sources=state.sources, validated_ranges=state.validated_ranges
    )

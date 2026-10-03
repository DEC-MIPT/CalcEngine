from collections.abc import AsyncIterator, Mapping, Sequence
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, sessionmaker

from app.api.calculations import router as calculations_router
from app.api.errors import install_error_handlers
from app.api.health import router as health_router
from app.api.limits import BodySizeLimit
from app.core.config import ApiSettings
from app.engine.registry import CalculatorRegistry
from app.schemas.calculation import ValidatedBound
from app.services.catalog import build_registry, load_validated_ranges
from app.services.parameter_source import ParameterSource


def create_app(
    api_settings: ApiSettings | None = None,
    registry: CalculatorRegistry | None = None,
    sources: Mapping[str, ParameterSource] | None = None,
    session_factory: sessionmaker[Session] | None = None,
    validated_ranges: Mapping[str, Sequence[ValidatedBound]] | None = None,
) -> FastAPI:
    """Собирает приложение (``calculation-api`` design.md, решения 1 и 7).

    Здесь читаются только ``ApiSettings``; настройки базы читаются при первом
    запросе, которому нужна ``dec_app``. Без переданного реестра при старте
    собираются реестр и проверенные диапазоны из файлов параметров. CORS разрешает
    только источники из ``DEC_CORS_ORIGINS``, без учётных данных (решение 8); заголовки
    ``Location`` и ``Content-Disposition`` открыты браузеру. Тесты передают свои реестр,
    диапазоны, источники и фабрику сессий.

    Args:
        api_settings: настройки API; по умолчанию читаются из окружения.
        registry: готовый реестр типов расчёта.
        sources: источник нормативных параметров для каждого типа.
        session_factory: готовая фабрика сессий ``dec_app``.
        validated_ranges: проверенные диапазоны к переданному реестру.

    Returns:
        Приложение FastAPI.
    """
    settings = api_settings or ApiSettings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        if registry is None:
            app.state.registry = build_registry(settings.dec_params_root)
            app.state.validated_ranges = load_validated_ranges(
                app.state.registry, settings.dec_params_root
            )
        else:
            app.state.registry = registry
            app.state.validated_ranges = dict(validated_ranges or {})
        yield
        if app.state.owns_session_factory:
            app.state.session_factory.kw["bind"].dispose()

    app = FastAPI(title="DEC", lifespan=lifespan)
    app.state.api_settings = settings
    app.state.sources = dict(sources or {})
    app.state.session_factory = session_factory
    app.state.owns_session_factory = False
    install_error_handlers(app)
    app.add_middleware(BodySizeLimit)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.dec_cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
        expose_headers=["Location", "Content-Disposition"],
    )
    app.include_router(health_router)
    app.include_router(calculations_router)
    return app


app = create_app()

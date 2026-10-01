from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import Session, sessionmaker

from app.api.errors import install_error_handlers
from app.api.health import router as health_router
from app.api.limits import BodySizeLimit
from app.core.config import ApiSettings
from app.engine.registry import CalculatorRegistry
from app.services.catalog import build_registry
from app.services.parameter_source import ParameterSource


def create_app(
    api_settings: ApiSettings | None = None,
    registry: CalculatorRegistry | None = None,
    sources: Mapping[str, ParameterSource] | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> FastAPI:
    """The composition root (``calculation-api`` design.md decisions 1 and 7).

    Only ``ApiSettings`` is read here; the database settings are read at the first
    request that needs ``dec_app``. Tests pass their own registry, sources and session
    factory.
    """
    settings = api_settings or ApiSettings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.registry = registry or build_registry(settings.dec_params_root)
        yield

    app = FastAPI(title="DEC", lifespan=lifespan)
    app.state.api_settings = settings
    app.state.sources = dict(sources or {})
    app.state.session_factory = session_factory
    install_error_handlers(app)
    app.add_middleware(BodySizeLimit)
    app.include_router(health_router)
    return app


app = create_app()

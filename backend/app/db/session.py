from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine, make_url
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings


def as_psycopg_url(raw_url: str) -> URL:
    """Приводит голый URL ``postgresql://`` к установленному драйверу psycopg (v3).

    Зависимость проекта — только ``psycopg``, а не ``psycopg2`` (его SQLAlchemy берёт
    по умолчанию для голой схемы ``postgresql``), поэтому URL, скопированный из
    ``.env.example`` как есть, иначе упал бы с ``ModuleNotFoundError``. Используется
    и в ``backend/alembic/env.py``, чтобы оба подключались одинаково.

    Args:
        raw_url: URL базы в любом виде схемы ``postgresql``.

    Returns:
        URL с драйвером ``postgresql+psycopg``.
    """
    return make_url(raw_url).set(drivername="postgresql+psycopg")


def get_engine(settings: Settings | None = None) -> Engine:
    settings = settings or Settings()  # type: ignore[call-arg]
    return create_engine(
        as_psycopg_url(settings.dec_app_database_url.get_secret_value()), hide_parameters=True
    )


def get_session_factory(engine: Engine | None = None) -> sessionmaker[Session]:
    return sessionmaker(bind=engine or get_engine(), autoflush=False, autocommit=False)

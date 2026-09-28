from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine, make_url
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings


def as_psycopg_url(raw_url: str) -> URL:
    """Normalize a bare ``postgresql://`` URL to the installed psycopg (v3) driver.

    Only ``psycopg`` is a project dependency, not ``psycopg2`` (SQLAlchemy's default
    for the bare ``postgresql`` scheme), so a URL copied from ``.env.example`` as-is
    would otherwise fail with ``ModuleNotFoundError``. Reused by ``backend/alembic/
    env.py`` so both connect the same way.
    """
    return make_url(raw_url).set(drivername="postgresql+psycopg")


def get_engine(settings: Settings | None = None) -> Engine:
    settings = settings or Settings()  # type: ignore[call-arg]
    return create_engine(as_psycopg_url(settings.dec_app_database_url.get_secret_value()))


def get_session_factory(engine: Engine | None = None) -> sessionmaker[Session]:
    return sessionmaker(bind=engine or get_engine(), autoflush=False, autocommit=False)

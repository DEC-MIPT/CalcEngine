import pytest
from pydantic import SecretStr

from app.core.config import Settings
from app.db.session import as_psycopg_url, get_engine, get_session_factory


def _fake_settings() -> Settings:
    return Settings(
        dec_app_database_url=SecretStr("postgresql://user:pass@localhost/dec_app")  # pragma: allowlist secret
    )


def test_as_psycopg_url_normalizes_bare_postgresql_scheme() -> None:
    url = as_psycopg_url("postgresql://user:pass@localhost/dec_app")  # pragma: allowlist secret
    assert url.drivername == "postgresql+psycopg"


def test_get_engine_normalizes_to_psycopg_driver() -> None:
    engine = get_engine(_fake_settings())
    try:
        assert engine.url.drivername == "postgresql+psycopg"
    finally:
        engine.dispose()


def test_get_engine_reads_settings_from_environment_when_not_given(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "DEC_APP_DATABASE_URL", "postgresql://user:pass@localhost/dec_app"  # pragma: allowlist secret
    )

    engine = get_engine()
    try:
        assert engine.url.drivername == "postgresql+psycopg"
    finally:
        engine.dispose()


def test_get_session_factory_binds_to_the_given_engine() -> None:
    engine = get_engine(_fake_settings())
    session_factory = get_session_factory(engine)
    session = session_factory()
    try:
        assert session.bind is engine
    finally:
        session.close()
        engine.dispose()

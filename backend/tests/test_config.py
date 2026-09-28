import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_settings_read_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "DEC_APP_DATABASE_URL", "postgresql://app_user:apppass@localhost/dec_app"
    )
    monkeypatch.setenv(
        "DEC_NORMATIVES_DATABASE_URL",
        "postgresql://norm_user:normpass@localhost/dec_normatives",
    )

    # mypy synthesizes Settings.__init__ from the model's fields and does not know
    # pydantic-settings fills a required field from the environment at runtime.
    settings = Settings()  # type: ignore[call-arg]

    assert (
        settings.dec_app_database_url.get_secret_value()
        == "postgresql://app_user:apppass@localhost/dec_app"
    )
    assert settings.dec_normatives_database_url is not None
    assert (
        settings.dec_normatives_database_url.get_secret_value()
        == "postgresql://norm_user:normpass@localhost/dec_normatives"
    )


def test_normatives_url_is_optional(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "DEC_APP_DATABASE_URL", "postgresql://app_user:apppass@localhost/dec_app"
    )
    monkeypatch.delenv("DEC_NORMATIVES_DATABASE_URL", raising=False)

    settings = Settings()  # type: ignore[call-arg]

    assert settings.dec_normatives_database_url is None


def test_missing_app_url_raises_validation_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)
    monkeypatch.delenv("DEC_NORMATIVES_DATABASE_URL", raising=False)

    with pytest.raises(ValidationError) as exc_info:
        Settings()  # type: ignore[call-arg]

    assert "DEC_APP_DATABASE_URL" in str(exc_info.value)


def test_repr_and_str_hide_password(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "DEC_APP_DATABASE_URL",
        "postgresql://app_user:supersecretpassword@localhost/dec_app",
    )
    monkeypatch.delenv("DEC_NORMATIVES_DATABASE_URL", raising=False)

    settings = Settings()  # type: ignore[call-arg]

    assert "supersecretpassword" not in repr(settings)
    assert "supersecretpassword" not in str(settings)

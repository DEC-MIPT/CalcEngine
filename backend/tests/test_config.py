from pathlib import Path

import pytest
from pydantic import ValidationError

from app.core.config import PARAMS_ROOT, ApiSettings, NormativesSettings, Settings

APP_DIR = Path(__file__).resolve().parents[1] / "app"


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
    assert not hasattr(settings, "dec_normatives_database_url")


def test_normatives_url_is_unset_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)
    monkeypatch.delenv("DEC_NORMATIVES_DATABASE_URL", raising=False)

    assert NormativesSettings().dec_normatives_database_url is None


def test_normatives_url_is_read_without_the_app_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)
    monkeypatch.setenv(
        "DEC_NORMATIVES_DATABASE_URL",
        "postgresql://dec_normatives_reader:normpass@localhost/dec",
    )

    settings = NormativesSettings()

    assert settings.dec_normatives_database_url is not None
    assert (
        settings.dec_normatives_database_url.get_secret_value()
        == "postgresql://dec_normatives_reader:normpass@localhost/dec"
    )
    assert "normpass" not in repr(settings) and "normpass" not in str(settings)


def test_only_the_normatives_settings_read_the_normatives_variable() -> None:
    readers = [
        path.relative_to(APP_DIR).as_posix()
        for path in sorted(APP_DIR.rglob("*.py"))
        if "DEC_NORMATIVES_DATABASE_URL" in path.read_text(encoding="utf-8")
    ]

    assert readers == ["core/config.py"]
    assert (APP_DIR / "core" / "config.py").read_text(encoding="utf-8").count(
        'validation_alias="DEC_NORMATIVES_DATABASE_URL"'
    ) == 1


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


@pytest.fixture
def no_api_variables(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    for name in ("DEC_CORS_ORIGINS", "DEC_PARAMS_ROOT", "DEC_APP_DATABASE_URL", "DEC_NORMATIVES_DATABASE_URL"):
        monkeypatch.delenv(name, raising=False)
    return monkeypatch


def test_api_settings_need_no_variable(no_api_variables: pytest.MonkeyPatch) -> None:
    settings = ApiSettings()

    assert settings.dec_cors_origins == []
    assert settings.dec_params_root == PARAMS_ROOT


def test_cors_origins_are_comma_separated(no_api_variables: pytest.MonkeyPatch) -> None:
    no_api_variables.setenv("DEC_CORS_ORIGINS", "http://localhost:5173, https://dec.example ,")

    assert ApiSettings().dec_cors_origins == ["http://localhost:5173", "https://dec.example"]


def test_an_empty_origin_variable_gives_no_origin(no_api_variables: pytest.MonkeyPatch) -> None:
    no_api_variables.setenv("DEC_CORS_ORIGINS", "")

    assert ApiSettings().dec_cors_origins == []


def test_the_default_params_root_holds_the_pilot_parameter_file() -> None:
    assert (PARAMS_ROOT / "foundations_shallow_r.yaml").is_file()
    assert PARAMS_ROOT == Path(__file__).resolve().parents[1] / "params"


def test_the_params_root_is_read_from_the_environment(
    no_api_variables: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    no_api_variables.setenv("DEC_PARAMS_ROOT", str(tmp_path))

    assert ApiSettings().dec_params_root == tmp_path

from pathlib import Path
from typing import Annotated

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode

PARAMS_ROOT = Path(__file__).resolve().parents[2] / "params"
"""Каталог ``backend/params``, найденный от пакета, чтобы не записывать путь конкретной машины."""


class Settings(BaseSettings):
    dec_app_database_url: SecretStr = Field(validation_alias="DEC_APP_DATABASE_URL")


class NormativesSettings(BaseSettings):
    """Подключение к каталогу норм; поле не обязательно (``normative-catalog-backend`` design.md, решение 4).

    Единственный читатель ``DEC_NORMATIVES_DATABASE_URL``: каталог работает без
    ``DEC_APP_DATABASE_URL``, а без этой переменной отвечает ``503 catalog_unavailable``.
    """

    dec_normatives_database_url: SecretStr | None = Field(
        default=None, validation_alias="DEC_NORMATIVES_DATABASE_URL"
    )


class ApiSettings(BaseSettings):
    """Что нужно приложению для старта; ни одно поле не обязательно (design.md, решение 7).

    URL баз остаются в ``Settings`` и читаются при первом запросе, которому они нужны.
    """

    dec_cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=list, validation_alias="DEC_CORS_ORIGINS"
    )
    dec_params_root: Path = Field(default=PARAMS_ROOT, validation_alias="DEC_PARAMS_ROOT")

    @field_validator("dec_cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

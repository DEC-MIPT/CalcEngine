from pathlib import Path
from typing import Annotated

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode

PARAMS_ROOT = Path(__file__).resolve().parents[2] / "params"
"""``backend/params``, found from the package so that no machine path is written down."""


class Settings(BaseSettings):
    dec_app_database_url: SecretStr = Field(validation_alias="DEC_APP_DATABASE_URL")
    dec_normatives_database_url: SecretStr | None = Field(
        default=None, validation_alias="DEC_NORMATIVES_DATABASE_URL"
    )


class ApiSettings(BaseSettings):
    """What the application needs to start; no field is required (design.md decision 7).

    The database URLs stay in ``Settings``, read at the first request that needs them.
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

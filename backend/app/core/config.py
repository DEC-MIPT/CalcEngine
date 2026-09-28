from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    dec_app_database_url: SecretStr = Field(validation_alias="DEC_APP_DATABASE_URL")
    dec_normatives_database_url: SecretStr | None = Field(
        default=None, validation_alias="DEC_NORMATIVES_DATABASE_URL"
    )

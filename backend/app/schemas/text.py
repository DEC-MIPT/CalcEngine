from pydantic import BaseModel, ConfigDict, Field


class LocalizedText(BaseModel):
    """Текст для человека на двух языках.

    Русский текст обязателен по смыслу, но его непустоту проверяет регистрация типа
    расчёта, чтобы сообщение называло величину (``frontend-app`` design.md, решение 6).

    Attributes:
        ru: русский текст.
        en: английский текст; если его нет, интерфейс показывает русский.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    ru: str
    en: str | None = Field(default=None, min_length=1)

import datetime
import unicodedata
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, model_validator

XML_FORBIDDEN = frozenset({0xFFFE, 0xFFFF})
"""Символы вне управляющих и суррогатов, которых нет в наборе символов XML 1.0."""


def writable_character(character: str) -> bool:
    """Проверяет, можно ли записать символ в текст отчёта.

    Args:
        character: один символ.

    Returns:
        ``False`` для управляющего символа (Cc), суррогата, U+FFFE и U+FFFF.
    """
    code = ord(character)
    return not (
        unicodedata.category(character) == "Cc"
        or 0xD800 <= code <= 0xDFFF
        or code in XML_FORBIDDEN
    )


def _writable_text(text: str) -> str:
    """Проверяет, что текст можно записать в документ.

    Отклоняются управляющие символы (категория Cc, в том числе табуляция и перевод
    строки) и любой другой символ, недопустимый в XML 1.0: суррогаты, U+FFFE и U+FFFF
    (``report-generator`` "GOST report structure", design.md, решение 18).

    Args:
        text: текст основной надписи или блока подписей.

    Returns:
        Тот же текст.

    Raises:
        ValueError: если в тексте есть такой символ.
    """
    if not all(writable_character(character) for character in text):
        raise ValueError(
            "text must not contain a control character or another character XML 1.0 does not allow"
        )
    return text


Text = Annotated[str, AfterValidator(_writable_text)]


class TitleBlockData(BaseModel):
    """Данные запроса на отчёт для граф 1, 5, 6 и 9 основной надписи формы 5.

    По GOST R 21.101-2026 (edition unverified), приложение Е: графа 1 — обозначение
    документа, 5 — наименование документа, 6 — вид документации, 9 — организация.
    Графа 6 может остаться пустой. Граф 2 и 3 в форме 5 нет.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    designation: Text
    document_name: Text
    documentation_kind: Text = ""
    organization: Text


class Signatory(BaseModel):
    """Подписант блока подписей: фамилия (графа 11) и дата подписания (графа 13)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    surname: Text = ""
    date: datetime.date | None = None

    @property
    def complete(self) -> bool:
        return bool(self.surname.strip()) and self.date is not None


class ReportRequest(BaseModel):
    """Что нужно отчёту, кроме конверта ("GOST report structure").

    Блок подписей по умолчанию включён. Пока он включён, строкам разработчика и
    нормоконтроля нужны фамилия и дата, а проверяющему, если он указан, — тоже обе;
    иначе запрос отклоняется до построения отчёта.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    title: TitleBlockData
    signature_block: bool = True
    developer: Signatory | None = None
    normative_control: Signatory | None = None
    checker: Signatory | None = None

    @model_validator(mode="after")
    def _signatories_are_complete(self) -> "ReportRequest":
        if not self.signature_block:
            return self
        for role in ("developer", "normative_control"):
            signatory = getattr(self, role)
            if signatory is None or not signatory.complete:
                raise ValueError(f"the signature block needs the surname and the date of {role}")
        if self.checker is not None and not self.checker.complete:
            raise ValueError("a checker needs a surname and a date")
        return self

import datetime
import unicodedata
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, model_validator


def _no_control_character(text: str) -> str:
    if any(unicodedata.category(character) == "Cc" for character in text):
        raise ValueError("text must not contain a control character (Unicode category Cc)")
    return text


Text = Annotated[str, AfterValidator(_no_control_character)]


class TitleBlockData(BaseModel):
    """What the report request gives for columns 1, 2, 3, 5, 6 and 9 of the form-5 title block.

    GOST R 21.101-2026 (edition unverified), Annex E: column 1 is the designation of the
    document, 2 the enterprise or complex, 3 the building, 5 the name of the document,
    6 the kind of documentation, 9 the organization. Columns 2, 3 and 6 may stay empty.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    designation: Text
    enterprise: Text = ""
    building: Text = ""
    document_name: Text
    documentation_kind: Text = ""
    organization: Text


class Signatory(BaseModel):
    """A person of the signature block: surname (column 11) and date of signing (column 13)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    surname: Text = ""
    date: datetime.date | None = None

    @property
    def complete(self) -> bool:
        return bool(self.surname.strip()) and self.date is not None


class ReportRequest(BaseModel):
    """What a report needs besides the envelope ("GOST report structure").

    The signature block is enabled by default. While it is enabled, the developer and the
    normative control lines need a surname and a date, and a checker, when given, needs
    both too; otherwise the request is rejected before any report is built.
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

import datetime
from io import BytesIO
from typing import Any

import pytest
from docx import Document
from pydantic import ValidationError

from app.schemas.report import (
    ReportRequest,
    Signatory,
    TitleBlockData,
    writable_character,
)

DAY = datetime.date(2026, 9, 30)


def title(**changes: Any) -> dict[str, Any]:
    return {"designation": "<DESIGNATION>", "document_name": "<DOCUMENT>", "organization": "<ORG>"} | changes


def person(surname: str = "<SURNAME>", date: datetime.date | None = DAY) -> dict[str, Any]:
    return {"surname": surname, "date": date}


def request(**changes: Any) -> ReportRequest:
    data: dict[str, Any] = {"title": title(), "developer": person(), "normative_control": person()}
    return ReportRequest.model_validate(data | changes)


def test_the_signature_block_is_enabled_by_default() -> None:
    assert request().signature_block is True


def test_column_6_may_stay_empty() -> None:
    assert TitleBlockData.model_validate(title()).documentation_kind == ""


@pytest.mark.parametrize("column", ["enterprise", "building"])
def test_form_5_has_no_columns_2_and_3(column: str) -> None:
    with pytest.raises(ValidationError, match="Extra inputs"):
        TitleBlockData.model_validate(title(**{column: "<TEXT>"}))


@pytest.mark.parametrize(
    "changes",
    [
        {"developer": None},
        {"normative_control": None},
        {"developer": person(date=None)},
        {"developer": person(surname="")},
        {"normative_control": person(surname="   ")},
        {"checker": person(date=None)},
        {"checker": person(surname="")},
    ],
    ids=[
        "no-developer",
        "no-normative-control",
        "developer-without-date",
        "developer-without-surname",
        "normative-control-blank-surname",
        "checker-without-date",
        "checker-without-surname",
    ],
)
def test_an_enabled_signature_block_rejects_an_incomplete_signatory(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError, match="surname and"):
        request(**changes)


def test_a_complete_checker_is_accepted() -> None:
    assert request(checker=person()).checker == Signatory(surname="<SURNAME>", date=DAY)


def test_a_disabled_signature_block_needs_no_signatory() -> None:
    disabled = ReportRequest.model_validate(
        {"title": title(), "signature_block": False, "checker": person(date=None)}
    )

    assert (disabled.developer, disabled.normative_control) == (None, None)


@pytest.mark.parametrize("character", ["\n", "\t", "\x00", "\x7f"], ids=["lf", "tab", "nul", "del"])
@pytest.mark.parametrize("field", ["designation", "documentation_kind", "surname"])
def test_a_control_character_in_any_text_is_rejected(field: str, character: str) -> None:
    text = f"a{character}b"
    changes = {"developer": person(surname=text)} if field == "surname" else {"title": title(**{field: text})}

    with pytest.raises(ValidationError, match="control character"):
        request(**changes)


def test_unicode_letters_and_signs_are_not_control_characters() -> None:
    accepted = request(title=title(designation="ПР-01/2026 «Основания» №5"))

    assert accepted.title.designation == "ПР-01/2026 «Основания» №5"


@pytest.mark.parametrize(
    "character", [chr(0xFFFE), chr(0xFFFF), chr(0xD800), chr(0xDFFF)], ids=["fffe", "ffff", "surrogate-low", "surrogate-high"]
)
@pytest.mark.parametrize("field", ["designation", "document_name", "organization", "surname"])
def test_a_character_xml_does_not_allow_is_rejected(field: str, character: str) -> None:
    text = f"a{character}b"
    changes = {"developer": person(surname=text)} if field == "surname" else {"title": title(**{field: text})}

    with pytest.raises(ValidationError, match="XML 1.0"):
        request(**changes)


def test_every_character_the_schema_accepts_can_be_written_to_a_docx() -> None:
    accepted = "".join(
        chr(code)
        for code in [*range(0x10000), 0x10000, 0x1F600, 0x10FFFD]
        if writable_character(chr(code))
    )
    document = Document()

    document.add_paragraph(accepted)
    document.save(BytesIO())

    assert len(accepted) == 0x10000 - 0x20 - 0x21 - 0x800 - 2 + 3

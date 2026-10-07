import datetime
from io import BytesIO
from typing import Any

import pytest
from docx import Document
from pydantic import ValidationError

from app.schemas.report import (
    MAX_LENGTH,
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

    with pytest.raises(ValidationError) as rejected:
        request(**changes)
    expected = "string_unicode" if 0xD800 <= ord(character) <= 0xDFFF else "value_error"
    assert [error["type"] for error in rejected.value.errors()] == [expected]


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


TITLE_FIELDS = {"designation": "1", "document_name": "5", "documentation_kind": "6", "organization": "9"}
ROLES = ("developer", "checker", "normative_control")


def cyrillic(length: int) -> str:
    return ("Ж" * length)[:length]


@pytest.mark.parametrize("field", list(TITLE_FIELDS))
def test_a_title_text_at_its_limit_is_accepted_and_one_more_character_is_rejected(field: str) -> None:
    limit = MAX_LENGTH[TITLE_FIELDS[field]]

    assert getattr(TitleBlockData.model_validate(title(**{field: cyrillic(limit)})), field) == cyrillic(limit)
    with pytest.raises(ValidationError) as rejected:
        TitleBlockData.model_validate(title(**{field: cyrillic(limit + 1)}))
    assert [(error["type"], error["loc"], error["ctx"]) for error in rejected.value.errors()] == [
        ("string_too_long", (field,), {"max_length": limit})
    ]


@pytest.mark.parametrize("role", ROLES)
def test_a_surname_at_its_limit_is_accepted_and_one_more_character_is_rejected(role: str) -> None:
    limit = MAX_LENGTH["11"]

    assert getattr(request(**{role: person(surname=cyrillic(limit))}), role).surname == cyrillic(limit)
    with pytest.raises(ValidationError) as rejected:
        request(**{role: person(surname=cyrillic(limit + 1))})
    assert [(error["type"], error["loc"]) for error in rejected.value.errors()] == [
        ("string_too_long", (role, "surname"))
    ]


def test_the_limit_counts_characters_not_bytes() -> None:
    text = cyrillic(MAX_LENGTH["1"])

    assert len(text.encode()) > MAX_LENGTH["1"]
    assert TitleBlockData.model_validate(title(designation=text)).designation == text


def test_the_length_is_checked_before_the_characters() -> None:
    with pytest.raises(ValidationError) as rejected:
        TitleBlockData.model_validate(title(designation=cyrillic(MAX_LENGTH["1"]) + "\x00"))
    assert [error["type"] for error in rejected.value.errors()] == ["string_too_long"]


def test_the_limits_are_in_the_json_schema() -> None:
    definitions = ReportRequest.model_json_schema()["$defs"]
    title_properties = definitions["TitleBlockData"]["properties"]

    assert {field: title_properties[field]["maxLength"] for field in TITLE_FIELDS} == {
        field: MAX_LENGTH[column] for field, column in TITLE_FIELDS.items()
    }
    assert definitions["Signatory"]["properties"]["surname"]["maxLength"] == MAX_LENGTH["11"]

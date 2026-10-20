import logging
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pytest
import yaml
from interim_fixture import (
    VERIFIER,
    assert_before_sunset,
    formula,
    manifest,
    table_value,
    type_file,
    write,
)

from app.core.exceptions import ParameterValidationError
from app.parameters.interim_loader import load_interim_root
from app.parameters.interim_schemas import InterimFormula, InterimTableValue
from app.services.interim_data import (
    Profile,
    check_documents,
    document_digest,
    effective_status,
    record_digest,
    warn_passed_sunsets,
)

TYPE = "synthetic_type"
SECRET = 987.654321
"""Синтетическое значение-метка: если оно попадёт в лог, тест это увидит."""


def verified(record: dict[str, Any], model: type[InterimFormula] | type[InterimTableValue] = InterimFormula) -> dict[str, Any]:
    """Запись, какой её оставил бы верификатор: с ``value_digest`` её текущего значения."""
    digest = record_digest(model.model_validate(record))
    return record | {
        "verification": {"status": "human-verified", "by": VERIFIER, "at": "2026-10-21", "portion": "P1", "value_digest": digest}
    }


def rejected(record: dict[str, Any]) -> dict[str, Any]:
    return record | {"verification": {"status": "rejected", "by": VERIFIER, "at": "2026-10-21", "comment": "<REASON>"}}


def load(root: Path, profile: Profile = "strict", **lists: Any) -> Any:
    write(root / "doc" / "manifest.yaml", manifest())
    write(root / "doc" / f"{TYPE}.yaml", type_file(**lists))
    return check_documents(load_interim_root(root, {TYPE}), profile)[TYPE]


def messages(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [record.getMessage() for record in caplog.records if record.name == "app.services.interim_data"]


def test_a_verified_record_with_its_digest_stays_verified(tmp_path: Path) -> None:
    data = load(tmp_path, formulas=[verified(formula())])

    assert data.file == f"doc/{TYPE}.yaml"
    assert [(checked.path, checked.status) for checked in data.records] == [("formulas[0]", "human-verified")]


@pytest.mark.parametrize(
    "change",
    [{"value": 2.0}, {"unit": "m"}, {"heading_symbol": "phi_II", "heading_value": 10.0, "heading_unit": "deg"}, {"page": 2}],
    ids=["value", "unit", "heading", "page"],
)
def test_a_changed_value_of_a_verified_record_counts_as_pending_and_is_named(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, change: dict[str, Any]
) -> None:
    edited = verified(table_value(value=SECRET), InterimTableValue) | change

    with caplog.at_level(logging.WARNING):
        data = load(tmp_path, "draft", table_values=[edited])

    assert data.records[0].status == "pending"
    assert data.records[0].record.verification.status == "human-verified"
    assert messages(caplog) == [f"code=interim_value_changed file=doc/{TYPE}.yaml record=table_values[0]"]


@pytest.mark.parametrize(
    "change",
    [
        {"tree": {"kind": "number", "value": 3.0}},
        {"norm_refs": [{"document": "<NORM-DOC-PLACEHOLDER-2>", "edition": "unverified", "clause": "unverified", "status": "unverified", "provenance": "machine-extracted"}]},
    ],
    ids=["tree", "references"],
)
def test_a_changed_tree_or_reference_needs_a_new_check(tmp_path: Path, change: dict[str, Any]) -> None:
    data = load(tmp_path, "draft", formulas=[verified(formula()) | change])

    assert data.records[0].status == "pending"


def test_the_digest_ignores_the_verification_record() -> None:
    record = InterimFormula.model_validate(formula())
    other = InterimFormula.model_validate(rejected(formula()))

    assert record_digest(record) == record_digest(other)
    assert len(record_digest(record)) == 64


def test_pending_and_rejected_records_keep_their_status() -> None:
    assert effective_status(InterimFormula.model_validate(formula())) == "pending"
    assert effective_status(InterimFormula.model_validate(rejected(formula()))) == "rejected"


def test_a_pending_record_without_a_verifier_passes(tmp_path: Path) -> None:
    data = load(tmp_path, "draft", formulas=[formula(page=None)])

    assert data.records[0].status == "pending"


@pytest.mark.parametrize(
    ("verification", "message"),
    [
        ({"status": "human-verified", "by": VERIFIER, "at": "2026-10-21", "portion": "P1"}, "a human-verified record needs: value_digest"),
        ({"status": "rejected", "by": VERIFIER, "at": "2026-10-21"}, "a rejected record needs: comment"),
    ],
    ids=["verified", "rejected"],
)
def test_a_checked_record_without_its_fields_stops_the_start_naming_file_record_and_field(
    tmp_path: Path, verification: dict[str, Any], message: str
) -> None:
    with pytest.raises(ParameterValidationError) as raised:
        load(tmp_path, formulas=[formula(verification=verification)])

    assert str(raised.value) == f"doc/{TYPE}.yaml: formulas.0.verification: Value error, {message}"


def test_strict_names_every_unchecked_record_at_startup(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING):
        data = load(tmp_path, formulas=[verified(formula()), formula(), rejected(formula())], table_values=[table_value(value=SECRET)])

    assert len(data.records) == 4
    assert messages(caplog) == [
        f"code=interim_record_unchecked file=doc/{TYPE}.yaml record=formulas[1] status=pending",
        f"code=interim_record_unchecked file=doc/{TYPE}.yaml record=formulas[2] status=rejected",
        f"code=interim_record_unchecked file=doc/{TYPE}.yaml record=table_values[0] status=pending",
    ]
    assert not any(str(SECRET) in message for message in messages(caplog))


def test_draft_lists_no_unchecked_record(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING):
        load(tmp_path, "draft", formulas=[formula()])

    assert messages(caplog) == []


def digest_of(root: Path) -> str:
    (document,) = load_interim_root(root, {TYPE})
    return document_digest(document)


def test_the_digest_is_carried_by_each_type_of_the_document(tmp_path: Path) -> None:
    data = load(tmp_path, "draft", formulas=[formula()])

    assert data.data_sha256 == digest_of(tmp_path)
    assert re.fullmatch(r"[0-9a-f]{64}", data.data_sha256)


def test_the_digest_does_not_depend_on_comments_key_order_indentation_or_line_breaks(tmp_path: Path) -> None:
    plain, styled = tmp_path / "plain", tmp_path / "styled"
    write(plain / "doc" / "manifest.yaml", manifest())
    write(plain / "doc" / f"{TYPE}.yaml", type_file(formulas=[formula()]))
    write(styled / "doc" / "manifest.yaml", dict(reversed(list(manifest().items()))))
    styled_file = styled / "doc" / f"{TYPE}.yaml"
    record = dict(reversed(list(formula().items())))
    text = yaml.safe_dump(
        {"method_bounds": [], "checks": [], "thresholds": [], "table_values": [], "formulas": [record]},
        indent=4,
        width=20,
        allow_unicode=True,
    )
    styled_file.write_text("# <COMMENT>\n" + text.replace("\n", "\r\n"), encoding="utf-8")

    assert digest_of(plain) == digest_of(styled)
    assert digest_of(plain) == digest_of(plain)


def test_a_float_written_as_an_integer_gives_the_same_digest(tmp_path: Path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    for root, value in ((first, 1.0), (second, 1)):
        write(root / "doc" / "manifest.yaml", manifest())
        write(root / "doc" / f"{TYPE}.yaml", type_file(table_values=[table_value(value=value)]))

    assert digest_of(first) == digest_of(second)


@pytest.mark.parametrize(
    ("target", "change"),
    [
        ("type", {"value": 2.0}),
        ("type", {"page": 2}),
        ("type", {"norm_refs": [{"document": "<NORM-DOC-PLACEHOLDER-2>", "edition": "unverified", "clause": "unverified", "status": "unverified", "provenance": "machine-extracted"}]}),
        ("type", {"verification": {"status": "pending", "comment": "<NOTE>"}}),
        ("manifest", {"edition": "<EDITION-2>"}),
    ],
    ids=["value", "page", "reference", "verification", "manifest"],
)
def test_the_digest_follows_the_data(tmp_path: Path, target: str, change: dict[str, Any]) -> None:
    before, after = tmp_path / "before", tmp_path / "after"
    write(before / "doc" / "manifest.yaml", manifest())
    write(before / "doc" / f"{TYPE}.yaml", type_file(table_values=[table_value()]))
    write(after / "doc" / "manifest.yaml", manifest(**change) if target == "manifest" else manifest())
    write(after / "doc" / f"{TYPE}.yaml", type_file(table_values=[table_value(**change) if target == "type" else table_value()]))

    assert digest_of(before) != digest_of(after)


def test_the_digest_covers_every_type_file_of_the_document(tmp_path: Path) -> None:
    write(tmp_path / "doc" / "manifest.yaml", manifest())
    write(tmp_path / "doc" / f"{TYPE}.yaml", type_file())
    alone = digest_of(tmp_path)
    write(tmp_path / "doc" / "another_type.yaml", type_file())

    (document,) = load_interim_root(tmp_path, {TYPE, "another_type"})

    assert document_digest(document) != alone


SUNSET = date(2099, 12, 31)


def test_on_or_before_the_sunset_nothing_is_logged_and_the_reminder_passes(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    path = write(tmp_path / "doc" / "manifest.yaml", manifest())
    documents = load_interim_root(tmp_path, set())

    with caplog.at_level(logging.WARNING):
        assert warn_passed_sunsets(documents, SUNSET) == ()
        assert warn_passed_sunsets(documents, SUNSET - timedelta(days=1)) == ()

    assert messages(caplog) == []
    assert_before_sunset(path, SUNSET)


def test_after_the_sunset_a_warning_names_document_date_and_event_and_the_reminder_fails(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    path = write(tmp_path / "doc" / "manifest.yaml", manifest())
    documents = load_interim_root(tmp_path, set())
    after = SUNSET + timedelta(days=1)

    with caplog.at_level(logging.WARNING):
        assert warn_passed_sunsets(documents, after) == ("doc",)

    assert messages(caplog) == ["code=interim_sunset_passed document=doc date=2099-12-31 event=<SUNSET-EVENT>"]
    with pytest.raises(AssertionError, match="passed its sunset 2099-12-31"):
        assert_before_sunset(path, after)

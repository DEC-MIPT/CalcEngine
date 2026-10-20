from typing import Any

import pytest
from interim_fixture import PENDING, VERIFIER, formula, manifest, table_value, type_file
from pydantic import ValidationError

from app.parameters.interim_schemas import (
    IDENTIFIER_LIMIT,
    LATEX_LIMIT,
    InterimManifest,
    InterimTypeFile,
    VerificationRecord,
    problems,
)

DIGEST = "0" * 64


def rejected(data: dict[str, Any], model: type[InterimTypeFile] | type[InterimManifest] = InterimTypeFile) -> tuple[str, ...]:
    with pytest.raises(ValidationError) as raised:
        model.model_validate(data)
    return problems(raised.value)


def test_a_type_file_with_its_five_lists_is_accepted() -> None:
    parsed = InterimTypeFile.model_validate(type_file(formulas=[formula()], table_values=[table_value()]))

    assert [path for path, _ in parsed.records()] == ["formulas[0]", "table_values[0]"]
    assert parsed.formulas[0].norm_refs[0].status == "unverified"


@pytest.mark.parametrize("refs", [None, []], ids=["no norm_refs", "empty norm_refs"])
def test_a_record_without_a_reference_is_rejected_naming_its_path(refs: list[object] | None) -> None:
    record = formula()
    if refs is None:
        del record["norm_refs"]
    else:
        record["norm_refs"] = refs

    found = rejected(type_file(formulas=[formula(), record]))

    assert any(problem.startswith("formulas.1.norm_refs:") for problem in found)


@pytest.mark.parametrize(
    ("data", "model", "path"),
    [
        (type_file(formulas=[formula(source_text="<TEXT>")]), InterimTypeFile, "formulas.0.source_text"),
        (type_file(notes=[]), InterimTypeFile, "notes"),
        (manifest(title="<TITLE>"), InterimManifest, "title"),
        (type_file(formulas=[formula(verification={"status": "pending", "note": "x"})]), InterimTypeFile, "formulas.0.verification.note"),
    ],
    ids=["record", "type file", "manifest", "verification"],
)
def test_an_unknown_field_is_rejected_naming_its_path(
    data: dict[str, Any], model: type[InterimTypeFile] | type[InterimManifest], path: str
) -> None:
    assert rejected(data, model) == (f"{path}: Extra inputs are not permitted",)


def test_a_type_file_without_one_of_its_lists_is_rejected() -> None:
    data = type_file()
    del data["checks"]

    assert rejected(data) == ("checks: Field required",)


@pytest.mark.parametrize(
    ("record", "prefix"),
    [
        (formula(latex="Ж" * (LATEX_LIMIT + 1)), "formulas.0.latex: "),
        (formula(parameter="p" * (IDENTIFIER_LIMIT + 1)), "formulas.0.parameter: "),
        (formula(units={"x": "1", "u" * (IDENTIFIER_LIMIT + 1): "1"}), "formulas.0.units.<key>.[key]: "),
        (formula(tree={"kind": "symbol", "name": "s" * (IDENTIFIER_LIMIT + 1)}), "formulas.0.tree: "),
        (
            formula(tree={"kind": "call", "function": "f" * (IDENTIFIER_LIMIT + 1), "args": [{"kind": "number", "value": 1.0}]}),
            "formulas.0.tree: ",
        ),
    ],
    ids=["latex", "parameter", "unit key", "symbol in tree", "function in tree"],
)
def test_an_over_long_label_is_rejected_without_repeating_it(record: dict[str, Any], prefix: str) -> None:
    found = rejected(type_file(formulas=[record]))

    assert any(problem.startswith(prefix) for problem in found), found
    assert not any(letter * 20 in problem for problem in found for letter in "Жpusf")


def test_the_limits_count_unicode_code_points() -> None:
    accepted = InterimTypeFile.model_validate(type_file(formulas=[formula(latex="Ж" * LATEX_LIMIT)]))

    assert len(accepted.formulas[0].latex) == LATEX_LIMIT


def test_an_invalid_tree_is_rejected_without_its_text() -> None:
    found = rejected(type_file(formulas=[formula(tree={"kind": "power", "base": "<SECRET-TEXT>"})]))

    assert found == ("formulas.0.tree: Value error, the expression tree is not valid",)


def test_a_non_finite_value_is_rejected() -> None:
    assert rejected(type_file(table_values=[table_value(value=float("inf"))]))[0].startswith("table_values.0.value:")


@pytest.mark.parametrize(
    ("verification", "missing"),
    [
        ({"status": "human-verified", "at": "2026-10-21", "portion": "P1", "value_digest": DIGEST}, "by"),
        ({"status": "human-verified", "by": VERIFIER, "portion": "P1", "value_digest": DIGEST}, "at"),
        ({"status": "human-verified", "by": VERIFIER, "at": "2026-10-21", "value_digest": DIGEST}, "portion"),
        ({"status": "human-verified", "by": VERIFIER, "at": "2026-10-21", "portion": "P1"}, "value_digest"),
        ({"status": "rejected", "at": "2026-10-21", "comment": "<REASON>"}, "by"),
        ({"status": "rejected", "by": VERIFIER, "comment": "<REASON>"}, "at"),
        ({"status": "rejected", "by": VERIFIER, "at": "2026-10-21"}, "comment"),
    ],
)
def test_a_checked_record_without_its_fields_is_rejected_naming_the_field(
    verification: dict[str, Any], missing: str
) -> None:
    found = rejected(type_file(formulas=[formula(verification=verification)]))

    assert found == (f"formulas.0.verification: Value error, a {verification['status']} record needs: {missing}",)


def test_a_verified_record_without_its_page_is_rejected() -> None:
    verified = {"status": "human-verified", "by": VERIFIER, "at": "2026-10-21", "portion": "P1", "value_digest": DIGEST}

    found = rejected(type_file(formulas=[formula(page=None, verification=verified)]))

    assert found == ("formulas.0: Value error, a human-verified record needs: page",)


def test_a_pending_record_needs_no_verifier_fields_and_no_page() -> None:
    parsed = InterimTypeFile.model_validate(type_file(formulas=[formula(page=None, verification=PENDING)]))

    assert parsed.formulas[0].verification == VerificationRecord(status="pending")


def test_a_manifest_names_document_edition_sunset_and_verifiers() -> None:
    parsed = InterimManifest.model_validate(manifest())

    assert (parsed.sunset.date.isoformat(), parsed.verifiers) == ("2099-12-31", (VERIFIER,))


def test_problems_of_a_root_error_name_the_root() -> None:
    with pytest.raises(ValidationError) as raised:
        InterimTypeFile.model_validate([])

    assert problems(raised.value)[0].startswith("<root>: ")

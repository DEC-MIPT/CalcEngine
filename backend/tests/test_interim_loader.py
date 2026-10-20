import logging
from pathlib import Path

import pytest
import yaml
from interim_fixture import VERIFIER, formula, manifest, table_value, type_file, write

from app.core.exceptions import ParameterValidationError
from app.parameters.interim_loader import load_interim_root

TYPE = "synthetic_type"
SECRET = 987.654321
"""Синтетическое значение-метка: если оно попадёт в лог или ошибку, тест это увидит."""

DIGEST = "0" * 64


def document(root: Path, name: str = "doc", **files: object) -> Path:
    write(root / name / "manifest.yaml", manifest())
    for calculation_type, data in files.items():
        write(root / name / f"{calculation_type}.yaml", data)
    return root / name


def messages(caplog: pytest.LogCaptureFixture) -> list[str]:
    return [record.getMessage() for record in caplog.records if record.name == "app.parameters.interim_loader"]


def test_a_document_with_its_manifest_and_type_files_is_loaded(tmp_path: Path) -> None:
    document(tmp_path, synthetic_type=type_file(formulas=[formula()]), other=type_file())

    (loaded,) = load_interim_root(tmp_path, {TYPE, "other"})

    assert loaded.name == "doc"
    assert loaded.manifest.verifiers == (VERIFIER,)
    assert [(found.path, found.calculation_type) for found in loaded.files] == [
        ("doc/other.yaml", "other"),
        ("doc/synthetic_type.yaml", TYPE),
    ]


def test_documents_are_read_in_the_order_of_their_directories(tmp_path: Path) -> None:
    document(tmp_path, "b", second=type_file())
    document(tmp_path, "a", first=type_file())

    assert [found.name for found in load_interim_root(tmp_path, {"first", "second"})] == ["a", "b"]


def test_a_file_of_an_unregistered_type_is_validated_kept_and_named_once(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    document(tmp_path, future_type=type_file(table_values=[table_value(value=SECRET)]))

    with caplog.at_level(logging.WARNING):
        (loaded,) = load_interim_root(tmp_path, {TYPE})

    assert [found.calculation_type for found in loaded.files] == ["future_type"]
    assert messages(caplog) == ["code=interim_type_unregistered file=doc/future_type.yaml"]


def test_an_invalid_file_of_an_unregistered_type_still_stops_the_start(tmp_path: Path) -> None:
    document(tmp_path, future_type=type_file(notes=[]))

    with pytest.raises(ParameterValidationError, match=r"^doc/future_type\.yaml: notes: "):
        load_interim_root(tmp_path, {TYPE})


def test_a_link_to_a_file_outside_the_root_is_not_read(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    root = tmp_path / "root"
    outside = write(tmp_path / "outside" / "synthetic_type.yaml", type_file(notes=[]))
    document(root)
    (root / "doc" / "synthetic_type.yaml").symlink_to(outside)

    with caplog.at_level(logging.WARNING):
        (loaded,) = load_interim_root(root, {TYPE})

    assert loaded.files == ()
    assert messages(caplog) == ["code=interim_file_skipped file=doc/synthetic_type.yaml reason=link_outside_root"]


def test_a_document_directory_linked_from_outside_is_not_read(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    root = tmp_path / "root"
    root.mkdir()
    (root / "doc").symlink_to(document(tmp_path / "outside"), target_is_directory=True)

    with caplog.at_level(logging.WARNING):
        assert load_interim_root(root, {TYPE}) == ()

    assert messages(caplog) == ["code=interim_file_skipped file=doc reason=link_outside_root"]


@pytest.mark.parametrize("name", ["README.md", "synthetic_type.yml", "nested"])
def test_a_file_that_is_not_a_manifest_or_a_type_file_is_not_read(
    tmp_path: Path, caplog: pytest.LogCaptureFixture, name: str
) -> None:
    directory = document(tmp_path)
    if name == "nested":
        write(directory / name / f"{TYPE}.yaml", type_file())
    else:
        (directory / name).write_text("<NOT-DATA>", encoding="utf-8")

    with caplog.at_level(logging.WARNING):
        (loaded,) = load_interim_root(tmp_path, {TYPE})

    assert loaded.files == ()
    assert messages(caplog) == [f"code=interim_file_skipped file=doc/{name} reason=not_a_data_file"]


def test_a_file_directly_under_the_root_is_not_read(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    write(tmp_path / f"{TYPE}.yaml", type_file())

    with caplog.at_level(logging.WARNING):
        assert load_interim_root(tmp_path, {TYPE}) == ()

    assert messages(caplog) == [f"code=interim_file_skipped file={TYPE}.yaml reason=not_a_document_directory"]


def test_a_link_inside_the_root_is_read(tmp_path: Path) -> None:
    directory = document(tmp_path)
    source = write(tmp_path / "shared" / "data.yaml", type_file())
    (directory / f"{TYPE}.yaml").symlink_to(source)
    write(tmp_path / "shared" / "manifest.yaml", manifest())

    loaded = {found.name: found for found in load_interim_root(tmp_path, {TYPE, "data"})}

    assert [found.calculation_type for found in loaded["doc"].files] == [TYPE]


def test_a_missing_root_stops_the_start(tmp_path: Path) -> None:
    with pytest.raises(ParameterValidationError, match="is not a directory"):
        load_interim_root(tmp_path / "missing", {TYPE})


def test_a_document_without_its_manifest_stops_the_start(tmp_path: Path) -> None:
    write(tmp_path / "doc" / f"{TYPE}.yaml", type_file())

    with pytest.raises(ParameterValidationError, match=r"^doc: no manifest\.yaml$"):
        load_interim_root(tmp_path, {TYPE})


def test_a_file_that_is_not_yaml_names_its_line_and_not_its_text(tmp_path: Path) -> None:
    directory = document(tmp_path)
    (directory / f"{TYPE}.yaml").write_text(f"formulas: [\n  {SECRET}: [", encoding="utf-8")

    with pytest.raises(ParameterValidationError) as raised:
        load_interim_root(tmp_path, {TYPE})

    assert str(raised.value).startswith(f"doc/{TYPE}.yaml: not valid YAML at line ")
    assert str(SECRET) not in str(raised.value)


def test_a_yaml_error_without_a_position_is_reported_without_one(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    document(tmp_path)

    def broken(_: str) -> object:
        raise yaml.YAMLError("<NO-MARK>")

    monkeypatch.setattr(yaml, "safe_load", broken)

    with pytest.raises(ParameterValidationError, match=r"^doc/manifest\.yaml: not valid YAML$"):
        load_interim_root(tmp_path, {TYPE})


def test_a_schema_error_names_the_file_and_the_path_and_no_value(tmp_path: Path) -> None:
    document(tmp_path, synthetic_type=type_file(table_values=[table_value(value=SECRET, unit="1", extra_field=SECRET)]))

    with pytest.raises(ParameterValidationError) as raised:
        load_interim_root(tmp_path, {TYPE})

    assert str(raised.value) == f"doc/{TYPE}.yaml: table_values.0.extra_field: Extra inputs are not permitted"


def test_an_invalid_manifest_names_the_manifest(tmp_path: Path) -> None:
    write(tmp_path / "doc" / "manifest.yaml", manifest(sunset={"date": "2099-12-31"}))

    with pytest.raises(ParameterValidationError, match=r"^doc/manifest\.yaml: sunset\.event: Field required$"):
        load_interim_root(tmp_path, {TYPE})


@pytest.mark.parametrize(
    "verification",
    [
        {"status": "human-verified", "by": "<SOMEONE-ELSE>", "at": "2026-10-21", "portion": "P1", "value_digest": DIGEST},
        {"status": "rejected", "by": "<SOMEONE-ELSE>", "at": "2026-10-21", "comment": "<REASON>"},
    ],
    ids=["human-verified", "rejected"],
)
def test_a_checked_record_by_someone_not_listed_stops_the_start(tmp_path: Path, verification: dict[str, object]) -> None:
    document(tmp_path, synthetic_type=type_file(formulas=[formula(), formula(verification=verification)]))

    with pytest.raises(ParameterValidationError) as raised:
        load_interim_root(tmp_path, {TYPE})

    assert str(raised.value) == f"doc/{TYPE}.yaml: formulas[1].verification.by: not a listed verifier"


def test_a_pending_record_may_name_anyone(tmp_path: Path) -> None:
    document(tmp_path, synthetic_type=type_file(formulas=[formula(verification={"status": "pending", "by": "<SOMEONE>"})]))

    (loaded,) = load_interim_root(tmp_path, {TYPE})

    assert loaded.files[0].content.formulas[0].verification.by == "<SOMEONE>"


def test_one_type_in_two_documents_stops_the_start(tmp_path: Path) -> None:
    document(tmp_path, "a", synthetic_type=type_file())
    document(tmp_path, "b", synthetic_type=type_file())

    with pytest.raises(ParameterValidationError, match=r"^b/synthetic_type\.yaml: the type also has data in a/synthetic_type\.yaml$"):
        load_interim_root(tmp_path, {TYPE})


def test_no_log_line_holds_a_data_value(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    directory = document(tmp_path, future_type=type_file(table_values=[table_value(value=SECRET)]))
    (directory / "notes.txt").write_text(str(SECRET), encoding="utf-8")

    with caplog.at_level(logging.DEBUG):
        load_interim_root(tmp_path, {TYPE})

    assert messages(caplog)
    assert not any(str(SECRET) in message for message in messages(caplog))

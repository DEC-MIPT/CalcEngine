"""Unit tests for the normatives-pipeline collector package.

All HTTP calls are mocked; no real network access required.
"""
from __future__ import annotations

import hashlib
import importlib
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from normatives_pipeline.collector.models import Document
from normatives_pipeline.collector.repositories.faufcc import FaufccRepository
from normatives_pipeline.collector.repositories.fgiscs import FgiscsRepository
from normatives_pipeline.collector.repositories.pravo import PravoRepository
from normatives_pipeline.collector.services import CollectService
from normatives_pipeline.collector.storage import FileStorage

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _source(base_url: str = "https://example.com", **params: str):
    return SimpleNamespace(base_url=base_url, params=params)


# ---------------------------------------------------------------------------
# Document model
# ---------------------------------------------------------------------------


def test_document_immutable() -> None:
    doc = Document(source="faufcc", designation="СП 22", title="Основания")
    with pytest.raises(AttributeError):
        doc.designation = "other"  # type: ignore[misc]


def test_document_edition_default_none() -> None:
    doc = Document(source="faufcc", designation="СП 22", title="Основания")
    assert doc.edition is None


def test_document_edition_set() -> None:
    doc = Document(source="faufcc", designation="СП 22", title="Основания", edition="2016")
    assert doc.edition == "2016"


def test_document_equality_by_value() -> None:
    a = Document(source="faufcc", designation="СП 22", title="Основания")
    b = Document(source="faufcc", designation="СП 22", title="Основания")
    assert a == b


# ---------------------------------------------------------------------------
# FileStorage
# ---------------------------------------------------------------------------


def test_storage_save_creates_file(tmp_path: Path) -> None:
    storage = FileStorage(tmp_path)
    content = b"hello pdf"
    path, sha256, is_new = storage.save("doc.pdf", content)
    assert path.exists()
    assert path.read_bytes() == content
    assert sha256 == hashlib.sha256(content).hexdigest()
    assert is_new is True


def test_storage_dedup_returns_existing(tmp_path: Path) -> None:
    storage = FileStorage(tmp_path)
    content = b"duplicate content"
    path1, sha1, new1 = storage.save("first.pdf", content)
    path2, sha2, new2 = storage.save("second.pdf", content)
    assert new1 is True
    assert new2 is False
    assert sha1 == sha2
    assert path1 == path2


def test_storage_different_content_creates_new_file(tmp_path: Path) -> None:
    storage = FileStorage(tmp_path)
    _, _, new1 = storage.save("a.pdf", b"content A")
    _, _, new2 = storage.save("b.pdf", b"content B")
    assert new1 is True
    assert new2 is True
    assert len(list(tmp_path.iterdir())) == 2


def test_storage_safe_name_strips_illegal_chars() -> None:
    assert FileStorage._safe_name("СП 22:13330/2016.pdf") == "СП 22_13330_2016.pdf"


def test_storage_safe_name_empty_fallback() -> None:
    assert FileStorage._safe_name("") == "unnamed"
    assert FileStorage._safe_name("///") == "_"  # slashes collapse to single underscore


# ---------------------------------------------------------------------------
# FaufccRepository
# ---------------------------------------------------------------------------

_FAUFCC_ENTRY = {
    "number": "СП 22.13330.2016",
    "name": "Основания зданий и сооружений",
    "year": "2016",
    "state": {"title": "Действует"},
    "asset": {"data": {"links": {"download": "https://cdn.faufcc.ru/sp22.pdf"}}},
}


def test_faufcc_search_returns_documents() -> None:
    src = _source("https://api.faufcc.ru", sp_registry_id="SP")
    repo = FaufccRepository(src, "TestAgent/1.0")
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": [_FAUFCC_ENTRY]}
    mock_resp.raise_for_status.return_value = None
    with patch("requests.get", return_value=mock_resp) as mock_get:
        docs = repo.search("22.13330")
    mock_get.assert_called_once()
    assert len(docs) == 1
    assert docs[0].designation == "СП 22.13330.2016"
    assert docs[0].edition == "2016"
    assert docs[0].download_url == "https://cdn.faufcc.ru/sp22.pdf"
    assert docs[0].state == "Действует"


def test_faufcc_search_empty_result() -> None:
    src = _source("https://api.faufcc.ru", sp_registry_id="SP")
    repo = FaufccRepository(src, "TestAgent/1.0")
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": []}
    mock_resp.raise_for_status.return_value = None
    with patch("requests.get", return_value=mock_resp):
        docs = repo.search("99.99999")
    assert docs == []


def test_faufcc_download_returns_bytes() -> None:
    src = _source("https://api.faufcc.ru", sp_registry_id="SP")
    repo = FaufccRepository(src, "TestAgent/1.0")
    doc = Document(
        source="faufcc", designation="СП 22", title="",
        download_url="https://cdn.faufcc.ru/sp22.pdf",
    )
    mock_resp = MagicMock()
    mock_resp.content = b"%PDF-1.4"
    mock_resp.raise_for_status.return_value = None
    with patch("requests.get", return_value=mock_resp):
        result = repo.download(doc)
    assert result == b"%PDF-1.4"


def test_faufcc_download_raises_when_no_url() -> None:
    src = _source("https://api.faufcc.ru", sp_registry_id="SP")
    repo = FaufccRepository(src, "TestAgent/1.0")
    doc = Document(source="faufcc", designation="СП 22", title="", download_url=None)
    with pytest.raises(ValueError, match="нет файла"):
        repo.download(doc)


def test_faufcc_to_document_no_year() -> None:
    entry: dict = {
        "number": "СП 22.13330",
        "name": "Title",
        "year": None,
        "state": None,
        "asset": {},
    }
    doc = FaufccRepository._to_document(entry)
    assert doc.edition is None


# ---------------------------------------------------------------------------
# PravoRepository
# ---------------------------------------------------------------------------

_PRAVO_ITEM = {
    "eoNumber": "ABC123",
    "number": "СП 22.13330.2016",
    "name": "Основания зданий",
}


def test_pravo_search_returns_documents() -> None:
    src = _source("https://pravo.gov.ru", minstroy_id="1234")
    repo = PravoRepository(src, "TestAgent/1.0")
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"items": [_PRAVO_ITEM]}
    mock_resp.raise_for_status.return_value = None
    with patch("requests.get", return_value=mock_resp):
        docs = repo.search(authority_id="1234")
    assert len(docs) == 1
    assert docs[0].designation == "СП 22.13330.2016"
    assert "ABC123" in docs[0].download_url  # type: ignore[operator]


def test_pravo_search_empty() -> None:
    src = _source("https://pravo.gov.ru", minstroy_id="1234")
    repo = PravoRepository(src, "TestAgent/1.0")
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"items": []}
    mock_resp.raise_for_status.return_value = None
    with patch("requests.get", return_value=mock_resp):
        docs = repo.search()
    assert docs == []


def test_pravo_search_with_name_filter() -> None:
    src = _source("https://pravo.gov.ru", minstroy_id="1234")
    repo = PravoRepository(src, "TestAgent/1.0")
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"items": [_PRAVO_ITEM]}
    mock_resp.raise_for_status.return_value = None
    with patch("requests.get", return_value=mock_resp) as mock_get:
        docs = repo.search(name="Основания")
    passed_params = mock_get.call_args.kwargs["params"]
    assert "Name" in passed_params
    assert len(docs) == 1


def test_pravo_download_returns_bytes() -> None:
    src = _source("https://pravo.gov.ru", minstroy_id="1234")
    repo = PravoRepository(src, "TestAgent/1.0")
    doc = Document(
        source="pravo", designation="X", title="",
        download_url="https://pravo.gov.ru/file/pdf?eoNumber=ABC",
    )
    mock_resp = MagicMock()
    mock_resp.content = b"%PDF-1.4"
    mock_resp.raise_for_status.return_value = None
    with patch("requests.get", return_value=mock_resp):
        result = repo.download(doc)
    assert result == b"%PDF-1.4"


def test_pravo_download_raises_when_no_url() -> None:
    src = _source("https://pravo.gov.ru", minstroy_id="1234")
    repo = PravoRepository(src, "TestAgent/1.0")
    doc = Document(source="pravo", designation="X", title="", download_url=None)
    with pytest.raises(ValueError):
        repo.download(doc)


# ---------------------------------------------------------------------------
# CollectService
# ---------------------------------------------------------------------------


def _make_repo(content: bytes = b"pdf") -> MagicMock:
    repo = MagicMock()
    repo.download.return_value = content
    return repo


def test_collect_saves_document(tmp_path: Path) -> None:
    storage = FileStorage(tmp_path)
    service = CollectService(storage)
    doc = Document(source="faufcc", designation="СП 22", title="")
    repo = _make_repo(b"%PDF-1.4")
    service.collect(repo, [doc])
    assert any(tmp_path.iterdir())


def test_collect_deduplicates(tmp_path: Path) -> None:
    storage = FileStorage(tmp_path)
    service = CollectService(storage)
    doc = Document(source="faufcc", designation="СП 22", title="")
    repo = _make_repo(b"same content")
    service.collect(repo, [doc, doc])
    assert len(list(tmp_path.iterdir())) == 1


def test_collect_skips_on_value_error(tmp_path: Path) -> None:
    storage = FileStorage(tmp_path)
    service = CollectService(storage)
    doc = Document(source="faufcc", designation="СП 22", title="", download_url=None)
    repo = MagicMock()
    repo.download.side_effect = ValueError("нет файла")
    service.collect(repo, [doc])
    assert list(tmp_path.iterdir()) == []


def test_collect_retries_on_network_error(tmp_path: Path) -> None:
    storage = FileStorage(tmp_path)
    service = CollectService(storage)
    doc = Document(source="faufcc", designation="СП 22", title="")
    repo = MagicMock()
    repo.download.side_effect = [OSError("timeout"), OSError("timeout"), b"ok"]
    with patch("time.sleep"):
        service.collect(repo, [doc])


def test_collect_gives_up_after_retries(tmp_path: Path) -> None:
    storage = FileStorage(tmp_path)
    service = CollectService(storage)
    doc = Document(source="faufcc", designation="СП 22", title="")
    repo = MagicMock()
    repo.download.side_effect = OSError("always fails")
    with patch("time.sleep"):
        service.collect(repo, [doc])
    assert list(tmp_path.iterdir()) == []


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_main_source_all(tmp_path: Path) -> None:
    from normatives_pipeline.collector import cli

    settings = SimpleNamespace(
        output_dir=tmp_path,
        user_agent="Test/1.0",
        sources={
            "faufcc": _source("https://api.faufcc.ru", sp_registry_id="SP"),
            "pravo": _source("https://pravo.gov.ru", minstroy_id="999"),
        },
    )
    with patch.object(cli, "FaufccRepository") as MockFaufcc, \
         patch.object(cli, "PravoRepository") as MockPravo, \
         patch.object(cli, "CollectService"), \
         patch.object(cli, "FileStorage"), \
         patch("normatives_pipeline.collector.cli.Settings") as MockSettings:
        MockSettings.load.return_value = settings
        MockFaufcc.return_value.search.return_value = []
        MockPravo.return_value.search.return_value = []
        cli.main([])
    MockSettings.load.assert_called_once()


def test_cli_main_source_faufcc_only(tmp_path: Path) -> None:
    from normatives_pipeline.collector import cli

    settings = SimpleNamespace(
        output_dir=tmp_path,
        user_agent="Test/1.0",
        sources={"faufcc": _source("https://api.faufcc.ru", sp_registry_id="SP")},
    )
    with patch.object(cli, "FaufccRepository") as MockFaufcc, \
         patch.object(cli, "PravoRepository") as MockPravo, \
         patch.object(cli, "CollectService"), \
         patch.object(cli, "FileStorage"), \
         patch("normatives_pipeline.collector.cli.Settings") as MockSettings:
        MockSettings.load.return_value = settings
        MockFaufcc.return_value.search.return_value = []
        cli.main(["--source", "faufcc"])
    MockPravo.assert_not_called()


def test_cli_main_source_pravo_only(tmp_path: Path) -> None:
    from normatives_pipeline.collector import cli

    settings = SimpleNamespace(
        output_dir=tmp_path,
        user_agent="Test/1.0",
        sources={
            "faufcc": _source("https://api.faufcc.ru", sp_registry_id="SP"),
            "pravo": _source("https://pravo.gov.ru", minstroy_id="999"),
        },
    )
    with patch.object(cli, "FaufccRepository") as MockFaufcc, \
         patch.object(cli, "PravoRepository") as MockPravo, \
         patch.object(cli, "CollectService"), \
         patch.object(cli, "FileStorage"), \
         patch("normatives_pipeline.collector.cli.Settings") as MockSettings:
        MockSettings.load.return_value = settings
        MockPravo.return_value.search.return_value = []
        cli.main(["--source", "pravo"])
    MockFaufcc.assert_not_called()
    MockPravo.assert_called_once()


def test_cli_main_collects_when_documents_found(tmp_path: Path) -> None:
    from normatives_pipeline.collector import cli

    settings = SimpleNamespace(
        output_dir=tmp_path,
        user_agent="Test/1.0",
        sources={"faufcc": _source("https://api.faufcc.ru", sp_registry_id="SP")},
    )
    found_doc = Document(source="faufcc", designation="СП 22.13330.2016", title="Основания")
    with patch.object(cli, "FaufccRepository") as MockFaufcc, \
         patch.object(cli, "CollectService") as MockService, \
         patch.object(cli, "FileStorage"), \
         patch("normatives_pipeline.collector.cli.Settings") as MockSettings:
        MockSettings.load.return_value = settings
        MockFaufcc.return_value.search.return_value = [found_doc]
        cli.main(["--source", "faufcc"])
    MockService.return_value.collect.assert_called()


def test_cli_main_document_filter(tmp_path: Path) -> None:
    from normatives_pipeline.collector import cli

    settings = SimpleNamespace(
        output_dir=tmp_path,
        user_agent="Test/1.0",
        sources={"faufcc": _source("https://api.faufcc.ru", sp_registry_id="SP")},
    )
    with patch.object(cli, "FaufccRepository") as MockFaufcc, \
         patch.object(cli, "CollectService"), \
         patch.object(cli, "FileStorage"), \
         patch("normatives_pipeline.collector.cli.Settings") as MockSettings:
        MockSettings.load.return_value = settings
        MockFaufcc.return_value.search.return_value = []
        cli.main(["--source", "faufcc", "--document", "22.13330"])
    call_args = MockFaufcc.return_value.search.call_args_list
    assert any("22.13330" in str(c) for c in call_args)
    assert not any("24.13330" in str(c) for c in call_args)


# ---------------------------------------------------------------------------
# FgiscsRepository
# ---------------------------------------------------------------------------

_FGISCS_ITEM = {
    "id": 42,
    "datasetName": "Нормативы СП",
    "identificationNumber": "SP001",
}


def test_main_module_importable() -> None:
    importlib.import_module("normatives_pipeline.collector.__main__")


def test_fgiscs_list_datasets_returns_documents() -> None:
    src = _source("https://fgiscs.minstroyrf.ru", referer="https://fgiscs.minstroyrf.ru/open-data")
    repo = FgiscsRepository(src, "TestAgent/1.0")
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"items": [_FGISCS_ITEM]}
    mock_resp.raise_for_status.return_value = None
    with patch("requests.get", return_value=mock_resp):
        docs = repo.list_datasets()
    assert len(docs) == 1
    assert docs[0].source == "fgiscs"
    assert docs[0].designation == "Нормативы СП"
    assert docs[0].extra["id"] == "42"


def test_fgiscs_download_returns_bytes() -> None:
    src = _source("https://fgiscs.minstroyrf.ru", referer="https://fgiscs.minstroyrf.ru")
    repo = FgiscsRepository(src, "TestAgent/1.0")
    doc = Document(source="fgiscs", designation="Нормативы", title="SP001", extra={"id": "42"})

    detail_resp = MagicMock()
    detail_resp.json.return_value = {"datasetFile": {"path": "data/sp.json"}}
    detail_resp.raise_for_status.return_value = None

    file_resp = MagicMock()
    file_resp.content = b'[{"data": 1}]'
    file_resp.raise_for_status.return_value = None

    with patch("requests.get", side_effect=[detail_resp, file_resp]):
        result = repo.download(doc)
    assert result == b'[{"data": 1}]'


def test_fgiscs_download_raises_when_no_id() -> None:
    src = _source("https://fgiscs.minstroyrf.ru", referer="https://fgiscs.minstroyrf.ru")
    repo = FgiscsRepository(src, "TestAgent/1.0")
    doc = Document(source="fgiscs", designation="X", title="", extra={})
    with pytest.raises(ValueError, match="нет идентификатора"):
        repo.download(doc)


def test_fgiscs_download_raises_when_no_path() -> None:
    src = _source("https://fgiscs.minstroyrf.ru", referer="https://fgiscs.minstroyrf.ru")
    repo = FgiscsRepository(src, "TestAgent/1.0")
    doc = Document(source="fgiscs", designation="X", title="", extra={"id": "99"})
    detail_resp = MagicMock()
    detail_resp.json.return_value = {"datasetFile": None}
    detail_resp.raise_for_status.return_value = None
    with patch("requests.get", return_value=detail_resp), pytest.raises(ValueError, match="нет файла"):
        repo.download(doc)

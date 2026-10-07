"""Общие фикстуры: хелпер для тестовой БД (DEC_TEST_NORMATIVES_DATABASE_URL)."""

from __future__ import annotations

import os
from collections.abc import Generator

import pytest


def require_test_db_url() -> str:
    """Возвращает DEC_TEST_NORMATIVES_DATABASE_URL; пропускает модуль если не задан."""
    url = os.environ.get("DEC_TEST_NORMATIVES_DATABASE_URL")
    if url is None:
        pytest.skip("DEC_TEST_NORMATIVES_DATABASE_URL не задан", allow_module_level=True)
    dbname = url.rstrip("/").split("/")[-1].split("?")[0]
    if not dbname.endswith("_test"):
        pytest.fail(
            f"DEC_TEST_NORMATIVES_DATABASE_URL должен указывать на базу с суффиксом _test, получено: {dbname!r}"
        )
    return url


@pytest.fixture(scope="session", autouse=True)
def _sync_ingest_url() -> Generator[None, None, None]:
    """Forward DEC_TEST_NORMATIVES_DATABASE_URL into DEC_DATABASE_URL when not set.

    ingest() reads DEC_DATABASE_URL internally; tests connect via require_test_db_url()
    (DEC_TEST_NORMATIVES_DATABASE_URL). Without this, ingest() writes to a different
    database than the one the test fixtures query.
    """
    test_url = os.environ.get("DEC_TEST_NORMATIVES_DATABASE_URL")
    already_set = "DEC_DATABASE_URL" in os.environ
    if test_url and not already_set:
        os.environ["DEC_DATABASE_URL"] = test_url
    yield
    if test_url and not already_set:
        del os.environ["DEC_DATABASE_URL"]

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
    """Always point DEC_DATABASE_URL at the test database for the duration of the suite.

    ingest() reads DEC_DATABASE_URL internally. Without overwriting it unconditionally,
    a machine where DEC_DATABASE_URL points at the working 'dec' would let tests write
    into the production database even when DEC_TEST_NORMATIVES_DATABASE_URL is set.
    """
    test_url = os.environ.get("DEC_TEST_NORMATIVES_DATABASE_URL")
    previous = os.environ.get("DEC_DATABASE_URL")
    if test_url:
        os.environ["DEC_DATABASE_URL"] = test_url
    yield
    if test_url:
        if previous is None:
            del os.environ["DEC_DATABASE_URL"]
        else:
            os.environ["DEC_DATABASE_URL"] = previous

import importlib
import logging

import pytest

import app.core.logging as core_logging
from app.core.logging import logger


def test_reimport_does_not_duplicate_the_handler() -> None:
    handlers_before = len(logger.handlers)

    importlib.reload(core_logging)

    assert len(logging.getLogger("app").handlers) == handlers_before


def test_logger_emits_a_line(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="app"):
        logger.info("hello from core.logging")

    assert "hello from core.logging" in caplog.text

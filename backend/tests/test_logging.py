import logging

import pytest

from app.core.logging import logger


def test_logger_emits_a_line(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="app"):
        logger.info("hello from core.logging")

    assert "hello from core.logging" in caplog.text

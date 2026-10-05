"""Настройка окружения тестов: явный URL локальной dev-базы."""

from __future__ import annotations

import os

os.environ.setdefault(
    "DEC_DATABASE_URL", "postgresql://dec:dec@localhost:5433/dec"  # pragma: allowlist secret
)

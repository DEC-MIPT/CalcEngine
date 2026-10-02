"""Слой models: доменные типы коллектора."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Document:
    source: str
    designation: str
    title: str
    download_url: str | None = None
    state: str | None = None
    extra: dict[str, str] = field(default_factory=dict)

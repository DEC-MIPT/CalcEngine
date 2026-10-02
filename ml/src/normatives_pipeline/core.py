"""Слой core: загрузка конфигурации источников из TOML-файла."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from .config import CONFIG_DIR

DEFAULT_CONFIG = CONFIG_DIR / "sources.toml"


@dataclass(frozen=True)
class SourceConfig:
    enabled: bool
    base_url: str
    params: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Settings:
    output_dir: Path
    user_agent: str
    sources: dict[str, SourceConfig]

    @classmethod
    def load(cls, path: Path = DEFAULT_CONFIG) -> "Settings":
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        sources: dict[str, SourceConfig] = {}
        for name, raw in data.get("sources", {}).items():
            sources[name] = SourceConfig(
                enabled=bool(raw.get("enabled", True)),
                base_url=str(raw["base_url"]),
                params={
                    key: str(value)
                    for key, value in raw.items()
                    if key not in ("enabled", "base_url")
                },
            )
        return cls(
            output_dir=Path(str(data.get("output_dir", "norm-base"))),
            user_agent=str(data.get("user_agent", "")),
            sources=sources,
        )

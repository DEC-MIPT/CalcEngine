"""Загрузка конфигурации пайплайна (TOML) — без хардкода в коде."""

from __future__ import annotations

import tomllib
from functools import lru_cache
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parents[2] / "configs"
PARSER_TOML = CONFIG_DIR / "parser.toml"
FORMULAS_TOML = CONFIG_DIR / "formulas.toml"


@lru_cache(maxsize=1)
def parser_config() -> dict:
    with PARSER_TOML.open("rb") as fh:
        return tomllib.load(fh)["parser"]


@lru_cache(maxsize=1)
def output_config() -> dict:
    with PARSER_TOML.open("rb") as fh:
        return tomllib.load(fh)["output"]


@lru_cache(maxsize=1)
def search_config() -> dict:
    with PARSER_TOML.open("rb") as fh:
        return tomllib.load(fh)["search"]


@lru_cache(maxsize=1)
def detect_config() -> dict:
    with PARSER_TOML.open("rb") as fh:
        return tomllib.load(fh)["detect"]


@lru_cache(maxsize=1)
def formula_manifest() -> list[dict]:
    with FORMULAS_TOML.open("rb") as fh:
        return tomllib.load(fh).get("formula", [])

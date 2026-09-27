"""Загрузка конфигурации пайплайна (TOML) — без хардкода в коде."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import tomllib

PARSER_TOML = Path(__file__).parent / "parser.toml"
FORMULAS_TOML = Path(__file__).parent / "formulas.toml"
OCR_TOML = Path(__file__).parent / "ocr.toml"


@lru_cache(maxsize=1)
def parser_config() -> dict:
    with PARSER_TOML.open("rb") as fh:
        return tomllib.load(fh)["parser"]


@lru_cache(maxsize=1)
def output_config() -> dict:
    with PARSER_TOML.open("rb") as fh:
        return tomllib.load(fh)["output"]


@lru_cache(maxsize=1)
def formula_manifest() -> list[dict]:
    with FORMULAS_TOML.open("rb") as fh:
        return tomllib.load(fh).get("formula", [])


@lru_cache(maxsize=1)
def ocr_config() -> dict:
    with OCR_TOML.open("rb") as fh:
        return tomllib.load(fh)

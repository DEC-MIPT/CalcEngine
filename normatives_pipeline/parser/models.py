"""Слой models: доменные типы парсера."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Clause:
    number: str
    text: str
    page: int


@dataclass(frozen=True)
class NotationEntry:
    symbol: str
    meaning: str
    unit: str = ""


@dataclass(frozen=True)
class Formula:
    number: str
    raw_text: str
    page: int
    latex: str = ""


@dataclass(frozen=True)
class Table:
    number: str
    rows: tuple[tuple[str, ...], ...]
    page: int


@dataclass(frozen=True)
class ParsedDocument:
    designation: str
    layer: str
    clauses: tuple[Clause, ...] = ()
    formulas: tuple[Formula, ...] = ()
    notation: tuple[NotationEntry, ...] = ()
    tables: tuple[Table, ...] = ()

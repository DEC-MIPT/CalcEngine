"""Слой models: доменные типы парсера."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NormRef:
    document: str
    edition: str
    clause: str
    status: str
    provenance: str


@dataclass(frozen=True)
class Clause:
    number: str
    text: str
    page: int
    line: int


@dataclass(frozen=True)
class NotationEntry:
    symbol: str
    meaning: str
    unit: str = ""
    page: int = 0


@dataclass(frozen=True)
class Formula:
    number: str
    raw_text: str
    page: int
    line: int
    latex: str = ""
    clause: str = ""


@dataclass(frozen=True)
class CrossRef:
    clause: str
    ref_type: str
    value: str
    url: str = ""


@dataclass(frozen=True)
class Condition:
    clause: str
    text: str
    page: int
    line: int
    kind: str = "condition"


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

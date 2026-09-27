"""Baseline-извлечение: пункты, формулы, обозначения, таблицы."""

from __future__ import annotations

import re
from pathlib import Path

import pdfplumber

from .models import Clause, Formula, NotationEntry, Table

CLAUSE_RE = re.compile(r"^\s*(\d+(?:\.\d+){1,3})\s+([А-ЯЁA-Z].*)$")
FORMULA_NUM_RE = re.compile(r"\((\d+\.\d+)\)\s*$")
TABLE_REF_RE = re.compile(r"таблиц[еы]\s+(\d+(?:\.\d+)?)")


def extract_clauses(pages: list[str]) -> list[Clause]:
    out: list[Clause] = []
    for page_no, text in enumerate(pages, start=1):
        for line in text.splitlines():
            m = CLAUSE_RE.match(line)
            if m:
                out.append(Clause(number=m.group(1), text=m.group(2).strip(), page=page_no))
    return out


def extract_formulas(pages: list[str]) -> list[Formula]:
    out: list[Formula] = []
    for page_no, text in enumerate(pages, start=1):
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if FORMULA_NUM_RE.search(line):
                raw = " ".join(lines[max(0, idx - 4) : idx + 1])
                number = FORMULA_NUM_RE.search(line).group(1)  # type: ignore[union-attr]
                out.append(Formula(number=number, raw_text=raw.strip(), page=page_no))
    return out


def extract_notation(pages: list[str]) -> list[NotationEntry]:
    out: list[NotationEntry] = []
    entry_re = re.compile(r"^\s*([^–—]{1,40}?)\s*[–—]\s*(.+)$")
    for text in pages:
        for line in text.splitlines():
            m = entry_re.match(line)
            if not m:
                continue
            meaning = m.group(2).strip()
            if re.search(r"[а-яёА-ЯЁ]", meaning) and len(m.group(1)) < 40:
                out.append(NotationEntry(symbol=m.group(1).strip(), meaning=meaning))
    return out


def extract_tables(path: Path, max_pages: int | None = None) -> list[Table]:
    out: list[Table] = []
    with pdfplumber.open(path) as pdf:
        pages = pdf.pages if max_pages is None else pdf.pages[:max_pages]
        for page_no, page in enumerate(pages, start=1):
            for tbl in page.extract_tables():
                rows = tuple(
                    tuple("" if cell is None else str(cell).strip() for cell in row)
                    for row in tbl
                )
                if rows:
                    out.append(Table(number="", rows=rows, page=page_no))
    return out


def extract_table_refs(text: str) -> list[str]:
    return TABLE_REF_RE.findall(text)

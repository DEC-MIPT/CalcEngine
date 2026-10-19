"""Baseline-извлечение: пункты, формулы, обозначения, таблицы (паттерны из конфига)."""

from __future__ import annotations

import re
from pathlib import Path

import pdfplumber

from ..config import parser_config
from .models import Clause, Condition, CrossRef, Formula, NotationEntry, Table

_CFG = parser_config()

CLAUSE_RE = re.compile(_CFG["clause_re"])
FORMULA_NUM_RES = [re.compile(p) for p in _CFG["formula_num_res"]]
TABLE_REF_RE = re.compile(_CFG["table_ref_re"])
GOST_RE = re.compile(_CFG["gost_re"])
GDE_RE = re.compile(_CFG["gde_re"])
NOTATION_RE = re.compile(_CFG["notation_re"])
FORMULA_NOTATION_RE = re.compile(_CFG["formula_notation_re"])
FORMULA_MAX_LEN = int(_CFG["formula_max_len"])
FORMULA_LOOKBACK = int(_CFG["formula_lookback"])
NOTATION_SCAN_LINES = int(_CFG["notation_scan_lines"])
SYNTHETIC_ID_TEMPLATE = _CFG["synthetic_id_template"]
COND_CUES = tuple(p.strip().lower() for p in _CFG["condition_cues"] if p.strip())
COND_MAX_LEN = int(_CFG.get("condition_max_len", 400))


def _clauses_by_page(clauses: list[Clause]) -> dict[int, list[Clause]]:
    by_page: dict[int, list[Clause]] = {}
    for cl in clauses:
        by_page.setdefault(cl.page, []).append(cl)
    return by_page


def _formula_number_in(lines: list[str], start: int, end: int) -> str | None:
    for i in range(max(0, start), min(end, len(lines) - 1) + 1):
        for pat in FORMULA_NUM_RES:
            m = pat.search(lines[i])
            if m:
                return m.group(1)
    return None


def _collect_notation(
    lines: list[str], start: int, page: int
) -> tuple[list[NotationEntry], int]:
    entries: list[NotationEntry] = []
    i = start
    while i < len(lines):
        m = FORMULA_NOTATION_RE.match(lines[i])
        if m and re.search(r"[а-яёА-ЯЁ]", m.group(2)):
            entries.append(
                NotationEntry(
                    symbol=m.group(1).strip(),
                    meaning=m.group(2).strip().rstrip(";.,"),
                    page=page,
                )
            )
            i += 1
        elif entries:
            break
        else:
            i += 1
    return entries, i


def extract_clauses(pages: list[str]) -> list[Clause]:
    out: list[Clause] = []
    for page_no, text in enumerate(pages, start=1):
        for line_no, line in enumerate(text.splitlines()):
            m = CLAUSE_RE.match(line)
            if m:
                out.append(
                    Clause(number=m.group(1), text=m.group(2).strip(), page=page_no, line=line_no)
                )
    return out


def extract_formulas(pages: list[str]) -> list[Formula]:
    out: list[Formula] = []
    for page_no, text in enumerate(pages, start=1):
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            for pat in FORMULA_NUM_RES:
                m = pat.search(line)
                if m:
                    raw = " ".join(lines[max(0, idx - 4) : idx + 1])
                    out.append(
                        Formula(number=m.group(1), raw_text=raw.strip(), page=page_no, line=idx)
                    )
                    break
    return out


def extract_formula_notation(
    pages: list[str], formulas: list[Formula]
) -> dict[str, list[NotationEntry]]:
    out: dict[str, list[NotationEntry]] = {}
    for formula in formulas:
        lines = pages[formula.page - 1].splitlines()
        gde_idx: int | None = None
        stop = min(formula.line + NOTATION_SCAN_LINES, len(lines))
        for i in range(formula.line + 1, stop):
            if GDE_RE.match(lines[i]):
                gde_idx = i
                break
        if gde_idx is None:
            continue
        entries, _ = _collect_notation(lines, gde_idx, formula.page)
        if entries:
            out[formula.number] = entries
    return out


def extract_unnumbered_formulas(
    pages: list[str], clauses: list[Clause]
) -> tuple[list[Formula], dict[str, list[NotationEntry]]]:
    by_page = _clauses_by_page(clauses)
    formulas: list[Formula] = []
    notation: dict[str, list[NotationEntry]] = {}
    counters: dict[str, int] = {}

    for page_no, text in enumerate(pages, start=1):
        lines = text.splitlines()
        idx = 0
        while idx < len(lines):
            if not GDE_RE.match(lines[idx]):
                idx += 1
                continue
            j = idx - 1
            while j >= 0 and not lines[j].strip():
                j -= 1
            if j < 0 or CLAUSE_RE.match(lines[j]):
                idx += 1
                continue
            formula_line = lines[j].strip()
            if len(formula_line) > FORMULA_MAX_LEN:
                idx += 1
                continue
            if _formula_number_in(lines, j - FORMULA_LOOKBACK, j) is not None:
                idx += 1
                continue

            entries, next_idx = _collect_notation(lines, idx, page_no)
            if not entries:
                idx += 1
                continue

            page_clauses = by_page.get(page_no, [])
            preceding = [c for c in page_clauses if c.line <= j]
            clause_num = preceding[-1].number if preceding else ""
            counters[clause_num] = counters.get(clause_num, 0) + 1
            number = SYNTHETIC_ID_TEMPLATE.format(
                clause=clause_num, index=counters[clause_num]
            )

            raw = " ".join([formula_line] + [lines[i].strip() for i in range(idx, next_idx)])
            formulas.append(
                Formula(number=number, raw_text=raw, page=page_no, line=j, clause=clause_num)
            )
            notation[number] = entries
            idx = next_idx
    return formulas, notation


def associate_formulas_to_clauses(
    clauses: list[Clause], formulas: list[Formula]
) -> list[Formula]:
    by_page = _clauses_by_page(clauses)
    out: list[Formula] = []
    for formula in formulas:
        page_clauses = by_page.get(formula.page, [])
        preceding = [c for c in page_clauses if c.line <= formula.line]
        clause_num = preceding[-1].number if preceding else ""
        out.append(
            Formula(
                number=formula.number,
                raw_text=formula.raw_text,
                page=formula.page,
                line=formula.line,
                latex=formula.latex,
                clause=clause_num,
            )
        )
    return out


def extract_notation(pages: list[str]) -> list[NotationEntry]:
    out: list[NotationEntry] = []
    for page_no, text in enumerate(pages, start=1):
        for line in text.splitlines():
            m = NOTATION_RE.match(line)
            if not m:
                continue
            meaning = m.group(2).strip()
            if re.search(r"[а-яёА-ЯЁ]", meaning) and len(m.group(1)) < 40:
                out.append(
                    NotationEntry(symbol=m.group(1).strip(), meaning=meaning, page=page_no)
                )
    return out


def extract_cross_refs(pages: list[str], clauses: list[Clause]) -> list[CrossRef]:
    by_page = _clauses_by_page(clauses)
    out: list[CrossRef] = []
    for page_no, text in enumerate(pages, start=1):
        lines = text.splitlines()
        for line_no, line in enumerate(lines):
            for m in GOST_RE.finditer(line):
                page_clauses = by_page.get(page_no, [])
                preceding = [c for c in page_clauses if c.line <= line_no]
                clause_num = preceding[-1].number if preceding else ""
                out.append(
                    CrossRef(clause=clause_num, ref_type="gost", value=m.group(0))
                )
    return out


def _caption_search(text: str) -> str:
    collapsed = re.sub(r"\s+", "", text)
    m = re.search(r"[Тт]аблиц[а-я]*(\d+(?:\.\d{1,2})?)", collapsed)
    return m.group(1) if m else ""


def _caption_line(text: str) -> str:
    for line in text.splitlines():
        collapsed = re.sub(r"\s+", "", line)
        m = re.match(r"^Таблица(\d+(?:\.\d{1,2})?)$", collapsed, re.IGNORECASE)
        if m:
            return m.group(1)
    return ""


def _table_caption(page, bbox: tuple, prev_page=None) -> str:
    top = bbox[1]
    if top <= 0:
        return ""
    crop = page.within_bbox((0, max(0, top - 60), page.width, top))
    number = _caption_search(crop.extract_text() or "")
    if number:
        return number
    if prev_page is not None:
        tail = prev_page.within_bbox(
            (0, max(0, prev_page.height - 200), prev_page.width, prev_page.height)
        )
        number = _caption_line(tail.extract_text() or "")
        if number:
            return number
    return ""


def extract_tables(path: Path, max_pages: int | None = None) -> list[Table]:
    out: list[Table] = []
    with pdfplumber.open(path) as pdf:
        pages = pdf.pages if max_pages is None else pdf.pages[:max_pages]
        prev_page = None
        for page_no, page in enumerate(pages, start=1):
            for tbl in page.find_tables():
                rows = tuple(
                    tuple("" if cell is None else str(cell).strip() for cell in row)
                    for row in tbl.extract()
                )
                if not rows:
                    continue
                number = _table_caption(page, tbl.bbox, prev_page)
                out.append(Table(number=number, rows=rows, page=page_no))
            prev_page = page

    resolved: list[Table] = []
    last_number = ""
    last_page: int | None = None
    for table in out:
        number = table.number
        if not number and last_number and (
            last_page is None or table.page - last_page <= 1
        ):
            number = last_number
        if number:
            last_number = number
            last_page = table.page
        resolved.append(Table(number=number, rows=table.rows, page=table.page))
    return resolved


def extract_table_refs(text: str) -> list[str]:
    return TABLE_REF_RE.findall(text)


def _cond_norm(text: str) -> str:
    return re.sub(r"[,\s]+", " ", text.lower()).strip()


def extract_conditions(pages: list[str], clauses: list[Clause]) -> list[Condition]:
    """Условия применимости: строки с фразами-маркерами («при условии что», «при
    соблюдении», «соблюдены следующие условия» и т. п.). Детерминированно, без моделей."""
    by_page = _clauses_by_page(clauses)
    out: list[Condition] = []
    for page_no, text in enumerate(pages, start=1):
        page_clauses = by_page.get(page_no, [])
        for line_no, line in enumerate(text.splitlines()):
            stripped = line.strip()
            if not stripped or len(stripped) > COND_MAX_LEN:
                continue
            norm = _cond_norm(stripped)
            if not any(cue in norm for cue in COND_CUES):
                continue
            preceding = [c for c in page_clauses if c.line <= line_no]
            clause_num = preceding[-1].number if preceding else ""
            out.append(
                Condition(clause=clause_num, text=stripped, page=page_no, line=line_no)
            )
    return out

"""Классификатор текстового слоя и извлечение текста страниц."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

MIN_TEXT_CHARS = 500

DESIGNATION_RE = re.compile(r"\bСП\s*\d{2}\.\d{5}(?:\.\d+)?\b")
EDITION_YEAR_RE = re.compile(r"(?:^|[^0-9])((?:19|20)\d{2})(?:$|[^0-9])")
_CHANGES_RE = re.compile(r"с\s+Изменениями\s+N\s+([0-9][0-9,\s]*)", re.IGNORECASE)


def read_pages(path: Path) -> list[str]:
    result = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    return result.stdout.split("\f")


def extract_designation(pages: list[str]) -> str:
    for page in pages[:3]:
        m = DESIGNATION_RE.search(page)
        if m:
            return " ".join(m.group(0).split())
    return ""


def extract_edition_year(designation: str) -> str:
    years = [m.group(1) for m in EDITION_YEAR_RE.finditer(designation)]
    return years[-1] if years else ""


def extract_edition_text(pages: list[str], designation: str) -> str:
    """Return edition string with change numbers if the title page lists them."""
    year = extract_edition_year(designation)
    for page in pages[:3]:
        m = _CHANGES_RE.search(page)
        if m:
            changes = re.sub(r"\s+", " ", m.group(1)).strip().rstrip(",")
            return f"{year} с Изм. N {changes}"
    return year


def classify(pages: list[str]) -> str:
    total = sum(len(page) for page in pages)
    return "text" if total >= MIN_TEXT_CHARS else "scan"

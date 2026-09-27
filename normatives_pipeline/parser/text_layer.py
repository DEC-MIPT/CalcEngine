"""Классификатор текстового слоя и извлечение текста страниц."""

from __future__ import annotations

import subprocess
from pathlib import Path

MIN_TEXT_CHARS = 500


def read_pages(path: Path) -> list[str]:
    result = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    return result.stdout.split("\f")


def classify(pages: list[str]) -> str:
    total = sum(len(page) for page in pages)
    return "text" if total >= MIN_TEXT_CHARS else "scan"

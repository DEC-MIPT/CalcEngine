"""Зонный import-скан: пакет нормативного пайплайна не импортирует backend (`app`).

Продолжение WP6 (secrets/zones follow-up, ответ Акиму 2026-10-04): правило
`AGENTS.md` «код зон не пересекается» проверяется автоматически, без новых
зависимостей — разбором AST, а не запуском импортов.
"""

from __future__ import annotations

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
FORBIDDEN = "app"


def _imported_roots(tree: ast.AST) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def test_pipeline_src_does_not_import_backend() -> None:
    offenders: list[str] = []
    for path in sorted(SRC.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        if FORBIDDEN in _imported_roots(tree):
            offenders.append(str(path.relative_to(SRC)))
    assert not offenders, f"ml/src импортирует backend-пакет {FORBIDDEN!r}: {offenders}"

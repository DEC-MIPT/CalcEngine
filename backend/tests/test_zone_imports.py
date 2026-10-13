import ast
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
PIPELINE = "normatives_pipeline"


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
    return found | {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}


def test_no_backend_module_imports_the_pipeline() -> None:
    sources = [path for folder in ("app", "tests", "alembic") for path in (BACKEND / folder).rglob("*.py")]

    offending = [
        str(path.relative_to(BACKEND))
        for path in sources
        if any(name.split(".")[0] == PIPELINE for name in imported_modules(path))
    ]

    assert sources and offending == []

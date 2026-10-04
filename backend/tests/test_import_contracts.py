import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[1]
MISSING_TOOL = "lint-imports not found; install backend/requirements-dev.txt"


def lint_imports() -> str:
    """Путь к ``lint-imports``: рядом с интерпретатором тестов, иначе на ``PATH``.

    Returns:
        Путь к исполняемому файлу.
    """
    found = shutil.which("lint-imports", path=str(Path(sys.executable).parent)) or shutil.which("lint-imports")
    if found is None:
        pytest.fail(MISSING_TOOL)
    return found


def lint(tmp_path: Path, module: str | None = None, body: str = "") -> subprocess.CompletedProcess[str]:
    """Прогоняет контракты ``pyproject.toml`` на копии ``app`` с добавленным модулем.

    Args:
        tmp_path: временный каталог для копии.
        module: путь нового модуля внутри ``app`` (например ``engine/upward.py`` или
            ``newpkg/__init__.py`` для нового пакета).
        body: текст нового модуля.

    Returns:
        Завершённый процесс ``lint-imports``.
    """
    tool = lint_imports()
    shutil.copytree(BACKEND / "app", tmp_path / "app", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(BACKEND / "pyproject.toml", tmp_path / "pyproject.toml")
    if module is not None:
        target = tmp_path / "app" / module
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    return subprocess.run(
        [tool, "--no-cache"],
        cwd=tmp_path,
        env=os.environ | {"PYTHONPATH": str(tmp_path)},
        capture_output=True,
        text=True,
        check=False,
    )


def test_the_backend_keeps_every_contract(tmp_path: Path) -> None:
    completed = lint(tmp_path)

    assert completed.returncode == 0, completed.stdout
    assert "Contracts: 4 kept, 0 broken." in completed.stdout


@pytest.mark.parametrize(
    ("module", "body", "contract", "offending"),
    [
        (
            "repositories/upward.py",
            "from app.services import calculation\n",
            "Layers follow backend-layered-architecture design.md decision 2 BROKEN",
            "app.repositories.upward -> app.services.calculation",
        ),
        (
            "api/direct.py",
            "from app.repositories import calculation_result\n",
            "api and worker do not import repositories or models BROKEN",
            "app.api.direct -> app.repositories.calculation_result",
        ),
        (
            "engine/reads.py",
            "from app.parameters import loader\n",
            "engine imports from the application only schemas and core BROKEN",
            "app.engine.reads -> app.parameters.loader",
        ),
        (
            "core/pipeline.py",
            "import normatives_pipeline\n",
            "the backend does not import the normative pipeline BROKEN",
            "app.core.pipeline -> normatives_pipeline",
        ),
        (
            "newpkg/__init__.py",
            "",
            "Layers follow backend-layered-architecture design.md decision 2 BROKEN",
            "app.newpkg",
        ),
        (
            "loose.py",
            "",
            "Layers follow backend-layered-architecture design.md decision 2 BROKEN",
            "app.loose",
        ),
    ],
    ids=["upward", "api-repositories", "engine-parameters", "pipeline", "package-outside-layers", "module-outside-layers"],
)
def test_a_forbidden_import_or_an_unplaced_package_breaks_its_contract_and_is_named(
    tmp_path: Path, module: str, body: str, contract: str, offending: str
) -> None:
    completed = lint(tmp_path, module, body)

    assert completed.returncode == 1
    assert contract in completed.stdout
    assert offending in completed.stdout


def test_a_missing_lint_imports_fails_with_a_clear_message(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    monkeypatch.setattr(sys, "executable", str(tmp_path / "python"))
    monkeypatch.setenv("PATH", str(empty))

    with pytest.raises(pytest.fail.Exception, match="lint-imports not found; install backend/requirements-dev.txt"):
        lint_imports()

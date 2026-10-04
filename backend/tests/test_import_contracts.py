import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[1]
LINT_IMPORTS = Path(sys.executable).with_name("lint-imports")


def lint(tmp_path: Path, module: str | None = None, body: str = "") -> subprocess.CompletedProcess[str]:
    """Прогоняет контракты ``pyproject.toml`` на копии ``app`` с добавленным модулем.

    Args:
        tmp_path: временный каталог для копии.
        module: путь нового модуля внутри ``app`` (например ``engine/upward.py``).
        body: текст нового модуля.

    Returns:
        Завершённый процесс ``lint-imports``.
    """
    shutil.copytree(BACKEND / "app", tmp_path / "app", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(BACKEND / "pyproject.toml", tmp_path / "pyproject.toml")
    if module is not None:
        (tmp_path / "app" / module).write_text(body, encoding="utf-8")
    return subprocess.run(
        [str(LINT_IMPORTS), "--no-cache"],
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
    ],
    ids=["upward", "api-repositories", "engine-parameters", "pipeline"],
)
def test_a_forbidden_import_breaks_its_contract_and_is_named(
    tmp_path: Path, module: str, body: str, contract: str, offending: str
) -> None:
    completed = lint(tmp_path, module, body)

    assert completed.returncode == 1
    assert contract in completed.stdout
    assert offending in completed.stdout

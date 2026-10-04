import subprocess
import sys
from pathlib import Path

import pytest

from scripts.check_env_example import (
    CONFIG,
    TEMPLATE,
    main,
    missing,
    settings_variables,
    template_keys,
)

SETTINGS = '''
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    url: str = Field(validation_alias="DEC_URL")
    other: str = Field(alias="DEC_OTHER")
    plain: int = 1
    again: str = Field(validation_alias="DEC_URL")
    computed: str = Field(default="x")
    choice: str = Field(validation_alias=None)

    def method(self) -> None: ...


class Helper:
    ignored: str = Field(validation_alias="DEC_IGNORED")
'''


def write(folder: Path, config: str | None, template: str | None) -> tuple[Path, Path]:
    config_path, template_path = folder / "config.py", folder / ".env.example"
    if config is not None:
        config_path.write_text(config, encoding="utf-8")
    if template is not None:
        template_path.write_text(template, encoding="utf-8")
    return config_path, template_path


def test_the_variables_are_the_aliases_or_the_upper_field_names_of_settings_classes() -> None:
    assert settings_variables(SETTINGS) == ["DEC_URL", "DEC_OTHER", "PLAIN", "COMPUTED", "CHOICE"]


def test_active_and_commented_keys_are_listed() -> None:
    text = "# A comment\nDEC_A=postgresql://x\n#  DEC_B=http://localhost\n  DEC_C = 1\nnot a key\n# lower=1\n"

    assert template_keys(text) == {"DEC_A", "DEC_B", "DEC_C"}


def test_a_variable_missing_from_the_template_fails_with_its_name(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    config, template = write(tmp_path, SETTINGS, "DEC_URL=x\n# DEC_OTHER=y\nPLAIN=1\n")

    code = main([], config, template)

    assert code == 1
    assert capsys.readouterr().out.splitlines() == [
        ".env.example: missing COMPUTED, read by config.py",
        ".env.example: missing CHOICE, read by config.py",
    ]


def test_a_complete_template_passes(tmp_path: Path) -> None:
    config, template = write(tmp_path, SETTINGS, "DEC_URL=x\nDEC_OTHER=y\nPLAIN=1\nCOMPUTED=\nCHOICE=\n")

    assert main([], config, template) == 0


def test_without_the_settings_module_nothing_is_checked(tmp_path: Path) -> None:
    config, template = write(tmp_path, None, None)

    assert missing(config, template) == []


def test_without_the_template_every_variable_is_missing(tmp_path: Path) -> None:
    config, template = write(tmp_path, SETTINGS, None)

    assert missing(config, template) == ["DEC_URL", "DEC_OTHER", "PLAIN", "COMPUTED", "CHOICE"]


def test_the_repository_template_lists_every_backend_variable() -> None:
    assert missing(CONFIG, TEMPLATE) == []


def test_the_script_runs_as_a_program() -> None:
    script = Path(__file__).resolve().parents[1] / "scripts" / "check_env_example.py"

    completed = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, check=False)

    assert (completed.returncode, completed.stdout) == (0, "")

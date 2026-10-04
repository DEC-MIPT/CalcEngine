import importlib.metadata
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from scripts.check_env_example import (
    CONFIG,
    ROOT,
    TEMPLATE,
    UNREADABLE,
    SettingsVariables,
    check,
    main,
    missing,
    settings_variables,
    template_keys,
)

HEADER = """
from typing import Annotated, ClassVar

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, EnvSettingsSource, SettingsConfigDict
"""


def module(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "config.py"
    path.write_text(HEADER + body, encoding="utf-8")
    return path


@pytest.mark.parametrize(
    ("body", "names"),
    [
        (
            (
                "class S(BaseSettings):\n"
                '    a: str = Field(validation_alias="DEC_A")\n'
                '    b: str = Field(alias="DEC_B")\n'
                '    c: str = Field(alias="DEC_ALIAS", validation_alias="DEC_C")\n'
                "    plain: int = 1\n"
                "    LIMIT: ClassVar[int] = 3\n"
                "    _private: str = 'x'\n"
            ),
            ["DEC_A", "DEC_B", "DEC_C", "PLAIN"],
        ),
        (
            'class S(BaseSettings):\n    a: str = Field(validation_alias=AliasChoices("DEC_A", "DEC_A2"))\n',
            ["DEC_A", "DEC_A2"],
        ),
        ('class S(BaseSettings):\n    model_config = SettingsConfigDict(env_prefix="DEC_")\n    a: str\n', ["DEC_A"]),
        (
            (
                "class S(BaseSettings):\n"
                "    model_config = SettingsConfigDict(alias_generator=lambda name: 'DEC_' + name.upper())\n"
                "    a: str\n"
            ),
            ["DEC_A"],
        ),
        ("class S(BaseSettings):\n    model_config = SettingsConfigDict(case_sensitive=True)\n    a: str\n", ["a"]),
        (
            (
                "class S(BaseSettings):\n"
                "    model_config = SettingsConfigDict(populate_by_name=True)\n"
                '    a: str = Field(validation_alias="DEC_A")\n'
            ),
            ["DEC_A", "A"],
        ),
        ('def env(name):\n    return Field("d", alias=name)\n\nclass S(BaseSettings):\n    a: str = env("DEC_A")\n', ["DEC_A"]),
        ('Url = Annotated[str, Field(alias="DEC_URL")]\n\nclass S(BaseSettings):\n    a: Url\n', ["DEC_URL"]),
        (
            (
                "class Base(BaseSettings):\n"
                '    model_config = SettingsConfigDict(env_prefix="DEC_")\n'
                "    a: str\n\n"
                "class Child(Base):\n"
                "    b: str\n"
            ),
            ["DEC_A", "DEC_B"],
        ),
    ],
    ids=[
        "aliases-and-skipped-attributes",
        "alias-choices",
        "env-prefix",
        "alias-generator",
        "case-sensitive",
        "populate-by-name",
        "field-from-a-helper",
        "type-alias",
        "inherited-prefix",
    ],
)
def test_the_names_are_the_ones_pydantic_settings_reads(tmp_path: Path, body: str, names: list[str]) -> None:
    assert settings_variables(module(tmp_path, body)) == SettingsVariables(names=names, unreadable=[])


@pytest.mark.parametrize(
    ("body", "unreadable"),
    [
        (
            (
                "class S(BaseSettings):\n"
                "    a: str\n\n"
                "    @classmethod\n"
                "    def settings_customise_sources(\n"
                "        cls, settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings\n"
                "    ):\n"
                '        return (EnvSettingsSource(settings_cls, env_prefix="P_"),)\n'
            ),
            ["S.*"],
        ),
        (
            (
                "class S(BaseSettings):\n"
                "    a: str\n\n"
                "    def __init__(self, **values):\n"
                '        super().__init__(_env_prefix="P_", **values)\n'
            ),
            ["S.*"],
        ),
        (
            (
                "class S(BaseSettings):\n"
                "    a: str\n\n"
                "    @classmethod\n"
                "    def _settings_init_sources(cls, *args, **kwargs):\n"
                "        return super()._settings_init_sources(*args, **kwargs)\n"
            ),
            ["S.*"],
        ),
        ('raise RuntimeError("broken")\n', ["<module> (RuntimeError)"]),
        ("import sys\nsys.exit(0)\n", ["<module> (SystemExit)"]),
    ],
    ids=["customised-sources", "custom-init", "private-init-sources", "module-fails", "module-exits"],
)
def test_names_set_by_code_or_a_broken_module_are_unreadable(tmp_path: Path, body: str, unreadable: list[str]) -> None:
    assert settings_variables(module(tmp_path, body)) == SettingsVariables(names=[], unreadable=unreadable)


def test_a_field_pydantic_settings_cannot_resolve_is_unreadable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from pydantic_settings import EnvSettingsSource

    def broken(self: object, field: object, field_name: str) -> list[tuple[str, str, bool]]:
        raise ValueError(field_name)

    monkeypatch.setattr(EnvSettingsSource, "_extract_field_info", broken)

    found = settings_variables(module(tmp_path, "class S(BaseSettings):\n    a: str\n"))

    assert found == SettingsVariables(names=[], unreadable=["S.a"])


def test_a_class_used_twice_in_the_module_is_read_once(tmp_path: Path) -> None:
    found = settings_variables(module(tmp_path, "class S(BaseSettings):\n    a: str\n\nAlias = S\n"))

    assert found == SettingsVariables(names=["A"], unreadable=[])


def test_a_path_that_is_not_a_module_cannot_be_loaded(tmp_path: Path) -> None:
    assert settings_variables(tmp_path) == SettingsVariables(names=[], unreadable=["<module> (ImportError)"])


def test_active_and_commented_keys_are_listed() -> None:
    text = "# A comment\nDEC_A=postgresql://x\n#  DEC_B=http://localhost\n  DEC_C = 1\nnot a key\n# lower=1\n"

    assert template_keys(text) == {"DEC_A", "DEC_B", "DEC_C"}


def test_a_variable_missing_from_the_template_exits_1_with_its_name(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    config = module(tmp_path, 'class S(BaseSettings):\n    a: str = Field(alias="DEC_A")\n    b: str\n')
    template = tmp_path / ".env.example"
    template.write_text("# DEC_A=x\n", encoding="utf-8")

    code = main([], config, template)

    assert code == 1
    assert capsys.readouterr().out.splitlines() == [".env.example: missing B, read by config.py"]


def test_something_unreadable_exits_2_and_names_it(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config = module(tmp_path, 'raise RuntimeError("broken")\n')

    code = main([], config, tmp_path / ".env.example")

    assert code == UNREADABLE == 2
    assert capsys.readouterr().out.splitlines() == ["config.py: cannot read the variable names of <module> (RuntimeError)"]


def test_a_complete_template_exits_0(tmp_path: Path) -> None:
    config = module(tmp_path, 'class S(BaseSettings):\n    a: str = Field(alias="DEC_A")\n')
    template = tmp_path / ".env.example"
    template.write_text("DEC_A=\n", encoding="utf-8")

    assert main([], config, template) == 0


def test_without_the_settings_module_nothing_is_checked(tmp_path: Path) -> None:
    assert check(tmp_path / "config.py", tmp_path / ".env.example") == SettingsVariables()


def test_without_the_template_every_variable_is_missing(tmp_path: Path) -> None:
    config = module(tmp_path, "class S(BaseSettings):\n    a: str\n    b: str\n")

    assert missing(config, tmp_path / ".env.example") == ["A", "B"]


def test_the_repository_settings_are_readable_and_listed() -> None:
    assert check(CONFIG, TEMPLATE) == SettingsVariables()


def test_the_hook_pins_the_installed_pydantic_versions() -> None:
    hooks = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    (hook,) = [hook for repo in hooks["repos"] for hook in repo["hooks"] if hook["id"] == "env-example-matches-settings"]
    pins = dict(requirement.split("==") for requirement in hook["additional_dependencies"])

    assert pins == {name: importlib.metadata.version(name) for name in ("pydantic", "pydantic-settings")}


def test_the_script_runs_as_a_program() -> None:
    script = Path(__file__).resolve().parents[1] / "scripts" / "check_env_example.py"

    completed = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, check=False)

    assert (completed.returncode, completed.stdout) == (0, "")

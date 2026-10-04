import subprocess
import sys
from pathlib import Path

import pytest

from scripts.check_env_example import (
    CONFIG,
    TEMPLATE,
    UNREADABLE,
    SettingsVariables,
    check,
    main,
    missing,
    settings_variables,
    template_keys,
)

SETTINGS = '''
from typing import ClassVar

import pydantic
import pydantic_settings
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env")
    LIMIT: ClassVar[int] = 3
    NAMES: ClassVar = ("a",)
    url: str = Field(validation_alias="DEC_URL")
    other: str = Field(alias="DEC_OTHER")
    plain: int = 1
    again: str = Field(validation_alias="DEC_URL")
    computed: str = Field(default="x")
    qualified: str = pydantic.Field(validation_alias="DEC_QUALIFIED")
    bare: str
    unannotated = "not a field"

    def method(self) -> None: ...


class Other(pydantic_settings.BaseSettings):
    model_config = {"case_sensitive": True}
    both: str = Field(alias="DEC_ALIAS", validation_alias="DEC_VALIDATION")
    reversed_order: str = Field(validation_alias="DEC_FIRST", alias="DEC_SECOND")


class Helper:
    ignored: str = Field(validation_alias="DEC_IGNORED")
'''

READABLE = [
    "DEC_URL",
    "DEC_OTHER",
    "PLAIN",
    "COMPUTED",
    "DEC_QUALIFIED",
    "BARE",
    "DEC_VALIDATION",
    "DEC_FIRST",
]


def write(folder: Path, config: str | None, template: str | None) -> tuple[Path, Path]:
    config_path, template_path = folder / "config.py", folder / ".env.example"
    if config is not None:
        config_path.write_text(config, encoding="utf-8")
    if template is not None:
        template_path.write_text(template, encoding="utf-8")
    return config_path, template_path


def test_the_variables_are_read_like_pydantic_reads_them() -> None:
    assert settings_variables(SETTINGS) == SettingsVariables(names=READABLE, unreadable=[])


@pytest.mark.parametrize(
    ("body", "unreadable"),
    [
        ('    a: str = Field(validation_alias=AliasChoices("A", "B"))\n', ["S.a"]),
        ('    a: str = Field(alias=AliasPath("a", 0))\n', ["S.a"]),
        ("    a: str = Field(validation_alias=NAME)\n", ["S.a"]),
        ("    a: str = Field(validation_alias=None)\n", ["S.a"]),
        ('    a: str = Field(validation_alias=CHOICES, alias="DEC_A")\n', ["S.a"]),
        ('    model_config = SettingsConfigDict(env_prefix="DEC_")\n    a: str\n    b: int = 1\n', ["S.a", "S.b"]),
        ('    model_config = {"env_prefix": "DEC_"}\n    a: str\n', ["S.a"]),
        ("    model_config = SettingsConfigDict(**OPTIONS)\n    a: str\n", ["S.a"]),
        ("    model_config = {KEY: 1}\n    a: str\n", ["S.a"]),
        ("    model_config = OPTIONS\n    a: str\n", ["S.a"]),
    ],
    ids=[
        "alias-choices",
        "alias-path",
        "name",
        "none",
        "validation-alias-not-constant-next-to-alias",
        "env-prefix-call",
        "env-prefix-dict",
        "config-kwargs",
        "config-dict-key-not-constant",
        "config-name",
    ],
)
def test_a_name_that_cannot_be_read_is_reported_not_guessed(body: str, unreadable: list[str]) -> None:
    found = settings_variables(f"class S(BaseSettings):\n{body}")

    assert found == SettingsVariables(names=[], unreadable=unreadable)


def test_a_class_derived_from_another_settings_class_is_unreadable() -> None:
    source = (
        "class Base(BaseSettings):\n    a: str\n\n"
        "class Child(Base):\n    b: str\n\n"
        "class Empty(Base):\n    pass\n\n"
        "class Plain(Helper):\n    c: str\n"
    )

    assert settings_variables(source) == SettingsVariables(names=["A"], unreadable=["Child.b", "Empty.*"])


def test_active_and_commented_keys_are_listed() -> None:
    text = "# A comment\nDEC_A=postgresql://x\n#  DEC_B=http://localhost\n  DEC_C = 1\nnot a key\n# lower=1\n"

    assert template_keys(text) == {"DEC_A", "DEC_B", "DEC_C"}


def test_a_variable_missing_from_the_template_exits_1_with_its_name(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    config, template = write(tmp_path, SETTINGS, "DEC_URL=x\n# DEC_OTHER=y\nPLAIN=1\nDEC_QUALIFIED=\nBARE=\n")

    code = main([], config, template)

    assert code == 1
    assert capsys.readouterr().out.splitlines() == [
        ".env.example: missing COMPUTED, read by config.py",
        ".env.example: missing DEC_VALIDATION, read by config.py",
        ".env.example: missing DEC_FIRST, read by config.py",
    ]


def test_an_unreadable_name_exits_2_and_names_the_class_and_field(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    config, template = write(tmp_path, 'class S(BaseSettings):\n    a: str = Field(alias=X)\n    b: str\n', "")

    code = main([], config, template)

    assert code == UNREADABLE == 2
    assert capsys.readouterr().out.splitlines() == [
        "config.py: cannot read the variable name of S.a",
        ".env.example: missing B, read by config.py",
    ]


def test_a_complete_template_exits_0(tmp_path: Path) -> None:
    config, template = write(tmp_path, SETTINGS, "".join(f"{name}=\n" for name in READABLE))

    assert main([], config, template) == 0


def test_without_the_settings_module_nothing_is_checked(tmp_path: Path) -> None:
    config, template = write(tmp_path, None, None)

    assert check(config, template) == SettingsVariables()


def test_without_the_template_every_variable_is_missing(tmp_path: Path) -> None:
    config, template = write(tmp_path, SETTINGS, None)

    assert missing(config, template) == READABLE


def test_the_repository_settings_are_readable_and_listed() -> None:
    assert check(CONFIG, TEMPLATE) == SettingsVariables()


def test_the_script_runs_as_a_program() -> None:
    script = Path(__file__).resolve().parents[1] / "scripts" / "check_env_example.py"

    completed = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, check=False)

    assert (completed.returncode, completed.stdout) == (0, "")

"""Сверяет переменные окружения настроек бэкенда с ключами ``.env.example``.

Хук pre-commit (``bootstrap-dev-environment`` design.md, решение 5; спецификация
``development-process`` "Pre-commit secret scan and documented configuration"). Модуль
настроек загружается, и имена переменных берутся у самого ``pydantic-settings`` — тем же
кодом, которым приложение читает окружение, поэтому имя не угадывается
(``dev-tooling-followups`` design.md, решение 4).
"""

import importlib.util
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType

from pydantic_settings import BaseSettings, EnvSettingsSource

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "backend" / "app" / "core" / "config.py"
TEMPLATE = ROOT / ".env.example"

KEY = re.compile(r"^\s*(?:#\s*)?([A-Z][A-Z0-9_]*)\s*=")
"""Ключ строки шаблона; закомментированная строка ``# KEY=...`` описывает необязательную переменную."""

UNREADABLE = 2
"""Код выхода, когда имена переменных нельзя получить; недостающая переменная — ``1``."""

MODULE = "_dec_settings_under_check"
"""Имя, под которым модуль настроек загружается на время проверки."""

SOURCE_METHODS = ("settings_customise_sources", "_settings_init_sources", "_settings_build_values", "__init__")
"""Методы ``BaseSettings``, которые выбирают источники или строят значения; их подмена задаёт имена кодом."""


@dataclass
class SettingsVariables:
    """Что модуль настроек говорит о своих переменных окружения.

    Attributes:
        names: имена переменных в порядке классов и полей, без повторов; без учёта
            регистра — в верхнем регистре, с ``case_sensitive=True`` — как есть.
        unreadable: что не удалось прочитать: ``<Класс>.*`` (класс подменяет источники
            настроек или ``__init__``), ``<Класс>.<поле>`` (``pydantic-settings`` не дал
            имён) или ``<module> (<Исключение>)`` (модуль не загрузился).
    """

    names: list[str] = field(default_factory=list)
    unreadable: list[str] = field(default_factory=list)


def _load(config: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(MODULE, config)
    if spec is None or spec.loader is None:
        raise ImportError(str(config))
    module = importlib.util.module_from_spec(spec)
    sys.modules[MODULE] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(MODULE, None)
    return module


def _settings_classes(module: ModuleType) -> list[type[BaseSettings]]:
    found: list[type[BaseSettings]] = []
    for value in vars(module).values():
        if isinstance(value, type) and issubclass(value, BaseSettings) and value is not BaseSettings and value not in found:
            found.append(value)
    return found


def _function(owner: type, name: str) -> object:
    method = getattr(owner, name)
    return getattr(method, "__func__", method)


def _overrides_sources(cls: type[BaseSettings]) -> bool:
    """Подменяет ли класс выбор источников, построение значений или ``__init__``: тогда имена задаёт код."""
    return any(_function(cls, name) is not _function(BaseSettings, name) for name in SOURCE_METHODS)


def settings_variables(config: Path) -> SettingsVariables:
    """Переменные окружения, которые читают классы ``BaseSettings`` модуля настроек.

    Модуль загружается, и для каждого поля имена берутся из
    ``EnvSettingsSource._extract_field_info`` — с алиасами, ``AliasChoices``, префиксом,
    регистром и ``populate_by_name``, как их разрешает ``pydantic-settings``. Класс,
    подменяющий метод из ``SOURCE_METHODS``, и модуль, который не загружается (в том
    числе через ``sys.exit``), — нечитаемы.

    Args:
        config: модуль настроек бэкенда.

    Returns:
        Имена переменных и то, что прочитать не удалось.
    """
    found = SettingsVariables()
    try:
        module = _load(config)
    except BaseException as error:  # noqa: BLE001 - even SystemExit from the module is reported, never raised
        found.unreadable.append(f"<module> ({type(error).__name__})")
        return found
    for cls in _settings_classes(module):
        if _overrides_sources(cls):
            found.unreadable.append(f"{cls.__name__}.*")
            continue
        source = EnvSettingsSource(cls)
        for name, info in cls.model_fields.items():
            try:
                resolved = source._extract_field_info(info, name)
            except Exception:  # noqa: BLE001 - a field pydantic-settings cannot resolve is reported
                found.unreadable.append(f"{cls.__name__}.{name}")
                continue
            for _, env_name, _ in resolved:
                variable = env_name if source.case_sensitive else env_name.upper()
                if variable not in found.names:
                    found.names.append(variable)
    return found


def template_keys(text: str) -> set[str]:
    """Ключи шаблона: активные строки ``KEY=...`` и закомментированные ``# KEY=...``.

    Args:
        text: текст ``.env.example``.

    Returns:
        Множество ключей.
    """
    return {match.group(1) for line in text.splitlines() if (match := KEY.match(line))}


def check(config: Path, template: Path) -> SettingsVariables:
    """Нечитаемое и переменные настроек, которых нет в шаблоне.

    Args:
        config: модуль настроек бэкенда.
        template: файл ``.env.example``.

    Returns:
        В ``names`` — недостающие имена, в ``unreadable`` — то, что прочитать не удалось;
        оба пусты, если модуля настроек ещё нет.
    """
    if not config.exists():
        return SettingsVariables()
    keys = template_keys(template.read_text(encoding="utf-8")) if template.exists() else set()
    found = settings_variables(config)
    return SettingsVariables([name for name in found.names if name not in keys], found.unreadable)


def missing(config: Path, template: Path) -> list[str]:
    """Переменные настроек, которых нет в шаблоне.

    Args:
        config: модуль настроек бэкенда.
        template: файл ``.env.example``.

    Returns:
        Недостающие имена; пустой список, если модуля настроек ещё нет.
    """
    return check(config, template).names


def main(argv: Sequence[str] | None = None, config: Path = CONFIG, template: Path = TEMPLATE) -> int:
    """Печатает нечитаемое и недостающие переменные и возвращает код выхода хука.

    Args:
        argv: имена файлов, которые pre-commit передаёт хуку; не используются.
        config: модуль настроек бэкенда.
        template: файл ``.env.example``.

    Returns:
        ``2``, если что-то не прочитать; ``1``, если шаблон перечисляет не все
        переменные; иначе ``0``.
    """
    found = check(config, template)
    for item in found.unreadable:
        print(f"{config.name}: cannot read the variable names of {item}")
    for name in found.names:
        print(f"{template.name}: missing {name}, read by {config.name}")
    if found.unreadable:
        return UNREADABLE
    return 1 if found.names else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

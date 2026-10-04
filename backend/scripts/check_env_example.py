"""Сверяет переменные окружения настроек бэкенда с ключами ``.env.example``.

Хук pre-commit (``bootstrap-dev-environment`` design.md, решение 5; спецификация
``development-process`` "Pre-commit secret scan and documented configuration"). Модуль
настроек разбирается через ``ast``, без импорта приложения, поэтому хуку не нужны
зависимости бэкенда. Имя переменной читается так, как его разрешает ``pydantic``; имя,
которое нельзя прочитать статически, не угадывается (``dev-tooling-followups`` design.md,
решение 4).
"""

import ast
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "backend" / "app" / "core" / "config.py"
TEMPLATE = ROOT / ".env.example"

KEY = re.compile(r"^\s*(?:#\s*)?([A-Z][A-Z0-9_]*)\s*=")
"""Ключ строки шаблона; закомментированная строка ``# KEY=...`` описывает необязательную переменную."""

UNREADABLE = 2
"""Код выхода, когда имя переменной нельзя прочитать статически; недостающая переменная — ``1``."""


@dataclass
class SettingsVariables:
    """Что модуль настроек говорит о своих переменных окружения.

    Attributes:
        names: прочитанные имена переменных в порядке полей, без повторов.
        unreadable: поля ``<Класс>.<поле>``, имя переменной которых не прочитать без
            запуска кода; ``<Класс>.*`` — класс без своих полей.
    """

    names: list[str] = field(default_factory=list)
    unreadable: list[str] = field(default_factory=list)


def _named(node: ast.expr, name: str) -> bool:
    return (isinstance(node, ast.Name) and node.id == name) or (
        isinstance(node, ast.Attribute) and node.attr == name
    )


def _is_class_var(annotation: ast.expr) -> bool:
    return _named(annotation, "ClassVar") or (
        isinstance(annotation, ast.Subscript) and _named(annotation.value, "ClassVar")
    )


def _target(statement: ast.stmt) -> tuple[str, ast.expr | None] | None:
    if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
        return statement.target.id, statement.value
    if isinstance(statement, ast.Assign) and len(statement.targets) == 1 and isinstance(statement.targets[0], ast.Name):
        return statement.targets[0].id, statement.value
    return None


def _has_prefix(config: ast.expr | None) -> bool:
    """Задаёт ли ``model_config`` префикс; значение, которое не прочитать, считается префиксом."""
    if isinstance(config, ast.Call):
        return any(keyword.arg in ("env_prefix", None) for keyword in config.keywords)
    if isinstance(config, ast.Dict):
        return any(not isinstance(key, ast.Constant) or key.value == "env_prefix" for key in config.keys)
    return True


def _is_field(node: ast.expr | None) -> bool:
    return isinstance(node, ast.Call) and _named(node.func, "Field")


def _fields(annotation: ast.expr, value: ast.expr | None) -> list[ast.Call]:
    """Вызовы ``Field(...)`` поля: в значении и в метаданных ``Annotated[...]``."""
    found = [value] if isinstance(value, ast.Call) and _is_field(value) else []
    if isinstance(annotation, ast.Subscript) and _named(annotation.value, "Annotated"):
        metadata = annotation.slice.elts[1:] if isinstance(annotation.slice, ast.Tuple) else []
        found += [item for item in metadata if isinstance(item, ast.Call) and _is_field(item)]
    return found


def _variable(name: str, annotation: ast.expr, value: ast.expr | None) -> str | None:
    """Имя переменной поля или ``None``, если его не прочитать статически.

    Два ``Field(...)`` у одного поля (в значении и в ``Annotated``) и ``Field(**...)``
    нечитаемы: какой алиас победит, решает ``pydantic`` при запуске.
    """
    fields = _fields(annotation, value)
    if not fields:
        return name.upper()
    if len(fields) > 1 or any(keyword.arg is None for keyword in fields[0].keywords):
        return None
    keywords = {keyword.arg: keyword.value for keyword in fields[0].keywords}
    for key in ("validation_alias", "alias"):
        if key in keywords:
            alias = keywords[key]
            return alias.value if isinstance(alias, ast.Constant) and isinstance(alias.value, str) else None
    return name.upper()


def _settings_classes(classes: list[ast.ClassDef]) -> set[str]:
    """Имена классов настроек модуля: наследники ``BaseSettings`` на любой глубине."""
    found = {node.name for node in classes if any(_named(base, "BaseSettings") for base in node.bases)}
    while True:
        more = {
            node.name
            for node in classes
            if node.name not in found and any(isinstance(base, ast.Name) and base.id in found for base in node.bases)
        }
        if not more:
            return found
        found |= more


def settings_variables(source: str) -> SettingsVariables:
    """Переменные окружения, которые читают классы ``BaseSettings`` модуля.

    Имя переменной — ``validation_alias`` поля, иначе ``alias``, иначе имя поля в верхнем
    регистре, как его ищет ``pydantic-settings`` без префикса. ``model_config`` и атрибуты
    ``ClassVar`` переменными не считаются, поля с подчёркиванием в начале — тоже (для
    ``pydantic`` они приватные). ``Field(...)`` читается и из значения, и из
    ``Annotated[...]``. Неконстантный алиас, ``Field(**...)``, два ``Field`` у поля,
    ``env_prefix`` в ``model_config`` и класс, унаследованный (на любой глубине) от
    другого класса настроек модуля, делают имена полей нечитаемыми.

    Args:
        source: текст модуля настроек.

    Returns:
        Прочитанные имена и нечитаемые поля.
    """
    found = SettingsVariables()
    classes = [node for node in ast.walk(ast.parse(source)) if isinstance(node, ast.ClassDef)]
    settings = _settings_classes(classes)
    for node in classes:
        if node.name not in settings:
            continue
        derived = any(isinstance(base, ast.Name) and base.id in settings for base in node.bases)
        fields: list[tuple[str, ast.expr, ast.expr | None]] = []
        prefixed = derived
        for statement in node.body:
            target = _target(statement)
            if target is None:
                continue
            name, value = target
            if name == "model_config":
                prefixed = prefixed or _has_prefix(value)
            elif (
                isinstance(statement, ast.AnnAssign)
                and not _is_class_var(statement.annotation)
                and not name.startswith("_")
            ):
                fields.append((name, statement.annotation, value))
        if derived and not fields:
            found.unreadable.append(f"{node.name}.*")
        for name, annotation, value in fields:
            variable = None if prefixed else _variable(name, annotation, value)
            if variable is None:
                found.unreadable.append(f"{node.name}.{name}")
            elif variable not in found.names:
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
    """Нечитаемые поля и переменные настроек, которых нет в шаблоне.

    Args:
        config: модуль настроек бэкенда.
        template: файл ``.env.example``.

    Returns:
        В ``names`` — недостающие имена в порядке полей, в ``unreadable`` — нечитаемые
        поля; оба пусты, если модуля настроек ещё нет.
    """
    if not config.exists():
        return SettingsVariables()
    keys = template_keys(template.read_text(encoding="utf-8")) if template.exists() else set()
    found = settings_variables(config.read_text(encoding="utf-8"))
    return SettingsVariables([name for name in found.names if name not in keys], found.unreadable)


def missing(config: Path, template: Path) -> list[str]:
    """Переменные настроек, которых нет в шаблоне.

    Args:
        config: модуль настроек бэкенда.
        template: файл ``.env.example``.

    Returns:
        Недостающие имена в порядке полей; пустой список, если модуля настроек ещё нет.
    """
    return check(config, template).names


def main(argv: Sequence[str] | None = None, config: Path = CONFIG, template: Path = TEMPLATE) -> int:
    """Печатает нечитаемые поля и недостающие переменные и возвращает код выхода хука.

    Args:
        argv: имена файлов, которые pre-commit передаёт хуку; не используются.
        config: модуль настроек бэкенда.
        template: файл ``.env.example``.

    Returns:
        ``2``, если имя какой-то переменной не прочитать; ``1``, если шаблон перечисляет
        не все переменные; иначе ``0``.
    """
    found = check(config, template)
    for item in found.unreadable:
        print(f"{config.name}: cannot read the variable name of {item}")
    for name in found.names:
        print(f"{template.name}: missing {name}, read by {config.name}")
    if found.unreadable:
        return UNREADABLE
    return 1 if found.names else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

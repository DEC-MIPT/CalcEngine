"""Сверяет переменные окружения настроек бэкенда с ключами ``.env.example``.

Хук pre-commit (``bootstrap-dev-environment`` design.md, решение 5; спецификация
``development-process`` "Pre-commit secret scan and documented configuration"). Модуль
настроек разбирается через ``ast``, без импорта приложения, поэтому хуку не нужны
зависимости бэкенда.
"""

import ast
import re
import sys
from collections.abc import Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "backend" / "app" / "core" / "config.py"
TEMPLATE = ROOT / ".env.example"

KEY = re.compile(r"^\s*(?:#\s*)?([A-Z][A-Z0-9_]*)\s*=")
"""Ключ строки шаблона; закомментированная строка ``# KEY=...`` описывает необязательную переменную."""


def _alias(value: ast.expr | None) -> str | None:
    if not (isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == "Field"):
        return None
    for keyword in value.keywords:
        if keyword.arg in ("validation_alias", "alias") and isinstance(keyword.value, ast.Constant):
            alias = keyword.value.value
            return alias if isinstance(alias, str) else None
    return None


def settings_variables(source: str) -> list[str]:
    """Переменные окружения, которые читают классы ``BaseSettings`` модуля.

    Имя переменной — ``validation_alias`` (или ``alias``) поля, иначе имя поля в верхнем
    регистре, как его ищет ``pydantic-settings`` без префикса.

    Args:
        source: текст модуля настроек.

    Returns:
        Имена переменных в порядке полей, без повторов.
    """
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.ClassDef):
            continue
        if not any(isinstance(base, ast.Name) and base.id == "BaseSettings" for base in node.bases):
            continue
        for statement in node.body:
            if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
                name = _alias(statement.value) or statement.target.id.upper()
                if name not in found:
                    found.append(name)
    return found


def template_keys(text: str) -> set[str]:
    """Ключи шаблона: активные строки ``KEY=...`` и закомментированные ``# KEY=...``.

    Args:
        text: текст ``.env.example``.

    Returns:
        Множество ключей.
    """
    return {match.group(1) for line in text.splitlines() if (match := KEY.match(line))}


def missing(config: Path, template: Path) -> list[str]:
    """Переменные настроек, которых нет в шаблоне.

    Args:
        config: модуль настроек бэкенда.
        template: файл ``.env.example``.

    Returns:
        Недостающие имена в порядке полей; пустой список, если модуля настроек ещё нет.
    """
    if not config.exists():
        return []
    keys = template_keys(template.read_text(encoding="utf-8")) if template.exists() else set()
    return [name for name in settings_variables(config.read_text(encoding="utf-8")) if name not in keys]


def main(argv: Sequence[str] | None = None, config: Path = CONFIG, template: Path = TEMPLATE) -> int:
    """Печатает недостающие переменные и возвращает код выхода хука.

    Args:
        argv: имена файлов, которые pre-commit передаёт хуку; не используются.
        config: модуль настроек бэкенда.
        template: файл ``.env.example``.

    Returns:
        ``0``, если шаблон перечисляет все переменные, иначе ``1``.
    """
    absent = missing(config, template)
    for name in absent:
        print(f"{template.name}: missing {name}, read by {config.name}")
    return 1 if absent else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

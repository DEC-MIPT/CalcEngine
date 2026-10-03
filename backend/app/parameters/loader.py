from pathlib import Path

import yaml
from pydantic import ValidationError

from app.core.exceptions import NotFoundError, ParameterValidationError
from app.parameters.param_schemas import ParameterFileSchema


def load_parameters(calculation_type: str, params_root: Path) -> ParameterFileSchema:
    """Читает и проверяет файл ``<params_root>/<calculation_type>.yaml``.

    Args:
        calculation_type: имя типа расчёта, оно же имя файла без расширения.
        params_root: каталог файлов параметров.

    Returns:
        Значения, заданные инженером, в типах ``app.schemas.parameters``.

    Raises:
        NotFoundError: если файла нет.
        ParameterValidationError: если файл не читается как YAML или не проходит
            проверку схемы. Сообщение начинается с пути к файлу, а место ошибки
            pydantic называет значение (например, выходную величину правила).
    """
    path = params_root / f"{calculation_type}.yaml"
    if not path.is_file():
        raise NotFoundError(
            f"no parameter file for calculation type {calculation_type!r} at {path}"
        )

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ParameterValidationError(f"{path}: {exc}") from exc

    try:
        return ParameterFileSchema.model_validate(raw)
    except ValidationError as exc:
        raise ParameterValidationError(f"{path}: {exc}") from exc

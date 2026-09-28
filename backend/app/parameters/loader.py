from pathlib import Path

import yaml
from pydantic import ValidationError

from app.core.exceptions import NotFoundError, ParameterValidationError
from app.parameters.param_schemas import ParameterFileSchema


def load_parameters(calculation_type: str, params_root: Path) -> ParameterFileSchema:
    """Read and validate ``<params_root>/<calculation_type>.yaml``.

    Returns the engineer-set values typed per ``app.schemas.parameters``. Raises a
    ``DECError`` subclass (never a bare pydantic/OS exception) when the file is
    missing or fails schema validation, per this task's verify clause.
    """
    path = params_root / f"{calculation_type}.yaml"
    if not path.is_file():
        raise NotFoundError(
            f"no parameter file for calculation type {calculation_type!r} at {path}"
        )

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ParameterValidationError(str(exc)) from exc

    try:
        return ParameterFileSchema.model_validate(raw)
    except ValidationError as exc:
        raise ParameterValidationError(str(exc)) from exc

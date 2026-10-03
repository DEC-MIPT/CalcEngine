import hashlib
import json
import math
from collections.abc import Mapping

from pydantic import BaseModel

from app.core.exceptions import CalculationError
from app.schemas.calculation import QuantityValue


def _normalized(data: object) -> object:
    if isinstance(data, BaseModel):
        return _normalized(data.model_dump(mode="json"))
    if isinstance(data, Mapping):
        return {str(key): _normalized(value) for key, value in data.items()}
    if isinstance(data, list | tuple):
        return [_normalized(item) for item in data]
    if isinstance(data, bool) or data is None or isinstance(data, str):
        return data
    if isinstance(data, int | float):
        number = float(data)
        if not math.isfinite(number):
            raise CalculationError(f"{data!r} is not a finite number and cannot be hashed")
        return number
    raise CalculationError(f"{type(data).__name__} cannot be part of a hashed value")


def canonical_json(data: object) -> str:
    """JSON with sorted keys, no insignificant whitespace, and every number a float.

    Floats are written by ``repr``, the shortest string that reads back to the same
    value, so ``1`` and ``1.0`` serialize alike (design.md decision 6).
    """
    return json.dumps(
        _normalized(data), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )


def _sha256(data: object) -> str:
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


def parameter_set_id(parameters: object) -> str:
    """The identity of a resolved parameter set, with every reference it carries."""
    return _sha256(parameters)


def input_hash(
    calculation_type: str, inputs: Mapping[str, QuantityValue], parameters: object
) -> str:
    """SHA-256 of the calculation type, the inputs in base units, and the parameter set.

    The algorithm is a proposal until Egor acknowledges it (task 1.8).
    """
    return _sha256(
        {
            "calculation_type": calculation_type,
            "inputs": inputs,
            "parameters": parameter_set_id(parameters),
        }
    )

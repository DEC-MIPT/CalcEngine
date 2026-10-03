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
    """Сериализует данные в канонический JSON.

    Ключи отсортированы, лишних пробелов нет, каждое число — float. Числа пишутся
    через ``repr``, самой короткой строкой, которая читается обратно в то же
    значение, поэтому ``1`` и ``1.0`` сериализуются одинаково (design.md, решение 6).

    Args:
        data: модели pydantic, словари, списки, кортежи, строки, числа, ``bool`` и
            ``None`` в любой вложенности.

    Returns:
        Каноническую JSON-строку.

    Raises:
        CalculationError: если в данных есть не конечное число или значение
            неподдерживаемого типа.
    """
    return json.dumps(
        _normalized(data), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )


def _sha256(data: object) -> str:
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


def parameter_set_id(parameters: object) -> str:
    """Вычисляет идентичность набора разрешённых параметров со всеми их ссылками.

    Args:
        parameters: набор разрешённых параметров.

    Returns:
        SHA-256 канонического JSON набора, шестнадцатеричной строкой.
    """
    return _sha256(parameters)


def input_hash(
    calculation_type: str, inputs: Mapping[str, QuantityValue], parameters: object
) -> str:
    """Вычисляет ``input_hash``: SHA-256 типа расчёта, входов в базовых единицах и набора параметров.

    Алгоритм принят Егором 2026-10-03 без изменений (задача 1.8).

    Args:
        calculation_type: имя типа расчёта.
        inputs: входы в базовых единицах.
        parameters: набор разрешённых параметров.

    Returns:
        Шестнадцатеричную строку из 64 символов.
    """
    return _sha256(
        {
            "calculation_type": calculation_type,
            "inputs": inputs,
            "parameters": parameter_set_id(parameters),
        }
    )

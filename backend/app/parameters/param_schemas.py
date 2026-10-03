from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.calculation import RoundingRule, ValidatedBound, check_bounds
from app.schemas.parameters import EngineerRule


class RoundingEntry(BaseModel):
    """Правило округления одной выходной величины, заданное инженером, и его источник.

    Правило, источник которого — норма, приходит из нормативного каталога, а не из
    этого файла (``calculation-core-contract`` design.md, решение 14).
    """

    model_config = ConfigDict(extra="forbid")

    rule: RoundingRule
    source: EngineerRule


class EngineerBound(ValidatedBound):
    """Граница проверенного диапазона, заданная инженером.

    Граница, источник которой — норма, приходит из нормативного каталога, а не из
    этого файла (``calculation-core-contract`` design.md, решение 15).
    """

    source: EngineerRule


class ParameterFileSchema(BaseModel):
    """Форма файла ``<params_root>/<calculation-type>.yaml``.

    Значения — межслойные типы из ``app.schemas``; этот класс только описывает, как
    они сгруппированы, и отклоняет любой ключ, которого формат не определяет.
    ``validated_range`` упорядочен: предупреждения идут в его порядке. Формуле или
    коэффициенту нормы здесь не место (design.md, решение 3): их источник —
    нормативный каталог, а не файл параметров, заданных инженером.
    """

    model_config = ConfigDict(extra="forbid")

    rounding_rules: dict[str, RoundingEntry] = Field(default_factory=dict)
    validated_range: tuple[EngineerBound, ...] = ()

    @model_validator(mode="after")
    def _validated_range_is_consistent(self) -> "ParameterFileSchema":
        check_bounds(self.validated_range)
        return self

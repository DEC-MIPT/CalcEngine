from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.calculation import RoundingRule, ValidatedBound, check_bounds
from app.schemas.parameters import EngineerRule


class RoundingEntry(BaseModel):
    """An engineer-set rounding rule of one output quantity and the engineer's source.

    A rule whose source is the norm comes from the normative catalog, never from
    this file (``calculation-core-contract`` design.md decision 14).
    """

    model_config = ConfigDict(extra="forbid")

    rule: RoundingRule
    source: EngineerRule


class EngineerBound(ValidatedBound):
    """A bound of the validated range set by the engineer.

    A bound whose source is the norm comes from the normative catalog, never from
    this file (``calculation-core-contract`` design.md decision 15).
    """

    source: EngineerRule


class ParameterFileSchema(BaseModel):
    """The shape of ``<params_root>/<calculation-type>.yaml``.

    Values are the cross-layer types from ``app.schemas``; this file only
    describes how they are grouped, and rejects any key the format does not
    define. ``validated_range`` is ordered: warnings follow its order. A formula
    or a coefficient the norm gives never belongs here (design.md decision 3):
    their source is the normative catalog, not an engineer-set parameter file.
    """

    model_config = ConfigDict(extra="forbid")

    rounding_rules: dict[str, RoundingEntry] = Field(default_factory=dict)
    validated_range: tuple[EngineerBound, ...] = ()

    @model_validator(mode="after")
    def _validated_range_is_consistent(self) -> "ParameterFileSchema":
        check_bounds(self.validated_range)
        return self

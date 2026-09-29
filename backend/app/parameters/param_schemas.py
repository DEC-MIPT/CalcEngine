from pydantic import BaseModel, ConfigDict, Field

from app.schemas.calculation import RoundingRule
from app.schemas.parameters import EngineerRule, ValidatedRange


class RoundingEntry(BaseModel):
    """An engineer-set rounding rule of one output quantity and the engineer's source.

    A rule whose source is the norm comes from the normative catalog, never from
    this file (``calculation-core-contract`` design.md decision 14).
    """

    model_config = ConfigDict(extra="forbid")

    rule: RoundingRule
    source: EngineerRule


class ParameterFileSchema(BaseModel):
    """The shape of ``<params_root>/<calculation-type>.yaml``.

    Values are the cross-layer types from ``app.schemas``; this file only
    describes how they are grouped by quantity name, and rejects any key the
    format does not define. A formula or a coefficient the norm gives never
    belongs here (design.md decision 3): their source is the normative catalog,
    not an engineer-set parameter file.
    """

    model_config = ConfigDict(extra="forbid")

    rounding_rules: dict[str, RoundingEntry] = Field(default_factory=dict)
    validated_ranges: dict[str, ValidatedRange] = Field(default_factory=dict)

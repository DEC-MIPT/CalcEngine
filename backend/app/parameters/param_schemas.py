from pydantic import BaseModel, ConfigDict, Field

from app.schemas.parameters import RoundingRule, ValidatedRange


class ParameterFileSchema(BaseModel):
    """The shape of ``<params_root>/<calculation-type>.yaml``.

    Values are the cross-layer types from ``app.schemas.parameters``; this file
    only describes how they are grouped by quantity name, and rejects any key the
    format does not define. A formula or a coefficient the norm gives never
    belongs here (design.md decision 3): their source is the normative catalog,
    not an engineer-set parameter file.
    """

    model_config = ConfigDict(extra="forbid")

    rounding_rules: dict[str, RoundingRule] = Field(default_factory=dict)
    validated_ranges: dict[str, ValidatedRange] = Field(default_factory=dict)

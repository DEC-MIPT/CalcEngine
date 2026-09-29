from pydantic import BaseModel, ConfigDict, model_validator


class EngineerRule(BaseModel):
    """A rule the design engineer sets where the norm gives none.

    Allowed only as the source of a rounding rule or a validated range
    (`calculation-core-contract` design.md, `NormRef` resolution 3); the engine
    never chooses one itself. Both fields are required: the rule is visible in
    the envelope and the report as engineer-set, never silent.
    """

    model_config = ConfigDict(extra="forbid")

    engineer: str
    rationale: str


class ValidatedRange(EngineerRule):
    """A narrower, engineer-set range within the method's own bounds."""

    min_value: float | None = None
    max_value: float | None = None

    @model_validator(mode="after")
    def _has_at_least_one_bound(self) -> "ValidatedRange":
        if self.min_value is None and self.max_value is None:
            raise ValueError("a validated range needs min_value, max_value, or both")
        if (
            self.min_value is not None
            and self.max_value is not None
            and self.min_value > self.max_value
        ):
            raise ValueError("min_value must not be greater than max_value")
        return self

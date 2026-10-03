from pydantic import BaseModel, ConfigDict


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

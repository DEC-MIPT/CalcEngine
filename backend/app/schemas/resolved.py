from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.calculation import NormRefs, QuantityValue
from app.schemas.expression import ExpressionNode, symbols
from app.schemas.units import UnitSymbol


class Formula(BaseModel):
    """A formula of a norm as a resolved parameter (design.md decision 11).

    ``units`` binds every symbol of the tree, and ``result_symbol``, to its unit.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    latex: str = Field(min_length=1)
    tree: ExpressionNode
    result_symbol: str = Field(min_length=1)
    units: dict[str, UnitSymbol]
    norm_refs: NormRefs

    @model_validator(mode="after")
    def _every_symbol_has_a_unit(self) -> "Formula":
        unbound = [
            name for name in (*symbols(self.tree), self.result_symbol) if name not in self.units
        ]
        if unbound:
            raise ValueError(f"symbols without a unit: {', '.join(unbound)}")
        return self


class Threshold(BaseModel):
    """A value of a norm that decides which branch of a method runs (design.md decision 11).

    A branch is not a trace step; its threshold is a resolved parameter with its own
    ``NormRef`` list, never a literal in code.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    latex: str = Field(min_length=1)
    value: QuantityValue
    norm_refs: NormRefs


class TableValue(BaseModel):
    """One entry of a norm's table as a resolved parameter."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    symbol: str = Field(min_length=1)
    latex: str = Field(min_length=1)
    value: QuantityValue
    norm_refs: NormRefs

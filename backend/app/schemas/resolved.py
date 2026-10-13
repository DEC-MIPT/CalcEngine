from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.calculation import NormRefs, QuantityValue
from app.schemas.expression import ExpressionNode, symbols
from app.schemas.units import UnitSymbol


class Formula(BaseModel):
    """Формула нормы как разрешённый параметр (design.md, решение 11).

    ``units`` связывает с единицей каждый символ дерева и ``result_symbol``.
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
    """Значение нормы, решающее, какая ветвь метода выполняется (design.md, решение 11).

    Ветвь — не шаг трассы; её порог — разрешённый параметр со своим списком
    ``NormRef``, а не литерал в коде.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    latex: str = Field(min_length=1)
    value: QuantityValue
    norm_refs: NormRefs


class Selector(BaseModel):
    """Значение заголовка строки таблицы, по которому выбрано табличное значение.

    ``symbol`` — имя входа типа расчёта, ``value`` — заголовок в его собственной
    единице (``calculation-engine`` "Table value selectors").
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    symbol: str = Field(min_length=1)
    value: QuantityValue


class TableValue(BaseModel):
    """Одно значение из таблицы нормы как разрешённый параметр.

    ``selectors`` — заголовки, по которым выбрана строка; пусто, если значение не
    зависит от входа. Движок сверяет их со входами в ``confirm_selectors``.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    symbol: str = Field(min_length=1)
    latex: str = Field(min_length=1)
    value: QuantityValue
    norm_refs: NormRefs
    selectors: tuple[Selector, ...] = ()

    @model_validator(mode="after")
    def _one_selector_per_symbol(self) -> "TableValue":
        names = [selector.symbol for selector in self.selectors]
        if len(names) != len(set(names)):
            raise ValueError("a table value has at most one selector per symbol")
        return self

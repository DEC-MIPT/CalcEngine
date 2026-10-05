from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.text import LocalizedText
from app.schemas.units import UNITS, Dimension, UnitSymbol


class FieldError(BaseModel):
    """Одно неверное поле запроса: где оно и что с ним не так."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    location: tuple[str | int, ...] = Field(min_length=1)
    message: str = Field(min_length=1)


class ErrorBody(BaseModel):
    """Тело каждого ответа об ошибке (``calculation-api`` "Error responses").

    ``fields`` есть только в теле ``422`` и там есть всегда.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    fields: tuple[FieldError, ...] | None = None


class InputView(BaseModel):
    """Объявленный вход типа расчёта в том виде, какой нужен форме ввода.

    Attributes:
        name: имя входа.
        base_unit: базовая единица входа.
        dimension: размерность базовой единицы.
        units: все единицы словаря этой размерности; форма предлагает их на выбор и
            не держит своей копии словаря (``calculation-api`` design.md, решение 10).
        label: подпись входа.
        symbol: обозначение входа в LaTeX.
        hint: пояснение для входа, если оно есть.
        whole_values_only: ``True``, если вход принимает только целые значения в
            базовой единице (``frontend-app`` design.md, решение 6).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    base_unit: UnitSymbol
    dimension: Dimension
    units: tuple[UnitSymbol, ...] = Field(min_length=1)
    label: LocalizedText
    symbol: str = Field(min_length=1)
    hint: LocalizedText | None = None
    whole_values_only: bool

    @model_validator(mode="after")
    def _units_fit_the_dimension(self) -> "InputView":
        if self.base_unit not in self.units:
            raise ValueError("the base unit must be one of the listed units")
        if any(UNITS[unit].dimension != self.dimension for unit in (self.base_unit, *self.units)):
            raise ValueError("every unit of an input must have the input's dimension")
        return self


class OutputView(BaseModel):
    """Объявленный выход типа расчёта с подписью и обозначением."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    base_unit: UnitSymbol
    label: LocalizedText
    symbol: str = Field(min_length=1)


class CalculationTypeView(BaseModel):
    """Зарегистрированный тип расчёта со входами и выходами в порядке контракта."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    inputs: tuple[InputView, ...]
    outputs: tuple[OutputView, ...]

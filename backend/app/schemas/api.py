from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.units import UNITS, Dimension, UnitSymbol


class FieldError(BaseModel):
    """One invalid field of a request: where it is, and what is wrong with it."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    location: tuple[str | int, ...] = Field(min_length=1)
    message: str = Field(min_length=1)


class ErrorBody(BaseModel):
    """The body of every error response (``calculation-api`` "Error responses").

    ``fields`` is present in a ``422`` body only, and always present there.
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
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    base_unit: UnitSymbol
    dimension: Dimension
    units: tuple[UnitSymbol, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _units_fit_the_dimension(self) -> "InputView":
        if self.base_unit not in self.units:
            raise ValueError("the base unit must be one of the listed units")
        if any(UNITS[unit].dimension != self.dimension for unit in (self.base_unit, *self.units)):
            raise ValueError("every unit of an input must have the input's dimension")
        return self


class OutputView(BaseModel):
    """A declared output of a calculation type."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    base_unit: UnitSymbol


class CalculationTypeView(BaseModel):
    """A registered calculation type with its inputs and outputs in contract order."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    inputs: tuple[InputView, ...]
    outputs: tuple[OutputView, ...]

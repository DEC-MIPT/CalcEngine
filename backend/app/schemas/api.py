from pydantic import BaseModel, ConfigDict, Field

from app.schemas.units import Dimension, UnitSymbol


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
    """A declared input of a calculation type, as the input form needs it."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    base_unit: UnitSymbol
    dimension: Dimension


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

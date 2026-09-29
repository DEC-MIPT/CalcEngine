from pydantic import BaseModel, ConfigDict, Field, model_validator


class QuantityDeclaration(BaseModel):
    """A quantity of a calculation type and the base unit it is held in."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    base_unit: str = Field(min_length=1)


class CalculationTypeContract(BaseModel):
    """What the registry holds for a calculation type besides its calculator.

    Base units and quantity names are data the engineer fills, never values of a
    norm. Output rounding declarations are added by task 4.3.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    inputs: tuple[QuantityDeclaration, ...] = Field(min_length=1)
    outputs: tuple[QuantityDeclaration, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _quantity_names_are_unique(self) -> "CalculationTypeContract":
        for group in (self.inputs, self.outputs):
            names = [quantity.name for quantity in group]
            if len(names) != len(set(names)):
                raise ValueError("quantity names must be unique within inputs and within outputs")
        return self

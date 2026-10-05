from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.calculation import QuantityValue, Source

Origin = Literal["manual calculation", "textbook", "norm application"]
"""Происхождение эталонного примера (`calculation-verification` "Reference examples")."""

ToleranceKind = Literal["absolute", "relative"]
"""Вид допуска: ``absolute`` — в единице ожидаемого значения, ``relative`` — доля от него."""


class SourceCitation(BaseModel):
    """Ссылка на источник эталонного примера.

    Attributes:
        document: документ (например, методичка), из которого взят пример.
        year: год документа.
        locator: страница или номер примера в документе.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    document: str = Field(pattern=r"\S")
    year: int = Field(gt=0)
    locator: str = Field(pattern=r"\S")


class ExpectedOutput(QuantityValue):
    """Ожидаемое значение выхода с допуском и его источником.

    Допуск задаёт инженер, заполняющий пример; требование фиксирует поля, а не число
    (`calculation-verification` design.md, решение 3).

    Attributes:
        tolerance: допуск, не меньше нуля.
        tolerance_kind: вид допуска.
        tolerance_source: пункт нормы, задающий точность, или решение инженера.
    """

    tolerance: float = Field(ge=0)
    tolerance_kind: ToleranceKind
    tolerance_source: Source


class ReferenceExample(BaseModel):
    """Эталонный пример типа расчёта (`calculation-verification` "Reference examples").

    Отсутствующее или пустое поле делает пример недействительным: модель его не
    принимает (design.md, решение 14).

    Attributes:
        example_id: идентификатор примера.
        calculation_type: зарегистрированное имя типа расчёта.
        inputs: входы со своими единицами.
        expected_outputs: ожидаемые выходы по именам величин.
        origin: происхождение примера.
        citation: ссылка на источник.
        source_norm_edition: редакция нормы, по которой посчитан пример, или ``unverified``.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    example_id: str = Field(pattern=r"\S")
    calculation_type: str = Field(pattern=r"\S")
    inputs: dict[str, QuantityValue] = Field(min_length=1)
    expected_outputs: dict[str, ExpectedOutput] = Field(min_length=1)
    origin: Origin
    citation: SourceCitation
    source_norm_edition: str = Field(pattern=r"\S")

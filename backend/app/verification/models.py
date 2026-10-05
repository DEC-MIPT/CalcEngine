from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

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


@dataclass(frozen=True)
class ExampleProblem:
    """Почему сырая карточка не стала эталонным примером.

    Значения карточки сюда не попадают, только её место и пути полей.

    Attributes:
        position: номер карточки в переданной последовательности, с нуля.
        example_id: ``example_id`` карточки, если он читается как непустая строка.
        fields: пути отсутствующих или недопустимых полей, например
            ``expected_outputs.y.tolerance``.
    """

    position: int
    example_id: str | None
    fields: tuple[str, ...]


@dataclass(frozen=True)
class ParsedExamples:
    """Итог разбора карточек: принятые примеры и проблемы отклонённых.

    Attributes:
        examples: примеры, прошедшие модель ``ReferenceExample``.
        problems: по одной записи на отклонённую карточку.
    """

    examples: tuple[ReferenceExample, ...]
    problems: tuple[ExampleProblem, ...]


def _example_id(data: Mapping[str, object]) -> str | None:
    value = data.get("example_id")
    return value if isinstance(value, str) and value.strip() else None


def parse_examples(raw: Sequence[Mapping[str, object]]) -> ParsedExamples:
    """Разбирает сырые карточки эталонных примеров.

    Карточка без ``tolerance`` или ``tolerance_kind`` у какого-либо ожидаемого выхода,
    без ``origin``, ссылки на источник или ``source_norm_edition`` отклоняется
    (`calculation-verification` "Reference examples", сценарий "Too few or incomplete
    examples"; задача 2.2). Набор с отклонённой карточкой недействителен — это решает
    раннер по ``problems``.

    Args:
        raw: карточки в том виде, в каком их прочитали из файла.

    Returns:
        Принятые примеры и проблемы отклонённых карточек.
    """
    examples: list[ReferenceExample] = []
    problems: list[ExampleProblem] = []
    for position, data in enumerate(raw):
        try:
            examples.append(ReferenceExample.model_validate(data))
        except ValidationError as error:
            fields = tuple(dict.fromkeys(".".join(str(part) for part in item["loc"]) for item in error.errors()))
            problems.append(ExampleProblem(position=position, example_id=_example_id(data), fields=fields))
    return ParsedExamples(examples=tuple(examples), problems=tuple(problems))

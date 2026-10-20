from datetime import date
from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    ValidationError,
    model_validator,
)

from app.core.exceptions import ExpressionError
from app.schemas.calculation import NormRefs
from app.schemas.expression import (
    CallNode,
    ExpressionNode,
    children,
    parse_expression,
    symbols,
)

IDENTIFIER_LIMIT = 64
LATEX_LIMIT = 500
COMMENT_LIMIT = 300
MANIFEST_TEXT_LIMIT = 200
"""Пределы длины в кодовых точках Unicode (``interim-normatives-source`` design.md, решение 2).

Они держат в файлах LaTeX и идентификаторы, а не текст нормы; это решение раскладки, не
значения нормы.
"""

Identifier = Annotated[str, Field(min_length=1, max_length=IDENTIFIER_LIMIT)]
Latex = Annotated[str, Field(min_length=1, max_length=LATEX_LIMIT)]
ManifestText = Annotated[str, Field(min_length=1, max_length=MANIFEST_TEXT_LIMIT)]
Digest = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]

VerificationStatus = Literal["pending", "human-verified", "rejected"]


def _names(tree: ExpressionNode) -> tuple[str, ...]:
    functions: list[str] = []
    stack = [tree]
    while stack:
        node = stack.pop()
        if isinstance(node, CallNode):
            functions.append(node.function)
        stack.extend(children(node))
    return (*symbols(tree), *functions)


def _expression_tree(value: JsonValue) -> JsonValue:
    try:
        tree = parse_expression(value)
    except ExpressionError:
        raise ValueError("the expression tree is not valid") from None
    if any(len(name) > IDENTIFIER_LIMIT for name in _names(tree)):
        raise ValueError(f"a symbol or function name in the tree is longer than {IDENTIFIER_LIMIT}")
    return value


ExpressionTree = Annotated[JsonValue, AfterValidator(_expression_tree)]
"""JSON-форма дерева выражения, как её хранит каталог; проверяется при чтении, хранится как есть."""


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class Sunset(_Strict):
    """Срок временного источника: дата и событие, которое его закрывает (design.md, решение 8)."""

    date: date
    event: ManifestText


class InterimManifest(_Strict):
    """``manifest.yaml`` каталога документа (design.md, решение 1).

    Attributes:
        document: обозначение документа нормы.
        edition: редакция, как напечатана на исходном тексте.
        sunset: срок временного источника.
        verifiers: имена, которым разрешено ставить ``human-verified`` и ``rejected``.
    """

    document: ManifestText
    edition: ManifestText
    sunset: Sunset
    verifiers: tuple[Identifier, ...] = ()


class VerificationRecord(_Strict):
    """Запись проверки рядом со значением (design.md, решение 3).

    ``human-verified`` требует ``by``, ``at``, ``portion`` и ``value_digest``; ``rejected`` —
    ``by``, ``at`` и ``comment``. Есть ли ``by`` в ``verifiers`` манифеста, проверяет
    загрузчик. Код этот статус не ставит: он только проверяет уже записанный.

    Attributes:
        status: статус проверки.
        by: кто проверил.
        at: дата проверки.
        portion: идентификатор порции верификатора.
        comment: комментарий; у ``rejected`` — причина.
        value_digest: SHA-256 канонической сериализации записи без ``verification``,
            снятый при проверке.
    """

    status: VerificationStatus
    by: Identifier | None = None
    at: date | None = None
    portion: Identifier | None = None
    comment: Annotated[str, Field(min_length=1, max_length=COMMENT_LIMIT)] | None = None
    value_digest: Digest | None = None

    @model_validator(mode="after")
    def _fields_of_the_status(self) -> "VerificationRecord":
        required = {
            "pending": (),
            "human-verified": ("by", "at", "portion", "value_digest"),
            "rejected": ("by", "at", "comment"),
        }[self.status]
        missing = [name for name in required if getattr(self, name) is None]
        if missing:
            raise ValueError(f"a {self.status} record needs: {', '.join(missing)}")
        return self


class _Record(_Strict):
    norm_refs: NormRefs
    page: int | None = Field(default=None, ge=1)
    verification: VerificationRecord

    @model_validator(mode="after")
    def _a_verified_record_has_its_page(self) -> "_Record":
        if self.verification.status == "human-verified" and self.page is None:
            raise ValueError("a human-verified record needs: page")
        return self


class InterimFormula(_Record):
    """Запись формулы; поля — как у строки ``catalog_read.type_formulas``."""

    parameter: Identifier
    result_symbol: Identifier
    latex: Latex
    tree: ExpressionTree
    units: dict[Identifier, Identifier]


class InterimTableValue(_Record):
    """Запись табличного значения; без заголовка все три поля ``heading_*`` пусты."""

    parameter: Identifier
    symbol: Identifier
    latex: Latex
    value: float
    unit: Identifier
    heading_symbol: Identifier | None = None
    heading_value: float | None = None
    heading_unit: Identifier | None = None


class InterimThreshold(_Record):
    """Запись порога ветви метода."""

    parameter: Identifier
    latex: Latex
    value: float
    unit: Identifier


class InterimCheck(_Record):
    """Запись ссылок нормы одной проверки."""

    parameter: Identifier


class InterimMethodBound(_Record):
    """Запись границы диапазона применения метода."""

    quantity: Identifier
    kind: Identifier
    value: float
    unit: Identifier
    inclusive: bool


InterimRecord = InterimFormula | InterimTableValue | InterimThreshold | InterimCheck | InterimMethodBound


class InterimTypeFile(_Strict):
    """``<calculation-type>.yaml``: пять списков, как пять представлений каталога (решение 2)."""

    formulas: tuple[InterimFormula, ...]
    table_values: tuple[InterimTableValue, ...]
    thresholds: tuple[InterimThreshold, ...]
    checks: tuple[InterimCheck, ...]
    method_bounds: tuple[InterimMethodBound, ...]

    def records(self) -> tuple[tuple[str, InterimRecord], ...]:
        """Записи файла с их путём в файле, например ``formulas[0]``, в порядке файла."""
        return tuple(
            (f"{name}[{index}]", record)
            for name in ("formulas", "table_values", "thresholds", "checks", "method_bounds")
            for index, record in enumerate(getattr(self, name))
        )


def problems(error: ValidationError) -> tuple[str, ...]:
    """Описывает ошибки проверки без проверенных значений.

    Текст pydantic по умолчанию повторяет значение поля, а в файлах временного источника
    это LaTeX или значение нормы; описание называет только путь поля и причину, а ключ
    словаря длиннее предела идентификатора заменяет на ``<key>`` (``interim-normatives``
    "Over-long label rejected", "No data value in the log").

    Args:
        error: ошибка проверки модели.

    Returns:
        Строки ``<путь>: <причина>`` в порядке ошибок.
    """
    return tuple(
        f"{'.'.join(_part(part) for part in item['loc']) or '<root>'}: {item['msg']}"
        for item in error.errors(include_url=False, include_input=False, include_context=False)
    )


def _part(part: str | int) -> str:
    text = str(part)
    return "<key>" if len(text) > IDENTIFIER_LIMIT else text

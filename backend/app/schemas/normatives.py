from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict, TypeAdapter

from app.schemas.calculation import NormRef, NormRefs


@dataclass(frozen=True)
class FormulaRow:
    """Строка ``catalog_read.type_formulas`` одного типа расчёта (``normative-catalog-backend`` design.md, решение 2).

    ``tree``, ``units`` и ``norm_refs`` — JSON как его отдал каталог; проверяет их
    источник параметров.
    """

    parameter: str
    result_symbol: str
    latex: str
    tree: object
    units: object
    norm_refs: object


@dataclass(frozen=True)
class TableValueRow:
    """Строка ``catalog_read.type_table_values``; без заголовка все три его поля — ``None``."""

    parameter: str
    symbol: str
    latex: str
    value: float
    unit: str
    heading_symbol: str | None
    heading_value: float | None
    heading_unit: str | None
    norm_refs: object


@dataclass(frozen=True)
class ThresholdRow:
    """Строка ``catalog_read.type_thresholds``."""

    parameter: str
    latex: str
    value: float
    unit: str
    norm_refs: object


@dataclass(frozen=True)
class CheckRow:
    """Строка ``catalog_read.type_checks``: ссылки нормы одной проверки."""

    parameter: str
    norm_refs: object


@dataclass(frozen=True)
class MethodBoundRow:
    """Строка ``catalog_read.type_method_bounds``: граница диапазона применения метода."""

    quantity: str
    kind: str
    value: float
    unit: str
    inclusive: bool
    norm_refs: object


class SearchHit(BaseModel):
    """Одно совпадение поиска по каталогу (спецификация "Normative search endpoint")."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["document", "clause", "formula"]
    document_id: int
    designation: str
    edition: str
    number: str | None
    title: str | None


class ClauseView(BaseModel):
    """Пункт документа в ответе ``GET /normatives/documents/{document_id}``."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    number: str
    title: str | None
    page: int | None


class DocumentView(BaseModel):
    """Документ каталога со своими пунктами в порядке документа (спецификация "Normative document endpoint")."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    document_id: int
    designation: str
    title: str
    edition: str
    year: int | None
    source_url: str | None
    clauses: tuple[ClauseView, ...]


_NORM_REFS: TypeAdapter[tuple[NormRef, ...]] = TypeAdapter(NormRefs)


def parse_norm_refs(raw: object) -> tuple[NormRef, ...]:
    """Разбирает колонку ``norm_refs`` каталога в непустой список ``NormRef``.

    Args:
        raw: значение колонки ``jsonb`` — список объектов с пятью полями ссылки.

    Returns:
        Ссылки в порядке каталога.

    Raises:
        pydantic.ValidationError: если список пуст, элемент не объект с пятью полями
            или ссылка нарушает правила ``NormRef``.
    """
    return _NORM_REFS.validate_python(raw)

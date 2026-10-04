from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Integer,
    MetaData,
    Numeric,
    Table,
    Text,
    select,
    text,
)
from sqlalchemy.orm import Session

from app.schemas.normatives import (
    CheckRow,
    ClauseView,
    DocumentView,
    FormulaRow,
    MethodBoundRow,
    SearchHit,
    TableValueRow,
    ThresholdRow,
)

SCHEMA = "catalog_read"

metadata = MetaData(schema=SCHEMA)
"""Представления контракта каталога (``normative-catalog-backend`` design.md, решение 2).

Это описание для запросов, а не модель: бэкенд не создаёт и не мигрирует ``dec_normatives``.
``numeric`` читается как ``float`` — то же, что ``float(Decimal(value))``, без округления.
"""

NUMBER = Numeric(asdecimal=False)

SEARCH = text(
    "SELECT kind, document_id, designation, edition, number, title"
    f" FROM {SCHEMA}.search(:query, :max_rows)"
    ' ORDER BY rank DESC, designation COLLATE "C", number COLLATE "C" NULLS FIRST'
)
"""Поиск функцией каталога; порядок равных по рангу — по обозначению и номеру побайтно, без локали базы."""

documents = Table(
    "documents",
    metadata,
    Column("document_id", Integer),
    Column("designation", Text),
    Column("title", Text),
    Column("edition", Text),
    Column("year", Integer),
    Column("source_url", Text),
)
clauses = Table(
    "clauses",
    metadata,
    Column("document_id", Integer),
    Column("position", Integer),
    Column("number", Text),
    Column("title", Text),
    Column("page", Integer),
)
type_formulas = Table(
    "type_formulas",
    metadata,
    Column("calculation_type", Text),
    Column("parameter", Text),
    Column("result_symbol", Text),
    Column("latex", Text),
    Column("tree", JSON),
    Column("units", JSON),
    Column("norm_refs", JSON),
)
type_table_values = Table(
    "type_table_values",
    metadata,
    Column("calculation_type", Text),
    Column("parameter", Text),
    Column("symbol", Text),
    Column("latex", Text),
    Column("value", NUMBER),
    Column("unit", Text),
    Column("heading_symbol", Text),
    Column("heading_value", NUMBER),
    Column("heading_unit", Text),
    Column("norm_refs", JSON),
)
type_thresholds = Table(
    "type_thresholds",
    metadata,
    Column("calculation_type", Text),
    Column("parameter", Text),
    Column("latex", Text),
    Column("value", NUMBER),
    Column("unit", Text),
    Column("norm_refs", JSON),
)
type_checks = Table(
    "type_checks",
    metadata,
    Column("calculation_type", Text),
    Column("parameter", Text),
    Column("norm_refs", JSON),
)
type_method_bounds = Table(
    "type_method_bounds",
    metadata,
    Column("calculation_type", Text),
    Column("quantity", Text),
    Column("kind", Text),
    Column("value", NUMBER),
    Column("unit", Text),
    Column("inclusive", Boolean),
    Column("norm_refs", JSON),
)


class NormativesRepository:
    """Чтение контракта каталога норм: по одному запросу Core на представление (решение 5).

    Каждое значение клиента передаётся связанным параметром. Строки возвращаются как
    их отдал каталог; проверяет их источник параметров.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def formulas(self, calculation_type: str) -> tuple[FormulaRow, ...]:
        """Формулы типа расчёта.

        Args:
            calculation_type: зарегистрированное имя типа расчёта.

        Returns:
            Строки этого типа, упорядоченные по параметру.
        """
        table = type_formulas
        rows = self._session.execute(
            select(
                table.c.parameter,
                table.c.result_symbol,
                table.c.latex,
                table.c.tree,
                table.c.units,
                table.c.norm_refs,
            )
            .where(table.c.calculation_type == calculation_type)
            .order_by(table.c.parameter)
        )
        return tuple(FormulaRow(**row) for row in rows.mappings())

    def table_values(self, calculation_type: str) -> tuple[TableValueRow, ...]:
        """Табличные значения типа расчёта.

        Args:
            calculation_type: зарегистрированное имя типа расчёта.

        Returns:
            Строки этого типа, упорядоченные по параметру и значению заголовка.
        """
        table = type_table_values
        rows = self._session.execute(
            select(
                table.c.parameter,
                table.c.symbol,
                table.c.latex,
                table.c.value,
                table.c.unit,
                table.c.heading_symbol,
                table.c.heading_value,
                table.c.heading_unit,
                table.c.norm_refs,
            )
            .where(table.c.calculation_type == calculation_type)
            .order_by(table.c.parameter, table.c.heading_value)
        )
        return tuple(TableValueRow(**row) for row in rows.mappings())

    def thresholds(self, calculation_type: str) -> tuple[ThresholdRow, ...]:
        """Пороги типа расчёта.

        Args:
            calculation_type: зарегистрированное имя типа расчёта.

        Returns:
            Строки этого типа, упорядоченные по параметру.
        """
        table = type_thresholds
        rows = self._session.execute(
            select(table.c.parameter, table.c.latex, table.c.value, table.c.unit, table.c.norm_refs)
            .where(table.c.calculation_type == calculation_type)
            .order_by(table.c.parameter)
        )
        return tuple(ThresholdRow(**row) for row in rows.mappings())

    def checks(self, calculation_type: str) -> tuple[CheckRow, ...]:
        """Ссылки нормы проверок типа расчёта.

        Args:
            calculation_type: зарегистрированное имя типа расчёта.

        Returns:
            Строки этого типа, упорядоченные по параметру.
        """
        table = type_checks
        rows = self._session.execute(
            select(table.c.parameter, table.c.norm_refs)
            .where(table.c.calculation_type == calculation_type)
            .order_by(table.c.parameter)
        )
        return tuple(CheckRow(**row) for row in rows.mappings())

    def method_bounds(self, calculation_type: str) -> tuple[MethodBoundRow, ...]:
        """Границы диапазона применения метода типа расчёта.

        Args:
            calculation_type: зарегистрированное имя типа расчёта.

        Returns:
            Строки этого типа, упорядоченные по величине и виду границы.
        """
        table = type_method_bounds
        rows = self._session.execute(
            select(
                table.c.quantity,
                table.c.kind,
                table.c.value,
                table.c.unit,
                table.c.inclusive,
                table.c.norm_refs,
            )
            .where(table.c.calculation_type == calculation_type)
            .order_by(table.c.quantity, table.c.kind)
        )
        return tuple(MethodBoundRow(**row) for row in rows.mappings())

    def search(self, query: str, max_rows: int) -> tuple[SearchHit, ...]:
        """Ищет документы, пункты и формулы функцией ``catalog_read.search``.

        Запрос уходит одним оператором, текст клиента — связанным параметром
        (спецификация "Normative search endpoint").

        Args:
            query: текст поиска как его написал клиент.
            max_rows: наибольшее число совпадений.

        Returns:
            Совпадения по убыванию ранга, затем по обозначению и номеру.
        """
        rows = self._session.execute(SEARCH, {"query": query, "max_rows": max_rows})
        return tuple(SearchHit(**row) for row in rows.mappings())

    def document(self, document_id: int) -> DocumentView | None:
        """Документ каталога с пунктами в порядке документа.

        Args:
            document_id: идентификатор документа в каталоге.

        Returns:
            Документ или ``None``, если каталог его не содержит.
        """
        found = self._session.execute(
            select(
                documents.c.document_id,
                documents.c.designation,
                documents.c.title,
                documents.c.edition,
                documents.c.year,
                documents.c.source_url,
            ).where(documents.c.document_id == document_id)
        ).mappings().first()
        if found is None:
            return None
        rows = self._session.execute(
            select(clauses.c.number, clauses.c.title, clauses.c.page)
            .where(clauses.c.document_id == document_id)
            .order_by(clauses.c.position)
        )
        return DocumentView(**found, clauses=tuple(ClauseView(**row) for row in rows.mappings()))

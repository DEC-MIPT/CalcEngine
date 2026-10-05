import logging
from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager
from itertools import groupby

from pydantic import BaseModel

from app.core.exceptions import (
    ExpressionError,
    InputValidationError,
    ParameterSourceUnavailableError,
    UnitError,
)
from app.db.catalog import UNREACHABLE, CatalogSessions
from app.engine.applicability import check_applicability
from app.engine.boundary import convert, inputs_to_base_units
from app.engine.registry import CalculatorRegistry
from app.repositories.normatives import NormativesRepository
from app.schemas.api import FieldError
from app.schemas.calculation import (
    MethodBound,
    QuantityDeclaration,
    QuantityValue,
    check_bounds,
)
from app.schemas.expression import parse_expression, symbols
from app.schemas.normatives import (
    CatalogSnapshot,
    CatalogTableRow,
    CheckRow,
    FormulaRow,
    MethodBoundRow,
    TableValueRow,
    ThresholdRow,
    parse_norm_refs,
)
from app.schemas.resolved import Formula, Selector, TableValue, Threshold
from app.services.catalog import PARAMETER_MODELS
from app.services.parameter_source import ParameterSource, ResolvedParameters

logger = logging.getLogger("app.services.catalog_source")

NO_ROW = "No table row matches this input."
"""Фиксированное сообщение: значение клиента в него не попадает (design.md, решение 6)."""

VIEWS: Mapping[type[BaseModel], str] = {
    Formula: "type_formulas",
    TableValue: "type_table_values",
    Threshold: "type_thresholds",
}
"""Представление для поля модели по его виду; поле со ссылками проверки — ``type_checks``."""

def _view(annotation: object) -> str:
    return next((view for kind, view in VIEWS.items() if annotation is kind), "type_checks")


class CatalogDataError(Exception):
    """Строки каталога нарушают контракт (design.md, решение 7).

    Attributes:
        parameter: параметр, в строках которого нарушение, или ``None``, если у
            нарушения нет параметра (нет привязки, граница метода).
    """

    def __init__(self, parameter: str | None = None) -> None:
        super().__init__(parameter)
        self.parameter = parameter


@contextmanager
def _guard(parameter: str | None) -> Generator[None, None, None]:
    """Превращает ошибку разбора строк каталога в ``CatalogDataError`` без её текста.

    Текст pydantic и других ошибок разбора может содержать значения, поэтому он
    отбрасывается.

    Args:
        parameter: параметр, строки которого разбираются, или ``None``.

    Raises:
        CatalogDataError: если разбор бросил ``ValueError`` (в том числе
            ``ValidationError`` pydantic), ``ExpressionError`` или ``UnitError``.
    """
    try:
        yield
    except (ValueError, ExpressionError, UnitError):
        raise CatalogDataError(parameter) from None


def _formula(row: FormulaRow, quantities: Sequence[QuantityDeclaration]) -> Formula:
    """Собирает формулу из строки каталога и сверяет единицы величин типа.

    ``formula_step`` сравнивает единицы точно и внутри формулы ничего не переводит, а
    входы получает в базовых единицах, поэтому символ или символ результата, названный
    как вход или выход типа, обязан нести базовую единицу этой величины (design.md,
    решение 7).

    Args:
        row: строка ``type_formulas``.
        quantities: входы и выходы контракта типа.

    Returns:
        Формула, проверенная моделью ``Formula``.

    Raises:
        CatalogDataError: если символ входа или выхода типа в формуле не в базовой
            единице этой величины.
    """
    formula = Formula.model_validate(
        {
            "latex": row.latex,
            "tree": parse_expression(row.tree),
            "result_symbol": row.result_symbol,
            "units": row.units,
            "norm_refs": parse_norm_refs(row.norm_refs),
        }
    )
    named = {*symbols(formula.tree), formula.result_symbol}
    if any(quantity.base_unit != formula.units[quantity.name] for quantity in quantities if quantity.name in named):
        raise CatalogDataError(row.parameter)
    return formula


def _threshold(row: ThresholdRow) -> Threshold:
    return Threshold.model_validate(
        {
            "latex": row.latex,
            "value": {"value": row.value, "unit": row.unit},
            "norm_refs": parse_norm_refs(row.norm_refs),
        }
    )


def _heading(row: TableValueRow) -> QuantityValue:
    return QuantityValue.model_validate({"value": row.heading_value, "unit": row.heading_unit})


def _table_value(row: TableValueRow, selectors: tuple[Selector, ...] = ()) -> TableValue:
    return TableValue.model_validate(
        {
            "symbol": row.symbol,
            "latex": row.latex,
            "value": {"value": row.value, "unit": row.unit},
            "norm_refs": parse_norm_refs(row.norm_refs),
            "selectors": selectors,
        }
    )


def _table_row(row: TableValueRow) -> CatalogTableRow:
    heading = None if row.heading_symbol is None else Selector(symbol=row.heading_symbol, value=_heading(row))
    return CatalogTableRow(parameter=row.parameter, entry=_table_value(row), heading=heading)


def _selected(
    parameter: str, rows: Sequence[TableValueRow], inputs: Mapping[str, QuantityValue]
) -> TableValue | None:
    """Проверяет строки одного табличного параметра и выбирает строку по заголовку.

    У параметра либо одна строка без заголовка, либо у всех строк заголовок с одним
    символом входа. Заголовок переводится в базовую единицу входа тем же ``convert``, что
    и в ``confirm_selectors`` движка, и выбирается строка, чей заголовок равен входу
    точно; ни интерполяции, ни ближайшей строки нет (design.md, решения 6 и 7).

    Args:
        parameter: имя параметра.
        rows: его строки.
        inputs: входы в базовых единицах.

    Returns:
        Табличное значение (у выбранного по заголовку — с его ``Selector``) или ``None``,
        если ни одна строка не совпала со входом.

    Raises:
        CatalogDataError: если строки смешаны с заголовком и без, строк без заголовка
            несколько, символов заголовка два, символ не вход, заголовок не переводится
            в единицу входа или два заголовка равны после перевода.
    """
    symbols = {row.heading_symbol for row in rows}
    if None in symbols:
        if len(rows) != 1:
            raise CatalogDataError(parameter)
        return _table_value(rows[0])
    (symbol, *others) = symbols
    if others or symbol is None or symbol not in inputs:
        raise CatalogDataError(parameter)
    given = inputs[symbol]
    headings = [convert(_heading(row), given.unit).value for row in rows]
    if len(set(headings)) != len(headings):
        raise CatalogDataError(parameter)
    if given.value not in headings:
        return None
    row = rows[headings.index(given.value)]
    return _table_value(row, (Selector(symbol=symbol, value=_heading(row)),))


def _bound(row: MethodBoundRow, base_units: Mapping[str, str]) -> MethodBound:
    if row.quantity not in base_units:
        raise CatalogDataError()
    value = convert(QuantityValue.model_validate({"value": row.value, "unit": row.unit}), base_units[row.quantity])
    return MethodBound.model_validate(
        {
            "quantity": row.quantity,
            "kind": row.kind,
            "value": value.value,
            "inclusive": row.inclusive,
            "source": parse_norm_refs(row.norm_refs),
        }
    )


def _check_binding(
    model: type[BaseModel],
    formulas: Sequence[FormulaRow],
    table_values: Sequence[TableValueRow],
    thresholds: Sequence[ThresholdRow],
    checks: Sequence[CheckRow],
) -> None:
    """Проверяет, что каждый параметр модели пришёл ровно один раз и из своего представления.

    Raises:
        CatalogDataError: без параметра, если у типа нет ни одной строки; с параметром,
            если он не объявлен в модели, его нет, он в двух представлениях или не в
            том, что соответствует виду его поля, или дважды в представлении без таблиц.
    """
    found: dict[str, list[str]] = {}
    for view, rows in (
        ("type_formulas", formulas),
        ("type_thresholds", thresholds),
        ("type_checks", checks),
    ):
        for row in rows:
            found.setdefault(row.parameter, []).append(view)
    for parameter in dict.fromkeys(row.parameter for row in table_values):
        found.setdefault(parameter, []).append("type_table_values")
    if not found:
        raise CatalogDataError()
    expected = {
        name: _view(field.annotation) for name, field in model.model_fields.items()
    }
    for parameter in sorted(set(found) | set(expected)):
        if parameter not in expected or found.get(parameter) != [expected[parameter]]:
            raise CatalogDataError(parameter)


class CatalogParameterSource:
    """Источник нормативных параметров из каталога норм (``normatives-catalog`` "Catalog parameter source").

    Читает строки типа расчёта в одной короткой сессии, по одному запросу на
    представление, проверяет их по контракту, собирает из них поля модели параметров
    типа и проверяет их этой моделью. Значения не меняются, кроме выбора строки таблицы и
    перевода границ метода в базовые единицы входов (design.md, решения 5, 6, 7 и 11).

    Args:
        sessions: фабрика сессий каталога.
        registry: реестр типов расчёта; из него берутся контракты.
        models: модель разрешённых параметров каждого типа.
    """

    def __init__(
        self,
        sessions: CatalogSessions,
        registry: CalculatorRegistry,
        models: Mapping[str, type[BaseModel]] = PARAMETER_MODELS,
    ) -> None:
        self._sessions = sessions
        self._registry = registry
        self._models = models

    def resolve(self, calculation_type: str, inputs: Mapping[str, QuantityValue]) -> ResolvedParameters:
        """Собирает параметры и диапазон метода типа расчёта из каталога.

        Вход, не совпавший ни с одной строкой таблицы, сначала проверяется по диапазону
        метода: вне диапазона источник отдаёт ``CatalogSnapshot`` вместо параметров, и
        движок сохраняет отказ (``201``); внутри диапазона вход отвергается (``422``).
        Нарушение контракта в строках каталога пишет одну строку лога с типом и
        параметром, без значений (решение 7); недоступный каталог — одну строку с типом.

        Args:
            calculation_type: зарегистрированное имя типа расчёта.
            inputs: входы запроса, уже проверенные по контракту типа.

        Returns:
            Параметры, проверенные моделью типа, и границы метода в базовых единицах.

        Raises:
            InputValidationError: если вход внутри диапазона метода не совпал ни с одной
                строкой таблицы.
            ParameterSourceUnavailableError: если каталог не настроен или не отвечает (ни
                URL, ни текст ошибки драйвера никуда не попадают, решение 4) или его строки
                нарушают контракт.
        """
        contract = self._registry.contract(calculation_type)
        base_inputs = inputs_to_base_units(contract, inputs)
        try:
            with self._sessions.factory()() as session:
                repository = NormativesRepository(session)
                formulas = repository.formulas(calculation_type)
                table_values = repository.table_values(calculation_type)
                thresholds = repository.thresholds(calculation_type)
                checks = repository.checks(calculation_type)
                bounds = repository.method_bounds(calculation_type)
        except UNREACHABLE:
            logger.warning("code=catalog_unavailable type=%s", calculation_type)
            raise ParameterSourceUnavailableError(
                f"The normative catalog is not available for the calculation type {calculation_type!r}."
            ) from None
        base_units = {quantity.name: quantity.base_unit for quantity in contract.inputs}
        try:
            return self._resolved(
                self._models[calculation_type],
                base_inputs,
                base_units,
                (*contract.inputs, *contract.outputs),
                formulas,
                table_values,
                thresholds,
                checks,
                bounds,
            )
        except CatalogDataError as breach:
            named = "" if breach.parameter is None else f" parameter={breach.parameter}"
            logger.warning("code=catalog_data_invalid type=%s%s", calculation_type, named)
            raise ParameterSourceUnavailableError(
                f"The catalog data of the calculation type {calculation_type!r} are not usable."
            ) from None

    @staticmethod
    def _resolved(
        model: type[BaseModel],
        inputs: Mapping[str, QuantityValue],
        base_units: Mapping[str, str],
        quantities: Sequence[QuantityDeclaration],
        formulas: Sequence[FormulaRow],
        table_values: Sequence[TableValueRow],
        thresholds: Sequence[ThresholdRow],
        checks: Sequence[CheckRow],
        bounds: Sequence[MethodBoundRow],
    ) -> ResolvedParameters:
        _check_binding(model, formulas, table_values, thresholds, checks)
        fields: dict[str, object] = {}
        for formula in formulas:
            with _guard(formula.parameter):
                fields[formula.parameter] = _formula(formula, quantities)
        for threshold in thresholds:
            with _guard(threshold.parameter):
                fields[threshold.parameter] = _threshold(threshold)
        for check in checks:
            with _guard(check.parameter):
                fields[check.parameter] = parse_norm_refs(check.norm_refs)
        table_rows: list[CatalogTableRow] = []
        unmatched: list[str] = []
        for parameter, group in groupby(table_values, key=lambda row: row.parameter):
            rows = tuple(group)
            with _guard(parameter):
                table_rows.extend(_table_row(row) for row in rows)
                entry = _selected(parameter, rows, inputs)
            if entry is None:
                unmatched.append(str(rows[0].heading_symbol))
            fields[parameter] = entry
        with _guard(None):
            method_range = tuple(_bound(row, base_units) for row in bounds)
            check_bounds(method_range)
        if unmatched:
            refusal, _ = check_applicability(inputs, method_range, ())
            if refusal is None:
                raise InputValidationError(
                    NO_ROW,
                    fields=tuple(
                        FieldError(location=("body", "inputs", symbol), message=NO_ROW)
                        for symbol in dict.fromkeys(unmatched)
                    ),
                )
            snapshot = CatalogSnapshot(
                formulas={name: value for name, value in fields.items() if isinstance(value, Formula)},
                table_rows=tuple(table_rows),
                thresholds={name: value for name, value in fields.items() if isinstance(value, Threshold)},
                checks={check.parameter: parse_norm_refs(check.norm_refs) for check in checks},
            )
            return ResolvedParameters(parameters=snapshot, method_range=method_range)
        with _guard(None):
            parameters = model.model_validate(fields)
        return ResolvedParameters(parameters=parameters, method_range=method_range)


def catalog_sources(
    registry: CalculatorRegistry,
    sessions: CatalogSessions,
    models: Mapping[str, type[BaseModel]] = PARAMETER_MODELS,
) -> dict[str, ParameterSource]:
    """Источник каталога для каждого зарегистрированного типа расчёта (design.md, решение 5).

    Все типы делят один ``CatalogParameterSource``. Тип без модели параметров источника
    не получает и отвечает ``503 parameter_source_unavailable``; у каждого типа из
    ``REGISTRATIONS`` модель есть.

    Args:
        registry: реестр типов расчёта.
        sessions: фабрика сессий каталога приложения.
        models: модель разрешённых параметров каждого типа.

    Returns:
        Источник для каждого типа реестра, у которого есть модель параметров.
    """
    source = CatalogParameterSource(sessions, registry, models)
    return {contract.name: source for contract in registry.contracts() if contract.name in models}

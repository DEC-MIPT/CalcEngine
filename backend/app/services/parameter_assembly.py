from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager
from itertools import groupby

from pydantic import BaseModel

from app.core.exceptions import ExpressionError, InputValidationError, UnitError
from app.engine.applicability import check_applicability
from app.engine.boundary import convert
from app.schemas.api import FieldError
from app.schemas.calculation import (
    MethodBound,
    ParameterSourceInfo,
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
from app.services.parameter_source import ResolvedParameters

NO_ROW = "No table row matches this input."
"""Фиксированное сообщение: значение клиента в него не попадает (``normative-catalog-backend`` design.md, решение 6)."""

VIEWS: Mapping[type[BaseModel], str] = {
    Formula: "type_formulas",
    TableValue: "type_table_values",
    Threshold: "type_thresholds",
}
"""Представление для поля модели по его виду; поле со ссылками проверки — ``type_checks``."""

def _view(annotation: object) -> str:
    return next((view for kind, view in VIEWS.items() if annotation is kind), "type_checks")


class ParameterDataError(Exception):
    """Строки данных нарушают контракт (``normative-catalog-backend`` design.md, решение 7).

    Attributes:
        parameter: параметр, в строках которого нарушение, или ``None``, если у
            нарушения нет параметра (нет привязки, граница метода).
    """

    def __init__(self, parameter: str | None = None) -> None:
        super().__init__(parameter)
        self.parameter = parameter


@contextmanager
def _guard(parameter: str | None) -> Generator[None, None, None]:
    """Превращает ошибку разбора строк данных в ``ParameterDataError`` без её текста.

    Текст pydantic и других ошибок разбора может содержать значения, поэтому он
    отбрасывается.

    Args:
        parameter: параметр, строки которого разбираются, или ``None``.

    Raises:
        ParameterDataError: если разбор бросил ``ValueError`` (в том числе
            ``ValidationError`` pydantic), ``ExpressionError`` или ``UnitError``.
    """
    try:
        yield
    except (ValueError, ExpressionError, UnitError):
        raise ParameterDataError(parameter) from None


def _formula(row: FormulaRow, quantities: Sequence[QuantityDeclaration]) -> Formula:
    """Собирает формулу из строки каталога и сверяет единицы величин типа.

    ``formula_step`` сравнивает единицы точно и внутри формулы ничего не переводит, а
    входы получает в базовых единицах, поэтому символ или символ результата, названный
    как вход или выход типа, обязан нести базовую единицу этой величины
    (``normative-catalog-backend`` design.md, решение 7).

    Args:
        row: строка ``type_formulas``.
        quantities: входы и выходы контракта типа.

    Returns:
        Формула, проверенная моделью ``Formula``.

    Raises:
        ParameterDataError: если символ входа или выхода типа в формуле не в базовой
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
        raise ParameterDataError(row.parameter)
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
    parameter: str,
    rows: Sequence[TableValueRow],
    inputs: Mapping[str, QuantityValue],
    selected_by: str | None,
) -> TableValue | None:
    """Проверяет строки одного табличного параметра и выбирает строку по заголовку.

    Параметр, который метод выбирает по входу, приходит строками, у каждой из которых
    заголовок этого входа; параметр, который метод не выбирает, — одной строкой без
    заголовка: без символа, значения и единицы. Заголовок переводится в базовую единицу
    входа тем же ``convert``, что и в ``confirm_selectors`` движка, и выбирается строка,
    чей заголовок равен входу точно; ни интерполяции, ни ближайшей строки нет
    (``normative-catalog-backend`` design.md, решения 6 и 7).

    Args:
        parameter: имя параметра.
        rows: его строки.
        inputs: входы в базовых единицах.
        selected_by: вход, по которому метод выбирает этот параметр, или ``None``.

    Returns:
        Табличное значение (у выбранного по заголовку — с его ``Selector``) или ``None``,
        если ни одна строка не совпала со входом.

    Raises:
        ParameterDataError: если строки смешаны с заголовком и без, строк без заголовка
            несколько, у строки без символа заголовка есть его значение или единица,
            заголовка нет у параметра, выбираемого по входу, или он есть у параметра,
            который по входу не выбирается, символов заголовка два, символ не тот вход,
            по которому метод выбирает параметр, заголовок не переводится в единицу входа
            или два заголовка равны после перевода.
    """
    symbols = {row.heading_symbol for row in rows}
    if None in symbols:
        (row, *more) = rows
        if more or selected_by is not None or row.heading_value is not None or row.heading_unit is not None:
            raise ParameterDataError(parameter)
        return _table_value(row)
    (symbol, *others) = symbols
    if others or symbol is None or symbol != selected_by or symbol not in inputs:
        raise ParameterDataError(parameter)
    given = inputs[symbol]
    headings = [convert(_heading(row), given.unit).value for row in rows]
    if len(set(headings)) != len(headings):
        raise ParameterDataError(parameter)
    if given.value not in headings:
        return None
    row = rows[headings.index(given.value)]
    return _table_value(row, (Selector(symbol=symbol, value=_heading(row)),))


def _bound(row: MethodBoundRow, base_units: Mapping[str, str]) -> MethodBound:
    if row.quantity not in base_units:
        raise ParameterDataError()
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
        ParameterDataError: без параметра, если у типа нет ни одной строки или у строки нет
            имени параметра; с параметром, если он не объявлен в модели, его нет, он в двух
            представлениях или не в том, что соответствует виду его поля, или дважды в
            представлении без таблиц.
    """
    if any(row.parameter is None for group in (formulas, table_values, thresholds, checks) for row in group):
        raise ParameterDataError()
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
        raise ParameterDataError()
    expected = {
        name: _view(field.annotation) for name, field in model.model_fields.items()
    }
    for parameter in sorted(set(found) | set(expected)):
        if parameter not in expected or found.get(parameter) != [expected[parameter]]:
            raise ParameterDataError(parameter)


def assemble(
    model: type[BaseModel],
    selectors: Mapping[str, str],
    inputs: Mapping[str, QuantityValue],
    base_units: Mapping[str, str],
    quantities: Sequence[QuantityDeclaration],
    formulas: Sequence[FormulaRow],
    table_values: Sequence[TableValueRow],
    thresholds: Sequence[ThresholdRow],
    checks: Sequence[CheckRow],
    bounds: Sequence[MethodBoundRow],
    source: ParameterSourceInfo | None = None,
) -> ResolvedParameters:
    """Собирает из строк данных параметры типа расчёта и диапазон метода.

    Общая сборка источников каталога и временного источника (``interim-normatives-source``
    design.md, решение 5): проверка привязки, формулы, пороги, ссылки проверок, выбор строки
    таблицы по входу и границы метода в базовых единицах входов
    (``normative-catalog-backend`` design.md, решения 5, 6, 7 и 11). Вход, не совпавший ни
    с одной строкой таблицы, вне диапазона метода даёт ``CatalogSnapshot`` вместо
    параметров, а внутри диапазона отвергается.

    Args:
        model: модель разрешённых параметров типа.
        selectors: табличный параметр, выбираемый по входу, → этот вход.
        inputs: входы в базовых единицах.
        base_units: базовая единица каждого входа типа.
        quantities: входы и выходы контракта типа.
        formulas: строки формул.
        table_values: строки табличных значений, сгруппированные по параметру.
        thresholds: строки порогов.
        checks: строки ссылок проверок.
        bounds: строки границ метода.
        source: описание источника для ``ResolvedParameters``.

    Returns:
        Параметры, проверенные моделью, или снимок данных, и границы метода.

    Raises:
        ParameterDataError: если строки нарушают контракт данных.
        InputValidationError: если вход внутри диапазона метода не совпал ни с одной
            строкой таблицы.
    """
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
            entry = _selected(parameter, rows, inputs, selectors.get(parameter))
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
        return ResolvedParameters(parameters=snapshot, method_range=method_range, source=source)
    with _guard(None):
        parameters = model.model_validate(fields)
    return ResolvedParameters(parameters=parameters, method_range=method_range, source=source)

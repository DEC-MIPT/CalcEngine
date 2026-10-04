from collections.abc import Mapping, Sequence
from itertools import groupby

from pydantic import BaseModel

from app.core.exceptions import InputValidationError
from app.db.catalog import CatalogSessions
from app.engine.boundary import convert, inputs_to_base_units
from app.engine.registry import CalculatorRegistry
from app.repositories.normatives import NormativesRepository
from app.schemas.api import FieldError
from app.schemas.calculation import MethodBound, QuantityValue
from app.schemas.expression import parse_expression
from app.schemas.normatives import (
    FormulaRow,
    MethodBoundRow,
    TableValueRow,
    ThresholdRow,
    parse_norm_refs,
)
from app.schemas.resolved import Formula, Selector, TableValue, Threshold
from app.services.catalog import PARAMETER_MODELS
from app.services.parameter_source import ResolvedParameters

NO_ROW = "No table row matches this input."
"""Фиксированное сообщение: значение клиента в него не попадает (design.md, решение 6)."""


def _formula(row: FormulaRow) -> Formula:
    return Formula.model_validate(
        {
            "latex": row.latex,
            "tree": parse_expression(row.tree),
            "result_symbol": row.result_symbol,
            "units": row.units,
            "norm_refs": parse_norm_refs(row.norm_refs),
        }
    )


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


def _selected(rows: Sequence[TableValueRow], inputs: Mapping[str, QuantityValue]) -> TableValue:
    """Выбирает строку таблицы, чей заголовок в базовой единице входа равен входу точно.

    Заголовок переводится тем же ``convert``, что и в ``confirm_selectors`` движка, поэтому
    источник и движок сравнивают одни и те же числа (design.md, решение 6).

    Args:
        rows: строки одного параметра.
        inputs: входы в базовых единицах.

    Returns:
        Табличное значение; у выбранного по заголовку — его ``Selector``.

    Raises:
        InputValidationError: если ни одна строка не совпала со входом.
    """
    symbol = rows[0].heading_symbol
    if symbol is None:
        (row,) = rows
        return _table_value(row)
    given = inputs[symbol]
    matches = [row for row in rows if convert(_heading(row), given.unit).value == given.value]
    if not matches:
        raise InputValidationError(NO_ROW, fields=(FieldError(location=("body", "inputs", symbol), message=NO_ROW),))
    (row,) = matches
    return _table_value(row, (Selector(symbol=symbol, value=_heading(row)),))


def _bound(row: MethodBoundRow, base_units: Mapping[str, str]) -> MethodBound:
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


class CatalogParameterSource:
    """Источник нормативных параметров из каталога норм (``normatives-catalog`` "Catalog parameter source").

    Читает строки типа расчёта в одной короткой сессии, по одному запросу на
    представление, собирает из них поля модели параметров типа и проверяет их этой
    моделью. Значения не меняются, кроме выбора строки таблицы и перевода границ метода
    в базовые единицы входов (design.md, решения 5, 6 и 11).

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

        Args:
            calculation_type: зарегистрированное имя типа расчёта.
            inputs: входы запроса, уже проверенные по контракту типа.

        Returns:
            Параметры, проверенные моделью типа, и границы метода в базовых единицах.

        Raises:
            InputValidationError: если вход не совпал ни с одной строкой таблицы.
        """
        contract = self._registry.contract(calculation_type)
        base_inputs = inputs_to_base_units(contract, inputs)
        with self._sessions.factory()() as session:
            repository = NormativesRepository(session)
            formulas = repository.formulas(calculation_type)
            table_values = repository.table_values(calculation_type)
            thresholds = repository.thresholds(calculation_type)
            checks = repository.checks(calculation_type)
            bounds = repository.method_bounds(calculation_type)
        fields: dict[str, object] = {row.parameter: _formula(row) for row in formulas}
        for parameter, rows in groupby(table_values, key=lambda row: row.parameter):
            fields[parameter] = _selected(tuple(rows), base_inputs)
        fields.update({row.parameter: _threshold(row) for row in thresholds})
        fields.update({row.parameter: parse_norm_refs(row.norm_refs) for row in checks})
        base_units = {quantity.name: quantity.base_unit for quantity in contract.inputs}
        return ResolvedParameters(
            parameters=self._models[calculation_type].model_validate(fields),
            method_range=tuple(_bound(row, base_units) for row in bounds),
        )

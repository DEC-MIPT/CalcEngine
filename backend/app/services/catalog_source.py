import logging
from collections.abc import Mapping

from pydantic import BaseModel

from app.core.exceptions import ParameterSourceUnavailableError
from app.db.catalog import UNREACHABLE, CatalogSessions
from app.engine.boundary import inputs_to_base_units
from app.engine.registry import CalculatorRegistry
from app.repositories.normatives import NormativesRepository
from app.schemas.calculation import QuantityValue
from app.services.catalog import PARAMETER_MODELS, TABLE_SELECTORS
from app.services.parameter_assembly import NO_ROW, ParameterDataError, assemble
from app.services.parameter_source import ParameterSource, ResolvedParameters

logger = logging.getLogger("app.services.catalog_source")

__all__ = ["NO_ROW", "CatalogParameterSource", "catalog_sources"]
"""``NO_ROW`` переехал в ``parameter_assembly`` и остаётся доступен отсюда."""


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
        selectors: для каждого типа табличный параметр, выбираемый по входу, → этот вход.
    """

    def __init__(
        self,
        sessions: CatalogSessions,
        registry: CalculatorRegistry,
        models: Mapping[str, type[BaseModel]] = PARAMETER_MODELS,
        selectors: Mapping[str, Mapping[str, str]] = TABLE_SELECTORS,
    ) -> None:
        self._sessions = sessions
        self._registry = registry
        self._models = models
        self._selectors = selectors

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
            return assemble(
                self._models[calculation_type],
                self._selectors.get(calculation_type, {}),
                base_inputs,
                base_units,
                (*contract.inputs, *contract.outputs),
                formulas,
                table_values,
                thresholds,
                checks,
                bounds,
            )
        except ParameterDataError as breach:
            named = "" if breach.parameter is None else f" parameter={breach.parameter}"
            logger.warning("code=catalog_data_invalid type=%s%s", calculation_type, named)
            raise ParameterSourceUnavailableError(
                f"The catalog data of the calculation type {calculation_type!r} are not usable."
            ) from None


def catalog_sources(
    registry: CalculatorRegistry,
    sessions: CatalogSessions,
    models: Mapping[str, type[BaseModel]] = PARAMETER_MODELS,
    selectors: Mapping[str, Mapping[str, str]] = TABLE_SELECTORS,
) -> dict[str, ParameterSource]:
    """Источник каталога для каждого зарегистрированного типа расчёта (design.md, решение 5).

    Все типы делят один ``CatalogParameterSource``. Тип без модели параметров источника
    не получает и отвечает ``503 parameter_source_unavailable``; у каждого типа из
    ``REGISTRATIONS`` модель есть.

    Args:
        registry: реестр типов расчёта.
        sessions: фабрика сессий каталога приложения.
        models: модель разрешённых параметров каждого типа.
        selectors: для каждого типа табличный параметр, выбираемый по входу, → этот вход.

    Returns:
        Источник для каждого типа реестра, у которого есть модель параметров.
    """
    source = CatalogParameterSource(sessions, registry, models, selectors)
    return {contract.name: source for contract in registry.contracts() if contract.name in models}

import hashlib
import json
import logging
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path

from pydantic import BaseModel, ConfigDict, ValidationError

from app.core.exceptions import ParameterSourceUnavailableError
from app.engine import foundations_shallow_r
from app.engine.boundary import inputs_to_base_units
from app.engine.registry import CalculatorRegistry
from app.parameters.interim_loader import load_interim_root
from app.parameters.interim_schemas import (
    InterimApplicabilityCondition,
    InterimCheck,
    InterimDiagramCases,
    InterimFormula,
    InterimMethodBound,
    InterimRecord,
    InterimTableValue,
    InterimThreshold,
    VerificationStatus,
)
from app.schemas.calculation import (
    ParameterSourceInfo,
    QuantityValue,
    validate_loads_domains,
)
from app.schemas.expression import BinaryNode, SymbolNode
from app.schemas.normatives import (
    CheckRow,
    FormulaRow,
    MethodBoundRow,
    TableValueRow,
    ThresholdRow,
)
from app.schemas.resolved import (
    ApplicabilityCondition,
    DiagramCases,
    Formula,
    TableValue,
)
from app.services.catalog import PARAMETER_MODELS, TABLE_SELECTORS
from app.services.interim_data import (
    CheckedRecord,
    InterimTypeData,
    Profile,
    check_documents,
    warn_passed_sunsets,
)
from app.services.parameter_assembly import ParameterDataError, assemble
from app.services.parameter_source import ParameterSource, ResolvedParameters

logger = logging.getLogger("app.services.interim_source")

USABLE: Mapping[Profile, frozenset[VerificationStatus]] = {
    "strict": frozenset({"human-verified"}),
    "draft": frozenset({"human-verified", "pending"}),
}
"""Статусы, которые профиль использует; ``rejected`` не использует ни один (design.md, решение 4)."""

LOADS_TYPE = "foundations_shallow_loads"
LOADS_DOCUMENT = "sp-22-13330-2016"
LOADS_SUPPLEMENT = "sp-22-13330-2016-loads-scope"
LOADS_FILES = {
    "resistance": f"{LOADS_DOCUMENT}/foundations_shallow_r.yaml",
    "pressure": f"{LOADS_DOCUMENT}/foundations_pressure_from_loads.yaml",
    "scope": f"{LOADS_SUPPLEMENT}/{LOADS_TYPE}.yaml",
}


def loads_source_digest(documents: Mapping[str, str]) -> str:
    if set(documents) != {LOADS_DOCUMENT, LOADS_SUPPLEMENT}:
        raise ParameterDataError()
    payload = {
        "format": "foundations-shallow-loads-source-v1",
        "documents": [{"name": name, "data_sha256": documents[name]} for name in sorted(documents)],
    }
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


class _PressureParameters(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    p_edge_plus: Formula
    p_edge_minus: Formula
    p_corner: Formula
    gamma_mt: TableValue
    edge_pressure_limit_multiplier: TableValue
    corner_pressure_limit_multiplier: TableValue


def _loads_limit(name: str, multiplier: TableValue) -> Formula:
    side = "edge" if name == "edge_limit" else "corner"
    coefficient = r"\lambda_e" if name == "edge_limit" else r"\lambda_c"
    return Formula(
        latex=rf"p_{{{side},lim}}={coefficient} R",
        tree=BinaryNode(kind="mul", left=SymbolNode(name=multiplier.symbol), right=SymbolNode(name="R")),
        result_symbol=name, units={multiplier.symbol: "1", "R": "kPa", name: "kPa"},
        norm_refs=multiplier.norm_refs,
    )


def _group(record: InterimRecord) -> tuple[str, ...]:
    """Группа записи для отбора профилем (design.md, решение 5, решение Акима 2026-10-21)."""
    if isinstance(record, InterimMethodBound):
        return ("bound", record.quantity, record.kind)
    if isinstance(record, InterimTableValue):
        heading = "" if record.heading_value is None else repr(record.heading_value)
        return ("parameter", record.parameter, record.heading_symbol or "", heading, record.heading_unit or "")
    return ("parameter", record.parameter)


def _name(group: tuple[str, ...]) -> str:
    return f"{group[1]}/{group[2]}" if group[0] == "bound" else group[1]


def _refs(record: InterimRecord) -> list[dict[str, object]]:
    return [reference.model_dump(mode="json") for reference in record.norm_refs]


@dataclass(frozen=True)
class _TypeRows:
    """Строки одного типа после отбора профилем, в порядке строк каталога."""

    formulas: tuple[FormulaRow, ...]
    table_values: tuple[TableValueRow, ...]
    thresholds: tuple[ThresholdRow, ...]
    checks: tuple[CheckRow, ...]
    bounds: tuple[MethodBoundRow, ...]
    unusable: tuple[str, ...]


def _rows(data: InterimTypeData, profile: Profile) -> _TypeRows:
    """Отбирает записи профилем по группам и строит из них строки каталога.

    Записи ``rejected`` уходят из группы первыми, так что исправленная запись рядом с
    отклонённой её заменяет. Пустая группа или группа, где осталась запись, которую профиль
    не использует, делает параметр или границу непригодными. Строки упорядочены, как их
    отдаёт каталог, поэтому одни данные дают обоим источникам равные параметры.
    """
    groups: dict[tuple[str, ...], list[CheckedRecord]] = {}
    for checked in data.records:
        groups.setdefault(_group(checked.record), []).append(checked)
    kept: list[InterimRecord] = []
    unusable: list[str] = [
        checked.record.parameter
        for checked in data.records
        if isinstance(checked.record, InterimApplicabilityCondition | InterimDiagramCases)
    ]
    for group, members in groups.items():
        live = [member for member in members if member.status != "rejected"]
        if not live or any(member.status not in USABLE[profile] for member in live):
            unusable.append(_name(group))
        else:
            kept.extend(member.record for member in live)
    formulas = [record for record in kept if isinstance(record, InterimFormula)]
    tables = [record for record in kept if isinstance(record, InterimTableValue)]
    thresholds = [record for record in kept if isinstance(record, InterimThreshold)]
    checks = [record for record in kept if isinstance(record, InterimCheck)]
    bounds = [record for record in kept if isinstance(record, InterimMethodBound)]
    return _TypeRows(
        formulas=tuple(
            FormulaRow(r.parameter, r.result_symbol, r.latex, r.tree, r.units, _refs(r))
            for r in sorted(formulas, key=lambda r: r.parameter)
        ),
        table_values=tuple(
            TableValueRow(
                r.parameter, r.symbol, r.latex, r.value, r.unit, r.heading_symbol, r.heading_value, r.heading_unit, _refs(r)
            )
            for r in sorted(tables, key=lambda r: (r.parameter, r.heading_value is not None, r.heading_value or 0.0))
        ),
        thresholds=tuple(
            ThresholdRow(r.parameter, r.latex, r.value, r.unit, _refs(r)) for r in sorted(thresholds, key=lambda r: r.parameter)
        ),
        checks=tuple(CheckRow(r.parameter, _refs(r)) for r in sorted(checks, key=lambda r: r.parameter)),
        bounds=tuple(
            MethodBoundRow(r.quantity, r.kind, r.value, r.unit, r.inclusive, _refs(r))
            for r in sorted(bounds, key=lambda r: (r.quantity, r.kind))
        ),
        unusable=tuple(dict.fromkeys(unusable)),
    )


class InterimParameterSource:
    """Временный источник нормативных параметров из YAML (``interim-normatives`` "Interim parameter source contract").

    Файлы загружены и проверены при старте; на запрос источник берёт строки типа после
    отбора профилем и собирает их той же сборкой, что и каталог, с теми же моделями и
    картами выбора (design.md, решение 5). Ссылки ``NormRef`` доходят до результата как
    записаны: статус источник не повышает (решение 4).

    Args:
        registry: реестр типов расчёта.
        data: проверенные данные каждого типа.
        profile: профиль временного источника.
        models: модель разрешённых параметров каждого типа.
        selectors: для каждого типа табличный параметр, выбираемый по входу, → этот вход.
    """

    def __init__(
        self,
        registry: CalculatorRegistry,
        data: Mapping[str, InterimTypeData],
        profile: Profile,
        models: Mapping[str, type[BaseModel]] = PARAMETER_MODELS,
        selectors: Mapping[str, Mapping[str, str]] = TABLE_SELECTORS,
    ) -> None:
        self._registry = registry
        self._profile = profile
        self._models = models
        self._selectors = selectors
        self._rows = {name: _rows(found, profile) for name, found in data.items()}
        self._info = {
            name: ParameterSourceInfo(kind="interim", data_sha256=found.data_sha256, profile=profile)
            for name, found in data.items()
        }

    def resolve(self, calculation_type: str, inputs: Mapping[str, QuantityValue]) -> ResolvedParameters:
        """Собирает параметры и диапазон метода типа из временных данных.

        Непригодный параметр или граница (нет записи, ``pending`` при ``strict``, только
        ``rejected``) и нарушение контракта в записях пишут одну строку лога с типом и
        параметром, без значений, и делают тип недоступным.

        Args:
            calculation_type: зарегистрированный тип расчёта с временными данными.
            inputs: входы запроса, уже проверенные по контракту типа.

        Returns:
            Параметры, проверенные моделью типа, и границы метода, с описанием источника
            ``interim``: digest данных и профиль.

        Raises:
            InputValidationError: если вход внутри диапазона метода не совпал ни с одной
                строкой таблицы.
            ParameterSourceUnavailableError: если параметр или граница непригодны или записи
                нарушают контракт.
        """
        contract = self._registry.contract(calculation_type)
        rows = self._rows[calculation_type]
        if rows.unusable:
            logger.warning(
                "code=interim_parameter_unusable type=%s profile=%s parameter=%s",
                calculation_type,
                self._profile,
                ",".join(rows.unusable),
            )
            raise ParameterSourceUnavailableError(
                f"The interim data of the calculation type {calculation_type!r} are not usable in the profile {self._profile!r}."
            )
        try:
            return assemble(
                self._models[calculation_type],
                self._selectors.get(calculation_type, {}),
                inputs_to_base_units(contract, inputs),
                {quantity.name: quantity.base_unit for quantity in contract.inputs},
                (*contract.inputs, *contract.outputs),
                rows.formulas,
                rows.table_values,
                rows.thresholds,
                rows.checks,
                rows.bounds,
                source=self._info[calculation_type],
            )
        except ParameterDataError as breach:
            named = "" if breach.parameter is None else f" parameter={breach.parameter}"
            logger.warning("code=interim_data_invalid type=%s%s", calculation_type, named)
            raise ParameterSourceUnavailableError(
                f"The interim data of the calculation type {calculation_type!r} are not usable."
            ) from None


class LoadsInterimParameterSource:
    def __init__(
        self, registry: CalculatorRegistry, found: Mapping[str, InterimTypeData], profile: Profile,
        model: type[BaseModel],
    ) -> None:
        self._registry = registry
        self._profile = profile
        self._model = model
        by_path = {data.file: data for data in found.values()}
        self._data = {name: by_path[path] for name, path in LOADS_FILES.items() if path in by_path}

    def _records(self, name: str) -> InterimTypeData:
        data = self._data[name]
        groups: dict[tuple[str, ...], list[CheckedRecord]] = {}
        for record in data.records:
            groups.setdefault(_group(record.record), []).append(record)
        for members in groups.values():
            live = [member for member in members if member.status != "rejected"]
            if not live or any(member.status not in USABLE[self._profile] for member in live):
                raise ParameterDataError(name)
        return replace(data, records=tuple(record for record in data.records if record.status != "rejected"))

    def resolve(self, calculation_type: str, inputs: Mapping[str, QuantityValue]) -> ResolvedParameters:
        contract = self._registry.contract(calculation_type)
        normalized = inputs_to_base_units(contract, inputs)
        validate_loads_domains(dict(normalized))
        base_units = {quantity.name: quantity.base_unit for quantity in contract.inputs}
        quantities = (*contract.inputs, *contract.outputs)
        try:
            if calculation_type != LOADS_TYPE or set(self._data) != set(LOADS_FILES):
                raise ParameterDataError()
            resistance = self._records("resistance")
            pressure = self._records("pressure")
            scope = self._records("scope")
            scope_rows = _rows(scope, self._profile)
            if (
                scope_rows.formulas or scope_rows.table_values or scope_rows.thresholds or scope_rows.checks
                or scope_rows.unusable or len(scope_rows.bounds) != 1
                or (scope_rows.bounds[0].quantity, scope_rows.bounds[0].kind, scope_rows.bounds[0].unit,
                    scope_rows.bounds[0].inclusive) != ("d_b", "max", "m", True)
            ):
                raise ParameterDataError("scope")
            conditions = [
                entry.record for entry in pressure.records
                if isinstance(entry.record, InterimApplicabilityCondition)
            ]
            diagrams = [entry.record for entry in pressure.records if isinstance(entry.record, InterimDiagramCases)]
            if len(conditions) != 1 or len(diagrams) != 1:
                raise ParameterDataError("pressure_conditions")
            condition, diagram = conditions[0], diagrams[0]
            if (
                condition.parameter != "relative_eccentricity_formula_5_11_limit"
                or (condition.quantity, condition.applies_to, condition.unit, condition.relation)
                != ("e/l", "5.11", "1", "le")
                or diagram.parameter != "pressure_diagram_cases"
                or tuple(case.figure_case for case in diagram.cases) != ("б", "в", "г")
                or diagram.units != {"e": "m", "l": "m", "p_min": "kPa"}
            ):
                raise ParameterDataError("pressure_conditions")
            pressure_rows = _rows(replace(pressure, records=tuple(
                entry for entry in pressure.records
                if not isinstance(entry.record, InterimApplicabilityCondition | InterimDiagramCases)
            )), self._profile)
            resistance_rows = _rows(resistance, self._profile)
            if resistance_rows.unusable or pressure_rows.unusable or pressure_rows.bounds:
                raise ParameterDataError()
            source = ParameterSourceInfo(
                kind="interim", profile=self._profile,
                data_sha256=loads_source_digest({
                    LOADS_DOCUMENT: pressure.data_sha256,
                    LOADS_SUPPLEMENT: scope.data_sha256,
                }),
            )
            resolved_r = assemble(
                foundations_shallow_r.Parameters, foundations_shallow_r.SELECTORS, normalized, base_units, quantities,
                resistance_rows.formulas, resistance_rows.table_values, resistance_rows.thresholds,
                resistance_rows.checks, (*resistance_rows.bounds, *scope_rows.bounds), source,
            )
            resolved_pressure = assemble(
                _PressureParameters, {}, normalized, base_units, quantities,
                pressure_rows.formulas, pressure_rows.table_values, pressure_rows.thresholds,
                pressure_rows.checks, (), source,
            )
            pressure_parameters = _PressureParameters.model_validate(resolved_pressure.parameters)
            parameters = self._model.model_validate({
                "resistance": resolved_r.parameters,
                **pressure_parameters.model_dump(),
                "edge_limit": _loads_limit("edge_limit", pressure_parameters.edge_pressure_limit_multiplier),
                "corner_limit": _loads_limit("corner_limit", pressure_parameters.corner_pressure_limit_multiplier),
                "applicability_condition": ApplicabilityCondition.model_validate(
                    condition.model_dump(exclude={"parameter", "page", "verification"}),
                ),
                "diagram_cases": DiagramCases.model_validate(
                    diagram.model_dump(exclude={"parameter", "page", "verification"}),
                ),
            })
            return ResolvedParameters(parameters, resolved_r.method_range, source)
        except (KeyError, ParameterDataError, ValidationError):
            logger.warning("code=interim_data_invalid type=%s", calculation_type)
            raise ParameterSourceUnavailableError(
                f"The interim data of the calculation type {calculation_type!r} are not usable."
            ) from None


def interim_sources(
    registry: CalculatorRegistry,
    root: Path,
    profile: Profile,
    today: date,
    models: Mapping[str, type[BaseModel]] = PARAMETER_MODELS,
    selectors: Mapping[str, Mapping[str, str]] = TABLE_SELECTORS,
) -> dict[str, ParameterSource]:
    """Загружает временные данные при старте и даёт источник каждому типу с файлом.

    Тип без файла источника не получает и отвечает ``503 parameter_source_unavailable``;
    файл незарегистрированного типа проверен и пропущен (design.md, решение 5). При старте
    пишутся предупреждения о прошедшем сроке и, в ``strict``, о непроверенных записях.

    Args:
        registry: реестр типов расчёта.
        root: корень временных данных.
        profile: профиль временного источника.
        today: сегодняшняя дата для проверки срока.
        models: модель разрешённых параметров каждого типа.
        selectors: для каждого типа табличный параметр, выбираемый по входу, → этот вход.

    Returns:
        Источник для каждого зарегистрированного типа с моделью параметров и файлом данных.

    Raises:
        ParameterValidationError: если данные не проходят проверку при загрузке.
    """
    registered = {contract.name for contract in registry.contracts()}
    documents = load_interim_root(root, registered)
    warn_passed_sunsets(documents, today)
    found = check_documents(documents, profile)
    served: Sequence[str] = [name for name in found if name in registered and name in models and name != LOADS_TYPE]
    source = InterimParameterSource(registry, {name: found[name] for name in served}, profile, models, selectors)
    result: dict[str, ParameterSource] = {name: source for name in served}
    if LOADS_TYPE in registered and LOADS_TYPE in models:
        result[LOADS_TYPE] = LoadsInterimParameterSource(registry, found, profile, models[LOADS_TYPE])
    return result

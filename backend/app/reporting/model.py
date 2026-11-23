from collections.abc import Mapping
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.core.exceptions import InputValidationError
from app.reporting.formula import Line, Math
from app.reporting.symbols import symbol_table
from app.schemas.calculation import (
    BoundViolation,
    CalculationTypeContract,
    CheckStep,
    DerivedViolation,
    NormRef,
    OutputValue,
    ParameterSourceInfo,
    QuantityValue,
    ResultEnvelope,
    RoundingRule,
    TraceStep,
)
from app.schemas.report import ReportRequest


class _Section(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class InputRow(_Section):
    """Один вход в том виде, в каком его дал запрос, до перевода в базовую единицу."""

    quantity: str = Field(min_length=1)
    value: QuantityValue


class InputSection(_Section):
    kind: Literal["inputs"] = "inputs"
    rows: tuple[InputRow, ...]
    guidance: tuple[str, ...] = ()
    math_guidance: tuple[Line, ...] = ()


class TraceSection(_Section):
    """Шаги трассы в порядке выполнения, каждый со своими ``norm_refs``; пусто при отказе."""

    kind: Literal["trace"] = "trace"
    refused: bool
    steps: tuple[TraceStep, ...]


class ConclusionSection(_Section):
    """Вердикт и то, что его решило: решающий шаг проверки или нарушенная граница.

    ``parameter_source`` — источник параметров из конверта; ``None`` у результата без него.
    """

    kind: Literal["conclusion"] = "conclusion"
    verdict: Literal["pass", "fail", "refused"]
    deciding_check: CheckStep | None
    violation: BoundViolation | None
    derived_violation: DerivedViolation | None = None
    parameter_source: ParameterSourceInfo | None = None


class AccountabilitySection(_Section):
    """Блок подотчётности результата: поля конверта, печатаемые после заключения."""

    kind: Literal["accountability"] = "accountability"
    envelope: ResultEnvelope


BodySection = Annotated[
    InputSection | TraceSection | ConclusionSection | AccountabilitySection,
    Field(discriminator="kind"),
]


class Report(_Section):
    """Что записывает модуль вывода: запрос (основная надпись, подписи) и разделы тела.

    ``symbols`` — обозначения в LaTeX, которыми печатаются имена шагов и величин;
    ``rounding`` — правила округления выходов по имени, по которым печатаются их
    значения в трассе и в заключении.
    """

    request: ReportRequest
    body: tuple[BodySection, ...]
    symbols: Mapping[str, str]
    rounding: Mapping[str, RoundingRule]
    default_rounding: RoundingRule | None = None
    norm_refs: tuple[NormRef, ...] = ()
    outputs: tuple[OutputValue, ...] = ()


def _input_rows(
    contract: CalculationTypeContract, inputs: Mapping[str, QuantityValue]
) -> tuple[InputRow, ...]:
    declared = [quantity.name for quantity in contract.inputs]
    if set(inputs) != set(declared):
        raise InputValidationError(
            f"inputs {sorted(inputs)} do not match the declared inputs {declared}"
        )
    return tuple(InputRow(quantity=name, value=inputs[name]) for name in declared)


def _conclusion(envelope: ResultEnvelope) -> ConclusionSection:
    reason = envelope.verdict_reason
    if isinstance(reason, BoundViolation):
        return ConclusionSection(
            verdict=envelope.verdict,
            deciding_check=None,
            violation=reason,
            parameter_source=envelope.parameter_source,
        )
    if isinstance(reason, DerivedViolation):
        return ConclusionSection(
            verdict=envelope.verdict,
            deciding_check=None,
            violation=None,
            derived_violation=reason,
            parameter_source=envelope.parameter_source,
        )
    deciding = next(
        step
        for step in envelope.trace
        if isinstance(step, CheckStep) and step.step_id == reason.step_id
    )
    return ConclusionSection(
        verdict=envelope.verdict,
        deciding_check=deciding,
        violation=None,
        parameter_source=envelope.parameter_source,
    )


def build_report(
    contract: CalculationTypeContract,
    inputs: Mapping[str, QuantityValue],
    envelope: ResultEnvelope,
    request: ReportRequest,
) -> Report:
    """Строит модель отчёта по одному результату (``calculation-core-contract`` design.md, решение 18).

    Тело содержит таблицу исходных данных в порядке входов контракта, трассу,
    заключение и блок подотчётности результата. У отказного расчёта остаются все
    разделы: в разделе трассы нет шагов, а заключение называет нарушенную границу.
    Обозначения шагов и величин берутся из выражений трассы и из контракта, правила
    округления — из выходов конверта.

    Args:
        contract: контракт типа расчёта.
        inputs: входы в том виде, в каком их дал запрос.
        envelope: конверт результата.
        request: данные основной надписи и подписей.

    Returns:
        Модель отчёта.
    """
    explicit = contract.name == "foundations_shallow_weights"
    return Report(
        request=request,
        body=(
            InputSection(
                rows=_input_rows(contract, inputs),
                guidance=(
                    "Направления изменения давления: x=b, y=l. Положительные Mx и Qx увеличивают давление в направлении +x; My и Qy в направлении +y.",
                    "Моменты на подошве: Mx+Qx*h и My+Qy*h; знаки сохраняются, вклады могут компенсироваться.",
                    "N не включает собственный вес фундамента и грунта. Этот вес учитывается один раз.",
                    "d задаёт толщину для собственного веса, h расстояние до плоскости приложения нагрузок, d_1 подготовленную глубину для R. Эти величины независимы.",
                ) if contract.name == "foundations_shallow_loads" else (),
                math_guidance=(
                    ("Направления изменения давления: ", Math("x=b"), ", ", Math("y=l"), ". Знаки нагрузок сохраняются."),
                    ("Нагрузки ", Math("N, M_x, M_y, Q_x, Q_y"), " заданы на верхнем срезе; плечо до подошвы ", Math("h"), "."),
                    ("Полная вертикальная сила на подошве: ", Math("V=N+G_{fund}+G_{soil}+G_{other}"),
                     ". Веса не входят в ", Math("N"), " повторно и не усредняются."),
                    (Math("M_{x,base}=M_x+Q_x h+M_{x,add,base}"), "; ",
                     Math("M_{y,base}=M_y+Q_y h+M_{y,add,base}"), ". Дополнительные моменты заданы на подошве."),
                    ("Веса заданы для одной фиксированной геометрии; перенос на другие размеры при подборе не допускается.",),
                ) if contract.name == "foundations_shallow_weights" else (),
            ),
            TraceSection(refused=envelope.verdict == "refused", steps=envelope.trace),
            _conclusion(envelope),
            AccountabilitySection(envelope=envelope),
        ),
        symbols=symbol_table(contract, envelope.trace),
        rounding={output.quantity: output.rounding_rule for output in envelope.outputs},
        default_rounding=RoundingRule(decimals=2, mode="half_up") if explicit else None,
        norm_refs=envelope.norm_refs if explicit else (),
        outputs=envelope.outputs if explicit else (),
    )

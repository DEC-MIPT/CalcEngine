from collections.abc import Mapping

from app.reporting.format import (
    VERDICT_TEXTS,
    format_bound,
    format_engineer_rule,
    format_norm_ref,
    format_rounding,
    format_source,
    parameter_source_lines,
)
from app.reporting.formula import Line
from app.reporting.model import AccountabilitySection
from app.reporting.symbols import equation, named
from app.schemas.calculation import BoundViolation, DerivedViolation, ResultEnvelope

RESPONSIBILITY = (
    "Ответственность за результат расчёта и за его применение в проектной документации"
    " несёт инженер-проектировщик, а не система."
)
"""Фраза об ответственности инженера из "Result accountability block"."""

NONE = "нет"


def _reason(envelope: ResultEnvelope, symbols: Mapping[str, str]) -> Line:
    reason = envelope.verdict_reason
    if isinstance(reason, BoundViolation):
        return (
            "нарушенная граница области применения метода: ",
            *equation(reason.bound.quantity, reason.value, symbols),
            ", ",
            *format_bound(reason.bound, reason.value.unit),
            f"; источник: {format_source(reason.bound.source)}",
        )
    if isinstance(reason, DerivedViolation):
        return (
            f"условие полного контакта {reason.check_id}; угол {reason.limiting_corner}; ",
            *equation(reason.quantity, reason.value, symbols),
            f"; источник: {format_source(reason.source)}",
        )
    return ("определяющая проверка ", named(reason.step_id, symbols))


def _list(title: str, items: list[Line]) -> list[Line]:
    return [(f"{title}: {NONE}",)] if not items else [(f"{title}:",), *(("— ", *item) for item in items)]


def accountability_lines(section: AccountabilitySection, symbols: Mapping[str, str]) -> list[Line]:
    """Собирает строки блока подотчётности на русском языке.

    В блок входит каждое поле конверта, которое требует "Result accountability block", и
    строка источника параметров, если конверт её несёт (``interim-normatives-source``
    design.md, решение 13). Значения величин — формулы. Фразу об ответственности инженера
    печатает после этих строк модуль вывода.

    Args:
        section: раздел подотчётности модели отчёта с конвертом результата.
        symbols: обозначения в LaTeX по имени шага или величины.

    Returns:
        Строки блока по порядку.
    """
    envelope = section.envelope
    outputs: list[Line] = [
        (
            *equation(output.quantity, output, symbols, output.rounding_rule),
            (
                f"; округление: {format_rounding(output.rounding_rule)};"
                f" источник правила: {format_source(output.rounding_source)}"
            ),
        )
        for output in envelope.outputs
    ]
    warnings: list[Line] = [
        (
            *equation(warning.bound.quantity, warning.value, symbols),
            " вне проверенного диапазона, ",
            *format_bound(warning.bound, warning.value.unit),
            f"; источник: {format_source(warning.bound.source)}",
        )
        for warning in envelope.warnings
    ]
    source: list[Line] = (
        [] if envelope.parameter_source is None else [(text,) for text in parameter_source_lines(envelope.parameter_source)]
    )
    return [
        (f"Идентификатор результата (result_id): {envelope.result_id}",),
        (f"Версия движка (engine_version): {envelope.engine_version}",),
        (f"Хеш входных данных (input_hash): {envelope.input_hash}",),
        *_list("Выходные величины (outputs)", outputs),
        *_list("Нормативные ссылки (norm_refs)", [(format_norm_ref(reference),) for reference in envelope.norm_refs]),
        *_list("Правила инженера (engineer_rules)", [(format_engineer_rule(rule),) for rule in envelope.engineer_rules]),
        (
            f"Вердикт (verdict): {VERDICT_TEXTS[envelope.verdict][0]}; основание (verdict_reason): ",
            *_reason(envelope, symbols),
        ),
        *_list("Предупреждения (warnings)", warnings),
        (f"Шагов с непроверенными ссылками (unverified_step_count): {envelope.unverified_step_count}",),
        *source,
    ]

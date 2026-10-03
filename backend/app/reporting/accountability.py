from app.reporting.format import (
    format_bound,
    format_engineer_rule,
    format_norm_ref,
    format_quantity,
    format_rounding,
    format_source,
)
from app.reporting.model import AccountabilitySection
from app.schemas.calculation import BoundViolation, ResultEnvelope

RESPONSIBILITY = (
    "Ответственность за результат расчёта и за его применение в проектной документации"
    " несёт инженер-проектировщик, а не система."
)
"""Фраза об ответственности инженера из "Result accountability block"."""

VERDICT_NAMES = {"pass": "выполнено", "fail": "не выполнено", "refused": "расчёт отклонён"}
NONE = "нет"


def _reason(envelope: ResultEnvelope) -> str:
    reason = envelope.verdict_reason
    if isinstance(reason, BoundViolation):
        return (
            f"нарушенная граница области применения метода: {reason.bound.quantity} ="
            f" {format_quantity(reason.value)}, {format_bound(reason.bound, reason.value.unit)};"
            f" источник: {format_source(reason.bound.source)}"
        )
    return f"определяющая проверка {reason.step_id}"


def _list(title: str, items: list[str]) -> list[str]:
    return [f"{title}: {NONE}"] if not items else [f"{title}:", *(f"— {item}" for item in items)]


def accountability_lines(section: AccountabilitySection) -> list[str]:
    """Собирает строки блока подотчётности на русском языке.

    В блок входит каждое поле конверта, которое требует "Result accountability block".
    Фразу об ответственности инженера печатает после этих строк модуль вывода.

    Args:
        section: раздел подотчётности модели отчёта с конвертом результата.

    Returns:
        Строки блока по порядку.
    """
    envelope = section.envelope
    outputs = [
        f"{output.quantity} = {format_quantity(output)}; округление: {format_rounding(output.rounding_rule)};"
        f" источник правила: {format_source(output.rounding_source)}"
        for output in envelope.outputs
    ]
    warnings = [
        f"{warning.bound.quantity} = {format_quantity(warning.value)} вне проверенного диапазона,"
        f" {format_bound(warning.bound, warning.value.unit)}; источник: {format_source(warning.bound.source)}"
        for warning in envelope.warnings
    ]
    return [
        f"Идентификатор результата (result_id): {envelope.result_id}",
        f"Версия движка (engine_version): {envelope.engine_version}",
        f"Хеш входных данных (input_hash): {envelope.input_hash}",
        *_list("Выходные величины (outputs)", outputs),
        *_list("Нормативные ссылки (norm_refs)", [format_norm_ref(reference) for reference in envelope.norm_refs]),
        *_list("Правила инженера (engineer_rules)", [format_engineer_rule(rule) for rule in envelope.engineer_rules]),
        f"Вердикт (verdict): {VERDICT_NAMES[envelope.verdict]}; основание (verdict_reason): {_reason(envelope)}",
        *_list("Предупреждения (warnings)", warnings),
        f"Шагов с непроверенными ссылками (unverified_step_count): {envelope.unverified_step_count}",
    ]

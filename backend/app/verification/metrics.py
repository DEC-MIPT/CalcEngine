from dataclasses import dataclass

from pydantic import TypeAdapter

from app.engine.module import module_traceability
from app.schemas.module import ModuleStep
from app.verification.models import ToleranceKind
from app.verification.runner import SuiteReport, Verdict


@dataclass(frozen=True)
class Deviation:
    """Отклонение одной ожидаемой величины примера от вычисленной (задача 2.13).

    Attributes:
        example_id: идентификатор примера.
        quantity: имя величины.
        deviation: вычисленное минус ожидаемое, в ``unit``; ``None``, если вычисленного
            значения нет (отказ, нет выхода, другая размерность).
        unit: единица ожидаемого значения.
        tolerance: допуск величины.
        tolerance_kind: вид допуска.
    """

    example_id: str
    quantity: str
    deviation: float | None
    unit: str
    tolerance: float
    tolerance_kind: ToleranceKind


@dataclass(frozen=True)
class Reproducibility:
    """Воспроизводимость по эталонным примерам (задача 2.14).

    Каждый пример считается дважды с теми же входами и параметрами; воспроизведён
    пример, у которого оба результата равны. Пример, расчёт которого бросил ошибку,
    в знаменателе есть, а в числителе нет: делитель — число примеров (`calculation-verification`
    "Metrics per run").

    Attributes:
        reproduced: число воспроизведённых примеров.
        examples: число примеров.
        not_reproduced: идентификаторы невоспроизведённых примеров по порядку.
    """

    reproduced: int
    examples: int
    not_reproduced: tuple[str, ...]

    @property
    def rate(self) -> float | None:
        """Доля воспроизведённых примеров; ``None`` для набора без примеров."""
        return None if self.examples == 0 else self.reproduced / self.examples

    @property
    def verdict(self) -> Verdict:
        """``NO-GO``, если доля ниже 100% (сбой детерминизма, design.md, решение 9) или примеров нет."""
        return "NO-GO" if self.not_reproduced or self.examples == 0 else "GO"


@dataclass(frozen=True)
class Traceability:
    """Полнота прослеживаемости по конвертам прогона (задача 3.5).

    Проверенный шаг — тот, у которого проверена каждая ``NormRef`` его ``norm_refs``;
    непроверенных шагов столько, сколько ``unverified_step_count`` конверта. Отказные
    конверты не входят. Правила инженера в долю не входят и считаются отдельно. Порога
    у метрики нет, вердикт она не решает (`calculation-verification` "Metrics per run").

    Attributes:
        verified_steps: число проверенных шагов.
        steps: число нормативных шагов трассы; инженерные формулы не входят.
        engineer_rules: число записей ``engineer_rules`` в конвертах.
    """

    verified_steps: int
    steps: int
    engineer_rules: int

    @property
    def completeness(self) -> float | None:
        """Доля проверенных шагов; ``None``, если шагов нет."""
        return None if self.steps == 0 else self.verified_steps / self.steps


def deviations(report: SuiteReport) -> tuple[Deviation, ...]:
    """Отклонения от эталонов по каждой ожидаемой величине каждого примера (задача 2.13).

    Агрегатный процент не считается: у величин разные единицы и допуски (design.md,
    решение 10). Пример, расчёт которого бросил ошибку, величин не даёт.

    Args:
        report: отчёт прогона набора.

    Returns:
        Отклонения в порядке примеров и их ожидаемых величин.
    """
    return tuple(
        Deviation(
            example_id=run.example_id,
            quantity=check.quantity,
            deviation=check.deviation,
            unit=check.expected.unit,
            tolerance=check.expected.tolerance,
            tolerance_kind=check.expected.tolerance_kind,
        )
        for run in report.runs
        for check in run.checks
    )


def reproducibility(report: SuiteReport) -> Reproducibility:
    """Считает воспроизводимость по прогонам примеров набора (задача 2.14).

    Args:
        report: отчёт прогона набора.

    Returns:
        Воспроизводимость набора.
    """
    not_reproduced = tuple(run.example_id for run in report.runs if not run.reproduced)
    return Reproducibility(
        reproduced=len(report.runs) - len(not_reproduced),
        examples=len(report.runs),
        not_reproduced=not_reproduced,
    )


def traceability(report: SuiteReport) -> Traceability:
    """Считает полноту прослеживаемости по неотказным конвертам прогона (задача 3.5).

    Args:
        report: отчёт прогона набора.

    Returns:
        Прослеживаемость набора.
    """
    envelopes = [run.result for run in report.runs if run.result is not None and run.result.verdict != "refused"]
    adapter: TypeAdapter[ModuleStep] = TypeAdapter(ModuleStep)
    measured = [module_traceability(tuple(adapter.validate_python(step.model_dump()) for step in result.trace)) for result in envelopes]
    steps = sum(item.normative_steps for item in measured)
    unverified = sum(item.unverified_steps for item in measured)
    return Traceability(
        verified_steps=steps - unverified,
        steps=steps,
        engineer_rules=sum(len(result.engineer_rules) for result in envelopes),
    )


@dataclass(frozen=True)
class GoReport:
    """Вердикт тестировщика с приложенными тремя метриками (задачи 2.15 и 3.5).

    Attributes:
        verdict: заявленный вердикт.
        deviations: отклонения от эталонов или ``None``, если не приложены.
        reproducibility: воспроизводимость или ``None``, если не приложена.
        traceability: полнота прослеживаемости или ``None``, если не приложена.
    """

    verdict: Verdict
    deviations: tuple[Deviation, ...] | None
    reproducibility: Reproducibility | None
    traceability: Traceability | None

    @property
    def missing_metrics(self) -> tuple[str, ...]:
        """Имена метрик, которые не приложены."""
        attached = {
            "deviation from the references": self.deviations,
            "reproducibility rate": self.reproducibility,
            "traceability completeness": self.traceability,
        }
        return tuple(name for name, value in attached.items() if value is None)

    @property
    def effective_verdict(self) -> Verdict:
        """Вердикт, который действует: GO без метрики недействителен и считается NO-GO.

        Сценарий "Metrics missing" требования "Metrics per run"; воспроизводимость ниже
        100% тоже даёт NO-GO (сценарий "Non-reproducible result").
        """
        if self.verdict == "NO-GO" or self.missing_metrics or self.reproducibility is None:
            return "NO-GO"
        return self.reproducibility.verdict


def go_report(report: SuiteReport) -> GoReport:
    """Строит вердикт набора эталонов с тремя метриками.

    Args:
        report: отчёт прогона набора.

    Returns:
        Вердикт ``GO``, только если набор прошёл и воспроизводимость 100%, с метриками;
        прослеживаемость вердикт не решает.
    """
    measured = reproducibility(report)
    verdict: Verdict = "GO" if report.verdict == "GO" and measured.verdict == "GO" else "NO-GO"
    return GoReport(
        verdict=verdict,
        deviations=deviations(report),
        reproducibility=measured,
        traceability=traceability(report),
    )

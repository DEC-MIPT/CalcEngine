from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Literal

from app.core.exceptions import DECError, UnitError
from app.engine.boundary import convert
from app.engine.pipeline import calculate
from app.engine.registry import CalculatorRegistry
from app.schemas.calculation import CalculationResult, MethodBound, QuantityValue
from app.verification.models import (
    ExampleProblem,
    ExpectedOutput,
    ParsedExamples,
    ReferenceExample,
)

CheckOutcome = Literal["within", "outside", "missing", "incompatible_unit"]
"""Итог сравнения одной величины с ожидаемым значением."""

ExampleOutcome = Literal["passed", "failed", "refused", "error"]
"""Итог примера: все величины в допуске, хотя бы одна нет, отказ расчёта или ошибка."""

Verdict = Literal["GO", "NO-GO"]

MIN_EXAMPLES_PER_TYPE = 3
"""Наименьшее число эталонных примеров на тип расчёта (design.md, решение 1); не значение нормы."""


@dataclass(frozen=True)
class ExampleParameters:
    """Разрешённые параметры, с которыми считается эталонный пример.

    Откуда они берутся, раннер не решает (`calculation-verification` design.md,
    решение 14).

    Attributes:
        parameters: разрешённые параметры калькулятора типа.
        method_range: границы диапазона метода.
    """

    parameters: object
    method_range: tuple[MethodBound, ...] = ()


Resolver = Callable[[ReferenceExample], ExampleParameters]
"""Функция, которая даёт параметры примера."""


@dataclass(frozen=True)
class QuantityCheck:
    """Сравнение одной ожидаемой величины с вычисленной.

    Attributes:
        quantity: имя величины.
        expected: ожидаемое значение с допуском.
        computed: вычисленное значение в единице ожидаемого или ``None``, если его нет
            или его нельзя перевести в эту единицу.
        outcome: итог сравнения.
    """

    quantity: str
    expected: ExpectedOutput
    computed: QuantityValue | None
    outcome: CheckOutcome

    @property
    def deviation(self) -> float | None:
        """Вычисленное минус ожидаемое в единице ожидаемого; ``None``, если вычисленного нет."""
        return None if self.computed is None else self.computed.value - self.expected.value


@dataclass(frozen=True)
class ExampleRun:
    """Прогон одного эталонного примера.

    Attributes:
        example_id: идентификатор примера.
        calculation_type: тип расчёта примера.
        outcome: итог примера.
        checks: сравнения по ожидаемым величинам, в порядке карточки; пусто при ошибке.
        error: имя класса ошибки, если расчёт или получение параметров её бросили.
        reproduced: оба расчёта примера дали равные результаты; ``False`` при ошибке
            (`calculation-verification` "Metrics per run", воспроизводимость).
    """

    example_id: str
    calculation_type: str
    outcome: ExampleOutcome
    checks: tuple[QuantityCheck, ...] = ()
    error: str | None = None
    reproduced: bool = False


@dataclass(frozen=True)
class TooFewExamples:
    """У типа расчёта меньше ``MIN_EXAMPLES_PER_TYPE`` принятых примеров.

    Attributes:
        calculation_type: тип расчёта из списка набора.
        count: сколько принятых примеров у него есть.
    """

    calculation_type: str
    count: int


@dataclass(frozen=True)
class RejectedExample:
    """Карточка отклонена при разборе (задача 2.2).

    Attributes:
        problem: место карточки и пути её недопустимых полей.
    """

    problem: ExampleProblem


@dataclass(frozen=True)
class NoCalculationTypes:
    """Набору не передан ни один тип расчёта, так что проверять нечего."""


InvalidReason = TooFewExamples | RejectedExample | NoCalculationTypes
"""Почему набор эталонов недействителен (сценарий "Too few or incomplete examples")."""


@dataclass(frozen=True)
class SuiteReport:
    """Отчёт прогона набора эталонов (design.md, решение 15).

    Attributes:
        verdict: ``GO``, только если набор действителен и каждый пример прошёл.
        runs: прогоны принятых примеров в порядке набора.
        invalid: причины, по которым набор недействителен; пусто для действительного.
    """

    verdict: Verdict
    runs: tuple[ExampleRun, ...]
    invalid: tuple[InvalidReason, ...] = ()

    @property
    def failures(self) -> tuple[tuple[str, QuantityCheck], ...]:
        """Величины вне допуска или без значения, с идентификатором примера."""
        return tuple(
            (run.example_id, check) for run in self.runs for check in run.checks if check.outcome != "within"
        )


def within_tolerance(computed: float, expected: ExpectedOutput) -> bool:
    """Проверяет правило допуска требования «Reference examples».

    ``absolute``: модуль разности не больше ``tolerance``; ``relative``: не больше
    ``tolerance`` на модуль ожидаемого значения. Граница допуска входит.

    Args:
        computed: вычисленное значение в единице ожидаемого.
        expected: ожидаемое значение с допуском.

    Returns:
        ``True``, если значение в допуске.
    """
    limit = expected.tolerance if expected.tolerance_kind == "absolute" else expected.tolerance * abs(expected.value)
    return abs(computed - expected.value) <= limit


def _check(quantity: str, expected: ExpectedOutput, result: CalculationResult) -> QuantityCheck:
    output = next((output for output in result.outputs if output.quantity == quantity), None)
    if output is None:
        return QuantityCheck(quantity=quantity, expected=expected, computed=None, outcome="missing")
    try:
        computed = convert(QuantityValue(value=output.value, unit=output.unit), expected.unit)
    except UnitError:
        return QuantityCheck(quantity=quantity, expected=expected, computed=None, outcome="incompatible_unit")
    outcome: CheckOutcome = "within" if within_tolerance(computed.value, expected) else "outside"
    return QuantityCheck(quantity=quantity, expected=expected, computed=computed, outcome=outcome)


def run_example(example: ReferenceExample, registry: CalculatorRegistry, resolve: Resolver) -> ExampleRun:
    """Считает один пример дважды через чистую функцию расчёта и сравнивает выходы.

    Пример идёт только через ``engine.pipeline.calculate`` и читает только конверт
    (design.md, "Swap boundary"). Отказ расчёта — провал примера. Второй расчёт с теми же
    входами и параметрами нужен для метрики воспроизводимости (задача 2.14): чистая
    функция не возвращает ``result_id``, поэтому результаты сравниваются целиком.

    Args:
        example: эталонный пример.
        registry: реестр типов расчёта.
        resolve: функция, которая даёт параметры примера.

    Returns:
        Прогон примера.
    """
    try:
        resolved = resolve(example)
        contract = registry.contract(example.calculation_type)
        calculator = registry.get(example.calculation_type)
        result, repeat = (
            calculate(contract, calculator, example.inputs, resolved.parameters, method_range=resolved.method_range)
            for _ in range(2)
        )
    except DECError as error:
        return ExampleRun(example.example_id, example.calculation_type, "error", error=type(error).__name__)
    checks = tuple(_check(quantity, expected, result) for quantity, expected in example.expected_outputs.items())
    reproduced = result == repeat
    if result.verdict == "refused":
        return ExampleRun(example.example_id, example.calculation_type, "refused", checks, reproduced=reproduced)
    outcome: ExampleOutcome = "passed" if all(check.outcome == "within" for check in checks) else "failed"
    return ExampleRun(example.example_id, example.calculation_type, outcome, checks, reproduced=reproduced)


def run_suite(
    examples: Sequence[ReferenceExample], registry: CalculatorRegistry, resolve: Resolver
) -> SuiteReport:
    """Прогоняет набор эталонных примеров (задача 2.3).

    Вердикт ``GO``, только если каждый пример прошёл; иначе ``NO-GO``, и отчёт
    называет пример, величину, вычисленное и ожидаемое значения и допуск (сценарий
    "A quantity outside its tolerance").

    Args:
        examples: эталонные примеры набора.
        registry: реестр типов расчёта.
        resolve: функция, которая даёт параметры примера.

    Returns:
        Отчёт набора.
    """
    runs = tuple(run_example(example, registry, resolve) for example in examples)
    verdict: Verdict = "GO" if all(run.outcome == "passed" for run in runs) else "NO-GO"
    return SuiteReport(verdict=verdict, runs=runs)


def suite_invalidity(parsed: ParsedExamples, calculation_types: Sequence[str]) -> tuple[InvalidReason, ...]:
    """Находит причины, по которым набор эталонов недействителен.

    Набор недействителен, если какая-либо карточка отклонена при разборе, если список
    типов пуст или если у типа из списка меньше ``MIN_EXAMPLES_PER_TYPE`` принятых
    примеров (задача 2.4). Отклонённая карточка в счёт примеров не входит.

    Args:
        parsed: итог ``parse_examples``.
        calculation_types: типы расчёта, которые набор обязан покрыть.

    Returns:
        Причины в порядке: отклонённые карточки, пустой список, типы с нехваткой примеров.
    """
    reasons: list[InvalidReason] = [RejectedExample(problem) for problem in parsed.problems]
    if not calculation_types:
        reasons.append(NoCalculationTypes())
    counts = Counter(example.calculation_type for example in parsed.examples)
    reasons.extend(
        TooFewExamples(calculation_type, counts[calculation_type])
        for calculation_type in dict.fromkeys(calculation_types)
        if counts[calculation_type] < MIN_EXAMPLES_PER_TYPE
    )
    return tuple(reasons)


def run_reference_suite(
    parsed: ParsedExamples, calculation_types: Sequence[str], registry: CalculatorRegistry, resolve: Resolver
) -> SuiteReport:
    """Проверяет действительность набора эталонов и прогоняет его принятые примеры.

    Недействительный набор даёт ``NO-GO`` с причинами, даже если каждый принятый
    пример прошёл (сценарий "Too few or incomplete examples"); принятые примеры всё
    равно прогоняются, чтобы отчёт показал и их.

    Args:
        parsed: итог ``parse_examples``.
        calculation_types: типы расчёта, которые набор обязан покрыть.
        registry: реестр типов расчёта.
        resolve: функция, которая даёт параметры примера.

    Returns:
        Отчёт набора.
    """
    report = run_suite(parsed.examples, registry, resolve)
    invalid = suite_invalidity(parsed, calculation_types)
    verdict: Verdict = "NO-GO" if invalid else report.verdict
    return SuiteReport(verdict=verdict, runs=report.runs, invalid=invalid)

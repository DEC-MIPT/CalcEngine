import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.core.exceptions import DECError
from app.engine.pipeline import calculate
from app.engine.registry import CalculatorRegistry
from app.schemas.calculation import CalculationResult, QuantityValue
from app.verification.runner import ExampleParameters, Verdict

CalculationVerdict = Literal["pass", "fail", "refused"]
"""Вердикт конверта, который хранит запись корпуса."""

VERDICT = "verdict"
"""Имя «величины» для отличия вердикта в отличиях и объявлениях."""

Value = QuantityValue | CalculationVerdict | None
"""Значение в отличии: выход с единицей, вердикт или ``None``, если выхода нет."""


class CorpusOutput(QuantityValue):
    """Сохранённый выход записи корпуса.

    Attributes:
        quantity: имя выходной величины.
    """

    quantity: str = Field(pattern=r"\S")


class CorpusEntry(BaseModel):
    """Запись замороженного регрессионного корпуса (`calculation-verification` "Regression corpus").

    Ключ записи — тип расчёта, входы и редакция; редакцию заменяет ``input_hash``, который
    покрывает идентичность набора параметров (design.md, решение 6).

    Attributes:
        entry_id: идентификатор записи.
        calculation_type: тип расчёта.
        inputs: входы со своими единицами.
        outputs: выходы конверта в порядке конверта.
        verdict: вердикт конверта.
        input_hash: ``input_hash`` конверта.
        engine_version: ``engine_version`` конверта.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    entry_id: str = Field(pattern=r"\S")
    calculation_type: str = Field(pattern=r"\S")
    inputs: dict[str, QuantityValue] = Field(min_length=1)
    outputs: tuple[CorpusOutput, ...]
    verdict: CalculationVerdict
    input_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    engine_version: str = Field(pattern=r"\S")


def freeze(
    entry_id: str, calculation_type: str, inputs: dict[str, QuantityValue], result: CalculationResult
) -> CorpusEntry:
    """Замораживает результат расчёта в запись корпуса (задача 3.2).

    Args:
        entry_id: идентификатор записи.
        calculation_type: тип расчёта, которым получен результат.
        inputs: входы, с которыми получен результат.
        result: результат чистой функции расчёта.

    Returns:
        Запись корпуса.
    """
    return CorpusEntry(
        entry_id=entry_id,
        calculation_type=calculation_type,
        inputs=inputs,
        outputs=tuple(
            CorpusOutput(quantity=output.quantity, value=output.value, unit=output.unit) for output in result.outputs
        ),
        verdict=result.verdict,
        input_hash=result.input_hash,
        engine_version=result.engine_version,
    )


class DeclaredDifference(BaseModel):
    """Отличие, объявленное в разделе "Declared result differences" `proposal.md` (решение 7).

    Attributes:
        entry_id: идентификатор записи корпуса.
        quantity: выходная величина или ``verdict``.
        old: значение в корпусе; ``None``, если выхода не было.
        new: значение после изменения; ``None``, если выхода больше нет.
        reason: причина отличия.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    entry_id: str = Field(pattern=r"\S")
    quantity: str = Field(pattern=r"\S")
    old: Value
    new: Value
    reason: str = Field(pattern=r"\S")


@dataclass(frozen=True)
class Difference:
    """Отличие пересчитанной записи от сохранённой по одной величине.

    Attributes:
        quantity: выходная величина или ``verdict``.
        old: сохранённое значение.
        new: пересчитанное значение.
    """

    quantity: str
    old: Value
    new: Value


EntryOutcome = Literal["unchanged", "declared", "undeclared", "error"]


@dataclass(frozen=True)
class EntryCheck:
    """Пересчёт одной записи корпуса.

    Attributes:
        entry_id: идентификатор записи.
        outcome: без отличий, все отличия объявлены, есть необъявленное, ошибка расчёта.
        differences: отличия по величинам; у каждого — объявлено ли оно.
        stored_engine_version: ``engine_version`` записи.
        recomputed_engine_version: ``engine_version`` пересчёта; ``None`` при ошибке.
        undeclared: отличия, которые не объявлены.
        error: имя класса ошибки, если пересчёт её бросил.
    """

    entry_id: str
    outcome: EntryOutcome
    differences: tuple[Difference, ...]
    stored_engine_version: str
    recomputed_engine_version: str | None
    undeclared: tuple[Difference, ...] = ()
    error: str | None = None


@dataclass(frozen=True)
class RegressionReport:
    """Итог пересчёта корпуса (задача 3.3).

    Attributes:
        verdict: ``NO-GO``, если у какой-либо записи есть необъявленное отличие или ошибка;
            тогда сборка падает.
        checks: пересчёты записей в порядке корпуса.
        unused_declarations: объявления, которым не нашлось отличия.
    """

    verdict: Verdict
    checks: tuple[EntryCheck, ...]
    unused_declarations: tuple[DeclaredDifference, ...]


CorpusResolver = Callable[[CorpusEntry], ExampleParameters]
"""Функция, которая даёт параметры записи корпуса (design.md, решение 14)."""


def _differences(entry: CorpusEntry, result: CalculationResult) -> tuple[Difference, ...]:
    stored = {output.quantity: QuantityValue(value=output.value, unit=output.unit) for output in entry.outputs}
    recomputed = {output.quantity: QuantityValue(value=output.value, unit=output.unit) for output in result.outputs}
    found = [
        Difference(quantity, stored.get(quantity), recomputed.get(quantity))
        for quantity in dict.fromkeys([*stored, *recomputed])
        if stored.get(quantity) != recomputed.get(quantity)
    ]
    if entry.verdict != result.verdict:
        found.append(Difference(VERDICT, entry.verdict, result.verdict))
    return tuple(found)


def _declared(entry_id: str, difference: Difference, declarations: Sequence[DeclaredDifference]) -> DeclaredDifference | None:
    return next(
        (
            declaration
            for declaration in declarations
            if (declaration.entry_id, declaration.quantity, declaration.old, declaration.new)
            == (entry_id, difference.quantity, difference.old, difference.new)
        ),
        None,
    )


def run_regression(
    entries: Sequence[CorpusEntry],
    registry: CalculatorRegistry,
    resolve: CorpusResolver,
    declarations: Sequence[DeclaredDifference] = (),
) -> RegressionReport:
    """Пересчитывает каждую запись корпуса и сравнивает выходы и вердикт (задача 3.3).

    Сравниваются только ``outputs`` (величина, значение, единица) и ``verdict``;
    ``result_id`` чистая функция не возвращает, а ``input_hash`` не сравнивается
    (требование "Regression corpus"). Отличие проходит, только если оно объявлено с той же
    записью, величиной, старым и новым значением (решение 7).

    Args:
        entries: записи корпуса.
        registry: реестр типов расчёта.
        resolve: функция, которая даёт параметры записи.
        declarations: объявленные отличия изменения.

    Returns:
        Итог пересчёта.
    """
    checks: list[EntryCheck] = []
    used: list[DeclaredDifference] = []
    for entry in entries:
        try:
            resolved = resolve(entry)
            result = calculate(
                registry.contract(entry.calculation_type),
                registry.get(entry.calculation_type),
                entry.inputs,
                resolved.parameters,
                method_range=resolved.method_range,
            )
        except DECError as error:
            checks.append(EntryCheck(entry.entry_id, "error", (), entry.engine_version, None, error=type(error).__name__))
            continue
        differences = _differences(entry, result)
        matched = [(difference, _declared(entry.entry_id, difference, declarations)) for difference in differences]
        used.extend(declaration for _, declaration in matched if declaration is not None)
        undeclared = tuple(difference for difference, declaration in matched if declaration is None)
        outcome: EntryOutcome = "unchanged" if not differences else "undeclared" if undeclared else "declared"
        checks.append(
            EntryCheck(entry.entry_id, outcome, differences, entry.engine_version, result.engine_version, undeclared)
        )
    verdict: Verdict = "GO" if all(check.outcome in ("unchanged", "declared") for check in checks) else "NO-GO"
    unused = tuple(declaration for declaration in declarations if declaration not in used)
    return RegressionReport(verdict=verdict, checks=tuple(checks), unused_declarations=unused)


_VERDICTS: dict[str, CalculationVerdict] = {"pass": "pass", "fail": "fail", "refused": "refused"}
_HEADING = re.compile(r"^#{2,}\s+Declared result differences\s*$")
_SEPARATOR = re.compile(r"^\|?\s*:?-{3,}")


def _value(cell: str) -> Value:
    text = cell.strip().strip("`")
    if text in ("", "-", "—"):
        return None
    if text in _VERDICTS:
        return _VERDICTS[text]
    number, _, unit = text.partition(" ")
    return QuantityValue(value=float(number), unit=unit.strip())


def parse_declared_differences(markdown: str) -> tuple[DeclaredDifference, ...]:
    """Читает раздел "Declared result differences" из текста `proposal.md` (решения 7 и 18).

    Раздел — заголовок второго или более глубокого уровня и таблица с колонками
    ``Entry | Quantity | Old | New | Reason``. Значение пишется как ``<число> <единица>``,
    как вердикт (``pass``, ``fail``, ``refused``) или как ``—``, если выхода нет. Раздел
    кончается на следующем заголовке. Без раздела объявлений нет.

    Args:
        markdown: текст `proposal.md`.

    Returns:
        Объявленные отличия в порядке таблицы.

    Raises:
        ValueError: если строка таблицы не из пяти ячеек или значение не читается.
    """
    declarations: list[DeclaredDifference] = []
    inside = False
    header_seen = False
    for number, line in enumerate(markdown.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            inside = bool(_HEADING.match(stripped))
            header_seen = False
            continue
        if not inside or not stripped.startswith("|"):
            continue
        if not header_seen:
            header_seen = True
            continue
        if _SEPARATOR.match(stripped):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 5:
            raise ValueError(f"line {number}: a declared difference has 5 cells, found {len(cells)}")
        entry_id, quantity, old, new, reason = cells
        try:
            declarations.append(
                DeclaredDifference(
                    entry_id=entry_id.strip("`"),
                    quantity=quantity.strip("`"),
                    old=_value(old),
                    new=_value(new),
                    reason=reason,
                )
            )
        except (ValueError, ValidationError) as error:
            raise ValueError(f"line {number}: the declared difference cannot be read") from error
    return tuple(declarations)

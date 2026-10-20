from collections.abc import Sequence
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal, localcontext
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.exceptions import ContractMetadataError, InputValidationError
from app.schemas.api import FieldError
from app.schemas.parameters import EngineerRule
from app.schemas.text import LocalizedText
from app.schemas.units import UNITS, UnitSymbol

UNVERIFIED: Literal["unverified"] = "unverified"


class QuantityDeclaration(BaseModel):
    """Величина типа расчёта и базовая единица, в которой она хранится.

    Подпись, обозначение, подсказка и признак целых значений описывают величину для
    человека и не влияют на расчёт, трассу, ``NormRef`` и ``input_hash``
    (``frontend-app`` design.md, решение 6). Регистрация типа требует ``label.ru`` и
    ``symbol`` у каждой величины.

    Attributes:
        name: имя величины.
        base_unit: базовая единица величины.
        label: подпись величины.
        symbol: обозначение величины в LaTeX.
        hint: пояснение для входа; у выхода его нет.
        whole_values_only: ``True`` для входа, который принимает только целые значения.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    base_unit: UnitSymbol
    label: LocalizedText | None = None
    symbol: str | None = None
    hint: LocalizedText | None = None
    whole_values_only: bool = False

    def described(self) -> tuple[LocalizedText, str]:
        """Возвращает подпись и обозначение величины, которые есть у зарегистрированного типа.

        Returns:
            Подпись и обозначение в LaTeX.

        Raises:
            ContractMetadataError: если подписи или обозначения нет.
        """
        if self.label is None or self.symbol is None:
            raise ContractMetadataError(f"quantity {self.name!r} has no label or symbol")
        return self.label, self.symbol

    def metadata_problems(self, role: str) -> tuple[str, ...]:
        """Перечисляет, чего не хватает величине из описания для человека.

        Args:
            role: ``input`` или ``output``; попадает в текст проблемы.

        Returns:
            По одной строке на проблему, с именем величины; пустой кортеж, если
            описание полное.
        """
        where = f"{role} {self.name!r}"
        problems = []
        if self.label is None or not self.label.ru.strip():
            problems.append(f"{where} has no label.ru")
        if self.symbol is None or not self.symbol.strip():
            problems.append(f"{where} has no symbol")
        if self.hint is not None and not self.hint.ru.strip():
            problems.append(f"{where} has a hint without hint.ru")
        return tuple(problems)


class QuantityValue(BaseModel):
    """Конечное значение с единицей из словаря единиц."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    value: float
    unit: UnitSymbol


class Substitution(QuantityValue):
    """Значение с единицей, подставленное вместо одного символа шага."""

    symbol: str = Field(min_length=1)


class NormRef(BaseModel):
    """Ссылка на одно место нормативного документа (design.md, раздел "NormRef").

    ``edition`` и ``clause`` — конкретная строка или зарезервированное значение
    ``unverified``; ``document`` всегда конкретный.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    document: str = Field(min_length=1)
    edition: Literal["unverified"] | str = Field(min_length=1)
    clause: Literal["unverified"] | str = Field(min_length=1)
    status: Literal["verified", "unverified"]
    provenance: Literal["human-verified", "machine-extracted"]

    @model_validator(mode="after")
    def _invariants_hold(self) -> "NormRef":
        if self.document == UNVERIFIED:
            raise ValueError("document must be a concrete designation, never 'unverified'")
        if self.status == "verified" and UNVERIFIED in (self.edition, self.clause):
            raise ValueError("a verified reference needs a concrete edition and clause")
        if self.provenance == "machine-extracted" and self.status == "verified":
            raise ValueError("a machine-extracted reference is always unverified")
        return self


NormRefs = Annotated[tuple[NormRef, ...], Field(min_length=1)]

Source = NormRefs | EngineerRule


class _TraceStep(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    step_id: str = Field(min_length=1)
    expression: str = Field(min_length=1)
    substitutions: tuple[Substitution, ...]
    result: QuantityValue
    norm_refs: NormRefs

    @property
    def verified(self) -> bool:
        """Шаг считается проверенным, только если проверена каждая его ссылка."""
        return all(reference.status == "verified" for reference in self.norm_refs)


class FormulaStep(_TraceStep):
    """Шаг, вычисляющий формулу; ``expression`` — LaTeX формулы."""

    kind: Literal["formula"] = "formula"


class TableStep(_TraceStep):
    """Шаг, берущий одно значение из таблицы нормы, выбранное по его подстановкам."""

    kind: Literal["table"] = "table"


Operator = Literal["le", "lt", "ge", "gt"]
"""Оператор сравнения шага проверки или ветви метода."""


class CheckStep(_TraceStep):
    """Сравнение ``result`` (левого значения) с ``right``."""

    kind: Literal["check"] = "check"
    operator: Operator
    right: QuantityValue
    passed: bool


Step = FormulaStep | TableStep | CheckStep
"""Любой шаг трассы."""

TraceStep = Annotated[Step, Field(discriminator="kind")]


def unverified_steps(trace: Sequence[Step]) -> int:
    """Считает шаги, которые не считаются проверенными; ни один шаг не пропускается.

    Args:
        trace: шаги трассы.

    Returns:
        Число непроверенных шагов.
    """
    return sum(not step.verified for step in trace)


def verdict_of(
    trace: Sequence[Step],
) -> tuple[Literal["pass", "fail"], str]:
    """Определяет вердикт выполненного расчёта и ``step_id`` решающей проверки.

    ``fail`` решает первая не пройденная проверка, ``pass`` — последняя проверка
    ("Automatic correctness validation").

    Args:
        trace: шаги трассы выполненного расчёта.

    Returns:
        Вердикт и ``step_id`` решающей проверки.

    Raises:
        ValueError: если в трассе нет ни одной проверки.
    """
    checks = [step for step in trace if isinstance(step, CheckStep)]
    if not checks:
        raise ValueError("a calculation that ran has at least one check step")
    failed = next((step for step in checks if not step.passed), None)
    if failed is not None:
        return "fail", failed.step_id
    return "pass", checks[-1].step_id


MAX_DECIMALS = 15
"""Предел числа знаков после запятой: столько значащих десятичных цифр гарантированно
держит float; это ограничение реализации, а не значение нормы."""


_ROUNDING_MODES = {"half_up": ROUND_HALF_UP, "half_even": ROUND_HALF_EVEN}


class RoundingRule(BaseModel):
    """Как округляется значение выхода; правило и его режим берутся из его источника."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    decimals: int = Field(ge=0, le=MAX_DECIMALS)
    mode: Literal["half_up", "half_even"]

    def apply(self, value: float) -> float:
        """Округляет значение выхода по этому правилу (``calculation-core-contract`` design.md, решение 14).

        Число с плавающей точкой превращается в самую короткую десятичную запись, которая
        читается обратно в то же значение, поэтому ``2.675`` округляется как ``2.675``, а
        не как его двоичный сосед. ``half_up`` округляет половину от нуля. Точность
        вычисления берётся по порядку значения и числу знаков, поэтому любое конечное
        значение округляется без ``decimal.InvalidOperation``.

        Args:
            value: неокруглённое значение.

        Returns:
            Округлённое значение.
        """
        exact = Decimal(repr(value))
        with localcontext() as context:
            context.prec = max(context.prec, exact.adjusted() + self.decimals + 2)
            return float(exact.quantize(Decimal(1).scaleb(-self.decimals), rounding=_ROUNDING_MODES[self.mode]))


class OutputDeclaration(QuantityDeclaration):
    """Выходная величина с правилом округления и источником этого правила."""

    rounding_rule: RoundingRule
    rounding_source: Source


class CalculationTypeContract(BaseModel):
    """Что реестр хранит о типе расчёта, кроме калькулятора.

    Базовые единицы и имена величин — данные, которые заполняет инженер, а не значения
    нормы. ``checks`` называет шаги проверки типа; нужен хотя бы один, чтобы у
    неотказного результата всегда была решающая проверка. Каждый выход объявляет своё
    правило округления и его источник, поэтому тип без них зарегистрировать нельзя.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(min_length=1)
    inputs: tuple[QuantityDeclaration, ...] = Field(min_length=1)
    outputs: tuple[OutputDeclaration, ...] = Field(min_length=1)
    checks: tuple[Annotated[str, Field(min_length=1)], ...] = Field(min_length=1)

    @model_validator(mode="after")
    def _quantity_names_are_unique(self) -> "CalculationTypeContract":
        for group in (self.inputs, self.outputs):
            names = [quantity.name for quantity in group]
            if len(names) != len(set(names)):
                raise ValueError("quantity names must be unique within inputs and within outputs")
        if len(self.checks) != len(set(self.checks)):
            raise ValueError("check names must be unique")
        if any(output.hint is not None or output.whole_values_only for output in self.outputs):
            raise ValueError("an output may not have a hint or whole_values_only")
        return self

    def metadata_problems(self) -> tuple[str, ...]:
        """Перечисляет проблемы описания величин типа для человека.

        Returns:
            Проблемы входов, затем выходов, в порядке контракта; пустой кортеж, если
            у каждой величины есть ``label.ru`` и ``symbol``.
        """
        return tuple(
            problem
            for role, group in (("input", self.inputs), ("output", self.outputs))
            for quantity in group
            for problem in quantity.metadata_problems(role)
        )


class _Bound(BaseModel):
    """Нижняя (``min``) или верхняя (``max``) граница одного входа в его базовой единице."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)

    quantity: str = Field(min_length=1)
    kind: Literal["min", "max"]
    value: float
    inclusive: bool


class MethodBound(_Bound):
    """Граница диапазона метода; её источник — всегда норма."""

    source: NormRefs


class ValidatedBound(_Bound):
    """Граница проверенного диапазона — из нормы или заданная инженером."""

    source: Source


def check_bounds(bounds: Sequence[MethodBound | ValidatedBound]) -> None:
    """Проверяет, что у каждой величины не больше одной нижней и одной верхней границы и диапазон не пуст.

    Args:
        bounds: границы одного диапазона.

    Raises:
        ValueError: если у величины две границы одного вида или её диапазон пуст.
    """
    sides: dict[tuple[str, str], MethodBound | ValidatedBound] = {}
    for bound in bounds:
        key = (bound.quantity, bound.kind)
        if key in sides:
            raise ValueError(f"quantity {bound.quantity!r} has two {bound.kind} bounds")
        sides[key] = bound
    for (quantity, kind), lower in sides.items():
        upper = sides.get((quantity, "max"))
        if kind != "min" or upper is None:
            continue
        empty = lower.value > upper.value or (
            lower.value == upper.value and not (lower.inclusive and upper.inclusive)
        )
        if empty:
            raise ValueError(f"the range of {quantity!r} is empty: its min is above its max")


class OutputValue(QuantityValue):
    """Выходная величина в базовой единице, округлённая по своему правилу."""

    quantity: str = Field(min_length=1)
    rounding_rule: RoundingRule
    rounding_source: Source


class ApplicabilityWarning(BaseModel):
    """Вход внутри диапазона метода, но вне проверенного диапазона."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    value: QuantityValue
    bound: ValidatedBound


class CheckReason(BaseModel):
    """Шаг проверки, решивший вердикт ``pass`` или ``fail``."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["check"] = "check"
    step_id: str = Field(min_length=1)


class BoundViolation(BaseModel):
    """Граница диапазона метода, по которой расчёт отказан."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["bound"] = "bound"
    value: QuantityValue
    bound: MethodBound


VerdictReason = Annotated[CheckReason | BoundViolation, Field(discriminator="kind")]


def ordered_sources(
    trace: Sequence[Step],
    refusal: BoundViolation | None,
    outputs: Sequence[OutputValue],
    warnings: Sequence[ApplicabilityWarning],
) -> tuple[tuple[NormRef, ...], tuple[EngineerRule, ...]]:
    """Перечисляет все использованные источники, каждый один раз, в порядке первого использования.

    Порядок: шаги трассы, затем граница отказа, затем источники округления в порядке
    ``outputs``, затем предупреждения (design.md, решение 17).

    Args:
        trace: шаги трассы.
        refusal: граница отказа или ``None``.
        outputs: выходы с источниками округления.
        warnings: предупреждения проверенного диапазона.

    Returns:
        Ссылки на нормы и правила инженера, без повторов.
    """
    sources: list[NormRefs | EngineerRule] = [step.norm_refs for step in trace]
    if refusal is not None:
        sources.append(refusal.bound.source)
    sources.extend(output.rounding_source for output in outputs)
    sources.extend(warning.bound.source for warning in warnings)
    norm_refs: list[NormRef] = []
    engineer_rules: list[EngineerRule] = []
    for source in sources:
        if isinstance(source, EngineerRule):
            if source not in engineer_rules:
                engineer_rules.append(source)
            continue
        for reference in source:
            if reference not in norm_refs:
                norm_refs.append(reference)
    return tuple(norm_refs), tuple(engineer_rules)


class CalculationResult(BaseModel):
    """Что возвращает чистая функция расчёта: конверт без ``result_id``."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    engine_version: str = Field(min_length=1)
    input_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    outputs: tuple[OutputValue, ...]
    norm_refs: tuple[NormRef, ...]
    engineer_rules: tuple[EngineerRule, ...]
    verdict: Literal["pass", "fail", "refused"]
    verdict_reason: VerdictReason
    warnings: tuple[ApplicabilityWarning, ...]
    trace: tuple[TraceStep, ...]
    unverified_step_count: int = Field(ge=0)

    @model_validator(mode="after")
    def _is_consistent(self) -> "CalculationResult":
        if self.verdict == "refused":
            self._check_refusal()
        else:
            self._check_deciding_step()
        self._check_sources_are_listed()
        if self.unverified_step_count != unverified_steps(self.trace):
            raise ValueError("unverified_step_count must equal the number of unverified steps")
        return self

    def _check_refusal(self) -> None:
        if self.verdict_reason.kind != "bound":
            raise ValueError("a refused calculation names the violated bound")
        if self.trace or self.outputs or self.unverified_step_count:
            raise ValueError(
                "a refused calculation has an empty trace and outputs and no unverified step"
            )

    def _check_deciding_step(self) -> None:
        reason = self.verdict_reason
        if reason.kind != "check":
            raise ValueError("a pass or fail verdict names its deciding check")
        checks = {step.step_id for step in self.trace if step.kind == "check"}
        if reason.step_id not in checks:
            raise ValueError(f"deciding check {reason.step_id!r} is not a check step of the trace")
        if (self.verdict, reason.step_id) != verdict_of(self.trace):
            raise ValueError(
                "the verdict and its deciding check do not follow from the check steps"
            )

    def _check_sources_are_listed(self) -> None:
        refusal = self.verdict_reason if isinstance(self.verdict_reason, BoundViolation) else None
        norm_refs, engineer_rules = ordered_sources(
            self.trace, refusal, self.outputs, self.warnings
        )
        if any(rule not in self.engineer_rules for rule in engineer_rules):
            raise ValueError("every engineer rule used is listed in engineer_rules")
        if any(reference not in self.norm_refs for reference in norm_refs):
            raise ValueError("every norm reference used is listed in norm_refs")
        if (self.norm_refs, self.engineer_rules) != (norm_refs, engineer_rules):
            raise ValueError(
                "norm_refs and engineer_rules list each source used once, in the order of first use"
            )


class ParameterSourceInfo(BaseModel):
    """Откуда пришли нормативные параметры расчёта (``interim-normatives-source`` design.md, решение 13).

    У каталога нет ни digest данных, ни профиля; у временного источника есть оба.

    Attributes:
        kind: ``catalog`` или ``interim``.
        data_sha256: SHA-256 данных временного источника; ``None`` у каталога.
        profile: профиль временного источника; ``None`` у каталога.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["catalog", "interim"]
    data_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    profile: Literal["strict", "draft"] | None = None

    @model_validator(mode="after")
    def _fields_of_the_kind(self) -> "ParameterSourceInfo":
        described = (self.data_sha256 is not None, self.profile is not None)
        if described != ((True, True) if self.kind == "interim" else (False, False)):
            raise ValueError("an interim source has a data digest and a profile, and the catalog has neither")
        return self


CATALOG_SOURCE = ParameterSourceInfo(kind="catalog")
"""Описание источника каталога норм."""


class ResultEnvelope(CalculationResult):
    """Результат расчёта с ``result_id``, который назначает слой сервисов."""

    result_id: UUID


class CalculationRequest(BaseModel):
    """Запрос на запуск типа расчёта, проверяемый до запуска движка.

    Схема отклоняет некорректный запрос, не конечное значение и единицу вне словаря;
    ``check_against`` отклоняет входы, не подходящие к контракту типа (``security``
    "Input validation", design.md, решения 12 и 13).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    calculation_type: str = Field(min_length=1)
    inputs: dict[str, QuantityValue]

    def check_against(self, contract: CalculationTypeContract) -> None:
        """Проверяет входы запроса по контракту типа расчёта.

        Собирает все неподходящие входы сразу, а не останавливается на первом
        (``calculation-api`` design.md, решение 5): пропущенные в порядке контракта,
        затем необъявленные и входы в единице другой размерности в порядке запроса.

        Args:
            contract: контракт типа расчёта из реестра.

        Raises:
            InputValidationError: если хотя бы один вход не подходит. Сообщение
                называет все такие входы, а ``fields`` содержит по записи на каждый
                с местом ``("body", "inputs", <имя входа>)``.
        """
        declared = {quantity.name: quantity.base_unit for quantity in contract.inputs}
        problems: list[tuple[str, str, str]] = []
        for name in declared:
            if name not in self.inputs:
                problems.append((name, f"{name!r} is missing", "Missing input."))
        for name, value in self.inputs.items():
            if name not in declared:
                problems.append((name, f"{name!r} is not declared", "Undeclared input."))
                continue
            given, base = UNITS[value.unit].dimension, UNITS[declared[name]].dimension
            if given != base:
                problems.append(
                    (
                        name,
                        f"{name!r} is in {value.unit!r} ({given}), not a unit of {base}",
                        f"Expected a unit of {base}.",
                    )
                )
        if problems:
            raise InputValidationError(
                f"inputs do not fit the declared inputs {sorted(declared)}: "
                + "; ".join(text for _, text, _ in problems),
                fields=tuple(
                    FieldError(location=("body", "inputs", name), message=message)
                    for name, _, message in problems
                ),
            )

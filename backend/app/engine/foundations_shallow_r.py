from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict

from app.core.exceptions import CalculationError
from app.engine.base import Calculator
from app.engine.pipeline import CalculatorOutput
from app.engine.registry import CalculatorRegistry
from app.engine.steps import (
    check_step,
    compare,
    confirm_selectors,
    formula_step,
    table_step,
)
from app.schemas.calculation import (
    CalculationTypeContract,
    NormRefs,
    OutputDeclaration,
    QuantityDeclaration,
    QuantityValue,
    RoundingRule,
    Source,
)
from app.schemas.resolved import Formula, TableValue, Threshold
from app.schemas.text import LocalizedText

NAME = "foundations_shallow_r"
CHECK = "p_le_R"

INPUTS = (
    QuantityDeclaration(
        name="b",
        base_unit="m",
        label=LocalizedText(ru="Ширина подошвы фундамента", en="Foundation base width"),
        symbol="b",
    ),
    QuantityDeclaration(
        name="d_1",
        base_unit="m",
        label=LocalizedText(ru="Приведённая глубина заложения", en="Reduced foundation depth"),
        symbol="d_1",
        hint=LocalizedText(
            ru="Значение, вычисленное отдельно; здесь оно вводится готовым",
            en="A value calculated separately and entered as is",
        ),
    ),
    QuantityDeclaration(
        name="d_b",
        base_unit="m",
        label=LocalizedText(ru="Глубина подвала", en="Basement depth"),
        symbol="d_b",
    ),
    QuantityDeclaration(
        name="gamma_II",
        base_unit="kN/m3",
        label=LocalizedText(ru="Удельный вес грунта ниже подошвы", en="Unit weight of soil below the base"),
        symbol=r"\gamma_{II}",
    ),
    QuantityDeclaration(
        name="gamma_II_prime",
        base_unit="kN/m3",
        label=LocalizedText(ru="Удельный вес грунта выше подошвы", en="Unit weight of soil above the base"),
        symbol=r"\gamma'_{II}",
    ),
    QuantityDeclaration(
        name="c_II",
        base_unit="kPa",
        label=LocalizedText(ru="Удельное сцепление грунта", en="Soil cohesion"),
        symbol="c_{II}",
    ),
    QuantityDeclaration(
        name="phi_II",
        base_unit="deg",
        label=LocalizedText(ru="Угол внутреннего трения грунта", en="Soil friction angle"),
        symbol=r"\varphi_{II}",
        hint=LocalizedText(
            ru="Целое число градусов: коэффициенты выбираются по строке таблицы",
            en="A whole number of degrees: the coefficients are chosen by a table row",
        ),
        whole_values_only=True,
    ),
    QuantityDeclaration(
        name="p",
        base_unit="kPa",
        label=LocalizedText(ru="Среднее давление под подошвой", en="Average pressure under the base"),
        symbol="p",
    ),
)


SELECTORS: Mapping[str, str] = {"m_gamma": "phi_II", "m_q": "phi_II", "m_c": "phi_II"}
"""Табличные параметры, которые метод выбирает по входу, и этот вход.

Коэффициенты M_γ, M_q, M_c принимаются по таблице 5.5 по φII (СП 22.13330.2016,
п. 5.6.7, unverified); остальные табличные параметры пилота ни по какому входу не
выбираются. Это строение метода, а не нормативное значение (``normative-catalog-backend``
design.md, решение 6).
"""

INPUT_SYMBOLS: Mapping[str, str] = {quantity.name: quantity.symbol for quantity in INPUTS if quantity.symbol}
"""Обозначение каждого входа пилота в LaTeX для выражений табличных шагов."""


class Parameters(BaseModel):
    """Разрешённые параметры расчётного сопротивления грунта R (СП 22.13330.2016, п. 5.6.7, unverified).

    Каждая формула, табличное значение и порог приходят из нормативного каталога со
    своим списком ``NormRef``; ни одно из них не записано в этом модуле (design.md,
    решение 11). ``d_1`` и ``d_b`` — входы: формула (5.8) и примечание 5 пункта в
    пилот не входят.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    gamma_c1: TableValue
    gamma_c2: TableValue
    k: TableValue
    m_gamma: TableValue
    m_q: TableValue
    m_c: TableValue
    k_z_threshold: Threshold
    k_z_below: Formula
    k_z_from: Formula
    r: Formula
    check_norm_refs: NormRefs


def _bind(values: dict[str, QuantityValue], symbol: str, value: QuantityValue) -> None:
    if symbol in values:
        raise CalculationError(f"symbol {symbol!r} is bound twice")
    values[symbol] = value


class FoundationsShallowR(Calculator[Mapping[str, QuantityValue], Parameters, CalculatorOutput]):
    """Порядок метода п. 5.6.7: коэффициенты, затем ``k_z``, затем R, затем p <= R."""

    def calculate(self, inputs: Mapping[str, QuantityValue], parameters: Parameters) -> CalculatorOutput:
        values = dict(inputs)
        entries = (
            ("gamma_c1", parameters.gamma_c1),
            ("gamma_c2", parameters.gamma_c2),
            ("k", parameters.k),
            ("m_gamma", parameters.m_gamma),
            ("m_q", parameters.m_q),
            ("m_c", parameters.m_c),
        )
        for name, entry in entries:
            confirm_selectors(entry, inputs, SELECTORS.get(name))
        tables = tuple(table_step(entry.symbol, entry, INPUT_SYMBOLS) for _, entry in entries)
        for step in tables:
            _bind(values, step.step_id, step.result)
        below = compare("k_z", inputs["b"], "lt", parameters.k_z_threshold.value)
        k_z_formula = parameters.k_z_below if below else parameters.k_z_from
        k_z = formula_step("k_z", k_z_formula, values)
        _bind(values, k_z_formula.result_symbol, k_z.result)
        r = formula_step("R", parameters.r, values)
        check = check_step(CHECK, ("p", inputs["p"]), "le", ("R", r.result), parameters.check_norm_refs)
        return CalculatorOutput(trace=(*tables, k_z, r, check), outputs={"R": r.result})


def contract(rounding_rule: RoundingRule, rounding_source: Source) -> CalculationTypeContract:
    """Строит контракт пилота.

    Округление R задаёт инженер в файле параметров.

    Args:
        rounding_rule: правило округления R.
        rounding_source: источник правила (``EngineerRule``).

    Returns:
        Контракт типа ``foundations_shallow_r``.
    """
    return CalculationTypeContract(
        name=NAME,
        inputs=INPUTS,
        outputs=(
            OutputDeclaration(
                name="R",
                base_unit="kPa",
                label=LocalizedText(ru="Расчётное сопротивление грунта", en="Design soil resistance"),
                symbol="R",
                rounding_rule=rounding_rule,
                rounding_source=rounding_source,
            ),
        ),
        checks=(CHECK,),
    )


def register(registry: CalculatorRegistry, rounding_rule: RoundingRule, rounding_source: Source) -> None:
    registry.register(
        contract(rounding_rule, rounding_source), FoundationsShallowR(), parameter_schema=Parameters
    )

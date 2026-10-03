from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict

from app.core.exceptions import CalculationError
from app.engine.base import Calculator
from app.engine.pipeline import CalculatorOutput
from app.engine.registry import CalculatorRegistry
from app.engine.steps import check_step, compare, formula_step, table_step
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

NAME = "foundations_shallow_r"
CHECK = "p_le_R"

INPUTS = (
    QuantityDeclaration(name="b", base_unit="m"),
    QuantityDeclaration(name="d_1", base_unit="m"),
    QuantityDeclaration(name="d_b", base_unit="m"),
    QuantityDeclaration(name="gamma_II", base_unit="kN/m3"),
    QuantityDeclaration(name="gamma_II_prime", base_unit="kN/m3"),
    QuantityDeclaration(name="c_II", base_unit="kPa"),
    QuantityDeclaration(name="phi_II", base_unit="deg"),
    QuantityDeclaration(name="p", base_unit="kPa"),
)


class Parameters(BaseModel):
    """The resolved parameters of the design soil resistance R (СП 22.13330.2016, clause 5.6.7, unverified).

    Every formula, table value and threshold comes from the normative catalog with its
    ``NormRef`` list; none of them is written in this module (design.md decision 11).
    ``d_1`` and ``d_b`` are inputs: formula (5.8) and note 5 of the clause are not part
    of the pilot.
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
    """The order of the method of clause 5.6.7: coefficients, then ``k_z``, then R, then p <= R."""

    def calculate(self, inputs: Mapping[str, QuantityValue], parameters: Parameters) -> CalculatorOutput:
        values = dict(inputs)
        conditions = tuple(
            table_step(entry.symbol, entry, {})
            for entry in (parameters.gamma_c1, parameters.gamma_c2, parameters.k)
        )
        bearing = tuple(
            table_step(entry.symbol, entry, {"phi_II": inputs["phi_II"]})
            for entry in (parameters.m_gamma, parameters.m_q, parameters.m_c)
        )
        for step in (*conditions, *bearing):
            _bind(values, step.step_id, step.result)
        below = compare("k_z", inputs["b"], "lt", parameters.k_z_threshold.value)
        k_z_formula = parameters.k_z_below if below else parameters.k_z_from
        k_z = formula_step("k_z", k_z_formula, values)
        _bind(values, k_z_formula.result_symbol, k_z.result)
        r = formula_step("R", parameters.r, values)
        check = check_step(CHECK, ("p", inputs["p"]), "le", ("R", r.result), parameters.check_norm_refs)
        return CalculatorOutput(trace=(*conditions, *bearing, k_z, r, check), outputs={"R": r.result})


def contract(rounding_rule: RoundingRule, rounding_source: Source) -> CalculationTypeContract:
    """The pilot's contract; the rounding of R is the engineer's, from the parameter file."""
    return CalculationTypeContract(
        name=NAME,
        inputs=INPUTS,
        outputs=(
            OutputDeclaration(
                name="R", base_unit="kPa", rounding_rule=rounding_rule, rounding_source=rounding_source
            ),
        ),
        checks=(CHECK,),
    )


def register(registry: CalculatorRegistry, rounding_rule: RoundingRule, rounding_source: Source) -> None:
    registry.register(contract(rounding_rule, rounding_source), FoundationsShallowR())

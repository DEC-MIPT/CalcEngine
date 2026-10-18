import ast
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy.orm import Session

from app.core.exceptions import CalculationError, ExpressionError, UnitError
from app.engine import foundations_shallow_r as pilot
from app.engine.pipeline import calculate
from app.engine.registry import CalculatorRegistry
from app.models.calculation_result import CalculationResultRow
from app.parameters.loader import load_parameters
from app.repositories.calculation_result import CalculationResultRepository
from app.schemas.calculation import (
    CalculationRequest,
    CalculationResult,
    NormRef,
    QuantityValue,
    RoundingRule,
)
from app.schemas.expression import parse_expression
from app.schemas.parameters import EngineerRule
from app.schemas.resolved import Formula, Selector, TableValue, Threshold
from app.services.calculation import CalculationService
from app.services.parameter_source import ResolvedParameters

BACKEND = Path(__file__).resolve().parents[1]
MODULE = BACKEND / "app" / "engine" / "foundations_shallow_r.py"

REF = NormRef(
    document="<NORM-DOC-PLACEHOLDER>",
    edition="unverified",
    clause="<CLAUSE-PLACEHOLDER>",
    status="unverified",
    provenance="machine-extracted",
)
RULE = EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>")
ROUNDING = RoundingRule(decimals=1, mode="half_up")


def sym(name: str) -> dict[str, Any]:
    return {"kind": "symbol", "name": name}


def num(value: float) -> dict[str, Any]:
    return {"kind": "number", "value": value}


def op(kind: str, *operands: dict[str, Any]) -> dict[str, Any]:
    tree = operands[0]
    for operand in operands[1:]:
        tree = {"kind": kind, "left": tree, "right": operand}
    return tree


def formula(latex: str, tree: dict[str, Any], result: str, units: dict[str, str]) -> Formula:
    return Formula(latex=latex, tree=parse_expression(tree), result_symbol=result, units=units, norm_refs=(REF,))


def entry(symbol: str, value: float, phi_ii: float | None = None) -> TableValue:
    selectors = () if phi_ii is None else (Selector(symbol="phi_II", value=QuantityValue(value=phi_ii, unit="deg")),)
    return TableValue(
        symbol=symbol, latex=symbol, value=QuantityValue(value=value, unit="1"), norm_refs=(REF,), selectors=selectors
    )


R_UNITS = {
    "gamma_c1": "1",
    "gamma_c2": "1",
    "k": "1",
    "M_gamma": "1",
    "M_q": "1",
    "M_c": "1",
    "k_z": "1",
    "b": "m",
    "d_1": "m",
    "d_b": "m",
    "gamma_II": "kN/m3",
    "gamma_II_prime": "kN/m3",
    "c_II": "kPa",
    "R": "kPa",
}

SYNTHETIC_R = op(
    "add",
    op("mul", sym("gamma_c1"), sym("c_II"), sym("M_c")),
    op("div", op("mul", sym("gamma_c2"), sym("M_q"), sym("d_1"), sym("gamma_II_prime")), sym("k")),
    op("mul", sym("M_gamma"), sym("k_z"), op("add", sym("b"), sym("d_b")), sym("gamma_II")),
)


def parameters(**changes: Any) -> pilot.Parameters:
    """Синтетические разрешённые параметры: ни формулы, ни коэффициента, ни порога нормы."""
    values: dict[str, Any] = {
        "gamma_c1": entry("gamma_c1", 2.0),
        "gamma_c2": entry("gamma_c2", 3.0),
        "k": entry("k", 4.0),
        "m_gamma": entry("M_gamma", 0.5, 20.0),
        "m_q": entry("M_q", 5.0, 20.0),
        "m_c": entry("M_c", 10.0, 20.0),
        "k_z_threshold": Threshold(latex="b_0", value=QuantityValue(value=5.0, unit="m"), norm_refs=(REF,)),
        "k_z_below": formula(r"k_z = \kappa", num(3.0), "k_z", {"k_z": "1"}),
        "k_z_from": formula(r"k_z = b / 4", op("div", sym("b"), num(4.0)), "k_z", {"b": "m", "k_z": "1"}),
        "r": formula(r"R = \mathrm{synthetic}", SYNTHETIC_R, "R", R_UNITS),
        "check_norm_refs": (REF,),
    }
    return pilot.Parameters(**(values | changes))


def inputs(b: float = 2.0, p: float = 100.0, b_unit: str = "m") -> dict[str, QuantityValue]:
    return {
        "b": QuantityValue(value=b, unit=b_unit),
        "d_1": QuantityValue(value=1.0, unit="m"),
        "d_b": QuantityValue(value=0.5, unit="m"),
        "gamma_II": QuantityValue(value=10.0, unit="kN/m3"),
        "gamma_II_prime": QuantityValue(value=20.0, unit="kN/m3"),
        "c_II": QuantityValue(value=3.0, unit="kPa"),
        "phi_II": QuantityValue(value=20.0, unit="deg"),
        "p": QuantityValue(value=p, unit="kPa"),
    }


def run(given: dict[str, QuantityValue] | None = None, resolved: pilot.Parameters | None = None) -> CalculationResult:
    return calculate(
        pilot.contract(ROUNDING, RULE),
        pilot.FoundationsShallowR(),
        inputs() if given is None else given,
        parameters() if resolved is None else resolved,
    )


def test_the_pilot_is_registered_with_its_check() -> None:
    registry = CalculatorRegistry()

    pilot.register(registry, ROUNDING, RULE)

    assert isinstance(registry.get(pilot.NAME), pilot.FoundationsShallowR)
    assert registry.contract(pilot.NAME).checks == (pilot.CHECK,)
    assert [quantity.name for quantity in registry.contract(pilot.NAME).outputs] == ["R"]


def test_the_rounding_of_r_comes_from_the_pilot_parameter_file() -> None:
    rounding = load_parameters(pilot.NAME, BACKEND / "params").rounding_rules["R"]

    output = pilot.contract(rounding.rule, rounding.source).outputs[0]

    assert (output.rounding_rule, output.rounding_source) == (rounding.rule, rounding.source)


def test_the_steps_run_in_the_order_of_the_method() -> None:
    result = run()

    assert [(step.kind, step.step_id) for step in result.trace] == [
        ("table", "gamma_c1"),
        ("table", "gamma_c2"),
        ("table", "k"),
        ("table", "M_gamma"),
        ("table", "M_q"),
        ("table", "M_c"),
        ("formula", "k_z"),
        ("formula", "R"),
        ("check", pilot.CHECK),
    ]
    assert [len(step.substitutions) for step in result.trace[:6]] == [0, 0, 0, 1, 1, 1]
    assert result.trace[3].substitutions[0].symbol == "phi_II"
    assert result.trace[3].expression == r"M_gamma = M_gamma\left(\varphi_{II}\right)"
    assert result.trace[0].expression == "gamma_c1"
    assert result.trace[7].result == QuantityValue(value=172.5, unit="kPa")
    assert result.trace[8].expression == r"p \le R"


def test_p_not_above_r_passes() -> None:
    result = run()

    assert (result.verdict, result.verdict_reason.kind) == ("pass", "check")
    assert [(output.quantity, output.value, output.unit) for output in result.outputs] == [("R", 172.5, "kPa")]
    assert result.unverified_step_count == 9


def test_p_above_r_fails_on_the_check() -> None:
    result = run(inputs(p=200.0))

    assert result.verdict == "fail"
    assert result.verdict_reason.model_dump() == {"kind": "check", "step_id": pilot.CHECK}


@pytest.mark.parametrize(
    ("b", "branch", "k_z", "r"),
    [(2.0, "k_z_below", 3.0, 172.5), (5.0, "k_z_from", 1.25, 169.4), (8.0, "k_z_from", 2.0, 220.0)],
    ids=["below", "at-threshold", "above"],
)
def test_the_threshold_chooses_the_k_z_formula(b: float, branch: str, k_z: float, r: float) -> None:
    result = run(inputs(b=b))

    step = result.trace[6]
    assert step.expression == getattr(parameters(), branch).latex
    assert step.result.value == k_z
    assert result.outputs[0].value == r


def test_the_threshold_compares_in_the_unit_of_b() -> None:
    other = Threshold(latex="b_0", value=QuantityValue(value=500.0, unit="cm"), norm_refs=(REF,))

    with pytest.raises(UnitError, match="'k_z' compares 'm' with 'cm'"):
        run(resolved=parameters(k_z_threshold=other))


def test_a_table_symbol_that_clashes_with_an_input_fails() -> None:
    with pytest.raises(CalculationError, match="symbol 'b' is bound twice"):
        run(resolved=parameters(k=entry("b", 4.0)))


def test_a_formula_symbol_without_a_value_fails_naming_it() -> None:
    unknown = formula("R = x", sym("x"), "R", {"x": "kPa", "R": "kPa"})

    with pytest.raises(ExpressionError, match="'x'"):
        run(resolved=parameters(r=unknown))


def test_the_same_inputs_and_parameters_give_the_same_result() -> None:
    first = run(inputs(b=2000.0, b_unit="mm"))
    second = run(inputs(b=2.0), pilot.Parameters.model_validate(parameters().model_dump()))

    assert first == second
    assert first.model_dump_json() == second.model_dump_json()


class FixedSource:
    def resolve(self, calculation_type: str, given: Mapping[str, QuantityValue]) -> ResolvedParameters:
        return ResolvedParameters(parameters=parameters(), method_range=())


def test_the_service_runs_the_registered_pilot(sqlite_session: Session) -> None:
    registry = CalculatorRegistry()
    pilot.register(registry, ROUNDING, RULE)
    request = CalculationRequest(calculation_type=pilot.NAME, inputs=inputs())
    service = CalculationService(
        registry,
        sources={pilot.NAME: FixedSource()},
        results=CalculationResultRepository(sqlite_session),
    )

    envelope = service.submit(request)

    assert envelope.verdict == "pass"
    assert envelope.outputs[0].value == 172.5


def test_a_heading_that_differs_from_phi_ii_stops_the_pilot() -> None:
    with pytest.raises(CalculationError, match="'M_q': selector 'phi_II' differs from the input"):
        run(resolved=parameters(m_q=entry("M_q", 5.0, 30.0)))


def test_a_heading_on_a_value_the_method_does_not_select_stops_the_pilot() -> None:
    soil = Selector(symbol="soil", value=QuantityValue(value=1.0, unit="1"))
    gamma_c1 = parameters().gamma_c1.model_copy(update={"selectors": (soil,)})

    with pytest.raises(CalculationError, match="'gamma_c1': selectors differ from the method's"):
        run(resolved=parameters(gamma_c1=gamma_c1))


@pytest.mark.parametrize("name", ["m_gamma", "m_q", "m_c"])
def test_a_coefficient_without_its_phi_ii_heading_stops_the_pilot(name: str) -> None:
    unselected = getattr(parameters(), name).model_copy(update={"selectors": ()})

    with pytest.raises(CalculationError, match="selectors differ from the method's"):
        run(resolved=parameters(**{name: unselected}))


def test_the_pilot_selects_by_phi_ii_exactly_the_table_coefficients() -> None:
    tables = [name for name, field in pilot.Parameters.model_fields.items() if field.annotation is TableValue]

    assert set(pilot.SELECTORS) <= set(tables)
    assert set(pilot.SELECTORS.values()) <= {quantity.name for quantity in pilot.INPUTS}
    assert pilot.SELECTORS == {"m_gamma": "phi_II", "m_q": "phi_II", "m_c": "phi_II"}


def test_every_input_of_the_pilot_has_its_latex_symbol_for_the_table_steps() -> None:
    assert pilot.INPUT_SYMBOLS == {quantity.name: quantity.symbol for quantity in pilot.INPUTS}
    assert pilot.INPUT_SYMBOLS["phi_II"] == r"\varphi_{II}"


def test_headings_in_radians_are_confirmed_for_phi_ii_given_in_radians() -> None:
    in_radians = Selector(symbol="phi_II", value=QuantityValue(value=0.3, unit="rad"))
    selected = {
        name: getattr(parameters(), name).model_copy(update={"selectors": (in_radians,)})
        for name in ("m_gamma", "m_q", "m_c")
    }
    given = inputs() | {"phi_II": QuantityValue(value=0.3, unit="rad")}

    result = run(given, parameters(**selected))

    assert [(s.symbol, s.value, s.unit) for s in result.trace[4].substitutions] == [("phi_II", 0.3, "rad")]


class MismatchedSource:
    def resolve(self, calculation_type: str, given: Mapping[str, QuantityValue]) -> ResolvedParameters:
        return ResolvedParameters(parameters=parameters(m_c=entry("M_c", 10.0, 10.0)), method_range=())


def test_a_mismatched_heading_stores_nothing(sqlite_session: Session) -> None:
    registry = CalculatorRegistry()
    pilot.register(registry, ROUNDING, RULE)
    service = CalculationService(
        registry,
        sources={pilot.NAME: MismatchedSource()},
        results=CalculationResultRepository(sqlite_session),
    )

    with pytest.raises(CalculationError, match="'M_c'"):
        service.submit(CalculationRequest(calculation_type=pilot.NAME, inputs=inputs()))

    assert sqlite_session.query(CalculationResultRow).count() == 0


def numeric_literals(source: str) -> list[object]:
    """Числовые константы модуля, кроме ``0`` и ``1``; булевы значения здесь не считаются числами."""
    return [
        node.value
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Constant)
        and isinstance(node.value, int | float | complex)
        and not isinstance(node.value, bool)
        and node.value not in (0, 1)
    ]


ALLOWED_IMPORTS = ("collections.abc", "pydantic", "app.core.exceptions", "app.engine", "app.schemas")


def imported_modules(source: str) -> list[str]:
    found: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            found.append(node.module or "")
    return found


def test_the_pilot_module_has_no_numeric_literal_other_than_0_and_1() -> None:
    assert numeric_literals(MODULE.read_text(encoding="utf-8")) == []


def test_the_literal_scan_finds_a_constant() -> None:
    found = numeric_literals("a = 0\nb = 1.0\nc = True\nd = 2 * x + 0.2\ne = 1j")

    assert set(found) == {2, 0.2, 1j} and len(found) == 3


def is_allowed(module: str) -> bool:
    return any(module == prefix or module.startswith(f"{prefix}.") for prefix in ALLOWED_IMPORTS)


def test_the_pilot_module_imports_nothing_that_performs_io() -> None:
    source = MODULE.read_text(encoding="utf-8")

    modules = imported_modules(source)

    assert modules
    assert [module for module in modules if not is_allowed(module)] == []
    assert "open" not in {node.id for node in ast.walk(ast.parse(source)) if isinstance(node, ast.Name)}


def test_the_import_scan_finds_every_import() -> None:
    modules = imported_modules("import os, socket\nfrom pathlib import Path\nfrom . import x\nfrom app.db import s")

    assert modules == ["os", "socket", "pathlib", "", "app.db"]
    assert not any(is_allowed(module) for module in modules)
    assert is_allowed("app.schemas.resolved") and not is_allowed("app.schemasx")


GOLDEN = Path(__file__).parent / "fixtures" / "pilot_envelope_before_metadata.json"
GOLDEN_CASES = json.loads(GOLDEN.read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", sorted(GOLDEN_CASES))
def test_the_metadata_changes_no_result_trace_norm_reference_or_hash(case: str) -> None:
    recorded = GOLDEN_CASES[case]
    given = {name: QuantityValue(**value) for name, value in recorded["inputs"].items()}

    assert run(given).model_dump(mode="json") == recorded["result"]

import pytest
from test_engine_foundations_shallow_r import ROUNDING, RULE
from test_reporting_model import envelope

from app.engine import foundations_shallow_r as pilot
from app.reporting.formula import Math
from app.reporting.symbols import equation, named, step_symbol, symbol_table
from app.schemas.calculation import CheckStep, FormulaStep, QuantityValue, TableStep


def steps() -> dict[str, FormulaStep | TableStep | CheckStep]:
    return {step.step_id: step for step in envelope().trace}


@pytest.mark.parametrize(
    ("expression", "symbol"),
    [
        (r"M_q = M_q\left(\varphi_{II}\right)", "M_q"),
        (r"R_{x=1} = 2", "R_{x=1}"),
        (r"\gamma_{c1}", r"\gamma_{c1}"),
    ],
)
def test_a_table_step_is_named_by_its_left_side_or_its_whole_expression(expression: str, symbol: str) -> None:
    step = steps()["M_q"].model_copy(update={"expression": expression})

    assert step_symbol(step) == symbol


def test_a_check_step_is_named_by_its_whole_expression() -> None:
    assert step_symbol(steps()["p_le_R"]) == r"p \le R"


@pytest.mark.parametrize("expression", [r"\kappa", " = 1"])
def test_a_formula_without_a_left_side_has_no_symbol(expression: str) -> None:
    assert step_symbol(steps()["k_z"].model_copy(update={"expression": expression})) is None


def test_the_contract_symbols_replace_the_step_symbols() -> None:
    full = pilot.contract(ROUNDING, RULE)
    unnamed = full.inputs[0].model_copy(update={"symbol": None})
    contract = full.model_copy(update={"inputs": (unnamed, *full.inputs[1:])})
    trace = envelope().trace
    renamed = [step.model_copy(update={"expression": r"\phi = 1"}) if step.step_id == "R" else step for step in trace]

    table = symbol_table(contract, renamed)

    assert table["R"] == "R"
    assert table["phi_II"] == r"\varphi_{II}"
    assert table["p_le_R"] == r"p \le R"
    assert table["M_gamma"] == "M_gamma"
    assert unnamed.name not in table


def test_a_name_without_a_symbol_prints_as_text() -> None:
    value = QuantityValue(value=2.0, unit="m")

    assert named("b", {"b": "b"}) == Math("b")
    assert named("b", {}) == "b"
    assert equation("b", value, {"b": "b"}) == (Math(r"b = 2\ \text{м}"),)
    assert equation("b", value, {}) == ("b = ", Math(r"2\ \text{м}"))

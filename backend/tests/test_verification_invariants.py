from types import SimpleNamespace
from typing import Any

import conftest
import pytest
from pydantic import ValidationError
from test_verification_runner import CONTRACT, TYPE

from app.verification.invariants import (
    DETERMINISM,
    UNIT_CHANGE,
    InputRange,
    Invariant,
    InvariantPlan,
    plan_problems,
    shared_invariants,
)

RANGES = (
    InputRange(quantity="b", lower=1.0, upper=40.0, unit="m"),
    InputRange(quantity="q", lower=0.5, upper=2.0, unit="1"),
)
SPECIFIC = Invariant(identifier="y-grows-with-b", statement="<STATEMENT>", quantities=("b", "y"))


def plan(**changes: Any) -> InvariantPlan:
    data: dict[str, Any] = {
        "calculation_type": TYPE,
        "valid_range": RANGES,
        "invariants": (*shared_invariants(CONTRACT), SPECIFIC),
    }
    return InvariantPlan.model_validate(data | changes)


def test_a_plan_with_a_range_per_input_and_the_shared_invariants_fits_its_contract() -> None:
    assert plan_problems(plan(), CONTRACT) == ()


def test_the_shared_invariants_name_every_quantity_of_the_type() -> None:
    determinism, unit_change = shared_invariants(CONTRACT)

    assert (determinism.identifier, unit_change.identifier) == (DETERMINISM, UNIT_CHANGE)
    assert determinism.quantities == unit_change.quantities == ("b", "q", "y")
    assert determinism.statement and unit_change.statement


def test_an_invariant_keeps_its_identifier_statement_and_quantities() -> None:
    assert (SPECIFIC.identifier, SPECIFIC.statement, SPECIFIC.quantities) == ("y-grows-with-b", "<STATEMENT>", ("b", "y"))


@pytest.mark.parametrize(
    "data",
    [
        {"identifier": " ", "statement": "s", "quantities": ("b",)},
        {"identifier": "i", "statement": "", "quantities": ("b",)},
        {"identifier": "i", "statement": "s", "quantities": ()},
        {"identifier": "i", "statement": "s", "quantities": ("b",), "extra": 1},
    ],
    ids=["blank identifier", "empty statement", "no quantities", "undeclared field"],
)
def test_an_incomplete_invariant_is_rejected(data: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        Invariant.model_validate(data)


@pytest.mark.parametrize(
    "data",
    [
        {"quantity": "b", "lower": 2.0, "upper": 1.0, "unit": "m"},
        {"quantity": "b", "lower": 1.0, "upper": float("inf"), "unit": "m"},
        {"quantity": "b", "lower": float("nan"), "upper": 1.0, "unit": "m"},
        {"quantity": "b", "lower": 1.0, "upper": 2.0, "unit": "furlong"},
        {"quantity": "", "lower": 1.0, "upper": 2.0, "unit": "m"},
    ],
    ids=["reversed", "infinite", "nan", "unit outside the vocabulary", "no quantity"],
)
def test_an_invalid_input_range_is_rejected(data: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        InputRange.model_validate(data)


def test_a_range_may_be_a_single_value() -> None:
    assert InputRange(quantity="b", lower=3.0, upper=3.0, unit="m").lower == 3.0


@pytest.mark.parametrize(
    "changes",
    [
        {"valid_range": (*RANGES, InputRange(quantity="b", lower=2.0, upper=3.0, unit="m"))},
        {"invariants": (SPECIFIC, SPECIFIC)},
        {"valid_range": ()},
        {"invariants": ()},
        {"calculation_type": " "},
    ],
    ids=["input ranged twice", "identifier repeated", "no ranges", "no invariants", "blank type"],
)
def test_an_inconsistent_plan_is_rejected(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        plan(**changes)


@pytest.mark.parametrize(
    ("changes", "problem"),
    [
        ({"calculation_type": "other_type"}, f"plan is for 'other_type', contract is '{TYPE}'"),
        ({"valid_range": RANGES[:1]}, "input 'q' has no range"),
        (
            {"valid_range": (*RANGES, InputRange(quantity="z", lower=0.0, upper=1.0, unit="m"))},
            "range of 'z' names no input",
        ),
        (
            {"valid_range": (RANGES[0], InputRange(quantity="q", lower=0.0, upper=1.0, unit="m"))},
            "range of 'q' is in a unit of another dimension",
        ),
        (
            {"valid_range": (InputRange(quantity="b", lower=1.0, upper=1e306, unit="mm"), RANGES[1])},
            None,
        ),
        ({"invariants": (shared_invariants(CONTRACT)[0], SPECIFIC)}, f"shared invariant {UNIT_CHANGE!r} is missing"),
        ({"invariants": (shared_invariants(CONTRACT)[1],)}, f"shared invariant {DETERMINISM!r} is missing"),
        (
            {"invariants": (*shared_invariants(CONTRACT), SPECIFIC.model_copy(update={"quantities": ("b", "w")}))},
            "invariant 'y-grows-with-b' names unknown quantity 'w'",
        ),
    ],
    ids=[
        "other type",
        "input without a range",
        "range of no input",
        "range in another dimension",
        "large range that converts",
        "unit change missing",
        "determinism missing",
        "unknown quantity",
    ],
)
def test_a_plan_that_does_not_fit_its_contract_is_named(changes: dict[str, Any], problem: str | None) -> None:
    problems = plan_problems(plan(**changes), CONTRACT)

    assert problems == (() if problem is None else (problem,))


def test_a_range_that_overflows_in_the_base_unit_is_named() -> None:
    contract = CONTRACT.model_copy(
        update={"inputs": (CONTRACT.inputs[0].model_copy(update={"base_unit": "mm"}), CONTRACT.inputs[1])}
    )
    huge = InputRange(quantity="b", lower=1.0, upper=1e306, unit="m")

    assert plan_problems(plan(valid_range=(huge, RANGES[1])), contract) == ("range of 'b' overflows in the base unit",)


def test_a_seed_is_chosen_for_the_run_when_none_is_given() -> None:
    config = SimpleNamespace(option=SimpleNamespace(hypothesis_seed=None))
    config.getoption = lambda name: getattr(config.option, name)

    conftest.pytest_configure(config)  # type: ignore[arg-type]

    assert isinstance(config.option.hypothesis_seed, int)
    assert 0 <= config.option.hypothesis_seed < 2**32


def test_a_given_seed_is_kept_and_reported() -> None:
    config = SimpleNamespace(option=SimpleNamespace(hypothesis_seed=777))
    config.getoption = lambda name: getattr(config.option, name)

    conftest.pytest_configure(config)  # type: ignore[arg-type]

    assert config.option.hypothesis_seed == 777
    assert conftest.pytest_report_header(config) == "hypothesis seed: 777"  # type: ignore[arg-type]


def test_this_run_has_its_seed_in_the_report(pytestconfig: pytest.Config) -> None:
    seed = pytestconfig.getoption("hypothesis_seed")

    assert seed is not None
    assert conftest.pytest_report_header(pytestconfig) == f"hypothesis seed: {seed}"

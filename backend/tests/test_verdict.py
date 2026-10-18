from typing import Any

import pytest
from pydantic import ValidationError

from app.engine.steps import check_step
from app.schemas.calculation import (
    CalculationResult,
    CalculationTypeContract,
    CheckReason,
    CheckStep,
    NormRef,
    OutputDeclaration,
    QuantityDeclaration,
    QuantityValue,
    RoundingRule,
    verdict_of,
)
from app.schemas.text import LocalizedText

REF = NormRef(
    document="<NORM-DOC-PLACEHOLDER>",
    edition="unverified",
    clause="<CLAUSE-CHECK>",
    status="unverified",
    provenance="machine-extracted",
)


def check(step_id: str, passed: bool) -> CheckStep:
    left = QuantityValue(value=4.0 if passed else 6.0, unit="kPa")
    right = QuantityValue(value=5.0, unit="kPa")
    return check_step(step_id, ("p", left), "le", ("R", right), (REF,))


def contract(**changes: Any) -> CalculationTypeContract:
    fields: dict[str, Any] = {
        "name": "t",
        "inputs": (QuantityDeclaration(name="x", label=LocalizedText(ru="x"), symbol="x", base_unit="m"),),
        "outputs": (
            OutputDeclaration(
                name="y",
                label=LocalizedText(ru="y"),
                symbol="y",
                base_unit="m",
                rounding_rule=RoundingRule(decimals=2, mode="half_up"),
                rounding_source=(REF,),
            ),
        ),
        "checks": ("c1", "c2"),
    }
    return CalculationTypeContract.model_validate(fields | changes)


def result(trace: tuple[CheckStep, ...], verdict: str, step_id: str) -> CalculationResult:
    return CalculationResult.model_validate(
        {
            "engine_version": "0.1.0",
            "input_hash": "0" * 64,
            "outputs": (),
            "norm_refs": (REF,),
            "engineer_rules": (),
            "verdict": verdict,
            "verdict_reason": CheckReason(step_id=step_id),
            "warnings": (),
            "trace": trace,
            "unverified_step_count": len(trace),
        }
    )


def test_a_contract_without_a_check_cannot_be_registered() -> None:
    with pytest.raises(ValidationError):
        contract(checks=())
    with pytest.raises(ValidationError):
        contract(checks=None)


def test_check_names_are_unique_and_not_empty() -> None:
    with pytest.raises(ValidationError, match="check names must be unique"):
        contract(checks=("c1", "c1"))
    with pytest.raises(ValidationError):
        contract(checks=("",))


def test_the_contract_holds_its_checks() -> None:
    assert contract().checks == ("c1", "c2")


def test_two_checks_with_the_second_failed_give_fail_naming_the_second() -> None:
    assert verdict_of((check("c1", True), check("c2", False))) == ("fail", "c2")


def test_two_passed_checks_give_pass_naming_the_last() -> None:
    assert verdict_of((check("c1", True), check("c2", True))) == ("pass", "c2")


def test_the_first_failed_check_decides() -> None:
    assert verdict_of((check("c1", False), check("c2", False))) == ("fail", "c1")


def test_a_trace_without_a_check_has_no_verdict() -> None:
    with pytest.raises(ValueError, match="at least one check step"):
        verdict_of(())


@pytest.mark.parametrize(
    "passed,verdict,step_id",
    [((True, False), "fail", "c2"), ((True, True), "pass", "c2"), ((False, True), "fail", "c1")],
)
def test_an_envelope_follows_the_verdict_rule(
    passed: tuple[bool, bool], verdict: str, step_id: str
) -> None:
    trace = (check("c1", passed[0]), check("c2", passed[1]))

    assert result(trace, verdict, step_id).verdict == verdict


@pytest.mark.parametrize(
    "passed,verdict,step_id",
    [
        ((True, False), "pass", "c2"),
        ((True, False), "fail", "c1"),
        ((True, True), "pass", "c1"),
        ((True, True), "fail", "c2"),
    ],
    ids=["pass-with-a-failed-check", "wrong-failed-check", "not-the-last-check", "fail-when-all-passed"],
)
def test_an_envelope_against_the_verdict_rule_is_rejected(
    passed: tuple[bool, bool], verdict: str, step_id: str
) -> None:
    trace = (check("c1", passed[0]), check("c2", passed[1]))

    with pytest.raises(ValidationError, match="do not follow from the check steps"):
        result(trace, verdict, step_id)

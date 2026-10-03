from typing import Any
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.calculation import (
    ApplicabilityWarning,
    BoundViolation,
    CalculationResult,
    CheckReason,
    CheckStep,
    FormulaStep,
    MethodBound,
    NormRef,
    OutputValue,
    QuantityValue,
    ResultEnvelope,
    RoundingRule,
    ValidatedBound,
)
from app.schemas.parameters import EngineerRule

HASH = "0" * 64


def ref(clause: str) -> NormRef:
    return NormRef(
        document="<NORM-DOC-PLACEHOLDER>",
        edition="unverified",
        clause=clause,
        status="unverified",
        provenance="machine-extracted",
    )


STEP_REF = ref("<CLAUSE-STEP>")
CHECK_REF = ref("<CLAUSE-CHECK>")
BOUND_REF = ref("<CLAUSE-BOUND>")
WARNING_REF = ref("<CLAUSE-WARNING>")
RULE = EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>")


def formula_step() -> FormulaStep:
    return FormulaStep(
        step_id="y",
        expression=r"y = 2 x",
        substitutions=(),
        result=QuantityValue(value=4.0, unit="m"),
        norm_refs=(STEP_REF,),
    )


def check_step() -> CheckStep:
    return CheckStep(
        step_id="check",
        expression=r"y \le y_{max}",
        substitutions=(),
        result=QuantityValue(value=4.0, unit="m"),
        norm_refs=(CHECK_REF,),
        operator="le",
        right=QuantityValue(value=5.0, unit="m"),
        passed=True,
    )


def output(source: Any = RULE) -> OutputValue:
    return OutputValue(
        quantity="y",
        value=4.0,
        unit="m",
        rounding_rule=RoundingRule(decimals=2, mode="half_up"),
        rounding_source=source,
    )


def method_bound() -> MethodBound:
    return MethodBound(quantity="x", kind="max", value=10.0, inclusive=True, source=(BOUND_REF,))


def warning(source: Any) -> ApplicabilityWarning:
    return ApplicabilityWarning(
        value=QuantityValue(value=9.0, unit="m"),
        bound=ValidatedBound(quantity="x", kind="max", value=8.0, inclusive=True, source=source),
    )


def completed(**changes: Any) -> dict[str, Any]:
    fields: dict[str, Any] = {
        "engine_version": "0.1.0",
        "input_hash": HASH,
        "outputs": (output(),),
        "norm_refs": (STEP_REF, CHECK_REF),
        "engineer_rules": (RULE,),
        "verdict": "pass",
        "verdict_reason": CheckReason(step_id="check"),
        "warnings": (),
        "trace": (formula_step(), check_step()),
        "unverified_step_count": 2,
    }
    return fields | changes


def refused(**changes: Any) -> dict[str, Any]:
    fields: dict[str, Any] = {
        "engine_version": "0.1.0",
        "input_hash": HASH,
        "outputs": (),
        "norm_refs": (BOUND_REF, WARNING_REF),
        "engineer_rules": (RULE,),
        "verdict": "refused",
        "verdict_reason": BoundViolation(
            value=QuantityValue(value=12.0, unit="m"), bound=method_bound()
        ),
        "warnings": (warning((WARNING_REF,)), warning(RULE)),
        "trace": (),
        "unverified_step_count": 0,
    }
    return fields | changes


def has_none(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, dict):
        return any(has_none(item) for item in value.values())
    if isinstance(value, list | tuple):
        return any(has_none(item) for item in value)
    return False


@pytest.mark.parametrize("fields", [completed(), refused()], ids=["completed", "refused"])
def test_no_field_of_an_envelope_is_null(fields: dict[str, Any]) -> None:
    envelope = ResultEnvelope(result_id=uuid4(), **fields)

    assert not has_none(envelope.model_dump())


@pytest.mark.parametrize("field", list(completed()))
def test_a_null_field_is_rejected(field: str) -> None:
    with pytest.raises(ValidationError):
        CalculationResult(**completed(**{field: None}))


def test_the_refused_envelope() -> None:
    result = CalculationResult(**refused())

    assert result.trace == ()
    assert result.outputs == ()
    assert result.unverified_step_count == 0
    assert isinstance(result.verdict_reason, BoundViolation)
    assert result.verdict_reason.bound.source == (BOUND_REF,)
    assert set(result.norm_refs) >= {BOUND_REF, WARNING_REF}
    assert RULE in result.engineer_rules


@pytest.mark.parametrize(
    "changes",
    [
        {"trace": (formula_step(),), "norm_refs": (BOUND_REF, WARNING_REF, STEP_REF)},
        {"outputs": (output(),)},
        {"unverified_step_count": 1},
    ],
    ids=["trace", "outputs", "unverified"],
)
def test_a_refused_calculation_has_no_trace_outputs_or_unverified_steps(
    changes: dict[str, Any],
) -> None:
    with pytest.raises(ValidationError, match="refused calculation has an empty trace"):
        CalculationResult(**refused(**changes))


def test_a_refusal_names_the_violated_bound() -> None:
    with pytest.raises(ValidationError, match="names the violated bound"):
        CalculationResult(**refused(verdict_reason=CheckReason(step_id="check")))


@pytest.mark.parametrize("verdict", ["pass", "fail"])
def test_a_pass_or_fail_names_its_deciding_check(verdict: str) -> None:
    reason = BoundViolation(value=QuantityValue(value=12.0, unit="m"), bound=method_bound())

    with pytest.raises(ValidationError, match="names its deciding check"):
        CalculationResult(
            **completed(
                verdict=verdict,
                verdict_reason=reason,
                norm_refs=(STEP_REF, CHECK_REF, BOUND_REF),
            )
        )


@pytest.mark.parametrize("step_id", ["missing", "y"], ids=["absent", "not-a-check"])
def test_the_deciding_check_is_a_check_step_of_the_trace(step_id: str) -> None:
    with pytest.raises(ValidationError, match="is not a check step"):
        CalculationResult(**completed(verdict_reason=CheckReason(step_id=step_id)))


@pytest.mark.parametrize(
    "norm_refs",
    [(WARNING_REF,), (BOUND_REF,)],
    ids=["bound-missing", "warning-missing"],
)
def test_a_refusal_lists_the_bound_and_warning_references(norm_refs: tuple[NormRef]) -> None:
    with pytest.raises(ValidationError, match="listed in norm_refs"):
        CalculationResult(**refused(norm_refs=norm_refs))


def test_a_refusal_lists_the_engineer_rule_of_a_warning() -> None:
    with pytest.raises(ValidationError, match="listed in engineer_rules"):
        CalculationResult(**refused(engineer_rules=()))


def test_a_result_lists_the_references_of_its_steps() -> None:
    with pytest.raises(ValidationError, match="listed in norm_refs"):
        CalculationResult(**completed(norm_refs=(CHECK_REF,)))


def test_a_result_lists_the_rounding_sources_of_its_outputs() -> None:
    rounding_ref = ref("<CLAUSE-ROUNDING>")

    with pytest.raises(ValidationError, match="listed in norm_refs"):
        CalculationResult(**completed(outputs=(output((rounding_ref,)),), engineer_rules=()))
    with pytest.raises(ValidationError, match="listed in engineer_rules"):
        CalculationResult(**completed(engineer_rules=()))


def test_the_envelope_is_the_result_with_a_result_id() -> None:
    result = CalculationResult(**completed())
    result_id = uuid4()

    envelope = ResultEnvelope(result_id=result_id, **result.model_dump())

    assert envelope.result_id == result_id
    assert CalculationResult(**envelope.model_dump(exclude={"result_id"})) == result


def test_an_envelope_needs_a_result_id() -> None:
    with pytest.raises(ValidationError):
        ResultEnvelope(**completed())


def test_input_hash_is_a_sha256_hex_digest() -> None:
    with pytest.raises(ValidationError):
        CalculationResult(**completed(input_hash="not-a-hash"))


@pytest.mark.parametrize("changes", [{"decimals": -1}, {"mode": "ceiling"}])
def test_a_rounding_rule_has_decimals_and_a_known_mode(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        RoundingRule.model_validate({"decimals": 2, "mode": "half_even"} | changes)


def test_a_bound_of_the_method_range_comes_from_the_norm() -> None:
    with pytest.raises(ValidationError):
        MethodBound.model_validate(
            {"quantity": "x", "kind": "min", "value": 0.0, "inclusive": False, "source": RULE}
        )


def test_a_bound_of_the_validated_range_may_be_set_by_the_engineer() -> None:
    bound = ValidatedBound(quantity="x", kind="min", value=0.0, inclusive=False, source=RULE)

    assert bound.source == RULE


def test_a_bound_value_is_finite() -> None:
    with pytest.raises(ValidationError):
        MethodBound(
            quantity="x", kind="max", value=float("inf"), inclusive=True, source=(BOUND_REF,)
        )


VERIFIED_REF = NormRef(
    document="<NORM-DOC-PLACEHOLDER>",
    edition="<YYYY>",
    clause="<CLAUSE-VERIFIED>",
    status="verified",
    provenance="human-verified",
)


def formula_with(*references: NormRef) -> FormulaStep:
    return formula_step().model_copy(update={"norm_refs": references})


def test_a_step_counts_as_verified_only_when_every_reference_is_verified() -> None:
    assert formula_with(VERIFIED_REF).verified
    assert not formula_with(VERIFIED_REF, STEP_REF).verified
    assert not formula_with(STEP_REF).verified


def test_an_unverified_step_is_kept_marked_and_counted() -> None:
    trace = (formula_with(VERIFIED_REF), check_step())

    result = CalculationResult(
        **completed(
            trace=trace, norm_refs=(VERIFIED_REF, CHECK_REF), unverified_step_count=1
        )
    )

    assert result.trace == trace
    assert [step.verified for step in result.trace] == [True, False]
    assert result.unverified_step_count == 1


@pytest.mark.parametrize("count", [0, 1, 3])
def test_a_wrong_unverified_step_count_is_rejected(count: int) -> None:
    with pytest.raises(ValidationError, match="number of unverified steps"):
        CalculationResult(**completed(unverified_step_count=count))

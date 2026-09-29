from typing import Any

import pytest
from pydantic import ValidationError

from app.core.exceptions import CalculationError, DECError, UnitError
from app.engine.result import assemble_result
from app.engine.steps import check_step, table_step
from app.schemas.calculation import (
    ApplicabilityWarning,
    BoundViolation,
    CalculationResult,
    CalculationTypeContract,
    CheckStep,
    MethodBound,
    NormRef,
    OutputDeclaration,
    OutputValue,
    QuantityDeclaration,
    QuantityValue,
    RoundingRule,
    TableStep,
    ValidatedBound,
)
from app.schemas.parameters import EngineerRule
from app.schemas.resolved import TableValue

HASH = "0" * 64


def ref(clause: str) -> NormRef:
    return NormRef(
        document="<NORM-DOC-PLACEHOLDER>",
        edition="unverified",
        clause=clause,
        status="unverified",
        provenance="machine-extracted",
    )


A, B, C, D = (ref(f"<CLAUSE-{name}>") for name in "ABCD")
RULE = EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>")


def declared_output(name: str, unit: str) -> OutputDeclaration:
    return OutputDeclaration(
        name=name,
        base_unit=unit,
        rounding_rule=RoundingRule(decimals=1, mode="half_up"),
        rounding_source=RULE,
    )


def contract(**changes: Any) -> CalculationTypeContract:
    fields: dict[str, Any] = {
        "name": "t",
        "inputs": (QuantityDeclaration(name="x", base_unit="m"),),
        "outputs": (
            declared_output("y1", "kPa"),
            declared_output("y2", "m"),
        ),
        "checks": ("check",),
    }
    return CalculationTypeContract.model_validate(fields | changes)


def table(step_id: str, *references: NormRef) -> TableStep:
    entry = TableValue(
        symbol=step_id, latex=step_id, value=QuantityValue(value=1.0, unit="1"), norm_refs=references
    )
    return table_step(step_id, entry, {})


def check(step_id: str = "check", *references: NormRef) -> CheckStep:
    left = QuantityValue(value=1.0, unit="kPa")
    right = QuantityValue(value=2.0, unit="kPa")
    return check_step(step_id, ("p", left), "le", ("R", right), references or (C,))


def output(quantity: str, unit: str, source: Any = RULE) -> OutputValue:
    return OutputValue(
        quantity=quantity,
        value=1.0,
        unit=unit,
        rounding_rule=RoundingRule(decimals=1, mode="half_up"),
        rounding_source=source,
    )


OUTPUTS = (output("y1", "kPa"), output("y2", "m"))


def validated(value: float, source: Any) -> ValidatedBound:
    return ValidatedBound(quantity="x", kind="max", value=value, inclusive=True, source=source)


def warning(bound: ValidatedBound) -> ApplicabilityWarning:
    return ApplicabilityWarning(value=QuantityValue(value=9.0, unit="m"), bound=bound)


def assemble(**changes: Any) -> CalculationResult:
    fields: dict[str, Any] = {
        "input_hash": HASH,
        "trace": (table("k", A), check()),
        "outputs": OUTPUTS,
        "warnings": (),
        "validated_range": (),
    }
    return assemble_result(contract(), **(fields | changes))


def test_a_norm_ref_used_by_two_steps_appears_once_at_its_first_use() -> None:
    result = assemble(trace=(table("k1", A), table("k2", B, A), check("check", C, B)))

    assert result.norm_refs == (A, B, C)


def test_an_engineer_rule_used_by_a_rounding_source_and_a_warning_appears_once() -> None:
    bound = validated(8.0, RULE)

    result = assemble(warnings=(warning(bound),), validated_range=(bound,))

    assert result.engineer_rules == (RULE,)


def test_outputs_follow_the_declared_order_of_output_quantities() -> None:
    result = assemble(outputs=tuple(reversed(OUTPUTS)))

    assert [item.quantity for item in result.outputs] == ["y1", "y2"]


def test_warnings_follow_the_declared_order_of_the_validated_range() -> None:
    first, second = validated(8.0, (D,)), validated(7.0, (B,))

    result = assemble(
        warnings=(warning(second), warning(first)), validated_range=(first, second)
    )

    assert [item.bound for item in result.warnings] == [first, second]
    assert result.norm_refs == (A, C, D, B)


def test_the_verdict_and_count_are_derived() -> None:
    result = assemble()

    assert (result.verdict, result.verdict_reason.kind) == ("pass", "check")
    assert result.unverified_step_count == 2


def test_a_refused_calculation_lists_the_bound_then_the_warnings() -> None:
    bound = validated(8.0, (D,))
    refusal = BoundViolation(
        value=QuantityValue(value=12.0, unit="m"),
        bound=MethodBound(quantity="x", kind="max", value=10.0, inclusive=True, source=(B,)),
    )

    result = assemble(
        trace=(), outputs=(), warnings=(warning(bound),), validated_range=(bound,), refusal=refusal
    )

    assert result.verdict == "refused"
    assert result.norm_refs == (B, D)
    assert (result.trace, result.outputs) == ((), ())


@pytest.mark.parametrize(
    "changes,match",
    [
        ({"outputs": (OUTPUTS[0], OUTPUTS[0], OUTPUTS[1])}, "given twice"),
        ({"outputs": (OUTPUTS[0],)}, "do not match the declared outputs"),
        ({"outputs": (*OUTPUTS, output("z", "m"))}, "do not match the declared outputs"),
        ({"trace": (table("k", A), check("other"))}, "not declared"),
        ({"trace": (table("k", A),)}, "at least one check step"),
        ({"warnings": (warning(validated(8.0, RULE)),)}, "outside the validated range"),
        ({"input_hash": "not-a-hash"}, "not valid"),
    ],
    ids=[
        "duplicate-output",
        "missing-output",
        "unknown-output",
        "undeclared-check",
        "no-check",
        "unknown-warning-bound",
        "invalid-result",
    ],
)
def test_parts_that_do_not_form_a_result_fail_with_a_dec_error(
    changes: dict[str, Any], match: str
) -> None:
    with pytest.raises(CalculationError, match=match):
        assemble(**changes)


def test_an_output_outside_its_base_unit_fails() -> None:
    with pytest.raises(UnitError, match="'y2'"):
        assemble(outputs=(output("y1", "kPa"), output("y2", "mm")))


def test_a_refusal_with_a_trace_fails() -> None:
    refusal = BoundViolation(
        value=QuantityValue(value=12.0, unit="m"),
        bound=MethodBound(quantity="x", kind="max", value=10.0, inclusive=True, source=(B,)),
    )

    with pytest.raises(CalculationError, match="no trace and no outputs"):
        assemble(refusal=refusal)


def test_assembly_errors_are_dec_errors() -> None:
    assert issubclass(CalculationError, DECError)


@pytest.mark.parametrize(
    "norm_refs", [(C, A), (A, C, A), (A, C, B)], ids=["misordered", "duplicated", "extra"]
)
def test_an_envelope_lists_its_references_once_in_order_of_first_use(
    norm_refs: tuple[NormRef, ...],
) -> None:
    fields = assemble().model_dump() | {"norm_refs": norm_refs}

    with pytest.raises(ValidationError, match="order of first use"):
        CalculationResult.model_validate(fields)


def test_an_output_rounded_by_another_rule_than_declared_fails() -> None:
    other = OutputValue(
        quantity="y1",
        value=1.0,
        unit="kPa",
        rounding_rule=RoundingRule(decimals=2, mode="half_up"),
        rounding_source=RULE,
    )

    with pytest.raises(CalculationError, match="not rounded by the rule"):
        assemble(outputs=(other, OUTPUTS[1]))

import datetime

import pytest
from test_engine_foundations_shallow_r import (
    REF,
    ROUNDING,
    RULE,
    entry,
    inputs,
    parameters,
)

from app.core.exceptions import InputValidationError
from app.engine import foundations_shallow_r as pilot
from app.engine.registry import CalculatorRegistry
from app.reporting.model import (
    AccountabilitySection,
    ConclusionSection,
    InputSection,
    Report,
    TraceSection,
    build_report,
)
from app.schemas.calculation import (
    CheckStep,
    MethodBound,
    NormRef,
    QuantityValue,
    ResultEnvelope,
)
from app.schemas.report import ReportRequest, Signatory, TitleBlockData
from app.services.calculation import CalculationService

VERIFIED = NormRef(
    document="<NORM-DOC-PLACEHOLDER>",
    edition="<EDITION>",
    clause="<CLAUSE>",
    status="verified",
    provenance="human-verified",
)
SIGNATORY = Signatory(surname="<SURNAME>", date=datetime.date(2026, 9, 30))
REQUEST = ReportRequest(
    title=TitleBlockData(designation="<DESIGNATION>", document_name="<DOCUMENT>", organization="<ORG>"),
    developer=SIGNATORY,
    normative_control=SIGNATORY,
)
BOUND = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(REF,))


def service() -> CalculationService:
    registry = CalculatorRegistry()
    pilot.register(registry, ROUNDING, RULE)
    return CalculationService(registry)


def envelope(
    given: dict[str, QuantityValue] | None = None, *, refused: bool = False, verified_k: bool = False
) -> ResultEnvelope:
    resolved = parameters(k=entry("k", 4.0).model_copy(update={"norm_refs": (VERIFIED,)})) if verified_k else parameters()
    return service().run(
        pilot.NAME,
        inputs() if given is None else given,
        resolved,
        method_range=(BOUND,) if refused else (),
    )


def report(given: dict[str, QuantityValue] | None = None, **kwargs: bool) -> Report:
    given = inputs() if given is None else given
    return build_report(pilot.contract(ROUNDING, RULE), given, envelope(given, **kwargs), REQUEST)


@pytest.mark.parametrize("refused", [False, True], ids=["completed", "refused"])
def test_the_body_sections_are_in_the_order_of_the_requirement(refused: bool) -> None:
    kinds = [section.kind for section in report(refused=refused).body]

    assert kinds == ["inputs", "trace", "conclusion", "accountability"]


def test_the_accountability_block_carries_the_envelope() -> None:
    given = inputs()
    result = envelope(given)

    block = build_report(pilot.contract(ROUNDING, RULE), given, result, REQUEST).body[-1]

    assert isinstance(block, AccountabilitySection)
    assert block.envelope == result


def test_the_input_table_follows_the_declared_order_in_the_units_of_the_request() -> None:
    given = dict(reversed(list(inputs(b=2000.0, b_unit="mm").items())))

    section = report(given).body[0]

    assert isinstance(section, InputSection)
    assert [row.quantity for row in section.rows] == [quantity.name for quantity in pilot.INPUTS]
    assert section.rows[0].value == QuantityValue(value=2000.0, unit="mm")


def test_a_check_step_carries_its_comparison_both_values_with_units_and_whether_it_passed() -> None:
    trace = report().body[1]

    assert isinstance(trace, TraceSection)
    check = trace.steps[-1]
    assert isinstance(check, CheckStep)
    assert (check.expression, check.operator, check.passed) == (r"p \le R", "le", True)
    assert (check.result, check.right) == (
        QuantityValue(value=100.0, unit="kPa"),
        QuantityValue(value=172.5, unit="kPa"),
    )


def test_each_norm_ref_of_a_step_is_carried_with_its_status() -> None:
    trace = report(verified_k=True).body[1]

    assert isinstance(trace, TraceSection)
    statuses = {step.step_id: [ref.status for ref in step.norm_refs] for step in trace.steps}
    assert statuses["k"] == ["verified"]
    assert statuses["gamma_c1"] == ["unverified"]
    assert not trace.refused


@pytest.mark.parametrize(("p", "verdict", "passed"), [(100.0, "pass", True), (200.0, "fail", False)])
def test_the_conclusion_names_the_deciding_check(p: float, verdict: str, passed: bool) -> None:
    conclusion = report(inputs(p=p)).body[2]

    assert isinstance(conclusion, ConclusionSection)
    assert conclusion.verdict == verdict
    assert conclusion.deciding_check is not None
    assert (conclusion.deciding_check.step_id, conclusion.deciding_check.passed) == (pilot.CHECK, passed)
    assert conclusion.violation is None


def test_a_refused_calculation_keeps_the_sections_and_names_the_bound() -> None:
    refused = report(refused=True)

    inputs_section, trace, conclusion, _ = refused.body
    assert isinstance(inputs_section, InputSection) and len(inputs_section.rows) == len(pilot.INPUTS)
    assert isinstance(trace, TraceSection) and (trace.refused, trace.steps) == (True, ())
    assert isinstance(conclusion, ConclusionSection)
    assert (conclusion.verdict, conclusion.deciding_check) == ("refused", None)
    assert conclusion.violation is not None
    assert conclusion.violation.bound == BOUND
    assert conclusion.violation.value == QuantityValue(value=2.0, unit="m")
    assert conclusion.violation.bound.source == (REF,)


def test_inputs_that_do_not_match_the_contract_are_rejected() -> None:
    given = inputs()
    result = envelope(given)
    del given["p"]

    with pytest.raises(InputValidationError, match="declared inputs"):
        build_report(pilot.contract(ROUNDING, RULE), given, result, REQUEST)


def test_the_report_keeps_the_request() -> None:
    assert report().request == REQUEST

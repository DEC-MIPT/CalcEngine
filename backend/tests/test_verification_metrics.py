import pytest
from test_verification_properties import DriftingCalculator
from test_verification_runner import (
    CONTRACT,
    METHOD,
    PARAMETERS,
    example,
    output,
    registry,
    resolve,
)

from app.engine.registry import CalculatorRegistry
from app.schemas.calculation import NormRef
from app.verification.metrics import (
    Deviation,
    GoReport,
    Reproducibility,
    Traceability,
    deviations,
    go_report,
    reproducibility,
    traceability,
)
from app.verification.models import ReferenceExample
from app.verification.runner import ExampleParameters, SuiteReport, run_suite

DRIFTING = "synthetic_drifting_type"


def with_drifting() -> CalculatorRegistry:
    """Реестр синтетического типа и его копии с калькулятором, который меняет результат."""
    built = registry()
    built.register(CONTRACT.model_copy(update={"name": DRIFTING}), DriftingCalculator())
    return built


def drifting(example_id: str) -> ReferenceExample:
    return ReferenceExample.model_validate(example(example_id).model_dump() | {"calculation_type": DRIFTING})


def test_a_deviation_is_the_computed_minus_the_expected_value_next_to_its_tolerance() -> None:
    report = run_suite([example("ex", y=output(6.25, tolerance=0.5), z=output(1.0))], registry(), resolve)

    assert deviations(report) == (
        Deviation(example_id="ex", quantity="y", deviation=-0.25, unit="m", tolerance=0.5, tolerance_kind="absolute"),
        Deviation(example_id="ex", quantity="z", deviation=None, unit="m", tolerance=0.01, tolerance_kind="absolute"),
    )


def test_a_deviation_is_in_the_unit_of_the_expected_value() -> None:
    report = run_suite([example("mm", y=output(6010.0, unit="mm", tolerance=0.5, kind="relative"))], registry(), resolve)

    (deviation,) = deviations(report)
    assert (deviation.deviation, deviation.unit, deviation.tolerance_kind) == (-10.0, "mm", "relative")


def test_every_quantity_of_every_example_has_a_deviation_in_order() -> None:
    report = run_suite([example("a"), example("b", b=4.0, y=output(12.0)), example("far", b=60.0)], registry(), resolve)

    assert [(item.example_id, item.quantity, item.deviation) for item in deviations(report)] == [
        ("a", "y", 0.0),
        ("b", "y", 0.0),
        ("far", "y", None),
    ]


def test_an_example_that_raised_gives_no_deviation() -> None:
    unknown = example().model_copy(update={"calculation_type": "not_registered"})

    assert deviations(run_suite([unknown], registry(), resolve)) == ()


def test_every_example_reproduced_gives_a_rate_of_one() -> None:
    measured = reproducibility(run_suite([example("a"), example("b")], registry(), resolve))

    assert (measured.reproduced, measured.examples, measured.rate, measured.not_reproduced) == (2, 2, 1.0, ())
    assert measured.verdict == "GO"


def test_a_rate_below_one_hundred_percent_gives_no_go() -> None:
    report = run_suite([example("a"), drifting("d")], with_drifting(), resolve)

    measured = reproducibility(report)

    assert (measured.reproduced, measured.examples, measured.rate) == (1, 2, 0.5)
    assert measured.not_reproduced == ("d",)
    assert measured.verdict == "NO-GO"


def test_an_example_that_raised_counts_as_not_reproduced() -> None:
    unknown = example("unknown").model_copy(update={"calculation_type": "not_registered"})

    measured = reproducibility(run_suite([example("a"), unknown], registry(), resolve))

    assert (measured.reproduced, measured.examples, measured.not_reproduced) == (1, 2, ("unknown",))


def test_a_refused_example_is_reproduced_when_both_refusals_are_equal() -> None:
    report = run_suite([example("far", b=60.0)], registry(), resolve)

    assert report.runs[0].outcome == "refused"
    assert reproducibility(report).not_reproduced == ()


def test_an_empty_run_has_no_rate_and_gives_no_go() -> None:
    empty = Reproducibility(reproduced=0, examples=0, not_reproduced=())

    assert (empty.rate, empty.verdict) == (None, "NO-GO")


def test_the_go_report_of_a_claimed_go_without_examples_is_no_go() -> None:
    report = go_report(SuiteReport(verdict="GO", runs=()))

    assert report.effective_verdict == "NO-GO"


def test_the_go_report_of_a_passing_reproduced_suite_is_go_with_both_metrics() -> None:
    report = go_report(run_suite([example("a"), example("b")], registry(), resolve))

    assert (report.verdict, report.effective_verdict, report.missing_metrics) == ("GO", "GO", ())
    assert report.deviations is not None and len(report.deviations) == 2
    assert report.reproducibility is not None and report.reproducibility.rate == 1.0
    assert report.traceability == Traceability(verified_steps=0, steps=4, engineer_rules=2)


def test_a_failing_suite_gives_a_no_go_report_with_its_metrics() -> None:
    report = go_report(run_suite([example("off", y=output(7.0))], registry(), resolve))

    assert (report.verdict, report.effective_verdict) == ("NO-GO", "NO-GO")
    assert report.deviations is not None and report.deviations[0].deviation == -1.0


def test_a_passing_suite_that_does_not_reproduce_gives_no_go() -> None:
    first_call = ReferenceExample.model_validate(
        example("d", y=output(8.0)).model_dump() | {"calculation_type": DRIFTING}
    )

    suite = run_suite([first_call], with_drifting(), resolve)

    assert suite.verdict == "GO"
    assert suite.runs[0].reproduced is False
    assert go_report(suite).verdict == "NO-GO"


@pytest.mark.parametrize(
    ("attach", "missing"),
    [
        ((False, True, True), ("deviation from the references",)),
        ((True, False, True), ("reproducibility rate",)),
        ((True, True, False), ("traceability completeness",)),
        (
            (False, False, False),
            ("deviation from the references", "reproducibility rate", "traceability completeness"),
        ),
    ],
    ids=["no deviations", "no reproducibility", "no traceability", "no metrics"],
)
def test_a_go_without_a_metric_is_invalid_and_counts_as_no_go(
    attach: tuple[bool, bool, bool], missing: tuple[str, ...]
) -> None:
    full = go_report(run_suite([example("a")], registry(), resolve))

    claimed = GoReport(
        verdict="GO",
        deviations=full.deviations if attach[0] else None,
        reproducibility=full.reproducibility if attach[1] else None,
        traceability=full.traceability if attach[2] else None,
    )

    assert claimed.missing_metrics == missing
    assert claimed.effective_verdict == "NO-GO"


def test_a_go_claimed_with_a_rate_below_one_hundred_percent_counts_as_no_go() -> None:
    claimed = GoReport(
        verdict="GO",
        deviations=(),
        reproducibility=Reproducibility(reproduced=1, examples=2, not_reproduced=("d",)),
        traceability=Traceability(verified_steps=0, steps=0, engineer_rules=0),
    )

    assert (claimed.missing_metrics, claimed.effective_verdict) == ((), "NO-GO")


def test_a_no_go_stays_no_go() -> None:
    claimed = GoReport(
        verdict="NO-GO",
        deviations=(),
        reproducibility=Reproducibility(1, 1, ()),
        traceability=Traceability(verified_steps=0, steps=0, engineer_rules=0),
    )

    assert claimed.effective_verdict == "NO-GO"


VERIFIED = NormRef(
    document="<NORM-DOC-PLACEHOLDER>",
    edition="<EDITION-PLACEHOLDER>",
    clause="<CLAUSE-PLACEHOLDER>",
    status="verified",
    provenance="human-verified",
)


def verified_formula(example: ReferenceExample) -> ExampleParameters:
    """Параметры, у формулы которых проверенная ссылка; ссылка проверки в калькуляторе — нет."""
    formula = PARAMETERS.formula.model_copy(update={"norm_refs": (VERIFIED,)})
    return ExampleParameters(parameters=PARAMETERS.model_copy(update={"formula": formula}), method_range=METHOD)


def test_traceability_counts_the_verified_steps_of_every_envelope() -> None:
    measured = traceability(run_suite([example("a"), example("b")], registry(), verified_formula))

    assert measured == Traceability(verified_steps=2, steps=4, engineer_rules=2)
    assert measured.completeness == 0.5


def test_unverified_references_give_a_completeness_of_zero() -> None:
    measured = traceability(run_suite([example("a")], registry(), resolve))

    assert (measured.verified_steps, measured.steps, measured.completeness) == (0, 2, 0.0)


def test_refused_and_failed_runs_are_not_counted() -> None:
    unknown = example("unknown").model_copy(update={"calculation_type": "not_registered"})

    measured = traceability(run_suite([example("a"), example("far", b=60.0), unknown], registry(), verified_formula))

    assert measured == Traceability(verified_steps=1, steps=2, engineer_rules=1)


def test_a_run_without_steps_has_no_completeness() -> None:
    measured = traceability(run_suite([example("far", b=60.0)], registry(), resolve))

    assert (measured.steps, measured.completeness) == (0, None)


def test_traceability_does_not_decide_the_verdict() -> None:
    report = go_report(run_suite([example("a"), example("b")], registry(), resolve))

    assert report.traceability is not None and report.traceability.completeness == 0.0
    assert (report.verdict, report.effective_verdict) == ("GO", "GO")

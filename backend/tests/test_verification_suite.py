from typing import Any

from test_verification_runner import TYPE, example, output, registry, resolve

from app.verification.models import parse_examples
from app.verification.runner import (
    MIN_EXAMPLES_PER_TYPE,
    DuplicateExampleId,
    NoCalculationTypes,
    RejectedExample,
    TooFewExamples,
    run_reference_suite,
    suite_invalidity,
)

OTHER = "synthetic_other_type"


def card(example_id: str, **changes: Any) -> dict[str, Any]:
    """Сырая карточка синтетического примера, которая проходит модель.

    Args:
        example_id: идентификатор примера.
        changes: поля, которые заменяют значения карточки.

    Returns:
        Словарь полей карточки.
    """
    return example(example_id).model_dump() | changes


def cards(count: int, calculation_type: str = TYPE) -> list[dict[str, Any]]:
    return [card(f"{calculation_type}-{index}", calculation_type=calculation_type) for index in range(count)]


def test_three_examples_per_listed_type_make_a_valid_suite() -> None:
    report = run_reference_suite(parse_examples(cards(3)), [TYPE], registry(), resolve)

    assert (report.verdict, report.invalid) == ("GO", ())
    assert [run.outcome for run in report.runs] == ["passed"] * 3


def test_the_minimum_is_three_examples_per_type() -> None:
    assert MIN_EXAMPLES_PER_TYPE == 3


def test_a_type_with_fewer_than_three_examples_makes_the_suite_invalid() -> None:
    report = run_reference_suite(parse_examples(cards(2)), [TYPE], registry(), resolve)

    assert report.verdict == "NO-GO"
    assert report.invalid == (TooFewExamples(calculation_type=TYPE, count=2),)
    assert [run.outcome for run in report.runs] == ["passed", "passed"]


def test_a_listed_type_without_examples_is_named_with_zero() -> None:
    report = run_reference_suite(parse_examples(cards(3)), [TYPE, OTHER], registry(), resolve)

    assert report.verdict == "NO-GO"
    assert report.invalid == (TooFewExamples(calculation_type=OTHER, count=0),)


def test_examples_of_an_unlisted_type_do_not_count_for_a_listed_one() -> None:
    parsed = parse_examples(cards(2) + cards(3, OTHER))

    assert suite_invalidity(parsed, [TYPE]) == (TooFewExamples(calculation_type=TYPE, count=2),)


def test_a_type_listed_twice_is_named_once() -> None:
    assert suite_invalidity(parse_examples([]), [TYPE, TYPE]) == (TooFewExamples(calculation_type=TYPE, count=0),)


def test_an_empty_list_of_types_makes_the_suite_invalid() -> None:
    report = run_reference_suite(parse_examples(cards(3)), [], registry(), resolve)

    assert report.verdict == "NO-GO"
    assert report.invalid == (NoCalculationTypes(),)


def test_a_rejected_card_makes_the_suite_invalid_and_does_not_count() -> None:
    raw = cards(3)
    del raw[1]["source_norm_edition"]

    report = run_reference_suite(parse_examples(raw), [TYPE], registry(), resolve)

    assert report.verdict == "NO-GO"
    rejected, too_few = report.invalid
    assert isinstance(rejected, RejectedExample)
    assert (rejected.problem.position, rejected.problem.example_id, rejected.problem.fields) == (
        1,
        f"{TYPE}-1",
        ("source_norm_edition",),
    )
    assert too_few == TooFewExamples(calculation_type=TYPE, count=2)
    assert [run.example_id for run in report.runs] == [f"{TYPE}-0", f"{TYPE}-2"]


def test_an_invalid_suite_still_reports_the_failures_of_its_examples() -> None:
    raw = cards(2) + [card("off", expected_outputs={"y": output(7.0)})]

    report = run_reference_suite(parse_examples(raw), [TYPE, OTHER], registry(), resolve)

    assert report.verdict == "NO-GO"
    assert report.invalid == (TooFewExamples(calculation_type=OTHER, count=0),)
    ((example_id, check),) = report.failures
    assert (example_id, check.quantity, check.outcome) == ("off", "y", "outside")


def test_a_valid_suite_with_a_failing_example_is_no_go_without_reasons() -> None:
    raw = cards(2) + [card("off", expected_outputs={"y": output(7.0)})]

    report = run_reference_suite(parse_examples(raw), [TYPE], registry(), resolve)

    assert (report.verdict, report.invalid) == ("NO-GO", ())


def test_a_repeated_example_id_makes_the_suite_invalid_and_counts_once() -> None:
    copies = [card("same", calculation_type=TYPE)] * 3

    report = run_reference_suite(parse_examples(copies), [TYPE], registry(), resolve)

    assert report.verdict == "NO-GO"
    assert report.invalid == (DuplicateExampleId(example_id="same"), TooFewExamples(calculation_type=TYPE, count=1))


def test_a_repeated_id_is_named_once_before_the_shortage() -> None:
    parsed = parse_examples([*cards(3), card(f"{TYPE}-0", calculation_type=TYPE)])

    assert suite_invalidity(parsed, [TYPE]) == (DuplicateExampleId(example_id=f"{TYPE}-0"),)

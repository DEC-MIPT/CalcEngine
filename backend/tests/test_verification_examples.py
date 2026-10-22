from typing import Any

import pytest
from test_verification_models import example_data

from app.verification.models import ExampleProblem, ReferenceExample, parse_examples

TOP_LEVEL = ("example_id", "calculation_type", "inputs", "expected_outputs", "origin", "citation", "source_norm_edition")
OUTPUT_FIELDS = ("value", "unit", "tolerance", "tolerance_kind", "tolerance_source")
CITATION_FIELDS = ("document", "year", "locator")


def without(data: dict[str, Any], field: str) -> dict[str, Any]:
    return {name: value for name, value in data.items() if name != field}


def with_output(**changes: Any) -> dict[str, Any]:
    return example_data(expected_outputs={"y": example_data()["expected_outputs"]["y"] | changes})


def with_citation(**changes: Any) -> dict[str, Any]:
    return example_data(citation=example_data()["citation"] | changes)


def only_problem(data: dict[str, Any]) -> ExampleProblem:
    parsed = parse_examples([data])
    assert parsed.examples == ()
    (problem,) = parsed.problems
    return problem


@pytest.mark.parametrize("field", TOP_LEVEL)
def test_an_example_without_a_field_of_the_requirement_is_rejected_naming_it(field: str) -> None:
    problem = only_problem(without(example_data(), field))

    assert problem.position == 0
    assert problem.fields == (field,)


@pytest.mark.parametrize("field", OUTPUT_FIELDS)
def test_an_expected_output_without_a_field_is_rejected_naming_its_path(field: str) -> None:
    output = without(example_data()["expected_outputs"]["y"], field)

    problem = only_problem(example_data(expected_outputs={"y": output}))

    assert problem.fields == (f"expected_outputs.y.{field}",)
    assert problem.example_id == "synthetic-ex1"


@pytest.mark.parametrize("field", CITATION_FIELDS)
def test_a_citation_without_the_document_year_or_locator_is_rejected(field: str) -> None:
    problem = only_problem(example_data(citation=without(example_data()["citation"], field)))

    assert problem.fields == (f"citation.{field}",)


@pytest.mark.parametrize(
    ("data", "path"),
    [
        (example_data(example_id=" "), "example_id"),
        (example_data(calculation_type=""), "calculation_type"),
        (example_data(source_norm_edition=" "), "source_norm_edition"),
        (with_citation(document=""), "citation.document"),
        (with_citation(locator=" "), "citation.locator"),
        (with_citation(year=0), "citation.year"),
        (example_data(inputs={}), "inputs"),
        (example_data(expected_outputs={}), "expected_outputs"),
        (example_data(origin="guesswork"), "origin"),
        (with_output(tolerance_kind="percent"), "expected_outputs.y.tolerance_kind"),
        (with_output(tolerance=-0.1), "expected_outputs.y.tolerance"),
        (with_output(tolerance=float("inf")), "expected_outputs.y.tolerance"),
        (with_output(unit="furlong"), "expected_outputs.y.unit"),
        (example_data(inputs={"a": {"value": float("nan"), "unit": "m"}}), "inputs.a.value"),
        (example_data(extra="x"), "extra"),
    ],
    ids=[
        "blank id",
        "empty type",
        "blank edition",
        "empty document",
        "blank locator",
        "year zero",
        "no inputs",
        "no outputs",
        "unknown origin",
        "unknown tolerance kind",
        "negative tolerance",
        "infinite tolerance",
        "unit outside the vocabulary",
        "non-finite input",
        "undeclared field",
    ],
)
def test_an_empty_or_invalid_field_is_rejected_naming_it(data: dict[str, Any], path: str) -> None:
    assert only_problem(data).fields == (path,)


def test_a_tolerance_source_that_is_neither_references_nor_a_rule_is_rejected() -> None:
    problem = only_problem(with_output(tolerance_source="the guide prints two digits"))

    assert problem.fields
    assert all(field.startswith("expected_outputs.y.tolerance_source") for field in problem.fields)


def test_every_missing_field_of_one_example_is_named_once() -> None:
    data = without(without(example_data(), "origin"), "source_norm_edition")

    assert only_problem(data).fields == ("origin", "source_norm_edition")


def test_a_problem_holds_the_place_and_the_paths_but_no_value() -> None:
    problem = only_problem(with_output(tolerance=-123.456))

    assert "123.456" not in repr(problem)


@pytest.mark.parametrize("example_id", [None, "", "  ", 7])
def test_a_problem_names_no_example_id_when_it_cannot_be_read(example_id: object) -> None:
    data = without(without(example_data(), "origin"), "example_id")
    if example_id is not None:
        data["example_id"] = example_id

    assert only_problem(data).example_id is None


def test_valid_and_rejected_cards_are_separated_in_order() -> None:
    raw = [
        example_data(example_id="first"),
        without(example_data(example_id="second"), "origin"),
        example_data(example_id="third"),
        with_output(tolerance_kind=None) | {"example_id": "fourth"},
    ]

    parsed = parse_examples(raw)

    assert [example.example_id for example in parsed.examples] == ["first", "third"]
    assert all(isinstance(example, ReferenceExample) for example in parsed.examples)
    assert [(problem.position, problem.example_id) for problem in parsed.problems] == [(1, "second"), (3, "fourth")]


def test_no_cards_give_no_examples_and_no_problems() -> None:
    parsed = parse_examples([])

    assert (parsed.examples, parsed.problems) == ((), ())

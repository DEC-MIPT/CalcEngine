from typing import Any

import pytest
from pydantic import ValidationError
from test_verification_runner import CONTRACT, METHOD, PARAMETERS, TYPE, registry

from app.engine import ENGINE_VERSION
from app.engine.pipeline import calculate
from app.schemas.calculation import QuantityValue
from app.verification.regression import (
    VERDICT,
    CorpusEntry,
    CorpusOutput,
    DeclaredDifference,
    Difference,
    freeze,
    parse_declared_differences,
    run_regression,
)
from app.verification.runner import ExampleParameters

INPUTS = {"b": QuantityValue(value=2.0, unit="m"), "q": QuantityValue(value=3.0, unit="1")}


def resolve(entry: CorpusEntry) -> ExampleParameters:
    return ExampleParameters(parameters=PARAMETERS, method_range=METHOD)


def frozen(entry_id: str = "e1", inputs: dict[str, QuantityValue] = INPUTS) -> CorpusEntry:
    return freeze(entry_id, TYPE, inputs, calculate(CONTRACT, registry().get(TYPE), inputs, PARAMETERS, method_range=METHOD))


def stored(entry: CorpusEntry, **changes: Any) -> CorpusEntry:
    """Запись корпуса, какой её оставило прежнее изменение: те же поля, кроме ``changes``."""
    return CorpusEntry.model_validate(entry.model_dump() | changes)


def y(value: float) -> CorpusOutput:
    return CorpusOutput(quantity="y", value=value, unit="m")


def declared(entry_id: str, quantity: str, old: Any, new: Any) -> DeclaredDifference:
    return DeclaredDifference(entry_id=entry_id, quantity=quantity, old=old, new=new, reason="<REASON>")


def test_a_frozen_entry_keeps_type_inputs_outputs_verdict_hash_and_engine_version() -> None:
    entry = frozen()

    assert (entry.entry_id, entry.calculation_type, entry.inputs) == ("e1", TYPE, INPUTS)
    assert entry.outputs == (y(6.0),)
    assert entry.verdict == "pass"
    assert len(entry.input_hash) == 64
    assert entry.engine_version == ENGINE_VERSION


def test_a_frozen_entry_survives_a_round_trip_through_json() -> None:
    entry = frozen()

    assert CorpusEntry.model_validate_json(entry.model_dump_json()) == entry


@pytest.mark.parametrize(
    "changes",
    [{"input_hash": "abc"}, {"verdict": "maybe"}, {"inputs": {}}, {"engine_version": " "}, {"entry_id": ""}],
    ids=["short hash", "unknown verdict", "no inputs", "blank engine version", "blank id"],
)
def test_an_invalid_entry_is_rejected(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        stored(frozen(), **changes)


def test_unchanged_results_pass() -> None:
    report = run_regression([frozen("e1"), frozen("e2", {**INPUTS, "b": QuantityValue(value=4.0, unit="m")})], registry(), resolve)

    assert report.verdict == "GO"
    assert [(check.entry_id, check.outcome, check.differences) for check in report.checks] == [
        ("e1", "unchanged", ()),
        ("e2", "unchanged", ()),
    ]


def test_an_undeclared_difference_fails_naming_the_entry_quantity_and_both_engine_versions() -> None:
    old = stored(frozen(), outputs=(y(5.5),), engine_version="0.0.9")

    report = run_regression([old], registry(), resolve)

    assert report.verdict == "NO-GO"
    (check,) = report.checks
    assert (check.entry_id, check.outcome) == ("e1", "undeclared")
    assert check.undeclared == (
        Difference(quantity="y", old=QuantityValue(value=5.5, unit="m"), new=QuantityValue(value=6.0, unit="m")),
    )
    assert (check.stored_engine_version, check.recomputed_engine_version) == ("0.0.9", ENGINE_VERSION)


def test_a_declared_difference_passes() -> None:
    old = stored(frozen(), outputs=(y(5.5),))
    declaration = declared("e1", "y", QuantityValue(value=5.5, unit="m"), QuantityValue(value=6.0, unit="m"))

    report = run_regression([old], registry(), resolve, [declaration])

    assert report.verdict == "GO"
    assert (report.checks[0].outcome, report.checks[0].undeclared, report.unused_declarations) == ("declared", (), ())


def test_a_declaration_with_another_value_does_not_cover_the_difference() -> None:
    old = stored(frozen(), outputs=(y(5.5),))
    wrong = declared("e1", "y", QuantityValue(value=5.5, unit="m"), QuantityValue(value=6.5, unit="m"))

    report = run_regression([old], registry(), resolve, [wrong])

    assert (report.verdict, report.checks[0].outcome) == ("NO-GO", "undeclared")
    assert report.unused_declarations == (wrong,)


def test_a_declaration_for_another_entry_does_not_cover_the_difference() -> None:
    old = stored(frozen(), outputs=(y(5.5),))
    other = declared("e2", "y", QuantityValue(value=5.5, unit="m"), QuantityValue(value=6.0, unit="m"))

    assert run_regression([old], registry(), resolve, [other]).verdict == "NO-GO"


def test_a_verdict_difference_is_named_and_can_be_declared() -> None:
    old = stored(frozen(), verdict="fail")

    undeclared = run_regression([old], registry(), resolve)
    covered = run_regression([old], registry(), resolve, [declared("e1", VERDICT, "fail", "pass")])

    assert undeclared.checks[0].undeclared == (Difference(quantity=VERDICT, old="fail", new="pass"),)
    assert (undeclared.verdict, covered.verdict) == ("NO-GO", "GO")


def test_an_output_that_disappeared_is_a_difference_to_nothing() -> None:
    old = stored(frozen(), outputs=(y(6.0), CorpusOutput(quantity="z", value=1.0, unit="m")))

    report = run_regression([old], registry(), resolve)

    assert report.checks[0].undeclared == (Difference(quantity="z", old=QuantityValue(value=1.0, unit="m"), new=None),)


def test_a_new_output_is_a_difference_from_nothing() -> None:
    old = stored(frozen(), outputs=())

    report = run_regression([old], registry(), resolve)

    assert report.checks[0].undeclared == (Difference(quantity="y", old=None, new=QuantityValue(value=6.0, unit="m")),)


def test_a_new_input_hash_with_the_same_outputs_and_verdict_passes() -> None:
    old = stored(frozen(), input_hash="0" * 64)

    assert run_regression([old], registry(), resolve).checks[0].outcome == "unchanged"


def test_an_entry_that_cannot_be_recomputed_fails_the_build() -> None:
    old = stored(frozen(), calculation_type="not_registered")

    report = run_regression([old], registry(), resolve)

    assert report.verdict == "NO-GO"
    check = report.checks[0]
    assert (check.outcome, check.error, check.recomputed_engine_version) == ("error", "NotFoundError", None)


PROPOSAL = """# Proposal

## Why

| Not | a | declaration | table | here |
|---|---|---|---|---|
| x | y | 1 m | 2 m | no |

## Declared result differences

| Entry | Quantity | Old | New | Reason |
|---|---|---|---|---|
| `e1` | `y` | 5.5 m | 6.0 m | The synthetic formula changed |
| e1 | verdict | fail | pass | The limit changed |
| e1 | z | 1.0 m | — | The output was dropped |

## Impact

| e9 | y | 1 m | 2 m | after the section |
"""


def test_the_declared_differences_are_read_from_their_section_only() -> None:
    assert parse_declared_differences(PROPOSAL) == (
        DeclaredDifference(
            entry_id="e1",
            quantity="y",
            old=QuantityValue(value=5.5, unit="m"),
            new=QuantityValue(value=6.0, unit="m"),
            reason="The synthetic formula changed",
        ),
        DeclaredDifference(entry_id="e1", quantity=VERDICT, old="fail", new="pass", reason="The limit changed"),
        DeclaredDifference(
            entry_id="e1", quantity="z", old=QuantityValue(value=1.0, unit="m"), new=None, reason="The output was dropped"
        ),
    )


def test_a_proposal_without_the_section_declares_nothing() -> None:
    assert parse_declared_differences("# Proposal\n\n## Why\n\nText.\n") == ()


@pytest.mark.parametrize(
    "row",
    ["| e1 | y | 5.5 m | 6.0 m |", "| e1 | y | five m | 6.0 m | r |", "| e1 | y | 5.5 furlong | 6.0 m | r |", "| e1 | y | 5.5 m | 6.0 m | |"],
    ids=["four cells", "not a number", "unit outside the vocabulary", "no reason"],
)
def test_an_unreadable_declaration_is_rejected_with_its_line(row: str) -> None:
    text = f"## Declared result differences\n\n| Entry | Quantity | Old | New | Reason |\n|---|---|---|---|---|\n{row}\n"

    with pytest.raises(ValueError, match="line 5"):
        parse_declared_differences(text)


def test_the_declarations_of_a_proposal_let_the_regression_pass() -> None:
    old = stored(frozen(), outputs=(y(5.5), CorpusOutput(quantity="z", value=1.0, unit="m")), verdict="fail")

    report = run_regression([old], registry(), resolve, parse_declared_differences(PROPOSAL))

    assert (report.verdict, report.checks[0].outcome, report.unused_declarations) == ("GO", "declared", ())

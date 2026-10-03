from typing import Any

import pytest
from pydantic import TypeAdapter, ValidationError

from app.schemas.calculation import (
    CalculationTypeContract,
    CheckStep,
    FormulaStep,
    NormRef,
    OutputDeclaration,
    QuantityDeclaration,
    QuantityValue,
    RoundingRule,
    Source,
    Substitution,
    TableStep,
    TraceStep,
)
from app.schemas.parameters import EngineerRule


def quantity(name: str, unit: str = "m") -> QuantityDeclaration:
    return QuantityDeclaration(name=name, base_unit=unit)


def output(name: str, unit: str = "m") -> OutputDeclaration:
    return OutputDeclaration(
        name=name,
        base_unit=unit,
        rounding_rule=RoundingRule(decimals=2, mode="half_up"),
        rounding_source=EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>"),
    )


def test_contract_holds_quantities_with_base_units() -> None:
    contract = CalculationTypeContract(
        checks=("c",),
        name="t", inputs=(quantity("b"), quantity("d", "kPa")), outputs=(output("r"),)
    )

    assert [(q.name, q.base_unit) for q in contract.inputs] == [("b", "m"), ("d", "kPa")]


@pytest.mark.parametrize("field", ["inputs", "outputs"])
def test_contract_needs_at_least_one_quantity_on_each_side(field: str) -> None:
    sides: dict[str, tuple[Any, ...]] = {
        "inputs": (quantity("a"),),
        "outputs": (output("b"),),
    }
    sides[field] = ()

    with pytest.raises(ValidationError):
        CalculationTypeContract(checks=("c",), name="t", **sides)


@pytest.mark.parametrize("field", ["inputs", "outputs"])
def test_quantity_names_must_be_unique_within_a_side(field: str) -> None:
    sides: dict[str, tuple[Any, ...]] = {
        "inputs": (quantity("a"),),
        "outputs": (output("b"),),
    }
    make = output if field == "outputs" else quantity
    sides[field] = (make("x"), make("x", "kPa"))

    with pytest.raises(ValidationError):
        CalculationTypeContract(checks=("c",), name="t", **sides)


def test_same_name_on_both_sides_is_allowed() -> None:
    contract = CalculationTypeContract(
        checks=("c",),
        name="t", inputs=(quantity("x"),), outputs=(output("x"),)
    )

    assert contract.inputs[0].name == contract.outputs[0].name


@pytest.mark.parametrize("name,unit", [("", "m"), ("x", "")])
def test_quantity_needs_a_name_and_a_base_unit(name: str, unit: str) -> None:
    with pytest.raises(ValidationError):
        QuantityDeclaration(name=name, base_unit=unit)


def test_contract_is_immutable() -> None:
    contract = CalculationTypeContract(
        checks=("c",),
        name="t", inputs=(quantity("a"),), outputs=(output("b"),)
    )

    with pytest.raises(ValidationError):
        contract.name = "other"


def norm_ref(**changes: str) -> NormRef:
    fields = {
        "document": "<NORM-DOC-PLACEHOLDER>",
        "edition": "unverified",
        "clause": "<CLAUSE-PLACEHOLDER>",
        "status": "unverified",
        "provenance": "machine-extracted",
    }
    return NormRef.model_validate(fields | changes)


def step_fields(**changes: Any) -> dict[str, Any]:
    fields: dict[str, Any] = {
        "step_id": "s1",
        "expression": r"y = a \cdot x",
        "substitutions": (Substitution(symbol="x", value=2.0, unit="m"),),
        "result": QuantityValue(value=4.0, unit="m"),
        "norm_refs": (norm_ref(),),
    }
    return fields | changes


def check_fields(**changes: Any) -> dict[str, Any]:
    fields = {"operator": "le", "right": QuantityValue(value=5.0, unit="m"), "passed": True}
    return step_fields(expression=r"y \le y_{max}", **fields) | changes


def test_unverified_edition_and_clause_serialize_as_the_reserved_string() -> None:
    reference = norm_ref(clause="unverified")

    assert reference.model_dump()["edition"] == "unverified"
    assert reference.model_dump()["clause"] == "unverified"


def test_a_verified_human_checked_reference_is_accepted() -> None:
    reference = norm_ref(
        edition="<YYYY>", status="verified", provenance="human-verified"
    )

    assert reference.status == "verified"


@pytest.mark.parametrize("field", ["edition", "clause"])
def test_verified_needs_a_concrete_edition_and_clause(field: str) -> None:
    concrete = {"edition": "<YYYY>", "clause": "<CLAUSE-PLACEHOLDER>"}
    concrete[field] = "unverified"

    with pytest.raises(ValidationError, match="concrete edition and clause"):
        norm_ref(status="verified", provenance="human-verified", **concrete)


def test_machine_extracted_is_never_verified() -> None:
    with pytest.raises(ValidationError, match="always unverified"):
        norm_ref(edition="<YYYY>", status="verified", provenance="machine-extracted")


def test_document_is_never_unverified() -> None:
    with pytest.raises(ValidationError, match="concrete designation"):
        norm_ref(document="unverified")


@pytest.mark.parametrize("field", ["document", "edition", "clause"])
def test_norm_ref_fields_are_not_empty(field: str) -> None:
    with pytest.raises(ValidationError):
        norm_ref(**{field: ""})


def test_norm_ref_rejects_unknown_status_and_provenance() -> None:
    with pytest.raises(ValidationError):
        norm_ref(status="checked")
    with pytest.raises(ValidationError):
        norm_ref(provenance="ocr")


@pytest.mark.parametrize("model", [FormulaStep, TableStep])
def test_a_step_without_norm_refs_is_rejected(model: type[FormulaStep]) -> None:
    with pytest.raises(ValidationError):
        model(**step_fields(norm_refs=()))


def test_a_check_step_without_norm_refs_is_rejected() -> None:
    with pytest.raises(ValidationError):
        CheckStep(**check_fields(norm_refs=()))


@pytest.mark.parametrize("field", ["step_id", "expression", "substitutions", "result"])
def test_step_fields_are_not_null(field: str) -> None:
    with pytest.raises(ValidationError):
        FormulaStep(**step_fields(**{field: None}))


def test_a_step_carries_one_norm_ref_per_locator() -> None:
    references = (norm_ref(clause="<CLAUSE-A>"), norm_ref(clause="<CLAUSE-B>"))

    step = TableStep(**step_fields(norm_refs=references))

    assert step.norm_refs == references


def test_a_check_step_records_operator_right_value_and_outcome() -> None:
    step = CheckStep(**check_fields())

    assert (step.operator, step.right.value, step.passed) == ("le", 5.0, True)


@pytest.mark.parametrize("field", ["operator", "right", "passed"])
def test_a_check_step_needs_its_comparison_fields(field: str) -> None:
    fields = check_fields()
    del fields[field]

    with pytest.raises(ValidationError):
        CheckStep(**fields)


def test_a_check_step_rejects_an_unknown_operator() -> None:
    with pytest.raises(ValidationError):
        CheckStep(**check_fields(operator="eq"))


@pytest.mark.parametrize(
    "kind,model", [("formula", FormulaStep), ("table", TableStep), ("check", CheckStep)]
)
def test_trace_step_is_selected_by_kind(kind: str, model: type) -> None:
    data = (check_fields() if kind == "check" else step_fields()) | {"kind": kind}

    adapter: TypeAdapter[Any] = TypeAdapter(TraceStep)

    step = adapter.validate_python(data)

    assert type(step) is model


def test_a_step_is_immutable() -> None:
    step = FormulaStep(**step_fields())

    with pytest.raises(ValidationError):
        step.step_id = "other"


def test_source_is_a_norm_ref_list_or_an_engineer_rule() -> None:
    adapter: TypeAdapter[Any] = TypeAdapter(Source)

    assert adapter.validate_python((norm_ref(),)) == (norm_ref(),)
    assert isinstance(
        adapter.validate_python({"engineer": "E", "rationale": "R"}), EngineerRule
    )
    with pytest.raises(ValidationError):
        adapter.validate_python(())


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_a_value_is_finite(value: float) -> None:
    with pytest.raises(ValidationError):
        QuantityValue(value=value, unit="m")


def test_a_substitution_names_its_symbol() -> None:
    with pytest.raises(ValidationError):
        Substitution(symbol="", value=1.0, unit="m")


def test_contract_with_a_base_unit_outside_the_vocabulary_is_invalid() -> None:
    with pytest.raises(ValidationError, match="unit vocabulary"):
        CalculationTypeContract(
            checks=("c",),
            name="t", inputs=(quantity("a", "furlong"),), outputs=(output("b"),)
        )


def test_dimensionless_quantity_has_the_unit_one() -> None:
    contract = CalculationTypeContract(
        checks=("c",),
        name="t", inputs=(quantity("k", "1"),), outputs=(output("b"),)
    )

    assert contract.inputs[0].base_unit == "1"


def test_a_value_with_a_unit_outside_the_vocabulary_is_rejected() -> None:
    with pytest.raises(ValidationError, match="unit vocabulary"):
        QuantityValue(value=1.0, unit="furlong")


def test_an_output_declares_its_rounding_rule_and_source() -> None:
    declared = output("r")

    assert (declared.rounding_rule.decimals, declared.rounding_rule.mode) == (2, "half_up")
    assert isinstance(declared.rounding_source, EngineerRule)


def test_a_rounding_source_may_be_a_norm_ref_list() -> None:
    reference = norm_ref()

    declared = OutputDeclaration(
        name="r",
        base_unit="kPa",
        rounding_rule=RoundingRule(decimals=0, mode="half_even"),
        rounding_source=(reference,),
    )

    assert declared.rounding_source == (reference,)


def test_a_rounding_source_is_not_an_empty_norm_ref_list() -> None:
    with pytest.raises(ValidationError):
        OutputDeclaration(
            name="r",
            base_unit="kPa",
            rounding_rule=RoundingRule(decimals=0, mode="half_even"),
            rounding_source=(),
        )


def test_an_input_declares_no_rounding() -> None:
    with pytest.raises(ValidationError):
        QuantityDeclaration.model_validate(
            {"name": "x", "base_unit": "m", "rounding_rule": {"decimals": 1, "mode": "half_up"}}
        )

import re
from collections.abc import Mapping
from typing import Any

import pytest

from app.core.exceptions import CalculationError
from app.engine.base import Calculator
from app.engine.boundary import run
from app.engine.hashing import canonical_json, input_hash, parameter_set_id
from app.schemas.calculation import (
    CalculationTypeContract,
    MethodBound,
    NormRef,
    OutputDeclaration,
    QuantityDeclaration,
    QuantityValue,
    RoundingRule,
)
from app.schemas.parameters import EngineerRule
from app.schemas.resolved import TableValue
from app.schemas.text import LocalizedText


def ref(**changes: str) -> NormRef:
    fields = {
        "document": "<NORM-DOC-PLACEHOLDER>",
        "edition": "<YYYY>",
        "clause": "<CLAUSE-PLACEHOLDER>",
        "status": "unverified",
        "provenance": "human-verified",
    }
    return NormRef.model_validate(fields | changes)


def entry(value: float = 0.5, reference: NormRef | None = None) -> TableValue:
    return TableValue(
        symbol="k",
        latex="k",
        value=QuantityValue(value=value, unit="1"),
        norm_refs=(reference or ref(),),
    )


def q(value: float, unit: str = "m") -> QuantityValue:
    return QuantityValue(value=value, unit=unit)


INPUTS = {"b": q(1.5), "p": q(200.0, "kPa")}


def test_identical_inputs_and_parameters_give_identical_hashes() -> None:
    assert input_hash("t", INPUTS, entry()) == input_hash("t", dict(INPUTS), entry())


def test_the_hash_is_a_sha256_hex_digest() -> None:
    assert re.fullmatch(r"[0-9a-f]{64}", input_hash("t", INPUTS, entry()))


def test_a_different_input_gives_a_different_hash() -> None:
    assert input_hash("t", INPUTS, entry()) != input_hash("t", INPUTS | {"b": q(1.6)}, entry())


def test_a_different_calculation_type_gives_a_different_hash() -> None:
    assert input_hash("t", INPUTS, entry()) != input_hash("u", INPUTS, entry())


def test_a_different_resolved_parameter_set_gives_a_different_hash() -> None:
    assert input_hash("t", INPUTS, entry(0.5)) != input_hash("t", INPUTS, entry(0.6))


def test_a_reference_that_changes_status_changes_the_hash() -> None:
    verified = ref(status="verified")

    assert input_hash("t", INPUTS, entry()) != input_hash("t", INPUTS, entry(reference=verified))


def test_an_integer_and_the_equal_float_give_the_same_hash() -> None:
    assert canonical_json(1) == canonical_json(1.0)
    assert input_hash("t", INPUTS, {"k": 2}) == input_hash("t", INPUTS, {"k": 2.0})


def test_key_order_does_not_change_the_hash() -> None:
    assert input_hash("t", {"b": q(1.5), "p": q(200.0, "kPa")}, {"x": 1, "y": 2}) == input_hash(
        "t", {"p": q(200.0, "kPa"), "b": q(1.5)}, {"y": 2, "x": 1}
    )


def test_canonical_json_form() -> None:
    data = {"b": [1, True, None, "γ"], "a": (0.1,)}

    assert canonical_json(data) == '{"a":[0.1],"b":[1.0,true,null,"γ"]}'


def test_a_parameter_set_id_covers_every_reference() -> None:
    assert parameter_set_id(entry()) != parameter_set_id(entry(reference=ref(clause="<OTHER>")))


@pytest.mark.parametrize("value", [float("nan"), float("inf"), object()], ids=["nan", "inf", "object"])
def test_a_value_that_cannot_be_hashed_fails(value: Any) -> None:
    with pytest.raises(CalculationError):
        canonical_json({"k": value})


CONTRACT = CalculationTypeContract(
    name="synthetic",
    inputs=(QuantityDeclaration(name="b", label=LocalizedText(ru="b"), symbol="b", base_unit="m"),),
    outputs=(
        OutputDeclaration(
            name="y",
            label=LocalizedText(ru="y"),
            symbol="y",
            base_unit="m",
            rounding_rule=RoundingRule(decimals=2, mode="half_up"),
            rounding_source=EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>"),
        ),
    ),
    checks=("check",),
)


class Identity(Calculator[Mapping[str, QuantityValue], TableValue, None]):
    def calculate(self, inputs: Mapping[str, QuantityValue], parameters: TableValue) -> None:
        return None


def test_the_hash_reads_inputs_after_conversion_to_base_units() -> None:
    in_mm = run(CONTRACT, Identity(), {"b": q(1500.0, "mm")}, entry())
    in_m = run(CONTRACT, Identity(), {"b": q(1.5)}, entry())

    assert in_mm.input_hash == in_m.input_hash == input_hash("synthetic", {"b": q(1.5)}, {
        "parameters": entry(),
        "method_range": (),
        "validated_range": (),
    })


def test_the_ranges_are_part_of_the_resolved_parameter_set() -> None:
    bound = MethodBound(quantity="b", kind="max", value=10.0, inclusive=True, source=(ref(),))

    plain = run(CONTRACT, Identity(), {"b": q(1.5)}, entry())
    bounded = run(CONTRACT, Identity(), {"b": q(1.5)}, entry(), method_range=(bound,))

    assert plain.input_hash != bounded.input_hash


def test_a_refused_run_has_an_input_hash() -> None:
    bound = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(ref(),))

    outcome = run(CONTRACT, Identity(), {"b": q(1.5)}, entry(), method_range=(bound,))

    assert outcome.refusal is not None
    assert re.fullmatch(r"[0-9a-f]{64}", outcome.input_hash)

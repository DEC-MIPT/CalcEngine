import builtins
import io
import os
import random
import socket
import time
import uuid
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel

from app.engine.base import Calculator
from app.engine.pipeline import CalculatorOutput, calculate
from app.engine.steps import check_step, formula_step, table_step
from app.schemas.calculation import (
    CalculationResult,
    CalculationTypeContract,
    MethodBound,
    NormRef,
    OutputDeclaration,
    QuantityDeclaration,
    QuantityValue,
    RoundingRule,
    ValidatedBound,
)
from app.schemas.expression import parse_expression
from app.schemas.parameters import EngineerRule
from app.schemas.resolved import Formula, Selector, TableValue
from app.schemas.text import LocalizedText

REF = NormRef(
    document="<NORM-DOC-PLACEHOLDER>",
    edition="unverified",
    clause="<CLAUSE-PLACEHOLDER>",
    status="unverified",
    provenance="machine-extracted",
)
RULE = EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>")

CONTRACT = CalculationTypeContract(
    name="synthetic",
    inputs=(
        QuantityDeclaration(name="b", label=LocalizedText(ru="b"), symbol="b", base_unit="m"),
        QuantityDeclaration(name="phi", label=LocalizedText(ru="phi"), symbol="phi", base_unit="deg"),
    ),
    outputs=(
        OutputDeclaration(
            name="y",
            label=LocalizedText(ru="y"),
            symbol="y", base_unit="m", rounding_rule=RoundingRule(decimals=2, mode="half_even"), rounding_source=RULE
        ),
    ),
    checks=("check",),
)


class Parameters(BaseModel):
    formula: Formula
    coefficient: TableValue
    limit: QuantityValue


PARAMETERS = Parameters(
    formula=Formula(
        latex=r"y = \sqrt{k} b",
        tree=parse_expression(
            {
                "kind": "mul",
                "left": {"kind": "call", "function": "sqrt", "args": [{"kind": "symbol", "name": "k"}]},
                "right": {"kind": "symbol", "name": "b"},
            }
        ),
        result_symbol="y",
        units={"k": "1", "b": "m", "y": "m"},
        norm_refs=(REF,),
    ),
    coefficient=TableValue(
        symbol="k",
        latex="k",
        value=QuantityValue(value=2.0, unit="1"),
        norm_refs=(REF,),
        selectors=(Selector(symbol="phi", value=QuantityValue(value=20.0, unit="deg")),),
    ),
    limit=QuantityValue(value=10.0, unit="m"),
)

METHOD = (MethodBound(quantity="b", kind="max", value=100.0, inclusive=True, source=(REF,)),)
VALIDATED = (ValidatedBound(quantity="b", kind="max", value=5.0, inclusive=True, source=RULE),)


class SyntheticCalculator(Calculator[Mapping[str, QuantityValue], Parameters, CalculatorOutput]):
    def calculate(self, inputs: Mapping[str, QuantityValue], parameters: Parameters) -> CalculatorOutput:
        k = table_step("k", parameters.coefficient, {"phi": r"\varphi"})
        y = formula_step("y", parameters.formula, {"k": k.result, "b": inputs["b"]})
        check = check_step("check", ("y", y.result), "le", ("y_{max}", parameters.limit), (REF,))
        return CalculatorOutput(trace=(k, y, check), outputs={"y": y.result})


def _forbidden(*args: Any, **kwargs: Any) -> Any:
    raise AssertionError("the calculation touched I/O, the clock or randomness")


@pytest.fixture
def sealed(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    for module, name in [
        (builtins, "open"),
        (io, "open"),
        (os, "open"),
        (os, "stat"),
        (os, "listdir"),
        (os, "urandom"),
        (socket, "socket"),
        (socket, "create_connection"),
        (socket, "getaddrinfo"),
        (time, "time"),
        (time, "time_ns"),
        (time, "monotonic"),
        (random, "random"),
        (random, "randrange"),
        (uuid, "uuid4"),
    ]:
        monkeypatch.setattr(module, name, _forbidden)
    yield


def inputs(b: float) -> dict[str, QuantityValue]:
    return {"b": QuantityValue(value=b, unit="mm"), "phi": QuantityValue(value=20.0, unit="deg")}


def test_the_seal_is_real(sealed: None) -> None:
    for attempt in (
        lambda: Path(__file__).read_text(),
        lambda: socket.create_connection(("localhost", 80)),
        lambda: time.time(),
        lambda: uuid.uuid4(),
    ):
        with pytest.raises(AssertionError, match="touched I/O"):
            attempt()


def test_a_calculation_completes_with_the_filesystem_and_the_network_patched_to_raise(
    sealed: None,
) -> None:
    result = calculate(
        CONTRACT,
        SyntheticCalculator(),
        inputs(6000.0),
        PARAMETERS,
        method_range=METHOD,
        validated_range=VALIDATED,
    )

    assert isinstance(result, CalculationResult)
    assert (result.verdict, len(result.trace), len(result.warnings)) == ("pass", 3, 1)
    assert result.outputs[0].value == 8.49


def test_a_refusal_completes_with_the_filesystem_and_the_network_patched_to_raise(
    sealed: None,
) -> None:
    result = calculate(
        CONTRACT,
        SyntheticCalculator(),
        inputs(200_000.0),
        PARAMETERS,
        method_range=METHOD,
        validated_range=VALIDATED,
    )

    assert isinstance(result, CalculationResult)
    assert result.verdict == "refused"

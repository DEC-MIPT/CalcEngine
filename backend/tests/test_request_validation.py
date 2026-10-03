from collections.abc import Mapping
from typing import Any

import pytest
from pydantic import ValidationError
from sqlalchemy.orm import Session

import app.services.calculation as service_module
from app.core.exceptions import DECError, InputValidationError, NotFoundError
from app.engine.base import Calculator
from app.engine.pipeline import CalculatorOutput
from app.engine.registry import CalculatorRegistry
from app.engine.steps import check_step
from app.repositories.calculation_result import CalculationResultRepository
from app.schemas.calculation import (
    CalculationRequest,
    CalculationTypeContract,
    NormRef,
    OutputDeclaration,
    QuantityDeclaration,
    QuantityValue,
    RoundingRule,
)
from app.schemas.parameters import EngineerRule
from app.services.calculation import CalculationService
from app.services.parameter_source import ResolvedParameters

REF = NormRef(
    document="<NORM-DOC-PLACEHOLDER>",
    edition="unverified",
    clause="<CLAUSE-PLACEHOLDER>",
    status="unverified",
    provenance="machine-extracted",
)

CONTRACT = CalculationTypeContract(
    name="synthetic",
    inputs=(
        QuantityDeclaration(name="b", base_unit="m"),
        QuantityDeclaration(name="p", base_unit="kPa"),
    ),
    outputs=(
        OutputDeclaration(
            name="y",
            base_unit="m",
            rounding_rule=RoundingRule(decimals=2, mode="half_up"),
            rounding_source=EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>"),
        ),
    ),
    checks=("check",),
)


class PassThrough(Calculator[Mapping[str, QuantityValue], None, CalculatorOutput]):
    def calculate(self, inputs: Mapping[str, QuantityValue], parameters: None) -> CalculatorOutput:
        check = check_step("check", ("b", inputs["b"]), "le", ("b", inputs["b"]), (REF,))
        return CalculatorOutput(trace=(check,), outputs={"y": inputs["b"]})


@pytest.fixture
def engine_calls(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    calls: list[str] = []
    original = service_module.calculate

    def spy(contract: CalculationTypeContract, *args: Any, **kwargs: Any) -> Any:
        calls.append(contract.name)
        return original(contract, *args, **kwargs)

    monkeypatch.setattr(service_module, "calculate", spy)
    return calls


class NoParameters:
    def resolve(self, calculation_type: str, inputs: Mapping[str, QuantityValue]) -> ResolvedParameters:
        return ResolvedParameters(parameters=None, method_range=())


@pytest.fixture
def service(sqlite_session: Session) -> CalculationService:
    registry = CalculatorRegistry()
    registry.register(CONTRACT, PassThrough())
    return CalculationService(
        registry,
        sources={"synthetic": NoParameters()},
        results=CalculationResultRepository(sqlite_session),
    )


def request(**inputs: Any) -> dict[str, Any]:
    values = {"b": {"value": 1.5, "unit": "m"}, "p": {"value": 200.0, "unit": "kPa"}}
    return {"calculation_type": "synthetic", "inputs": values | inputs}


def submit(service: CalculationService, data: dict[str, Any]) -> Any:
    return service.submit(CalculationRequest.model_validate(data))


def test_a_valid_request_reaches_the_engine(
    service: CalculationService, engine_calls: list[str]
) -> None:
    envelope = submit(service, request(b={"value": 1500.0, "unit": "mm"}))

    assert engine_calls == ["synthetic"]
    assert envelope.outputs[0].value == 1.5


@pytest.mark.parametrize(
    "data",
    [
        {"inputs": request()["inputs"]},
        {"calculation_type": "", "inputs": request()["inputs"]},
        {"calculation_type": "synthetic", "inputs": [1.5, 200.0]},
        request(b={"value": "one and a half", "unit": "m"}),
        request(b={"value": 1.5}),
        request(b={"value": 1.5, "unit": "m", "comment": "extra"}),
        request() | {"extra": True},
        request(b={"value": float("nan"), "unit": "m"}),
        request(b={"value": float("inf"), "unit": "m"}),
    ],
    ids=[
        "no-type",
        "empty-type",
        "inputs-not-a-mapping",
        "value-not-a-number",
        "no-unit",
        "extra-input-field",
        "extra-request-field",
        "nan",
        "inf",
    ],
)
def test_a_malformed_request_is_rejected_before_the_engine(
    service: CalculationService, engine_calls: list[str], data: dict[str, Any]
) -> None:
    with pytest.raises(ValidationError):
        submit(service, data)

    assert engine_calls == []


def test_a_unit_outside_the_vocabulary_is_rejected_before_the_engine(
    service: CalculationService, engine_calls: list[str]
) -> None:
    with pytest.raises(ValidationError, match="unit vocabulary"):
        submit(service, request(b={"value": 1.5, "unit": "furlong"}))

    assert engine_calls == []


def test_a_unit_of_another_dimension_is_rejected_before_the_engine(
    service: CalculationService, engine_calls: list[str]
) -> None:
    with pytest.raises(InputValidationError, match="'b' is in 'kPa'"):
        submit(service, request(b={"value": 1.5, "unit": "kPa"}))

    assert engine_calls == []


@pytest.mark.parametrize(
    "inputs",
    [{"b": {"value": 1.5, "unit": "m"}}, request(z={"value": 1.0, "unit": "m"})["inputs"]],
    ids=["missing-input", "unknown-input"],
)
def test_inputs_that_do_not_match_the_contract_are_rejected_before_the_engine(
    service: CalculationService, engine_calls: list[str], inputs: dict[str, Any]
) -> None:
    with pytest.raises(InputValidationError, match="declared inputs"):
        submit(service, {"calculation_type": "synthetic", "inputs": inputs})

    assert engine_calls == []


def test_an_unknown_calculation_type_is_rejected_before_the_engine(
    service: CalculationService, engine_calls: list[str]
) -> None:
    with pytest.raises(NotFoundError):
        submit(service, request() | {"calculation_type": "missing"})

    assert engine_calls == []


def test_input_validation_error_is_a_dec_error() -> None:
    assert issubclass(InputValidationError, DECError)

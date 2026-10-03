import datetime
import uuid
from collections.abc import Mapping
from typing import Any

import pytest
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.exceptions import (
    DECError,
    InputValidationError,
    NotFoundError,
    ParameterSourceUnavailableError,
)
from app.engine.base import Calculator
from app.engine.pipeline import CalculatorOutput
from app.engine.registry import CalculatorRegistry
from app.engine.steps import check_step, formula_step
from app.models.calculation_result import CalculationResultRow
from app.repositories.calculation_result import CalculationResultRepository
from app.schemas.api import FieldError
from app.schemas.calculation import (
    CalculationRequest,
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
from app.schemas.resolved import Formula
from app.schemas.stored import NormSource, StoredResult
from app.services.calculation import CalculationService, norm_sources
from app.services.parameter_source import ResolvedParameters


def ref(document: str, clause: str = "<CLAUSE-PLACEHOLDER>") -> NormRef:
    return NormRef(
        document=document,
        edition="unverified",
        clause=clause,
        status="unverified",
        provenance="machine-extracted",
    )


REF = ref("<NORM-DOC-A>")
RULE = EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>")

CONTRACT = CalculationTypeContract(
    name="synthetic",
    inputs=(
        QuantityDeclaration(name="b", base_unit="m"),
        QuantityDeclaration(name="d", base_unit="m"),
        QuantityDeclaration(name="p", base_unit="kPa"),
    ),
    outputs=(
        OutputDeclaration(
            name="y", base_unit="m", rounding_rule=RoundingRule(decimals=2, mode="half_up"), rounding_source=RULE
        ),
    ),
    checks=("check",),
)


class SyntheticParameters(BaseModel):
    formula: Formula
    limit: QuantityValue


PARAMETERS = SyntheticParameters(
    formula=Formula(
        latex=r"y = 2 b",
        tree=parse_expression(
            {"kind": "mul", "left": {"kind": "number", "value": 2}, "right": {"kind": "symbol", "name": "b"}}
        ),
        result_symbol="y",
        units={"b": "m", "y": "m"},
        norm_refs=(REF,),
    ),
    limit=QuantityValue(value=10.0, unit="m"),
)


class SyntheticCalculator(Calculator[Mapping[str, QuantityValue], SyntheticParameters, CalculatorOutput]):
    def calculate(
        self, inputs: Mapping[str, QuantityValue], parameters: SyntheticParameters
    ) -> CalculatorOutput:
        y = formula_step("y", parameters.formula, inputs)
        check = check_step("check", ("y", y.result), "le", ("y_{max}", parameters.limit), (ref("<NORM-DOC-B>"),))
        return CalculatorOutput(trace=(y, check), outputs={"y": y.result})


class FixedSource:
    def __init__(self, method_range: tuple[MethodBound, ...] = ()) -> None:
        self.method_range = method_range
        self.calls: list[tuple[str, dict[str, QuantityValue]]] = []

    def resolve(self, calculation_type: str, inputs: Mapping[str, QuantityValue]) -> ResolvedParameters:
        self.calls.append((calculation_type, dict(inputs)))
        return ResolvedParameters(parameters=PARAMETERS, method_range=self.method_range)


class SpyRepository(CalculationResultRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)
        self.added: list[dict[str, Any]] = []

    def add(self, **record: Any) -> None:
        self.added.append(record)
        super().add(**record)


@pytest.fixture
def results(sqlite_session: Session) -> SpyRepository:
    return SpyRepository(sqlite_session)


def make_service(
    results: CalculationResultRepository | None,
    source: FixedSource | None = None,
    validated_range: tuple[ValidatedBound, ...] = (),
) -> CalculationService:
    registry = CalculatorRegistry()
    registry.register(CONTRACT, SyntheticCalculator())
    return CalculationService(
        registry,
        sources={} if source is None else {"synthetic": source},
        validated_ranges={"synthetic": validated_range},
        results=results,
    )


def request(**inputs: Any) -> CalculationRequest:
    values: dict[str, Any] = {
        "b": {"value": 1.5, "unit": "m"},
        "d": {"value": 2.0, "unit": "m"},
        "p": {"value": 200.0, "unit": "kPa"},
    }
    given = {name: value for name, value in (values | inputs).items() if value is not None}
    return CalculationRequest.model_validate({"calculation_type": "synthetic", "inputs": given})


def test_every_offending_input_is_named_in_one_error() -> None:
    bad = request(b=None, d=None, z={"value": 1.0, "unit": "m"}, p={"value": 1.0, "unit": "m"})

    with pytest.raises(InputValidationError) as raised:
        bad.check_against(CONTRACT)

    message = str(raised.value)
    for text in ("'b' is missing", "'d' is missing", "'z' is not declared", "'p' is in 'm'"):
        assert text in message
    assert raised.value.fields == (
        FieldError(location=("body", "inputs", "b"), message="Missing input."),
        FieldError(location=("body", "inputs", "d"), message="Missing input."),
        FieldError(location=("body", "inputs", "p"), message="Expected a unit of pressure."),
        FieldError(location=("body", "inputs", "z"), message="Undeclared input."),
    )


def test_two_missing_and_one_undeclared_input_give_one_error_naming_all_three() -> None:
    with pytest.raises(InputValidationError) as raised:
        request(b=None, d=None, z={"value": 1.0, "unit": "m"}).check_against(CONTRACT)

    assert raised.value.fields == (
        FieldError(location=("body", "inputs", "b"), message="Missing input."),
        FieldError(location=("body", "inputs", "d"), message="Missing input."),
        FieldError(location=("body", "inputs", "z"), message="Undeclared input."),
    )
    for name in ("'b'", "'d'", "'z'"):
        assert name in str(raised.value)


def test_a_request_that_fits_raises_nothing() -> None:
    request().check_against(CONTRACT)


def test_an_input_error_without_fields_has_none() -> None:
    assert InputValidationError("plain").fields == ()


def test_a_valid_request_is_run_on_the_source_parameters_and_stored(
    results: SpyRepository, engine_calls: list[str], sqlite_session: Session
) -> None:
    source = FixedSource()

    envelope = make_service(results, source).submit(request())

    assert engine_calls == ["synthetic"]
    assert source.calls == [("synthetic", dict(request().inputs))]
    assert envelope.verdict == "pass"
    row = sqlite_session.get(CalculationResultRow, envelope.result_id)
    assert row is not None
    assert row.envelope == envelope.model_dump(mode="json")
    assert row.inputs == {"b": {"value": 1.5, "unit": "m"}, "d": {"value": 2.0, "unit": "m"}, "p": {"value": 200.0, "unit": "kPa"}}


def test_an_unknown_type_calls_neither_the_engine_nor_the_repository(
    results: SpyRepository, engine_calls: list[str]
) -> None:
    unknown = request().model_copy(update={"calculation_type": "missing"})

    with pytest.raises(NotFoundError):
        make_service(results, FixedSource()).submit(unknown)

    assert (engine_calls, results.added) == ([], [])


def test_a_contract_mismatch_calls_neither_the_engine_nor_the_repository(
    results: SpyRepository, engine_calls: list[str]
) -> None:
    source = FixedSource()

    with pytest.raises(InputValidationError):
        make_service(results, source).submit(request(b=None))

    assert (engine_calls, results.added, source.calls) == ([], [], [])


def test_a_type_without_a_source_is_rejected_naming_the_type(
    results: SpyRepository, engine_calls: list[str]
) -> None:
    with pytest.raises(ParameterSourceUnavailableError, match="'synthetic'") as raised:
        make_service(results).submit(request())

    assert isinstance(raised.value, DECError)
    assert (engine_calls, results.added) == ([], [])


def test_the_contract_is_checked_before_the_source(results: SpyRepository) -> None:
    with pytest.raises(InputValidationError):
        make_service(results).submit(request(b=None))


def test_a_refused_calculation_is_stored_with_verdict_refused(
    results: SpyRepository, sqlite_session: Session
) -> None:
    bound = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(REF,))

    envelope = make_service(results, FixedSource(method_range=(bound,))).submit(request())

    assert envelope.verdict == "refused"
    row = sqlite_session.get(CalculationResultRow, envelope.result_id)
    assert row is not None
    assert row.envelope["verdict"] == "refused"


def test_the_validated_range_of_the_type_is_applied(results: SpyRepository) -> None:
    bound = ValidatedBound(quantity="b", kind="max", value=1.0, inclusive=True, source=RULE)

    envelope = make_service(results, FixedSource(), validated_range=(bound,)).submit(request())

    assert envelope.verdict == "pass"
    assert [warning.bound for warning in envelope.warnings] == [bound]


def test_submit_needs_a_result_repository(engine_calls: list[str]) -> None:
    with pytest.raises(RuntimeError, match="result repository"):
        make_service(None, FixedSource()).submit(request())

    assert engine_calls == []


def test_norm_sources_are_distinct_documents_in_first_use_order(results: SpyRepository) -> None:
    envelope = make_service(results, FixedSource()).submit(request())

    assert norm_sources(envelope) == [
        {"document": "<NORM-DOC-A>", "edition": "unverified"},
        {"document": "<NORM-DOC-B>", "edition": "unverified"},
    ]
    assert results.added[0]["norm_sources"] == norm_sources(envelope)


def test_a_document_cited_twice_is_listed_once(results: SpyRepository) -> None:
    envelope = make_service(results, FixedSource()).submit(request())
    twice = envelope.model_copy(update={"norm_refs": (REF, ref("<NORM-DOC-A>", "<OTHER-CLAUSE>"))})

    assert norm_sources(twice) == [{"document": "<NORM-DOC-A>", "edition": "unverified"}]


def test_the_stored_record_holds_every_field_of_the_requirement(results: SpyRepository) -> None:
    service = make_service(results, FixedSource())
    given = request()
    envelope = service.submit(given)

    stored = service.get(envelope.result_id)

    assert isinstance(stored, StoredResult)
    assert stored.result_id == envelope.result_id
    assert stored.calculation_type == "synthetic"
    assert stored.inputs == given.inputs
    assert stored.envelope == envelope
    assert (stored.engine_version, stored.input_hash) == (envelope.engine_version, envelope.input_hash)
    assert isinstance(stored.created_at, datetime.datetime)
    assert stored.norm_sources == (
        NormSource(document="<NORM-DOC-A>", edition="unverified"),
        NormSource(document="<NORM-DOC-B>", edition="unverified"),
    )


def test_a_refused_result_is_read_back_with_its_fields(results: SpyRepository) -> None:
    bound = MethodBound(quantity="b", kind="max", value=1.0, inclusive=True, source=(REF,))
    service = make_service(results, FixedSource(method_range=(bound,)))
    envelope = service.submit(request())

    stored = service.get(envelope.result_id)

    assert stored.envelope == envelope
    assert stored.envelope.verdict == "refused"
    assert stored.norm_sources == (NormSource(document="<NORM-DOC-A>", edition="unverified"),)


def test_re_running_the_stored_inputs_gives_the_same_hash_and_envelope(results: SpyRepository) -> None:
    service = make_service(results, FixedSource())
    stored = service.get(service.submit(request(b={"value": 1500.0, "unit": "mm"})).result_id)

    again = service.submit(
        CalculationRequest(calculation_type=stored.calculation_type, inputs=stored.inputs)
    )

    assert again.input_hash == stored.input_hash
    assert again.result_id != stored.result_id
    assert again.model_dump(exclude={"result_id"}) == stored.envelope.model_dump(exclude={"result_id"})


def test_an_unknown_result_id_is_not_found(results: SpyRepository) -> None:
    with pytest.raises(NotFoundError):
        make_service(results, FixedSource()).get(uuid.uuid4())


def test_get_needs_a_result_repository() -> None:
    with pytest.raises(RuntimeError, match="result repository"):
        make_service(None).get(uuid.uuid4())


def model_objects(value: Any) -> list[object]:
    """Объекты классов из ``app.models`` внутри значения, на любой глубине."""
    found: list[object] = [value] if type(value).__module__.startswith("app.models") else []
    if isinstance(value, BaseModel):
        children: list[Any] = [getattr(value, name) for name in type(value).model_fields]
    elif isinstance(value, Mapping):
        children = [*value.keys(), *value.values()]
    elif isinstance(value, tuple | list):
        children = list(value)
    else:
        children = []
    for child in children:
        found.extend(model_objects(child))
    return found


def test_no_value_the_service_returns_is_an_orm_object(results: SpyRepository) -> None:
    service = make_service(results, FixedSource())
    envelope = service.submit(request())

    assert model_objects(envelope) == []
    assert model_objects(service.get(envelope.result_id)) == []
    assert model_objects([CalculationResultRow()]) != []

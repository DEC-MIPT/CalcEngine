import uuid
from pathlib import Path
from typing import Annotated, Any

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from test_services_catalog import IdentityCalculator, synthetic_contract
from test_services_submit import CONTRACT, FixedSource, SyntheticCalculator, request

from app.api.dependencies import get_service
from app.core.config import PARAMS_ROOT, ApiSettings
from app.core.exceptions import DECError
from app.engine import foundations_shallow_r
from app.engine.registry import CalculatorRegistry
from app.main import create_app
from app.models import Base
from app.parameters.param_schemas import EngineerBound
from app.schemas.calculation import ValidatedBound
from app.schemas.parameters import EngineerRule
from app.services.calculation import CalculationService
from app.services.catalog import build_registry, calculation_types

RULE = EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>")


@pytest.fixture(autouse=True)
def no_database_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEC_APP_DATABASE_URL", raising=False)


def get_types(app: FastAPI) -> tuple[int, Any]:
    with TestClient(app) as client:
        response = client.get("/calculation-types")
    return response.status_code, response.json()


def test_the_registered_types_are_listed_in_contract_order() -> None:
    registry = build_registry(PARAMS_ROOT)

    status, body = get_types(create_app(registry=registry))

    assert status == 200
    assert body == [view.model_dump(mode="json") for view in calculation_types(registry)]
    (pilot,) = body
    assert [item["name"] for item in pilot["inputs"]] == [q.name for q in foundations_shallow_r.INPUTS]
    assert pilot["inputs"][0] == {
        "name": "b",
        "base_unit": "m",
        "dimension": "length",
        "units": ["m", "cm", "mm"],
        "label": {"ru": "Ширина подошвы фундамента", "en": "Foundation base width"},
        "symbol": "b",
        "hint": None,
        "whole_values_only": False,
    }
    assert pilot["outputs"] == [
        {
            "name": "R",
            "base_unit": "kPa",
            "label": {"ru": "Расчётное сопротивление грунта", "en": "Design soil resistance"},
            "symbol": "R",
        }
    ]


def test_an_empty_registry_gives_an_empty_list() -> None:
    assert get_types(create_app(registry=CalculatorRegistry())) == (200, [])


def test_several_types_keep_their_registration_order() -> None:
    registry = CalculatorRegistry()
    registry.register(synthetic_contract("second"), IdentityCalculator())
    registry.register(synthetic_contract("first"), IdentityCalculator())

    _, body = get_types(create_app(registry=registry))

    assert [entry["name"] for entry in body] == ["second", "first"]


def test_the_listing_answers_without_the_database_variable() -> None:
    status, body = get_types(create_app())

    assert status == 200
    assert [entry["name"] for entry in body] == [foundations_shallow_r.NAME]


def test_the_start_up_loads_the_validated_range_of_each_type(tmp_path: Path) -> None:
    (tmp_path / f"{foundations_shallow_r.NAME}.yaml").write_text(
        """\
rounding_rules:
  R:
    rule: {decimals: 1, mode: half_up}
    source: {engineer: "<ENGINEER>", rationale: "<RATIONALE>"}
validated_range:
  - quantity: b
    kind: max
    value: 3.0
    inclusive: true
    source: {engineer: "<ENGINEER>", rationale: "<RATIONALE>"}
""",
        encoding="utf-8",
    )
    application = create_app(ApiSettings.model_validate({"DEC_PARAMS_ROOT": tmp_path}))

    with TestClient(application):
        ranges = application.state.validated_ranges

    assert ranges == {
        foundations_shallow_r.NAME: (
            EngineerBound(quantity="b", kind="max", value=3.0, inclusive=True, source=RULE),
        )
    }


def test_the_pilot_parameter_file_has_an_empty_validated_range() -> None:
    application = create_app()

    with TestClient(application):
        assert application.state.validated_ranges == {foundations_shallow_r.NAME: ()}


def test_a_given_registry_comes_with_the_given_ranges_or_none() -> None:
    bound = ValidatedBound(quantity="b", kind="max", value=1.0, inclusive=True, source=RULE)
    given = create_app(registry=CalculatorRegistry(), validated_ranges={"synthetic": (bound,)})
    bare = create_app(registry=CalculatorRegistry())

    with TestClient(given), TestClient(bare):
        assert given.state.validated_ranges == {"synthetic": (bound,)}
        assert bare.state.validated_ranges == {}


def test_the_service_provider_wires_the_session_the_sources_and_the_ranges() -> None:
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    registry = CalculatorRegistry()
    registry.register(CONTRACT, SyntheticCalculator())
    bound = ValidatedBound(quantity="b", kind="max", value=1.0, inclusive=True, source=RULE)
    application = create_app(
        registry=registry,
        sources={"synthetic": FixedSource()},
        validated_ranges={"synthetic": (bound,)},
        session_factory=sessionmaker(bind=engine),
    )

    @application.post("/submit-for-test")
    def submit_for_test(service: Annotated[CalculationService, Depends(get_service)]) -> dict[str, Any]:
        envelope = service.submit(request())
        return {"id": str(envelope.result_id), "warnings": len(envelope.warnings)}

    @application.get("/read-for-test/{result_id}")
    def read_for_test(
        result_id: uuid.UUID, service: Annotated[CalculationService, Depends(get_service)]
    ) -> dict[str, str]:
        return {"verdict": service.get(result_id).envelope.verdict}

    with TestClient(application) as client:
        created = client.post("/submit-for-test").json()
        stored = client.get(f"/read-for-test/{created['id']}")
        unknown = client.get(f"/read-for-test/{uuid.uuid4()}")

    assert created["warnings"] == 1
    assert (stored.status_code, stored.json()) == (200, {"verdict": "pass"})
    assert (unknown.status_code, unknown.json()["code"]) == (404, "not_found")


def test_a_session_is_not_opened_by_the_listing(monkeypatch: pytest.MonkeyPatch) -> None:
    opened: list[Session] = []
    engine = create_engine("sqlite://", poolclass=StaticPool)

    class CountingSession(Session):
        def __init__(self, **kwargs: Any) -> None:
            super().__init__(**kwargs)
            opened.append(self)

    application = create_app(
        registry=CalculatorRegistry(), session_factory=sessionmaker(bind=engine, class_=CountingSession)
    )

    assert get_types(application) == (200, [])
    assert opened == []


def test_a_validated_range_bound_without_its_engineer_stops_the_start_up(tmp_path: Path) -> None:
    (tmp_path / f"{foundations_shallow_r.NAME}.yaml").write_text(
        """\
rounding_rules:
  R:
    rule: {decimals: 1, mode: half_up}
    source: {engineer: "<ENGINEER>", rationale: "<RATIONALE>"}
validated_range:
  - quantity: b
    kind: max
    value: 3.0
    inclusive: true
    source: {rationale: "<RATIONALE>"}
""",
        encoding="utf-8",
    )
    application = create_app(ApiSettings.model_validate({"DEC_PARAMS_ROOT": tmp_path}))

    with pytest.raises(DECError) as raised, TestClient(application):
        pass

    assert f"{foundations_shallow_r.NAME}.yaml" in str(raised.value)
    assert "validated_range.0.source.engineer" in str(raised.value)

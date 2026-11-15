import json
import random
from collections.abc import Iterator
from datetime import date
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from test_api_calculations import DOCX, REPORT_BODY
from test_reporting_docx import read_back

from app.core.config import INTERIM_ROOT, PARAMS_ROOT
from app.engine.foundations_shallow_loads import (
    CHECKS,
    NAME,
    OUTPUTS,
    Parameters,
    pressure_steps,
)
from app.main import create_app
from app.models import Base
from app.reporting import docx_writer
from app.schemas.calculation import CalculationResult, QuantityValue, ResultEnvelope
from app.services.catalog import build_registry, load_validated_ranges
from app.services.interim_source import interim_sources
from app.verification import runner
from app.verification.metrics import deviations, reproducibility, traceability
from app.verification.models import ReferenceExample, parse_examples
from app.verification.runner import ExampleParameters, run_example, run_reference_suite

FIXTURE = Path(__file__).parent / "fixtures" / "foundations_loads_references.json"
EXAMPLES = tuple(ReferenceExample.model_validate(item) for item in json.loads(FIXTURE.read_text()))


def payload(case: int = 0, /, **changes: tuple[float, str]) -> dict[str, Any]:
    given = EXAMPLES[case].model_dump(mode="json")["inputs"]
    given.update({name: {"value": value, "unit": unit} for name, (value, unit) in changes.items()})
    return {"calculation_type": NAME, "inputs": given}


@pytest.fixture
def client() -> Iterator[TestClient]:
    registry = build_registry(PARAMS_ROOT)
    sources = interim_sources(registry, INTERIM_ROOT, "strict", date(2026, 11, 15))
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    try:
        with TestClient(create_app(
            registry=registry, sources=sources,
            validated_ranges=load_validated_ranges(registry, PARAMS_ROOT),
            session_factory=sessionmaker(bind=engine),
        )) as test_client:
            yield test_client
    finally:
        engine.dispose()


def test_approved_references_run_independently_and_report_metrics() -> None:
    registry = build_registry(PARAMS_ROOT)
    source = interim_sources(registry, INTERIM_ROOT, "strict", date(2026, 11, 15))[NAME]

    def resolve(example: ReferenceExample) -> ExampleParameters:
        result = source.resolve(NAME, example.inputs)
        return ExampleParameters(result.parameters, result.method_range)

    report = run_reference_suite(parse_examples(json.loads(FIXTURE.read_text())), [NAME], registry, resolve)
    assert report.invalid == ()
    assert [run.outcome for run in report.runs] == ["passed"] * 3
    assert reproducibility(report).rate == 1
    assert len(deviations(report)) == 30
    assert all(abs(item.deviation or 0) <= 0.005 for item in deviations(report))
    measured = traceability(report)
    assert measured.completeness == 0
    assert measured.engineer_rules > 0
    assert measured.steps == sum(
        step.kind != "engineer_formula" for run in report.runs if run.result for step in run.result.trace
    )
    assert [example.origin for example in EXAMPLES] == ["manual calculation"] * 3
    for example in EXAMPLES:
        assert "27258b6d18d3d928f26976e3c9876f78fa4640cba4ff26d83b04035d7dbc55ea" in example.citation.locator  # pragma: allowlist secret
        assert "Akim 2026-11-14" in example.citation.document
        assert tuple(example.expected_outputs) == OUTPUTS
        assert all(value.tolerance == 0.005 and value.tolerance_kind == "absolute" for value in example.expected_outputs.values())


@pytest.mark.parametrize("case", range(3), ids=["C", "X", "XY"])
def test_approved_reference_roundtrips_through_api_and_docx(client: TestClient, case: int) -> None:
    response = client.post("/calculations", json=payload(case))
    assert response.status_code == 201, response.text
    body = response.json()
    assert client.get(response.headers["location"]).json() == body
    result = ResultEnvelope.model_validate(body)
    assert result.verdict == "pass"
    assert tuple(output.quantity for output in result.outputs) == OUTPUTS
    for output in result.outputs:
        assert output.unit == "kPa"
        assert output.value == pytest.approx(EXAMPLES[case].expected_outputs[output.quantity].value, abs=0.005, rel=0)
    checks = [step for step in result.trace if step.kind == "check"]
    assert tuple(step.step_id for step in checks) == CHECKS
    assert [step.result.value for step in checks] == [
        [120, 120, 120, 120], [120, 150, 120, 150], [120, 150, 135, 165],
    ][case]
    assert [step.right.value for step in checks] == pytest.approx([152.02, 182.424, 182.424, 228.03])
    assert all(step.passed for step in checks)
    assert result.verdict_reason.kind == "check"
    assert result.verdict_reason.step_id == CHECKS[-1]
    report = client.post(f"/calculations/{result.result_id}/report", json=REPORT_BODY)
    assert (report.status_code, report.headers["content-type"]) == (200, DOCX)
    paragraphs, rows = read_back(report.content)
    text = "\n".join(paragraphs)
    assert "x=b, y=l" in text
    assert "N не включает собственный вес" in text
    assert "Эти величины независимы" in text
    assert "Инженерная формула" in text
    assert len(rows) == 16
    assert "Все проверки выполнены." in text
    assert result.parameter_source is not None
    assert result.parameter_source.profile == "strict"
    assert result.parameter_source.data_sha256 is not None
    assert result.parameter_source.data_sha256 in text
    for output in result.outputs:
        number = f"{output.value:.2f}".replace(".", ",")
        assert number in text


@pytest.mark.parametrize(
    ("moment_unit", "moment_scale", "force_unit", "force_scale"),
    [("N*m", 1000, "N", 1000), ("MN*m", 0.001, "MN", 0.001), ("kN*m", 1, "kN", 1),
     ("N*m", 1000, "kN", 1), ("MN*m", 0.001, "kN", 1),
     ("kN*m", 1, "N", 1000), ("kN*m", 1, "MN", 0.001)],
)
def test_force_and_moment_units_convert_through_api_independently(
    client: TestClient, moment_unit: str, moment_scale: float, force_unit: str, force_scale: float,
) -> None:
    baseline = client.post("/calculations", json=payload(2)).json()
    converted = client.post("/calculations", json=payload(
        2, Mx=(40 * moment_scale, moment_unit), My=(-30 * moment_scale, moment_unit),
        N=(600 * force_scale, force_unit), Qx=(20 * force_scale, force_unit), Qy=(-15 * force_scale, force_unit),
    ))
    assert converted.status_code == 201, converted.text
    body = converted.json()
    assert body["input_hash"] == baseline["input_hash"]
    assert body["trace"] == baseline["trace"]
    assert body["outputs"] == baseline["outputs"]


@pytest.mark.parametrize(
    ("changes", "corner", "minimum"),
    [({"Mx": (200, "kN*m"), "My": (300, "kN*m")}, "mm", -80),
     ({"Mx": (242, "kN*m")}, "mp", -1),
     ({"Mx": (-242, "kN*m")}, "pp", -1)],
)
def test_contact_refusal_is_saved_diagnostic_and_available_as_docx(
    client: TestClient, changes: dict[str, tuple[float, str]], corner: str, minimum: float,
) -> None:
    response = client.post("/calculations", json=payload(**changes))
    assert response.status_code == 201, response.text
    body = response.json()
    assert client.get(response.headers["location"]).json() == body
    assert body["verdict"] == "refused"
    assert body["outputs"] == []
    assert not any(step["kind"] == "check" for step in body["trace"])
    reason = body["verdict_reason"]
    assert reason["kind"] == "derived"
    assert reason["limiting_corner"] == corner
    assert reason["value"] == {"value": minimum, "unit": "kPa"}
    assert reason["check_id"] == "full_contact"
    report = client.post(f"/calculations/{body['result_id']}/report", json=REPORT_BODY)
    assert report.status_code == 200, report.text
    paragraphs, _ = read_back(report.content)
    text = "\n".join(paragraphs)
    assert "Диагностическая трасса" in text
    assert "Проверки несущей способности не выполнялись" in text
    assert f"определяющий угол: {corner}" in text
    assert "Все проверки выполнены." not in text
    assert "Проверка не выполнена." not in text
    assert docx_writer.REFUSED_TRACE not in text


def test_zero_contact_is_completed_and_not_treated_as_a_refusal(client: TestClient) -> None:
    response = client.post("/calculations", json=payload(Mx=(240, "kN*m")))
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["verdict"] != "refused"
    outputs = {output["quantity"]: output["value"] for output in body["outputs"]}
    assert outputs["p_corner_mp"] == outputs["p_corner_mm"] == 0
    assert len([step for step in body["trace"] if step["kind"] == "check"]) == 4


def test_method_bound_refusal_retains_the_historical_empty_shape(client: TestClient) -> None:
    response = client.post("/calculations", json=payload(d_b=(2.001, "m")))
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["verdict"] == "refused"
    assert body["verdict_reason"]["kind"] == "bound"
    assert body["verdict_reason"]["bound"]["quantity"] == "d_b"
    assert body["trace"] == body["outputs"] == []
    assert client.get(response.headers["location"]).json() == body
    report = client.post(f"/calculations/{body['result_id']}/report", json=REPORT_BODY)
    assert report.status_code == 200
    paragraphs, _ = read_back(report.content)
    assert docx_writer.REFUSED_TRACE in paragraphs


@pytest.mark.parametrize(
    ("change", "field"),
    [({"b": (4, "m")}, "b"), ({"phi_II": (20.5, "deg")}, "phi_II"),
     ({"h": (-1, "m")}, "h"), ({"N": (-1, "kN")}, "N"), ({"d": (0, "m")}, "d")],
)
def test_invalid_engineering_inputs_return_422_with_named_fields(
    client: TestClient, change: dict[str, tuple[float, str]], field: str,
) -> None:
    response = client.post("/calculations", json=payload(**change))
    assert response.status_code == 422, response.text
    assert response.json()["code"] == "invalid_input"
    assert ["body", "inputs", field] in [item["location"] for item in response.json()["fields"]]


@pytest.mark.parametrize(
    ("field", "value"),
    [("limiting_corner", "mm"), ("step_id", "missing"), ("related_inputs", ["unknown"]),
     ("value", {"value": -2, "unit": "kPa"}), ("source", {"engineer": "unknown", "rationale": "unknown"})],
)
def test_corrupted_saved_contact_diagnostic_is_rejected(client: TestClient, field: str, value: Any) -> None:
    body = client.post("/calculations", json=payload(Mx=(242, "kN*m"))).json()
    body["verdict_reason"][field] = value
    with pytest.raises(ValidationError):
        ResultEnvelope.model_validate(body)


def test_accountability_prints_derived_refusal_source_when_enabled(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(docx_writer, "ACCOUNTABILITY_SECTION", True)
    body = client.post("/calculations", json=payload(Mx=(-242, "kN*m"))).json()
    report = client.post(f"/calculations/{body['result_id']}/report", json=REPORT_BODY)
    assert report.status_code == 200
    text = "\n".join(read_back(report.content)[0])
    assert "Подотчётность результата" in text
    assert "условие полного контакта full_contact; угол pp" in text
    assert "Источник нормативных параметров:" in text


def test_public_metadata_lists_fifteen_inputs_and_ten_outputs(client: TestClient) -> None:
    detail = next(item for item in client.get("/calculation-types").json() if item["name"] == NAME)
    assert [item["name"] for item in detail["inputs"]] == list(EXAMPLES[0].inputs)
    assert [item["name"] for item in detail["outputs"]] == list(OUTPUTS)
    units = {item["name"]: item["units"] for item in detail["inputs"]}
    assert units["Mx"] == ["N*m", "kN*m", "MN*m"]
    assert "m3" not in {item["base_unit"] for item in detail["inputs"]}
    assert all(QuantityValue(value=1, unit=unit) for unit in units["Mx"])


def test_seeded_pressure_invariants_preserve_axes_signs_and_transfer() -> None:
    generator = random.Random(20261115)
    registry = build_registry(PARAMS_ROOT)
    source = interim_sources(registry, INTERIM_ROOT, "strict", date(2026, 11, 15))[NAME]
    for _ in range(32):
        width = generator.uniform(0.5, 5)
        height = generator.uniform(0, 3)
        given = dict(EXAMPLES[0].inputs)
        given.update({
            "b": QuantityValue(value=width, unit="m"),
            "l": QuantityValue(value=width + generator.uniform(0, 5), unit="m"),
            "h": QuantityValue(value=height, unit="m"),
            "N": QuantityValue(value=generator.uniform(0, 2000), unit="kN"),
            "Mx": QuantityValue(value=generator.uniform(-200, 200), unit="kN*m"),
            "My": QuantityValue(value=generator.uniform(-200, 200), unit="kN*m"),
            "Qx": QuantityValue(value=generator.uniform(-100, 100), unit="kN"),
            "Qy": QuantityValue(value=generator.uniform(-100, 100), unit="kN"),
        })
        resolved = source.resolve(NAME, given)
        assert isinstance(resolved.parameters, Parameters)
        trace, values, corner = pressure_steps(given, resolved.parameters)
        assert pressure_steps(given, resolved.parameters) == (trace, values, corner)
        corners = [values[f"p_corner_{suffix}"].value for suffix in ("pp", "pm", "mp", "mm")]
        assert sum(corners) == pytest.approx(4 * values["p"].value)
        for axis in ("x", "y"):
            assert values[f"p_{axis}_min"].value + values[f"p_{axis}_max"].value == pytest.approx(2 * values["p"].value)
        swapped = given | {"b": given["l"], "l": given["b"], "Mx": given["My"], "My": given["Mx"], "Qx": given["Qy"], "Qy": given["Qx"]}
        _, swapped_values, _ = pressure_steps(swapped, resolved.parameters)
        for name, other in (("p_x_min", "p_y_min"), ("p_x_max", "p_y_max"), ("p_corner_pm", "p_corner_mp"), ("p_corner_pp", "p_corner_pp")):
            assert values[name].value == pytest.approx(swapped_values[other].value)
        inverted = given | {name: QuantityValue(value=-given[name].value, unit=given[name].unit) for name in ("Mx", "My", "Qx", "Qy")}
        _, inverted_values, _ = pressure_steps(inverted, resolved.parameters)
        for original, reflected in (("pp", "mm"), ("pm", "mp"), ("mp", "pm"), ("mm", "pp")):
            assert values[f"p_corner_{original}"].value == pytest.approx(inverted_values[f"p_corner_{reflected}"].value)
        transferred = given | {
            "Mx": values["Mx_base"], "My": values["My_base"], "h": QuantityValue(value=0, unit="m"),
        }
        _, transferred_values, _ = pressure_steps(transferred, resolved.parameters)
        for name in OUTPUTS[1:]:
            assert values[name].value == pytest.approx(transferred_values[name].value)
        cancelled = given | {
            "Mx": QuantityValue(value=-given["Qx"].value * height, unit="kN*m"),
            "My": QuantityValue(value=-given["Qy"].value * height, unit="kN*m"),
        }
        _, cancelled_values, _ = pressure_steps(cancelled, resolved.parameters)
        assert all(cancelled_values[name].value == cancelled_values["p"].value for name in OUTPUTS[1:])


def test_loads_reference_metrics_use_unrounded_pressure() -> None:
    registry = build_registry(PARAMS_ROOT)
    source = interim_sources(registry, INTERIM_ROOT, "strict", date(2026, 11, 15))[NAME]
    raw = EXAMPLES[0].model_dump(mode="json")
    raw["inputs"]["N"]["value"] = 600.0294
    raw["expected_outputs"]["p"]["value"] = 119.999
    example = ReferenceExample.model_validate(raw)

    def resolve(item: ReferenceExample) -> ExampleParameters:
        resolved = source.resolve(NAME, item.inputs)
        return ExampleParameters(resolved.parameters, resolved.method_range)

    run = run_example(example, registry, resolve)
    assert run.result is not None
    assert next(value.value for value in run.result.outputs if value.quantity == "p") == 120.0
    pressure = next(check for check in run.checks if check.quantity == "p")
    assert pressure.computed is not None
    assert pressure.computed.value == pytest.approx(120.0049)
    assert pressure.outcome == "outside"
    assert run.outcome == "failed"


def test_loads_reference_gate_refuses_to_use_display_when_raw_trace_output_is_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    registry = build_registry(PARAMS_ROOT)
    source = interim_sources(registry, INTERIM_ROOT, "strict", date(2026, 11, 15))[NAME]
    original = runner.calculate

    def without_pressure(*args: Any, **kwargs: Any) -> CalculationResult:
        result = original(*args, **kwargs)
        return result.model_copy(update={"trace": tuple(step for step in result.trace if step.step_id != "p")})

    def resolve(item: ReferenceExample) -> ExampleParameters:
        resolved = source.resolve(NAME, item.inputs)
        return ExampleParameters(resolved.parameters, resolved.method_range)

    monkeypatch.setattr(runner, "calculate", without_pressure)
    run = run_example(EXAMPLES[0], registry, resolve)
    assert run.outcome == "failed"
    pressure = next(check for check in run.checks if check.quantity == "p")
    assert pressure.outcome == "missing"
    assert pressure.computed is None


def test_zero_resistance_from_prepared_table_does_not_require_division_by_resistance(client: TestClient) -> None:
    response = client.post("/calculations", json=payload(
        phi_II=(0, "deg"), d_1=(0, "m"), d_b=(0, "m"), c_II=(0, "kPa"),
    ))
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["verdict"] == "fail"
    assert body["verdict_reason"] == {"kind": "check", "step_id": "p_le_R"}
    assert next(output["value"] for output in body["outputs"] if output["quantity"] == "R") == 0
    checks = [step for step in body["trace"] if step["kind"] == "check"]
    assert len(checks) == 4
    assert all(step["right"]["value"] == 0 for step in checks)

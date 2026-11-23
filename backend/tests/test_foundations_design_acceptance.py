import json
import platform
import re
from collections.abc import Iterator, Sequence
from datetime import date
from io import BytesIO
from pathlib import Path
from time import perf_counter
from unittest.mock import patch

import pytest
from docx import Document
from docx.oxml.ns import qn
from docx.table import _Cell
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import INTERIM_ROOT, PARAMS_ROOT
from app.main import create_app
from app.models import Base
from app.services.catalog import build_registry, load_validated_ranges
from app.services.interim_source import InterimParameterSource, interim_sources
from app.verification.metrics import deviations, reproducibility, traceability
from app.verification.models import ReferenceExample, parse_examples
from app.verification.runner import ExampleParameters, run_reference_suite

FIXTURES = Path(__file__).parent / "fixtures"
REFERENCES = tuple(
    ReferenceExample.model_validate(item)
    for item in json.loads((FIXTURES / "foundations_weights_references.json").read_text())
)
AVERAGED = ReferenceExample.model_validate(
    json.loads((FIXTURES / "foundations_loads_references.json").read_text())[0]
)
REPORT = {
    "title": {"designation": "DEC", "document_name": "Acceptance", "organization": "DEC"},
    "signature_block": False,
}


def test_approved_weights_references_run_independently_and_report_metrics() -> None:
    registry = build_registry(PARAMS_ROOT)
    source = interim_sources(registry, INTERIM_ROOT, "strict", date(2026, 11, 15))[
        "foundations_shallow_weights"
    ]

    def resolve(example: ReferenceExample) -> ExampleParameters:
        result = source.resolve(example.calculation_type, example.inputs)
        return ExampleParameters(result.parameters, result.method_range)

    parsed = parse_examples(json.loads((FIXTURES / "foundations_weights_references.json").read_text()))
    report = run_reference_suite(
        parsed, ["foundations_shallow_weights"], registry, resolve,
    )
    assert report.invalid == ()
    assert [run.outcome for run in report.runs] == ["passed"] * 3
    assert reproducibility(report).rate == 1
    measured = deviations(report)
    assert len(measured) == 30
    assert all(item.deviation is not None and abs(item.deviation) <= 0.005 for item in measured)
    trace = traceability(report)
    assert trace.completeness == 0
    assert trace.engineer_rules > 0
    assert trace.steps == sum(
        step.kind != "engineer_formula"
        for run in report.runs if run.result for step in run.result.trace
    )
    assert all("24044046751e1024b457deef3ca4f99fb9bc8cb261e741ce43cb2f928cbe5578" in example.citation.locator  # pragma: allowlist secret
               for example in REFERENCES)
    assert all(example.origin == "manual calculation" for example in REFERENCES)


@pytest.fixture
def acceptance_client() -> Iterator[TestClient]:
    registry = build_registry(PARAMS_ROOT)
    sources = interim_sources(registry, INTERIM_ROOT, "strict", date(2026, 11, 15))
    engine = create_engine(
        "sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    try:
        with TestClient(create_app(
            registry=registry, sources=sources, session_factory=sessionmaker(engine),
            validated_ranges=load_validated_ranges(registry, PARAMS_ROOT),
        )) as client:
            yield client
    finally:
        engine.dispose()


def math_text(cell: _Cell) -> str:
    assert cell._tc.xpath(".//m:oMath")
    assert not cell.text
    return "".join(node.text or "" for node in cell._tc.iter(qn("m:t"))).replace("\xa0", " ").replace("−", "-")


@pytest.mark.parametrize("reference", REFERENCES, ids=lambda reference: reference.example_id)
def test_admitted_weights_api_stored_context_and_docx(
    acceptance_client: TestClient, reference: ReferenceExample,
) -> None:
    response = acceptance_client.post("/calculations", json={
        "calculation_type": reference.calculation_type,
        "inputs": {name: quantity.model_dump() for name, quantity in reference.inputs.items()},
    })
    assert response.status_code == 201, response.text
    envelope = response.json()
    outputs = {item["quantity"]: item for item in envelope["outputs"]}
    assert outputs.keys() == reference.expected_outputs.keys()
    for name, expected in reference.expected_outputs.items():
        assert outputs[name]["value"] == pytest.approx(expected.value, abs=0.005, rel=0)
        assert outputs[name]["unit"] == expected.unit
    assert envelope["verdict"] == "pass"
    result_id = envelope["result_id"]
    with patch.object(InterimParameterSource, "resolve", side_effect=AssertionError("stored evidence must not recalculate")):
        assert acceptance_client.get(response.headers["Location"]).json() == envelope
        context_response = acceptance_client.get(f"/foundation-calculations/{result_id}/context")
        assert context_response.status_code == 200
        context = context_response.json()["context"]
        report = acceptance_client.post(f"/calculations/{result_id}/report", json=REPORT)
    assert context["weight_mode"] == "explicit"
    assert context["methodology_version"] == "rectangular-explicit-weights-v1"
    assert context["pressure_state"] == "full_contact"
    assert "d" not in context["inputs"]
    for corner in context["corners"]:
        expected = reference.expected_outputs[f"p_corner_{corner['name']}"]
        assert corner["pressure"]["value"] == pytest.approx(expected.value, abs=0.005, rel=0)
        assert corner["step_id"] == f"p_corner_{corner['name']}"
    assert report.status_code == 200, report.text
    document = Document(BytesIO(report.content))
    assert len(document.inline_shapes) == 1
    report_text = "".join(node.text or "" for node in document.element.body.iter(qn("w:t"), qn("m:t")))
    assert f"{reference.expected_outputs['R'].value:.2f}".replace(".", ",") in report_text
    inputs, loads, geometry, trace, corners = document.tables
    assert len(inputs.rows) == len(reference.inputs) + 1
    assert len(geometry.rows) == 6
    quantities = {math_text(row.cells[0]): math_text(row.cells[1]) for row in trace.rows[1:]}
    assert f"{reference.expected_outputs['p'].value:.2f}".replace(".", ",") in quantities["p"]
    loads_text = [math_text(row.cells[1]) for row in loads.rows[1:]]
    for name in ("G_fund", "G_soil", "G_other", "Mx_add_base", "My_add_base"):
        number = f"{reference.inputs[name].value:.2f}".replace(".", ",")
        assert any(text.startswith(number + " ") for text in loads_text)
    assert [row.cells[0].text for row in corners.rows[1:]] == ["pp", "pm", "mp", "mm"]
    for row in corners.rows[1:]:
        for cell in row.cells[1:4]:
            assert re.fullmatch(r"[-−]?\d+,\d{2}", math_text(cell))
        actual = math_text(row.cells[3]).replace(",", ".").replace("−", "-")
        assert float(actual) == pytest.approx(reference.expected_outputs[f"p_corner_{row.cells[0].text}"].value, abs=0.005, rel=0)
    formulas = [p for p in document.paragraphs if p.text.startswith("Выражение: ")]
    assert len(formulas) == len(envelope["trace"])
    assert all(p._p.xpath("./m:oMath") and p.text == "Выражение: " for p in formulas)
    step_headers = [p.text for p in document.paragraphs if re.match(r"^\d+\. ", p.text)]
    assert [int(header.split('.', 1)[0]) for header in step_headers] == list(range(1, len(formulas) + 1))
    checks = [p for p in document.paragraphs if p.text.startswith("Сравнение:")]
    assert len(checks) == 4 and all(p._p.xpath('./m:oMath') for p in checks)
    assert [p.text.endswith(' — выполнено') for p in checks] == [
        step['passed'] for step in envelope['trace'] if step['kind'] == 'check'
    ]
    assert "Выходные величины" in report_text
    assert "решение инженера Аким:" not in report_text
    rationales = [p for p in document.paragraphs if p.text.startswith("Обоснование инженерной формулы:")]
    engineer_steps = [step for step in envelope["trace"] if step["kind"] == "engineer_formula"]
    assert len(rationales) == len(engineer_steps)
    for paragraph, step in zip(rationales, engineer_steps, strict=True):
        assert step['source']['rationale'].split(":", 1)[0] in paragraph.text
        if '=' in step['source']['rationale']:
            assert '=' not in paragraph.text and paragraph._p.xpath('./m:oMath')
    overall_refs = [p.text for p in document.paragraphs if p.text.startswith("Нормативные ссылки расчёта:")]
    assert len(overall_refs) == 1 and overall_refs[0].count("СП 22.13330.2016") == 1
    assert all("таблица 5.4" in text and "формула (5.7)" in text for text in overall_refs)


def selection_body(sizes: Sequence[tuple[float, float]]) -> dict:
    return {
        "common_inputs": {
            name: value.model_dump() for name, value in AVERAGED.inputs.items()
            if name not in ("b", "l")
        },
        "candidates": [
            {"b": {"value": b, "unit": "m"}, "l": {"value": l, "unit": "m"}}
            for b, l in sizes
        ],
    }


def test_exhaustive_list_uses_independent_pressure_and_resistance_controls(
    acceptance_client: TestClient,
) -> None:
    sizes = [(1.5, 2), (2, 2), (1.5, 3), (2, 3), (1.5, 4), (2, 4)]
    response = acceptance_client.post("/foundation-selections", json=selection_body(sizes))
    assert response.status_code == 201, response.text
    result = response.json()
    assert result["status"] == "selected"
    passing: list[int] = []
    for index, ((b, l), outcome) in enumerate(zip(sizes, result["outcomes"], strict=True)):
        expected_p = 600 / (b * l) + 20
        expected_r = 1.1 * (0.51 * b * 20 + 3.06 * 20 + 5.66 * 10)
        envelope = outcome["envelope"]
        outputs = {item["quantity"]: item["value"] for item in envelope["outputs"]}
        assert outputs["p"] == pytest.approx(expected_p, abs=0.005, rel=0)
        assert outputs["R"] == pytest.approx(expected_r, abs=0.005, rel=0)
        expected_pass = expected_p <= expected_r
        assert envelope["verdict"] == ("pass" if expected_pass else "fail")
        if expected_pass:
            passing.append(index)
    expected_index = min(passing, key=lambda index: (sizes[index][0] * sizes[index][1], index))
    assert expected_index == 3
    assert result["selected_candidate_index"] == expected_index
    assert result["selected_result_id"] == result["outcomes"][expected_index]["envelope"]["result_id"]


def test_256_candidate_api_runtime_measurement(acceptance_client: TestClient) -> None:
    start = perf_counter()
    response = acceptance_client.post("/foundation-selections", json=selection_body([(2, 3)] * 256))
    elapsed = perf_counter() - start
    cpu = next(
        (line.partition(":")[2].strip() for line in Path("/proc/cpuinfo").read_text().splitlines()
         if line.startswith("model name")),
        platform.machine(),
    )
    Path("/tmp/dec-design-acceptance-status.txt").write_text(
        f"candidate_count=256\nboundary=TestClient POST /foundation-selections including "
        f"validation, source resolution, sequential calculation, SQLite persistence and response serialization\n"
        f"elapsed_seconds={elapsed:.6f}\nhttp_status={response.status_code}\n"
        f"cpu={cpu}\nplatform={platform.platform()}\npython={platform.python_version()}\n"
        f"postgres_migration_reversibility=unverified; no isolated configured PostgreSQL database\n",
    )
    assert response.status_code == 201, response.text
    result = response.json()
    assert result["status"] == "selected"
    assert result["selected_candidate_index"] == 0
    assert len(result["outcomes"]) == 256
    assert all(item["status"] == "evaluated" for item in result["outcomes"])
    assert len({item["envelope"]["result_id"] for item in result["outcomes"]}) == 256

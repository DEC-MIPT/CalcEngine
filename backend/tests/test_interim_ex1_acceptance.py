import logging

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from test_api_calculations import DOCX, REPORT_BODY
from test_reporting_docx import read_back

from app.core.config import INTERIM_ROOT, PARAMS_ROOT, ApiSettings
from app.engine import foundations_shallow_r as pilot
from app.main import create_app
from app.models import Base
from app.parameters.interim_loader import load_interim_root
from app.services.interim_data import document_digest


def test_ex1_uses_real_strict_interim_data_through_the_api_and_docx(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """Check foundations-r-linovskiy2023-ex1 from the reference-example card.

    Source: docs/decisions/reference-examples-foundations.md, ex1, Linovskiy and
    Yakushkina (2023), Example 1, pp. 7-9. The guide supplies phi_II = 19 degrees
    and mean pressure p = 189.5 kPa in addition to the card's inputs. Akim's
    2026-10-28 answer sets the absolute R tolerance to 0.005 kPa and confirms
    that amendment 5 did not change formula (5.7), making ex1 an acceptance gate.
    """
    monkeypatch.setenv("DEC_PARAMETER_SOURCE", "interim")
    monkeypatch.setenv("DEC_INTERIM_PROFILE", "strict")
    monkeypatch.setenv("DEC_INTERIM_ROOT", str(INTERIM_ROOT))
    (document,) = load_interim_root(INTERIM_ROOT, {pilot.NAME})
    digest = document_digest(document)
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    application = create_app(
        ApiSettings.model_validate({"DEC_PARAMS_ROOT": PARAMS_ROOT}),
        session_factory=sessionmaker(bind=engine),
    )
    request = {
        "calculation_type": pilot.NAME,
        "inputs": {
            "b": {"value": 2.1, "unit": "m"},
            "d_1": {"value": 1.5, "unit": "m"},
            "d_b": {"value": 0.0, "unit": "m"},
            "gamma_II": {"value": 18.74, "unit": "kN/m3"},
            "gamma_II_prime": {"value": 18.74, "unit": "kN/m3"},
            "c_II": {"value": 16.0, "unit": "kPa"},
            "phi_II": {"value": 19.0, "unit": "deg"},
            "p": {"value": 189.5, "unit": "kPa"},
        },
    }
    try:
        with caplog.at_level(logging.WARNING), TestClient(application) as client:
            response = client.post("/calculations", json=request)
            assert response.status_code == 201, response.json()
            envelope = response.json()
            assert envelope["verdict"] == "pass"
            assert envelope["parameter_source"] == {
                "kind": "interim", "profile": "strict", "data_sha256": digest,
            }
            (output,) = envelope["outputs"]
            assert (output["quantity"], output["unit"]) == ("R", "kPa")
            assert output["value"] == pytest.approx(206.16, abs=0.005, rel=0)
            assert client.get(response.headers["location"]).json() == envelope

            report = client.post(f"/calculations/{envelope['result_id']}/report", json=REPORT_BODY)
            assert report.status_code == 200
            assert report.headers["content-type"] == DOCX
            paragraphs, _ = read_back(report.content)
            source_line = (
                "Источник нормативных параметров: временные нормативные данные, профиль strict,"
                f" SHA-256 данных {digest}."
            )
            assert paragraphs.count(source_line) == 1
        assert not any(
            code in record.message
            for record in caplog.records
            if f"/{pilot.NAME}.yaml" in record.message
            for code in ("interim_record_unchecked", "interim_value_changed")
        )
    finally:
        engine.dispose()

from collections import Counter
from datetime import date
from hashlib import sha256

import pytest
import yaml
from test_engine_foundations_shallow_r import ROUNDING, RULE, inputs

from app.core.config import INTERIM_ROOT
from app.engine import foundations_shallow_r as pilot
from app.engine.hashing import canonical_json
from app.engine.registry import CalculatorRegistry
from app.parameters.interim_loader import load_interim_root
from app.services.interim_data import (
    Profile,
    check_documents,
    effective_status,
    record_digest,
)
from app.services.interim_source import interim_sources

DOCUMENT = INTERIM_ROOT / "sp-22-13330-2016"
FILE = DOCUMENT / f"{pilot.NAME}.yaml"
TODAY = date(2026, 10, 22)


def registry() -> CalculatorRegistry:
    found = CalculatorRegistry()
    pilot.register(found, ROUNDING, RULE)
    return found


def raw_records() -> list[tuple[str, dict]]:
    data = yaml.safe_load(FILE.read_text(encoding="utf-8"))
    return [(name, record) for name, records in data.items() for record in records]


def test_the_loader_accepts_the_pilot_file_and_every_record_has_its_page() -> None:
    document = next(document for document in load_interim_root(INTERIM_ROOT, {pilot.NAME})
                    if document.name == "sp-22-13330-2016")
    file = next(file for file in document.files if file.calculation_type == pilot.NAME)

    assert file.calculation_type == pilot.NAME
    assert all(record.page is not None for _, record in file.content.records())
    counts = Counter(name for name, _ in raw_records())
    assert counts == {"formulas": 3, "table_values": 141, "thresholds": 1, "checks": 1}


def test_portion_p1_1_verified_the_pilot_formulas_and_k_and_no_checked_value_changed() -> None:
    document = next(document for document in load_interim_root(INTERIM_ROOT, {pilot.NAME})
                    if document.name == "sp-22-13330-2016")
    file = next(file for file in document.files if file.calculation_type == pilot.NAME)
    records = list(file.content.records())

    verified = {
        getattr(record, "parameter", None)
        for _, record in records
        if record.verification.portion == "P1-1"
    }
    assert verified == {"r", "k_z_below", "k_z_from", "k"}
    assert all(
        record.verification.portion == "P1-1" and effective_status(record) == "human-verified"
        for _, record in records
        if record.verification.portion == "P1-1"
    )


def test_the_file_is_written_in_the_form_the_loader_digests() -> None:
    document = next(document for document in load_interim_root(INTERIM_ROOT, {pilot.NAME})
                    if document.name == "sp-22-13330-2016")
    file = next(file for file in document.files if file.calculation_type == pilot.NAME)
    parsed = [record for _, record in file.content.records()]

    for record, (_, raw) in zip(parsed, raw_records(), strict=True):
        body = {key: value for key, value in raw.items() if key != "verification"}
        assert sha256(canonical_json(body).encode("utf-8")).hexdigest() == record_digest(record)


@pytest.mark.parametrize("profile", ["draft", "strict"])
def test_both_profiles_use_every_record_and_resolve_the_pilot(
    profile: Profile, caplog: pytest.LogCaptureFixture
) -> None:
    found = interim_sources(registry(), INTERIM_ROOT, profile, TODAY)

    resolved = found[pilot.NAME].resolve(pilot.NAME, inputs())

    assert isinstance(resolved.parameters, pilot.Parameters)
    assert resolved.source is not None and resolved.source.profile == profile
    assert resolved.method_range == ()
    assert not any(
        code in record.message
        for record in caplog.records
        if f"/{pilot.NAME}.yaml" in record.message
        for code in ("interim_record_unchecked", "interim_value_changed")
    )


def test_every_real_record_is_verified_with_its_current_digest() -> None:
    document = next(document for document in load_interim_root(INTERIM_ROOT, {pilot.NAME})
                    if document.name == "sp-22-13330-2016")
    file = next(file for file in document.files if file.calculation_type == pilot.NAME)
    records = [record for _, record in file.content.records()]

    assert len(records) == 146
    assert Counter(record.verification.portion for record in records) == {
        "P1-1": 4, "P2-1": 2, "P2-2": 138, "P3-1": 2,
    }
    for record in records:
        assert effective_status(record) == "human-verified"
        assert record.verification.value_digest == record_digest(record)


def test_the_checked_data_include_the_pilot_and_unregistered_future_type() -> None:
    found = check_documents(load_interim_root(INTERIM_ROOT, {pilot.NAME}), "draft")

    assert set(found) == {pilot.NAME, "foundations_pressure_from_loads", "foundations_shallow_loads"}

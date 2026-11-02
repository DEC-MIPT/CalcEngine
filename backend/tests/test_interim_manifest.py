from datetime import UTC, date, datetime

from interim_fixture import assert_before_sunset

from app.core.config import INTERIM_ROOT
from app.parameters.interim_loader import load_interim_root
from app.services.interim_data import warn_passed_sunsets

MANIFEST = INTERIM_ROOT / "sp-22-13330-2016" / "manifest.yaml"


def test_the_loader_accepts_the_real_manifest() -> None:
    (document,) = load_interim_root(INTERIM_ROOT, {"foundations_shallow_r"})

    assert document.name == "sp-22-13330-2016"
    assert document.manifest.document == "СП 22.13330.2016"
    assert document.manifest.verifiers == ("Akim",)
    assert document.manifest.sunset.date == date(2026, 12, 1)
    assert [file.calculation_type for file in document.files] == ["foundations_shallow_r"]


def test_the_real_sunset_has_not_passed() -> None:
    assert_before_sunset(MANIFEST, datetime.now(UTC).date())


def test_the_startup_reminder_is_silent_before_the_sunset() -> None:
    documents = load_interim_root(INTERIM_ROOT, set())

    assert warn_passed_sunsets(documents, date(2026, 12, 1)) == ()
    assert warn_passed_sunsets(documents, date(2026, 12, 2)) == ("sp-22-13330-2016",)

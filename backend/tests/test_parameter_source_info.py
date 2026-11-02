from typing import Any

import pytest
from catalog_fixture import PILOT
from pydantic import ValidationError
from sqlalchemy import Engine
from test_engine_foundations_shallow_r import inputs, parameters
from test_services_catalog_source import make_source, with_phi

from app.schemas.calculation import CATALOG_SOURCE, ParameterSourceInfo
from app.schemas.normatives import CatalogSnapshot
from app.services.parameter_source import ResolvedParameters

DIGEST = "a" * 64


def test_the_catalog_source_describes_itself_as_the_catalog(catalog_sqlite: Engine) -> None:
    resolved = make_source(catalog_sqlite).resolve(PILOT, inputs())

    assert resolved.source == ParameterSourceInfo(kind="catalog")
    assert resolved.source == CATALOG_SOURCE


def test_a_catalog_snapshot_carries_the_catalog_source_too(catalog_sqlite: Engine) -> None:
    resolved = make_source(catalog_sqlite).resolve(PILOT, with_phi(40.0))

    assert isinstance(resolved.parameters, CatalogSnapshot)
    assert resolved.source == CATALOG_SOURCE


def test_a_resolution_without_a_description_has_no_source() -> None:
    assert ResolvedParameters(parameters=parameters(), method_range=()).source is None


def test_an_interim_source_has_its_digest_and_profile() -> None:
    info = ParameterSourceInfo(kind="interim", data_sha256=DIGEST, profile="draft")

    assert (info.kind, info.data_sha256, info.profile) == ("interim", DIGEST, "draft")


@pytest.mark.parametrize(
    "fields",
    [
        {"kind": "interim"},
        {"kind": "interim", "data_sha256": DIGEST},
        {"kind": "interim", "profile": "strict"},
        {"kind": "catalog", "data_sha256": DIGEST},
        {"kind": "catalog", "profile": "strict"},
    ],
)
def test_a_description_with_the_fields_of_the_other_kind_is_rejected(fields: dict[str, Any]) -> None:
    with pytest.raises(ValidationError, match="an interim source has a data digest and a profile"):
        ParameterSourceInfo.model_validate(fields)


@pytest.mark.parametrize(
    "fields",
    [
        {"kind": "file"},
        {"kind": "interim", "data_sha256": "A" * 64, "profile": "strict"},
        {"kind": "interim", "data_sha256": DIGEST, "profile": "loose"},
    ],
)
def test_an_unknown_kind_digest_or_profile_is_rejected(fields: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        ParameterSourceInfo.model_validate(fields)

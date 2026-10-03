import pytest
from pydantic import ValidationError

from app.schemas.units import UNITS, Dimension, Unit


def test_each_unit_is_found_by_its_symbol() -> None:
    assert all(symbol == unit.symbol for symbol, unit in UNITS.items())


def test_dimensionless_unit_is_one() -> None:
    assert UNITS["1"].dimension is Dimension.DIMENSIONLESS
    assert UNITS["1"].factor == 1.0


def test_every_dimension_has_exactly_one_reference_unit() -> None:
    for dimension in Dimension:
        references = [
            unit for unit in UNITS.values() if unit.dimension is dimension and unit.factor == 1.0
        ]
        assert len(references) == 1, dimension


def test_vocabulary_is_read_only() -> None:
    with pytest.raises(TypeError):
        UNITS["ft"] = Unit(symbol="ft", dimension=Dimension.LENGTH, factor=0.3048)  # type: ignore[index]


@pytest.mark.parametrize("factor", [0.0, -1.0])
def test_unit_factor_is_positive(factor: float) -> None:
    with pytest.raises(ValidationError):
        Unit(symbol="x", dimension=Dimension.LENGTH, factor=factor)

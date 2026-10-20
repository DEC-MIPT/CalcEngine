import math
import os
from collections.abc import Callable, Iterator, Mapping

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from pilot_invariants import FORMULA_INVARIANTS, PILOT_RANGES
from sqlalchemy.orm import sessionmaker
from test_engine_foundations_shallow_r import BACKEND
from verification_strategies import inputs_in_range

from app.db.catalog import CatalogSessions, get_catalog_engine
from app.engine import foundations_shallow_r as pilot
from app.engine.boundary import convert, inputs_to_base_units
from app.engine.pipeline import calculate
from app.schemas.calculation import QuantityValue
from app.services.catalog import build_registry
from app.services.catalog_source import CatalogParameterSource
from app.services.parameter_source import ResolvedParameters
from app.verification.invariants import InvariantPlan

pytestmark = pytest.mark.postgres

URL = os.environ.get("DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL")
CASES = settings(max_examples=100, deadline=None, database=None)
"""100 случаев на инвариант, без лимита времени на случай и без базы примеров (решение 16)."""
REGISTRY = build_registry(BACKEND / "params")
CONTRACT = REGISTRY.contract(pilot.NAME)
"""Контракт пилота, как в работе: округление R из файла параметров инженера."""
PLAN = InvariantPlan(calculation_type=pilot.NAME, valid_range=PILOT_RANGES, invariants=FORMULA_INVARIANTS)
ARITHMETIC = 1e-9
"""Относительный допуск арифметики с плавающей точкой; это не значение нормы.

Формула вычисляется в ``float``: шаги R при равных шагах входа и R при большем входе
могут разойтись на единицы последнего разряда.
"""

Inputs = dict[str, QuantityValue]
Resolve = Callable[[Mapping[str, QuantityValue]], ResolvedParameters]


@pytest.fixture(scope="module")
def resolve() -> Iterator[Resolve]:
    """Параметры пилота из ингестированного каталога Егора под ролью-читателем.

    Формула 5.7, коэффициенты табл. 5.5 и порог ``k_z`` приходят из каталога тем же
    ``CatalogParameterSource``, что и в работе; в тесты дерево формулы не пишется (WP2,
    задача 7.1b). Каталог от входов зависит только строкой таблицы по ``phi_II``, поэтому
    параметры читаются один раз на значение ``phi_II``. Без
    ``DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL`` тест пропускается.
    """
    if URL is None:
        pytest.skip("DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL is not set")
    engine = get_catalog_engine(URL)
    source = CatalogParameterSource(CatalogSessions(sessionmaker(bind=engine)), REGISTRY)
    by_phi: dict[float, ResolvedParameters] = {}

    def resolved(inputs: Mapping[str, QuantityValue]) -> ResolvedParameters:
        phi = inputs["phi_II"].value
        if phi not in by_phi:
            by_phi[phi] = source.resolve(pilot.NAME, inputs)
        return by_phi[phi]

    yield resolved
    engine.dispose()


def drawn(data: st.DataObject) -> Inputs:
    """Входы пилота внутри допустимого диапазона, в базовых единицах."""
    return inputs_to_base_units(CONTRACT, data.draw(inputs_in_range(PLAN)))


def r(resolve: Resolve, inputs: Inputs) -> float:
    """Неокруглённое R пилота на параметрах каталога, в кПа."""
    found = resolve(inputs)
    assert isinstance(found.parameters, pilot.Parameters)
    result = calculate(CONTRACT, pilot.FoundationsShallowR(), inputs, found.parameters, method_range=found.method_range)
    return next(step.result.value for step in result.trace if step.step_id == "R")


def changed(inputs: Inputs, quantity: str, value: float) -> Inputs:
    return {**inputs, quantity: QuantityValue(value=value, unit=inputs[quantity].unit)}


def upper(quantity: str) -> float:
    return next(item.upper for item in PILOT_RANGES if item.quantity == quantity)


def lower(quantity: str) -> float:
    return next(item.lower for item in PILOT_RANGES if item.quantity == quantity)


def close(first: float, second: float, scale: float) -> bool:
    return math.isclose(first, second, rel_tol=0.0, abs_tol=ARITHMETIC * max(abs(scale), 1.0))


def not_smaller(smaller: float, larger: float) -> bool:
    return larger >= smaller or close(smaller, larger, smaller)


def steps_are_equal(resolve: Resolve, data: st.DataObject, quantity: str) -> bool:
    """Три значения входа с равным шагом дают два равных шага R."""
    inputs = drawn(data)
    start = inputs[quantity].value
    step = data.draw(st.floats(min_value=0.0, max_value=(upper(quantity) - start) / 2, allow_nan=False))
    first, second, third = (r(resolve, changed(inputs, quantity, start + k * step)) for k in (0, 1, 2))
    return close(second - first, third - second, max(abs(first), abs(third)))


def grows(resolve: Resolve, data: st.DataObject, quantity: str) -> bool:
    """Больший вход в пределах диапазона даёт R не меньше."""
    inputs = drawn(data)
    larger = data.draw(st.floats(min_value=inputs[quantity].value, max_value=upper(quantity), allow_nan=False))
    return not_smaller(r(resolve, inputs), r(resolve, changed(inputs, quantity, larger)))


@CASES
@given(data=st.data())
def test_equal_steps_of_c_ii_give_equal_steps_of_r(resolve: Resolve, data: st.DataObject) -> None:
    assert steps_are_equal(resolve, data, "c_II")


@CASES
@given(data=st.data())
def test_equal_steps_of_d_1_give_equal_steps_of_r(resolve: Resolve, data: st.DataObject) -> None:
    assert steps_are_equal(resolve, data, "d_1")


@CASES
@given(data=st.data())
def test_a_larger_c_ii_gives_an_r_not_smaller(resolve: Resolve, data: st.DataObject) -> None:
    assert grows(resolve, data, "c_II")


@CASES
@given(data=st.data())
def test_a_larger_gamma_ii_gives_an_r_not_smaller(resolve: Resolve, data: st.DataObject) -> None:
    assert grows(resolve, data, "gamma_II")


@CASES
@given(data=st.data())
def test_a_larger_d_b_gives_an_r_not_smaller(resolve: Resolve, data: st.DataObject) -> None:
    assert grows(resolve, data, "d_b")


@CASES
@given(data=st.data())
def test_a_larger_b_gives_an_r_not_smaller(resolve: Resolve, data: st.DataObject) -> None:
    assert grows(resolve, data, "b")


@CASES
@given(data=st.data())
def test_r_does_not_drop_across_the_k_z_threshold(resolve: Resolve, data: st.DataObject) -> None:
    """Дополняет ``R-grows-with-b`` вплотную к порогу ``k_z`` из каталога, куда случайные пары b почти не попадают."""
    inputs = drawn(data)
    parameters = resolve(inputs).parameters
    assert isinstance(parameters, pilot.Parameters)
    threshold = convert(parameters.k_z_threshold.value, "m").value
    below = math.nextafter(threshold, -math.inf)

    assert lower("b") <= below < threshold <= upper("b")
    assert not_smaller(r(resolve, changed(inputs, "b", below)), r(resolve, changed(inputs, "b", threshold)))

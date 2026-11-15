import pytest
from test_engine_foundations_shallow_r import ROUNDING, RULE
from test_loads_interim_source import inputs, resolve

from app.engine.base import Calculator
from app.engine.foundations_shallow_loads import FoundationsLoadsModule, contract
from app.engine.pipeline import calculate
from app.engine.registry import CalculatorRegistry
from app.schemas.calculation import CalculationResult, QuantityValue


@pytest.fixture
def registry() -> CalculatorRegistry:
    result = CalculatorRegistry()
    declared = contract(ROUNDING, RULE)
    result.register_module(declared, FoundationsLoadsModule(declared))
    return result


def test_registered_module_get_returns_two_argument_calculator(registry: CalculatorRegistry) -> None:
    name = "foundations_shallow_loads"
    calculator = registry.get(name)
    assert isinstance(calculator, Calculator)
    result = calculator.calculate(inputs(), resolve().parameters)
    assert isinstance(result, CalculationResult)
    explicit = calculate(registry.contract(name), calculator, inputs(), resolve().parameters, module=registry.module(name))
    assert result == explicit


@pytest.mark.parametrize("case", ["completed", "contact_refused", "bound_refused"])
def test_bound_module_dispatch_preserves_ranges_and_diagnostics_without_module_argument(
    registry: CalculatorRegistry, case: str,
) -> None:
    name = "foundations_shallow_loads"
    resolved = resolve()
    supplied = inputs()
    if case == "contact_refused":
        supplied |= {"Mx": QuantityValue(value=1000, unit="kN*m")}
    elif case == "bound_refused":
        supplied |= {"d_b": QuantityValue(value=3, unit="m")}
    implicit = calculate(registry.contract(name), registry.get(name), supplied, resolved.parameters,
                         method_range=resolved.method_range)
    explicit = calculate(registry.contract(name), registry.get(name), supplied, resolved.parameters,
                         method_range=resolved.method_range, module=registry.module(name))
    assert implicit == explicit
    assert implicit.verdict == ("pass" if case == "completed" else "refused")
    if case == "contact_refused":
        assert implicit.verdict_reason.kind == "derived" and implicit.trace
    elif case == "bound_refused":
        assert implicit.verdict_reason.kind == "bound" and not implicit.trace


@pytest.mark.parametrize("case", ["valid", "bound_refused", "invalid_domain"])
def test_legacy_boundary_rejects_module_binding_before_any_input_processing(
    registry: CalculatorRegistry, monkeypatch: pytest.MonkeyPatch, case: str,
) -> None:
    from app.core.exceptions import CalculationError
    from app.engine import boundary

    resolved = resolve()
    supplied = inputs()
    if case == "bound_refused":
        supplied |= {"d_b": QuantityValue(value=3, unit="m")}
    elif case == "invalid_domain":
        supplied |= {"b": QuantityValue(value=-1, unit="m")}

    def unexpected(*args: object, **kwargs: object) -> None:
        pytest.fail("legacy input conversion, identity or applicability must not run for a typed module")

    for operation in ("inputs_to_base_units", "input_hash", "check_applicability"):
        monkeypatch.setattr(boundary, operation, unexpected)
    name = "foundations_shallow_loads"
    with pytest.raises(CalculationError, match="pipeline.calculate"):
        boundary.run(registry.contract(name), registry.get(name), supplied, resolved.parameters,
                     method_range=resolved.method_range)


def test_registration_requires_public_quantity_entry_point(
    registry: CalculatorRegistry, monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.core.exceptions import ContractMetadataError

    monkeypatch.delattr(FoundationsLoadsModule, "execute_public")
    with pytest.raises(ContractMetadataError, match="public quantity adapter"):
        CalculatorRegistry().register_module(registry.contract("foundations_shallow_loads"),
                                            registry.module("foundations_shallow_loads"))

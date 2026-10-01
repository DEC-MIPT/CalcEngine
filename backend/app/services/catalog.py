from pathlib import Path

from app.core.exceptions import ParameterValidationError
from app.engine import foundations_shallow_r
from app.engine.registry import CalculatorRegistry
from app.parameters.loader import load_parameters


def _register_foundations_shallow_r(registry: CalculatorRegistry, params_root: Path) -> None:
    values = load_parameters(foundations_shallow_r.NAME, params_root)
    entry = values.rounding_rules.get("R")
    if entry is None:
        raise ParameterValidationError(
            f"{foundations_shallow_r.NAME}.yaml: no rounding rule for the output 'R'"
        )
    foundations_shallow_r.register(registry, entry.rule, entry.source)


REGISTRATIONS = (_register_foundations_shallow_r,)


def build_registry(params_root: Path) -> CalculatorRegistry:
    """Every known calculation type, registered with its engineer-set values.

    A missing or invalid parameter file stops the application at start-up
    (``calculation-api`` design.md decision 2).
    """
    registry = CalculatorRegistry()
    for register in REGISTRATIONS:
        register(registry, params_root)
    return registry

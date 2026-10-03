from pathlib import Path

from app.core.exceptions import ParameterValidationError
from app.engine import foundations_shallow_r
from app.engine.registry import CalculatorRegistry
from app.parameters.loader import load_parameters
from app.schemas.api import CalculationTypeView, InputView, OutputView
from app.schemas.units import UNITS


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


def calculation_types(registry: CalculatorRegistry) -> tuple[CalculationTypeView, ...]:
    """Описывает зарегистрированные типы расчёта для формы ввода.

    Правила округления, проверки и источники в описание не входят: они относятся к
    результату, а не к форме (``calculation-api`` design.md, решение 10).

    Args:
        registry: реестр типов расчёта.

    Returns:
        По одному описанию на тип в порядке регистрации; входы и выходы в порядке
        контракта, размерность входа берётся из словаря единиц.
    """
    return tuple(
        CalculationTypeView(
            name=contract.name,
            inputs=tuple(
                InputView(
                    name=quantity.name,
                    base_unit=quantity.base_unit,
                    dimension=UNITS[quantity.base_unit].dimension,
                )
                for quantity in contract.inputs
            ),
            outputs=tuple(
                OutputView(name=output.name, base_unit=output.base_unit)
                for output in contract.outputs
            ),
        )
        for contract in registry.contracts()
    )

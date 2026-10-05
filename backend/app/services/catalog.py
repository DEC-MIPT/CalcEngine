from pathlib import Path

from app.core.exceptions import ParameterValidationError
from app.engine import foundations_shallow_r
from app.engine.registry import CalculatorRegistry
from app.parameters.loader import load_parameters
from app.schemas.api import CalculationTypeView, InputView, OutputView
from app.schemas.calculation import (
    OutputDeclaration,
    QuantityDeclaration,
    ValidatedBound,
)
from app.schemas.units import UNITS, units_of


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
    """Регистрирует каждый известный тип расчёта со значениями, заданными инженером.

    Отсутствующий или неверный файл параметров останавливает приложение при старте
    (``calculation-api`` design.md, решение 2).

    Args:
        params_root: каталог файлов параметров.

    Returns:
        Реестр типов расчёта.

    Raises:
        NotFoundError: если файла параметров типа нет.
        ParameterValidationError: если файл не проходит проверку или в нём нет
            правила округления выхода.
    """
    registry = CalculatorRegistry()
    for register in REGISTRATIONS:
        register(registry, params_root)
    return registry


def load_validated_ranges(
    registry: CalculatorRegistry, params_root: Path
) -> dict[str, tuple[ValidatedBound, ...]]:
    """Читает проверенный диапазон каждого зарегистрированного типа из его ``.yaml``.

    Вызывается при старте вместе с ``build_registry``, поэтому ошибка в файле
    останавливает приложение, а не первый запрос (``calculation-api`` design.md,
    решения 2 и 3).

    Args:
        registry: реестр типов расчёта.
        params_root: каталог файлов параметров.

    Returns:
        Для каждого типа — границы проверенного диапазона в порядке файла.

    Raises:
        NotFoundError: если у зарегистрированного типа нет файла параметров.
        ParameterValidationError: если файл не проходит проверку схемы.
    """
    return {
        contract.name: load_parameters(contract.name, params_root).validated_range
        for contract in registry.contracts()
    }


def _input_view(quantity: QuantityDeclaration) -> InputView:
    label, symbol = quantity.described()
    dimension = UNITS[quantity.base_unit].dimension
    return InputView(
        name=quantity.name,
        base_unit=quantity.base_unit,
        dimension=dimension,
        units=units_of(dimension),
        label=label,
        symbol=symbol,
        hint=quantity.hint,
        whole_values_only=quantity.whole_values_only,
    )


def _output_view(output: OutputDeclaration) -> OutputView:
    label, symbol = output.described()
    return OutputView(name=output.name, base_unit=output.base_unit, label=label, symbol=symbol)


def calculation_types(registry: CalculatorRegistry) -> tuple[CalculationTypeView, ...]:
    """Описывает зарегистрированные типы расчёта для формы ввода.

    Правила округления, проверки и источники в описание не входят: они относятся к
    результату, а не к форме (``calculation-api`` design.md, решение 10).

    Args:
        registry: реестр типов расчёта.

    Returns:
        По одному описанию на тип в порядке регистрации; входы и выходы в порядке
        контракта; размерность входа и допустимые для него единицы берутся из
        словаря единиц.
    """
    return tuple(
        CalculationTypeView(
            name=contract.name,
            inputs=tuple(_input_view(quantity) for quantity in contract.inputs),
            outputs=tuple(_output_view(output) for output in contract.outputs),
        )
        for contract in registry.contracts()
    )

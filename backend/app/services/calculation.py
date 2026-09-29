from collections.abc import Callable, Mapping, Sequence
from uuid import UUID, uuid4

from app.engine.pipeline import calculate
from app.engine.registry import CalculatorRegistry
from app.schemas.calculation import (
    CalculationResult,
    MethodBound,
    QuantityValue,
    ResultEnvelope,
    ValidatedBound,
)


class CalculationService:
    """Runs a registered calculation type and gives each result its ``result_id``.

    Storing the envelope in ``dec_app`` belongs to a later change
    (``calculation-core-contract`` design.md decision 12).
    """

    def __init__(
        self, registry: CalculatorRegistry, new_id: Callable[[], UUID] = uuid4
    ) -> None:
        self._registry = registry
        self._new_id = new_id

    def envelope(self, result: CalculationResult) -> ResultEnvelope:
        """The result with a new ``result_id``; every other field is the result's."""
        return ResultEnvelope.model_validate(dict(result) | {"result_id": self._new_id()})

    def run(
        self,
        calculation_type: str,
        inputs: Mapping[str, QuantityValue],
        parameters: object,
        *,
        method_range: Sequence[MethodBound] = (),
        validated_range: Sequence[ValidatedBound] = (),
    ) -> ResultEnvelope:
        result = calculate(
            self._registry.contract(calculation_type),
            self._registry.get(calculation_type),
            inputs,
            parameters,
            method_range=method_range,
            validated_range=validated_range,
        )
        return self.envelope(result)

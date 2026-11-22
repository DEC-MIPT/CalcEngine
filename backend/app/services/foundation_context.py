from collections.abc import Mapping
from typing import Literal, cast

from app.engine.boundary import convert
from app.schemas.calculation import QuantityValue, ResultEnvelope
from app.schemas.foundation_design import FoundationContext, PressureCorner

FOUNDATION_TYPES = frozenset({"foundations_shallow_loads", "foundations_shallow_weights"})


def foundation_context(
    calculation_type: str, inputs: Mapping[str, QuantityValue], envelope: ResultEnvelope,
    methodology_version: str,
) -> FoundationContext:
    geometry = {name: convert(inputs[name], "m") for name in ("b", "l")}
    trace_values = {step.step_id: step.result for step in envelope.trace}
    for name in ("A", "Wx", "Wy"):
        if name in trace_values:
            geometry[name] = trace_values[name]
    corners: list[PressureCorner] = []
    if all(f"p_corner_{name}" in trace_values for name in ("pp", "pm", "mp", "mm")):
        signs: tuple[tuple[Literal["pp", "pm", "mp", "mm"], int, int], ...] = (("pp", 1, 1), ("pm", 1, -1), ("mp", -1, 1), ("mm", -1, -1))
        for name, sx, sy in signs:
            corners.append(PressureCorner(
                name=name, x=QuantityValue(value=sx * geometry["b"].value / 2, unit="m"),
                y=QuantityValue(value=sy * geometry["l"].value / 2, unit="m"),
                pressure=trace_values[f"p_corner_{name}"], step_id=f"p_corner_{name}",
            ))
    state: Literal["unavailable", "diagnostic", "full_contact"] = "unavailable" if not corners else "diagnostic" if envelope.verdict == "refused" else "full_contact"
    return FoundationContext(
        result_id=envelope.result_id, calculation_type=cast(Literal["foundations_shallow_loads", "foundations_shallow_weights"], calculation_type),
        methodology_version=methodology_version, input_hash=envelope.input_hash,
        weight_mode="explicit" if calculation_type == "foundations_shallow_weights" else "averaged",
        inputs=dict(inputs), geometry=geometry, trace_values=trace_values,
        pressure_state=state, corners=tuple(corners),
    )

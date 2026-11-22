import json
import re
from datetime import date
from pathlib import Path
from uuid import UUID

from app.core.config import INTERIM_ROOT, PARAMS_ROOT
from app.engine.foundations_shallow_loads import NAME
from app.schemas.calculation import QuantityValue
from app.services.calculation import CalculationService
from app.services.catalog import build_registry, calculation_types
from app.services.interim_source import interim_sources


def exported(name: str, value: object, schema: str) -> str:
    serialized = re.sub(
        r'^([ ]*"(?:input_hash|data_sha256)": "[0-9a-f]{64}",?)$',
        r'\1 // pragma: allowlist secret',
        json.dumps(value, ensure_ascii=False, indent=2),
        flags=re.MULTILINE,
    )
    return f"export const {name} = {serialized} satisfies {schema}\n"


registry = build_registry(PARAMS_ROOT)
sources = interim_sources(registry, INTERIM_ROOT, "strict", date(2026, 11, 16))
source = sources[NAME]
references = json.loads(Path("tests/fixtures/foundations_loads_references.json").read_text())
central, one_axis, biaxial = (example["inputs"] for example in references)
scenarios = [
    ("Central", "55555555-5555-4555-8555-555555555555", central),
    ("OneAxis", "66666666-6666-4666-8666-666666666666", one_axis),
    ("Biaxial", "77777777-7777-4777-8777-777777777777", biaxial),
    ("Fail", "88888888-8888-4888-8888-888888888888", central | {"N": {"value": 900, "unit": "kN"}}),
    ("BoundRefusal", "99999999-9999-4999-8999-999999999999", central | {"d_b": {"value": 3, "unit": "m"}}),
    ("ContactRefusal", "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", central | {
        "Mx": {"value": 180, "unit": "kN*m"},
        "My": {"value": 180, "unit": "kN*m"},
    }),
    ("ZeroContact", "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb", central | {
        "Mx": {"value": 240, "unit": "kN*m"},
    }),
]

parts = [
    "import type { components } from '../api/schema'\n",
    "type CalculationTypeView = components['schemas']['CalculationTypeView']\n",
    "type CalculationRequest = components['schemas']['CalculationRequest']\n",
    "type ResultEnvelope = components['schemas']['ResultEnvelope']\n",
    "type ParameterSourceInfo = components['schemas']['ParameterSourceInfo']\n",
    "export const LOADS_TYPE = 'foundations_shallow_loads'\n",
    exported("loadsCalculationType", next(item for item in calculation_types(registry) if item.name == NAME).model_dump(mode="json"), "CalculationTypeView"),
]
for name, result_id, values in scenarios:
    inputs = {key: QuantityValue.model_validate(value) for key, value in values.items()}
    resolved = source.resolve(NAME, inputs)
    service = CalculationService(registry, new_id=lambda result_id=result_id: UUID(result_id))
    envelope = service.run(NAME, inputs, resolved.parameters, method_range=resolved.method_range, source=resolved.source)
    parts.extend([
        f"export const LOADS_{''.join('_' + letter if letter.isupper() else letter for letter in name).strip('_').upper()}_ID = '{result_id}'\n",
        exported(f"loads{name}Inputs", values, "CalculationRequest['inputs']"),
        exported(f"loads{name}Envelope", envelope.model_dump(mode="json"), "ResultEnvelope"),
        f"export const loads{name}Json = {json.dumps(envelope.model_dump_json(), ensure_ascii=False)}\n",
    ])

strict = source.resolve(NAME, {key: QuantityValue.model_validate(value) for key, value in central.items()}).source
draft = interim_sources(registry, INTERIM_ROOT, "draft", date(2026, 11, 16))[NAME].resolve(
    NAME, {key: QuantityValue.model_validate(value) for key, value in central.items()},
).source
assert strict is not None and draft is not None
parts.extend([
    exported("loadsStrictSource", strict.model_dump(mode="json"), "ParameterSourceInfo"),
    exported("loadsDraftSource", draft.model_dump(mode="json"), "ParameterSourceInfo"),
    "export const loadsScenarios = [\n"
    + "".join(f"  {{ name: '{name}', inputs: loads{name}Inputs, envelope: loads{name}Envelope, json: loads{name}Json }},\n" for name, _, _ in scenarios)
    + "]\n",
])
print("\n".join(parts), end="")

import json
import re
from datetime import date
from itertools import count
from pathlib import Path
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import INTERIM_ROOT, PARAMS_ROOT
from app.models import Base
from app.repositories.calculation_result import CalculationResultRepository
from app.repositories.foundation_design import FoundationDesignRepository
from app.schemas.calculation import CalculationRequest
from app.schemas.foundation_design import FoundationSelectionRequest
from app.services.calculation import CalculationService
from app.services.catalog import build_registry, calculation_types, load_validated_ranges
from app.services.foundation_design import FoundationDesignService
from app.services.interim_source import interim_sources

LOADS = 'foundations_shallow_loads'
WEIGHTS = 'foundations_shallow_weights'
registry = build_registry(PARAMS_ROOT)
sources = interim_sources(registry, INTERIM_ROOT, 'strict', date(2026, 11, 22))
ids = count(1)


def new_id():
    return UUID(f'dec00000-0000-4000-8000-{next(ids):012d}')


def export(name, value, schema):
    text = json.dumps(value.model_dump(mode='json'), ensure_ascii=False, indent=2)
    text = re.sub(r'^([ ]*"(?:input_hash|data_sha256)": "[0-9a-f]{64}",?)$',
                  r'\1 // pragma: allowlist secret', text, flags=re.MULTILINE)
    print(f"export const {name} = {text} satisfies components['schemas']['{schema}']")


def references(name):
    return json.loads(Path(f'tests/fixtures/foundations_{name}_references.json').read_text())


def candidate(b, l):
    return {key: {'value': value, 'unit': 'm'} for key, value in (('b', b), ('l', l))}


print("import type { components } from '../api/schema'")
export('weightsCalculationType', next(item for item in calculation_types(registry) if item.name == WEIGHTS), 'CalculationTypeView')
engine = create_engine('sqlite://')
Base.metadata.create_all(engine)
with Session(engine) as session:
    storage = FoundationDesignRepository(session)
    results = CalculationResultRepository(session)
    validated = load_validated_ranges(registry, PARAMS_ROOT)

    def calculation_service(factory):
        return CalculationService(registry, new_id=factory, sources=sources, validated_ranges=validated,
                                  results=results, design_results=storage)

    calculations = calculation_service(new_id)

    def selection_service(budget):
        return FoundationDesignService(registry, calculations, storage, new_id=new_id, clock=lambda: 0.0, budget=budget)

    design = selection_service(10)
    weights = [example['inputs'] for example in references('weights')]
    weights.append(weights[-1] | {'Mx_add_base': {'value': 2000, 'unit': 'kN*m'}})
    for label, values in zip(('Central', 'OneAxis', 'Biaxial', 'ContactRefusal'), weights, strict=True):
        request = CalculationRequest(calculation_type=WEIGHTS, inputs=values)
        envelope = calculations.submit(request)
        export(f'weights{label}Request', request, 'CalculationRequest')
        export(f'weights{label}Envelope', envelope, 'ResultEnvelope')
        export(f'weights{label}Context', design.context(envelope.result_id), 'FoundationContextResponse')
    central = references('loads')[0]['inputs']
    common = {key: value for key, value in central.items() if key not in ('b', 'l')}
    for label, candidates, budget in (
        ('Selected', [candidate(2, 2), candidate(2, 3)], 10),
        ('Exhausted', [candidate(2, 2)], 10),
        ('Incomplete', [candidate(2, 3)], 0),
    ):
        service = selection_service(budget)
        result = service.select(FoundationSelectionRequest(common_inputs=common, candidates=candidates))
        export(f'selection{label}', result, 'FoundationSelectionResult')
        if result.selected_result_id is not None:
            export('selectionWinnerContext', service.context(result.selected_result_id), 'FoundationContextResponse')
    for label, values, result_id in (
        ('Central', central, '55555555-5555-4555-8555-555555555555'),
        ('ContactRefusal', central | {'Mx': {'value': 180, 'unit': 'kN*m'}, 'My': {'value': 180, 'unit': 'kN*m'}}, 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'),
    ):
        envelope = calculation_service(lambda: UUID(result_id)).submit(CalculationRequest(calculation_type=LOADS, inputs=values))
        export(f'loads{label}Context', design.context(envelope.result_id), 'FoundationContextResponse')

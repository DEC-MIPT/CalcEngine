import json
from datetime import date
from io import BytesIO
from pathlib import Path
from unittest.mock import patch
from uuid import UUID, uuid4

import pytest
from docx import Document
from docx.oxml.ns import qn
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import create_engine, func, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import INTERIM_ROOT, PARAMS_ROOT
from app.core.exceptions import CalculationError, ParameterSourceUnavailableError
from app.main import create_app
from app.models import Base
from app.models.calculation_result import CalculationResultRow
from app.models.foundation_design import FoundationContextRow, FoundationSelectionRow
from app.schemas.foundation_design import (
    FoundationContextResponse,
    FoundationSelectionRequest,
    FoundationSelectionResult,
)
from app.services.catalog import build_registry, load_validated_ranges
from app.services.foundation_design import foundation_design_service
from app.services.interim_source import interim_sources

C = json.loads((Path(__file__).parent / 'fixtures/foundations_loads_references.json').read_text())[0]
REPORT = {'title': {'designation': 'DEC', 'document_name': 'Selection', 'organization': 'DEC'}, 'signature_block': False}


def request(candidates=None, **changes):
    common = {key: value for key, value in C['inputs'].items() if key not in ('b', 'l')}
    common.update(changes)
    return {'common_inputs': common, 'candidates': candidates or [
        {'b': {'value': 2, 'unit': 'm'}, 'l': {'value': 2, 'unit': 'm'}},
        {'b': {'value': 2, 'unit': 'm'}, 'l': {'value': 3, 'unit': 'm'}},
        {'b': {'value': 1.5, 'unit': 'm'}, 'l': {'value': 4, 'unit': 'm'}},
        {'b': {'value': 2.5, 'unit': 'm'}, 'l': {'value': 2.5, 'unit': 'm'}},
    ]}


@pytest.fixture
def resources():
    registry = build_registry(PARAMS_ROOT)
    sources = interim_sources(registry, INTERIM_ROOT, 'strict', date(2026, 11, 15))
    engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    factory = sessionmaker(engine)
    yield registry, sources, factory
    engine.dispose()


@pytest.fixture
def client(resources):
    registry, sources, factory = resources
    with TestClient(create_app(registry=registry, sources=sources, session_factory=factory,
        validated_ranges=load_validated_ranges(registry, PARAMS_ROOT))) as found:
        yield found


def service(resources, **options):
    registry, sources, factory = resources
    session = factory()
    found = foundation_design_service(session, registry, sources=sources, validated_ranges={})
    for key, value in options.items():
        setattr(found, '_' + key, value)
    return found, session


def test_minimum_area_source_resolution_tie_and_context(client, resources):
    response = client.post('/foundation-selections', json=request())
    assert response.status_code == 201, response.text
    result = response.json()
    assert result['status'] == 'selected' and result['selected_candidate_index'] == 1
    assert [item['envelope']['verdict'] for item in result['outcomes']] == ['fail', 'pass', 'pass', 'pass']
    assert [item['envelope']['outputs'][0]['value'] for item in result['outcomes']] == pytest.approx([152.02, 152.02, 146.41, 157.63])
    assert client.get(response.headers['Location']).json() == result
    assert client.get('/calculations/' + result['selected_result_id']).json() == result['outcomes'][1]['envelope']
    context = client.get('/foundation-calculations/' + result['selected_result_id'] + '/context').json()
    assert context['status'] == 'available'
    assert context['context']['weight_mode'] == 'averaged'
    assert [item['pressure']['value'] for item in context['context']['corners']] == [120] * 4
    with resources[2]() as session:
        assert session.scalar(select(func.count()).select_from(CalculationResultRow)) == 1
        assert session.scalar(select(func.count()).select_from(FoundationContextRow)) == 1
        assert session.scalar(select(func.count()).select_from(FoundationSelectionRow)) == 1
    body = request()
    body['candidates'][1:3] = list(reversed(body['candidates'][1:3]))
    reversed_result = client.post('/foundation-selections', json=body).json()
    assert reversed_result['selected_candidate_index'] == 1
    assert reversed_result['outcomes'][1]['candidate']['b']['value'] == 1.5


def test_no_solution_and_reports(client):
    response = client.post('/foundation-selections', json=request(N={'value': 60000, 'unit': 'kN'}))
    assert response.status_code == 201
    assert response.json()['status'] == 'no_acceptable_candidate'
    doc = client.post(response.headers['Location'] + '/report', json=REPORT)
    assert doc.status_code == 200
    text = '\n'.join(p.text for p in Document(BytesIO(doc.content)).paragraphs)
    assert 'no_acceptable_candidate' in text and 'foundation-min-area-v1' in text


@pytest.mark.parametrize('change', [
    {'candidates': []}, {'candidates': [request()['candidates'][0]] * 257},
    {'calculation_type': 'foundations_shallow_weights'}, {'policy_version': 'unknown'},
    {'common_inputs': {}}, {'unknown': 'field'},
])
def test_invalid_request_before_storage(client, resources, change):
    response = client.post('/foundation-selections', json=request() | change)
    assert response.status_code == 422
    with resources[2]() as session:
        assert session.scalar(select(func.count()).select_from(FoundationSelectionRow)) == 0


@pytest.mark.parametrize('name,value', [('b', {'value': 1, 'unit': 'm'}), ('phi_II', {'value': 2.5, 'unit': 'deg'})])
def test_invalid_common_fields(client, name, value):
    body = request()
    body['common_inputs'][name] = value
    assert client.post('/foundation-selections', json=body).status_code == 422


def test_validates_all_candidates_before_resolution(client, resources):
    body = request()
    body['candidates'][-1]['b'] = {'value': 10, 'unit': 'm'}
    with patch.object(type(resources[1]['foundations_shallow_loads']), 'resolve', side_effect=AssertionError('must not run')):
        response = client.post('/foundation-selections', json=body)
    assert response.status_code == 422
    assert response.json()['fields'][0]['location'][:3] == ['body', 'candidates', 3]


def test_equivalent_units_and_duplicates(client):
    body = request([
        {'b': {'value': 200, 'unit': 'cm'}, 'l': {'value': 3000, 'unit': 'mm'}},
        {'b': {'value': 2, 'unit': 'm'}, 'l': {'value': 3, 'unit': 'm'}},
    ])
    result = client.post('/foundation-selections', json=body).json()
    assert result['status'] == 'selected' and result['selected_candidate_index'] == 0
    assert len(result['outcomes']) == 2
    assert result['outcomes'][0]['envelope']['input_hash'] == result['outcomes'][1]['envelope']['input_hash']


def test_context_unavailable_and_missing_ids(client, resources):
    ordinary = client.post('/calculations', json={'calculation_type': C['calculation_type'], 'inputs': C['inputs']}).json()
    assert client.get(f"/foundation-calculations/{ordinary['result_id']}/context").json()['status'] == 'available'
    with resources[2]() as session:
        session.delete(session.get(FoundationContextRow, UUID(ordinary['result_id'])))
        session.commit()
    response = client.get(f"/foundation-calculations/{ordinary['result_id']}/context")
    assert response.status_code == 404
    assert response.json()["code"] == "foundation_context_unavailable"
    missing = str(uuid4())
    assert client.get('/foundation-selections/' + missing).status_code == 404
    assert client.get('/foundation-calculations/' + missing + '/context').status_code == 404


@pytest.mark.parametrize('reason', ['source', 'calculation'])
def test_incomplete_error_retains_evidence(resources, reason):
    found, session = service(resources)
    exception = ParameterSourceUnavailableError('unavailable') if reason == 'source' else CalculationError('failed')
    original = found._calculations.evaluate
    count = 0
    def evaluate(given):
        nonlocal count
        count += 1
        if count == 2:
            raise exception
        return original(given)
    with patch.object(found._calculations, 'evaluate', side_effect=evaluate):
        result = found.select(FoundationSelectionRequest.model_validate(request()))
    assert result.status == 'incomplete'
    assert [item.status for item in result.outcomes] == ['evaluated', 'error', 'skipped', 'skipped']
    assert result.outcomes[0].envelope is not None and result.selected_candidate_index is None
    assert session.scalar(select(func.count()).select_from(CalculationResultRow)) == 0
    session.close()


@pytest.mark.parametrize('stop', ['time', 'cancel'])
def test_late_stop_preserves_completed_envelope(resources, stop):
    ticks = iter([0, 0, 11])
    found, session = service(resources, clock=(lambda: next(ticks)) if stop == 'time' else (lambda: 0))
    events = iter([False, True])
    result = found.select(FoundationSelectionRequest.model_validate(request([request()['candidates'][1]])),
        cancelled=(lambda: next(events)) if stop == 'cancel' else (lambda: False))
    assert result.status == 'incomplete'
    assert result.outcomes[0].status == 'evaluated' and result.outcomes[0].envelope is not None
    assert result.stop_reason == ('time_budget' if stop == 'time' else 'cancelled')
    assert result.selected_result_id is None
    session.close()


def test_atomic_rollback(client, resources):
    with patch('app.repositories.foundation_design.FoundationDesignRepository.add_selection', side_effect=OperationalError('storage failed', {}, Exception())):
        response = client.post('/foundation-selections', json=request())
        assert response.status_code == 503
        assert response.json()["code"] == "database_unavailable"
    with resources[2]() as session:
        assert session.scalar(select(func.count()).select_from(CalculationResultRow)) == 0
        assert session.scalar(select(func.count()).select_from(FoundationContextRow)) == 0


def test_forged_selection_rejected(client):
    result = client.post('/foundation-selections', json=request()).json()
    with pytest.raises(ValidationError):
        FoundationSelectionResult.model_validate(result | {'selected_candidate_index': 3, 'selected_result_id': result['outcomes'][3]['envelope']['result_id']})
    with pytest.raises(ValidationError):
        FoundationContextResponse(status='available')


def test_context_for_contact_refusal(client):
    given = dict(C['inputs']) | {'Mx': {'value': 1000, 'unit': 'kN*m'}}
    result = client.post('/calculations', json={'calculation_type': C['calculation_type'], 'inputs': given}).json()
    context = client.get(f"/foundation-calculations/{result['result_id']}/context").json()['context']
    assert context['pressure_state'] == 'diagnostic'
    assert min(corner['pressure']['value'] for corner in context['corners']) < 0
    assert result['outputs'] == []


def test_selection_report_preserves_title_selected_trace_and_figure(client):
    selection = client.post('/foundation-selections', json=request()).json()
    response = client.post(f"/foundation-selections/{selection['selection_id']}/report", json=REPORT)
    assert response.status_code == 200
    document = Document(BytesIO(response.content))
    text = '\n'.join(p.text for p in document.paragraphs)
    assert '2 Расчёт' in text and 'foundation-min-area-v1' in text
    assert selection['selected_result_id'] in text and 'Схема нагрузок' in text
    assert len(document.inline_shapes) == 1
    assert 'TextBox' not in document._element.xml
    footer = '\n'.join(table._element.xml for section in document.sections for footer in (section.footer, section.first_page_footer) for table in footer.tables)
    assert 'Selection' in footer
    assert 'pgBorders' in document.sections[0]._sectPr.xml
    assert 'текст' not in document.inline_shapes[0]._inline.docPr.get('descr', '')
    assert 'альтернатива' in document.inline_shapes[0]._inline.docPr.get('descr', '')


def test_new_explicit_result_report_has_complete_weight_and_moment_context(client):
    example = json.loads((Path(__file__).parent / 'fixtures/foundations_weights_references.json').read_text())[2]
    envelope = client.post('/calculations', json={'calculation_type': 'foundations_shallow_weights', 'inputs': example['inputs']}).json()
    response = client.post(f"/calculations/{envelope['result_id']}/report", json=REPORT)
    assert response.status_code == 200
    document = Document(BytesIO(response.content))
    math_nodes = document.element.body.xpath('.//m:oMath')
    expressions = {''.join(node.text or '' for node in math.iter(qn('m:t'))) for math in math_nodes}
    for symbol in ('Gfund', 'Gsoil', 'Gother', 'V', 'Mx,base', 'My,base', 'Mx,add,base', 'p++'):
        assert symbol in expressions
    assert len(document.inline_shapes) == 1



def test_explicit_report_refusal_has_diagnostic_values_but_no_output_section(client):
    example = json.loads((Path(__file__).parent / 'fixtures/foundations_weights_references.json').read_text())[0]
    inputs = example['inputs'] | {'Mx': {'value': 1000, 'unit': 'kN*m'}}
    result = client.post('/calculations', json={'calculation_type': 'foundations_shallow_weights', 'inputs': inputs}).json()
    assert result['verdict_reason']['kind'] == 'derived'
    response = client.post(f"/calculations/{result['result_id']}/report", json=REPORT)
    assert response.status_code == 200
    document = Document(BytesIO(response.content))
    text = '\n'.join(p.text for p in document.paragraphs)
    assert 'Выходные величины' not in text and 'Все проверки выполнены.' not in text
    assert 'Диагностическая эпюра:' in text
    assert text.count('Нормативные ссылки расчёта: СП 22.13330.2016') == 1
    reason = next(p for p in document.paragraphs if p.text.startswith('Получено:'))
    assert len(reason._p.xpath('./m:oMath')) == 3
    assert '0,00' in ''.join(t.text or '' for t in reason._p.iter(qn('m:t')))


def test_historical_report_stays_usable_without_context(client, resources):
    result = client.post('/calculations', json={'calculation_type': C['calculation_type'], 'inputs': C['inputs']}).json()
    with resources[2]() as session:
        session.delete(session.get(FoundationContextRow, UUID(result['result_id'])))
        session.commit()
    response = client.post(f"/calculations/{result['result_id']}/report", json=REPORT)
    assert response.status_code == 200
    assert len(Document(BytesIO(response.content)).inline_shapes) == 0


@pytest.mark.parametrize('stop', ['time', 'cancel'])
def test_early_stop_stores_all_unattempted_indices(resources, stop):
    found, session = service(resources, budget=0 if stop == 'time' else 10)
    with patch.object(found._calculations, 'evaluate', side_effect=AssertionError('must not evaluate')):
        result = found.select(FoundationSelectionRequest.model_validate(request()), cancelled=lambda: stop == 'cancel')
    assert result.status == 'incomplete' and result.selected_result_id is None
    assert [item.index for item in result.outcomes] == [0, 1, 2, 3]
    assert all(item.status == 'skipped' and item.envelope is None for item in result.outcomes)
    assert result.stop_reason == ('time_budget' if stop == 'time' else 'cancelled')
    session.close()


def test_maximum_candidate_list_accepted_without_deduplication(resources):
    found, session = service(resources, budget=60)
    body = request([request()['candidates'][1]] * 256)
    result = found.select(FoundationSelectionRequest.model_validate(body))
    assert result.status == 'selected' and result.selected_candidate_index == 0
    assert len(result.outcomes) == 256
    assert len({item.envelope.result_id for item in result.outcomes}) == 256
    session.close()


def test_body_limit_applies_before_selection(client, resources):
    with patch.object(type(resources[1]['foundations_shallow_loads']), 'resolve', side_effect=AssertionError('must not run')):
        response = client.post('/foundation-selections', content=' ' * (1024 * 1024 + 1), headers={'Content-Type': 'application/json'})
    assert response.status_code == 413 and response.json()['code'] == 'payload_too_large'


def test_malformed_outcome_count_is_validation_error(client):
    result = client.post('/foundation-selections', json=request()).json()
    result['outcomes'].extend([result['outcomes'][1]] * 3)
    with pytest.raises(ValidationError):
        FoundationSelectionResult.model_validate(result)


@pytest.mark.parametrize("preceding_body_message", [False, True])
def test_route_disconnect_is_forwarded_to_cooperative_service(resources, preceding_body_message):
    import asyncio
    import threading

    from fastapi import Request, Response

    from app.api.foundation_design import create_selection

    found, session = service(resources)
    entered = threading.Event()
    original = found.select
    callbacks = []

    def selecting(given, cancelled):
        entered.set()
        assert entered.wait(1)
        while not cancelled():
            entered.wait(0.001)
        callbacks.append(cancelled())
        return original(given, cancelled)

    messages = [{"type": "http.request", "body": b"", "more_body": False}] if preceding_body_message else []

    async def receive():
        if messages:
            return messages.pop(0)
        while not entered.is_set():
            await asyncio.sleep(0)
        return {'type': 'http.disconnect'}

    async def run():
        with patch.object(found, 'select', side_effect=selecting):
            return await create_selection(FoundationSelectionRequest.model_validate(request()), Request({'type': 'http'}, receive), found, Response())

    result = asyncio.run(run())
    assert callbacks == [True]
    assert result.status == 'incomplete' and result.stop_reason == 'cancelled'
    session.close()


@pytest.mark.parametrize('change', [
    {'weight_mode': 'explicit'}, {'geometry': {}},
    {'geometry': {'b': {'value': -1, 'unit': 'm'}, 'l': {'value': 2, 'unit': 'm'}}},
    {'geometry': {'b': {'value': 2, 'unit': 'cm'}, 'l': {'value': 2, 'unit': 'm'}}},
    {'pressure_state': 'unavailable'}, {'corners': []},
])
def test_context_rejects_inconsistent_physical_contract(client, change):
    from app.schemas.foundation_design import FoundationContext
    result = client.post('/foundation-selections', json=request()).json()
    context = client.get(f"/foundation-calculations/{result['selected_result_id']}/context").json()['context']
    with pytest.raises(ValidationError):
        FoundationContext.model_validate(context | change)


@pytest.mark.parametrize('field,value', [
    ('x', {'value': 1, 'unit': 'cm'}),
    ('pressure', {'value': 120, 'unit': 'MPa'}),
    ('step_id', 'not_the_stored_corner'),
])
def test_context_rejects_untraceable_corner(client, field, value):
    from app.schemas.foundation_design import FoundationContext
    result = client.post('/foundation-selections', json=request()).json()
    context = client.get(f"/foundation-calculations/{result['selected_result_id']}/context").json()['context']
    context['corners'][0][field] = value
    with pytest.raises(ValidationError):
        FoundationContext.model_validate(context)


@pytest.mark.parametrize('change', [
    {'selected_candidate_index': None}, {'selected_result_id': str(uuid4())},
    {'status': 'no_acceptable_candidate', 'selected_candidate_index': None, 'selected_result_id': None},
    {'status': 'incomplete', 'selected_candidate_index': None, 'selected_result_id': None},
])
def test_selection_rejects_forged_terminal_state(client, change):
    result = client.post('/foundation-selections', json=request()).json()
    with pytest.raises(ValidationError):
        FoundationSelectionResult.model_validate(result | change)


def test_candidate_evidence_and_order_are_validated(client):
    from app.schemas.foundation_design import CandidateOutcome
    result = client.post('/foundation-selections', json=request()).json()
    candidate = result['outcomes'][1]
    for change in [{'envelope': None}, {'reason': 'cancelled'}, {'status': 'error'}, {'status': 'error', 'envelope': None}]:
        with pytest.raises(ValidationError):
            CandidateOutcome.model_validate(candidate | change)
    result['outcomes'][0], result['outcomes'][1] = result['outcomes'][1], result['outcomes'][0]
    with pytest.raises(ValidationError):
        FoundationSelectionResult.model_validate(result)


def test_unexpected_candidate_failure_is_incomplete_without_error_text(resources):
    found, session = service(resources)
    with patch.object(found._calculations, 'evaluate', side_effect=RuntimeError('sensitive driver data')):
        result = found.select(FoundationSelectionRequest.model_validate(request()))
    assert result.status == 'incomplete' and result.stop_reason == 'calculation_error'
    assert 'sensitive' not in result.model_dump_json()
    assert [item.status for item in result.outcomes] == ['error', 'skipped', 'skipped', 'skipped']
    session.close()


def test_selection_identity_stable_and_source_dependent(resources):
    found, session = service(resources)
    body = FoundationSelectionRequest.model_validate(request())
    first = found.select(body)
    second = found.select(body)
    assert first.input_hash == second.input_hash
    assert first.selection_id != second.selection_id
    assert first.selected_result_id != second.selected_result_id
    session.close()


def test_exact_decimal_equivalent_units_select_first_without_500(client):
    body = request([
        {'b': {'value': 1400, 'unit': 'mm'}, 'l': {'value': 3000, 'unit': 'mm'}},
        {'b': {'value': 1.4, 'unit': 'm'}, 'l': {'value': 3, 'unit': 'm'}},
    ], N={'value': 300, 'unit': 'kN'})
    response = client.post('/foundation-selections', json=body)
    assert response.status_code == 201, response.text
    assert response.json()['selected_candidate_index'] == 0


def test_method_refusal_preserves_unavailable_pressure_context_and_report(client):
    given = C['inputs'] | {'d_b': {'value': 3, 'unit': 'm'}}
    result = client.post('/calculations', json={'calculation_type': C['calculation_type'], 'inputs': given}).json()
    assert result['verdict'] == 'refused' and result['trace'] == []
    context = client.get(f"/foundation-calculations/{result['result_id']}/context").json()['context']
    assert context['pressure_state'] == 'unavailable' and context['corners'] == []
    report = client.post(f"/calculations/{result['result_id']}/report", json=REPORT)
    assert report.status_code == 200
    assert 'Эпюра недоступна' in '\n'.join(p.text for p in Document(BytesIO(report.content)).paragraphs)



def test_explicit_method_refusal_does_not_describe_an_absent_pressure_plot(client):
    example = json.loads((Path(__file__).parent / 'fixtures/foundations_weights_references.json').read_text())[0]
    inputs = example['inputs'] | {'d_b': {'value': 3, 'unit': 'm'}}
    result = client.post('/calculations', json={'calculation_type': 'foundations_shallow_weights', 'inputs': inputs}).json()
    assert result['verdict_reason']['kind'] == 'bound' and result['trace'] == []
    response = client.post(f"/calculations/{result['result_id']}/report", json=REPORT)
    assert response.status_code == 200
    document = Document(BytesIO(response.content))
    text = '\n'.join(p.text for p in document.paragraphs)
    assert 'Эпюра недоступна' in text and 'Величины по шагам расчёта' not in text
    assert 'Угловые давления отсутствуют' in document.inline_shapes[0]._inline.docPr.get('descr', '')


def test_incomplete_search_report_contains_no_fabricated_result(resources):
    found, session = service(resources, budget=0)
    result = found.select(FoundationSelectionRequest.model_validate(request()))
    from app.schemas.report import ReportRequest
    data = found.report(result.selection_id, ReportRequest.model_validate(REPORT))
    text = '\n'.join(p.text for p in Document(BytesIO(data)).paragraphs)
    assert 'incomplete' in text and 'time_budget' in text
    assert 'Подтверждённый размер не выбран' in text
    assert not Document(BytesIO(data)).inline_shapes
    session.close()


def test_schema_rejects_mixed_complete_and_skipped_winner(client):
    result = client.post('/foundation-selections', json=request()).json()
    result['outcomes'][0] |= {'status': 'skipped', 'envelope': None, 'reason': 'not_evaluated'}
    with pytest.raises(ValidationError):
        FoundationSelectionResult.model_validate(result)
    result = client.post('/foundation-selections', json=request()).json()
    with pytest.raises(ValidationError):
        FoundationSelectionResult.model_validate(result | {'status': 'incomplete', 'stop_reason': 'cancelled'})


def test_context_pressure_unit_is_checked_after_trace_provenance(client):
    from app.schemas.foundation_design import FoundationContext
    result = client.post('/foundation-selections', json=request()).json()
    context = client.get(f"/foundation-calculations/{result['selected_result_id']}/context").json()['context']
    context['corners'][0]['pressure']['unit'] = 'MPa'
    context['trace_values']['p_corner_pp']['unit'] = 'MPa'
    with pytest.raises(ValidationError):
        FoundationContext.model_validate(context)


def test_candidate_dimension_unit_error_has_named_index(resources):
    from app.core.exceptions import InputValidationError, UnitError
    found, session = service(resources)
    with patch('app.services.foundation_design.inputs_to_base_units', side_effect=UnitError('invalid unit')), pytest.raises(InputValidationError) as problem:
        found.select(FoundationSelectionRequest.model_validate(request()))
    assert problem.value.fields[0].location == ('body', 'candidates', 0)
    session.close()


def test_search_identity_changes_with_resolved_source_identity(resources):
    from dataclasses import replace
    found, session = service(resources)
    body = FoundationSelectionRequest.model_validate(request())
    first = found.select(body)
    source = resources[1]['foundations_shallow_loads']
    resolve = source.resolve
    def changed(name, inputs):
        resolved = resolve(name, inputs)
        return replace(resolved, source=resolved.source.model_copy(update={'data_sha256': 'a' * 64}))
    with patch.object(type(source), 'resolve', side_effect=changed):
        second = found.select(body)
    assert first.input_hash != second.input_hash
    session.close()


def test_report_accepts_stored_candidate_without_source_descriptor(resources):
    from dataclasses import replace

    from app.schemas.report import ReportRequest
    found, session = service(resources)
    source = resources[1]['foundations_shallow_loads']
    resolve = source.resolve
    with patch.object(type(source), 'resolve', side_effect=lambda name, inputs: replace(resolve(name, inputs), source=None)):
        selected = found.select(FoundationSelectionRequest.model_validate(request()))
    assert selected.status == 'selected'
    report = found.report(selected.selection_id, ReportRequest.model_validate(REPORT))
    assert len(Document(BytesIO(report)).inline_shapes) == 1
    session.close()


def test_diagnostic_report_labels_figure_before_numeric_tables(client):
    given = C['inputs'] | {'Mx': {'value': 1000, 'unit': 'kN*m'}}
    result = client.post('/calculations', json={'calculation_type': C['calculation_type'], 'inputs': given}).json()
    assert result['verdict'] == 'refused' and result['outputs'] == []
    response = client.post(f"/calculations/{result['result_id']}/report", json=REPORT)
    assert response.status_code == 200
    document = Document(BytesIO(response.content))
    paragraphs = [p.text for p in document.paragraphs]
    label = next(i for i, text in enumerate(paragraphs) if text.startswith('Диагностическая эпюра:'))
    caption = next(i for i, text in enumerate(paragraphs) if text.startswith('Слева: схема'))
    assert label < caption
    assert 'Перераспределение' in paragraphs[label]
    assert len(document.inline_shapes) == 1


def test_explicit_weights_only_zero_structural_force_has_figure(client):
    example = json.loads((Path(__file__).parent / 'fixtures/foundations_weights_references.json').read_text())[0]
    inputs = example['inputs'] | {'N': {'value': 0, 'unit': 'kN'}}
    response = client.post('/calculations', json={'calculation_type': 'foundations_shallow_weights', 'inputs': inputs})
    assert response.status_code == 201, response.text
    result = response.json()
    assert result['verdict'] == 'pass'
    report = client.post(f"/calculations/{result['result_id']}/report", json=REPORT)
    assert report.status_code == 200
    assert len(Document(BytesIO(report.content)).inline_shapes) == 1


def test_schematic_line_clips_to_canvas_and_blank_glyph_keeps_background():
    from app.reporting.foundation_figures import _Drawing
    drawing = _Drawing(width=20, height=20)
    drawing.line((-10, 5), (30, 5))
    assert list(drawing.rows[5]) == [30] * 20
    assert list(drawing.rows[4]) == [255] * 20
    drawing.text(0, 0, ' ')
    assert list(drawing.rows[4]) == [255] * 20

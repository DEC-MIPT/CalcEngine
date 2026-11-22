import { describe, expect, it } from 'vitest'
import { api } from '@/api/client'
import { selectionSelected, weightsCentralEnvelope, weightsCentralRequest } from './designFixtures'

const post = (body: unknown) => fetch('http://127.0.0.1:8000/foundation-selections', {
  method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
})

describe('captured design-tools API', () => {
  it('rejects other calculation types and zero or more than 256 rows without evaluating a subset', async () => {
    const { request } = selectionSelected
    for (const bad of [null, { ...request, calculation_type: weightsCentralRequest.calculation_type },
      { ...request, candidates: [] }, { ...request, candidates: Array(257).fill(request.candidates[0]) },
      { ...request, common_inputs: null }, { ...request, candidates: null }]) {
      expect((await post(bad)).status).toBe(422)
    }
  })

  it('does not invent results for unrecorded candidates or change their order', async () => {
    const { request } = selectionSelected
    for (const candidates of [[...request.candidates].reverse(), [null, request.candidates[1]], Array(256).fill(request.candidates[0])]) {
      const response = await post({ ...request, candidates })
      expect(await response.json()).toMatchObject({ code: 'mock_fixture_unavailable' })
    }
  })

  it('serves the stored envelope and context with equal identity', async () => {
    const posted = await api.POST('/calculations', { body: weightsCentralRequest })
    expect(posted.data).toEqual(weightsCentralEnvelope)
    const context = await api.GET('/foundation-calculations/{result_id}/context', { params: { path: { result_id: weightsCentralEnvelope.result_id } } })
    expect(context.data?.context?.input_hash).toBe(weightsCentralEnvelope.input_hash)
    const absent = await api.GET('/foundation-calculations/{result_id}/context', { params: { path: { result_id: 'absent' } } })
    expect(absent.error).toMatchObject({ code: 'foundation_context_unavailable' })
  })

  it('serves reports only for stored selections', async () => {
    for (const [id, status] of [[selectionSelected.selection_id, 200], ['absent', 404]] as const) {
      const response = await fetch(`http://127.0.0.1:8000/foundation-selections/${id}/report`, { method: 'POST' })
      expect(response.status).toBe(status)
    }
  })
})

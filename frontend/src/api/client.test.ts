import { describe, expect, it } from 'vitest'
import { baseUrlFrom, createApi, unwrap } from './client'

function json(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json' },
  })
}

function apiWith(respond: () => Response | Promise<Response>) {
  return createApi({ baseUrl: 'http://test.local', fetch: async () => respond() })
}

describe('baseUrlFrom', () => {
  it('takes the configured address in any build', () => {
    expect(baseUrlFrom({ VITE_API_BASE_URL: 'https://api.example', DEV: false })).toBe('https://api.example')
  })

  it('falls back to the local backend only in development', () => {
    expect(baseUrlFrom({ DEV: true })).toBe('http://127.0.0.1:8000')
    expect(baseUrlFrom({ DEV: false })).toBe('')
  })
})

describe('unwrap', () => {
  it('returns the data of a successful response', async () => {
    const api = apiWith(() => json(200, []))

    expect(await unwrap(api.GET('/calculation-types'))).toEqual({ ok: true, data: [] })
  })

  it('passes a 422 body on with the place of each error', async () => {
    const fields = [{ location: ['body', 'inputs', 'phi_II'], message: 'Missing input.' }]
    const api = apiWith(() => json(422, { code: 'invalid_input', message: 'Invalid input', fields }))

    const result = await unwrap(
      api.POST('/calculations', { body: { calculation_type: 't', inputs: {} } }),
    )

    expect(result).toEqual({
      ok: false,
      error: { kind: 'api', status: 422, code: 'invalid_input', message: 'Invalid input', fields },
    })
  })

  it.each([
    [404, 'result_not_found'],
    [503, 'parameter_source_unavailable'],
  ])('keeps the status and code of a %i response without fields', async (status, code) => {
    const api = apiWith(() => json(status, { code, message: 'Not now' }))

    const result = await unwrap(
      api.GET('/calculations/{result_id}', { params: { path: { result_id: 'x' } } }),
    )

    expect(result).toEqual({
      ok: false,
      error: { kind: 'api', status, code, message: 'Not now', fields: [] },
    })
  })

  it('treats null fields as none', async () => {
    const api = apiWith(() => json(503, { code: 'c', message: 'm', fields: null }))

    const result = await unwrap(api.GET('/calculation-types'))

    expect(result).toMatchObject({ ok: false, error: { fields: [] } })
  })

  it('reports a failed request as a network error', async () => {
    const api = apiWith(() => {
      throw new TypeError('Failed to fetch')
    })

    expect(await unwrap(api.GET('/calculation-types'))).toEqual({
      ok: false,
      error: { kind: 'network' },
    })
  })

  it.each([
    ['text', new Response('Bad gateway', { status: 502 })],
    ['json without a code', json(500, { detail: 'boom' })],
    ['json null', json(500, null)],
  ])('keeps a %s error body out of the message', async (_name, response) => {
    const api = apiWith(() => response)

    const result = await unwrap(api.GET('/calculation-types'))

    expect(result).toMatchObject({
      ok: false,
      error: { kind: 'api', code: 'unexpected_response', message: 'Unexpected response' },
    })
  })
})

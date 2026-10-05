import { describe, expect, it } from 'vitest'
import { createApi, unwrap } from '../api/client'
import { calculationTypes, FAIL_ID, failEnvelope, PASS_ID, passEnvelope } from './fixtures'
import { serviceUnavailable } from './handlers'
import { server } from './server'

const api = createApi({ baseUrl: 'http://test.local' })

const reportRequest = {
  title: { designation: 'd', document_name: 'n', documentation_kind: '', organization: 'o' },
  signature_block: false,
}

const givenInputs = {
  b: { value: 2, unit: 'm' },
  d_1: { value: 1, unit: 'm' },
  d_b: { value: 0.5, unit: 'm' },
  gamma_II: { value: 10, unit: 'kN/m3' },
  gamma_II_prime: { value: 20, unit: 'kN/m3' },
  c_II: { value: 3, unit: 'kPa' },
  phi_II: { value: 20, unit: 'deg' },
  p: { value: 100, unit: 'kPa' },
} as const

function create(inputs: object, type = 'foundations_shallow_r') {
  return unwrap(
    api.POST('/calculations', {
      body: { calculation_type: type, inputs: inputs as typeof givenInputs },
    }),
  )
}

describe('mock handlers', () => {
  it('list the pilot type with the metadata of its inputs', async () => {
    const result = await unwrap(api.GET('/calculation-types'))

    expect(result).toEqual({ ok: true, data: calculationTypes })
    expect(calculationTypes[0].inputs.find((input) => input.name === 'phi_II')).toMatchObject({
      whole_values_only: true,
      symbol: '\\varphi_{II}',
    })
  })

  it('answer a pressure within the resistance with the passing envelope', async () => {
    expect(await create(givenInputs)).toEqual({ ok: true, data: passEnvelope })
  })

  it('answer a pressure above the resistance with the failing envelope', async () => {
    const result = await create({ ...givenInputs, p: { value: 200, unit: 'kPa' } })

    expect(result).toEqual({ ok: true, data: failEnvelope })
  })

  it('answer a missing input with a 422 that names its place', async () => {
    const { p, ...withoutP } = givenInputs
    expect(p).toBeDefined()

    expect(await create(withoutP)).toMatchObject({
      ok: false,
      error: {
        status: 422,
        code: 'invalid_input',
        fields: [{ location: ['body', 'inputs', 'p'], message: 'Missing input.' }],
      },
    })
  })

  it('answer an unknown type with a 422 that names the type', async () => {
    expect(await create(givenInputs, 'beam')).toMatchObject({
      ok: false,
      error: { status: 422, fields: [{ location: ['body', 'calculation_type'] }] },
    })
  })

  it('can be replaced by the 503 of an unavailable parameter source', async () => {
    server.use(serviceUnavailable)

    expect(await create(givenInputs)).toMatchObject({
      ok: false,
      error: { status: 503, code: 'parameter_source_unavailable' },
    })
  })

  it.each([
    [PASS_ID, passEnvelope],
    [FAIL_ID, failEnvelope],
  ])('return the stored result %s', async (id, envelope) => {
    const result = await unwrap(
      api.GET('/calculations/{result_id}', { params: { path: { result_id: id } } }),
    )

    expect(result).toEqual({ ok: true, data: envelope })
  })

  it('answer an unknown result with a 404', async () => {
    const result = await unwrap(
      api.GET('/calculations/{result_id}', { params: { path: { result_id: 'nobody' } } }),
    )

    expect(result).toMatchObject({ ok: false, error: { status: 404, code: 'not_found' } })
  })

  it('return a report file with its name for a known result', async () => {
    const response = await api.POST('/calculations/{result_id}/report', {
      params: { path: { result_id: PASS_ID } },
      body: reportRequest,
      parseAs: 'blob',
    })

    expect(response.response.headers.get('content-disposition')).toBe(
      'attachment; filename="report.docx"',
    )
    expect((response.data as Blob).size).toBe(4)
  })

  it('answer a report request for an unknown result with a 404', async () => {
    const result = await unwrap(
      api.POST('/calculations/{result_id}/report', {
        params: { path: { result_id: 'nobody' } },
        body: reportRequest,
      }),
    )

    expect(result).toMatchObject({ ok: false, error: { status: 404 } })
  })
})

import { describe, expect, expectTypeOf, it } from 'vitest'
import type { components } from '@/api/schema'
import {
  calculationTypes,
  LOADS_TYPE,
  loadsBoundRefusalEnvelope,
  loadsCalculationType,
  loadsCentralEnvelope,
  loadsCentralInputs,
  loadsContactRefusalEnvelope,
  loadsOneAxisInputs,
  loadsScenarios,
} from './fixtures'

type Envelope = components['schemas']['ResultEnvelope']
type Inputs = components['schemas']['CalculationRequest']['inputs']
const base = 'http://test.local'
const reportRequest = {
  title: { designation: 'd', document_name: 'n', documentation_kind: '', organization: 'o' },
  signature_block: false,
}

function post(inputs: Inputs) {
  return fetch(`${base}/calculations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ calculation_type: LOADS_TYPE, inputs }),
  })
}

function convertInputs(inputs: Inputs, names: string[], scale: number, unit: components['schemas']['QuantityValue']['unit']): Inputs {
  return {
    ...inputs,
    ...Object.fromEntries(names.map((name) => [name, { value: inputs[name].value * scale, unit }])),
  }
}

describe('captured loads API contract', () => {
  it('lists both types and the ordered fifteen-input, ten-output loads metadata', async () => {
    const response = await fetch(`${base}/calculation-types`)
    const listing = await response.json()

    expect(listing).toEqual(calculationTypes)
    expect(listing.map((type: { name: string }) => type.name)).toEqual(['foundations_shallow_r', LOADS_TYPE])
    expect(loadsCalculationType.inputs.map((input) => input.name)).toEqual([
      'b', 'd_1', 'd_b', 'gamma_II', 'gamma_II_prime', 'c_II', 'phi_II', 'l', 'h', 'd', 'N', 'Mx', 'My', 'Qx', 'Qy',
    ])
    expect(loadsCalculationType.outputs.map((output) => output.name)).toEqual([
      'R', 'p', 'p_x_min', 'p_x_max', 'p_y_min', 'p_y_max', 'p_corner_pp', 'p_corner_pm', 'p_corner_mp', 'p_corner_mm',
    ])
    expect(loadsCalculationType.inputs.find((input) => input.name === 'Mx')?.units).toEqual(['N*m', 'kN*m', 'MN*m'])
    expect(loadsCalculationType.inputs.some((input) => String(input.base_unit) === 'm3')).toBe(false)
  })

  it('keeps engineer attribution and disjoint historical bound and derived refusals', () => {
    const step = loadsCentralEnvelope.trace.find((item) => item.kind === 'engineer_formula')
    expect(step).toBeDefined()
    if (!step || step.kind !== 'engineer_formula') throw new Error('captured engineer step missing')
    expect(step.source.engineer).not.toBe('')
    expect(step.source.rationale).not.toBe('')
    expect(step).not.toHaveProperty('norm_refs')
    expectTypeOf(step.kind).toEqualTypeOf<'engineer_formula'>()
    expectTypeOf(loadsBoundRefusalEnvelope.verdict_reason.kind).toEqualTypeOf<'bound'>()
    expectTypeOf(loadsContactRefusalEnvelope.verdict_reason.kind).toEqualTypeOf<'derived'>()
    expect(loadsBoundRefusalEnvelope.trace).toEqual([])
    expect(loadsBoundRefusalEnvelope.verdict_reason).toHaveProperty('bound.quantity', 'd_b')
    expect(loadsBoundRefusalEnvelope.verdict_reason).not.toHaveProperty('limiting_corner')
    expect(loadsContactRefusalEnvelope.verdict_reason).toMatchObject({
      kind: 'derived', check_id: 'full_contact', quantity: 'p_corner_min', limiting_corner: 'mm',
    })
    expect(loadsContactRefusalEnvelope.verdict_reason).not.toHaveProperty('bound')
    expect(loadsContactRefusalEnvelope.outputs).toEqual([])
    expect(loadsContactRefusalEnvelope.trace.length).toBeGreaterThan(0)
    expect((loadsContactRefusalEnvelope as Envelope).trace.some((item) => item.kind === 'check')).toBe(false)
  })

  it.each(loadsScenarios)('round trips the immutable recorded $name response and report route', async ({ inputs, envelope, json }) => {
    const response = await post(inputs)
    expect(response.status).toBe(201)
    expect(response.headers.get('location')).toBe(`/calculations/${envelope.result_id}`)
    const wireBody = await response.text()
    expect(typeof json).toBe('string')
    expect(wireBody === json, 'POST matches the captured backend JSON exactly').toBe(true)
    const body = JSON.parse(wireBody) as Envelope
    expect(body).toEqual(envelope)
    const stored = await fetch(`${base}/calculations/${envelope.result_id}`)
    expect((await stored.text()) === json, 'GET preserves the captured backend JSON exactly').toBe(true)
    const report = await fetch(`${base}/calculations/${envelope.result_id}/report`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(reportRequest),
    })
    expect(report.status).toBe(200)
    expect(report.headers.get('content-type')).toBe('application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    expect(report.headers.get('content-disposition')).toContain('report.docx')
    expect((await report.arrayBuffer()).byteLength).toBeGreaterThan(0)
    body.outputs.length = 0
    body.trace.length = 0
    expect(await (await fetch(`${base}/calculations/${envelope.result_id}`)).json()).toEqual(envelope)
  })

  it.each([
    ['N*m', 1000, ['Mx', 'My']],
    ['MN*m', 0.001, ['Mx', 'My']],
    ['N', 1000, ['N', 'Qx', 'Qy']],
    ['MN', 0.001, ['N', 'Qx', 'Qy']],
  ] as const)('matches captured inputs after independent %s conversion', async (unit, scale, names) => {
    const inputs = convertInputs(loadsOneAxisInputs, [...names], scale, unit)
    const response = await post(inputs)
    expect(response.status).toBe(201)
    expect(await response.json()).toEqual(loadsScenarios.find((scenario) => scenario.name === 'OneAxis')?.envelope)
  })

  it.each([
    ['N', 600.0001],
    ['Mx', 0.0000001],
    ['d_b', 0.0000001],
  ] as const)('rejects nearby uncaptured %s without deriving pressures or rounding into a fixture', async (name, value) => {
    const response = await post({ ...loadsCentralInputs, [name]: { ...loadsCentralInputs[name], value } })
    expect(response.status).toBe(422)
    const body = await response.json()
    expect(body).toMatchObject({ code: 'mock_fixture_unavailable' })
    expect(body).not.toHaveProperty('outputs')
    expect(body).not.toHaveProperty('trace')
    expect(body).not.toHaveProperty('verdict_reason')
  })

  it('does not collapse a nonzero moment to a recorded one by six-digit display rounding', async () => {
    const response = await post({ ...loadsOneAxisInputs, Mx: { value: 40.00001, unit: 'kN*m' } })
    expect(response.status).toBe(422)
    expect(await response.json()).toMatchObject({ code: 'mock_fixture_unavailable' })
  })

  it('does not match a signed negative zero to a recorded positive zero', async () => {
    const request = JSON.stringify({ calculation_type: LOADS_TYPE, inputs: loadsCentralInputs })
      .replace('"Mx":{"value":0', '"Mx":{"value":-0')
    const response = await fetch(`${base}/calculations`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: request,
    })
    expect(response.status).toBe(422)
    expect(await response.json()).toMatchObject({ code: 'mock_fixture_unavailable' })
  })
})


describe('loads request validation in recorded mocks', () => {
  it.each([
    ['missing', () => Object.fromEntries(Object.entries(loadsCentralInputs).filter(([name]) => name !== 'N')), 'N'],
    ['extra', () => ({ ...loadsCentralInputs, p: { value: 120, unit: 'kPa' } }), 'p'],
    ['wrong dimension', () => ({ ...loadsCentralInputs, Mx: { value: 0, unit: 'kN' } }), 'Mx'],
  ] as const)('rejects %s fields with a readable input location', async (_, inputs, field) => {
    const response = await fetch(`${base}/calculations`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ calculation_type: LOADS_TYPE, inputs: inputs() }),
    })
    expect(response.status).toBe(422)
    expect(await response.json()).toMatchObject({
      code: 'invalid_input', fields: expect.arrayContaining([expect.objectContaining({ location: ['body', 'inputs', field] })]),
    })
  })

  it.each([
    null,
    [],
    'request',
    { calculation_type: LOADS_TYPE, inputs: null },
    { calculation_type: LOADS_TYPE, inputs: [] },
    { calculation_type: '', inputs: loadsCentralInputs },
    { calculation_type: 42, inputs: loadsCentralInputs },
    { calculation_type: LOADS_TYPE, inputs: loadsCentralInputs, parameters: {} },
    { calculation_type: LOADS_TYPE, inputs: { ...loadsCentralInputs, N: [] } },
    { calculation_type: LOADS_TYPE, inputs: { ...loadsCentralInputs, N: 600 } },
    { calculation_type: LOADS_TYPE, inputs: { ...loadsCentralInputs, N: { value: 600, unit: 'kN', extra: true } } },
    { calculation_type: LOADS_TYPE, inputs: { ...loadsCentralInputs, N: { value: 600, unit: 42 } } },
    { calculation_type: LOADS_TYPE, inputs: { ...loadsCentralInputs, N: { value: '600', unit: 'kN' } } },
    { calculation_type: LOADS_TYPE, inputs: { ...loadsCentralInputs, N: { value: null, unit: 'kN' } } },
    { calculation_type: LOADS_TYPE, inputs: { ...loadsCentralInputs, N: { value: 600, unit: 'furlong' } } },
  ])('returns a validation error for malformed request %#', async (body) => {
    const response = await fetch(`${base}/calculations`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
    })
    expect(response.status).toBe(422)
    expect(await response.json()).toMatchObject({ code: 'validation_error' })
  })
})


it('rejects malformed JSON without an unhandled mock exception', async () => {
  const response = await fetch(`${base}/calculations`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{',
  })
  expect(response.status).toBe(422)
  expect(await response.json()).toMatchObject({ code: 'validation_error' })
})


it.each([
  ['N', 600000.1, 'N'],
  ['Mx', 40000.01, 'N*m'],
] as const)('rejects nearby %s after unrounded conversion of %s %s', async (name, value, unit) => {
  const inputs = name === 'Mx' ? loadsOneAxisInputs : loadsCentralInputs
  const response = await post({ ...inputs, [name]: { value, unit } })
  expect(response.status).toBe(422)
  expect(await response.json()).toMatchObject({ code: 'mock_fixture_unavailable' })
})

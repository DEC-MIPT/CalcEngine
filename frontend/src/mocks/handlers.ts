import { http, HttpResponse } from 'msw'
import type { components } from '../api/schema'
import { UNIT_FACTORS } from '../lib/unitFactors'
import {
  calculationTypes,
  FAIL_ID,
  failEnvelope,
  PASS_ID,
  passEnvelope,
  REFUSED_ID,
  refusedEnvelope,
  WARNING_ID,
  warningEnvelope,
  LOADS_TYPE,
  loadsCalculationType,
  loadsScenarios,
} from './fixtures'

type CalculationRequest = components['schemas']['CalculationRequest']
type ErrorBody = components['schemas']['ErrorBody']
type Quantity = components['schemas']['QuantityValue']
type Envelope = components['schemas']['ResultEnvelope']

const DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
const RESISTANCE_KPA = 172.5
const METRES: Record<string, number> = { m: 1, cm: 0.01, mm: 0.001 }
const METHOD_MAX_B_M = refusedEnvelope.verdict_reason.bound.value
const VALIDATED_MAX_B_M = warningEnvelope.warnings[0].bound.value

const envelopes: Record<string, Envelope> = {
  [PASS_ID]: passEnvelope,
  [FAIL_ID]: failEnvelope,
  [REFUSED_ID]: refusedEnvelope,
  [WARNING_ID]: warningEnvelope,
  ...Object.fromEntries(loadsScenarios.map(({ envelope }) => [envelope.result_id, envelope])),
}

const serializedLoads: Record<string, string> = Object.fromEntries(
  loadsScenarios.map(({ envelope, json }) => [envelope.result_id, json]),
)

function envelopeResponse(envelope: Envelope, status = 200, location?: string) {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (location) headers.Location = location
  const serialized = serializedLoads[envelope.result_id]
  return serialized === undefined
    ? HttpResponse.json(envelope, { status, headers })
    : new HttpResponse(serialized, { status, headers })
}

function lookup(id: unknown) {
  const key = String(id)
  return Object.hasOwn(envelopes, key) ? envelopes[key as keyof typeof envelopes] : undefined
}

function pilotScenario(inputs: CalculationRequest['inputs']) {
  const widthM = inputs.b.value * METRES[inputs.b.unit]
  if (widthM > METHOD_MAX_B_M) return refusedEnvelope
  if (widthM > VALIDATED_MAX_B_M) return warningEnvelope
  return inBaseUnit(inputs.p, 'kPa') > RESISTANCE_KPA ? failEnvelope : passEnvelope
}

function inBaseUnit(quantity: Quantity, base: string) {
  if (quantity.unit === base) return quantity.value
  return quantity.value * UNIT_FACTORS[quantity.unit] / UNIT_FACTORS[base]
}

function loadsScenario(inputs: CalculationRequest['inputs']) {
  return loadsScenarios.find((recorded) => {
    const expected: CalculationRequest['inputs'] = recorded.inputs
    return loadsCalculationType.inputs.every((input) =>
      Object.is(inBaseUnit(inputs[input.name], input.base_unit), inBaseUnit(expected[input.name], input.base_unit)),
    )
  })?.envelope
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function error(status: number, body: ErrorBody) {
  return HttpResponse.json(body, { status })
}

function invalidInput(location: (string | number)[], message: string) {
  return error(422, {
    code: 'invalid_input',
    message: 'The inputs do not fit the calculation type.',
    fields: [{ location, message }],
  })
}

function invalidSchema(location: (string | number)[], message: string) {
  return error(422, {
    code: 'validation_error',
    message: 'The request does not match the calculation schema.',
    fields: [{ location, message }],
  })
}

export const serviceUnavailable = http.post('*/calculations', () =>
  error(503, {
    code: 'parameter_source_unavailable',
    message: 'The parameter source is not available.',
  }),
)

export const handlers = [
  http.get('*/calculation-types', () => HttpResponse.json(calculationTypes)),

  http.post('*/calculations', async ({ request }) => {
    let body: unknown
    try {
      body = await request.json()
    } catch {
      return invalidSchema(['body'], 'Expected a JSON calculation request.')
    }
    if (!isRecord(body) || Object.keys(body).some((name) => name !== 'calculation_type' && name !== 'inputs')) {
      return invalidSchema(['body'], 'Expected a calculation type and inputs.')
    }
    const { calculation_type, inputs } = body
    if (typeof calculation_type !== 'string' || !calculation_type || !isRecord(inputs)) {
      return invalidSchema(['body'], 'Expected a calculation type and inputs.')
    }
    const type = calculationTypes.find((candidate) => candidate.name === calculation_type)
    if (!type) {
      return invalidInput(['body', 'calculation_type'], 'Unknown calculation type.')
    }
    const missing = type.inputs.find((input) => !(input.name in inputs))
    if (missing) {
      return invalidInput(['body', 'inputs', missing.name], 'Missing input.')
    }
    const quantities: CalculationRequest['inputs'] = {}
    for (const [name, value] of Object.entries(inputs)) {
      const declaration = type.inputs.find((input) => input.name === name)
      if (!declaration) return invalidInput(['body', 'inputs', name], 'Undeclared input.')
      if (!isRecord(value) || Object.keys(value).some((key) => key !== 'value' && key !== 'unit')) {
        return invalidSchema(['body', 'inputs', name], 'Expected a value and unit.')
      }
      if (typeof value.value !== 'number' || !Number.isFinite(value.value)) {
        return invalidSchema(['body', 'inputs', name, 'value'], 'Expected a finite number.')
      }
      if (typeof value.unit !== 'string') {
        return invalidSchema(['body', 'inputs', name, 'unit'], 'Expected a unit.')
      }
      if (!Object.hasOwn(UNIT_FACTORS, value.unit)) {
        return invalidSchema(['body', 'inputs', name, 'unit'], 'Expected a supported unit.')
      }
      if (!declaration.units.includes(value.unit)) {
        return invalidInput(['body', 'inputs', name], 'Expected a unit of the declared dimension.')
      }
      quantities[name] = { value: value.value, unit: value.unit }
    }
    const envelope = calculation_type === LOADS_TYPE ? loadsScenario(quantities) : pilotScenario(quantities)
    if (!envelope) {
      return error(422, {
        code: 'mock_fixture_unavailable',
        message: 'No recorded mock result matches these inputs.',
      })
    }
    return envelopeResponse(envelope, 201, `/calculations/${envelope.result_id}`)
  }),

  http.get('*/calculations/:id', ({ params }) => {
    const envelope = lookup(params.id)
    return envelope
      ? envelopeResponse(envelope)
      : error(404, { code: 'not_found', message: 'The requested resource does not exist.' })
  }),

  http.post('*/calculations/:id/report', ({ params }) => {
    if (!lookup(params.id)) {
      return error(404, { code: 'not_found', message: 'The requested resource does not exist.' })
    }
    return new HttpResponse(new Uint8Array([0x50, 0x4b, 0x03, 0x04]), {
      headers: {
        'Content-Type': DOCX,
        'Content-Disposition': 'attachment; filename="report.docx"',
      },
    })
  }),
]

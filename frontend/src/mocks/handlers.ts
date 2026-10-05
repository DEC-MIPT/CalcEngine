import { http, HttpResponse } from 'msw'
import type { components } from '../api/schema'
import { calculationTypes, FAIL_ID, failEnvelope, PASS_ID, passEnvelope } from './fixtures'

type CalculationRequest = components['schemas']['CalculationRequest']
type ErrorBody = components['schemas']['ErrorBody']

const DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
const RESISTANCE_KPA = 172.5

const envelopes = { [PASS_ID]: passEnvelope, [FAIL_ID]: failEnvelope } as const

function lookup(id: unknown) {
  const key = String(id)
  return Object.hasOwn(envelopes, key) ? envelopes[key as keyof typeof envelopes] : undefined
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

export const serviceUnavailable = http.post('*/calculations', () =>
  error(503, {
    code: 'parameter_source_unavailable',
    message: 'The parameter source is not available.',
  }),
)

export const handlers = [
  http.get('*/calculation-types', () => HttpResponse.json(calculationTypes)),

  http.post('*/calculations', async ({ request }) => {
    const { calculation_type, inputs } = (await request.json()) as CalculationRequest
    const type = calculationTypes.find((candidate) => candidate.name === calculation_type)
    if (!type) {
      return invalidInput(['body', 'calculation_type'], 'Unknown calculation type.')
    }
    const missing = type.inputs.find((input) => !(input.name in inputs))
    if (missing) {
      return invalidInput(['body', 'inputs', missing.name], 'Missing input.')
    }
    const envelope = inputs.p.value > RESISTANCE_KPA ? failEnvelope : passEnvelope
    return HttpResponse.json(envelope, {
      status: 201,
      headers: { Location: `/calculations/${envelope.result_id}` },
    })
  }),

  http.get('*/calculations/:id', ({ params }) => {
    const envelope = lookup(params.id)
    return envelope
      ? HttpResponse.json(envelope)
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

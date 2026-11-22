import { describe, expect, it } from 'vitest'
import { CANDIDATE_LIMIT } from '@/lib/foundationDesign'
import { loadsCalculationType } from '@/mocks/loadsFixtures'
import { readCandidates, selectionErrors } from './foundationCandidates'

const row = { id: 9, b: '0200,00', bUnit: 'cm', l: '3000', lUnit: 'mm' }
const t = (key: string) => key

describe('foundation candidate request and errors', () => {
  it('keeps all 256 rows, duplicates, decimal inputs and original units', () => {
    const rows = Array.from({ length: CANDIDATE_LIMIT }, (_, id) => ({ ...row, id }))
    const { errors, values } = readCandidates(rows, t)
    expect(errors).toEqual({})
    expect(values).toHaveLength(256)
    expect(values[255]).toEqual({ b: { value: 200, unit: 'cm' }, l: { value: 3000, unit: 'mm' } })
  })

  it('rejects missing and negative dimensions independently', () => {
    expect(readCandidates([{ ...row, b: '', l: '-1' }], t).errors).toEqual({
      '9-b': 'foundation.positive', '9-l': 'foundation.positive',
    })
  })

  it('reports by common input and original row; deduplicates generic messages', () => {
    const errors = selectionErrors([
      { location: ['body', 'common_inputs', 'h'], message: 'common' },
      { location: ['body', 'common_inputs', 'h'], message: 'duplicate' },
      { location: ['body', 'common_inputs', 'unknown'], message: 'generic' },
      { location: ['body', 'candidates', 1, 'l'], message: 'generic' },
      { location: ['body', 'candidates', 0, 'b'], message: 'candidate' },
      { location: ['body', 'candidates', 0, 'b'], message: 'duplicate' },
      { location: ['body', 'candidates', 0, 'other'], message: 'generic' },
      { location: ['body', 'candidates', 0, 'l'], message: 'length' },
    ], loadsCalculationType.inputs, [row])
    expect(errors).toEqual({ byField: { h: 'common' }, byCandidate: { '9-b': 'candidate', '9-l': 'length' }, general: ['generic'] })
  })
})

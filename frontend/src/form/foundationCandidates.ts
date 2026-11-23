import type { FieldError } from '@/api/client'
import type { components } from '@/api/schema'
import type { useI18n } from '@/i18n/context'
import type { CandidateDraft } from './draftContext'
import { parseValue } from './parseValue'

type Candidate = components['schemas']['FoundationCandidate']
type Input = components['schemas']['InputView']

export const candidateFieldId = (key: string) => `candidate-${key}`

export function readCandidates(rows: readonly CandidateDraft[], t: ReturnType<typeof useI18n>['t']) {
  const errors: Record<string, string> = {}
  const values = rows.map((row): Candidate => {
    function quantity(axis: 'b' | 'l') {
      const parsed = parseValue(row[axis], false)
      if (!parsed.ok || parsed.value <= 0) {
        errors[`${row.id}-${axis}`] = t('foundation.positive')
      }
      return { value: parsed.ok ? parsed.value : 0, unit: row[`${axis}Unit`] }
    }
    return { b: quantity('b'), l: quantity('l') }
  })
  return { errors, values }
}

export function selectionErrors(fields: readonly FieldError[], inputs: readonly Input[], rows: readonly CandidateDraft[]) {
  const byField: Record<string, string> = {}
  const byCandidate: Record<string, string> = {}
  const general: string[] = []
  for (const { location: [, group, key, axis], message } of fields) {
    if (group === 'common_inputs' && typeof key === 'string' && inputs.some((item) => item.name === key)) {
      byField[key] ??= message
    } else if (group === 'candidates' && typeof key === 'number' && rows[key] && (axis === 'b' || axis === 'l')) {
      byCandidate[`${rows[key].id}-${axis}`] ??= message
    } else {
      if (!general.includes(message)) general.push(message)
    }
  }
  return { byField, byCandidate, general }
}

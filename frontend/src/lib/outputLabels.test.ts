import { describe, expect, it } from 'vitest'
import { calculationTypes, loadsCalculationType } from '@/mocks/fixtures'
import { outputLabels } from './outputLabels'

describe('unambiguous output metadata labels', () => {
  it('returns no guessed labels without type metadata', () => {
    expect(outputLabels([], 'ru').size).toBe(0)
  })

  it('uses localized labels and the existing Russian fallback', () => {
    expect(outputLabels(calculationTypes, 'ru').get('R')).toBe('Расчётное сопротивление грунта')
    expect(outputLabels([loadsCalculationType], 'en').get('p')).toBe('Среднее давление')
  })

  it('omits conflicts permanently while retaining independent output labels', () => {
    const conflicting = {
      ...loadsCalculationType,
      outputs: loadsCalculationType.outputs.map((output) => output.name === 'p'
        ? { ...output, label: { ru: 'Other meaning', en: 'Other meaning' } }
        : output),
    }
    const labels = outputLabels([loadsCalculationType, conflicting, loadsCalculationType], 'ru')
    expect(labels.has('p')).toBe(false)
    expect(labels.get('p_x_min')).toBe('Минимальное давление по x')
  })
})

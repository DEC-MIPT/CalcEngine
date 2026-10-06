import { describe, expect, it } from 'vitest'
import { unitLabel } from './units'

describe('unitLabel', () => {
  it.each([
    ['m', 'м'],
    ['mm', 'мм'],
    ['kPa', 'кПа'],
    ['kN/m3', 'кН/м³'],
    ['deg', '°'],
    ['rad', 'рад'],
    ['1', 'безразм.'],
  ])('shows %s as %s in Russian', (code, label) => {
    expect(unitLabel(code, 'ru')).toBe(label)
  })

  it('keeps the code in English and for a code outside the vocabulary', () => {
    expect(unitLabel('kPa', 'en')).toBe('kPa')
    expect(unitLabel('furlong', 'ru')).toBe('furlong')
  })
})

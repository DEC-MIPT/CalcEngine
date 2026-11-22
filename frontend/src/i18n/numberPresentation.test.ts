import { describe, expect, it } from 'vitest'
import { formatNumber } from './translate'

describe('unrounded number presentation', () => {
  it.each([1e-25, -1e-25, Number.MIN_VALUE, -Number.MIN_VALUE])('preserves raw nonzero %s in scientific notation', (value) => {
    expect(formatNumber(value, 'en')).not.toBe('0')
    expect(formatNumber(value, 'en')).not.toBe('-0')
    expect(formatNumber(value, 'en')).toContain('E')
  })

  it('keeps scientific mantissas localized', () => {
    expect(formatNumber(1.2345e-25, 'ru')).toBe('1,2345E-25')
    expect(formatNumber(1.2345e-25, 'en')).toBe('1.2345E-25')
  })

  it('preserves ordinary zeros, explicit output decimals and the decimal precision boundary', () => {
    expect(formatNumber(0, 'en')).toBe('0')
    expect(formatNumber(-0, 'en')).toBe('-0')
    expect(formatNumber(1e-25, 'en', 2)).toBe('0.00')
    expect(formatNumber(1e-20, 'en')).toBe('0.00000000000000000001')
    expect(formatNumber(120, 'ru', 2)).toBe('120,00')
  })
})

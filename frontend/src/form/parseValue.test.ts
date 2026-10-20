import { describe, expect, it } from 'vitest'
import { parseValue } from './parseValue'

describe('parseValue', () => {
  it.each([
    ['empty', ''],
    ['empty', '   '],
    ['notNumber', 'abc'],
    ['notNumber', '1.2.3'],
    ['notNumber', '0x10'],
    ['notNumber', 'Infinity'],
    ['notNumber', '1e'],
    ['notFinite', '1e999'],
    ['notFinite', '-1e999'],
  ])('rejects as %s: %j', (error, text) => {
    expect(parseValue(text, false)).toEqual({ ok: false, error })
  })

  it.each([
    ['30', 30],
    ['30.0', 30],
    ['30e0', 30],
    ['-2.5', -2.5],
    ['+7', 7],
    ['.5', 0.5],
    ['172,5', 172.5],
    [' 12 ', 12],
    ['1E3', 1000],
  ])('accepts %j as %d', (text, value) => {
    expect(parseValue(text, false)).toEqual({ ok: true, value })
  })

  it('accepts a whole value spelled in any way on a whole-values input', () => {
    for (const text of ['30', '30.0', '30e0']) {
      expect(parseValue(text, true)).toEqual({ ok: true, value: 30 })
    }
  })

  it('rejects a fraction on a whole-values input and accepts it elsewhere', () => {
    expect(parseValue('30.5', true)).toEqual({ ok: false, error: 'notWhole' })
    expect(parseValue('30.5', false)).toEqual({ ok: true, value: 30.5 })
  })
})

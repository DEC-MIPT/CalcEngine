import { describe, expect, it } from 'vitest'
import { mapFieldErrors } from './serverErrors'

const names = ['b', 'p']

describe('mapFieldErrors', () => {
  it('marks the field that ends the location', () => {
    expect(mapFieldErrors([{ location: ['body', 'inputs', 'p'], message: 'bad p' }], names)).toEqual({
      byField: { p: 'bad p' },
      general: [],
    })
  })

  it('marks two fields', () => {
    const mapped = mapFieldErrors(
      [
        { location: ['body', 'inputs', 'b'], message: 'bad b' },
        { location: ['body', 'inputs', 'p'], message: 'bad p' },
      ],
      names,
    )
    expect(mapped.byField).toEqual({ b: 'bad b', p: 'bad p' })
    expect(mapped.general).toEqual([])
  })

  it('keeps the first message of a field', () => {
    const mapped = mapFieldErrors(
      [
        { location: ['p'], message: 'first' },
        { location: ['p'], message: 'second' },
      ],
      names,
    )
    expect(mapped.byField).toEqual({ p: 'first' })
  })

  it('sends an entry that names no field, or ends with an index, above the form', () => {
    const mapped = mapFieldErrors(
      [
        { location: ['body', 'calculation_type'], message: 'unknown type' },
        { location: ['body', 'inputs', 0], message: 'by index' },
        { location: [], message: 'no place' },
      ],
      names,
    )
    expect(mapped).toEqual({ byField: {}, general: ['unknown type', 'by index', 'no place'] })
  })
})

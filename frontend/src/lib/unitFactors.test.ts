/// <reference types="node" />
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, expect, it } from 'vitest'
import { calculationTypes } from '@/mocks/fixtures'
import { toBaseUnit, UNIT_FACTORS } from './unitFactors'

const backendUnits = readFileSync(resolve(process.cwd(), '../backend/app/schemas/units.py'), 'utf-8')

function backendFactors(): Record<string, number> {
  const found: Record<string, number> = {}
  for (const [, symbol, expression] of backendUnits.matchAll(/Unit\(symbol="([^"]+)",[^)]*?factor=([^)]+)\)/g)) {
    found[symbol] = expression.includes('math.pi') ? Math.PI / Number(expression.split('/')[1]) : Number(expression)
  }
  return found
}

describe('unit factors of the echo (9.3)', () => {
  it('match the backend table: the same units with the same factors', () => {
    const backend = backendFactors()

    expect(Object.keys(backend).length).toBeGreaterThan(10)
    expect(Object.keys(UNIT_FACTORS).sort()).toEqual(Object.keys(backend).sort())
    for (const [symbol, factor] of Object.entries(backend)) {
      expect(UNIT_FACTORS[symbol]).toBeCloseTo(factor, 15)
    }
  })

  it('cover every unit that the mock types list', () => {
    const listed = new Set(
      (calculationTypes as unknown as { inputs: { units: string[]; base_unit: string }[] }[]).flatMap((type) =>
        type.inputs.flatMap((input) => [...input.units, input.base_unit]),
      ),
    )

    for (const unit of listed) expect(UNIT_FACTORS).toHaveProperty(unit)
  })

  it.each([
    [2, 'cm', 'm', 0.02],
    [2, 'mm', 'm', 0.002],
    [150, 'MPa', 'kPa', 150000],
    [150000, 'Pa', 'kPa', 150],
    [18, 'N/m3', 'kN/m3', 0.018],
    [90, 'deg', 'rad', 1.5708],
    [3, 'm', 'm', 3],
    [0, 'cm', 'm', 0],
  ])('converts %s %s to %s as %s without float noise', (value, unit, base, expected) => {
    expect(toBaseUnit(value, unit, base)).toBe(expected)
  })

  it('gives nothing for a unit with no factor, a prototype name or an overflow', () => {
    expect(toBaseUnit(1, 'furlong', 'm')).toBeNull()
    expect(toBaseUnit(1, 'm', 'furlong')).toBeNull()
    expect(toBaseUnit(1, 'constructor', 'm')).toBeNull()
    expect(toBaseUnit(1e308, 'MN', 'N')).toBeNull()
  })
})

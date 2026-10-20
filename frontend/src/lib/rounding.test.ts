import { describe, expect, it } from 'vitest'
import type { components } from '@/api/schema'
import { checkRounding, outputRounding, roundValue } from './rounding'

type Envelope = components['schemas']['ResultEnvelope']
type CheckStep = Extract<Envelope['trace'][number], { kind: 'check' }>

const halfUp = (decimals: number) => ({ decimals, mode: 'half_up' as const })
const halfEven = (decimals: number) => ({ decimals, mode: 'half_even' as const })

describe('roundValue', () => {
  it.each([
    [168.28900000000002, halfUp(2), 168.29],
    [168.28900000000002, halfUp(1), 168.3],
    [2.675, halfUp(2), 2.68],
    [1.005, halfUp(2), 1.01],
    [-2.5, halfUp(0), -3],
    [2.5, halfEven(0), 2],
    [3.5, halfEven(0), 4],
    [0.125, halfEven(2), 0.12],
    [1e-7, halfUp(2), 0],
    [172.5, halfUp(2), 172.5],
  ])('rounds %s by %o to %s, from its shortest decimal like the backend', (value, rule, rounded) => {
    expect(roundValue(value, rule)).toBe(rounded)
  })
})

describe('outputRounding', () => {
  it('maps each output quantity to its rule', () => {
    const outputs = [{ quantity: 'R', rounding_rule: halfUp(2) }] as unknown as Envelope['outputs']

    expect(Object.fromEntries(outputRounding(outputs))).toEqual({ R: halfUp(2) })
  })
})

describe('checkRounding', () => {
  const check = (left: number, operator: CheckStep['operator'], right: number, passed: boolean, symbols = ['p', 'R']) =>
    ({
      kind: 'check',
      step_id: 'c',
      expression: 'p \\le R',
      substitutions: [
        { symbol: symbols[0], value: left, unit: 'kPa' },
        { symbol: symbols[1], value: right, unit: 'kPa' },
      ],
      result: { value: left, unit: 'kPa' },
      right: { value: right, unit: 'kPa' },
      norm_refs: [],
      operator,
      passed,
    }) as CheckStep
  const rounding = new Map([['R', halfUp(2)]])

  it('rounds each side that is an output', () => {
    expect(checkRounding(check(150, 'le', 168.289, true), rounding)).toEqual([undefined, halfUp(2)])
    expect(checkRounding(check(168.289, 'ge', 150, true, ['R', 'p']), rounding)).toEqual([halfUp(2), undefined])
  })

  it.each([
    ['le', 168.29, 168.289, false],
    ['lt', 168.29, 168.2949, true],
    ['ge', 168.29, 168.2949, false],
    ['gt', 168.3, 168.2951, true],
  ] as const)('rounds no side when rounding would contradict the check (%s)', (operator, left, right, passed) => {
    expect(checkRounding(check(left, operator, right, passed), rounding)).toEqual([undefined, undefined])
  })
})

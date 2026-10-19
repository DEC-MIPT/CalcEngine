import { describe, expect, it } from 'vitest'
import type { components } from '@/api/schema'
import { calculationTypes } from '@/mocks/fixtures'
import { stepSymbol, symbolTable } from './stepSymbol'

type Step = components['schemas']['ResultEnvelope']['trace'][number]
type CalculationType = components['schemas']['CalculationTypeView']

const step = (step_id: string, kind: Step['kind'], expression: string) =>
  ({ step_id, kind, expression, substitutions: [], result: { value: 1, unit: '1' }, norm_refs: [] }) as unknown as Step

describe('stepSymbol', () => {
  it.each([
    ['table', '\\gamma_{c1}', '\\gamma_{c1}'],
    ['table', 'M_{\\gamma} = M_{\\gamma}\\left(\\varphi_{II}\\right)', 'M_{\\gamma}'],
    ['formula', 'k_z = 1', 'k_z'],
    ['formula', 'R = \\frac{\\gamma_{c1}\\gamma_{c2}}{k}', 'R'],
    ['formula', 'S_{i=1} = \\sum_{i=1}^{n} a_i', 'S_{i=1}'],
    ['check', 'p \\le R', 'p \\le R'],
    ['check', 'a = b', 'a = b'],
  ] as const)('reads the symbol of a %s step from %s', (kind, expression, symbol) => {
    expect(stepSymbol(step('s', kind, expression))).toBe(symbol)
  })

  it.each([
    ['formula', '\\frac{a}{b}'],
    ['formula', ' = 1'],
  ] as const)('finds no symbol in a %s step %s', (kind, expression) => {
    expect(stepSymbol(step('s', kind, expression))).toBeNull()
  })
})

describe('symbolTable', () => {
  const steps = [step('gamma_c1', 'table', '\\gamma_{c1}'), step('q', 'formula', '\\frac{a}{b}'), step('R', 'formula', 'R = 1')]

  it('maps each step with a symbol by its id', () => {
    expect(Object.fromEntries(symbolTable(steps))).toEqual({ gamma_c1: '\\gamma_{c1}', R: 'R' })
  })

  it('adds the inputs and outputs of the calculation types', () => {
    const table = symbolTable(steps, calculationTypes as unknown as CalculationType[])

    expect(table.get('phi_II')).toBe('\\varphi_{II}')
    expect(table.get('gamma_II_prime')).toBe("\\gamma'_{II}")
    expect(table.get('R')).toBe('R')
    expect(table.get('gamma_c1')).toBe('\\gamma_{c1}')
  })

  it('keeps a name that two types declare alike and drops one they declare differently', () => {
    const type = (symbols: Record<string, string>) =>
      ({ inputs: Object.entries(symbols).map(([name, symbol]) => ({ name, symbol })), outputs: [] }) as unknown as CalculationType
    const table = symbolTable(
      [step('x', 'table', 'x_{step}')],
      [type({ a: 'a_1', x: 'x_1' }), type({ a: 'a_1', x: 'x_2' }), type({ x: 'x_1' })],
    )

    expect(table.get('a')).toBe('a_1')
    expect(table.get('x')).toBe('x_{step}')
  })
})

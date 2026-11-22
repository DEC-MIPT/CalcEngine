import { describe, expect, it } from 'vitest'
import type { components } from '@/api/schema'
import { calculationTypes, loadsCentralEnvelope, passEnvelope } from '@/mocks/fixtures'
import { symbolTable } from './stepSymbol'
import { checkPresentation } from './checkPresentation'

type Step = components['schemas']['ResultEnvelope']['trace'][number]
type Check = Extract<Step, { kind: 'check' }>
const checks = loadsCentralEnvelope.trace.filter((step) => step.kind === 'check')
const pilot = passEnvelope.trace.find((step) => step.kind === 'check')!

describe('closed typed-check display convention', () => {
  it('uses supplied symbols for all four checks, including the complete corner subscript', () => {
    const before = JSON.stringify(loadsCentralEnvelope)
    const symbols = symbolTable(loadsCentralEnvelope.trace, calculationTypes)
    expect(checks.map((step) => checkPresentation(step, symbols))).toEqual([
      String.raw`p \le R`, String.raw`p_{x,max} \le p_{edge,lim}`,
      String.raw`p_{y,max} \le p_{edge,lim}`, String.raw`p_{corner,max} \le p_{corner,lim}`,
    ])
    expect(JSON.stringify(loadsCentralEnvelope)).toBe(before)
  })

  it('retains the normal pilot spelling and never derives values or outcomes', () => {
    expect(checkPresentation(pilot)).toBe(pilot.expression)
    expect(checkPresentation({ ...pilot, passed: !pilot.passed, result: { value: 1e-25, unit: 'kPa' } })).toBe(pilot.expression)
  })

  it.each([['le', String.raw`\le`], ['lt', '<'], ['ge', String.raw`\ge`], ['gt', '>']] as const)(
    'matches only the supplied engine spelling for %s', (operator, spelling) => {
      const step: Check = { ...pilot, operator, expression: `p ${spelling} R` }
      expect(checkPresentation(step)).toBe(step.expression)
    },
  )

  it('escapes literal identifiers when metadata is absent or trace aliases are ambiguous', () => {
    expect(checkPresentation(checks[1])).toBe(String.raw`\mathrm{p\_x\_max} \le \mathrm{edge\_limit}`)
    expect(checkPresentation(checks[1], symbolTable(loadsCentralEnvelope.trace))).toBe(String.raw`\mathrm{p\_x\_max} \le p_{edge,lim}`)
    const aliases = new Map([['p_x_max', 'q'], ['other_quantity', 'q'], ['edge_limit', 'L']])
    expect(checkPresentation(checks[1], aliases)).toBe(String.raw`\mathrm{p\_x\_max} \le L`)
  })

  it.each([String.raw`\gamma'_{II}`, String.raw`\varphi_{II}`, 'p_{++}', 'W_x'])(
    'accepts the closed single-quantity alias %s', (alias) => {
      expect(checkPresentation(pilot, new Map([['p', alias]]))).toBe(`${alias} \\le R`)
    },
  )

  it.each([
    String.raw`\href{javascript:alert(1)}{p}`, String.raw`\class{evil}{p}`,
    String.raw`\require{html}`, String.raw`\frac{p}{R}`, 'p_x_max', 'p+q', '',
  ])('rejects an unsupported or hostile alias %s', (alias) => {
    expect(checkPresentation(pilot, new Map([['p', alias]]))).toBeNull()
    expect(checkPresentation(pilot, new Map([['R', alias]]))).toBeNull()
  })

  it.each([String.raw`p  \le R`, String.raw`p \le R `, 'p < R', String.raw`p \le R \href{x}{y}`])(
    'does not repair an expression outside the exact typed grammar: %s', (expression) => {
      expect(checkPresentation({ ...pilot, expression })).toBeNull()
    },
  )

  it('rejects missing, extra or unsafe substitution identifiers', () => {
    for (const substitutions of [[], [pilot.substitutions[0]], [...pilot.substitutions, pilot.substitutions[0]]]) {
      expect(checkPresentation({ ...pilot, substitutions })).toBeNull()
    }
    for (const symbol of ['p-x', String.raw`\href{x}{y}`, 'p R']) {
      const left = { ...pilot.substitutions[0], symbol }
      expect(checkPresentation({ ...pilot, expression: `${symbol} \\le R`, substitutions: [left, pilot.substitutions[1]] })).toBeNull()
      const right = { ...pilot.substitutions[1], symbol }
      expect(checkPresentation({ ...pilot, expression: `p \\le ${symbol}`, substitutions: [pilot.substitutions[0], right] })).toBeNull()
    }
  })

  it('fails closed for malformed runtime bindings and inherited operator keys', () => {
    for (const substitutions of [null, {}, [null, pilot.substitutions[1]], [pilot.substitutions[0], null],
      [{ symbol: 1 }, pilot.substitutions[1]], [pilot.substitutions[0], { symbol: 1 }]]) {
      expect(checkPresentation({ ...pilot, substitutions } as unknown as Check)).toBeNull()
    }
    for (const operator of ['constructor', '__proto__', 'toString']) {
      expect(checkPresentation({ ...pilot, operator } as unknown as Check)).toBeNull()
    }
    expect(checkPresentation(pilot, new Map([['p', 1]]) as unknown as ReadonlyMap<string, string>)).toBeNull()
  })
})

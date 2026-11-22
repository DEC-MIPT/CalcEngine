import type { components } from '@/api/schema'

type Step = components['schemas']['ResultEnvelope']['trace'][number]
type CheckStep = Extract<Step, { kind: 'check' }>

const OPERATORS = { le: String.raw`\le`, lt: '<', ge: String.raw`\ge`, gt: '>' } as const
const NO_SYMBOLS: ReadonlyMap<string, string> = new Map()
const IDENTIFIER = /^[A-Za-z][A-Za-z0-9_]*$/
const SYMBOL = /^(?:[A-Za-z][A-Za-z0-9]*|\\(?:alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|vartheta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|varphi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Upsilon|Phi|Psi|Omega))(?:'*_(?:[A-Za-z0-9]|\{[A-Za-z0-9,+-]+\})'*|'*)$/

function literalIdentifier(identifier: string): string {
  return identifier.includes('_') ? `\\mathrm{${identifier.replaceAll('_', String.raw`\_`)}}` : identifier
}

function operand(identifier: string, symbols: ReadonlyMap<string, string>): string | null {
  const alias = symbols.get(identifier)
  if (alias === undefined) return literalIdentifier(identifier)
  if (typeof alias !== 'string' || !SYMBOL.test(alias)) return null
  for (const [name, symbol] of symbols) {
    if (name !== identifier && symbol === alias) return literalIdentifier(identifier)
  }
  return alias
}

export function checkPresentation(step: CheckStep, symbols: ReadonlyMap<string, string> = NO_SYMBOLS): string | null {
  if (!Array.isArray(step.substitutions) || step.substitutions.length !== 2) return null
  const [left, right] = step.substitutions
  if (!left || !right || typeof left.symbol !== 'string' || typeof right.symbol !== 'string') return null
  if (!IDENTIFIER.test(left.symbol) || !IDENTIFIER.test(right.symbol)) return null
  if (!Object.hasOwn(OPERATORS, step.operator)) return null
  const operator = OPERATORS[step.operator]
  if (step.expression !== `${left.symbol} ${operator} ${right.symbol}`) return null
  const shownLeft = operand(left.symbol, symbols)
  const shownRight = operand(right.symbol, symbols)
  return shownLeft === null || shownRight === null ? null : `${shownLeft} ${operator} ${shownRight}`
}

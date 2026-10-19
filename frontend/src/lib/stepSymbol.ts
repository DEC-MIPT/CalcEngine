import type { components } from '@/api/schema'

type Step = components['schemas']['ResultEnvelope']['trace'][number]
type CalculationType = components['schemas']['CalculationTypeView']

function leftSide(expression: string): string | null {
  let depth = 0
  for (let index = 0; index < expression.length; index++) {
    const char = expression[index]
    if (char === '{') depth++
    else if (char === '}') depth--
    else if (char === '=' && depth === 0) return expression.slice(0, index).trim() || null
  }
  return null
}

export function stepSymbol(step: Step): string | null {
  if (step.kind === 'check') return step.expression
  return leftSide(step.expression) ?? (step.kind === 'table' ? step.expression : null)
}

export function symbolTable(steps: readonly Step[], types: readonly CalculationType[] = []): ReadonlyMap<string, string> {
  const table = new Map<string, string>()
  for (const step of steps) {
    const symbol = stepSymbol(step)
    if (symbol !== null) table.set(step.step_id, symbol)
  }
  const declared = new Map<string, string | null>()
  for (const type of types) {
    for (const quantity of [...type.inputs, ...type.outputs]) {
      const known = declared.get(quantity.name)
      declared.set(quantity.name, known === undefined || known === quantity.symbol ? quantity.symbol : null)
    }
  }
  for (const [name, symbol] of declared) {
    if (symbol !== null) table.set(name, symbol)
  }
  return table
}

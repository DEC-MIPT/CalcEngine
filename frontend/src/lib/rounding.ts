import type { components } from '@/api/schema'

type RoundingRule = components['schemas']['RoundingRule']
type Envelope = components['schemas']['ResultEnvelope']
type CheckStep = Extract<Envelope['trace'][number], { kind: 'check' }>

export type OutputRounding = ReadonlyMap<string, RoundingRule>

const MODES = { half_up: 'halfExpand', half_even: 'halfEven' } as const

export function roundValue(value: number, rule: RoundingRule): number {
  const format = new Intl.NumberFormat('en-US', {
    maximumFractionDigits: rule.decimals,
    roundingMode: MODES[rule.mode],
    useGrouping: false,
  })
  return Number(format.format(String(value) as Intl.StringNumericLiteral))
}

export function outputRounding(outputs: Envelope['outputs']): OutputRounding {
  return new Map(outputs.map((output) => [output.quantity, output.rounding_rule]))
}

const HOLDS: Record<CheckStep['operator'], (left: number, right: number) => boolean> = {
  le: (left, right) => left <= right,
  lt: (left, right) => left < right,
  ge: (left, right) => left >= right,
  gt: (left, right) => left > right,
}

export function checkRounding(
  step: CheckStep,
  rounding: OutputRounding,
): readonly [RoundingRule | undefined, RoundingRule | undefined] {
  const [left, right] = step.substitutions.map((substitution) => rounding.get(substitution.symbol))
  const shown = (value: number, rule: RoundingRule | undefined) => (rule ? roundValue(value, rule) : value)
  const agrees = HOLDS[step.operator](shown(step.result.value, left), shown(step.right.value, right)) === step.passed
  return agrees ? [left, right] : [undefined, undefined]
}

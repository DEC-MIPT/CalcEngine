import { WarningCircle } from '@phosphor-icons/react'
import type { components } from '@/api/schema'
import { useResultRounding } from '@/lib/resultDisplay'
import { preservesComparison } from '@/lib/rounding'
import { useI18n } from '@/i18n/context'
import { QuantityText } from './Quantity'

type Quantity = components['schemas']['QuantityValue']
export type BoundShape = { quantity: string; kind: 'min' | 'max'; value: number; inclusive: boolean }

const OPERATORS = {
  max: { inclusive: 'le', exclusive: 'lt' },
  min: { inclusive: 'ge', exclusive: 'gt' },
} as const

const SYMBOLS = { le: '≤', lt: '<', ge: '≥', gt: '>' } as const

function Amount({ value, unit }: { value: number; unit: string }) {
  return <QuantityText value={value} unit={unit} />
}

export function BoundNote({ id, bound, unit }: { id: string; bound: BoundShape; unit: string }) {
  const { t } = useI18n()
  const operator = OPERATORS[bound.kind][bound.inclusive ? 'inclusive' : 'exclusive']
  return (
    <p
      id={id}
      className="flex items-start gap-1.5 border border-warning bg-warning-surface px-2 py-1 text-sm text-warning-foreground"
    >
      <WarningCircle aria-hidden="true" weight="fill" size={16} className="mt-0.5 shrink-0" />
      <span>
        {t('form.boundNote')}: <code>{bound.quantity}</code> <span aria-hidden="true">{SYMBOLS[operator]}</span>
        <span className="sr-only">{t(`trace.op.${operator}`)}</span> <Amount value={bound.value} unit={unit} />
      </span>
    </p>
  )
}

export function BoundFacts({
  value,
  bound,
  boundLabel,
}: {
  value: Quantity
  bound: BoundShape
  boundLabel: string
}) {
  const { t } = useI18n()
  const operator = OPERATORS[bound.kind][bound.inclusive ? 'inclusive' : 'exclusive']
  const rule = useResultRounding()
  const rounding = rule && !preservesComparison(operator, value.value, bound.value, rule) ? null : rule
  return (
    <dl className="grid gap-x-4 gap-y-1 sm:grid-cols-[max-content_1fr]">
      <dt className="text-sm font-medium">{t('bound.input')}</dt>
      <dd data-fact="input">
        <code>{bound.quantity}</code> = <QuantityText {...value} rounding={rounding} />
      </dd>
      <dt className="text-sm font-medium">{boundLabel}</dt>
      <dd data-fact="bound">
        <code>{bound.quantity}</code> <span aria-hidden="true">{SYMBOLS[operator]}</span>
        <span className="sr-only">{t(`trace.op.${operator}`)}</span> <QuantityText value={bound.value} unit={value.unit} rounding={rounding} />
      </dd>
    </dl>
  )
}

import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { unitLabel } from '@/i18n/units'

type Quantity = components['schemas']['QuantityValue']
type BoundShape = { quantity: string; kind: 'min' | 'max'; value: number; inclusive: boolean }

const OPERATORS = {
  max: { inclusive: 'le', exclusive: 'lt' },
  min: { inclusive: 'ge', exclusive: 'gt' },
} as const

const SYMBOLS = { le: '≤', lt: '<', ge: '≥', gt: '>' } as const

function Amount({ value, unit }: { value: number; unit: string }) {
  const { language, formatNumber } = useI18n()
  return (
    <>
      {formatNumber(value)} {unitLabel(unit, language)}
    </>
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
  return (
    <dl className="grid gap-x-4 gap-y-1 sm:grid-cols-[max-content_1fr]">
      <dt className="text-sm font-medium">{t('bound.input')}</dt>
      <dd data-fact="input">
        <code>{bound.quantity}</code> = <Amount value={value.value} unit={value.unit} />
      </dd>
      <dt className="text-sm font-medium">{boundLabel}</dt>
      <dd data-fact="bound">
        <code>{bound.quantity}</code> <span aria-hidden="true">{SYMBOLS[operator]}</span>
        <span className="sr-only">{t(`trace.op.${operator}`)}</span> <Amount value={bound.value} unit={value.unit} />
      </dd>
    </dl>
  )
}

import { ArrowRight, CheckCircle, XCircle } from '@phosphor-icons/react'
import { useId } from 'react'
import { Link } from 'react-router'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import type { TextKey } from '@/i18n/dictionary'
import { unitLabel } from '@/i18n/units'
import { EditInputsLink } from './EditInputsLink'
import { Formula } from './Formula'
import { buttonClass } from './ui/button'

type Envelope = components['schemas']['ResultEnvelope']
type Step = Envelope['trace'][number]
type CheckStep = Extract<Step, { kind: 'check' }>
type Quantity = components['schemas']['QuantityValue']
type CheckReason = components['schemas']['CheckReason']

const SYMBOLS = { le: '≤', lt: '<', ge: '≥', gt: '>' } as const

function Reading({ quantity }: { quantity: Quantity }) {
  const { language, formatNumber } = useI18n()
  return (
    <span className="whitespace-nowrap">
      {formatNumber(quantity.value)} <span className="text-muted-foreground">{unitLabel(quantity.unit, language)}</span>
    </span>
  )
}

export function VerdictStamp({
  envelope,
  reason,
  editType = null,
}: {
  envelope: Envelope
  reason: CheckReason
  editType?: string | null
}) {
  const { t, formatNumber } = useI18n()
  const headingId = useId()
  const passed = envelope.verdict === 'pass'
  const check = envelope.trace.find(
    (step): step is CheckStep => step.kind === 'check' && step.step_id === reason.step_id,
  )
  const Icon = passed ? CheckCircle : XCircle
  const tone = passed ? 'border-primary' : 'border-destructive'
  return (
    <section
      aria-labelledby={headingId}
      data-verdict={envelope.verdict}
      className={`grid border-2 bg-card sm:grid-cols-[1fr_auto] ${tone}`}
    >
      <div className="grid gap-2 p-4">
        <h2 id={headingId} className={`flex items-center gap-2 text-verdict font-bold ${passed ? 'text-primary' : 'text-destructive'}`}>
          <Icon aria-hidden="true" weight="fill" size={26} className="shrink-0" />
          {t(passed ? 'verdict.pass' : 'verdict.fail')}
        </h2>
        {check && (
          <div className="flex flex-wrap items-baseline gap-x-5 gap-y-1" data-check={check.step_id}>
            <span className="text-xl">
              <Formula latex={check.expression} />
            </span>
            <p className="font-mono text-verdict">
              <Reading quantity={check.result} /> <span aria-hidden="true">{SYMBOLS[check.operator]}</span>
              <span className="sr-only">{t(`trace.op.${check.operator}`)}</span> <Reading quantity={check.right} />
            </p>
          </div>
        )}
      </div>
      <div className={`grid content-center gap-2 border-t-2 p-4 sm:border-t-0 sm:border-l-2 ${tone}`}>
        <Link to={`/calculations/${envelope.result_id}/report`} className={buttonClass}>
          {t('result.toReport')}
          <ArrowRight aria-hidden="true" size={18} />
        </Link>
        {editType && <EditInputsLink type={editType} primary={false} />}
      </div>
      <dl className={`col-span-full grid border-t text-sm sm:grid-cols-3 ${tone}`}>
        {(
          [
            ['stamp.steps', formatNumber(envelope.trace.length)],
            ['stamp.warnings', formatNumber(envelope.warnings.length)],
            ['stamp.engine', envelope.engine_version],
          ] satisfies [TextKey, string][]
        ).map(([key, value]) => (
          <div
            key={key}
            className="flex items-baseline justify-between gap-3 border-border px-4 py-2 not-last:border-b sm:grid sm:justify-start sm:gap-0.5 sm:not-last:border-r sm:not-last:border-b-0"
          >
            <dt className="text-muted-foreground">{t(key)}</dt>
            <dd className="font-mono">{value}</dd>
          </div>
        ))}
      </dl>
    </section>
  )
}

import { CheckCircle, XCircle } from '@phosphor-icons/react'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { checkRounding, type OutputRounding } from '@/lib/rounding'
import { Checking } from './Checking'
import { Formula } from './Formula'
import { NormRefList } from './NormRefList'
import { QuantityText } from './Quantity'
import type { StampReveal } from './VerdictStamp'

type Step = components['schemas']['ResultEnvelope']['trace'][number]
type Reason = components['schemas']['CheckReason']
const NO_ROUNDING: OutputRounding = new Map()
const OPERATORS = { le: '≤', lt: '<', ge: '≥', gt: '>' } as const

export function StoredChecks({
  steps,
  reason,
  rounding = NO_ROUNDING,
  reveal = 'none',
  normStatus = true,
  labels,
}: {
  steps: readonly Step[]
  reason: Reason
  rounding?: OutputRounding
  reveal?: StampReveal
  normStatus?: boolean
  labels?: ReadonlyMap<string, string>
}) {
  const { t } = useI18n()
  const pending = reveal === 'pending'
  return (
    <section aria-labelledby="checks-title" className="mt-8 grid min-w-0 gap-3" data-reveal={reveal}>
      <h2 id="checks-title">{t('checks.title')}</h2>
      <div className="relative min-w-0">
        {pending && <Checking marker="checks" />}
        <div inert={pending} className={pending ? 'invisible' : undefined}>
          <p className="mb-3 text-sm">
            {t('checks.reason')}: <code className="break-all">{reason.step_id}</code>
          </p>
          <ol className="grid min-w-0 border border-border bg-card">
            {steps.filter((step) => step.kind === 'check').map((step, index) => {
              const [left, right] = checkRounding(step, rounding)
              const Icon = step.passed ? CheckCircle : XCircle
              const label = labels?.get(step.substitutions[0]?.symbol)
              return (
                <li key={step.step_id} data-check-step={step.step_id} data-deciding={step.step_id === reason.step_id} className="grid min-w-0 gap-3 p-3 not-last:border-b not-last:border-border">
                  <div className="flex min-w-0 flex-wrap items-baseline justify-between gap-2">
                    <h3 className="min-w-0 break-words text-base font-semibold">{label ?? `${t('checks.item')} ${index + 1}`}</h3>
                    {step.step_id === reason.step_id && <span className="border border-foreground px-2 text-sm font-semibold">{t('checks.deciding')}</span>}
                  </div>
                  <div
                    role="region"
                    aria-label={`${t('checks.formula')}: ${step.step_id}`}
                    // eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex -- Keyboard users must be able to scroll wide formulas.
                    tabIndex={0}
                    className="min-w-0 overflow-x-auto focus-visible:outline-offset-[-2px]"
                  >
                    <Formula latex={step.expression} />
                  </div>
                  <p className="font-mono" data-comparison>
                    <QuantityText {...step.result} rounding={left} />{' '}
                    <span aria-hidden="true">{OPERATORS[step.operator]}</span>
                    <span className="sr-only">{t(`trace.op.${step.operator}`)}</span>{' '}
                    <QuantityText {...step.right} rounding={right} />
                  </p>
                  <p className={`flex items-center gap-1.5 font-semibold ${step.passed ? 'text-success' : 'text-destructive'}`}>
                    <Icon size={18} weight="fill" aria-hidden="true" className="shrink-0" />
                    {t(step.passed ? 'trace.check.passed' : 'trace.check.failed')}
                  </p>
                  {step.norm_refs.length > 0 && <NormRefList refs={step.norm_refs} showStatus={normStatus} />}
                </li>
              )
            })}
          </ol>
        </div>
      </div>
    </section>
  )
}

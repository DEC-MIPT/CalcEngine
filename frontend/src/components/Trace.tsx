import { CheckCircle, WarningCircle, XCircle } from '@phosphor-icons/react'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { unitLabel } from '@/i18n/units'
import { Formula } from './Formula'
import { NormRefList } from './NormRefList'

type Step = components['schemas']['ResultEnvelope']['trace'][number]
type Quantity = components['schemas']['QuantityValue']

function Value({ quantity }: { quantity: Quantity }) {
  const { language, formatNumber } = useI18n()
  return (
    <>
      {formatNumber(quantity.value)} {unitLabel(quantity.unit, language)}
    </>
  )
}

const SYMBOLS = { le: '≤', lt: '<', ge: '≥', gt: '>' } as const

type CheckStep = Extract<Step, { kind: 'check' }>

function Comparison({ step }: { step: CheckStep }) {
  const { t } = useI18n()
  const Icon = step.passed ? CheckCircle : XCircle
  return (
    <div className="grid gap-1">
      <p>
        <Value quantity={step.result} />{' '}
        <span aria-hidden="true">{SYMBOLS[step.operator]}</span>{' '}
        <span className="sr-only">{t(`trace.op.${step.operator}`)}</span> <Value quantity={step.right} />
      </p>
      <p
        className={
          step.passed
            ? 'inline-flex w-fit items-center gap-1.5 border border-success bg-success-surface px-2 py-0.5 font-medium text-success'
            : 'inline-flex w-fit items-center gap-1.5 border-2 border-destructive bg-destructive-surface px-2 py-0.5 font-medium text-destructive'
        }
      >
        <Icon aria-hidden="true" weight="fill" size={18} />
        {t(step.passed ? 'trace.check.passed' : 'trace.check.failed')}
      </p>
    </div>
  )
}

function TraceStep({ step }: { step: Step }) {
  const { t } = useI18n()
  return (
    <li className="grid gap-3 border border-border bg-card p-4" data-step={step.step_id}>
      <h3 className="flex flex-wrap items-baseline gap-x-3 text-base">
        <code className="font-semibold">{step.step_id}</code>
        <span className="text-sm font-normal text-muted-foreground">{t(`trace.kind.${step.kind}`)}</span>
      </h3>
      <div className="overflow-x-auto">
        <Formula latex={step.expression} display />
      </div>
      {step.substitutions.length > 0 && (
        <div>
          <h4 className="text-sm font-medium">{t('trace.substitutions')}</h4>
          <ul className="flex flex-wrap gap-x-5 gap-y-1">
            {step.substitutions.map((substitution) => (
              <li key={substitution.symbol} className="flex items-baseline gap-1">
                <Formula latex={substitution.symbol} /> <span>=</span> <Value quantity={substitution} />
              </li>
            ))}
          </ul>
        </div>
      )}
      {step.kind === 'check' ? (
        <Comparison step={step} />
      ) : (
        <p>
          <span className="text-sm font-medium">{t('trace.result')}: </span>
          <Value quantity={step.result} />
        </p>
      )}
      {step.norm_refs.length > 0 && (
        <div>
          <h4 className="text-sm font-medium">{t('trace.norms')}</h4>
          <NormRefList refs={step.norm_refs} />
        </div>
      )}
    </li>
  )
}

export function Trace({
  steps,
  unverifiedStepCount,
}: {
  steps: readonly Step[]
  unverifiedStepCount: number
}) {
  const { t, formatNumber } = useI18n()
  return (
    <section aria-labelledby="trace-title" className="mt-8 grid gap-4">
      <h2 id="trace-title">{t('trace.title')}</h2>
      {unverifiedStepCount > 0 && (
        <p className="flex w-fit items-center gap-2 border border-warning bg-warning-surface px-3 py-2 text-warning-foreground">
          <WarningCircle aria-hidden="true" weight="fill" size={20} />
          <span>
            {t('trace.unverified')}: <strong>{formatNumber(unverifiedStepCount)}</strong>
          </span>
        </p>
      )}
      <ol className="grid gap-3">
        {steps.map((step, index) => (
          <TraceStep key={`${step.step_id}-${index}`} step={step} />
        ))}
      </ol>
    </section>
  )
}

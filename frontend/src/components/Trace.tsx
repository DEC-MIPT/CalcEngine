import { CaretRight, CheckCircle, WarningCircle, XCircle } from '@phosphor-icons/react'
import { useId, useLayoutEffect, useRef, useState } from 'react'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { arrivalOf, type Arrival, type TracePlayback } from '@/lib/useTracePlayback'
import { Formula } from './Formula'
import { NormRefList } from './NormRefList'
import { QuantityText } from './Quantity'
import { Button } from './ui/button'

type Step = components['schemas']['ResultEnvelope']['trace'][number]
type Quantity = components['schemas']['QuantityValue']

function Value({ quantity }: { quantity: Quantity }) {
  return <QuantityText value={quantity.value} unit={quantity.unit} />
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

function StepSummary({ step }: { step: Step }) {
  const { t } = useI18n()
  return (
    <span className="ml-auto" data-summary>
      <span className="font-mono">
        <Value quantity={step.result} />
      </span>
      {step.kind === 'check' && <> · {t(step.passed ? 'trace.check.passed' : 'trace.check.failed')}</>}
    </span>
  )
}

const ARRIVAL_CLASS: Record<Arrival, string> = { pending: ' step-pending', reveal: ' step-reveal', shown: '' }

function TraceStep({
  step,
  index,
  expanded,
  onToggle,
  arrival,
}: {
  step: Step
  index: number
  expanded: boolean
  onToggle: () => void
  arrival: Arrival
}) {
  const { t } = useI18n()
  const detailsId = useId()
  return (
    <li
      id={`trace-step-${index}`}
      className={`data-row scroll-mt-4 not-last:border-b not-last:border-border${ARRIVAL_CLASS[arrival]}`}
      data-step={step.step_id}
      data-arrival={arrival}
      inert={arrival === 'pending'}
    >
      <h3 className="text-base">
        <button
          type="button"
          aria-expanded={expanded}
          aria-controls={detailsId}
          onClick={onToggle}
          className="flex w-full cursor-pointer flex-wrap items-baseline gap-x-3 px-3 py-2.5 text-left font-sans hover:bg-secondary focus-visible:outline-offset-[-2px]"
        >
          <CaretRight
            aria-hidden="true"
            size={16}
            className={`shrink-0 self-center transition-transform motion-reduce:transition-none ${expanded ? 'rotate-90' : ''}`}
          />
          <code className="font-semibold">{step.step_id}</code>
          <span className="text-sm text-muted-foreground">{t(`trace.kind.${step.kind}`)}</span>
          <StepSummary step={step} />
        </button>
      </h3>
      <div id={detailsId} hidden={!expanded} className="step-details grid gap-3 border-t border-dashed border-border bg-background/40 px-3 py-3 pl-10">
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
      </div>
    </li>
  )
}

function Counter({ shown, total }: { shown: number; total: number }) {
  const width = String(total).length
  return (
    <>
      {String(shown).padStart(width, '0')}/{total}
    </>
  )
}

export function Trace({
  steps,
  unverifiedStepCount,
  playback,
}: {
  steps: readonly Step[]
  unverifiedStepCount: number
  playback?: TracePlayback
}) {
  const { t, formatNumber } = useI18n()
  const section = useRef<HTMLElement>(null)
  const playing = playback?.phase === 'playing'
  const skip = playback?.skip
  useLayoutEffect(() => {
    const node = section.current
    if (!playing || !node || !skip) return
    node.addEventListener('click', skip)
    return () => node.removeEventListener('click', skip)
  }, [playing, skip])
  const [expanded, setExpanded] = useState<ReadonlySet<number>>(() => new Set(steps.map((_, index) => index)))
  const toggle = (index: number) =>
    setExpanded((current) => {
      const next = new Set(current)
      if (!next.delete(index)) next.add(index)
      return next
    })
  return (
    <section ref={section} aria-labelledby="trace-title" className="mt-8 grid gap-4" data-playback={playback?.phase ?? 'idle'}>
      <h2 id="trace-title" tabIndex={-1} className="scroll-mt-4">
        {t('trace.title')}
      </h2>
      {unverifiedStepCount > 0 && (
        <p className="flex w-fit items-center gap-2 border border-warning bg-warning-surface px-3 py-2 text-warning-foreground">
          <WarningCircle aria-hidden="true" weight="fill" size={20} />
          <span>
            {t('trace.unverified')}: <strong>{formatNumber(unverifiedStepCount)}</strong>
          </span>
        </p>
      )}
      <div className="flex flex-wrap gap-2">
        <Button
          className="border-border bg-card text-foreground hover:bg-secondary"
          onClick={() => setExpanded(new Set(steps.map((_, index) => index)))}
        >
          {t('trace.expandAll')}
        </Button>
        <Button className="border-border bg-card text-foreground hover:bg-secondary" onClick={() => setExpanded(new Set())}>
          {t('trace.collapseAll')}
        </Button>
      </div>
      {playing && (
        <p aria-hidden="true" className="trace-hint flex flex-wrap items-baseline gap-x-3 font-mono text-sm text-muted-foreground" data-skip-hint>
          <span className="text-foreground">
            <span className="trace-caret">▮</span> {t('trace.playing')} <Counter shown={playback.shown} total={steps.length} />
          </span>
          <span>{t('trace.skipHint')}</span>
        </p>
      )}
      <ol className="border border-border bg-card">
        {steps.map((step, index) => (
          <TraceStep
            key={`${step.step_id}-${index}`}
            step={step}
            index={index}
            expanded={expanded.has(index)}
            onToggle={() => toggle(index)}
            arrival={arrivalOf(index, playback)}
          />
        ))}
      </ol>
    </section>
  )
}

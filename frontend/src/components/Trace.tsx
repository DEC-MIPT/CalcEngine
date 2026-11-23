import { CaretRight, CheckCircle, WarningCircle, XCircle } from '@phosphor-icons/react'
import { useId, useMemo, useState } from 'react'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import type { TextKey } from '@/i18n/dictionary'
import { loadsTraceSections, type LoadsTraceSection } from '@/lib/loadsTraceSections'
import { checkRounding, type OutputRounding } from '@/lib/rounding'
import { useResultRounding } from '@/lib/resultDisplay'
import { checkPresentation } from '@/lib/checkPresentation'
import { symbolTable } from '@/lib/stepSymbol'
import { arrivalOf, type Arrival, type TracePlayback } from '@/lib/useTracePlayback'
import { Formula } from './Formula'
import { NamedSymbol } from './NamedSymbol'
import { NormRefList } from './NormRefList'
import { QuantityText } from './Quantity'
import { Source } from './Source'
import { Button } from './ui/button'

type Step = components['schemas']['ResultEnvelope']['trace'][number]
type Quantity = components['schemas']['QuantityValue']
type RoundingRule = components['schemas']['RoundingRule']
type NormRef = components['schemas']['NormRef']

const NO_ROUNDING: OutputRounding = new Map()

const SECTION_TITLES: Record<LoadsTraceSection, TextKey> = {
  resistance: 'trace.section.resistance',
  geometry: 'trace.section.geometry',
  mean: 'trace.section.mean',
  x: 'trace.section.x',
  y: 'trace.section.y',
  corners: 'trace.section.corners',
  contact: 'trace.section.contact',
  checks: 'trace.section.checks',
  other: 'trace.section.other',
}

function Value({ quantity, rounding }: { quantity: Quantity; rounding?: RoundingRule | null }) {
  return <QuantityText value={quantity.value} unit={quantity.unit} rounding={rounding} />
}

const SYMBOLS = { le: '≤', lt: '<', ge: '≥', gt: '>' } as const

type CheckStep = Extract<Step, { kind: 'check' }>

function Comparison({ step, rounding }: { step: CheckStep; rounding: OutputRounding }) {
  const { t } = useI18n()
  const Icon = step.passed ? CheckCircle : XCircle
  const fallback = useResultRounding()
  const [left, right] = checkRounding(step, rounding, fallback)
  return (
    <div className="grid gap-1">
      <p>
        <Value quantity={step.result} rounding={left ?? null} />{' '}
        <span aria-hidden="true">{SYMBOLS[step.operator]}</span>{' '}
        <span className="sr-only">{t(`trace.op.${step.operator}`)}</span> <Value quantity={step.right} rounding={right ?? null} />
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

function resultRounding(step: Step, rounding: OutputRounding, fallback?: RoundingRule): RoundingRule | null | undefined {
  return step.kind === 'check' ? checkRounding(step, rounding, fallback)[0] ?? null : rounding.get(step.step_id)
}

function StepSummary({ step, rounding }: { step: Step; rounding: OutputRounding }) {
  const { t } = useI18n()
  const fallback = useResultRounding()
  return (
    <span className="ml-auto" data-summary>
      <span className="font-mono">
        <Value quantity={step.result} rounding={resultRounding(step, rounding, fallback)} />
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
  symbols,
  rounding,
  normStatus,
  compact,
  sectionTitle,
  anchorPrefix,
  hideEngineerSource,
  fallbackNormRefs,
}: {
  step: Step
  index: number
  expanded: boolean
  onToggle: () => void
  arrival: Arrival
  symbols: ReadonlyMap<string, string>
  rounding: OutputRounding
  normStatus: boolean
  compact: boolean
  sectionTitle?: string
  anchorPrefix: string
  hideEngineerSource: boolean
  fallbackNormRefs: readonly NormRef[]
}) {
  const { t } = useI18n()
  const detailsId = useId()
  const StepHeading = compact ? 'h4' : 'h3'
  return (
    <li
      id={`${anchorPrefix}-step-${index}`}
      tabIndex={-1}
      className={`data-row scroll-mt-4 not-last:border-b not-last:border-border${ARRIVAL_CLASS[arrival]}`}
      data-step={step.step_id}
      data-arrival={arrival}
      inert={arrival === 'pending'}
    >
      {sectionTitle && (
        <h3 className="border-b border-border bg-secondary px-3 py-2 text-sm font-semibold" data-trace-section>
          {sectionTitle}
        </h3>
      )}
      <StepHeading className="text-base" data-step-heading>
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
          <span className="font-semibold" data-step-label>
            <NamedSymbol
              name={step.step_id}
              latex={step.kind === 'check' ? step.expression : symbols.get(step.step_id)}
              presentation={step.kind === 'check' ? checkPresentation(step, symbols) : undefined}
            />
          </span>
          <span className="text-sm text-muted-foreground">{t(`trace.kind.${step.kind}`)}</span>
          <StepSummary step={step} rounding={rounding} />
        </button>
      </StepHeading>
      <div id={detailsId} hidden={!expanded} className="step-details grid gap-3 border-t border-dashed border-border bg-background/40 px-3 py-3 pl-10">
        <div
          role="region"
          aria-label={`${t('trace.formula')}: ${step.step_id}`}
          // eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex -- Keyboard users must be able to scroll wide formulas.
          tabIndex={0}
          className="overflow-x-auto focus-visible:outline-offset-[-2px]"
        >
          <Formula latex={step.expression} presentation={step.kind === 'check' ? checkPresentation(step, symbols) : undefined} display />
        </div>
        {step.substitutions.length > 0 && (
          <div>
            <h4 className="text-sm font-medium">{t('trace.substitutions')}</h4>
            <ul className="flex flex-wrap gap-x-5 gap-y-1">
              {step.substitutions.map((substitution) => (
                <li key={substitution.symbol} className="flex flex-wrap items-baseline gap-1">
                  <NamedSymbol name={substitution.symbol} latex={symbols.get(substitution.symbol)} /> <span>=</span>{' '}
                  <Value quantity={substitution} rounding={rounding.get(substitution.symbol)} />
                </li>
              ))}
            </ul>
          </div>
        )}
        {step.kind === 'check' ? (
          <Comparison step={step} rounding={rounding} />
        ) : (
          <p>
            <span className="text-sm font-medium">{t('trace.result')}: </span>
            <Value quantity={step.result} rounding={rounding.get(step.step_id)} />
          </p>
        )}
        {step.kind === 'engineer_formula' ? (
          <>
            <div>
              <h4 className="text-sm font-medium">{t('trace.engineerSource')}</h4>
              <Source source={step.source} omitEngineerName={hideEngineerSource} />
            </div>
            {hideEngineerSource && (
              <div>
                <h4 className="text-sm font-medium">{t('trace.resultNorms')}</h4>
                <NormRefList refs={fallbackNormRefs} showStatus={normStatus} />
              </div>
            )}
          </>
        ) : step.norm_refs.length > 0 && (
          <div>
            <h4 className="text-sm font-medium">{t('trace.norms')}</h4>
            <NormRefList refs={step.norm_refs} showStatus={normStatus} />
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
  symbols,
  rounding = NO_ROUNDING,
  normStatus = true,
  title,
  description,
  anchorPrefix = 'trace',
  hideEngineerSource = false,
  fallbackNormRefs = [],
}: {
  steps: readonly Step[]
  unverifiedStepCount: number
  playback?: TracePlayback
  symbols?: ReadonlyMap<string, string>
  rounding?: OutputRounding
  normStatus?: boolean
  title?: string
  description?: string
  anchorPrefix?: string
  hideEngineerSource?: boolean
  fallbackNormRefs?: readonly NormRef[]
}) {
  const { t, formatNumber } = useI18n()
  const table = useMemo(() => symbols ?? symbolTable(steps), [symbols, steps])
  const sections = useMemo(() => loadsTraceSections(steps), [steps])
  const playing = playback?.phase === 'playing'
  const [expanded, setExpanded] = useState<ReadonlySet<number>>(() => new Set(steps.map((_, index) => index)))
  const toggle = (index: number) =>
    setExpanded((current) => {
      const next = new Set(current)
      if (!next.delete(index)) next.add(index)
      return next
    })
  return (
    <section aria-labelledby={`${anchorPrefix}-title`} className="mt-8 grid gap-4" data-playback={playback?.phase ?? 'idle'}>
      <h2 id={`${anchorPrefix}-title`} tabIndex={-1} className="scroll-mt-4">
        {title ?? t('trace.title')}
      </h2>
      {description && <p className="max-w-prose text-sm">{description}</p>}
      {normStatus && unverifiedStepCount > 0 && (
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
      <ol className="min-w-0 border border-border bg-card" data-trace-layout={sections ? 'compact' : 'expanded'}>
        {steps.map((step, index) => (
          <TraceStep
            key={`${step.step_id}-${index}`}
            step={step}
            index={index}
            anchorPrefix={anchorPrefix}
            hideEngineerSource={hideEngineerSource}
            fallbackNormRefs={fallbackNormRefs}
            expanded={expanded.has(index)}
            onToggle={() => toggle(index)}
            arrival={arrivalOf(index, playback)}
            symbols={table}
            rounding={rounding}
            normStatus={normStatus}
            compact={sections !== null}
            sectionTitle={sections && (index === 0 || sections[index] !== sections[index - 1]) ? t(SECTION_TITLES[sections[index]]) : undefined}
          />
        ))}
      </ol>
    </section>
  )
}

import { ArrowDown, ArrowRight, CheckCircle, XCircle } from '@phosphor-icons/react'
import { useId, useState, type ReactNode } from 'react'
import { Link } from 'react-router'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import type { TextKey } from '@/i18n/dictionary'
import { jumpTo } from '@/lib/jumpTo'
import { checkRounding, outputRounding } from '@/lib/rounding'
import { useResultRounding } from '@/lib/resultDisplay'
import { checkPresentation } from '@/lib/checkPresentation'
import { useFocusOnMount } from '@/lib/useFocusOnMount'
import { Checking } from './Checking'
import type { SentForm } from '@/form/draftContext'
import { EditInputsLink } from './EditInputsLink'
import { Formula } from './Formula'
import { QuantityText } from './Quantity'
import { SourceLabel } from './SourceLabel'
import { buttonClass } from './ui/button'

type Envelope = components['schemas']['ResultEnvelope']
type Step = Envelope['trace'][number]
type CheckStep = Extract<Step, { kind: 'check' }>
type Quantity = components['schemas']['QuantityValue']
type CheckReason = components['schemas']['CheckReason']
type RoundingRule = components['schemas']['RoundingRule']

const SYMBOLS = { le: '≤', lt: '<', ge: '≥', gt: '>' } as const

const REVEAL_CLASS: Record<StampReveal, string> = {
  pending: ' stamp-pending',
  celebrate: ' stamp-celebrate',
  plain: '',
  none: '',
}

function Reading({ quantity, rounding }: { quantity: Quantity; rounding: RoundingRule | undefined }) {
  return (
    <span className="whitespace-nowrap max-sm:whitespace-normal">
      <QuantityText value={quantity.value} unit={quantity.unit} unitClassName="text-muted-foreground" rounding={rounding ?? null} />
    </span>
  )
}

export type StampReveal = 'pending' | 'celebrate' | 'plain' | 'none'

function StampMark() {
  return (
    <svg aria-hidden="true" viewBox="0 0 64 64" className="stamp-mark" fill="none" strokeLinecap="square">
      <path className="sm-frame" pathLength={1} d="M4 4H60V60H4Z" strokeWidth={3} />
      <path className="sm-tick" pathLength={1} d="M16 33L28 45L49 20" strokeWidth={6} />
    </svg>
  )
}

export function VerdictStamp({
  envelope,
  reason,
  editType = null,
  editExample,
  reveal = 'none',
  symbols,
}: {
  envelope: Envelope
  reason: CheckReason
  editType?: string | null
  editExample?: SentForm['example']
  reveal?: StampReveal
  symbols?: ReadonlyMap<string, string>
}) {
  const { t, formatNumber } = useI18n()
  const headingId = useId()
  const focus = useFocusOnMount<HTMLElement>()
  const [entersShown] = useState(reveal === 'none')
  const passed = envelope.verdict === 'pass'
  const check = envelope.trace.find(
    (step): step is CheckStep => step.kind === 'check' && step.step_id === reason.step_id,
  )
  const rounding = new Map(outputRounding(envelope.outputs))
  const resistanceRounding = rounding.get('R')
  if (resistanceRounding) {
    rounding.set('edge_limit', resistanceRounding)
    rounding.set('corner_limit', resistanceRounding)
  }
  const fallback = useResultRounding()
  const [left, right] = check ? checkRounding(check, rounding, fallback) : []
  const Icon = passed ? CheckCircle : XCircle
  const tone = passed ? 'border-primary' : 'border-destructive'
  return (
    <section
      ref={focus}
      tabIndex={-1}
      aria-labelledby={headingId}
      aria-live={passed ? 'polite' : 'assertive'}
      aria-atomic="true"
      data-verdict={envelope.verdict}
      data-reveal={reveal}
      className={`stamp-frame relative grid border-2 bg-card sm:grid-cols-[1fr_auto] ${tone}${entersShown ? ' stamp-enter' : ''}${REVEAL_CLASS[reveal]}`}
    >
      {reveal === 'pending' && <Checking marker="stamp" />}
      <div className="relative grid min-w-0 gap-2 p-4">
        {reveal === 'celebrate' && <StampMark />}
        <h2 id={headingId} className={`flex items-center gap-2 text-verdict font-bold ${passed ? 'text-primary' : 'text-destructive'}`}>
          <Icon aria-hidden="true" weight="fill" size={26} className="shrink-0" />
          {t(passed ? 'verdict.pass' : 'verdict.fail')}
        </h2>
        {check && (
          <div className="flex flex-wrap items-baseline gap-x-5 gap-y-1" data-check={check.step_id}>
            <span className="text-xl">
              <Formula latex={check.expression} presentation={checkPresentation(check, symbols)} />
            </span>
            <p className="min-w-0 font-mono text-verdict">
              <Reading quantity={check.result} rounding={left} /> <span aria-hidden="true">{SYMBOLS[check.operator]}</span>
              <span className="sr-only">{t(`trace.op.${check.operator}`)}</span> <Reading quantity={check.right} rounding={right} />
            </p>
          </div>
        )}
      </div>
      <div className={`grid min-w-0 content-center gap-2 border-t-2 p-4 sm:border-t-0 sm:border-l-2 ${tone}`}>
        <Link to={`/calculations/${envelope.result_id}/report`} className={buttonClass}>
          {t('result.toReport')}
          <ArrowRight aria-hidden="true" size={18} />
        </Link>
        {editType && <EditInputsLink type={editType} example={editExample} primary={false} />}
      </div>
      <dl className={`col-span-full grid min-w-0 border-t text-sm sm:grid-cols-3 ${tone}`}>
        {(
          [
            [
              'stamp.steps',
              <a
                href="#trace-title"
                onClick={(event) => jumpTo(event, 'trace-title')}
                className="whitespace-nowrap"
                data-to-trace
              >
                {formatNumber(envelope.trace.length)} <span className="font-sans">— {t('stamp.toTrace')}</span>
                <ArrowDown aria-hidden="true" size={14} className="ml-1 inline align-[-2px]" />
              </a>,
            ],
            ['stamp.warnings', formatNumber(envelope.warnings.length)],
            ['stamp.engine', envelope.engine_version],
          ] satisfies [TextKey, ReactNode][]
        ).map(([key, value]) => (
          <div
            key={key}
            className="flex items-baseline justify-between gap-3 border-border px-4 py-2 not-last:border-b sm:grid sm:justify-start sm:gap-0.5 sm:not-last:border-r sm:not-last:border-b-0"
          >
            <dt className="text-muted-foreground">{t(key)}</dt>
            <dd className="font-mono">{value}</dd>
          </div>
        ))}
        {envelope.parameter_source && (
          <div className="grid gap-0.5 border-t border-border px-4 py-2 sm:col-span-full">
            <dt className="text-muted-foreground">{t('source.label')}</dt>
            <dd>
              <SourceLabel source={envelope.parameter_source} />
            </dd>
          </div>
        )}
      </dl>
    </section>
  )
}

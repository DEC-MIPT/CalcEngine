import { useMemo, type CSSProperties, type MouseEvent } from 'react'
import { flushSync } from 'react-dom'
import type { components } from '@/api/schema'
import { jumpTo } from '@/lib/jumpTo'
import { symbolTable } from '@/lib/stepSymbol'
import { checkPresentation } from '@/lib/checkPresentation'
import { arrivalOf, type TracePlayback } from '@/lib/useTracePlayback'
import { NamedSymbol } from './NamedSymbol'
import type { StampReveal } from './VerdictStamp'

type Envelope = components['schemas']['ResultEnvelope']
type Step = Envelope['trace'][number]

function VerdictMark({ verdict }: { verdict: Envelope['verdict'] }) {
  const passed = verdict === 'pass'
  return (
    <svg viewBox="0 0 20 20" className={`tr-mark ${passed ? 'text-primary' : 'text-destructive'}`} fill="none" stroke="currentColor">
      <path
        pathLength={1}
        strokeWidth={3}
        strokeLinecap="square"
        d={passed ? 'M3 10.5L8 15.5L17 4.5' : verdict === 'refused' ? 'M4 10H16' : 'M4 4L16 16M16 4L4 16'}
        data-mark={verdict}
      />
    </svg>
  )
}

export function TraceRuler({
  steps = [],
  verdict,
  playback,
  reveal = 'none',
  symbols,
  scrollLabel,
}: {
  steps?: readonly Step[]
  verdict?: Envelope['verdict']
  playback?: TracePlayback
  reveal?: StampReveal
  symbols?: ReadonlyMap<string, string>
  scrollLabel?: string
}) {
  const table = useMemo(() => symbols ?? symbolTable(steps), [symbols, steps])
  const playing = playback?.phase === 'playing'
  const dense = scrollLabel !== undefined && steps.length > 16
  const follow = (event: MouseEvent<HTMLAnchorElement>, index: number) => {
    if (playing) flushSync(playback.skip)
    jumpTo(event, `trace-step-${index}`)
  }
  const ruler = (
    <div
      aria-hidden={!dense || undefined}
      className={`trace-ruler${reveal === 'celebrate' ? ' tr-celebrate' : ''}`}
      style={{ '--steps': Math.max(steps.length, 1) } as CSSProperties}
      data-ruler={steps.length}
      data-dense={dense || undefined}
    >
      {steps.map((step, index) => {
        const arrival = arrivalOf(index, playback)
        return (
          <a
            key={`${step.step_id}-${index}`}
            href={`#trace-step-${index}`}
            tabIndex={dense ? undefined : -1}
            onClick={(event) => follow(event, index)}
            className={`tr-step tr-${arrival}`}
            data-tick={index}
            title={dense ? `${index + 1}. ${step.step_id}` : undefined}
            aria-label={dense ? `${index + 1}. ${step.step_id}` : undefined}
            data-arrival={arrival}
          >
            <span className="tr-bar" />
            <span className="tr-label">
              {dense ? <span className="tr-index">{index + 1}</span> : (
                <NamedSymbol
                  name={step.step_id}
                  latex={step.kind === 'check' ? step.expression : table.get(step.step_id)}
                  presentation={step.kind === 'check' ? checkPresentation(step, table) : undefined}
                />
              )}
            </span>
          </a>
        )
      })}
      {playing && (
        <span className="tr-cursor" style={{ '--at': playback.shown } as CSSProperties} data-ruler-cursor />
      )}
      {verdict && reveal !== 'pending' && (
        <span aria-hidden="true" className="tr-end" data-ruler-verdict={verdict}>
          <VerdictMark verdict={verdict} />
        </span>
      )}
    </div>
  )
  return dense ? (
    <nav aria-label={scrollLabel} className="trace-ruler-scroll">{ruler}</nav>
  ) : ruler
}

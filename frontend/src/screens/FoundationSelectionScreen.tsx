import { useCallback, useState } from 'react'
import { Link, useParams } from 'react-router'
import { api, unwrap } from '@/api/client'
import type { components } from '@/api/schema'
import { useRequest } from '@/api/useRequest'
import { QuantityText } from '@/components/Quantity'
import { ErrorState, LoadingState, NotFoundState } from '@/components/RequestStates'
import { DerivedRefusal, Refusal } from '@/components/Refusal'
import { StoredChecks } from '@/components/StoredChecks'
import { Trace } from '@/components/Trace'
import { useI18n } from '@/i18n/context'
import { useFocusOnMount } from '@/lib/useFocusOnMount'

type Outcome = components['schemas']['CandidateOutcome']

function CandidateOutcome({ outcome, selected }: { outcome: Outcome; selected: boolean }) {
  const { t } = useI18n()
  const [visited, setVisited] = useState(false)
  const { envelope, reason, candidate } = outcome
  const diagnosis = envelope?.verdict_reason
  return (
    <li className="grid min-w-0 gap-2 border border-border bg-card p-3" data-candidate={outcome.index}>
      <h2 className="text-lg">
        {t('foundation.candidate')} {outcome.index + 1}{selected ? ` — ${t('foundation.selected')}` : ''}
      </h2>
      <p className="font-mono">b: <QuantityText {...candidate.b} /> · l: <QuantityText {...candidate.l} /></p>
      <p>{envelope ? t(`foundation.${envelope.verdict}`) : t(outcome.status === 'error' ? 'foundation.error' : 'foundation.skipped')}</p>
      {reason && <p>{t(reason === 'cancelled' ? 'foundation.stopCancelled' : `foundation.${reason}`)}</p>}
      {envelope && diagnosis && (
        <details className="min-w-0" onToggle={(event) => { if (event.currentTarget.open) setVisited(true) }}>
          <summary className="cursor-pointer">{t('foundation.evidence')}</summary>
          {visited && diagnosis.kind === 'check' && <StoredChecks steps={envelope.trace} reason={diagnosis} />}
          {visited && diagnosis.kind === 'bound' && <Refusal reason={diagnosis} source={envelope.parameter_source} />}
          {visited && diagnosis.kind === 'derived' && <DerivedRefusal reason={diagnosis} source={envelope.parameter_source} />}
          {visited && envelope.trace.length > 0 && <Trace anchorPrefix={`candidate-trace-${outcome.index}`} steps={envelope.trace} unverifiedStepCount={envelope.unverified_step_count} />}
        </details>
      )}
    </li>
  )
}

export function FoundationSelectionScreen() {
  const { id } = useParams() as { id: string }
  const { t } = useI18n()
  const heading = useFocusOnMount<HTMLHeadingElement>()
  const load = useCallback(() => unwrap(api.GET('/foundation-selections/{selection_id}', {
    params: { path: { selection_id: id } },
  })), [id])
  const { state, retry } = useRequest(load)
  if (state.status === 'error' && state.error.kind === 'api' && state.error.status === 404) return <NotFoundState />
  return (
    <section className="grid min-w-0 gap-5">
      <h1 ref={heading} tabIndex={-1}>{t('foundation.compare')}</h1>
      {state.status === 'loading' && <LoadingState />}
      {state.status === 'error' && <ErrorState error={state.error} onRetry={retry} />}
      {state.status === 'ok' && <>
        <p className="text-lg font-semibold">{t(`foundation.${state.data.status}`)}</p>
        {state.data.stop_reason && <p>{t(state.data.stop_reason === 'cancelled' ? 'foundation.stopCancelled' : `foundation.${state.data.stop_reason}`)}</p>}
        <p>{t('foundation.policy')} <code>{state.data.request.policy_version}</code></p>
        <div className="flex flex-wrap gap-4">
          {state.data.status === 'selected' && state.data.selected_result_id && (
            <Link to={`/calculations/${encodeURIComponent(state.data.selected_result_id)}`}>{t('foundation.openSelected')}</Link>
          )}
          <Link to={`/foundation-selections/${encodeURIComponent(id)}/report`}>{t('result.toReport')}</Link>
        </div>
        <details>
          <summary className="cursor-pointer">{t('foundation.original')}</summary>
          <dl className="grid grid-cols-[minmax(0,1fr)_minmax(0,1fr)] gap-2 border border-border p-3">
            {Object.entries(state.data.request.common_inputs).map(([name, value]) => (
              <div className="contents" key={name}><dt className="break-words font-mono">{name}</dt><dd><QuantityText {...value} /></dd></div>
            ))}
          </dl>
        </details>
        <ol className="grid min-w-0 gap-3">
          {state.data.outcomes.map((outcome) => (
            <CandidateOutcome key={outcome.index} outcome={outcome} selected={state.data.selected_candidate_index === outcome.index} />
          ))}
        </ol>
      </>}
    </section>
  )
}

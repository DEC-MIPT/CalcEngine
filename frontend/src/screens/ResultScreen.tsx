import { ArrowRight } from '@phosphor-icons/react'
import { useCallback } from 'react'
import { Link, useParams } from 'react-router'
import { api, unwrap } from '@/api/client'
import { useRequest } from '@/api/useRequest'
import { Outputs } from '@/components/Outputs'
import { Refusal } from '@/components/Refusal'
import { ErrorState, LoadingState, NotFoundState } from '@/components/RequestStates'
import { Trace } from '@/components/Trace'
import { buttonClass } from '@/components/ui/button'
import { VerdictStamp } from '@/components/VerdictStamp'
import { Warnings } from '@/components/Warnings'
import { useI18n } from '@/i18n/context'

export function ResultScreen() {
  const { t } = useI18n()
  const { id } = useParams() as { id: string }
  const load = useCallback(
    () => unwrap(api.GET('/calculations/{result_id}', { params: { path: { result_id: id } } })),
    [id],
  )
  const { state, retry } = useRequest(load)

  if (state.status === 'error' && state.error.kind === 'api' && state.error.status === 404) {
    return <NotFoundState subject="result" />
  }
  return (
    <>
      <h1>{t('result.title')}</h1>
      {state.status === 'loading' && <LoadingState />}
      {state.status === 'error' && <ErrorState error={state.error} onRetry={retry} />}
      {state.status === 'ok' && (
        <>
          {state.data.verdict_reason.kind === 'bound' ? (
            <>
              <Refusal reason={state.data.verdict_reason} />
              <p className="mt-4">
                <Link to={`/calculations/${state.data.result_id}/report`} className={buttonClass}>
                  {t('result.toReport')}
                  <ArrowRight aria-hidden="true" size={18} />
                </Link>
              </p>
            </>
          ) : (
            <>
              <VerdictStamp envelope={state.data} reason={state.data.verdict_reason} />
              <Outputs outputs={state.data.outputs} />
              <Warnings warnings={state.data.warnings} />
              <Trace steps={state.data.trace} unverifiedStepCount={state.data.unverified_step_count} />
            </>
          )}
        </>
      )}
    </>
  )
}

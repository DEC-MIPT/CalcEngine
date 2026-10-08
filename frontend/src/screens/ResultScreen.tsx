import { ArrowRight } from '@phosphor-icons/react'
import { useCallback } from 'react'
import { Link, useParams } from 'react-router'
import { api, unwrap } from '@/api/client'
import { useRequest } from '@/api/useRequest'
import { Outputs } from '@/components/Outputs'
import { Refusal } from '@/components/Refusal'
import { ErrorState, LoadingState, NotFoundState } from '@/components/RequestStates'
import { Trace } from '@/components/Trace'
import { EditInputsLink } from '@/components/EditInputsLink'
import { buttonClass, secondaryButtonClass } from '@/components/ui/button'
import { VerdictStamp } from '@/components/VerdictStamp'
import { Warnings } from '@/components/Warnings'
import { useDraft } from '@/form/draftContext'
import { useI18n } from '@/i18n/context'
import { cn } from '@/lib/utils'

export function ResultScreen() {
  const { t } = useI18n()
  const { id } = useParams() as { id: string }
  const load = useCallback(
    () => unwrap(api.GET('/calculations/{result_id}', { params: { path: { result_id: id } } })),
    [id],
  )
  const { state, retry } = useRequest(load)
  const { sent } = useDraft()

  if (state.status === 'error' && state.error.kind === 'api' && state.error.status === 404) {
    return <NotFoundState subject="result" />
  }
  const editType = state.status === 'ok' && sent?.resultId === state.data.result_id ? sent.type : null
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
              <p className="mt-4 flex flex-wrap gap-3">
                {editType && <EditInputsLink type={editType} bound={state.data.verdict_reason.bound} primary />}
                <Link
                  to={`/calculations/${state.data.result_id}/report`}
                  className={cn(buttonClass, editType && secondaryButtonClass)}
                >
                  {t('result.toReport')}
                  <ArrowRight aria-hidden="true" size={18} />
                </Link>
              </p>
            </>
          ) : (
            <>
              <VerdictStamp envelope={state.data} reason={state.data.verdict_reason} editType={editType} />
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

import { useSearchParams } from 'react-router'
import { api, unwrap } from '@/api/client'
import { useRequest } from '@/api/useRequest'
import { CalculationForm } from '@/components/CalculationForm'
import { ErrorState, LoadingState, NotFoundState } from '@/components/RequestStates'
import { useI18n } from '@/i18n/context'

const loadTypes = () => unwrap(api.GET('/calculation-types'))

export function CalculationFormScreen() {
  const { t } = useI18n()
  const [params] = useSearchParams()
  const name = params.get('type')
  const { state, retry } = useRequest(loadTypes)

  const type = state.status === 'ok' ? state.data.find((candidate) => candidate.name === name) : undefined
  if (state.status === 'ok' && !type) return <NotFoundState subject="type" />
  return (
    <>
      <h1>{t('form.title')}</h1>
      {state.status === 'loading' && <LoadingState />}
      {state.status === 'error' && <ErrorState error={state.error} onRetry={retry} />}
      {type && (
        <>
          <p className="mb-6">
            <code>{type.name}</code>
          </p>
          <CalculationForm key={type.name} type={type} />
        </>
      )}
    </>
  )
}

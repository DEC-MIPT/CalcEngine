import { Link, useSearchParams } from 'react-router'
import { api, unwrap } from '@/api/client'
import { useRequest } from '@/api/useRequest'
import { CalculationForm } from '@/components/CalculationForm'
import { ErrorState, LoadingState, NotFoundState } from '@/components/RequestStates'
import { useI18n } from '@/i18n/context'
import { LOADS_TYPE, WEIGHTS_TYPE } from '@/lib/foundationDesign'
import { typeName } from '@/lib/typeName'

const loadTypes = () => unwrap(api.GET('/calculation-types'))

export function CalculationFormScreen() {
  const { t, language } = useI18n()
  const [params] = useSearchParams()
  const name = params.get('type')
  const { state, retry } = useRequest(loadTypes)

  const type = state.status === 'ok' ? state.data.find((candidate) => candidate.name === name) : undefined
  const searching = name === LOADS_TYPE && params.get('task') === 'selection'
  const otherType = name === WEIGHTS_TYPE ? LOADS_TYPE : WEIGHTS_TYPE
  const switchable = state.status === 'ok' && (name === LOADS_TYPE || name === WEIGHTS_TYPE) && state.data.some((entry) => entry.name === otherType)
  if (state.status === 'ok' && !type) return <NotFoundState subject="type" />
  return (
    <>
      <h1>{t('form.title')}</h1>
      {state.status === 'loading' && <LoadingState />}
      {state.status === 'error' && <ErrorState error={state.error} onRetry={retry} />}
      {type && (
        <>
          <p className="mb-5 font-heading text-xl font-semibold">{typeName(type, language)}</p>
          {(switchable || name === LOADS_TYPE) && (
            <nav aria-label={t('foundation.candidates')} className="mb-5 flex flex-wrap gap-x-5 gap-y-2">
              {switchable && <Link to={`/calculations/new?type=${otherType}`}>{t(otherType === LOADS_TYPE ? 'foundation.averaged' : 'foundation.explicit')}</Link>}
              {name === LOADS_TYPE && (searching
                ? <Link to={`/calculations/new?type=${LOADS_TYPE}`}>{t('foundation.check')}</Link>
                : <Link to={`/calculations/new?type=${LOADS_TYPE}&task=selection`}>{t('foundation.search')}</Link>)}
            </nav>
          )}
          {name === WEIGHTS_TYPE && <p className="mb-5 text-sm">{t('foundation.searchAveraged')}</p>}
          <CalculationForm key={`${type.name}:${String(searching)}`} type={type} searching={searching} />
        </>
      )}
    </>
  )
}

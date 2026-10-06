import { ArrowRight } from '@phosphor-icons/react'
import { Link } from 'react-router'
import { api, unwrap } from '@/api/client'
import { useRequest } from '@/api/useRequest'
import { ErrorState, LoadingState } from '@/components/RequestStates'
import { useI18n } from '@/i18n/context'

const loadTypes = () => unwrap(api.GET('/calculation-types'))

export function TypeSelectionScreen() {
  const { t } = useI18n()
  const { state, retry } = useRequest(loadTypes)
  return (
    <>
      <h1>{t('types.title')}</h1>
      {state.status === 'loading' && <LoadingState />}
      {state.status === 'error' && <ErrorState error={state.error} onRetry={retry} />}
      {state.status === 'ok' &&
        (state.data.length === 0 ? (
          <p>{t('types.empty')}</p>
        ) : (
          <ul className="max-w-2xl border border-border bg-card">
            {state.data.map((type) => (
              <li key={type.name} className="not-last:border-b not-last:border-border">
                <Link
                  to={`/calculations/new?type=${encodeURIComponent(type.name)}`}
                  className="flex items-center justify-between gap-4 px-4 py-3 no-underline hover:bg-secondary"
                >
                  <code>{type.name}</code>
                  <ArrowRight aria-hidden="true" size={18} />
                </Link>
              </li>
            ))}
          </ul>
        ))}
    </>
  )
}

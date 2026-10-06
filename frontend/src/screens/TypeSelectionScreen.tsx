import { ArrowRight } from '@phosphor-icons/react'
import type { ReactNode } from 'react'
import { Link } from 'react-router'
import { api, unwrap } from '@/api/client'
import type { components } from '@/api/schema'
import { useRequest } from '@/api/useRequest'
import { Formula } from '@/components/Formula'
import { ErrorState, LoadingState } from '@/components/RequestStates'
import { Button } from '@/components/ui/button'
import { useI18n } from '@/i18n/context'
import { pickText } from '@/i18n/translate'
import { unitLabel } from '@/i18n/units'

type CalculationType = components['schemas']['CalculationTypeView']

const loadTypes = () => unwrap(api.GET('/calculation-types'))

const headCell = 'px-3 py-2 text-left font-heading text-sm font-semibold text-muted-foreground'

function Registry({ children }: { children: ReactNode }) {
  const { t } = useI18n()
  return (
    <table className="w-full border-collapse border border-border bg-card">
      <thead className="border-b border-foreground">
        <tr>
          <th scope="col" className={headCell}>
            {t('types.column.result')}
          </th>
          <th scope="col" className={`${headCell} w-24 text-right`}>
            {t('types.column.inputs')}
          </th>
          <th scope="col" className={`${headCell} hidden w-64 sm:table-cell`}>
            {t('types.column.id')}
          </th>
          <th scope="col" className="w-10">
            <span className="sr-only">{t('types.column.open')}</span>
          </th>
        </tr>
      </thead>
      <tbody>{children}</tbody>
    </table>
  )
}

function Notice({ children }: { children: ReactNode }) {
  return (
    <tr>
      <td colSpan={4} className="px-3 py-4">
        {children}
      </td>
    </tr>
  )
}

function TypeRow({ type }: { type: CalculationType }) {
  const { language } = useI18n()
  const name = type.outputs.map((output) => pickText(output.label, language)).join(' · ')
  return (
    <tr className="relative not-last:border-b not-last:border-border hover:bg-secondary has-[a:focus-visible]:bg-secondary">
      <td className="px-3 py-3">
        <Link
          to={`/calculations/new?type=${encodeURIComponent(type.name)}`}
          className="font-medium text-foreground no-underline after:absolute after:inset-0 focus-visible:outline-offset-[-2px]"
        >
          {name}
        </Link>
        <span aria-hidden="true" className="mt-0.5 flex flex-wrap gap-x-3 text-sm text-muted-foreground">
          {type.outputs.map((output) => (
            <span key={output.name} className="inline-flex items-baseline">
              <Formula latex={output.symbol} />, {unitLabel(output.base_unit, language)}
            </span>
          ))}
        </span>
      </td>
      <td className="px-3 py-3 text-right font-mono">{type.inputs.length}</td>
      <td className="hidden px-3 py-3 font-mono text-sm text-muted-foreground sm:table-cell">{type.name}</td>
      <td className="px-3 py-3 text-primary">
        <ArrowRight aria-hidden="true" size={18} />
      </td>
    </tr>
  )
}

export function TypeSelectionScreen() {
  const { t } = useI18n()
  const { state, retry } = useRequest(loadTypes)
  return (
    <>
      <h1>{t('types.title')}</h1>
      {state.status === 'error' ? (
        <ErrorState error={state.error} onRetry={retry} title="types.loadFailed" />
      ) : (
        <Registry>
          {state.status === 'loading' && (
            <Notice>
              <LoadingState />
            </Notice>
          )}
          {state.status === 'ok' && state.data.length === 0 && (
            <Notice>
              <div className="grid justify-items-start gap-3">
                <p>{t('types.empty')}</p>
                <Button onClick={retry}>{t('state.retry')}</Button>
              </div>
            </Notice>
          )}
          {state.status === 'ok' && state.data.map((type) => <TypeRow key={type.name} type={type} />)}
        </Registry>
      )}
    </>
  )
}

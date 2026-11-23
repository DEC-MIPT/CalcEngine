import { ArrowRight } from '@phosphor-icons/react'
import { Fragment, type ReactNode } from 'react'
import { Link } from 'react-router'
import { api, unwrap } from '@/api/client'
import type { components } from '@/api/schema'
import { useRequest } from '@/api/useRequest'
import { Formula } from '@/components/Formula'
import { DimensionGrid } from '@/components/DimensionGrid'
import { ErrorState, LoadingState } from '@/components/RequestStates'
import { Button } from '@/components/ui/button'
import { useI18n } from '@/i18n/context'
import { unitLabel } from '@/i18n/units'
import { calculationFormUrl, LOADS_TYPE, WEIGHTS_EXAMPLE, WEIGHTS_TYPE } from '@/lib/foundationDesign'
import { typeName } from '@/lib/typeName'

type CalculationType = components['schemas']['CalculationTypeView']

const loadTypes = () => unwrap(api.GET('/calculation-types'))

const headCell = 'px-3 py-2.5 sm:px-4 text-left font-heading text-sm font-semibold tracking-wide text-muted-foreground uppercase'

function Registry({ children }: { children: ReactNode }) {
  const { t } = useI18n()
  return (
    <table className="w-full border-collapse border-2 border-foreground bg-card">
      <thead className="border-b-2 border-foreground">
        <tr>
          <th scope="col" className={headCell}>
            {t('types.column.result')}
          </th>
          <th scope="col" className={`${headCell} hidden w-24 text-right sm:table-cell`}>
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

function TypeRow({ type, example }: { type: CalculationType; example?: typeof WEIGHTS_EXAMPLE }) {
  const { language, t } = useI18n()
  return (
    <tr className="registry-row group relative not-last:border-b not-last:border-border">
      <td className="px-3 py-4 sm:px-4 sm:py-5">
        <Link
          to={calculationFormUrl(type.name, example)}
          className="font-heading text-xl font-semibold text-foreground no-underline group-hover:text-primary-foreground group-has-[a:focus-visible]:text-primary-foreground after:absolute after:inset-0 focus-visible:outline-offset-[-4px] focus-visible:outline-primary-foreground sm:text-3xl"
        >
          {type.name === WEIGHTS_TYPE ? t(example ? 'types.foundationExample' : 'types.foundationDemo') : typeName(type, language)}
        </Link>
        <span
          aria-hidden="true"
          className="mt-1 flex flex-wrap gap-x-3 text-sm text-muted-foreground group-hover:text-primary-foreground group-has-[a:focus-visible]:text-primary-foreground"
        >
          {type.outputs.map((output) => {
            const unit = unitLabel(output.base_unit, language)
            return (
              <span key={output.name} className="inline-flex items-baseline">
                <Formula latex={output.symbol} />
                {unit && <>, {unit}</>}
              </span>
            )
          })}
        </span>
      </td>
      <td className="hidden px-3 py-4 text-right font-mono text-lg sm:table-cell sm:px-4 sm:py-5 group-hover:text-primary-foreground group-has-[a:focus-visible]:text-primary-foreground">
        {type.inputs.length}
      </td>
      <td className="hidden px-3 py-4 sm:px-4 sm:py-5 font-mono text-xs text-muted-foreground group-hover:text-primary-foreground group-has-[a:focus-visible]:text-primary-foreground sm:table-cell">
        {type.name}
      </td>
      <td className="px-3 py-4 sm:px-4 sm:py-5 text-primary group-hover:text-primary-foreground group-has-[a:focus-visible]:text-primary-foreground">
        <ArrowRight
          aria-hidden="true"
          size={24}
          weight="bold"
          className="transition-transform group-hover:translate-x-1.5 group-has-[a:focus-visible]:translate-x-1.5"
        />
      </td>
    </tr>
  )
}

function Hero() {
  const { t } = useI18n()
  return (
    <section className="hero on-accent bg-primary text-primary-foreground">
      <div className="mx-auto grid max-w-5xl items-end gap-x-10 gap-y-8 px-4 pt-10 pb-12 lg:grid-cols-[minmax(0,1fr)_minmax(0,24rem)] lg:pt-16 lg:pb-16">
        <div className="grid gap-5">
          <p className="font-mono text-xs tracking-[0.25em] uppercase opacity-85">{t('hero.kicker')}</p>
          <h1 className="hero-title">{t('types.title')}</h1>
          <p className="max-w-xl text-base/relaxed opacity-90 sm:text-lg/relaxed">{t('hero.lede')}</p>
        </div>
        <DimensionGrid />
      </div>
    </section>
  )
}

export function TypeSelectionScreen() {
  const { t } = useI18n()
  const { state, retry } = useRequest(loadTypes)
  const visibleTypes = state.status === 'ok' ? state.data.filter((type) => type.name !== LOADS_TYPE) : []
  return (
    <>
      <Hero />
      <div className="mx-auto max-w-5xl px-4 py-10">
        {state.status === 'error' ? (
          <ErrorState error={state.error} onRetry={retry} title="types.loadFailed" />
        ) : (
          <Registry>
            {state.status === 'loading' && (
              <Notice>
                <LoadingState />
              </Notice>
            )}
            {state.status === 'ok' && visibleTypes.length === 0 && (
              <Notice>
                <div className="grid justify-items-start gap-3">
                  <p>{t('types.empty')}</p>
                  <Button onClick={retry}>{t('state.retry')}</Button>
                </div>
              </Notice>
            )}
            {visibleTypes.map((type) => (
              <Fragment key={type.name}>
                <TypeRow type={type} />
                {type.name === WEIGHTS_TYPE && <TypeRow type={type} example={WEIGHTS_EXAMPLE} />}
              </Fragment>
            ))}
          </Registry>
        )}
      </div>
    </>
  )
}

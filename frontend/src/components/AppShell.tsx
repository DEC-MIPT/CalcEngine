import { CaretRight, Flask } from '@phosphor-icons/react'
import { Link, NavLink, Outlet, useMatches } from 'react-router'
import { DraftProvider } from '@/form/DraftProvider'
import { I18nProvider } from '@/i18n/I18nProvider'
import { useI18n } from '@/i18n/context'

export type Crumb = 'form' | 'result' | 'report' | 'notFound'

const SHORT_ID = 8

function useTrail(): { crumbs: readonly Crumb[]; id?: string } {
  const match = useMatches().at(-1)
  const handle = match?.handle as { trail?: readonly Crumb[] } | undefined
  return { crumbs: handle?.trail ?? [], id: match?.params.id }
}

function CrumbLabel({ crumb, id }: { crumb: Crumb; id?: string }) {
  const { t } = useI18n()
  if (crumb === 'result' && id) {
    return (
      <>
        {t('crumb.result')} <span className="font-mono">№ {id.slice(0, SHORT_ID)}</span>
      </>
    )
  }
  return <>{t(`crumb.${crumb}`)}</>
}

function Trail() {
  const { t } = useI18n()
  const { crumbs, id } = useTrail()
  return (
    <nav aria-label={t('nav.main')}>
      <ol className="flex flex-wrap items-center gap-x-2 gap-y-1 text-sm">
        <li>
          <NavLink
            to="/"
            end
            className="aria-[current=page]:cursor-default aria-[current=page]:text-foreground aria-[current=page]:no-underline"
          >
            {t('nav.types')}
          </NavLink>
        </li>
        {crumbs.map((crumb, index) => {
          const last = index === crumbs.length - 1
          return (
            <li key={crumb} className="flex items-center gap-x-2">
              <CaretRight aria-hidden="true" size={12} className="text-muted-foreground" />
              {last ? (
                <span aria-current="page">
                  <CrumbLabel crumb={crumb} id={id} />
                </span>
              ) : (
                <Link to={`/calculations/${id}`}>
                  <CrumbLabel crumb={crumb} id={id} />
                </Link>
              )}
            </li>
          )
        })}
      </ol>
    </nav>
  )
}

function DemoBadge() {
  const { t } = useI18n()
  if (import.meta.env.MODE !== 'mock') return null
  return (
    <p className="inline-flex items-center gap-1.5 border border-warning bg-warning-surface px-2 py-0.5 text-sm text-warning-foreground sm:ml-auto">
      <Flask aria-hidden="true" weight="fill" size={16} />
      {t('app.demo')}
    </p>
  )
}

function Shell() {
  const { t } = useI18n()
  const bleed = (useMatches().at(-1)?.handle as { bleed?: boolean } | undefined)?.bleed === true
  return (
    <>
      <header className="border-b border-border bg-card">
        <div className="mx-auto flex max-w-5xl flex-wrap items-center gap-x-4 gap-y-2 px-4 py-2.5">
          <p className="flex items-center gap-2 font-heading text-lg font-semibold">
            <span aria-hidden="true" className="bg-primary px-1.5 font-mono text-sm font-bold tracking-widest text-primary-foreground">
              DEC
            </span>
            {t('app.title')}
          </p>
          <span aria-hidden="true" className="h-5 w-px bg-border max-sm:hidden" />
          <Trail />
          <DemoBadge />
        </div>
      </header>
      <main className={bleed ? undefined : 'mx-auto max-w-5xl px-4 py-8'}>
        <Outlet />
      </main>
    </>
  )
}

export function AppShell() {
  return (
    <I18nProvider>
      <DraftProvider>
        <Shell />
      </DraftProvider>
    </I18nProvider>
  )
}

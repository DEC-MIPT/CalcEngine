import { NavLink, Outlet } from 'react-router'
import { I18nProvider } from '@/i18n/I18nProvider'
import { useI18n } from '@/i18n/context'

function Shell() {
  const { t } = useI18n()
  return (
    <>
      <header className="border-b border-border bg-card">
        <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-x-6 gap-y-3 px-4 py-3">
          <p className="font-heading text-lg font-semibold">{t('app.title')}</p>
          <nav aria-label={t('nav.main')} className="flex flex-wrap items-center gap-x-6 gap-y-3">
            <NavLink
              to="/"
              end
              className="aria-[current=page]:cursor-default aria-[current=page]:text-foreground aria-[current=page]:no-underline"
            >
              {t('nav.types')}
            </NavLink>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-4 py-8">
        <Outlet />
      </main>
    </>
  )
}

export function AppShell() {
  return (
    <I18nProvider>
      <Shell />
    </I18nProvider>
  )
}

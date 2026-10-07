import { CircleNotch, WarningCircle } from '@phosphor-icons/react'
import { Link, useLocation } from 'react-router'
import type { ApiError } from '@/api/client'
import { useI18n } from '@/i18n/context'
import type { TextKey } from '@/i18n/dictionary'
import { Button } from './ui/button'

export function LoadingState() {
  const { t } = useI18n()
  return (
    <p role="status" className="inline-flex items-center gap-2 text-muted-foreground">
      <CircleNotch aria-hidden="true" size={18} className="animate-spin" />
      {t('state.loading')}
    </p>
  )
}

type ErrorStateProps = {
  error: ApiError
  onRetry: () => void
  title?: TextKey
}

export function ErrorState({ error, onRetry, title }: ErrorStateProps) {
  const { t } = useI18n()
  const unavailable = error.kind === 'network' || error.status === 503
  return (
    <div
      role="alert"
      className="flex max-w-2xl gap-3 border border-destructive bg-destructive-surface p-4"
    >
      <WarningCircle aria-hidden="true" weight="fill" size={24} className="mt-0.5 shrink-0 text-destructive" />
      <div className="grid gap-2">
        <p className="font-medium">{t(title ?? (unavailable ? 'state.unavailable' : 'state.failed'))}</p>
        {error.kind === 'api' && (
          <>
            <p className="text-sm">
              {t('state.code')}: <code>{error.code}</code>
            </p>
            <p className="text-sm">
              {t('state.serverMessage')}: {error.message}
            </p>
          </>
        )}
        <div>
          <Button onClick={onRetry}>{t('state.retry')}</Button>
        </div>
      </div>
    </div>
  )
}

const notFoundKey = {
  page: 'notFound.page',
  result: 'notFound.result',
  type: 'notFound.type',
} as const

export function NotFoundState({ subject = 'page' }: { subject?: 'page' | 'result' | 'type' }) {
  const { t } = useI18n()
  const { pathname, search } = useLocation()
  return (
    <>
      <h1>{t(notFoundKey[subject])}</h1>
      <dl className="mb-5 grid max-w-2xl border border-border bg-card text-sm sm:grid-cols-[max-content_1fr]">
        <dt className="border-border px-3 py-2 text-muted-foreground max-sm:pb-0 sm:border-r">{t('notFound.code')}</dt>
        <dd className="px-3 py-2 font-mono">404</dd>
        <dt className="border-t border-border px-3 py-2 text-muted-foreground max-sm:pb-0 sm:border-r">
          {t('notFound.address')}
        </dt>
        <dd className="border-border px-3 py-2 font-mono break-all sm:border-t">
          {pathname}
          {search}
        </dd>
      </dl>
      <p>
        <Link to="/">{t('notFound.toTypes')}</Link>
      </p>
    </>
  )
}

import { WarningCircle } from '@phosphor-icons/react'
import { Link } from 'react-router'
import type { ApiError } from '@/api/client'
import { useI18n } from '@/i18n/context'
import { Button } from './ui/button'

export function LoadingState() {
  const { t } = useI18n()
  return (
    <p role="status" className="text-muted-foreground">
      {t('state.loading')}
    </p>
  )
}

export function ErrorState({ error, onRetry }: { error: ApiError; onRetry: () => void }) {
  const { t } = useI18n()
  const unavailable = error.kind === 'network' || error.status === 503
  return (
    <div
      role="alert"
      className="flex max-w-2xl gap-3 border border-destructive border-l-4 bg-destructive-surface p-4"
    >
      <WarningCircle aria-hidden="true" weight="fill" size={24} className="mt-0.5 shrink-0 text-destructive" />
      <div className="grid gap-2">
        <p className="font-medium">{t(unavailable ? 'state.unavailable' : 'state.failed')}</p>
        {error.kind === 'api' && (
          <>
            <p className="text-sm">
              {t('state.code')}: <code>{error.code}</code>
            </p>
            <p className="text-sm">{error.message}</p>
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
  return (
    <>
      <h1>{t(notFoundKey[subject])}</h1>
      <p>
        <Link to="/">{t('notFound.toTypes')}</Link>
      </p>
    </>
  )
}

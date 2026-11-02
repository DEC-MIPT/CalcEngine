import { Hourglass, WarningCircle } from '@phosphor-icons/react'
import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'

type ParameterSource = components['schemas']['ParameterSourceInfo']

const SHORT_DIGEST = 12

export function SourceLabel({ source }: { source: ParameterSource }) {
  const { t } = useI18n()
  if (source.kind === 'catalog') {
    return <span data-source="catalog">{t('source.catalog')}</span>
  }
  const draft = source.profile === 'draft'
  const digest = source.data_sha256 ?? ''
  const Icon = draft ? WarningCircle : Hourglass
  return (
    <span data-source="interim" data-profile={source.profile ?? undefined} className="grid gap-1">
      <span
        className={`inline-flex w-fit items-center gap-1.5 border-2 px-2 py-0.5 font-sans font-semibold ${
          draft ? 'border-dashed border-warning bg-warning-surface' : 'border-solid border-foreground'
        }`}
      >
        <Icon aria-hidden="true" weight="fill" size={16} className="shrink-0" />
        {t('source.interim')}
      </span>
      <span className="font-mono">
        {t('source.profile')} {source.profile}
        {digest && (
          <>
            {' · '}
            <span className="sr-only">{t('source.digest')} </span>
            <span aria-hidden="true" title={digest}>
              {digest.slice(0, SHORT_DIGEST)}…
            </span>
            <span className="sr-only">{digest}</span>
          </>
        )}
      </span>
      {draft && <span className="font-sans font-semibold">{t('source.draft')}</span>}
    </span>
  )
}

import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { BoundFacts } from './Bound'
import { Source } from './Source'
import { Status } from './Status'

type ApplicabilityWarning = components['schemas']['ApplicabilityWarning']

export function Warnings({ warnings }: { warnings: readonly ApplicabilityWarning[] }) {
  const { t } = useI18n()
  if (warnings.length === 0) return null
  return (
    <div className="mt-8 grid gap-3">
      {warnings.map((warning) => (
        <Status key={`${warning.bound.quantity}-${warning.bound.kind}`} tone="warning" title={t('warning.title')}>
          <BoundFacts value={warning.value} bound={warning.bound} boundLabel={t('bound.validated')} />
          <div>
            <h3 className="text-sm font-medium">{t('bound.source')}</h3>
            <Source source={warning.bound.source} />
          </div>
        </Status>
      ))}
    </div>
  )
}

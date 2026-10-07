import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { BoundFacts } from './Bound'
import { NormRefList } from './NormRefList'
import { Status } from './Status'

type BoundViolation = components['schemas']['BoundViolation']

export function Refusal({ reason }: { reason: BoundViolation }) {
  const { t } = useI18n()
  return (
    <Status tone="refusal" title={t('refusal.title')}>
      <BoundFacts value={reason.value} bound={reason.bound} boundLabel={t('bound.method')} />
      <div>
        <h3 className="text-sm font-medium">{t('bound.source')}</h3>
        <NormRefList refs={reason.bound.source} />
      </div>
      <p>{t('refusal.noResult')}</p>
    </Status>
  )
}

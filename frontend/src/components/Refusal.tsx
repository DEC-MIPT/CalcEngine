import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { BoundFacts } from './Bound'
import { NormRefList } from './NormRefList'
import { SourceLabel } from './SourceLabel'
import { Status } from './Status'

type BoundViolation = components['schemas']['BoundViolation']
type ParameterSource = components['schemas']['ParameterSourceInfo']

export function Refusal({ reason, source }: { reason: BoundViolation; source?: ParameterSource | null }) {
  const { t } = useI18n()
  return (
    <Status tone="refusal" title={t('refusal.title')} focusOnMount>
      <BoundFacts value={reason.value} bound={reason.bound} boundLabel={t('bound.method')} />
      <div>
        <h3 className="text-sm font-medium">{t('bound.source')}</h3>
        <NormRefList refs={reason.bound.source} />
      </div>
      {source && (
        <dl className="grid gap-0.5 text-sm">
          <dt className="text-muted-foreground">{t('source.label')}</dt>
          <dd>
            <SourceLabel source={source} />
          </dd>
        </dl>
      )}
      <p>{t('refusal.noResult')}</p>
    </Status>
  )
}

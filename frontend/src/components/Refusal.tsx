import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { BoundFacts } from './Bound'
import { NormRefList } from './NormRefList'
import { SourceLabel } from './SourceLabel'
import { Status } from './Status'
import { Source } from './Source'
import { QuantityText } from './Quantity'

type BoundViolation = components['schemas']['BoundViolation']
type ParameterSource = components['schemas']['ParameterSourceInfo']
type DerivedViolation = components['schemas']['DerivedViolation']

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

export function DerivedRefusal({
  reason,
  source,
  hideEngineerSource = false,
  fallbackNormRefs = [],
}: {
  reason: DerivedViolation
  source?: ParameterSource | null
  hideEngineerSource?: boolean
  fallbackNormRefs?: readonly components['schemas']['NormRef'][]
}) {
  const { t } = useI18n()
  return (
    <Status tone="refusal" title={t('refusal.contact.title')} focusOnMount>
      <p>{t('refusal.contact.scope')}</p>
      <dl className="grid grid-cols-[auto_1fr] items-baseline gap-x-4 gap-y-1 text-sm">
        <dt>{t('refusal.contact.quantity')}</dt>
        <dd><code>{reason.quantity}</code></dd>
        <dt>{t('refusal.contact.value')}</dt>
        <dd><QuantityText value={reason.value.value} unit={reason.value.unit} /></dd>
        <dt>{t('refusal.contact.limit')}</dt>
        <dd>
          <span aria-hidden="true">≥</span>
          <span className="sr-only">{t('trace.op.ge')}</span>{' '}
          <QuantityText value={reason.limit.value} unit={reason.limit.unit} />
        </dd>
        <dt>{t('refusal.contact.corner')}</dt>
        <dd><code>{reason.limiting_corner}</code></dd>
        <dt>{t('refusal.contact.inputs')}</dt>
        <dd>{reason.related_inputs.join(', ')}</dd>
      </dl>
      <div>
        <h3 className="text-sm font-medium">{t('bound.source')}</h3>
        {hideEngineerSource ? <NormRefList refs={fallbackNormRefs} /> : <Source source={reason.source} />}
      </div>
      {source && (
        <dl className="grid gap-0.5 text-sm">
          <dt className="text-muted-foreground">{t('source.label')}</dt>
          <dd><SourceLabel source={source} /></dd>
        </dl>
      )}
    </Status>
  )
}

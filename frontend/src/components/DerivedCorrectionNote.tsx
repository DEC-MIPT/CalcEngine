import type { components } from '@/api/schema'
import { useI18n } from '@/i18n/context'
import { QuantityText } from './Quantity'
import { Source } from './Source'

type Reason = components['schemas']['DerivedViolation']

export function DerivedCorrectionNote({ id, reason }: { id: string; reason: Reason }) {
  const { t } = useI18n()
  return (
    <div id={id} className="grid min-w-0 gap-2 border border-warning bg-warning-surface px-2 py-2 text-sm text-warning-foreground">
      <p className="font-semibold">{t('form.derivedCorrection')}</p>
      <p>{t('refusal.contact.scope')}</p>
      <p>
        <code>{reason.quantity}</code>: <QuantityText {...reason.value} />;{' '}
        {t('refusal.contact.limit')}: <span aria-hidden="true">≥</span>
        <span className="sr-only">{t('trace.op.ge')}</span>{' '}
        <QuantityText {...reason.limit} />
      </p>
      <p>{t('refusal.contact.corner')}: <code>{reason.limiting_corner}</code></p>
      <Source source={reason.source} />
    </div>
  )
}

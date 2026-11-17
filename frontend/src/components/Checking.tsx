import { useI18n } from '@/i18n/context'

export function Checking({ marker }: { marker: 'stamp' | 'outputs' | 'checks' }) {
  const { t } = useI18n()
  return (
    <p aria-hidden="true" className="stamp-status font-mono" {...{ [`data-${marker}-status`]: '' }}>
      <span>{t('stamp.checking')}</span>
      <span className="trace-caret">▮</span>
    </p>
  )
}

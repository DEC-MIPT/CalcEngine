import { useParams } from 'react-router'
import { ReportForm } from '@/components/ReportForm'
import { useI18n } from '@/i18n/context'

export function ReportScreen({ selection = false }: { selection?: boolean }) {
  const { t } = useI18n()
  const { id } = useParams() as { id: string }
  return (
    <>
      <h1>{t('report.title')}</h1>
      <ReportForm key={id} resultId={id} selection={selection} />
    </>
  )
}

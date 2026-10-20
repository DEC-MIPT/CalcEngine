import { DownloadSimple } from '@phosphor-icons/react'
import { useLayoutEffect, useRef } from 'react'
import { useI18n } from '@/i18n/context'
import { buttonClass } from './ui/button'

export type StampStrike = 'animated' | 'instant'

export type StampTitle = { designation: string; document_name: string; organization: string }

const COLUMNS: readonly { name: keyof StampTitle; column: string; className: string }[] = [
  { name: 'designation', column: '1', className: 'font-mono text-lg font-semibold' },
  { name: 'document_name', column: '5', className: '' },
  { name: 'organization', column: '9', className: '' },
]

export function ReportStamp({
  title,
  fileName,
  strike,
  onDownload,
}: {
  title: StampTitle
  fileName: string
  strike: StampStrike
  onDownload: () => void
}) {
  const { t } = useI18n()
  const download = useRef<HTMLButtonElement>(null)
  useLayoutEffect(() => {
    download.current?.focus()
  }, [])
  return (
    <section
      aria-labelledby="report-stamp-title"
      data-report-stamp
      data-strike={strike}
      className={`grid max-w-2xl border-2 border-primary bg-card sm:grid-cols-[minmax(0,1fr)_9rem]${strike === 'animated' ? ' report-strike' : ''}`}
    >
      <h2 id="report-stamp-title" className="sr-only">
        {t('report.ready')}
      </h2>
      <dl className="grid grid-cols-[auto_minmax(0,1fr)]">
        {COLUMNS.map(({ name, column, className }) => (
          <div key={name} className="col-span-2 grid grid-cols-subgrid not-last:border-b not-last:border-border" data-column={column}>
            <dt className="border-r border-border px-2.5 py-1.5 font-mono whitespace-nowrap text-sm text-muted-foreground">
              <span aria-hidden="true">
                {t('report.column')} {column}
              </span>
              <span className="sr-only">{t(`report.field.${name}`)}</span>
            </dt>
            <dd className={`min-w-0 px-2.5 py-1.5 break-words ${className}`}>{title[name]}</dd>
          </div>
        ))}
      </dl>
      <p
        className="flex items-center justify-center border-t border-primary px-3 py-2 font-mono font-semibold tracking-[0.2em] text-primary sm:border-t-0 sm:border-l"
        data-issued
      >
        {t('report.issued')}
      </p>
      <div className="flex flex-wrap items-center gap-3 border-t-2 border-primary p-3 sm:col-span-2">
        <button ref={download} type="button" onClick={onDownload} className={buttonClass}>
          <DownloadSimple aria-hidden="true" size={18} />
          {t('report.download')} <span className="font-mono font-normal">{fileName}</span>
        </button>
      </div>
    </section>
  )
}

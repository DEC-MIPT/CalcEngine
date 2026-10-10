import { fireEvent, render, screen, within } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import type { Language } from '@/i18n/dictionary'
import { ReportStamp, type StampStrike } from './ReportStamp'

const TITLE = { designation: 'DEC-2026-001', document_name: 'Bearing resistance', organization: 'Project LLC' }

function show(strike: StampStrike, language: Language = 'ru') {
  const onDownload = vi.fn()
  render(
    <I18nProvider initialLanguage={language}>
      <ReportStamp title={TITLE} fileName="report.docx" strike={strike} onDownload={onDownload} />
    </I18nProvider>,
  )
  return onDownload
}

describe('ReportStamp', () => {
  it('names each column of the title block for assistive technology', () => {
    show('instant')
    const stamp = screen.getByRole('region', { name: 'Отчёт сформирован' })

    expect(within(stamp).getByText('Обозначение документа')).toHaveClass('sr-only')
    expect(within(stamp).getByText('гр. 1').getAttribute('aria-hidden')).toBe('true')
    expect(stamp.className).not.toContain('report-strike')
  })

  it('strikes only when asked to, and downloads on the button', () => {
    const onDownload = show('animated', 'en')
    const stamp = screen.getByRole('region', { name: 'Report generated' })

    expect(stamp.className).toContain('report-strike')
    expect(within(stamp).getByText('ISSUED')).toBeInTheDocument()
    fireEvent.click(within(stamp).getByRole('button', { name: 'Download report.docx' }))
    expect(onDownload).toHaveBeenCalledOnce()
  })
})

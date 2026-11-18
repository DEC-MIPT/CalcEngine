import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import { loadsContactRefusalEnvelope } from '@/mocks/fixtures'
import { expectNoA11yViolations } from '@/test/axe'
import { DerivedCorrectionNote } from './DerivedCorrectionNote'

const reason = loadsContactRefusalEnvelope.verdict_reason

describe('stored derived correction note', () => {
  it('describes the focused input with stored diagnostic facts and engineer attribution', async () => {
    const { container } = render(
      <I18nProvider initialLanguage="ru">
        <label htmlFor="corrected">Vertical load</label>
        <input id="corrected" aria-describedby="correction" />
        <DerivedCorrectionNote id="correction" reason={reason} />
      </I18nProvider>,
    )
    const field = screen.getByRole('textbox', { name: 'Vertical load' })
    expect(field).toHaveAccessibleDescription(/p_corner_min: -30 кПа/u)
    expect(field).toHaveAccessibleDescription(/больше или равно 0 кПа/u)
    expect(field).toHaveAccessibleDescription(/Определяющий угол: mm/u)
    expect(screen.getByText(`Инженер: ${reason.source.engineer}`)).toBeVisible()
    expect(screen.getByText(`Обоснование: ${reason.source.rationale}`)).toBeVisible()
    expect(screen.queryByText('проверено')).not.toBeInTheDocument()
    expect(container.querySelector('[data-output], [data-verdict]')).toBeNull()
    await expectNoA11yViolations(container)
  })

  it('localizes guidance without changing the stored diagnostic quantity or corner', () => {
    render(<I18nProvider initialLanguage="en"><DerivedCorrectionNote id="correction" reason={reason} /></I18nProvider>)
    expect(screen.getByText('Previous refusal reason — review the related inputs')).toBeVisible()
    expect(screen.getByText('p_corner_min')).toBeVisible()
    expect(screen.getByText('mm')).toBeVisible()
    expect(screen.getByText(`Engineer: ${reason.source.engineer}`)).toBeVisible()
    expect(screen.getByText('greater than or equal to')).toHaveClass('sr-only')
  })

  it('keeps a tiny raw diagnostic value nonzero instead of applying an output rounding rule', () => {
    const tiny = { ...reason, value: { value: -1e-25, unit: 'kPa' } }
    const { container } = render(<I18nProvider initialLanguage="en"><DerivedCorrectionNote id="correction" reason={tiny} /></I18nProvider>)
    expect(container).toHaveTextContent('p_corner_min: -1E-25 kPa')
    expect(tiny.value.value).toBe(-1e-25)
  })
})

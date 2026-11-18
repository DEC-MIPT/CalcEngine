import { render, screen } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { DraftContext, type Draft, type SentForm } from '@/form/draftContext'
import type { FormCorrectionState } from '@/form/correction'
import { I18nProvider } from '@/i18n/I18nProvider'
import { loadsCalculationType, loadsContactRefusalEnvelope } from '@/mocks/fixtures'
import { CalculationForm } from './CalculationForm'

const reason = loadsContactRefusalEnvelope.verdict_reason
const resultId = loadsContactRefusalEnvelope.result_id

afterEach(() => vi.unstubAllGlobals())

function show(sent: SentForm, relatedInputs = reason.related_inputs) {
  vi.stubGlobal('matchMedia', () => ({ matches: true }))
  const draft: Draft = {
    read: () => ({ values: { N: '+0600.000' }, units: { N: 'kN' } }),
    setValue: vi.fn(), setUnit: vi.fn(), remember: vi.fn(), sent,
  }
  const state: FormCorrectionState = {
    derivedCorrection: { resultId, reason: { ...reason, related_inputs: relatedInputs } },
  }
  const router = createMemoryRouter([{
    path: '/calculations/new',
    element: <I18nProvider><DraftContext.Provider value={draft}><CalculationForm type={loadsCalculationType} /></DraftContext.Provider></I18nProvider>,
  }], { initialEntries: [{ pathname: '/calculations/new', state }] })
  return render(<RouterProvider router={router} />)
}

describe('derived correction context binding', () => {
  it.each([
    { resultId: 'another-result', type: loadsCalculationType.name },
    { resultId, type: 'foundations_shallow_r' },
  ])('ignores a correction that does not match the submitted result/type: %j', (sent) => {
    show(sent)
    expect(document.getElementById('field-N')).toHaveValue('+0600.000')
    expect(screen.queryByText('Причина предыдущего отказа — проверьте связанные исходные данные')).not.toBeInTheDocument()
    expect(document.getElementById('derived-N')).toBeNull()
  })

  it('uses the first registered related input without manufacturing a diagnostic field', () => {
    show({ resultId, type: loadsCalculationType.name }, [reason.quantity, 'N'])
    const field = document.getElementById('field-N')!
    expect(field).toHaveFocus()
    expect(field).toHaveAccessibleDescription(/p_corner_min: -30 кПа/u)
    expect(document.getElementById(`field-${reason.quantity}`)).toBeNull()
  })

  it('does not attach a correction when the supplied related names are not form inputs', () => {
    show({ resultId, type: loadsCalculationType.name }, [reason.quantity])
    expect(document.getElementById('derived-N')).toBeNull()
    expect(document.getElementById(`field-${reason.quantity}`)).toBeNull()
    expect(screen.getAllByRole('textbox')).toHaveLength(15)
  })
})

import { render, screen } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import type { components } from '@/api/schema'
import { I18nProvider } from '@/i18n/I18nProvider'
import type { Language } from '@/i18n/dictionary'
import { failEnvelope, passEnvelope, warningEnvelope } from '@/mocks/fixtures'
import { expectNoA11yViolations } from '@/test/axe'
import { VerdictStamp } from './VerdictStamp'

type Envelope = components['schemas']['ResultEnvelope']
type CheckReason = components['schemas']['CheckReason']

function show(envelope: object, language: Language = 'ru') {
  const router = createMemoryRouter(
    [
      {
        path: '/',
        element: (
          <I18nProvider initialLanguage={language}>
            <VerdictStamp envelope={envelope as Envelope} reason={(envelope as Envelope).verdict_reason as CheckReason} />
          </I18nProvider>
        ),
      },
    ],
    { initialEntries: ['/'] },
  )
  return render(<RouterProvider router={router} />)
}

describe('VerdictStamp (critique of the result screen)', () => {
  it('names a passed check, its comparison with both values and units, and the report action', () => {
    show(passEnvelope)
    const stamp = screen.getByRole('region', { name: 'Проверка выполнена' })

    expect(stamp).toHaveAttribute('data-verdict', 'pass')
    expect(stamp.className).toContain('border-primary')
    expect(stamp.querySelector('[data-check="p_le_R"] p')).toHaveTextContent('100 кПа ≤меньше или равно 172,5 кПа')
    expect(screen.getByRole('img', { name: 'p \\le R' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Запросить отчёт' })).toHaveAttribute(
      'href',
      `/calculations/${passEnvelope.result_id}/report`,
    )
  })

  it('names a failed check in red words, not by colour alone', () => {
    show(failEnvelope)
    const stamp = screen.getByRole('region', { name: 'Проверка не выполнена' })

    expect(stamp.className).toContain('border-destructive')
    expect(stamp.querySelector('[data-check] p')).toHaveTextContent('200 кПа ≤меньше или равно 172,5 кПа')
  })

  it('reads out the number of steps and warnings and the engine version', () => {
    show(warningEnvelope)
    const facts = [...document.querySelectorAll('dl > div')].map((fact) => fact.textContent)

    expect(facts).toEqual(['Шагов расчёта9', 'Предупреждений1', 'Версия движка0.1.0'])
  })

  it('shows the verdict without a comparison when the deciding check is not in the trace', () => {
    show({ ...passEnvelope, verdict_reason: { kind: 'check', step_id: 'missing' } })

    expect(screen.getByRole('region', { name: 'Проверка выполнена' })).toBeInTheDocument()
    expect(document.querySelector('[data-check]')).toBeNull()
  })

  it('speaks English', () => {
    show(failEnvelope, 'en')

    expect(screen.getByRole('region', { name: 'Check failed' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Request a report' })).toBeInTheDocument()
    expect(screen.getByText('Engine version')).toBeInTheDocument()
  })

  it.each([passEnvelope, failEnvelope])('has no axe violation', async (envelope) => {
    const { container } = show(envelope)

    await expectNoA11yViolations(container)
  })
})

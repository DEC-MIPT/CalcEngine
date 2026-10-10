import { fireEvent, render, screen } from '@testing-library/react'
import { useState } from 'react'
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
    expect(stamp.className).toContain('stamp-enter')
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

    expect(facts).toEqual(['Шагов расчёта9 — к ходу расчёта', 'Предупреждений1', 'Версия движка0.1.0'])
  })

  it('links the number of steps to the trace heading', () => {
    show(passEnvelope)

    const link = screen.getByRole('link', { name: '9 — к ходу расчёта' })
    expect(link).toHaveAttribute('href', '#trace-title')
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

describe('VerdictStamp focus and frame (9.4)', () => {
  it.each([
    ['pass', passEnvelope, 'Проверка выполнена'],
    ['fail', failEnvelope, 'Проверка не выполнена'],
  ])('takes focus on arrival for a %s and carries the frame class', (_verdict, envelope, name) => {
    show(envelope)
    const stamp = screen.getByRole('region', { name })

    expect(stamp).toHaveFocus()
    expect(stamp).toHaveAttribute('tabindex', '-1')
    expect(stamp).toHaveClass('stamp-frame')
  })

  it('takes focus once: a later drawing does not take it back', () => {
    function Host() {
      const [count, setCount] = useState(0)
      return (
        <I18nProvider initialLanguage="ru">
          <button type="button" onClick={() => setCount(count + 1)}>
            draw {count}
          </button>
          <VerdictStamp envelope={passEnvelope as Envelope} reason={passEnvelope.verdict_reason as CheckReason} />
        </I18nProvider>
      )
    }
    render(<RouterProvider router={createMemoryRouter([{ path: '/', element: <Host /> }])} />)
    const button = screen.getByRole('button')
    button.focus()

    fireEvent.click(button)

    expect(screen.getByRole('button', { name: 'draw 1' })).toHaveFocus()
  })
})

describe('VerdictStamp: reveal after the trace playback', () => {
  function reveal(envelope: object, state: 'pending' | 'celebrate' | 'plain') {
    const typed = envelope as Envelope
    const router = createMemoryRouter(
      [
        {
          path: '/',
          element: (
            <I18nProvider initialLanguage="ru">
              <VerdictStamp envelope={typed} reason={typed.verdict_reason as CheckReason} reveal={state} />
            </I18nProvider>
          ),
        },
      ],
      { initialEntries: ['/'] },
    )
    return render(<RouterProvider router={router} />)
  }

  it('keeps the verdict readable to assistive technology while the trace plays', () => {
    reveal(passEnvelope, 'pending')

    const stamp = screen.getByRole('region', { name: 'Проверка выполнена' })
    expect(stamp).toHaveAttribute('data-reveal', 'pending')
    expect(stamp.className).toContain('stamp-pending')
    expect(stamp.className).not.toContain('stamp-enter')
    expect(screen.getByRole('heading', { name: 'Проверка выполнена' })).toBeInTheDocument()
    const status = stamp.querySelector('[data-stamp-status]')!
    expect(status).toHaveAttribute('aria-hidden', 'true')
    expect(status.textContent).toBe('ВЫПОЛНЕНИЕ РАСЧЕТА▮')
  })

  it('announces a passed check politely', () => {
    reveal(passEnvelope, 'plain')
    expect(screen.getByRole('region', { name: 'Проверка выполнена' })).toHaveAttribute('aria-live', 'polite')
    expect(screen.getByRole('region', { name: 'Проверка выполнена' })).toHaveAttribute('aria-atomic', 'true')
  })

  it('announces a failed check assertively', () => {
    reveal(failEnvelope, 'plain')

    expect(screen.getByRole('region', { name: 'Проверка не выполнена' })).toHaveAttribute('aria-live', 'assertive')
  })

  it('draws the check mark only for the celebrated verdict', () => {
    reveal(passEnvelope, 'celebrate')

    const stamp = screen.getByRole('region', { name: 'Проверка выполнена' })
    expect(stamp.className).toContain('stamp-celebrate')
    expect(stamp.querySelector('svg.stamp-mark')).toHaveAttribute('aria-hidden', 'true')
    expect(stamp.querySelector('[data-stamp-status]')).toBeNull()
  })

  it('shows a plain verdict with no mark and no status', () => {
    reveal(warningEnvelope, 'plain')

    const stamp = screen.getByRole('region', { name: 'Проверка выполнена' })
    expect(stamp.className).not.toMatch(/stamp-(pending|celebrate)/)
    expect(stamp.querySelector('.stamp-mark')).toBeNull()
  })

  it('reports no accessibility violation while pending', async () => {
    const { container } = reveal(passEnvelope, 'pending')

    await expectNoA11yViolations(container)
  })
})

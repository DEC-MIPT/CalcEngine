import { fireEvent, render, screen, within } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { loadsBoundRefusalEnvelope, loadsContactRefusalEnvelope, warningEnvelope } from '@/mocks/fixtures'
import { server } from '@/mocks/server'
import { hasPlayed, resetPlayed } from '@/lib/playback'
import { routes } from '@/routes'

beforeEach(() => resetPlayed())
afterEach(() => vi.unstubAllGlobals())

function open(id: string, reduced: boolean) {
  vi.stubGlobal('matchMedia', () => ({ matches: reduced }))
  return render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: [`/calculations/${id}`] })} />)
}

describe('stored derived diagnostic contract', () => {
  it.each([false, true])('shows the entire captured prefix immediately with reduced motion %s', async (reduced) => {
    open(loadsContactRefusalEnvelope.result_id, reduced)
    const refusal = await screen.findByRole('region', { name: /условие полного контакта не выполнено/ })
    const trace = screen.getByRole('region', { name: 'Диагностическая последовательность' })
    expect([...trace.querySelectorAll('[data-step]')].map((step) => step.getAttribute('data-step'))).toEqual(loadsContactRefusalEnvelope.trace.map((step) => step.step_id))
    expect(trace.querySelector('[inert]')).toBeNull()
    expect(trace.querySelector('[data-arrival="pending"]')).toBeNull()
    expect(trace).toHaveAttribute('data-playback', 'idle')
    expect(refusal).toHaveFocus()
    expect(document.querySelector('[data-verdict]')).toBeNull()
    expect(document.querySelector('[data-output]')).toBeNull()
    expect(document.querySelector('[data-check-step]')).toBeNull()
    expect(document.querySelector('[data-reveal="pending"]')).toBeNull()
    expect(document.querySelector('.stamp-celebrate, .stamp-mark, [data-skip-hint]')).toBeNull()
    expect(hasPlayed(loadsContactRefusalEnvelope.result_id)).toBe(false)
  })

  it('retains engineer attribution throughout the prefix when normative-status badges are disabled', async () => {
    open(loadsContactRefusalEnvelope.result_id, false)
    await screen.findByRole('region', { name: /условие полного контакта не выполнено/ })
    const trace = screen.getByRole('region', { name: 'Диагностическая последовательность' })
    fireEvent.click(within(trace).getByRole('button', { name: 'Развернуть все шаги' }))
    for (const step of loadsContactRefusalEnvelope.trace) {
      if (step.kind !== 'engineer_formula') continue
      const row = trace.querySelector(`[data-step="${step.step_id}"]`) as HTMLElement
      expect(within(row).getByText('Инженерная формула')).toBeVisible()
      expect(within(row).getByText('Инженерное правило')).toBeVisible()
      expect(within(row).getByText(`Инженер: ${step.source.engineer}`)).toBeVisible()
      expect(within(row).getByText(`Обоснование: ${step.source.rationale}`)).toBeVisible()
      expect(within(row).queryByText('Нормативные ссылки')).not.toBeInTheDocument()
    }
    expect(within(trace).queryByText('не проверено')).not.toBeInTheDocument()
  })

  it('renders the exact captured reason, corner and provenance without turning diagnostic values into final outputs', async () => {
    open(loadsContactRefusalEnvelope.result_id, false)
    const refusal = await screen.findByRole('region', { name: /условие полного контакта не выполнено/ })
    const reason = loadsContactRefusalEnvelope.verdict_reason
    expect(refusal).toHaveTextContent(reason.quantity)
    expect(refusal).toHaveTextContent('-30 кПа')
    expect(refusal).toHaveTextContent('0 кПа')
    expect(within(refusal).getByText(reason.limiting_corner)).toBeVisible()
    expect(refusal).toHaveTextContent(reason.related_inputs.join(', '))
    expect(refusal).toHaveTextContent(reason.source.rationale)
    expect(within(refusal).getByText(loadsContactRefusalEnvelope.parameter_source.data_sha256)).toHaveClass('sr-only')
    expect(screen.queryByRole('heading', { name: 'Выходные величины' })).not.toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Проверки несущей способности' })).not.toBeInTheDocument()
    expect(screen.queryByRole('region', { name: 'Проверка выполнена' })).not.toBeInTheDocument()
    expect(screen.queryByRole('region', { name: 'Проверка не выполнена' })).not.toBeInTheDocument()
  })

  it('keeps a historical input-bound refusal immediate without inventing a diagnostic trace', async () => {
    open(loadsBoundRefusalEnvelope.result_id, false)
    const refusal = await screen.findByRole('region', { name: /^Расчёт не выполнен/ })
    expect(refusal).toHaveFocus()
    expect(screen.queryByRole('heading', { name: 'Ход расчёта' })).not.toBeInTheDocument()
    expect(document.querySelector('[data-step], [data-check-step], [data-output]')).toBeNull()
    expect(hasPlayed(loadsBoundRefusalEnvelope.result_id)).toBe(false)
  })

  it('renders an explicitly synthetic stored diagnostic warning without claiming a validated loads range', async () => {
    const envelope = { ...loadsContactRefusalEnvelope, warnings: warningEnvelope.warnings }
    server.use(http.get('*/calculations/:id', () => HttpResponse.json(envelope)))
    open(envelope.result_id, false)

    const refusal = await screen.findByRole('region', { name: /условие полного контакта не выполнено/ })
    const warning = await screen.findByRole('region', { name: /входное значение вне проверенного диапазона/ })

    expect(refusal).toHaveFocus()
    expect(warning).toHaveTextContent('6 м')
    expect(warning).toHaveTextContent('5 м')
    expect(warning).toHaveTextContent(warningEnvelope.warnings[0].bound.source.engineer)
    expect(warning).toHaveTextContent(warningEnvelope.warnings[0].bound.source.rationale)
    expect(screen.getByRole('region', { name: 'Диагностическая последовательность' })).toBeInTheDocument()
    expect(document.querySelector('[data-output], [data-verdict], [data-check-step]')).toBeNull()
  })
})

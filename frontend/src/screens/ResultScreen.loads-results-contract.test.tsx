import { render, screen, waitFor, within } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import type { components } from '@/api/schema'
import {
  catalogSource, loadsBoundRefusalEnvelope, loadsCentralEnvelope, loadsContactRefusalEnvelope,
  loadsDraftSource, loadsFailEnvelope, loadsStrictSource, passEnvelope, warningEnvelope,
} from '@/mocks/fixtures'
import { server } from '@/mocks/server'
import { routes } from '@/routes'

type Envelope = components['schemas']['ResultEnvelope']

function open(envelope: Envelope) {
  server.use(http.get('*/calculations/:id', () => HttpResponse.json(envelope)))
  return render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: [`/calculations/${envelope.result_id}`] })} />)
}

const ids = (selector: string, attribute: string) => [...document.querySelectorAll(selector)].map((node) => node.getAttribute(attribute))

describe('stored loads result screen contract', () => {
  it.each([loadsCentralEnvelope, loadsFailEnvelope])('preserves supplied output and check order on a completed result', async (envelope) => {
    const before = structuredClone(envelope)
    open(envelope)
    await screen.findByRole('region', { name: envelope.verdict === 'pass' ? 'Проверка выполнена' : 'Проверка не выполнена' })
    const outputNames = envelope.outputs.map((output) => output.quantity)
    expect(ids('[data-output]', 'data-output')).toEqual(outputNames)
    const trace = screen.getByRole('region', { name: 'Ход расчёта' })
    expect([...trace.querySelectorAll('[data-step]')].map((step) => step.getAttribute('data-step'))).toEqual(envelope.trace.map((step) => step.step_id))
    const stamp = screen.getByRole('region', { name: envelope.verdict === 'pass' ? 'Проверка выполнена' : 'Проверка не выполнена' })
    if (envelope.verdict_reason.kind !== 'check') throw new Error('Completed fixture required')
    expect(stamp.querySelector('[data-check]')).toHaveAttribute('data-check', envelope.verdict_reason.step_id)
    expect(envelope).toEqual(before)
  })

  it.each([loadsStrictSource, loadsDraftSource, catalogSource])('keeps the supplied parameter source $kind/$profile visible without changing the verdict', async (source) => {
    open({ ...loadsCentralEnvelope, parameter_source: source })
    const stamp = await screen.findByRole('region', { name: 'Проверка выполнена' })
    const label = stamp.querySelector(`[data-source="${source.kind}"]`)
    expect(label).toBeInTheDocument()
    if (source.kind === 'interim') {
      expect(label).toHaveAttribute('data-profile', source.profile)
      expect(within(stamp).getByText(source.data_sha256)).toHaveClass('sr-only')
      expect(within(stamp).getByTitle(source.data_sha256!)).toHaveTextContent(`${source.data_sha256!.slice(0, 12)}…`)
      expect(label).toHaveTextContent('ВРЕМЕННЫЕ ДАННЫЕ')
      if (source.profile === 'draft') expect(label).toHaveTextContent('Черновик: значения не прошли верификацию')
    } else expect(label).toHaveTextContent('каталог норм')
  })

  it('shows a supplied warning alongside a passing result without silently rewriting its source or bounds', async () => {
    open({ ...loadsCentralEnvelope, warnings: warningEnvelope.warnings })
    await screen.findByRole('region', { name: 'Проверка выполнена' })
    const warning = await screen.findByText('входное значение вне проверенного диапазона')
    expect(warning).toBeInTheDocument()
    expect(document.querySelector('[data-verdict]')).toHaveAttribute('data-verdict', 'pass')
    expect(document.querySelector('[data-verdict]')).not.toHaveAttribute('data-reveal', 'celebrate')
  })

  it.each([loadsBoundRefusalEnvelope, loadsContactRefusalEnvelope])('keeps diagnostic refusals outside final outputs and completed bearing results', async (envelope) => {
    open(envelope)
    await screen.findByRole('link', { name: 'Запросить отчёт' })
    expect(screen.queryByRole('heading', { name: 'Выходные величины' })).not.toBeInTheDocument()
    expect(document.querySelector('[data-output]')).toBeNull()
    expect(document.querySelector('[data-verdict]')).toBeNull()
    expect(screen.queryByRole('region', { name: 'Проверка выполнена' })).not.toBeInTheDocument()
    expect(screen.queryByRole('region', { name: 'Проверка не выполнена' })).not.toBeInTheDocument()
    expect(screen.getByText(loadsStrictSource.data_sha256)).toHaveClass('sr-only')
  })

  it('preserves the historical pilot output, deciding check and hidden norm-status policy', async () => {
    open(passEnvelope as Envelope)
    await screen.findByRole('region', { name: 'Проверка выполнена' })
    expect(ids('[data-output]', 'data-output')).toEqual(['R'])
    expect(document.querySelector('[data-output="R"] [data-value]')).toHaveTextContent('172,5')
    const stamp = screen.getByRole('region', { name: 'Проверка выполнена' })
    expect(stamp.querySelector('[data-check]')).toHaveAttribute('data-check', 'p_le_R')
    const trace = screen.getByRole('region', { name: 'Ход расчёта' })
    await waitFor(() => expect(within(trace).queryByText('не проверено')).not.toBeInTheDocument())
    expect(screen.queryByText('Источник правила')).not.toBeInTheDocument()
  })
})

import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { PASS_ID, passEnvelope } from '@/mocks/fixtures'
import { server } from '@/mocks/server'
import { routes } from '@/routes'
import { expectNoA11yViolations } from '@/test/axe'

function open(address: string) {
  const router = createMemoryRouter(routes, { initialEntries: [address] })
  return { router, ...render(<RouterProvider router={router} />) }
}

function recordRequests() {
  const seen: string[] = []
  const listener = ({ request }: { request: Request }) => {
    seen.push(`${request.method} ${new URL(request.url).pathname}`)
  }
  server.events.on('request:start', listener)
  return { seen, stop: () => server.events.removeListener('request:start', listener) }
}

afterEach(() => vi.restoreAllMocks())

describe('submit opens the stored result (4.3)', () => {
  it('opens /calculations/<id> after a submit of the form', async () => {
    const { router } = open('/calculations/new?type=foundations_shallow_r')
    const values: Record<string, string> = {
      b: '2',
      d_1: '1.5',
      d_b: '0',
      gamma_II: '18',
      gamma_II_prime: '18',
      c_II: '10',
      phi_II: '20',
      p: '100',
    }
    await screen.findByRole('button', { name: 'Рассчитать' })
    for (const [name, value] of Object.entries(values)) {
      fireEvent.change(document.getElementById(`field-${name}`)!, { target: { value } })
    }

    fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))

    expect(await screen.findByRole('heading', { name: 'Результат расчёта' })).toBeInTheDocument()
    await waitFor(() => expect(router.state.location.pathname).toBe(`/calculations/${PASS_ID}`))
    expect(await screen.findByText(PASS_ID)).toBeInTheDocument()
  })
})

describe('opening a result by its address (4.3)', () => {
  it('reads GET /calculations/{id} and runs no calculation, also after a reload', async () => {
    const requests = recordRequests()
    const first = open(`/calculations/${PASS_ID}`)
    expect(await screen.findByText(PASS_ID)).toBeInTheDocument()
    first.unmount()

    open(`/calculations/${PASS_ID}`)
    expect(await screen.findByText(PASS_ID)).toBeInTheDocument()
    requests.stop()

    expect(requests.seen).toEqual([`GET /calculations/${PASS_ID}`, `GET /calculations/${PASS_ID}`])
  })

  it('shows the trace of the stored result under the id', async () => {
    open(`/calculations/${PASS_ID}`)

    expect(await screen.findByRole('heading', { name: 'Ход расчёта', level: 2 })).toBeInTheDocument()
    expect(screen.getAllByRole('heading', { level: 3 })).toHaveLength(passEnvelope.trace.length)
  })

  it('shows the loading state first and has no accessibility violations', async () => {
    const { container } = open(`/calculations/${PASS_ID}`)

    expect(screen.getByRole('status')).toBeInTheDocument()
    await screen.findByText(PASS_ID)
    await expectNoA11yViolations(container)
  })

  it('says that the result was not found for an unknown id and links to the type selection', async () => {
    open('/calculations/00000000-0000-4000-8000-000000000000')

    expect(await screen.findByRole('heading', { name: 'Результат не найден' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'К выбору типа расчёта' })).toHaveAttribute('href', '/')
  })

  it('shows a 503 with its code and retries the same request', async () => {
    server.use(
      http.get('*/calculations/:id', () =>
        HttpResponse.json({ code: 'database_unavailable', message: 'down' }, { status: 503 }),
      ),
    )
    open(`/calculations/${PASS_ID}`)

    expect(await screen.findByRole('alert')).toHaveTextContent('database_unavailable')
    server.resetHandlers()
    fireEvent.click(screen.getByRole('button', { name: 'Повторить' }))

    expect(await screen.findByText(PASS_ID)).toBeInTheDocument()
  })
})

describe('link from the result to the report (4.4)', () => {
  it('lands on /calculations/<id>/report of the same id', async () => {
    const { router } = open(`/calculations/${PASS_ID}`)

    fireEvent.click(await screen.findByRole('link', { name: 'Запросить отчёт' }))

    expect(router.state.location.pathname).toBe(`/calculations/${PASS_ID}/report`)
    expect(screen.getByText(PASS_ID)).toBeInTheDocument()
  })
})

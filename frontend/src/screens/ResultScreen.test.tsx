import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { PASS_ID, passEnvelope, REFUSED_ID, WARNING_ID } from '@/mocks/fixtures'
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
    expect(await screen.findByRole('region', { name: 'Проверка выполнена' })).toBeInTheDocument()
  })
})

describe('opening a result by its address (4.3)', () => {
  it('reads GET /calculations/{id} and runs no calculation, also after a reload', async () => {
    const requests = recordRequests()
    const first = open(`/calculations/${PASS_ID}`)
    expect(await screen.findByRole('region', { name: 'Проверка выполнена' })).toBeInTheDocument()
    first.unmount()

    open(`/calculations/${PASS_ID}`)
    expect(await screen.findByRole('region', { name: 'Проверка выполнена' })).toBeInTheDocument()
    requests.stop()

    expect(requests.seen.filter((request) => request !== 'GET /calculation-types')).toEqual([
      `GET /calculations/${PASS_ID}`,
      `GET /calculations/${PASS_ID}`,
    ])
  })

  it('shows the trace of the stored result under the id', async () => {
    open(`/calculations/${PASS_ID}`)

    expect(await screen.findByRole('heading', { name: 'Ход расчёта', level: 2 })).toBeInTheDocument()
    expect(within(screen.getByRole('region', { name: 'Ход расчёта' })).getAllByRole('heading', { level: 3 })).toHaveLength(
      passEnvelope.trace.length,
    )
  })

  it('typesets the substitutions by the symbols of the calculation types', async () => {
    open(`/calculations/${PASS_ID}`)

    const step = await screen.findByText((_, element) => element?.getAttribute('data-step') === 'R')
    await waitFor(() =>
      expect(within(step).getByText('gamma_II').closest('li')!.querySelector('[role="img"]')).toHaveAttribute(
        'aria-label',
        '\\gamma_{II}',
      ),
    )
  })

  it('still shows the trace, with the substitutions by name, when the calculation types do not load', async () => {
    server.use(http.get('*/calculation-types', () => HttpResponse.json({}, { status: 500 })))
    open(`/calculations/${PASS_ID}`)

    const step = await screen.findByText((_, element) => element?.getAttribute('data-step') === 'R')
    expect(within(step).getByText('gamma_II')).toHaveProperty('tagName', 'CODE')
    expect(within(step).getByText('gamma_c1')).toHaveClass('sr-only')
  })

  it('shows no verification status of the norms in the trace and no source column in the outputs', async () => {
    open(`/calculations/${PASS_ID}`)

    const trace = (await screen.findByRole('heading', { name: 'Ход расчёта', level: 2 })).closest('section')!
    expect(within(trace).queryByText('Шагов с непроверенными нормативными ссылками', { exact: false })).toBeNull()
    expect(within(trace).queryByText('не проверено')).toBeNull()
    expect(within(trace).getAllByText('<NORM-DOC-PLACEHOLDER>').length).toBeGreaterThan(0)
    expect(screen.queryByText('Источник правила')).toBeNull()
  })

  it('shows the outputs above the trace', async () => {
    open(`/calculations/${PASS_ID}`)

    const outputs = await screen.findByRole('heading', { name: 'Выходные величины', level: 2 })
    const trace = screen.getByRole('heading', { name: 'Ход расчёта', level: 2 })
    expect(outputs.compareDocumentPosition(trace) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
    expect(document.querySelector('[data-output="R"] [data-value]')).toHaveTextContent('172,5')
  })

  it('shows the loading state first and has no accessibility violations', async () => {
    const { container } = open(`/calculations/${PASS_ID}`)

    expect(screen.getByRole('status')).toBeInTheDocument()
    await screen.findByRole('region', { name: 'Проверка выполнена' })
    await expectNoA11yViolations(container)
  })

  it('says that the result was not found for an unknown id and links to the type selection', async () => {
    open('/calculations/00000000-0000-4000-8000-000000000000')

    expect(await screen.findByRole('heading', { name: 'Результат не найден' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'К выбору типа расчёта' })).toHaveAttribute('href', '/')
  })

  it('says that the result was not found for an id the backend rejects as malformed', async () => {
    server.use(
      http.get('*/calculations/:id', () =>
        HttpResponse.json(
          {
            code: 'validation_error',
            message: 'The request does not match its schema.',
            fields: [{ location: ['path', 'result_id'], message: 'Invalid value.' }],
          },
          { status: 422 },
        ),
      ),
    )
    open('/calculations/abc')

    expect(await screen.findByRole('heading', { name: 'Результат не найден' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Повторить' })).toBeNull()
  })

  it.each([
    ['another field', [{ location: ['query', 'x'], message: 'Invalid value.' }]],
    ['no field', []],
  ])('shows a 422 that names %s as an error', async (_case, fields) => {
    server.use(
      http.get('*/calculations/:id', () =>
        HttpResponse.json({ code: 'validation_error', message: 'The request does not match its schema.', fields }, { status: 422 }),
      ),
    )
    open(`/calculations/${PASS_ID}`)

    expect(await screen.findByRole('alert')).toHaveTextContent('validation_error')
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

    expect(await screen.findByRole('region', { name: 'Проверка выполнена' })).toBeInTheDocument()
  })
})

describe('link from the result to the report (4.4)', () => {
  it('lands on /calculations/<id>/report of the same id', async () => {
    const { router } = open(`/calculations/${PASS_ID}`)

    fireEvent.click(await screen.findByRole('link', { name: 'Запросить отчёт' }))

    expect(router.state.location.pathname).toBe(`/calculations/${PASS_ID}/report`)
  })
})


const region = (name: RegExp) => screen.findByRole('region', { name })

describe('refusal (6.4b)', () => {
  it('shows the violated bound, the input value and the bound sources, and no result value', async () => {
    const { container } = open(`/calculations/${REFUSED_ID}`)
    const refusal = await region(/^Расчёт не выполнен: входное значение вне диапазона метода$/)

    expect(refusal.querySelector('[data-fact="input"]')).toHaveTextContent('b = 12 м')
    expect(refusal.querySelector('[data-fact="bound"]')).toHaveTextContent('b ≤меньше или равно 10 м')
    expect(within(refusal).getByText('Источник границы').nextElementSibling).toHaveTextContent('<NORM-DOC-PLACEHOLDER>')
    expect(within(refusal).getByText(/Результат не вычислялся/)).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Выходные величины' })).toBeNull()
    expect(screen.queryByRole('heading', { name: 'Ход расчёта' })).toBeNull()
    expect(container).not.toHaveTextContent('кПа')
    expect(screen.getByRole('link', { name: 'Запросить отчёт' })).toBeInTheDocument()
    await expectNoA11yViolations(container)
  })
})

describe('applicability warning (6.4c)', () => {
  it('shows the input, the violated validated bound and its engineer-set source next to the outputs', async () => {
    const { container } = open(`/calculations/${WARNING_ID}`)
    const warning = await region(/^Предупреждение: входное значение вне проверенного диапазона$/)
    const outputs = screen.getByRole('heading', { name: 'Выходные величины' }).closest('section')!

    expect(outputs.querySelector('[data-output="R"] [data-value]')).toHaveTextContent('183,8')
    expect(outputs.nextElementSibling).toContainElement(warning)
    expect(warning.querySelector('[data-fact="input"]')).toHaveTextContent('b = 6 м')
    expect(warning.querySelector('[data-fact="bound"]')).toHaveTextContent('b ≤меньше или равно 5 м')
    expect(within(warning).getByText('Задано инженером')).toBeInTheDocument()
    expect(within(warning).getByText('Инженер: <ENGINEER>')).toBeInTheDocument()
    expect(within(warning).getByText('Обоснование: <RATIONALE>')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Ход расчёта' })).toBeInTheDocument()
    await expectNoA11yViolations(container)
  })

  it('shows no warning for a result without one', async () => {
    open(`/calculations/${PASS_ID}`)

    await screen.findByRole('heading', { name: 'Выходные величины' })
    expect(screen.queryByRole('region', { name: /^Предупреждение/ })).toBeNull()
  })
})

describe('a value outside the range is sent and decided by the backend (5.4)', () => {
  it.each([
    ['12', 'm', /^Расчёт не выполнен/],
    ['600', 'cm', /^Предупреждение/],
  ])('sends b = %s %s as entered and shows the outcome', async (value, unit, outcome) => {
    const bodies: unknown[] = []
    server.events.on('request:start', async ({ request }) => {
      if (request.method === 'POST') bodies.push(await request.clone().json())
    })
    open('/calculations/new?type=foundations_shallow_r')
    const values: Record<string, string> = {
      b: value,
      d_1: '1.5',
      d_b: '0',
      gamma_II: '18',
      gamma_II_prime: '18',
      c_II: '10',
      phi_II: '20',
      p: '100',
    }
    await screen.findByRole('button', { name: 'Рассчитать' })
    for (const [name, entered] of Object.entries(values)) {
      fireEvent.change(document.getElementById(`field-${name}`)!, { target: { value: entered } })
    }
    if (unit !== 'm') {
      fireEvent.change(screen.getByRole('combobox', { name: 'Единица: Ширина подошвы фундамента' }), {
        target: { value: unit },
      })
    }

    fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))

    expect(await region(outcome)).toBeInTheDocument()
    expect(bodies).toEqual([
      expect.objectContaining({ inputs: expect.objectContaining({ b: { value: Number(value), unit } }) }),
    ])
    server.events.removeAllListeners('request:start')
  })
})


describe('verdict first (critique of the result screen)', () => {
  it('puts the trace ruler and then the verdict stamp right under the title and no result id on the screen', async () => {
    const { container } = open(`/calculations/${PASS_ID}`)
    const stamp = await screen.findByRole('region', { name: 'Проверка выполнена' })

    const ruler = screen.getByRole('heading', { level: 1 }).nextElementSibling!
    expect(ruler).toHaveAttribute('data-ruler', String(passEnvelope.trace.length))
    expect(ruler.nextElementSibling).toBe(stamp)
    expect(container).not.toHaveTextContent(PASS_ID)
    expect(screen.getAllByRole('link', { name: 'Запросить отчёт' })).toHaveLength(1)
  })

  it('keeps the report action under a refusal', async () => {
    open(`/calculations/${REFUSED_ID}`)

    await region(/^Расчёт не выполнен/)
    expect(screen.getByRole('link', { name: 'Запросить отчёт' })).toHaveAttribute(
      'href',
      `/calculations/${REFUSED_ID}/report`,
    )
    expect(screen.queryByRole('region', { name: /^Проверка/ })).toBeNull()
  })
})

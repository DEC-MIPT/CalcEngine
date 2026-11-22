import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { selectionExhausted, selectionIncomplete, selectionSelected, weightsCentralContext, weightsCentralRequest, weightsContactRefusalEnvelope, weightsCentralEnvelope } from '@/mocks/designFixtures'
import { server } from '@/mocks/server'
import { routes } from '@/routes'
import { expectNoA11yViolations } from '@/test/axe'

vi.mock('@/components/Formula', () => ({ Formula: ({ latex }: { latex: string }) => <span>{latex}</span> }))

const formPath = '/calculations/new?type=foundations_shallow_loads'
const searchPath = `${formPath}&task=selection`
const explicitPath = '/calculations/new?type=foundations_shallow_weights'
const run = () => screen.getByRole('button', { name: 'Подобрать размеры' })

function open(address: string) {
  const router = createMemoryRouter(routes, { initialEntries: [address] })
  return { router, ...render(<RouterProvider router={router} />) }
}

function field(id: string) {
  return document.getElementById(id) as HTMLInputElement
}

function fillInput(id: string, value: number | string) {
  fireEvent.change(field(id), { target: { value: String(value) } })
}

async function fillCommon() {
  await screen.findByRole('button', { name: 'Подобрать размеры' })
  for (const [key, { value }] of Object.entries(selectionSelected.request.common_inputs)) fillInput(`field-${key}`, value)
}

function fillCandidate(index: number, b: string | number, l: string | number) {
  fillInput(`candidate-${index}-b`, b)
  fillInput(`candidate-${index}-l`, l)
}

function add() {
  fireEvent.click(screen.getByRole('button', { name: 'Добавить вариант' }))
}

afterEach(() => vi.unstubAllGlobals())

describe('foundation design tools', () => {
  it('switches to explicit weights and submits the typed scalar contract', async () => {
    vi.stubGlobal('matchMedia', () => ({ matches: true }))
    let posted: unknown
    server.use(http.post('*/calculations', async ({ request }) => {
      posted = await request.json()
      return HttpResponse.json({ code: 'database_unavailable', message: 'Unavailable' }, { status: 503 })
    }))
    open(formPath)
    fireEvent.click(await screen.findByRole('link', { name: 'Явные веса' }))
    await screen.findByText('Подбор доступен только для усреднённых весов.')
    expect(field('field-d')).toBeNull()
    expect(field('field-h')).toBeInTheDocument()
    expect(screen.getAllByRole('textbox')).toHaveLength(19)
    for (const [key, { value }] of Object.entries(weightsCentralRequest.inputs)) fillInput(`field-${key}`, value)
    fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))
    await screen.findByRole('alert')
    expect(posted).toEqual(weightsCentralRequest)
  })

  it('ignores a selection request for the explicit type and offers only check', async () => {
    open(`${explicitPath}&task=selection`)
    expect(await screen.findByRole('button', { name: 'Рассчитать' })).toBeEnabled()
    expect(screen.queryByRole('group', { name: 'Варианты размеров' })).toBeNull()
  })

  it('submits ordered original dimensions with no b or l in the common map and opens a stored selection', async () => {
    const { router, container } = open(searchPath)
    await fillCommon()
    expect(field('field-b')).toBeNull()
    expect(field('field-l')).toBeNull()
    fillCandidate(0, '02,00', '2')
    add()
    fillCandidate(1, '2', '3')
    fireEvent.click(run())
    await screen.findByRole('link', { name: 'Открыть выбранный расчёт' })
    expect(router.state.location.pathname).toBe(`/foundation-selections/${selectionSelected.selection_id}`)
    const items = container.querySelectorAll('[data-candidate]')
    expect(items[0]).toHaveTextContent('Проверки не пройдены')
    expect(items[1]).toHaveTextContent('Вариант 2 — Вариант выбран')
    await expectNoA11yViolations(container)
    fireEvent.click(items[1].querySelector('summary')!)
    await waitFor(() => expect(items[1].querySelectorAll('[data-check-step]')).toHaveLength(4))
    expect(items[1].querySelector('[data-deciding="true"]')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('link', { name: 'Открыть выбранный расчёт' }))
    await screen.findByRole('heading', { name: 'Схема нагрузок' }, { timeout: 5000 })
    expect(router.state.location.pathname).toBe(`/calculations/${selectionSelected.selected_result_id}`)
  })

  it('validates individual dimensions and maps server candidate errors without losing the draft', async () => {
    server.use(http.post('*/foundation-selections', () => HttpResponse.json({ code: 'invalid_input', message: 'invalid', fields: [
      { location: ['body', 'candidates', 0, 'l'], message: 'Проверьте длину.' },
    ] }, { status: 422 })))
    const { router } = open(searchPath)
    await fillCommon()
    fillCandidate(0, '2', '0')
    fireEvent.click(run())
    expect(screen.getByText('Введите положительный размер.')).toBeVisible()
    expect(field('candidate-0-l')).toHaveFocus()
    add()
    expect(screen.getByRole('group', { name: 'Вариант 2' })).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'Удалить вариант 2' }))
    fillCandidate(0, '2', '300,0')
    fireEvent.change(screen.getByRole('combobox', { name: 'Единица l · Вариант 1' }), { target: { value: 'cm' } })
    fireEvent.click(run())
    expect(await screen.findByText('Проверьте длину.')).toBeInTheDocument()
    expect(field('candidate-0-l')).toHaveFocus()
    expect(router.state.location.search).toContain('task=selection')
    expect(field('candidate-0-l')).toHaveValue('300,0')
  })

  it('aborts a request and ignores its late success; both back navigation and retry keep the draft', async () => {
    let delivered: (() => void) | undefined
    let signal: AbortSignal | undefined
    server.use(http.post('*/foundation-selections', async ({ request }) => {
      signal = request.signal
      await new Promise<void>((resolve) => { delivered = resolve })
      return HttpResponse.json(selectionSelected, { status: 201 })
    }))
    const { router } = open(searchPath)
    await fillCommon()
    fillCandidate(0, '2,00', '3')
    fireEvent.click(run())
    await waitFor(() => expect(signal).toBeDefined())
    expect(screen.getByText('Проверяем варианты…')).toBeVisible()
    fireEvent.click(screen.getByRole('button', { name: 'Отменить подбор' }))
    await act(async () => { delivered?.() })
    expect(signal?.aborted).toBe(true)
    expect(screen.getByText(/Если сервер уже сохранил результат/)).toBeVisible()
    fireEvent.click(screen.getByRole('link', { name: 'Проверить заданные размеры' }))
    await act(() => router.navigate(-1))
    expect(field('candidate-0-b')).toHaveValue('2,00')
    expect(router.state.location.pathname).toBe('/calculations/new')
  })

  it.each([
    [selectionExhausted, 'Ни один вариант не прошёл проверки'],
    [selectionIncomplete, 'Подбор прерван, победитель не определён'],
  ])('opens a stored non-winning selection and its correct report route', async (result, message) => {
    const { router } = open(`/foundation-selections/${result.selection_id}`)
    expect(await screen.findByText(message)).toBeVisible()
    expect(screen.queryByRole('link', { name: 'Открыть выбранный расчёт' })).toBeNull()
    if (result.stop_reason) expect(screen.getAllByText('Истёк лимит времени').length).toBeGreaterThan(0)
    fireEvent.click(screen.getByRole('link', { name: 'Запросить отчёт' }))
    expect(router.state.location.pathname).toBe(`/foundation-selections/${result.selection_id}/report`)
    expect(screen.getByRole('link', { name: 'Подбор' })).toHaveAttribute('href', `/foundation-selections/${result.selection_id}`)
  })

  it('preserves diagnostic pressure signs without showing four bearing checks', async () => {
    open(`/calculations/${weightsContactRefusalEnvelope.result_id}`)
    expect(await screen.findByText(/Диагностические давления без перераспределения контакта/)).toBeVisible()
    const table = screen.getByRole('table', { name: 'Давления в углах' })
    expect(within(table).getAllByRole('row')).toHaveLength(5)
    expect(table).toHaveTextContent(/[-−]\d/)
    expect(screen.queryByRole('heading', { name: 'Проверки' })).toBeNull()
  })

  it('retains the trace on context errors and retries only the optional context', async () => {
    let calls = 0
    server.use(http.get('*/foundation-calculations/:id/context', () => {
      calls += 1
      return calls === 1
        ? HttpResponse.json({ code: 'database_unavailable', message: 'Unavailable' }, { status: 503 })
        : HttpResponse.json(weightsCentralContext)
    }))
    open(`/calculations/${weightsCentralEnvelope.result_id}`)
    expect(await screen.findByText('Не удалось загрузить схему и эпюру.')).toBeVisible()
    expect(screen.getByRole('heading', { name: 'Ход расчёта' })).toBeVisible()
    fireEvent.click(screen.getByRole('button', { name: 'Повторить' }))
    expect(await screen.findByRole('heading', { name: 'Эпюра давлений' })).toBeVisible()
    expect(calls).toBe(2)
  })

  it('keeps historical results and reports available when the context is absent', async () => {
    server.use(http.get('*/foundation-calculations/:id/context', () => HttpResponse.json({
      code: 'foundation_context_unavailable', message: 'No stored context',
    }, { status: 404 })))
    open(`/calculations/${weightsCentralEnvelope.result_id}`)
    expect(await screen.findByText(/Для этого результата эпюра недоступна/)).toBeVisible()
    expect(screen.getByRole('link', { name: 'Запросить отчёт' })).toBeVisible()
    expect(screen.queryByRole('link', { name: 'Изменить исходные данные' })).toBeNull()
  })

  it('does not display mismatched saved context', async () => {
    server.use(http.get('*/foundation-calculations/:id/context', () => HttpResponse.json({
      ...weightsCentralContext, context: { ...weightsCentralContext.context, input_hash: 'different' },
    })))
    open(`/calculations/${weightsCentralEnvelope.result_id}`)
    expect(await screen.findByText(/Для этого результата эпюра недоступна/)).toBeVisible()
    expect(screen.queryByRole('table', { name: 'Давления в углах' })).toBeNull()
  })

  it('shows source-resolution failure and never chooses a candidate from an incomplete search', async () => {
    const request = { ...selectionIncomplete, stop_reason: 'parameter_source_unavailable', outcomes: [
      { ...selectionIncomplete.outcomes[0], status: 'error', reason: 'parameter_source_unavailable' },
    ] }
    server.use(http.get('*/foundation-selections/:id', () => HttpResponse.json(request)))
    open(`/foundation-selections/${selectionIncomplete.selection_id}`)
    expect(await screen.findByText('Ошибка расчёта')).toBeVisible()
    expect(screen.getAllByText('Источник параметров недоступен')).toHaveLength(2)
    expect(screen.queryByRole('link', { name: 'Открыть выбранный расчёт' })).toBeNull()
  })

  it('retries selection retrieval without resubmitting a search', async () => {
    let calls = 0
    server.use(http.get('*/foundation-selections/:id', () => ++calls === 1
      ? HttpResponse.json({ code: 'database_unavailable', message: 'Unavailable' }, { status: 503 })
      : HttpResponse.json(selectionExhausted)))
    open(`/foundation-selections/${selectionExhausted.selection_id}`)
    await screen.findByRole('alert')
    fireEvent.click(screen.getByRole('button', { name: 'Повторить' }))
    expect(await screen.findByText('Ни один вариант не прошёл проверки')).toBeVisible()
    expect(calls).toBe(2)
  })


  it('renders no pressure plot when evidence exists only for dimensions', async () => {
    server.use(http.get('*/foundation-calculations/:id/context', () => HttpResponse.json({
      ...weightsCentralContext, context: { ...weightsCentralContext.context, pressure_state: 'unavailable', corners: [] },
    })))
    open(`/calculations/${weightsCentralEnvelope.result_id}`)
    expect(await screen.findByText(/Для этого результата эпюра недоступна/)).toBeVisible()
    expect(screen.getByRole('heading', { name: 'Схема нагрузок' })).toBeVisible()
    expect(screen.queryByRole('heading', { name: 'Эпюра давлений' })).toBeNull()
  })

  it('reports a missing stored selection', async () => {
    open('/foundation-selections/not-stored')
    expect(await screen.findByRole('heading', { name: 'Страница не найдена' })).toBeVisible()
  })

  it('maps common-input errors and permits a retry after a service error', async () => {
    let queries = 0
    server.use(http.post('*/foundation-selections', () => {
      queries += 1
      return queries === 1 ? HttpResponse.json({ code: 'database_unavailable', message: 'Unavailable' }, { status: 503 })
        : HttpResponse.json({ code: 'invalid_input', message: 'Invalid', fields: [
          { location: ['body', 'common_inputs', 'h'], message: 'Проверьте h.' },
        ] }, { status: 422 })
    }))
    open(searchPath)
    await fillCommon()
    fillCandidate(0, 2, 3)
    fireEvent.click(run())
    await screen.findByRole('alert')
    fireEvent.click(screen.getByRole('button', { name: 'Повторить' }))
    expect(await screen.findByText('Проверьте h.')).toBeVisible()
    expect(field('field-h')).toHaveFocus()
  })


  it('explains a server cancellation without selecting a winner', async () => {
    server.use(http.get('*/foundation-selections/:id', () => HttpResponse.json({
      ...selectionIncomplete, stop_reason: 'cancelled', outcomes: [{ ...selectionIncomplete.outcomes[0], reason: 'cancelled' }],
    })))
    open(`/foundation-selections/${selectionIncomplete.selection_id}`)
    expect(await screen.findAllByText('Запрос отменён')).toHaveLength(2)
    expect(screen.queryByRole('link', { name: 'Открыть выбранный расчёт' })).toBeNull()
  })

})

import { fireEvent, render, screen } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { MemoryRouter } from 'react-router'
import { describe, expect, it, vi } from 'vitest'
import { createApi, unwrap } from '@/api/client'
import { useRequest } from '@/api/useRequest'
import { I18nProvider } from '@/i18n/I18nProvider'
import { server } from '@/mocks/server'
import { expectNoA11yViolations } from '@/test/axe'
import { ErrorState, LoadingState, NotFoundState } from './RequestStates'

const api = createApi({ baseUrl: 'http://test.local' })
const loadTypes = () => unwrap(api.GET('/calculation-types'))

function Types() {
  const { state, retry } = useRequest(loadTypes)
  if (state.status === 'loading') return <LoadingState />
  if (state.status === 'error') return <ErrorState error={state.error} onRetry={retry} />
  return <p>types: {state.data.length}</p>
}

function renderWithShell(node: React.ReactNode) {
  return render(
    <MemoryRouter>
      <I18nProvider>{node}</I18nProvider>
    </MemoryRouter>,
  )
}

function failing(status: number, code: string, message: string) {
  let calls = 0
  server.use(
    http.get('*/calculation-types', () => {
      calls += 1
      return HttpResponse.json({ code, message }, { status })
    }),
  )
  return () => calls
}

describe('request states', () => {
  it('shows the loading state, then the data', async () => {
    renderWithShell(<Types />)

    expect(screen.getByRole('status')).toHaveTextContent('Загрузка…')
    expect(await screen.findByText('types: 3')).toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('shows a 503 as unavailable, with its code and message, and a retry', async () => {
    failing(503, 'parameter_source_unavailable', 'Parameter source is not configured')
    renderWithShell(<Types />)

    const alert = await screen.findByRole('alert')

    expect(alert).toHaveTextContent('Расчёт сейчас недоступен.')
    expect(alert).toHaveTextContent('Код ошибки: parameter_source_unavailable')
    expect(alert).toHaveTextContent('Сообщение сервера: Parameter source is not configured')
    expect(screen.getByRole('button', { name: 'Повторить' })).toBeInTheDocument()
    await expectNoA11yViolations(alert)
  })

  it('shows another error as a failed request with its code', async () => {
    failing(500, 'internal_error', 'Boom')
    renderWithShell(<Types />)

    const alert = await screen.findByRole('alert')

    expect(alert).toHaveTextContent('Не удалось выполнить запрос.')
    expect(alert).toHaveTextContent('internal_error')
  })

  it('shows an unreachable backend as unavailable, without a code', async () => {
    server.use(http.get('*/calculation-types', () => HttpResponse.error()))
    renderWithShell(<Types />)

    const alert = await screen.findByRole('alert')

    expect(alert).toHaveTextContent('Расчёт сейчас недоступен.')
    expect(alert).not.toHaveTextContent('Код ошибки')
  })

  it('repeats the same request on retry and shows the data when it succeeds', async () => {
    const requests: string[] = []
    let healthy = false
    server.use(
      http.get('*/calculation-types', ({ request }) => {
        requests.push(request.url)
        return healthy
          ? HttpResponse.json([])
          : HttpResponse.json({ code: 'parameter_source_unavailable', message: 'x' }, { status: 503 })
      }),
    )
    renderWithShell(<Types />)
    await screen.findByRole('alert')

    healthy = true
    fireEvent.click(screen.getByRole('button', { name: 'Повторить' }))

    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(await screen.findByText('types: 0')).toBeInTheDocument()
    expect(requests).toHaveLength(2)
    expect(requests[1]).toBe(requests[0])
  })

  it('ignores the answer that arrives after the screen has gone', async () => {
    let answered = false
    server.use(
      http.get('*/calculation-types', async () => {
        await new Promise((resolve) => setTimeout(resolve, 20))
        answered = true
        return HttpResponse.json([])
      }),
    )
    const { unmount } = renderWithShell(<Types />)

    unmount()
    await vi.waitFor(() => expect(answered).toBe(true))

    expect(screen.queryByText('types: 0')).not.toBeInTheDocument()
  })

  it('shows the not found state of a page and of a result with a link to type selection', () => {
    const { unmount } = renderWithShell(<NotFoundState />)
    expect(screen.getByRole('heading', { name: 'Страница не найдена' })).toBeInTheDocument()
    unmount()

    renderWithShell(<NotFoundState subject="result" />)
    expect(screen.getByRole('heading', { name: 'Результат не найден' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'К выбору типа расчёта' })).toHaveAttribute('href', '/')
  })

  it('reads out the code and the requested address of a page that is not found', () => {
    renderWithShell(<NotFoundState />)
    const facts = [...document.querySelectorAll('dl > dt')].map((term) => [term.textContent, term.nextElementSibling?.textContent])

    expect(facts).toEqual([
      ['Код', '404'],
      ['Адрес', '/'],
    ])
  })

  it('frames an error with a thin rule on every side, not a coloured left edge', () => {
    renderWithShell(<ErrorState error={{ kind: 'network' }} onRetry={() => undefined} />)

    expect(screen.getByRole('alert').className).not.toMatch(/border-l-\d/)
    expect(screen.getByRole('alert').className).toContain('border-destructive')
  })

  it('shows the loading state with a mark hidden from assistive technology', () => {
    renderWithShell(<LoadingState />)

    expect(screen.getByRole('status')).toHaveTextContent('Загрузка…')
    expect(screen.getByRole('status').querySelector('svg')).toHaveAttribute('aria-hidden', 'true')
  })
})

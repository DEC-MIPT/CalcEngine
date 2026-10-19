import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { PASS_ID } from '@/mocks/fixtures'
import { server } from '@/mocks/server'
import { routes } from '@/routes'

const ENTERED = '987654.321'
const ECHO = 'ECHOED-INPUT-MARK'
const TRACE = 'TRACEBACK-MARK File "engine.py", line 7'
const BODY_ONLY = 'BODY-ONLY-FIELD-MARK'

const levels = ['log', 'info', 'warn', 'error', 'debug', 'trace'] as const

function spyOnConsole() {
  const spies = levels.map((level) => vi.spyOn(console, level).mockImplementation(() => {}))
  return () => spies.flatMap((spy) => spy.mock.calls).map((call) => call.map(String).join(' ')).join('\n')
}

function leaked(text: string) {
  return [ENTERED, ECHO, TRACE, BODY_ONLY, '"code"'].filter((mark) => text.includes(mark))
}

function stackLines(text: string) {
  return /\n\s+at\s+\S+/.test(text) || /Traceback|TypeError|ReferenceError/.test(text)
}

function body(code: string, extra: Record<string, unknown> = {}) {
  return { code, message: 'A message for the person.', debug: BODY_ONLY, traceback: TRACE, ...extra }
}

async function submitPilotForm() {
  render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: ['/calculations/new?type=foundations_shallow_r'] })} />)
  await screen.findByRole('button', { name: 'Рассчитать' })
  const values = { b: '2', d_1: '1.5', d_b: '0', gamma_II: '18', gamma_II_prime: '18', c_II: '10', phi_II: '20', p: ENTERED }
  for (const [name, value] of Object.entries(values)) {
    fireEvent.change(document.getElementById(`field-${name}`)!, { target: { value } })
  }
  fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))
}

afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
})

describe('no entered value, response body or stack trace in the console or on screen (4.5)', () => {
  const scenarios: [string, () => Promise<void>][] = [
    [
      '422',
      async () => {
        server.use(
          http.post('*/calculations', () =>
            HttpResponse.json(
              body('invalid_input', {
                fields: [{ location: ['body', 'inputs', 'p'], message: 'p does not fit', input: ECHO, ctx: { given: ENTERED } }],
              }),
              { status: 422 },
            ),
          ),
        )
        await submitPilotForm()
        await screen.findByText('p does not fit')
      },
    ],
    [
      '404',
      async () => {
        server.use(http.get('*/calculations/:id', () => HttpResponse.json(body('not_found'), { status: 404 })))
        render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: [`/calculations/${PASS_ID}`] })} />)
        await screen.findByRole('heading', { name: 'Результат не найден' })
      },
    ],
    [
      '503',
      async () => {
        server.use(http.post('*/calculations', () => HttpResponse.json(body('parameter_source_unavailable'), { status: 503 })))
        await submitPilotForm()
        await screen.findByRole('alert')
      },
    ],
    [
      'network failure',
      async () => {
        server.use(http.post('*/calculations', () => HttpResponse.error()))
        await submitPilotForm()
        await screen.findByRole('alert')
      },
    ],
  ]

  it.each(scenarios)('keeps them out during a %s', async (_name, run) => {
    const consoleText = spyOnConsole()

    await run()

    const screenText = document.body.textContent
    expect(leaked(consoleText())).toEqual([])
    expect(stackLines(consoleText())).toBe(false)
    expect(leaked(screenText).filter((mark) => mark !== ENTERED)).toEqual([])
    expect(stackLines(screenText)).toBe(false)
  })
})

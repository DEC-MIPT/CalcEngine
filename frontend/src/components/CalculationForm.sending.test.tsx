import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it, vi } from 'vitest'
import type { components } from '@/api/schema'
import { DraftProvider } from '@/form/DraftProvider'
import type { SendingStage } from '@/form/useSendingHints'
import { I18nProvider } from '@/i18n/I18nProvider'
import type { Language } from '@/i18n/dictionary'
import { calculationTypes, passEnvelope } from '@/mocks/fixtures'
import { server } from '@/mocks/server'
import { expectNoA11yViolations } from '@/test/axe'
import { CalculationForm } from './CalculationForm'

const forced = vi.hoisted(() => ({ stage: null as string | null }))

vi.mock('@/form/useSendingHints', async (importOriginal) => {
  const original = await importOriginal<typeof import('@/form/useSendingHints')>()
  return {
    ...original,
    useSendingHints: (active: boolean) => {
      const real = original.useSendingHints(active)
      return forced.stage && active ? (forced.stage as SendingStage) : real
    },
  }
})

type CalculationType = components['schemas']['CalculationTypeView']
const [pilot] = calculationTypes as unknown as CalculationType[]

const values: Record<string, string> = { b: '2', d_1: '1.5', d_b: '0', gamma_II: '18', gamma_II_prime: '18', c_II: '10', phi_II: '20', p: '100' }

function open(language: Language = 'ru') {
  const router = createMemoryRouter(
    [
      {
        path: '/calculations/new',
        element: (
          <I18nProvider initialLanguage={language}>
            <DraftProvider>
              <CalculationForm type={pilot} />
            </DraftProvider>
          </I18nProvider>
        ),
      },
      { path: '/calculations/:id', element: <p>opened</p> },
    ],
    { initialEntries: ['/calculations/new'] },
  )
  return render(<RouterProvider router={router} />)
}

const field = (name: string) => document.getElementById(`field-${name}`) as HTMLInputElement

function fill() {
  for (const [name, value] of Object.entries(values)) fireEvent.change(field(name), { target: { value } })
}

function hold() {
  let release = () => {}
  const pending = new Promise<void>((resolve) => {
    release = resolve
  })
  const seen: unknown[] = []
  server.use(
    http.post('*/calculations', async ({ request }) => {
      seen.push(await request.json())
      await pending
      return HttpResponse.json(passEnvelope, { status: 201 })
    }),
  )
  return { release, seen }
}

const submitButton = () => screen.getByRole('button', { name: /Рассчитать|Расчёт…/ })

describe('CalculationForm: the request in progress (9.5)', () => {
  it('locks the fields, keeps their values readable, and shows the rule and a status text', async () => {
    forced.stage = null
    const { release } = hold()
    const { container } = open()
    fill()

    fireEvent.click(submitButton())

    expect(await screen.findByText('Расчёт выполняется…')).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent('Расчёт выполняется…')
    for (const input of screen.getAllByRole('textbox')) expect(input).toHaveAttribute('readonly')
    for (const select of screen.getAllByRole('combobox')) expect(select).toBeDisabled()
    expect(field('b').value).toBe('2')
    expect(container.querySelector('.send-rule')).not.toBeNull()
    await expectNoA11yViolations(container)
    release()
    await waitFor(() => expect(screen.queryByText('Расчёт выполняется…')).not.toBeInTheDocument())
  })

  it('sends one request when the form is submitted twice, by Enter in a field too', async () => {
    forced.stage = null
    const { release, seen } = hold()
    open()
    fill()

    fireEvent.click(submitButton())
    await screen.findByText('Расчёт выполняется…')
    fireEvent.submit(field('b').form!)
    fireEvent.submit(field('p').form!)
    release()

    await waitFor(() => expect(screen.getByText('opened')).toBeInTheDocument())
    expect(seen).toHaveLength(1)
  })

  it('unlocks the fields with their values after a 503 and shows the error', async () => {
    forced.stage = null
    server.use(
      http.post('*/calculations', () =>
        HttpResponse.json({ code: 'parameter_source_unavailable', message: 'x' }, { status: 503 }),
      ),
    )
    open()
    fill()

    fireEvent.click(submitButton())

    expect(await screen.findByRole('alert')).toBeInTheDocument()
    for (const input of screen.getAllByRole('textbox')) expect(input).not.toHaveAttribute('readonly')
    for (const select of screen.getAllByRole('combobox')) expect(select).toBeEnabled()
    expect(field('b').value).toBe('2')
    expect(screen.getByRole('status')).toHaveTextContent('')
  })

  it.each([
    ['slow', 'ru', 'Сервер считает…'],
    ['longer', 'ru', 'Дольше обычного. Введённые данные сохранены.'],
    ['slow', 'en', 'The server is calculating…'],
    ['longer', 'en', 'This takes longer than usual. The entered data is kept.'],
  ] as const)('shows the %s message in %s', async (stage, language, text) => {
    forced.stage = stage
    const { release } = hold()
    open(language)
    fill()

    fireEvent.click(screen.getByRole('button', { name: language === 'ru' ? 'Рассчитать' : 'Calculate' }))

    expect(await screen.findByText(text)).toBeInTheDocument()
    release()
    forced.stage = null
  })
})

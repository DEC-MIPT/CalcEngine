import { fireEvent, render, screen } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, it } from 'vitest'
import { FAIL_ID, PASS_ID, REFUSED_ID, WARNING_ID } from '@/mocks/fixtures'
import { serviceUnavailable } from '@/mocks/handlers'
import { server } from '@/mocks/server'
import { routes } from '@/routes'
import { expectNoA11yViolations } from './axe'

const FORM = '/calculations/new?type=foundations_shallow_r'
const INPUTS = { b: '2', d_1: '1.5', d_b: '0', gamma_II: '18', gamma_II_prime: '18', c_II: '10', phi_II: '20', p: '100' }

function open(address: string) {
  return render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: [address] })} />)
}

function unavailable(path: string, method: 'get' | 'post' = 'get') {
  server.use(
    http[method](path, () => HttpResponse.json({ code: 'database_unavailable', message: 'x' }, { status: 503 })),
  )
}

function unreachable(path: string) {
  server.use(http.get(path, () => HttpResponse.error()))
}

function fillForm() {
  for (const [name, value] of Object.entries(INPUTS)) {
    fireEvent.change(document.getElementById(`field-${name}`)!, { target: { value } })
  }
}

describe('axe over the four screens in their states (8.5)', () => {
  describe('type selection', () => {
    it('loading and loaded', async () => {
      const { container } = open('/')
      await expectNoA11yViolations(container)
      await screen.findByRole('link', { name: /Расчётное сопротивление грунта/ })
      await expectNoA11yViolations(container)
    })

    it('503 and network failure', async () => {
      unavailable('*/calculation-types')
      const first = open('/')
      await screen.findByText('database_unavailable')
      await expectNoA11yViolations(first.container)
      first.unmount()

      unreachable('*/calculation-types')
      const second = open('/')
      await screen.findByRole('button', { name: /Повторить/ })
      await expectNoA11yViolations(second.container)
    })
  })

  describe('input form', () => {
    it('loading, loaded and the client marks', async () => {
      const { container } = open(FORM)
      await expectNoA11yViolations(container)
      const submit = await screen.findByRole('button', { name: 'Рассчитать' })
      await expectNoA11yViolations(container)

      fireEvent.click(submit)
      await screen.findAllByText('Введите значение.')
      await expectNoA11yViolations(container)
    })

    it('a server 422 and a 503 on submit', async () => {
      server.use(
        http.post('*/calculations', () =>
          HttpResponse.json(
            {
              code: 'invalid_input',
              message: 'The inputs do not fit the calculation type.',
              fields: [
                { location: ['body', 'inputs', 'b'], message: 'Value out of range.' },
                { location: ['body'], message: 'Something else.' },
              ],
            },
            { status: 422 },
          ),
        ),
      )
      const first = open(FORM)
      await screen.findByRole('button', { name: 'Рассчитать' })
      fillForm()
      fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))
      await screen.findByText('Value out of range.')
      await expectNoA11yViolations(first.container)
      first.unmount()

      server.use(serviceUnavailable)
      const second = open(FORM)
      await screen.findByRole('button', { name: 'Рассчитать' })
      fillForm()
      fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))
      await screen.findByText('parameter_source_unavailable')
      await expectNoA11yViolations(second.container)
    })

    it('503 of the listing', async () => {
      unavailable('*/calculation-types')
      const { container } = open(FORM)
      await screen.findByText('database_unavailable')
      await expectNoA11yViolations(container)
    })
  })

  describe('result', () => {
    it.each([
      ['pass', PASS_ID, /^Проверка выполнена$/],
      ['fail', FAIL_ID, /^Проверка не выполнена$/],
      ['warning', WARNING_ID, /^Предупреждение: входное значение вне проверенного диапазона$/],
      ['refusal', REFUSED_ID, /^Расчёт не выполнен: входное значение вне диапазона метода$/],
    ])('%s', async (_, id, region) => {
      const { container } = open(`/calculations/${id}`)
      await expectNoA11yViolations(container)
      await screen.findByRole('region', { name: region })
      await expectNoA11yViolations(container)
    })

    it('not found, 503 and network failure', async () => {
      const first = open('/calculations/nobody')
      await screen.findByRole('heading', { name: 'Результат не найден' })
      await expectNoA11yViolations(first.container)
      first.unmount()

      unavailable('*/calculations/:id')
      const second = open(`/calculations/${PASS_ID}`)
      await screen.findByText('database_unavailable')
      await expectNoA11yViolations(second.container)
      second.unmount()

      unreachable('*/calculations/:id')
      const third = open(`/calculations/${PASS_ID}`)
      await screen.findByRole('button', { name: /Повторить/ })
      await expectNoA11yViolations(third.container)
    })
  })

  describe('report request', () => {
    it.each([
      ['a pass', PASS_ID],
      ['a refusal', REFUSED_ID],
    ])('empty and with the client marks for %s', async (_, id) => {
      const { container } = open(`/calculations/${id}/report`)
      await expectNoA11yViolations(container)
      fireEvent.click(await screen.findByRole('button', { name: /Сформировать отчёт/ }))
      await screen.findAllByText('Заполните поле.')
      await expectNoA11yViolations(container)
    })

    it.each([
      ['503', 503, { code: 'database_unavailable', message: 'x' }],
      [
        '422',
        422,
        {
          code: 'validation_error',
          message: 'The request does not match its schema.',
          fields: [
            { location: ['body', 'title', 'designation'], message: 'Too long.' },
            { location: ['body'], message: 'Something else.' },
          ],
        },
      ],
    ])('a server %s on the report request', async (_, status, body) => {
      server.use(http.post('*/calculations/:id/report', () => HttpResponse.json(body, { status })))
      const { container } = open(`/calculations/${PASS_ID}/report`)
      for (const [label, value] of Object.entries({
        'Обозначение документа': 'ДЕК-1',
        'Наименование документа': 'Расчёт',
        Организация: 'ООО',
        'Разработал: Фамилия': 'Иванов',
        'Разработал: Дата': '2026-10-07',
        'Нормоконтроль: Фамилия': 'Петрова',
        'Нормоконтроль: Дата': '2026-10-08',
      })) {
        fireEvent.change(await screen.findByLabelText(label), { target: { value } })
      }
      fireEvent.click(screen.getByRole('button', { name: /Сформировать отчёт/ }))
      await screen.findByRole('alert')
      await expectNoA11yViolations(container)
    })
  })
})

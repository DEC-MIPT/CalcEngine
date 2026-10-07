import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { PASS_ID, REFUSED_ID } from '@/mocks/fixtures'
import { server } from '@/mocks/server'
import { routes } from '@/routes'
import { expectNoA11yViolations } from '@/test/axe'

const SUBMIT = /Скачать отчёт/
const TITLE = {
  'Обозначение документа': 'ДЕК-2026-001-РР',
  'Наименование документа': 'Расчёт сопротивления грунта',
  Организация: 'ООО «Проект»',
}
const SIGNATURES = {
  'Разработал: Фамилия': 'Иванов',
  'Разработал: Дата': '2026-10-07',
  'Нормоконтроль: Фамилия': 'Петрова',
  'Нормоконтроль: Дата': '2026-10-08',
}

let saved: { href: string; download: string }[]
let bodies: unknown[]

beforeEach(() => {
  saved = []
  bodies = []
  Object.assign(URL, { createObjectURL: vi.fn(() => 'blob:report'), revokeObjectURL: vi.fn() })
  vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(function (this: HTMLAnchorElement) {
    saved.push({ href: this.href, download: this.download })
  })
  server.events.on('request:start', async ({ request }) => {
    if (request.method === 'POST') bodies.push(await request.clone().json())
  })
})

afterEach(() => {
  server.events.removeAllListeners('request:start')
  vi.restoreAllMocks()
  Reflect.deleteProperty(URL, 'createObjectURL')
  Reflect.deleteProperty(URL, 'revokeObjectURL')
})

function open(id = PASS_ID) {
  const router = createMemoryRouter(routes, { initialEntries: [`/calculations/${id}/report`] })
  return { router, ...render(<RouterProvider router={router} />) }
}

function fill(values: Record<string, string>) {
  for (const [label, value] of Object.entries(values)) {
    fireEvent.change(screen.getByLabelText(label), { target: { value } })
  }
}

const submit = () => fireEvent.click(screen.getByRole('button', { name: SUBMIT }))
const messageOf = (label: string | RegExp) => {
  const field = screen.getByLabelText(label)
  return field.getAttribute('aria-invalid') ? document.getElementById(field.getAttribute('aria-describedby')!)?.textContent : null
}

describe('report form: title block and switch (7.1a)', () => {
  it('requires the designation, the document name and the organization, not the documentation kind', async () => {
    open()

    submit()

    expect(messageOf('Обозначение документа')).toBe('Заполните поле.')
    expect(messageOf('Наименование документа')).toBe('Заполните поле.')
    expect(messageOf('Организация')).toBe('Заполните поле.')
    expect(messageOf(/^Вид документации · необязательно$/)).toBeNull()
    expect(screen.getByLabelText('Обозначение документа')).toHaveFocus()
    expect(screen.getByText(/Полей с ошибкой: 7/)).toBeInTheDocument()
    await new Promise((resolve) => setTimeout(resolve, 20))
    expect(bodies).toEqual([])
  })

  it('hides the signatories when the block is off and sends none of them', async () => {
    open()
    fill(SIGNATURES)
    fireEvent.click(screen.getByRole('switch', { name: 'Заполнить блок подписей' }))
    fill(TITLE)

    expect(screen.getByRole('switch')).not.toBeChecked()
    expect(document.querySelector('[data-signatories]')).toBeNull()
    expect(screen.getByText(/печатаются без фамилий и дат/)).toBeInTheDocument()
    submit()

    await screen.findByRole('status')
    expect(bodies).toEqual([
      {
        title: { designation: 'ДЕК-2026-001-РР', document_name: 'Расчёт сопротивления грунта', documentation_kind: '', organization: 'ООО «Проект»' },
        signature_block: false,
      },
    ])
  })

  it('removes the mark of a field as soon as it is edited', () => {
    open()
    submit()

    fill({ 'Обозначение документа': 'Д' })

    expect(messageOf('Обозначение документа')).toBeNull()
    expect(messageOf('Организация')).toBe('Заполните поле.')
  })

  it('has no accessibility violations, empty and with the marks', async () => {
    const { container } = open()
    await expectNoA11yViolations(container)

    submit()
    await expectNoA11yViolations(container)
  })
})

describe('report form: signatories (7.1b)', () => {
  it.each([
    ['Разработал: Дата', 'Заполните поле.'],
    ['Нормоконтроль: Фамилия', 'Заполните поле.'],
  ])('marks an empty %s and sends nothing', async (label, message) => {
    open()
    fill({ ...TITLE, ...SIGNATURES, [label]: '' })

    submit()

    expect(messageOf(label)).toBe(message)
    await new Promise((resolve) => setTimeout(resolve, 20))
    expect(bodies).toEqual([])
  })

  it('treats a blank surname as empty', () => {
    open()
    fill({ ...TITLE, ...SIGNATURES, 'Разработал: Фамилия': '   ' })

    submit()

    expect(messageOf('Разработал: Фамилия')).toBe('Заполните поле.')
  })

  it('asks for both parts of a checker given in part', () => {
    open()
    fill({ ...TITLE, ...SIGNATURES, 'Проверил: Фамилия': 'Сидоров' })

    submit()

    expect(messageOf('Проверил: Дата')).toBe('Для проверяющего нужны и фамилия, и дата.')
    expect(messageOf('Проверил: Фамилия')).toBeNull()
  })

  it('sends a complete checker and leaves out an empty one', async () => {
    open()
    fill({ ...TITLE, ...SIGNATURES })
    submit()
    await screen.findByRole('status')
    fill({ 'Проверил: Фамилия': 'Сидоров', 'Проверил: Дата': '2026-10-09' })
    submit()

    await waitFor(() => expect(bodies).toHaveLength(2))
    expect(bodies[0]).not.toHaveProperty('checker')
    expect(bodies[1]).toMatchObject({
      signature_block: true,
      developer: { surname: 'Иванов', date: '2026-10-07' },
      normative_control: { surname: 'Петрова', date: '2026-10-08' },
      checker: { surname: 'Сидоров', date: '2026-10-09' },
    })
  })
})

describe('report download and errors (7.2)', () => {
  it('saves the file under the name the response gives and stays on the report screen', async () => {
    const { router } = open()
    fill({ ...TITLE, ...SIGNATURES })

    submit()

    expect(await screen.findByRole('status')).toHaveTextContent('Отчёт сохранён: report.docx')
    expect(saved).toEqual([{ href: 'blob:report', download: 'report.docx' }])
    expect(router.state.location.pathname).toBe(`/calculations/${PASS_ID}/report`)
  })

  it('falls back to a name with the result id when the response gives none', async () => {
    server.use(
      http.post('*/calculations/:id/report', () => new HttpResponse(new Uint8Array([1]), { headers: { 'Content-Type': 'application/octet-stream' } })),
    )
    open()
    fill({ ...TITLE, ...SIGNATURES })

    submit()

    await screen.findByRole('status')
    expect(saved[0].download).toBe(`dec-report-${PASS_ID}.docx`)
  })

  it('downloads the report of a refused result as any other, with no error', async () => {
    open(REFUSED_ID)
    fill({ ...TITLE, ...SIGNATURES })

    submit()

    await screen.findByRole('status')
    expect(saved).toHaveLength(1)
    expect(screen.queryByRole('alert')).toBeNull()
  })

  it('marks the field a 422 names, shows an entry with no field above the form, and saves no file', async () => {
    server.use(
      http.post('*/calculations/:id/report', () =>
        HttpResponse.json(
          {
            code: 'validation_error',
            message: 'The request does not match its schema.',
            fields: [
              { location: ['body', 'title', 'designation'], message: 'String should have at most 123 characters' },
              { location: ['body'], message: 'the signature block needs the surname and the date of developer' },
              { location: ['body', 'signature_block'], message: 'Input should be a valid boolean' },
            ],
          },
          { status: 422 },
        ),
      ),
    )
    open()
    fill({ ...TITLE, ...SIGNATURES })

    submit()

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('Запрос отклонён')
    expect(within(alert).getByText('the signature block needs the surname and the date of developer')).toBeInTheDocument()
    expect(messageOf('Обозначение документа')).toBe('String should have at most 123 characters')
    expect(screen.getByText('Input should be a valid boolean')).toBeInTheDocument()
    expect(saved).toEqual([])
  })

  it('shows the message of a 422 that names no field', async () => {
    server.use(
      http.post('*/calculations/:id/report', () =>
        HttpResponse.json({ code: 'validation_error', message: 'The request does not match its schema.', fields: [] }, { status: 422 }),
      ),
    )
    open()
    fill({ ...TITLE, ...SIGNATURES })

    submit()

    expect(await screen.findByRole('alert')).toHaveTextContent('The request does not match its schema.')
  })

  it.each([
    ['404', 'nobody', undefined, 'not_found'],
    ['409', PASS_ID, { status: 409, code: 'calculation_type_not_registered', message: "The calculation type 'x' is not registered." }, 'calculation_type_not_registered'],
  ] as const)('shows a %s with its message and code, saves no file, and retries', async (_status, id, error, code) => {
    if (error) {
      server.use(http.post('*/calculations/:id/report', () => HttpResponse.json({ code: error.code, message: error.message }, { status: error.status })))
    }
    open(id)
    fill({ ...TITLE, ...SIGNATURES })

    submit()

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('Не удалось выполнить запрос.')
    expect(alert).toHaveTextContent(code)
    expect(saved).toEqual([])
    fireEvent.click(within(alert).getByRole('button', { name: 'Повторить' }))
    await waitFor(() => expect(bodies).toHaveLength(2))
  })

  it('shows an unreachable backend as unavailable', async () => {
    server.use(http.post('*/calculations/:id/report', () => HttpResponse.error()))
    open()
    fill({ ...TITLE, ...SIGNATURES })

    submit()

    expect(await screen.findByRole('alert')).toHaveTextContent('Расчёт сейчас недоступен.')
    expect(saved).toEqual([])
  })
})

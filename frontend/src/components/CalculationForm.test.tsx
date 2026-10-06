import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import type { components } from '@/api/schema'
import { I18nProvider } from '@/i18n/I18nProvider'
import type { Language } from '@/i18n/dictionary'
import { calculationTypes, FAIL_ID, failEnvelope, passEnvelope } from '@/mocks/fixtures'
import { server } from '@/mocks/server'
import { expectNoA11yViolations } from '@/test/axe'
import { CalculationForm } from './CalculationForm'

type CalculationType = components['schemas']['CalculationTypeView']

const [pilot] = calculationTypes as unknown as CalculationType[]
const label = (name: string) => pilot.inputs.find((input) => input.name === name)!.label.ru

const synthetic: CalculationType = {
  name: 'synthetic',
  outputs: [],
  inputs: [
    {
      name: 'x',
      base_unit: 'm',
      dimension: 'length',
      units: ['m', 'mm'],
      label: { ru: 'Длина икс', en: 'Length x' },
      symbol: 'x',
      hint: { ru: 'Подсказка икс', en: 'Hint x' },
      whole_values_only: false,
    },
    {
      name: 'n',
      base_unit: 'deg',
      dimension: 'angle',
      units: ['rad', 'deg'],
      label: { ru: 'Только русский текст' },
      symbol: 'n',
      hint: null,
      whole_values_only: true,
    },
  ],
}

const other: CalculationType = {
  name: 'other',
  outputs: [],
  inputs: [
    {
      name: 'q',
      base_unit: 'kPa',
      dimension: 'pressure',
      units: ['kPa'],
      label: { ru: 'Давление кью' },
      symbol: 'q',
      hint: null,
      whole_values_only: false,
    },
  ],
}

function open(type: CalculationType, language: Language = 'ru') {
  const router = createMemoryRouter(
    [
      {
        path: '/calculations/new',
        element: (
          <I18nProvider initialLanguage={language}>
            <CalculationForm type={type} />
          </I18nProvider>
        ),
      },
      { path: '/calculations/:id', element: <p>opened</p> },
    ],
    { initialEntries: ['/calculations/new'] },
  )
  return { router, ...render(<RouterProvider router={router} />) }
}

function type(name: string, text: string) {
  fireEvent.change(screen.getByLabelText(name), { target: { value: text } })
}

const pilotValues: Record<string, string> = {
  b: '2',
  d_1: '1.5',
  d_b: '0',
  gamma_II: '18',
  gamma_II_prime: '18',
  c_II: '10',
  phi_II: '20',
  p: '100',
}

function fillPilot(overrides: Record<string, string> = {}) {
  for (const [name, text] of Object.entries({ ...pilotValues, ...overrides })) {
    type(label(name), text)
  }
}

const submit = () => fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))

function recordRequests(response: () => Response = () => HttpResponse.json(passEnvelope, { status: 201 })) {
  const bodies: components['schemas']['CalculationRequest'][] = []
  server.use(
    http.post('*/calculations', async ({ request }) => {
      bodies.push((await request.json()) as components['schemas']['CalculationRequest'])
      return response()
    }),
  )
  return bodies
}

describe('CalculationForm: fields from the contract (5.1a)', () => {
  it('shows one field per declared input in the declared order, with label, symbol and hint', () => {
    open(synthetic)

    const fields = screen.getAllByRole('textbox')
    expect(fields.map((field) => field.getAttribute('name'))).toEqual(['x', 'n'])
    const first = fields[0]
    expect(first).toHaveAccessibleName('Длина икс')
    expect(first).toHaveAccessibleDescription('Подсказка икс')
    expect(first.closest('div.grid')?.querySelector('svg')).not.toBeNull()
  })

  it('shows the fields of another type with the same component', () => {
    const { unmount } = open(synthetic)
    unmount()
    open(other)

    expect(screen.getAllByRole('textbox').map((field) => field.getAttribute('name'))).toEqual(['q'])
    expect(screen.queryByLabelText('Длина икс')).not.toBeInTheDocument()
  })

  it('shows the English texts of the listing and falls back to Russian for a quantity without one', () => {
    open(synthetic, 'en')

    expect(screen.getByLabelText('Length x')).toHaveAccessibleDescription('Hint x')
    expect(screen.getByLabelText('Только русский текст')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Calculate' })).toBeInTheDocument()
  })

  it('has no accessibility violations', async () => {
    const { container } = open(pilot)

    await expectNoA11yViolations(container)
  })
})

describe('CalculationForm: unit choice (5.1b)', () => {
  it('offers only degrees for phi_II, as text and not as a choice, and every unit for b', () => {
    open(pilot)

    expect(screen.queryByRole('combobox', { name: new RegExp(label('phi_II')) })).not.toBeInTheDocument()
    const phi = screen.getByLabelText(label('phi_II')).parentElement!
    expect(phi).toHaveTextContent('°')
    expect(phi).not.toHaveTextContent('рад')
    const width = screen.getByRole('combobox', { name: new RegExp(label('b')) })
    expect(within(width).getAllByRole('option').map((option) => option.textContent)).toEqual(['м', 'см', 'мм'])
    expect(width).toHaveValue('m')
  })

  it('shows a type with one unit as text', () => {
    open(other)

    expect(screen.queryByRole('combobox')).not.toBeInTheDocument()
    expect(screen.getByLabelText('Давление кью').parentElement).toHaveTextContent('кПа')
  })

  it('shows the unit codes in English', () => {
    open(pilot, 'en')

    const width = screen.getByRole('combobox', { name: /Foundation base width/ })
    expect(within(width).getAllByRole('option').map((option) => option.textContent)).toEqual(['m', 'cm', 'mm'])
  })

  it('sends the chosen unit and the base unit of a fixed input', async () => {
    const bodies = recordRequests()
    open(pilot)
    fillPilot()

    fireEvent.change(screen.getByRole('combobox', { name: new RegExp(label('b')) }), {
      target: { value: 'cm' },
    })
    submit()

    await waitFor(() => expect(bodies).toHaveLength(1))
    expect(bodies[0].calculation_type).toBe('foundations_shallow_r')
    expect(bodies[0].inputs.b).toEqual({ value: 2, unit: 'cm' })
    expect(bodies[0].inputs.phi_II).toEqual({ value: 20, unit: 'deg' })
    expect(bodies[0].inputs.p).toEqual({ value: 100, unit: 'kPa' })
  })
})

describe('CalculationForm: client checks (5.2)', () => {
  it('marks empty fields, focuses the first, and sends no request', async () => {
    const bodies = recordRequests()
    open(pilot)

    submit()

    const field = screen.getByLabelText(label('b'))
    expect(field).toHaveAttribute('aria-invalid', 'true')
    expect(field).toHaveAccessibleDescription('Введите значение.')
    expect(field).toHaveFocus()
    expect(screen.getAllByText('Введите значение.')).toHaveLength(pilot.inputs.length)
    expect(bodies).toHaveLength(0)
  })

  it.each([
    ['abc', 'Введите число.'],
    ['1e999', 'Число слишком велико.'],
  ])('rejects %j with its own message and keeps the value', (text, message) => {
    const bodies = recordRequests()
    open(pilot)
    fillPilot({ p: text })

    submit()

    const field = screen.getByLabelText(label('p'))
    expect(field).toHaveValue(text)
    expect(field).toHaveAccessibleDescription(message)
    expect(bodies).toHaveLength(0)
  })

  it('rejects 30.5 on a whole-values input with the rule, keeps the value and sends nothing', () => {
    const bodies = recordRequests()
    open(pilot)
    fillPilot({ phi_II: '30.5' })

    submit()

    const field = screen.getByLabelText(label('phi_II'))
    expect(field).toHaveValue('30.5')
    expect(field).toHaveAccessibleDescription(expect.stringContaining('целым'))
    expect(bodies).toHaveLength(0)
  })

  it.each(['30', '30.0', '30e0'])('accepts %j on a whole-values input and sends 30', async (text) => {
    const bodies = recordRequests()
    open(pilot)
    fillPilot({ phi_II: text })

    submit()

    await waitFor(() => expect(bodies).toHaveLength(1))
    expect(bodies[0].inputs.phi_II).toEqual({ value: 30, unit: 'deg' })
  })

  it('clears the mark of a field when it is edited', () => {
    open(pilot)
    submit()

    type(label('b'), '2')

    const field = screen.getByLabelText(label('b'))
    expect(field).not.toHaveAttribute('aria-invalid')
    expect(field).not.toHaveAccessibleDescription()
  })
})

describe('CalculationForm: server 422 (5.3)', () => {
  const rejected = (fields: { location: (string | number)[]; message: string }[]) => () =>
    HttpResponse.json({ code: 'invalid_input', message: 'The inputs do not fit.', fields }, { status: 422 })

  it('marks the one field that the body names and keeps every value', async () => {
    recordRequests(rejected([{ location: ['body', 'inputs', 'p'], message: 'p does not fit' }]))
    const { router } = open(pilot)
    fillPilot()

    submit()

    expect(await screen.findByText('p does not fit')).toBeInTheDocument()
    expect(screen.getByLabelText(label('p'))).toHaveAccessibleDescription('p does not fit')
    expect(screen.getByLabelText(label('b'))).toHaveValue('2')
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(router.state.location.pathname).toBe('/calculations/new')
  })

  it('marks two fields', async () => {
    recordRequests(
      rejected([
        { location: ['body', 'inputs', 'b'], message: 'b is wrong' },
        { location: ['body', 'inputs', 'd_1'], message: 'd_1 is wrong' },
      ]),
    )
    open(pilot)
    fillPilot()

    submit()

    expect(await screen.findByText('b is wrong')).toBeInTheDocument()
    expect(screen.getByText('d_1 is wrong')).toBeInTheDocument()
  })

  it('shows an entry that names no field above the form', async () => {
    recordRequests(rejected([{ location: ['body', 'calculation_type'], message: 'unknown type' }]))
    open(pilot)
    fillPilot()

    submit()

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('Запрос отклонён')
    expect(alert).toHaveTextContent('unknown type')
    expect(screen.getByLabelText(label('b'))).not.toHaveAttribute('aria-invalid')
  })

  it('shows the message of the body when it lists no field', async () => {
    recordRequests(rejected([]))
    open(pilot)
    fillPilot()

    submit()

    expect(await screen.findByRole('alert')).toHaveTextContent('The inputs do not fit.')
  })

  it('shows 503 with its code and retries the same request', async () => {
    let healthy = false
    const bodies = recordRequests(() =>
      healthy
        ? HttpResponse.json(passEnvelope, { status: 201 })
        : HttpResponse.json({ code: 'parameter_source_unavailable', message: 'down' }, { status: 503 }),
    )
    const { router } = open(pilot)
    fillPilot()

    submit()

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('parameter_source_unavailable')
    expect(screen.getByLabelText(label('b'))).toHaveValue('2')

    healthy = true
    fireEvent.click(within(alert).getByRole('button', { name: 'Повторить' }))

    await waitFor(() => expect(router.state.location.pathname).toBe(`/calculations/${passEnvelope.result_id}`))
    expect(bodies).toHaveLength(2)
    expect(bodies[1]).toEqual(bodies[0])
  })
})

describe('CalculationForm: values outside the method range (5.4)', () => {
  it('accepts an extreme value, sends it as entered and opens the stored result', async () => {
    const bodies = recordRequests(() => HttpResponse.json(failEnvelope, { status: 201 }))
    const { router } = open(pilot)
    fillPilot({ p: '1000000', phi_II: '89' })

    submit()

    await waitFor(() => expect(router.state.location.pathname).toBe(`/calculations/${FAIL_ID}`))
    expect(bodies[0].inputs.p).toEqual({ value: 1000000, unit: 'kPa' })
    expect(bodies[0].inputs.phi_II).toEqual({ value: 89, unit: 'deg' })
  })

  it('disables the button while the request is pending', async () => {
    let release = () => {}
    const pending = new Promise<void>((resolve) => {
      release = resolve
    })
    server.use(
      http.post('*/calculations', async () => {
        await pending
        return HttpResponse.json(passEnvelope, { status: 201 })
      }),
    )
    open(pilot)
    fillPilot()

    submit()

    expect(await screen.findByRole('button', { name: 'Расчёт…' })).toBeDisabled()
    release()
    await waitFor(() => expect(screen.queryByRole('button', { name: 'Расчёт…' })).not.toBeInTheDocument())
  })
})

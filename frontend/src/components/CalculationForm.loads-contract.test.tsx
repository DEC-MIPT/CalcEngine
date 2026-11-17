import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, Outlet, RouterProvider } from 'react-router'
import { afterEach, describe, expect, it, vi } from 'vitest'
import type { components } from '@/api/schema'
import { DraftProvider } from '@/form/DraftProvider'
import { I18nProvider } from '@/i18n/I18nProvider'
import {
  LOADS_TYPE,
  loadsBiaxialJson,
  loadsCalculationType,
  loadsCentralInputs,
} from '@/mocks/fixtures'
import { server } from '@/mocks/server'
import { CalculationForm } from './CalculationForm'

type Request = components['schemas']['CalculationRequest']
const label = (name: string) => loadsCalculationType.inputs.find((input) => input.name === name)!.label.ru
const field = (name: string) => screen.getByRole('textbox', { name: label(name) })
const unit = (name: string) => screen.getByRole('combobox', { name: `Единица: ${label(name)}` })
const rawInputs = Object.fromEntries(Object.entries(loadsCentralInputs).map(([name, quantity]) => [name, String(quantity.value)]))

afterEach(() => vi.unstubAllGlobals())

function open() {
  vi.stubGlobal('matchMedia', () => ({ matches: true }))
  const router = createMemoryRouter([
    {
      element: <I18nProvider initialLanguage="ru"><DraftProvider><Outlet /></DraftProvider></I18nProvider>,
      children: [
        { path: '/calculations/new', element: <CalculationForm type={loadsCalculationType} /> },
        { path: '/calculations/:id', element: <p>Stored result opened</p> },
      ],
    },
  ], { initialEntries: ['/calculations/new'] })
  return { router, ...render(<RouterProvider router={router} />) }
}

function fill(overrides: Record<string, string> = {}) {
  for (const [name, value] of Object.entries({ ...rawInputs, ...overrides })) {
    fireEvent.change(field(name), { target: { value } })
  }
}

function record(fields: string[] = [], success = false) {
  const requests: Request[] = []
  server.use(http.post('*/calculations', async ({ request }) => {
    requests.push(await request.json() as Request)
    return success
      ? new HttpResponse(loadsBiaxialJson, { status: 201, headers: { 'Content-Type': 'application/json' } })
      : HttpResponse.json({
        code: 'invalid_input', message: 'Request correction recorded by the test server.',
        fields: fields.map((name) => ({
          location: ['body', 'inputs', name], message: 'Outside the supported engineering domain.',
        })),
      }, { status: 422 })
  }))
  return requests
}

const submit = () => fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))

describe('loads form transport and correction contract', () => {
  it('renders exactly fifteen metadata fields in order with their actual hints and a named sign diagram', () => {
    open()
    expect(screen.getAllByRole('textbox').map((input) => input.getAttribute('name'))).toEqual([
      'b', 'd_1', 'd_b', 'gamma_II', 'gamma_II_prime', 'c_II', 'phi_II', 'l', 'h', 'd', 'N', 'Mx', 'My', 'Qx', 'Qy',
    ])
    for (const input of loadsCalculationType.inputs) {
      expect(field(input.name)).toHaveValue('')
      if (input.hint) expect(field(input.name)).toHaveAccessibleDescription(input.hint.ru)
    }
    expect(field('N')).toHaveAccessibleDescription(/Без собственного веса/)
    const guidance = screen.getByRole('region', { name: 'Схема направлений и знаков' })
    expect(within(guidance).getByRole('img', { name: /Прямоугольная подошва: вид сверху/ })).toBeInTheDocument()
    expect(guidance).toHaveTextContent('Mx_base = Mx + Qx·h')
    expect(guidance).toHaveTextContent('My_base = My + Qy·h')
    expect(guidance).toHaveTextContent('d_1')
  })

  it('sends signed moments and shears with their original chosen units without pre-adding weight', async () => {
    const requests = record([], true)
    const { router } = open()
    fill({ N: '+600000,0', Mx: '+40000,0', My: '-0,0300', Qx: '+20000', Qy: '-0,01500' })
    for (const [name, value] of [['N', 'N'], ['Mx', 'N*m'], ['My', 'MN*m'], ['Qx', 'N'], ['Qy', 'MN']]) {
      fireEvent.change(unit(name), { target: { value } })
    }
    submit()
    await waitFor(() => expect(requests).toHaveLength(1))
    expect(requests[0].calculation_type).toBe(LOADS_TYPE)
    expect(requests[0].inputs).toMatchObject({
      N: { value: 600000, unit: 'N' }, Mx: { value: 40000, unit: 'N*m' },
      My: { value: -0.03, unit: 'MN*m' }, Qx: { value: 20000, unit: 'N' }, Qy: { value: -0.015, unit: 'MN' },
    })
    expect(Object.keys(requests[0].inputs)).toHaveLength(15)
    await waitFor(() => expect(router.state.location.pathname).toMatch(/^\/calculations\/[\da-f-]+$/))
    expect(await screen.findByText('Stored result opened')).toBeInTheDocument()
  })

  it('keeps d, h and d_1 independent in both raw fields and the sent quantities', async () => {
    const requests = record(['d_1'])
    open()
    fill({ d: '2,75', h: '0', d_1: '1,125', N: '+600,00' })
    submit()
    await waitFor(() => expect(requests).toHaveLength(1))
    expect(requests[0].inputs).toMatchObject({
      d: { value: 2.75, unit: 'm' }, h: { value: 0, unit: 'm' }, d_1: { value: 1.125, unit: 'm' }, N: { value: 600, unit: 'kN' },
    })
    await waitFor(() => expect(field('d_1')).toHaveFocus())
    expect(field('d')).toHaveValue('2,75')
    expect(field('h')).toHaveValue('0')
    expect(field('d_1')).toHaveValue('1,125')
    expect(field('N')).toHaveValue('+600,00')
  })

  it.each(['20,5', '20.0000001'])('marks fractional metadata-whole angle %s without rounding or posting', async (value) => {
    const requests = record(['phi_II'])
    open()
    fill({ phi_II: value })
    submit()
    expect(field('phi_II')).toHaveAttribute('aria-invalid', 'true')
    expect(field('phi_II')).toHaveFocus()
    expect(field('phi_II')).toHaveValue(value)
    await Promise.resolve()
    expect(requests).toHaveLength(0)
  })

  it.each(['0', '45', '-1', '46'])('sends whole angle %s unchanged and leaves engineering range decisions to backend corrections', async (value) => {
    const requests = record(['phi_II'])
    open()
    fill({ phi_II: value })
    submit()
    await waitFor(() => expect(requests).toHaveLength(1))
    expect(requests[0].inputs.phi_II).toEqual({ value: Number(value), unit: 'deg' })
    await waitFor(() => expect(field('phi_II')).toHaveAttribute('aria-invalid', 'true'))
    expect(field('phi_II')).toHaveFocus()
    expect(field('phi_II')).toHaveValue(value)
    expect(screen.queryByRole('combobox', { name: `Единица: ${label('phi_II')}` })).toBeNull()
  })

  it('maps backend b/l corrections to the first named field without swapping sides or signed loads', async () => {
    const requests = record(['b', 'l'])
    open()
    fill({ b: '3000,001', l: '3', Mx: '-40,00', My: '+30,00', Qx: '-20', Qy: '+15' })
    fireEvent.change(unit('b'), { target: { value: 'mm' } })
    submit()
    await waitFor(() => expect(requests).toHaveLength(1))
    expect(requests[0].inputs).toMatchObject({
      b: { value: 3000.001, unit: 'mm' }, l: { value: 3, unit: 'm' },
      Mx: { value: -40, unit: 'kN*m' }, My: { value: 30, unit: 'kN*m' }, Qx: { value: -20, unit: 'kN' }, Qy: { value: 15, unit: 'kN' },
    })
    await waitFor(() => expect(field('b')).toHaveFocus())
    expect(field('b')).toHaveValue('3000,001')
    expect(field('l')).toHaveValue('3')
    expect(field('Mx')).toHaveValue('-40,00')
    expect(field('My')).toHaveValue('+30,00')
    expect(unit('b')).toHaveValue('mm')
    expect(field('b')).toHaveAttribute('aria-invalid', 'true')
    expect(field('l')).toHaveAttribute('aria-invalid', 'true')
  })
})

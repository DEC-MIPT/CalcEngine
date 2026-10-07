import { cleanup, render, screen } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import { PASS_ID } from './mocks/fixtures'
import { routes } from './routes'

function open(address: string) {
  render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: [address] })} />)
}

describe('routes', () => {
  it.each([
    ['/calculations/new?type=foundations_shallow_r', 'Исходные данные'],
    [`/calculations/${PASS_ID}`, 'Результат расчёта'],
    ['/calculations/abc/report', 'Report request'],
  ])('renders the screen of %s', (address, heading) => {
    open(address)

    expect(screen.getByRole('heading', { name: heading })).toBeInTheDocument()
  })

  it('renders the type selection at the root address', async () => {
    open('/')

    expect(screen.getByRole('heading', { name: 'Выберите тип расчёта' })).toBeInTheDocument()
    expect(await screen.findByRole('link', { name: 'Расчётное сопротивление грунта' })).toBeInTheDocument()
  })

  it('passes the type to the form and the id to the result and the report', async () => {
    open('/calculations/new?type=foundations_shallow_r')
    expect(await screen.findByText('Расчётное сопротивление грунта')).toBeInTheDocument()
  })

  it('passes the id to the result, its report link, and to the report screen', async () => {
    open(`/calculations/${PASS_ID}`)
    expect(await screen.findByRole('link', { name: 'Запросить отчёт' })).toHaveAttribute(
      'href',
      `/calculations/${PASS_ID}/report`,
    )
    cleanup()

    open('/calculations/abc/report')
    expect(screen.getByText('abc')).toBeInTheDocument()
  })

  it('renders a not found screen with a link to the type selection for an unknown address', () => {
    open('/nowhere')

    expect(screen.getByRole('heading', { name: 'Страница не найдена' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'К выбору типа расчёта' })).toHaveAttribute('href', '/')
  })
})

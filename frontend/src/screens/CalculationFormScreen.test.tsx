import { fireEvent, render, screen } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import { server } from '@/mocks/server'
import { routes } from '@/routes'

function open(address: string) {
  return render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: [address] })} />)
}

describe('CalculationFormScreen', () => {
  it('shows the title and the loading state first, then the form of the type in the address', async () => {
    open('/calculations/new?type=foundations_shallow_r')

    expect(screen.getByRole('heading', { name: 'Исходные данные' })).toBeInTheDocument()
    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(await screen.findByText('foundations_shallow_r')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Рассчитать' })).toBeInTheDocument()
  })

  it.each(['/calculations/new?type=nope', '/calculations/new'])(
    'says that the type is not found for %s and links to the type selection',
    async (address) => {
      open(address)

      expect(await screen.findByRole('heading', { name: 'Тип расчёта не найден' })).toBeInTheDocument()
      expect(screen.getByRole('link', { name: 'К выбору типа расчёта' })).toHaveAttribute('href', '/')
    },
  )

  it('shows a 503 of the listing with its code and retries the same request', async () => {
    server.use(
      http.get('*/calculation-types', () =>
        HttpResponse.json({ code: 'database_unavailable', message: 'x' }, { status: 503 }),
      ),
    )
    open('/calculations/new?type=foundations_shallow_r')

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('database_unavailable')

    server.resetHandlers()
    fireEvent.click(screen.getByRole('button', { name: 'Повторить' }))

    expect(await screen.findByRole('button', { name: 'Рассчитать' })).toBeInTheDocument()
  })
})

import { fireEvent, render, screen } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import { calculationTypes } from '@/mocks/fixtures'
import { server } from '@/mocks/server'
import { routes } from '@/routes'
import { expectNoA11yViolations } from '@/test/axe'

function open() {
  return render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: ['/'] })} />)
}

const [pilot] = calculationTypes
const second = { ...pilot, name: 'second_type' }

describe('TypeSelectionScreen', () => {
  it('lists every type of the listing, shows loading first, and has no a11y violations', async () => {
    server.use(http.get('*/calculation-types', () => HttpResponse.json([pilot, second])))
    const { container } = open()

    expect(screen.getByRole('status')).toBeInTheDocument()
    const links = await screen.findAllByRole('link', { name: /_/ })

    expect(links.map((link) => link.textContent)).toEqual(['foundations_shallow_r', 'second_type'])
    await expectNoA11yViolations(container)
  })

  it('opens the form of the chosen type with its name in the address', async () => {
    server.use(http.get('*/calculation-types', () => HttpResponse.json([pilot, second])))
    const router = createMemoryRouter(routes, { initialEntries: ['/'] })
    render(<RouterProvider router={router} />)

    fireEvent.click(await screen.findByRole('link', { name: 'second_type' }))

    expect(screen.getByRole('heading', { name: 'Calculation inputs' })).toBeInTheDocument()
    expect(screen.getByText('second_type')).toBeInTheDocument()
    expect(router.state.location.search).toBe('?type=second_type')
  })

  it('encodes a type name in the address', async () => {
    server.use(http.get('*/calculation-types', () => HttpResponse.json([{ ...pilot, name: 'a b&c' }])))
    open()

    expect(await screen.findByRole('link', { name: 'a b&c' })).toHaveAttribute(
      'href',
      '/calculations/new?type=a%20b%26c',
    )
  })

  it('says so when the listing is empty', async () => {
    server.use(http.get('*/calculation-types', () => HttpResponse.json([])))
    open()

    expect(await screen.findByText('Нет доступных типов расчёта.')).toBeInTheDocument()
    expect(screen.queryByRole('list')).not.toBeInTheDocument()
  })

  it('shows a 503 with its code and retries the same request', async () => {
    let healthy = false
    server.use(
      http.get('*/calculation-types', () =>
        healthy
          ? HttpResponse.json([pilot])
          : HttpResponse.json({ code: 'parameter_source_unavailable', message: 'x' }, { status: 503 }),
      ),
    )
    open()

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('Расчёт сейчас недоступен.')
    expect(alert).toHaveTextContent('parameter_source_unavailable')

    healthy = true
    fireEvent.click(screen.getByRole('button', { name: 'Повторить' }))

    expect(await screen.findByRole('link', { name: 'foundations_shallow_r' })).toBeInTheDocument()
  })
})

import { render, screen } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import { routes } from './routes'

function open(address: string) {
  render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: [address] })} />)
}

describe('routes', () => {
  it.each([
    ['/', 'Calculation types'],
    ['/calculations/new?type=foundations_shallow_r', 'Calculation inputs'],
    ['/calculations/abc', 'Calculation result'],
    ['/calculations/abc/report', 'Report request'],
  ])('renders the screen of %s', (address, heading) => {
    open(address)

    expect(screen.getByRole('heading', { name: heading })).toBeInTheDocument()
  })

  it('passes the type to the form and the id to the result and the report', () => {
    open('/calculations/new?type=foundations_shallow_r')
    expect(screen.getByText('foundations_shallow_r')).toBeInTheDocument()
  })

  it.each(['/calculations/abc', '/calculations/abc/report'])('shows the id on %s', (address) => {
    open(address)

    expect(screen.getByText('abc')).toBeInTheDocument()
  })

  it('renders a not found screen with a link to the type selection for an unknown address', () => {
    open('/nowhere')

    expect(screen.getByRole('heading', { name: 'Page not found' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Calculation types' })).toHaveAttribute('href', '/')
  })
})

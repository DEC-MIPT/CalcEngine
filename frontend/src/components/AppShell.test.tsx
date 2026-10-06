import { render, screen, within } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import { routes } from '@/routes'
import { expectNoA11yViolations } from '@/test/axe'

function open(address: string) {
  return render(
    <RouterProvider router={createMemoryRouter(routes, { initialEntries: [address] })} />,
  )
}

describe('AppShell', () => {
  it('shows the title, and the link to type selection on every screen', () => {
    for (const address of ['/', '/calculations/new', '/calculations/abc', '/nowhere']) {
      const { unmount } = open(address)
      expect(screen.getByText('Калькулятор инженера-проектировщика')).toBeInTheDocument()
      const navigation = screen.getByRole('navigation', { name: 'Основная навигация' })
      expect(within(navigation).getByRole('link', { name: 'Типы расчётов' })).toHaveAttribute(
        'href',
        '/',
      )
      expect(screen.queryByRole('group', { name: 'Язык интерфейса' })).not.toBeInTheDocument()
      expect(screen.getByRole('main')).toBeInTheDocument()
      unmount()
    }
  })

  it('marks the type selection link as the current page only on type selection', () => {
    const { unmount } = open('/')
    expect(screen.getByRole('link', { name: 'Типы расчётов' })).toHaveAttribute('aria-current', 'page')
    unmount()

    open('/nowhere')
    expect(screen.getByRole('link', { name: 'Типы расчётов' })).not.toHaveAttribute('aria-current')
  })

  it('has no detectable accessibility violations', async () => {
    const { container } = open('/nowhere')

    await expectNoA11yViolations(container)
  })
})

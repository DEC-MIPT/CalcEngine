import { fireEvent, render, screen, within } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { routes } from '@/routes'
import { AppShell } from './AppShell'
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

  it('shows the language switch when it is turned on, and switching changes the texts', () => {
    render(
      <RouterProvider
        router={createMemoryRouter([{ element: <AppShell languageSwitch />, children: [{ path: '/', element: null }] }], {
          initialEntries: ['/'],
        })}
      />,
    )
    const group = screen.getByRole('group', { name: 'Язык интерфейса' })

    fireEvent.click(within(group).getByRole('button', { name: 'English' }))

    expect(screen.getByText("Design Engineer's Calculator")).toBeInTheDocument()
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


const trailOf = () =>
  within(screen.getByRole('navigation', { name: 'Основная навигация' }))
    .getAllByRole('listitem')
    .map((item) => item.textContent)

describe('AppShell: status line (critique of the shell)', () => {
  afterEach(() => vi.unstubAllEnvs())

  it.each([
    ['/', ['Типы расчётов']],
    ['/calculations/new?type=foundations_shallow_r', ['Типы расчётов', 'Исходные данные']],
    ['/calculations/11111111-1111-4111-8111-111111111111', ['Типы расчётов', 'Результат № 11111111']],
    ['/calculations/11111111-1111-4111-8111-111111111111/report', ['Типы расчётов', 'Результат № 11111111', 'Отчёт']],
    ['/nowhere', ['Типы расчётов', 'Не найдено']],
  ])('shows where %s is in the trail, the last crumb as the current page', (address, crumbs) => {
    open(address)

    expect(trailOf()).toEqual(crumbs)
    const current = screen.getByRole('navigation', { name: 'Основная навигация' }).querySelector('[aria-current="page"]')
    expect(current).toHaveTextContent(crumbs.at(-1)!)
  })

  it('links the result crumb of the report screen back to the result', () => {
    open('/calculations/11111111-1111-4111-8111-111111111111/report')

    expect(screen.getByRole('link', { name: 'Результат № 11111111' })).toHaveAttribute(
      'href',
      '/calculations/11111111-1111-4111-8111-111111111111',
    )
  })

  it('labels demonstration data only when the mocks answer', () => {
    const { unmount } = open('/')
    expect(screen.queryByText('Демонстрационные данные')).not.toBeInTheDocument()
    unmount()

    vi.stubEnv('MODE', 'mock')
    open('/')
    expect(screen.getByText('Демонстрационные данные')).toBeInTheDocument()
  })
})

import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import { routes } from '@/routes'
import { expectNoA11yViolations } from '@/test/axe'

const values: Record<string, string> = {
  b: '2',
  d_1: '1.5',
  d_b: '0',
  gamma_II: '18',
  gamma_II_prime: '18',
  c_II: '10',
  phi_II: '20',
  p: '100',
}

function open(address: string) {
  const router = createMemoryRouter(routes, { initialEntries: [address] })
  return { router, ...render(<RouterProvider router={router} />) }
}

const field = (name: string) => document.getElementById(`field-${name}`) as HTMLInputElement

async function fillAndSend(overrides: Record<string, string> = {}) {
  await screen.findByRole('button', { name: 'Рассчитать' })
  for (const [name, value] of Object.entries({ ...values, ...overrides })) {
    fireEvent.change(field(name), { target: { value } })
  }
  fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))
  await screen.findByRole('link', { name: 'Запросить отчёт' })
}

const FORM = '/calculations/new?type=foundations_shallow_r'

describe('form draft and the edit-inputs action (9.2a, 9.2b)', () => {
  it('keeps the values and units on the browser back action', async () => {
    const { router } = open(FORM)
    await screen.findByRole('button', { name: 'Рассчитать' })
    fireEvent.change(screen.getAllByRole('combobox')[0], { target: { value: 'cm' } })
    await fillAndSend({ b: '200' })

    await act(() => router.navigate(-1))

    await screen.findByRole('button', { name: 'Рассчитать' })
    expect(field('b').value).toBe('200')
    expect(field('p').value).toBe('100')
    expect((screen.getAllByRole('combobox')[0] as HTMLSelectElement).value).toBe('cm')
  })

  it('writes nothing to the storage or the address', async () => {
    const { router } = open(FORM)
    await fillAndSend({ p: '987654.321' })

    expect(localStorage.length).toBe(0)
    expect(sessionStorage.length).toBe(0)
    expect(router.state.location.search).toBe('')
    expect(router.state.location.pathname).not.toContain('987654')
  })

  it('offers "edit inputs" on the result just calculated and opens the form with the values', async () => {
    open(FORM)
    await fillAndSend()

    const link = screen.getByRole('link', { name: 'Изменить исходные данные' })
    expect(link).toHaveAttribute('href', FORM)
    fireEvent.click(link)

    await screen.findByRole('button', { name: 'Рассчитать' })
    expect(field('gamma_II').value).toBe('18')
    expect(field('p').value).toBe('100')
  })

  it('has no accessibility violations with the action on the result', async () => {
    const { container } = open(FORM)
    await fillAndSend()
    await expectNoA11yViolations(container)
  })

  it('offers no action for a result opened by its address', async () => {
    open('/calculations/11111111-1111-4111-8111-111111111111')
    await screen.findByRole('link', { name: 'Запросить отчёт' })

    expect(screen.queryByRole('link', { name: 'Изменить исходные данные' })).not.toBeInTheDocument()
  })

  it('offers no action for an earlier result reached by the history after a newer calculation', async () => {
    const { router } = open(FORM)
    await fillAndSend()
    fireEvent.click(screen.getByRole('link', { name: 'Изменить исходные данные' }))
    await screen.findByRole('button', { name: 'Рассчитать' })
    fireEvent.change(field('b'), { target: { value: '12' } })
    fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))
    await screen.findByText(/Расчёт не выполнен/)

    await act(() => router.navigate(-2))

    await screen.findByRole('heading', { name: 'Проверка выполнена' })
    expect(screen.queryByRole('link', { name: 'Изменить исходные данные' })).not.toBeInTheDocument()
  })

  it('makes "edit inputs" the main action of a refusal, with the report as the second', async () => {
    open(FORM)
    await fillAndSend({ b: '12' })
    await screen.findByText(/Расчёт не выполнен/)

    const edit = screen.getByRole('link', { name: 'Изменить исходные данные' })
    const report = screen.getByRole('link', { name: 'Запросить отчёт' })
    expect(edit.compareDocumentPosition(report) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
    expect(edit.className).toContain('bg-primary')
    expect(report.className).not.toContain('bg-primary/')
    expect(report.className).toContain('bg-card')
  })

  it('opens the form from a refusal with focus in the named field and the bound in text', async () => {
    open(FORM)
    await fillAndSend({ b: '12' })
    await screen.findByText(/Расчёт не выполнен/)

    fireEvent.click(screen.getByRole('link', { name: 'Изменить исходные данные' }))

    await screen.findByRole('button', { name: 'Рассчитать' })
    await waitFor(() => expect(field('b')).toHaveFocus())
    expect(field('b').value).toBe('12')
    expect(field('b')).toHaveAccessibleDescription(/Метод допускает: b меньше или равно 10 м/)

    fireEvent.change(field('b'), { target: { value: '8' } })
    expect(screen.queryByText(/Метод допускает/)).not.toBeInTheDocument()
  })
})

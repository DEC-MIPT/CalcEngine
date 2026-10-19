import { render, screen } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import { FAIL_ID, PASS_ID, REFUSED_ID, WARNING_ID } from '@/mocks/fixtures'
import { routes } from '@/routes'

function open(id: string) {
  return render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: [`/calculations/${id}`] })} />)
}

describe('verdict focus on arrival (9.4)', () => {
  it.each([
    [PASS_ID, 'Проверка выполнена'],
    [FAIL_ID, 'Проверка не выполнена'],
    [REFUSED_ID, /Расчёт не выполнен/],
  ])('puts focus on the verdict region of result %s', async (id, name) => {
    open(id)

    expect(await screen.findByRole('region', { name })).toHaveFocus()
  })

  it('puts focus on the verdict of a result with a warning, not on the warning', async () => {
    open(WARNING_ID)

    const verdict = await screen.findByRole('region', { name: 'Проверка выполнена' })
    expect(verdict).toHaveFocus()
    expect(screen.getByRole('region', { name: /Предупреждение/ })).not.toHaveFocus()
  })
})

import { render, screen } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { expect, it } from 'vitest'
import { LOADS_CONTACT_REFUSAL_ID, loadsContactRefusalEnvelope } from '@/mocks/fixtures'
import { routes } from '@/routes'

it('routes the stored derived reason to its diagnostic refusal instead of a checked result', async () => {
  const router = createMemoryRouter(routes, { initialEntries: [`/calculations/${LOADS_CONTACT_REFUSAL_ID}`] })
  render(<RouterProvider router={router} />)

  const region = await screen.findByRole('region', { name: /условие полного контакта не выполнено/ })
  expect(region).toHaveTextContent(loadsContactRefusalEnvelope.verdict_reason.quantity)
  expect(region).toHaveTextContent('Проверки несущей способности не выполнялись.')
  expect(screen.queryByRole('heading', { name: 'Выходные величины' })).not.toBeInTheDocument()
  expect(screen.queryByRole('region', { name: 'Проверка выполнена' })).not.toBeInTheDocument()
  expect(screen.queryByRole('region', { name: 'Проверка не выполнена' })).not.toBeInTheDocument()
  expect(screen.getByRole('link', { name: 'Запросить отчёт' })).toHaveAttribute(
    'href', `/calculations/${LOADS_CONTACT_REFUSAL_ID}/report`,
  )
})

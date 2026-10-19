import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, describe, expect, it, vi } from 'vitest'
import type { components } from '@/api/schema'
import { DraftProvider } from '@/form/DraftProvider'
import { I18nProvider } from '@/i18n/I18nProvider'
import { calculationTypes } from '@/mocks/fixtures'
import { CalculationForm } from './CalculationForm'

type CalculationType = components['schemas']['CalculationTypeView']
const [pilot] = calculationTypes as unknown as CalculationType[]
const values: Record<string, string> = { b: '2', d_1: '1.5', d_b: '0', gamma_II: '18', gamma_II_prime: '18', c_II: '10', phi_II: '20', p: '100' }

afterEach(() => vi.unstubAllGlobals())

function open(reduced: boolean) {
  vi.stubGlobal('matchMedia', () => ({ matches: reduced }))
  const router = createMemoryRouter(
    [
      {
        path: '/calculations/new',
        element: (
          <I18nProvider initialLanguage="ru">
            <DraftProvider>
              <CalculationForm type={pilot} />
            </DraftProvider>
          </I18nProvider>
        ),
      },
      { path: '/calculations/:id', element: <p>opened</p> },
    ],
    { initialEntries: ['/calculations/new'] },
  )
  const view = render(<RouterProvider router={router} />)
  for (const [name, value] of Object.entries(values)) {
    fireEvent.change(document.getElementById(`field-${name}`)!, { target: { value } })
  }
  return view
}

describe('CalculationForm: the computation trace (UX bold pass, zone 2)', () => {
  it('traces the computation over the rows and holds the result for at least 700 ms', async () => {
    const { container } = open(false)
    const started = performance.now()

    fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))

    expect(container.querySelector('form')).toHaveClass('computing')
    expect(container.querySelector('.compute-scan')).toHaveStyle({ '--rows': String(pilot.inputs.length) })
    expect(container.querySelector('svg.compute-plot')).toHaveAttribute('aria-hidden', 'true')
    expect(container.querySelectorAll('[data-row]')).toHaveLength(pilot.inputs.length)
    expect(container.querySelector('[data-row]:last-of-type')).toHaveStyle({ '--row': String(pilot.inputs.length - 1) })

    await waitFor(() => expect(screen.getByText('opened')).toBeInTheDocument(), { timeout: 2000 })
    expect(performance.now() - started).toBeGreaterThanOrEqual(690)
  })

  it('shows no trace and holds nothing back under reduced motion', async () => {
    const { container } = open(true)
    const started = performance.now()

    fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))

    expect(container.querySelector('form')).not.toHaveClass('computing')
    expect(container.querySelector('.compute-scan')).toBeNull()
    expect(container.querySelector('svg.compute-plot')).toBeNull()
    await waitFor(() => expect(screen.getByText('opened')).toBeInTheDocument())
    expect(performance.now() - started).toBeLessThan(600)
  })
})

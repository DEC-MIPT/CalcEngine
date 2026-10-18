import { act, fireEvent, render, screen } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { FAIL_ID, PASS_ID, passEnvelope, REFUSED_ID, WARNING_ID } from '@/mocks/fixtures'
import { resetPlayed, stepInterval } from '@/lib/playback'
import { routes } from '@/routes'

const STEPS = passEnvelope.trace.length

function open(id: string) {
  const router = createMemoryRouter(routes, { initialEntries: [`/calculations/${id}`] })
  render(<RouterProvider router={router} />)
  return router
}

const stamp = () => document.querySelector('[data-verdict]')!
const outputs = () => screen.getByRole('heading', { name: 'Выходные величины' }).closest('section')!
const pending = () => document.querySelectorAll('[data-step][data-arrival="pending"]').length

async function playThrough() {
  for (let step = 0; step < STEPS; step++) {
    await act(() => vi.advanceTimersByTimeAsync(stepInterval(STEPS)))
  }
}

beforeEach(() => {
  vi.useFakeTimers({ shouldAdvanceTime: true })
  vi.stubGlobal('matchMedia', () => ({ matches: false }))
})

afterEach(() => {
  vi.useRealTimers()
  vi.unstubAllGlobals()
  resetPlayed()
})

describe('result screen: trace playback and verdict reveal', () => {
  it('holds the verdict until the last step and then stamps a clean pass', async () => {
    open(PASS_ID)
    const region = await screen.findByRole('region', { name: 'Проверка выполнена' })

    expect(region).toHaveFocus()
    expect(stamp()).toHaveAttribute('data-reveal', 'pending')
    expect(outputs()).toHaveAttribute('data-reveal', 'pending')
    expect(outputs().querySelector('tbody')).toHaveAttribute('inert')
    expect(pending()).toBe(STEPS)
    await playThrough()

    expect(pending()).toBe(0)
    expect(stamp()).toHaveAttribute('data-reveal', 'celebrate')
    expect(outputs()).toHaveAttribute('data-reveal', 'celebrate')
    expect(outputs().querySelector('tbody')).not.toHaveAttribute('inert')
  })

  it.each([
    [FAIL_ID, 'Проверка не выполнена'],
    [WARNING_ID, 'Проверка выполнена'],
  ])('shows the verdict of %s plainly right after the last step', async (id, name) => {
    open(id)
    await screen.findByRole('region', { name })

    await playThrough()

    expect(stamp()).toHaveAttribute('data-reveal', 'plain')
    expect(outputs()).toHaveAttribute('data-reveal', 'plain')
  })

  it('shows everything at once after a skip, with no celebration', async () => {
    open(PASS_ID)
    await screen.findByRole('region', { name: 'Проверка выполнена' })
    await act(() => vi.advanceTimersByTimeAsync(0))

    fireEvent.keyDown(document.body, { key: 'Escape' })

    expect(pending()).toBe(0)
    expect(stamp()).toHaveAttribute('data-reveal', 'none')
    expect(outputs()).toHaveAttribute('data-reveal', 'none')
    expect(document.querySelector('[data-outputs-status]')).toBeNull()
  })

  it('does not play again when the same result is opened again', async () => {
    const router = open(PASS_ID)
    await screen.findByRole('region', { name: 'Проверка выполнена' })
    await act(() => router.navigate(`/calculations/${FAIL_ID}`))
    await screen.findByRole('region', { name: 'Проверка не выполнена' })

    await act(() => router.navigate(`/calculations/${PASS_ID}`))
    await screen.findByRole('region', { name: 'Проверка выполнена' })

    expect(stamp()).toHaveAttribute('data-reveal', 'none')
    expect(outputs()).toHaveAttribute('data-reveal', 'none')
    expect(pending()).toBe(0)
  })

  it('shows a refusal at once, with no trace to play', async () => {
    open(REFUSED_ID)

    await screen.findByRole('region', { name: /Расчёт не выполнен/ })

    expect(document.querySelector('[data-step]')).toBeNull()
    expect(document.querySelector('[data-stamp-status]')).toBeNull()
  })
})

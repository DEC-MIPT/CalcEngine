import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { loadsCentralInputs, loadsContactRefusalEnvelope, loadsContactRefusalInputs, LOADS_TYPE } from '@/mocks/fixtures'
import { routes } from '@/routes'

const label = /условие полного контакта не выполнено/
const rawN = '+0600.000'
const rawMx = '+180000.000'
const field = (name: string) => document.getElementById(`field-${name}`) as HTMLInputElement
const unit = (name: string) => field(name).parentElement!.querySelector('select')!
const reason = loadsContactRefusalEnvelope.verdict_reason

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

function open(address = `/calculations/new?type=${LOADS_TYPE}`) {
  vi.stubGlobal('matchMedia', () => ({ matches: true }))
  const router = createMemoryRouter(routes, { initialEntries: [address] })
  return { router, ...render(<RouterProvider router={router} />) }
}

async function submitRefusal() {
  await screen.findByRole('button', { name: 'Рассчитать' })
  for (const [name, quantity] of Object.entries(loadsContactRefusalInputs)) {
    fireEvent.change(field(name), { target: { value: String(quantity.value) } })
  }
  fireEvent.change(field('N'), { target: { value: rawN } })
  fireEvent.change(field('b'), { target: { value: '02.0000' } })
  fireEvent.change(field('Mx'), { target: { value: rawMx } })
  fireEvent.change(unit('Mx'), { target: { value: 'N*m' } })
  fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))
  return screen.findByRole('region', { name: label })
}

describe('derived refusal edit eligibility and private draft contract', () => {
  it('restores exact raw strings and units, focuses the first related input and keeps a readable stored reason nearby', async () => {
    const storage = vi.spyOn(Storage.prototype, 'setItem')
    const log = vi.spyOn(console, 'log')
    const { router } = open()
    await submitRefusal()
    expect(document.body).not.toHaveTextContent(rawN)
    expect(document.body).not.toHaveTextContent(rawMx)
    const edit = screen.getByRole('link', { name: 'Изменить исходные данные' })
    const report = screen.getByRole('link', { name: 'Запросить отчёт' })
    expect(edit.compareDocumentPosition(report) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
    fireEvent.click(edit)
    await screen.findByRole('button', { name: 'Рассчитать' })
    await waitFor(() => expect(field(reason.related_inputs[0])).toHaveFocus())
    expect(field('N')).toHaveValue(rawN)
    expect(field('b')).toHaveValue('02.0000')
    expect(field('Mx')).toHaveValue(rawMx)
    expect(unit('Mx')).toHaveValue('N*m')
    expect(document.getElementById(`field-${reason.quantity}`)).toBeNull()
    expect(field(reason.related_inputs[0])).toHaveAccessibleDescription(/-30.*кПа/u)
    expect(field(reason.related_inputs[0])).toHaveAccessibleDescription(/mm/u)
    expect(JSON.stringify(router.state.location)).not.toContain(rawN)
    expect(JSON.stringify(router.state.location)).not.toContain(rawMx)
    expect(router.state.location.search).toBe(`?type=${LOADS_TYPE}`)
    expect(storage).not.toHaveBeenCalled()
    expect(log).not.toHaveBeenCalled()
  })

  it.each(['value', 'unit'] as const)('clears stale correction context after changing a related %s', async (kind) => {
    const { router } = open()
    await submitRefusal()
    fireEvent.click(screen.getByRole('link', { name: 'Изменить исходные данные' }))
    await screen.findByRole('button', { name: 'Рассчитать' })
    await waitFor(() => expect(field('N')).toHaveFocus())
    expect(field('N')).toHaveAccessibleDescription(/-30.*кПа/u)
    if (kind === 'value') fireEvent.change(field('Mx'), { target: { value: '180001' } })
    else fireEvent.change(unit('Mx'), { target: { value: 'kN*m' } })
    await waitFor(() => expect(field('N')).not.toHaveAccessibleDescription(/-30.*кПа/u))
    expect(router.state.location.state?.derivedCorrection).toBeUndefined()
  })

  it('does not expose edit actions for direct/reloaded stored results or persist earlier raw draft values', async () => {
    const first = open()
    await submitRefusal()
    expect(screen.getByRole('link', { name: 'Изменить исходные данные' })).toBeInTheDocument()
    first.unmount()
    const reload = open(`/calculations/${loadsContactRefusalEnvelope.result_id}`)
    await screen.findByRole('region', { name: label })
    expect(screen.queryByRole('link', { name: 'Изменить исходные данные' })).not.toBeInTheDocument()
    await act(() => reload.router.navigate(`/calculations/new?type=${LOADS_TYPE}`))
    await screen.findByRole('button', { name: 'Рассчитать' })
    expect(field('N')).toHaveValue('')
    expect(field('Mx')).toHaveValue('')
    expect(unit('Mx')).toHaveValue('kN*m')
  })

  it('clears correction context on a new submit even when local validation rejects an unrelated field', async () => {
    const { router } = open()
    await submitRefusal()
    fireEvent.click(screen.getByRole('link', { name: 'Изменить исходные данные' }))
    await screen.findByRole('button', { name: 'Рассчитать' })
    await waitFor(() => expect(field('N')).toHaveFocus())
    fireEvent.change(field('phi_II'), { target: { value: '' } })
    expect(field('N')).toHaveAccessibleDescription(/-30.*кПа/u)

    fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))

    await waitFor(() => expect(field('phi_II')).toHaveFocus())
    expect(field('phi_II')).toHaveAttribute('aria-invalid', 'true')
    expect(field('N')).not.toHaveAccessibleDescription(/-30.*кПа/u)
    expect(router.state.location.state?.derivedCorrection).toBeUndefined()
    expect(field('N')).toHaveValue(rawN)
    expect(field('Mx')).toHaveValue(rawMx)
    expect(unit('Mx')).toHaveValue('N*m')
  })

  it('does not offer edit for an older refusal after the same draft has submitted a newer result', async () => {
    const { router } = open()
    await submitRefusal()
    fireEvent.click(screen.getByRole('link', { name: 'Изменить исходные данные' }))
    await screen.findByRole('button', { name: 'Рассчитать' })
    for (const [name, quantity] of Object.entries(loadsCentralInputs)) {
      fireEvent.change(field(name), { target: { value: String(quantity.value) } })
      if (unit(name)) fireEvent.change(unit(name), { target: { value: quantity.unit } })
    }
    fireEvent.click(screen.getByRole('button', { name: 'Рассчитать' }))
    await screen.findByRole('region', { name: 'Проверка выполнена' })
    await act(() => router.navigate(-2))
    await screen.findByRole('region', { name: label })
    expect(screen.queryByRole('link', { name: 'Изменить исходные данные' })).not.toBeInTheDocument()
  })

  it('ignores a forged correction history state without a matching submitted in-memory draft', async () => {
    vi.stubGlobal('matchMedia', () => ({ matches: true }))
    render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: [{
      pathname: '/calculations/new', search: `?type=${LOADS_TYPE}`,
      state: { derivedCorrection: { resultId: loadsContactRefusalEnvelope.result_id, reason } },
    }] })} />)
    await screen.findByRole('button', { name: 'Рассчитать' })
    expect(field('N')).toHaveValue('')
    expect(field('N')).not.toHaveAccessibleDescription(/-30.*кПа/u)
    expect(document.getElementById(`field-${reason.quantity}`)).toBeNull()
  })
})

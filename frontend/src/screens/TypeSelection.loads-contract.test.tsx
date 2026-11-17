import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import { LOADS_TYPE, loadsCalculationType } from '@/mocks/fixtures'
import { routes } from '@/routes'

const guidance = 'Схема направлений и знаков'
const label = (name: string) => loadsCalculationType.inputs.find((input) => input.name === name)!.label.ru

function start() {
  const router = createMemoryRouter(routes, { initialEntries: ['/'] })
  render(<RouterProvider router={router} />)
  return router
}

async function typeLink(name: string) {
  const table = await screen.findByRole('table')
  const links = await within(table).findAllByRole('link')
  return links.find((link) => link.getAttribute('href') === `/calculations/new?type=${name}`)!
}

describe('loads type selection and isolated form drafts', () => {
  it('opens the fifteen-field loads form using only keyboard selection', async () => {
    const user = userEvent.setup()
    const router = start()
    const link = await typeLink(LOADS_TYPE)
    expect(link).toBeDefined()
    for (let steps = 0; document.activeElement !== link && steps < screen.getAllByRole('link').length; steps += 1) {
      await user.tab()
    }
    expect(link).toHaveFocus()
    await user.keyboard('{Enter}')
    await screen.findByRole('textbox', { name: label('N') })
    expect(router.state.location.search).toBe(`?type=${LOADS_TYPE}`)
    expect(screen.getAllByRole('textbox')).toHaveLength(15)
    expect(screen.getByRole('region', { name: guidance })).toBeInTheDocument()
  })

  it('isolates pilot and loads drafts and restores entered strings and units on browser back', async () => {
    const user = userEvent.setup()
    const router = start()
    await user.click(await typeLink(LOADS_TYPE))
    const width = await screen.findByRole('textbox', { name: label('b') })
    fireEvent.change(width, { target: { value: '002,500' } })
    fireEvent.change(screen.getByRole('textbox', { name: label('Mx') }), { target: { value: '-40,00' } })
    fireEvent.change(screen.getByRole('textbox', { name: label('N') }), { target: { value: '+600,00' } })
    fireEvent.change(screen.getByRole('combobox', { name: `Единица: ${label('b')}` }), { target: { value: 'cm' } })
    fireEvent.change(screen.getByRole('combobox', { name: `Единица: ${label('Mx')}` }), { target: { value: 'MN*m' } })
    await user.click(screen.getAllByRole('link').find((link) => link.getAttribute('href') === '/')!)
    await user.click(await typeLink('foundations_shallow_r'))
    await waitFor(() => expect(screen.getAllByRole('textbox')).toHaveLength(8))
    expect(screen.getByRole('textbox', { name: label('b') })).toHaveValue('')
    expect(screen.queryByRole('textbox', { name: label('N') })).toBeNull()
    expect(screen.queryByRole('region', { name: guidance })).toBeNull()
    fireEvent.change(screen.getByRole('textbox', { name: label('b') }), { target: { value: '1,75' } })
    await act(async () => { await router.navigate(-2) })
    expect(await screen.findByRole('textbox', { name: label('N') })).toHaveValue('+600,00')
    expect(screen.getByRole('textbox', { name: label('b') })).toHaveValue('002,500')
    expect(screen.getByRole('textbox', { name: label('Mx') })).toHaveValue('-40,00')
    expect(screen.getByRole('combobox', { name: `Единица: ${label('b')}` })).toHaveValue('cm')
    expect(screen.getByRole('combobox', { name: `Единица: ${label('Mx')}` })).toHaveValue('MN*m')
    await user.click(screen.getAllByRole('link').find((link) => link.getAttribute('href') === '/')!)
    await user.click(await typeLink('foundations_shallow_r'))
    expect(await screen.findByRole('textbox', { name: label('b') })).toHaveValue('1,75')
  })
})

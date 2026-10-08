import { fireEvent, render, screen, within } from '@testing-library/react'
import { http, HttpResponse } from 'msw'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, expect, it } from 'vitest'
import { calculationTypes } from '@/mocks/fixtures'
import { server } from '@/mocks/server'
import { routes } from '@/routes'
import { expectNoA11yViolations } from '@/test/axe'

function open() {
  return render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: ['/'] })} />)
}

const [pilot] = calculationTypes
const second = {
  ...pilot,
  name: 'second_type',
  outputs: [{ ...pilot.outputs[0], label: { ru: 'Вторая величина', en: 'Second quantity' } }],
}
const PILOT_NAME = 'Расчётное сопротивление грунта'

describe('TypeSelectionScreen', () => {
  it('lists every type of the listing, shows loading first, and has no a11y violations', async () => {
    server.use(http.get('*/calculation-types', () => HttpResponse.json([pilot, second])))
    const { container } = open()

    expect(screen.getByRole('status')).toBeInTheDocument()
    const table = await screen.findByRole('table')
    const links = await within(table).findAllByRole('link')

    expect(links.map((link) => link.textContent)).toEqual([PILOT_NAME, 'Вторая величина'])
    expect(within(table).getByText('foundations_shallow_r')).toBeInTheDocument()
    expect(within(table).getByText('second_type')).toBeInTheDocument()
    expect(within(table).getAllByText(String(pilot.inputs.length))).toHaveLength(2)
    await expectNoA11yViolations(container)
  })

  it('opens the form of the chosen type with its name in the address', async () => {
    server.use(http.get('*/calculation-types', () => HttpResponse.json([pilot, second])))
    const router = createMemoryRouter(routes, { initialEntries: ['/'] })
    render(<RouterProvider router={router} />)

    fireEvent.click(await screen.findByRole('link', { name: 'Вторая величина' }))

    expect(screen.getByRole('heading', { name: 'Исходные данные' })).toBeInTheDocument()
    expect(await screen.findByText('Вторая величина')).toBeInTheDocument()
    expect(router.state.location.search).toBe('?type=second_type')
  })

  it('encodes a type name in the address', async () => {
    server.use(http.get('*/calculation-types', () => HttpResponse.json([{ ...pilot, name: 'a b&c' }])))
    open()

    expect(await screen.findByRole('link', { name: PILOT_NAME })).toHaveAttribute(
      'href',
      '/calculations/new?type=a%20b%26c',
    )
  })

  it('calls an empty listing a configuration fault and retries it', async () => {
    let types: unknown[] = []
    server.use(http.get('*/calculation-types', () => HttpResponse.json(types)))
    open()

    expect(await screen.findByText(/Реестр типов расчёта пуст/)).toBeInTheDocument()
    expect(within(screen.getByRole('table')).queryByRole('link')).not.toBeInTheDocument()

    types = [pilot]
    fireEvent.click(screen.getByRole('button', { name: 'Повторить' }))

    expect(await screen.findByRole('link', { name: PILOT_NAME })).toBeInTheDocument()
  })

  it('shows a 503 with its code and retries the same request', async () => {
    let healthy = false
    server.use(
      http.get('*/calculation-types', () =>
        healthy
          ? HttpResponse.json([pilot])
          : HttpResponse.json({ code: 'parameter_source_unavailable', message: 'x' }, { status: 503 }),
      ),
    )
    open()

    const alert = await screen.findByRole('alert')
    expect(alert).toHaveTextContent('Не удалось загрузить список типов расчёта.')
    expect(alert).not.toHaveTextContent('Расчёт сейчас недоступен.')
    expect(alert).toHaveTextContent('parameter_source_unavailable')
    expect(alert).toHaveTextContent('Сообщение сервера: x')

    healthy = true
    fireEvent.click(screen.getByRole('button', { name: 'Повторить' }))

    expect(await screen.findByRole('link', { name: PILOT_NAME })).toBeInTheDocument()
  })
})

describe('TypeSelectionScreen hero (UX bold pass, zone 1)', () => {
  it('puts the page heading in a full-bleed hero with the kicker, the lede and a hidden drawing', async () => {
    const { container } = open()

    const heading = screen.getByRole('heading', { level: 1, name: 'Выберите тип расчёта' })
    const hero = heading.closest('section')!
    expect(hero).toHaveClass('on-accent')
    expect(within(hero).getByText('Прозрачный расчёт по нормам')).toBeInTheDocument()
    expect(within(hero).getByText(/Каждый шаг — с формулой/)).toBeInTheDocument()
    expect(hero.querySelector('svg.dimension-grid')).toHaveAttribute('aria-hidden', 'true')
    expect(screen.getByRole('main')).not.toHaveClass('max-w-5xl')
    await screen.findByRole('link', { name: PILOT_NAME })
    await expectNoA11yViolations(container)
  })

  it('keeps the other screens inside the page column', () => {
    render(<RouterProvider router={createMemoryRouter(routes, { initialEntries: ['/nowhere'] })} />)

    expect(screen.getByRole('main')).toHaveClass('max-w-5xl')
  })
})

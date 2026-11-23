import { render, screen, within } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import { expectNoA11yViolations } from '@/test/axe'
import { LoadsDirections } from './LoadsDirections'

describe('loads direction and sign guidance', () => {
  it('names the diagram and provides all engineering conventions in readable Russian text', async () => {
    const { container } = render(<I18nProvider initialLanguage="ru"><LoadsDirections /></I18nProvider>)
    const guidance = screen.getByRole('region', { name: 'Схема направлений и знаков' })
    const diagram = within(guidance).getByRole('img', { name: /Прямоугольная подошва: вид сверху/ })
    expect(diagram.tagName).toBe('svg')
    expect(diagram).toHaveAccessibleName(/Ширина b направлена вдоль x, длина l — вдоль y/)
    expect(within(guidance).getByText(/Mx и Qx задают изменение давления вдоль x=b/)).toHaveTextContent('My и Qy — вдоль y=l')
    expect(within(guidance).getByText(/Моменты переносятся к подошве алгебраически/)).toHaveTextContent('могут взаимно компенсироваться')
    expect(within(guidance).getByText(/Моменты переносятся к подошве алгебраически/)).toHaveTextContent('у положительного края своей оси')
    expect(within(guidance).getByText(/Вертикальная нагрузка без собственного веса/)).toHaveTextContent('добавляется один раз')
    expect(within(guidance).getByText('Толщина в весовом слагаемом γ_mt·d.')).toBeInTheDocument()
    expect(within(guidance).getByText(/Расстояние от сечения нагрузок на верху/)).toBeInTheDocument()
    expect(within(guidance).getByText(/Независимо подготовленная приведённая глубина/)).toHaveTextContent('не выводятся друг из друга')
    expect(within(guidance).getByText(/Заранее подготовленное инженером значение/)).toHaveTextContent('Отказ метода не запрещает более глубокий физический подвал')
    expect(within(guidance).getByText(/Введите b ≤ l/)).toHaveTextContent('автоматически не переставляются')
    expect(within(guidance).getByText(/φ_II: целое число градусов/)).toHaveTextContent('Дробный угол не округляется; интерполяция не выполняется')
    expect(within(guidance).getByText(/Углы обозначены знаками координат/)).toHaveTextContent('pp (+,+), pm (+,−), mp (−,+), mm (−,−)')
    await expectNoA11yViolations(container)
  })

  it('localizes the equivalent text and diagram name in English', async () => {
    const { container } = render(<I18nProvider initialLanguage="en"><LoadsDirections /></I18nProvider>)
    const guidance = screen.getByRole('region', { name: 'Directions and sign convention' })
    expect(within(guidance).getByRole('img')).toHaveAccessibleName(/Rectangular base: plan view Width b runs along x; length l runs along y/)
    expect(within(guidance).getByText(/Moments transfer to the base algebraically/)).toHaveTextContent('M and Q·h may cancel')
    expect(within(guidance).getByText(/Vertical load excluding foundation and overlying soil weight/)).toBeInTheDocument()
    expect(within(guidance).getByText(/An engineer-prepared value for the R method/)).toHaveTextContent('without clamping')
    expect(within(guidance).getByText(/φ_II: a whole number of degrees/)).toHaveTextContent('The server checks row availability')
    expect(within(guidance).getByText(/Enter b ≤ l/)).toHaveTextContent('Square bases are allowed')
    await expectNoA11yViolations(container)
  })

  it('retains the explicit-weight guidance without describing the averaged allowance', async () => {
    const { container } = render(<I18nProvider initialLanguage="en"><LoadsDirections explicit /></I18nProvider>)
    const guidance = screen.getByRole('region', { name: 'Directions and sign convention' })
    const hint = within(guidance).getByText(/Structural loads are supplied at the upper cut/)
    expect(hint.closest('figcaption')).toHaveClass('sr-only')
    expect(within(guidance).getByText(/Mx_base = /)).toHaveTextContent('Mx + Qx·h + Mx_add_base')
    expect(within(guidance).queryByText(/Vertical load excluding foundation and overlying soil weight/)).not.toBeInTheDocument()
    await expectNoA11yViolations(container)
  })

  it('keeps SVG descriptions unique when more than one diagram is mounted', () => {
    render(<I18nProvider><LoadsDirections /><LoadsDirections /></I18nProvider>)
    const images = screen.getAllByRole('img')
    expect(images[0].getAttribute('aria-labelledby')).not.toBe(images[1].getAttribute('aria-labelledby'))
    for (const image of images) {
      for (const id of image.getAttribute('aria-labelledby')!.split(' ')) {
        expect(document.getElementById(id)).toBeInTheDocument()
      }
    }
  })
})

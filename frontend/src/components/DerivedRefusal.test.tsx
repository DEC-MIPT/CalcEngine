import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import { loadsContactRefusalEnvelope, loadsDraftSource, loadsStrictSource } from '@/mocks/fixtures'
import { expectNoA11yViolations } from '@/test/axe'
import { DerivedRefusal } from './Refusal'

const reason = loadsContactRefusalEnvelope.verdict_reason

describe('derived refusal compatibility', () => {
  it.each([undefined, loadsStrictSource, loadsDraftSource])('shows only stored diagnostic facts with source %j', async (source) => {
    const { container } = render(
      <I18nProvider initialLanguage="ru">
        <DerivedRefusal reason={reason} source={source} />
      </I18nProvider>,
    )

    const region = screen.getByRole('region', { name: /условие полного контакта не выполнено/ })
    expect(region).toHaveFocus()
    expect(region).toHaveTextContent('Проверки несущей способности не выполнялись.')
    expect(screen.getByText('Диагностическая величина').nextElementSibling).toHaveTextContent(reason.quantity)
    expect(screen.getByText('Минимальное давление').nextElementSibling).toHaveTextContent('-30 кПа')
    expect(screen.getByText('Требуемое давление').nextElementSibling).toHaveTextContent('больше или равно')
    expect(screen.getByText('Требуемое давление').nextElementSibling).toHaveTextContent('0 кПа')
    expect(screen.getByText('Определяющий угол').nextElementSibling).toHaveTextContent('mm')
    expect(screen.getByText('Связанные исходные данные').nextElementSibling).toHaveTextContent(reason.related_inputs.join(', '))
    expect(screen.getByText(`Инженер: ${reason.source.engineer}`)).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Выходные величины' })).not.toBeInTheDocument()
    expect(screen.queryByText('Проверка выполнена')).not.toBeInTheDocument()
    if (source) {
      expect(screen.getByText(source.data_sha256)).toHaveClass('sr-only')
      expect(region).toHaveTextContent(`профиль ${source.profile}`)
    } else {
      expect(screen.queryByText('Источник параметров')).not.toBeInTheDocument()
    }
    await expectNoA11yViolations(container)
  })

  it('explains the full-contact refusal in English', () => {
    render(
      <I18nProvider initialLanguage="en">
        <DerivedRefusal reason={reason} />
      </I18nProvider>,
    )
    expect(screen.getByRole('region', { name: /full-contact condition is not satisfied/ })).toHaveTextContent(
      'Bearing checks were not performed.',
    )
    expect(screen.getByText('Required pressure').nextElementSibling).toHaveTextContent('greater than or equal to')
  })
})

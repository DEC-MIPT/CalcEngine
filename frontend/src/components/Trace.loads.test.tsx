import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import { loadsCentralEnvelope } from '@/mocks/fixtures'
import { expectNoA11yViolations } from '@/test/axe'
import { Trace } from './Trace'

const engineer = loadsCentralEnvelope.trace.find((step) => step.kind === 'engineer_formula')!

describe('engineer trace compatibility', () => {
  it('lets keyboard users reach the named formula scroll region', async () => {
    const user = userEvent.setup()
    render(
      <I18nProvider initialLanguage="en">
        <Trace steps={[engineer]} unverifiedStepCount={0} />
      </I18nProvider>,
    )
    const formula = screen.getByRole('region', { name: `Formula: ${engineer.step_id}` })
    expect(formula).toHaveClass('overflow-x-auto')
    await user.tab()
    await user.tab()
    await user.tab()
    await user.tab()
    expect(formula).toHaveFocus()
    expect(formula).toHaveClass('focus-visible:outline-offset-[-2px]')
  })

  it.each([false, true])('keeps engineer attribution visible with normative status %s', async (normStatus) => {
    const { container } = render(
      <I18nProvider initialLanguage="ru">
        <Trace steps={[engineer]} unverifiedStepCount={0} normStatus={normStatus} />
      </I18nProvider>,
    )

    expect(screen.getByText('Инженерная формула')).toBeInTheDocument()
    expect(screen.getByText('Инженерное правило')).toBeInTheDocument()
    expect(screen.getByText(`Инженер: ${engineer.source.engineer}`)).toBeInTheDocument()
    expect(screen.getByText(`Обоснование: ${engineer.source.rationale}`)).toBeInTheDocument()
    expect(screen.queryByText('Нормативные ссылки')).not.toBeInTheDocument()
    expect(screen.queryByText('проверено')).not.toBeInTheDocument()
    expect(screen.queryByText('не проверено')).not.toBeInTheDocument()
    await expectNoA11yViolations(container)
  })

  it('names the engineer formula and source in English', () => {
    render(
      <I18nProvider initialLanguage="en">
        <Trace steps={[engineer]} unverifiedStepCount={0} normStatus={false} />
      </I18nProvider>,
    )
    expect(screen.getByText('Engineer formula')).toBeInTheDocument()
    expect(screen.getByText('Engineer rule')).toBeInTheDocument()
    expect(screen.getByText(`Engineer: ${engineer.source.engineer}`)).toBeInTheDocument()
  })
})

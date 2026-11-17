import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import { loadsDraftSource, loadsStrictSource } from '@/mocks/fixtures'
import { expectNoA11yViolations } from '@/test/axe'
import { SourceLabel } from './SourceLabel'

describe('SourceLabel for captured loads source identity', () => {
  it.each([loadsStrictSource, loadsDraftSource])('preserves the aggregate digest and $profile status accessibly', async (source) => {
    const { container } = render(
      <I18nProvider initialLanguage="ru"><SourceLabel source={source} /></I18nProvider>,
    )
    const label = container.querySelector('[data-source="interim"]')
    expect(label).toHaveAttribute('data-profile', source.profile)
    expect(label).toHaveTextContent('ВРЕМЕННЫЕ ДАННЫЕ')
    const shortened = screen.getByText(`${source.data_sha256.slice(0, 12)}…`)
    expect(shortened).toHaveAttribute('title', source.data_sha256)
    expect(shortened).toHaveAttribute('aria-hidden', 'true')
    expect(screen.getByText(source.data_sha256)).toHaveClass('sr-only')
    if (source.profile === 'draft') {
      expect(label).toHaveTextContent('Черновик: значения не прошли верификацию')
    } else {
      expect(label).not.toHaveTextContent('Черновик')
    }
    await expectNoA11yViolations(container)
  })
})

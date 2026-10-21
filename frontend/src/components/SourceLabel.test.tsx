import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import type { Language } from '@/i18n/dictionary'
import { catalogSource, draftSource, strictSource } from '@/mocks/fixtures'
import { expectNoA11yViolations } from '@/test/axe'
import { SourceLabel } from './SourceLabel'

function show(source: Parameters<typeof SourceLabel>[0]['source'], language: Language = 'ru') {
  return render(
    <I18nProvider initialLanguage={language}>
      <SourceLabel source={source} />
    </I18nProvider>,
  )
}

describe('SourceLabel', () => {
  it('names the catalog and nothing else', () => {
    const { container } = show(catalogSource)

    expect(container).toHaveTextContent('каталог норм')
    expect(container.querySelector('[data-source="catalog"]')).not.toBeNull()
    expect(container).not.toHaveTextContent('ВРЕМЕННЫЕ ДАННЫЕ')
  })

  it('marks interim data in words and with an icon, with the profile and the short digest', () => {
    const { container } = show(strictSource)
    const label = container.querySelector('[data-source="interim"]')!

    expect(label).toHaveAttribute('data-profile', 'strict')
    expect(label).toHaveTextContent('ВРЕМЕННЫЕ ДАННЫЕ')
    expect(label.querySelector('svg')).not.toBeNull()
    expect(label).toHaveTextContent('профиль strict')
    expect(screen.getByText('0123456789ab…')).toHaveAttribute('title', strictSource.data_sha256)
    expect(label).not.toHaveTextContent('Черновик')
  })

  it('gives the full digest to screen readers and hides the short form from them', () => {
    show(strictSource)

    expect(screen.getByText(strictSource.data_sha256)).toHaveClass('sr-only')
    expect(screen.getByText('0123456789ab…')).toHaveAttribute('aria-hidden', 'true')
    expect(screen.getByText('SHA-256 данных')).toHaveClass('sr-only')
  })

  it('says in words that a draft is not verified', () => {
    const { container } = show(draftSource)

    expect(container.querySelector('[data-profile="draft"]')).not.toBeNull()
    expect(screen.getByText(/Черновик: значения не прошли верификацию, результат нельзя считать проверенным/)).toBeInTheDocument()
    expect(screen.getByText('ВРЕМЕННЫЕ ДАННЫЕ').className).toContain('border-dashed')
  })

  it('shows the interim label without a digest when the source has none', () => {
    const { container } = show({ kind: 'interim', profile: 'strict' })

    expect(container).toHaveTextContent('профиль strict')
    expect(container).not.toHaveTextContent('…')
  })

  it('shows an interim source without a profile', () => {
    const { container } = show({ kind: 'interim' })

    expect(container.querySelector('[data-source="interim"]')).not.toHaveAttribute('data-profile')
  })

  it('speaks English', () => {
    show(draftSource, 'en')

    expect(screen.getByText('INTERIM DATA')).toBeInTheDocument()
    expect(screen.getByText(/Draft: the values have not been verified/)).toBeInTheDocument()
  })

  it.each([
    ['catalog', catalogSource],
    ['strict', strictSource],
    ['draft', draftSource],
  ])('has no axe violations for %s', async (_, source) => {
    const { container } = show(source)
    await expectNoA11yViolations(container)
  })
})

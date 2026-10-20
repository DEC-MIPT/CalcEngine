import { render } from '@testing-library/react'
import { createElement } from 'react'
import { describe, expect, it } from 'vitest'
import { LanguageSwitch } from '@/components/LanguageSwitch'
import { I18nProvider } from '@/i18n/I18nProvider'
import { expectNoA11yViolations } from './axe'

describe('expectNoA11yViolations', () => {
  it('passes for a labelled control', async () => {
    const { container } = render(
      <I18nProvider>
        <LanguageSwitch />
      </I18nProvider>,
    )
    await expectNoA11yViolations(container)
  })

  it('fails for an input without a label', async () => {
    const { container } = render(createElement('input', { type: 'text' }))
    await expect(expectNoA11yViolations(container)).rejects.toThrow(/label/i)
  })
})

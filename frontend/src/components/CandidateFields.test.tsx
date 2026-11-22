import { render, screen } from '@testing-library/react'
import { expect, it, vi } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import { CANDIDATE_LIMIT } from '@/lib/foundationDesign'
import { CandidateFields } from './CandidateFields'

it('prevents adding a 257th row without removing existing rows', () => {
  const rows = Array.from({ length: CANDIDATE_LIMIT }, (_, id) => ({ id, b: '2', l: '3', bUnit: 'm', lUnit: 'm' }))
  const change = vi.fn()
  const { container } = render(<I18nProvider><CandidateFields candidates={rows} dimensions={[]} errors={{}} locked={false} onChange={change} /></I18nProvider>)
  expect(screen.getByRole('button', { name: 'Добавить вариант' })).toBeDisabled()
  expect(container.querySelectorAll('input')).toHaveLength(512)
  expect(change).not.toHaveBeenCalled()
})

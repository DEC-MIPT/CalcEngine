import { act, renderHook } from '@testing-library/react'
import type { ReactNode } from 'react'
import { describe, expect, it, vi } from 'vitest'
import { DraftProvider } from './DraftProvider'
import { useDraft } from './draftContext'

const wrapper = ({ children }: { children: ReactNode }) => <DraftProvider>{children}</DraftProvider>

describe('form draft (9.2a)', () => {
  it('starts empty for every type and keeps values and units apart by type', () => {
    const { result } = renderHook(() => useDraft(), { wrapper })

    act(() => {
      result.current.setValue('a', 'x', '1')
      result.current.setUnit('a', 'x', 'mm')
      result.current.setValue('a', 'y', '2')
    })

    expect(result.current.read('a')).toEqual({ values: { x: '1', y: '2' }, units: { x: 'mm' } })
    expect(result.current.read('b')).toEqual({ values: {}, units: {} })
  })

  it('remembers the result that the draft was last sent for', () => {
    const { result } = renderHook(() => useDraft(), { wrapper })
    expect(result.current.sent).toBeNull()

    act(() => result.current.remember('r-1', 'a'))

    expect(result.current.sent).toEqual({ resultId: 'r-1', type: 'a' })
  })

  it('throws outside the provider', () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})

    expect(() => renderHook(() => useDraft())).toThrow('useDraft must be used inside DraftProvider')
  })
})

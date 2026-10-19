import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useSendingHints } from './useSendingHints'

beforeEach(() => vi.useFakeTimers())
afterEach(() => vi.useRealTimers())

describe('sending hints (9.5)', () => {
  it('says nothing while no request is sent', () => {
    const { result } = renderHook(() => useSendingHints(false))

    act(() => vi.advanceTimersByTime(20_000))

    expect(result.current).toBeNull()
  })

  it('moves from sending to slow after 3 seconds and to longer after 10, counted from the submit', () => {
    const { result } = renderHook(() => useSendingHints(true))
    expect(result.current).toBe('sending')

    act(() => vi.advanceTimersByTime(2_999))
    expect(result.current).toBe('sending')
    act(() => vi.advanceTimersByTime(1))
    expect(result.current).toBe('slow')

    act(() => vi.advanceTimersByTime(6_999))
    expect(result.current).toBe('slow')
    act(() => vi.advanceTimersByTime(1))
    expect(result.current).toBe('longer')
  })

  it('starts again from sending for the next request', () => {
    const { result, rerender } = renderHook(({ active }) => useSendingHints(active), {
      initialProps: { active: true },
    })
    act(() => vi.advanceTimersByTime(11_000))
    expect(result.current).toBe('longer')

    rerender({ active: false })
    expect(result.current).toBeNull()
    rerender({ active: true })

    expect(result.current).toBe('sending')
  })
})

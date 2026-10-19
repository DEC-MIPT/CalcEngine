import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { markPlayed, resetPlayed, stepInterval } from './playback'
import { useTracePlayback } from './useTracePlayback'

function motion(reduce: boolean) {
  vi.stubGlobal('matchMedia', () => ({ matches: reduce }))
}

function press(key: string, target: EventTarget = document.body) {
  const event = new KeyboardEvent('keydown', { key, bubbles: true, cancelable: true })
  act(() => {
    target.dispatchEvent(event)
  })
  return event
}

beforeEach(() => {
  vi.useFakeTimers()
  motion(false)
})

afterEach(() => {
  vi.useRealTimers()
  vi.unstubAllGlobals()
  resetPlayed()
  document.body.innerHTML = ''
})

describe('useTracePlayback', () => {
  it('shows the steps one by one and ends after the last', () => {
    const { result } = renderHook(() => useTracePlayback('r1', 3))
    expect(result.current).toMatchObject({ shown: 0, phase: 'playing' })

    act(() => vi.advanceTimersByTime(stepInterval(3)))
    expect(result.current.shown).toBe(1)
    act(() => vi.advanceTimersByTime(stepInterval(3)))
    act(() => vi.advanceTimersByTime(stepInterval(3)))

    expect(result.current).toMatchObject({ shown: 3, phase: 'ended' })
  })

  it('shows everything at once under reduced motion', () => {
    motion(true)

    const { result } = renderHook(() => useTracePlayback('r1', 3))

    expect(result.current).toMatchObject({ shown: 3, phase: 'idle' })
  })

  it('does not play a result already played in this session', () => {
    markPlayed('r1')

    const { result } = renderHook(() => useTracePlayback('r1', 3))

    expect(result.current).toMatchObject({ shown: 3, phase: 'idle' })
  })

  it('marks the result as played on its first showing', () => {
    renderHook(() => useTracePlayback('r1', 3)).unmount()

    const { result } = renderHook(() => useTracePlayback('r1', 3))

    expect(result.current.phase).toBe('idle')
  })

  it('does not play an empty trace', () => {
    const { result } = renderHook(() => useTracePlayback('r1', 0))

    expect(result.current).toMatchObject({ shown: 0, phase: 'idle' })
  })

  it('skips by its function', () => {
    const { result } = renderHook(() => useTracePlayback('r1', 3))

    act(() => result.current.skip())

    expect(result.current).toMatchObject({ shown: 3, phase: 'skipped' })
  })

  it.each([' ', 'Enter', 'Escape'])('skips on %j and keeps the page from scrolling', (key) => {
    const { result } = renderHook(() => useTracePlayback('r1', 3))

    const event = press(key)

    expect(event.defaultPrevented).toBe(true)
    expect(result.current).toMatchObject({ shown: 3, phase: 'skipped' })
  })

  it('skips on a key pressed on a control without taking the key from it', () => {
    const button = document.body.appendChild(document.createElement('button'))
    const { result } = renderHook(() => useTracePlayback('r1', 3))

    const event = press(' ', button)

    expect(event.defaultPrevented).toBe(false)
    expect(result.current.phase).toBe('skipped')
  })

  it('skips on a click anywhere on the page', () => {
    const { result } = renderHook(() => useTracePlayback('r1', 3))

    act(() => {
      document.body.click()
    })

    expect(result.current).toMatchObject({ shown: 3, phase: 'skipped' })
  })

  it('stops listening to clicks once the playback is over', () => {
    const { result } = renderHook(() => useTracePlayback('r1', 3))
    for (let step = 0; step < 3; step += 1) act(() => vi.advanceTimersByTime(stepInterval(3)))

    act(() => {
      document.body.click()
    })

    expect(result.current.phase).toBe('ended')
  })

  it('skips on Tab and leaves the focus move to the browser', () => {
    const { result } = renderHook(() => useTracePlayback('r1', 3))

    const event = press('Tab')

    expect(event.defaultPrevented).toBe(false)
    expect(result.current).toMatchObject({ shown: 3, phase: 'skipped' })
  })

  it('ignores other keys', () => {
    const { result } = renderHook(() => useTracePlayback('r1', 3))

    const event = press('a')

    expect(event.defaultPrevented).toBe(false)
    expect(result.current.phase).toBe('playing')
  })

  it('stops listening to the keys once the playback is over', () => {
    renderHook(() => useTracePlayback('r1', 1))
    act(() => vi.advanceTimersByTime(stepInterval(1)))

    expect(press(' ').defaultPrevented).toBe(false)
  })
})

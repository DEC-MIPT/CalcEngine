import { afterEach, describe, expect, it, vi } from 'vitest'
import { prefersReducedMotion, withMinimumDuration } from './motion'

afterEach(() => {
  vi.useRealTimers()
  vi.unstubAllGlobals()
})

describe('prefersReducedMotion (UX bold pass, zone 2)', () => {
  it('treats a browser without matchMedia as asking for reduced motion', () => {
    vi.stubGlobal('matchMedia', undefined)

    expect(prefersReducedMotion()).toBe(true)
  })

  it.each([true, false])('follows the media query when it is available (matches: %s)', (matches) => {
    const query = vi.fn(() => ({ matches }))
    vi.stubGlobal('matchMedia', query)

    expect(prefersReducedMotion()).toBe(matches)
    expect(query).toHaveBeenCalledWith('(prefers-reduced-motion: reduce)')
  })
})

describe('withMinimumDuration (UX bold pass, zone 2)', () => {
  it('waits for the pause when the work is faster', async () => {
    vi.useFakeTimers()
    let done = false
    const run = withMinimumDuration(Promise.resolve('value'), 700).then((value) => {
      done = true
      return value
    })

    await vi.advanceTimersByTimeAsync(699)
    expect(done).toBe(false)
    await vi.advanceTimersByTimeAsync(1)

    await expect(run).resolves.toBe('value')
  })

  it('waits for the work when it is slower than the pause', async () => {
    vi.useFakeTimers()
    const work = new Promise<string>((resolve) => setTimeout(() => resolve('late'), 1500))
    const run = withMinimumDuration(work, 700)

    await vi.advanceTimersByTimeAsync(1500)

    await expect(run).resolves.toBe('late')
  })

  it('returns the work itself without a pause of zero', () => {
    const work = Promise.resolve(1)

    expect(withMinimumDuration(work, 0)).toBe(work)
  })

  it('passes a failure of the work on', async () => {
    await expect(withMinimumDuration(Promise.reject(new Error('boom')), 10)).rejects.toThrow('boom')
  })
})

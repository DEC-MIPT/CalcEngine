import { describe, expect, it } from 'vitest'
import { cn } from './utils'

describe('cn', () => {
  it('joins class names and lets the later Tailwind class win', () => {
    expect(cn('p-2', undefined, { hidden: false }, 'p-4')).toBe('p-4')
  })
})

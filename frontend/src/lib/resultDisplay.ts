import { createContext, useContext } from 'react'
import type { components } from '@/api/schema'

const DEMO_ROUNDING: components['schemas']['RoundingRule'] = { decimals: 2, mode: 'half_up' }

export const DemoResultDisplay = createContext(false)

export function useResultRounding() {
  return useContext(DemoResultDisplay) ? DEMO_ROUNDING : undefined
}

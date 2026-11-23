import { createContext, useContext } from 'react'
import type { WEIGHTS_EXAMPLE } from '@/lib/foundationDesign'

export interface FormDraft {
  values: Readonly<Record<string, string>>
  units: Readonly<Record<string, string>>
}

export interface SentForm {
  resultId: string
  type: string
  example?: typeof WEIGHTS_EXAMPLE
}

export type CandidateDraft = { id: number; b: string; l: string; bUnit: string; lUnit: string }

export interface Draft {
  candidates: readonly CandidateDraft[]
  setCandidates: (candidates: readonly CandidateDraft[]) => void
  read: (type: string) => FormDraft
  setValue: (type: string, name: string, text: string) => void
  setUnit: (type: string, name: string, unit: string) => void
  sent: SentForm | null
  remember: (resultId: string, type: string, example?: SentForm['example']) => void
}

export const DraftContext = createContext<Draft | null>(null)

export function useDraft(): Draft {
  const value = useContext(DraftContext)
  if (value === null) {
    throw new Error('useDraft must be used inside DraftProvider')
  }
  return value
}

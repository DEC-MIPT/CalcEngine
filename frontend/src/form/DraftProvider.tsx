import { useCallback, useMemo, useState, type ReactNode } from 'react'
import { DraftContext, type Draft, type FormDraft, type SentForm } from './draftContext'

const EMPTY: FormDraft = { values: {}, units: {} }

export function DraftProvider({ children }: { children: ReactNode }) {
  const [drafts, setDrafts] = useState<Readonly<Record<string, FormDraft>>>({})
  const [sent, setSent] = useState<SentForm | null>(null)

  const read = useCallback((type: string) => drafts[type] ?? EMPTY, [drafts])
  const setValue = useCallback((type: string, name: string, text: string) => {
    setDrafts((current) => {
      const draft = current[type] ?? EMPTY
      return { ...current, [type]: { ...draft, values: { ...draft.values, [name]: text } } }
    })
  }, [])
  const setUnit = useCallback((type: string, name: string, unit: string) => {
    setDrafts((current) => {
      const draft = current[type] ?? EMPTY
      return { ...current, [type]: { ...draft, units: { ...draft.units, [name]: unit } } }
    })
  }, [])
  const remember = useCallback((resultId: string, type: string) => setSent({ resultId, type }), [])

  const value = useMemo<Draft>(
    () => ({ read, setValue, setUnit, sent, remember }),
    [read, setValue, setUnit, sent, remember],
  )
  return <DraftContext.Provider value={value}>{children}</DraftContext.Provider>
}

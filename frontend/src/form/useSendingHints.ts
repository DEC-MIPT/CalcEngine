import { useEffect, useState } from 'react'

export type SendingStage = 'sending' | 'slow' | 'longer'

const SLOW_AFTER_MS = 3_000
const LONGER_AFTER_MS = 10_000

export function useSendingHints(active: boolean): SendingStage | null {
  const [stage, setStage] = useState<SendingStage>('sending')
  useEffect(() => {
    if (!active) return
    const slow = setTimeout(() => setStage('slow'), SLOW_AFTER_MS)
    const longer = setTimeout(() => setStage('longer'), LONGER_AFTER_MS)
    return () => {
      clearTimeout(slow)
      clearTimeout(longer)
      setStage('sending')
    }
  }, [active])
  return active ? stage : null
}

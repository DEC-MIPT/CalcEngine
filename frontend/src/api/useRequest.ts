import { useEffect, useState } from 'react'
import type { ApiError, ApiResult } from './client'

export type RequestState<T> =
  | { status: 'loading' }
  | { status: 'ok'; data: T }
  | { status: 'error'; error: ApiError }

interface Settled<T> {
  load: () => Promise<ApiResult<T>>
  attempt: number
  result: ApiResult<T>
}

export function useRequest<T>(load: () => Promise<ApiResult<T>>): {
  state: RequestState<T>
  retry: () => void
} {
  const [attempt, setAttempt] = useState(0)
  const [settled, setSettled] = useState<Settled<T> | null>(null)

  useEffect(() => {
    let current = true
    void load().then((result) => {
      if (current) setSettled({ load, attempt, result })
    })
    return () => {
      current = false
    }
  }, [load, attempt])

  let state: RequestState<T> = { status: 'loading' }
  if (settled !== null && settled.load === load && settled.attempt === attempt) {
    state = settled.result.ok
      ? { status: 'ok', data: settled.result.data }
      : { status: 'error', error: settled.result.error }
  }
  return { state, retry: () => setAttempt((value) => value + 1) }
}

import { useLayoutEffect, useRef } from 'react'

export function useFocusOnMount<T extends HTMLElement>(enabled = true) {
  const ref = useRef<T>(null)
  useLayoutEffect(() => {
    if (enabled) ref.current?.focus({ preventScroll: true })
    // eslint-disable-next-line react-hooks/exhaustive-deps -- focus once, on arrival
  }, [])
  return ref
}

import { Formula } from './Formula'

export function NamedSymbol({ name, latex, presentation }: { name: string; latex: string | undefined; presentation?: string | null }) {
  if (latex === undefined) return <code>{name}</code>
  return (
    <>
      <span aria-hidden="true">
        <Formula latex={latex} presentation={presentation} />
      </span>
      <span className="sr-only">{name}</span>
    </>
  )
}

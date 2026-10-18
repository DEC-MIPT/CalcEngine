import { Formula } from './Formula'

export function NamedSymbol({ name, latex }: { name: string; latex: string | undefined }) {
  if (latex === undefined) return <code>{name}</code>
  return (
    <>
      <span aria-hidden="true">
        <Formula latex={latex} />
      </span>
      <span className="sr-only">{name}</span>
    </>
  )
}

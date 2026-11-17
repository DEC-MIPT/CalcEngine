import type { components } from '@/api/schema'
import type { Language } from '@/i18n/dictionary'
import { pickText } from '@/i18n/translate'

type CalculationType = components['schemas']['CalculationTypeView']

export function outputLabels(types: readonly CalculationType[], language: Language): ReadonlyMap<string, string> {
  const labels = new Map<string, string | null>()
  for (const type of types) {
    for (const output of type.outputs) {
      const label = pickText(output.label, language)
      const known = labels.get(output.name)
      labels.set(output.name, known === undefined || known === label ? label : null)
    }
  }
  return new Map([...labels].filter((entry): entry is [string, string] => entry[1] !== null))
}

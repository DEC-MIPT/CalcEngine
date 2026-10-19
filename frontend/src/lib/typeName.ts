import type { components } from '@/api/schema'
import type { Language } from '@/i18n/dictionary'
import { pickText } from '@/i18n/translate'

type CalculationType = components['schemas']['CalculationTypeView']

export function typeName(type: CalculationType, language: Language): string {
  return type.outputs.map((output) => pickText(output.label, language)).join(' · ')
}

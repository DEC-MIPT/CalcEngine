import type { components } from '@/api/schema'
import { ru, en, type Language } from '@/i18n/dictionary'
import { LOADS_TYPE, WEIGHTS_TYPE } from './foundationDesign'
import { pickText } from '@/i18n/translate'

type CalculationType = components['schemas']['CalculationTypeView']

export function typeName(type: CalculationType, language: Language): string {
  const mode = type.name === LOADS_TYPE ? 'foundation.averaged' : type.name === WEIGHTS_TYPE ? 'foundation.explicit' : null
  const output = type.outputs.map((output) => pickText(output.label, language)).join(' · ')
  if (!mode) return output
  const modeName = language === 'en' ? en[mode] ?? ru[mode] : ru[mode]
  return `${output} — ${modeName}`
}

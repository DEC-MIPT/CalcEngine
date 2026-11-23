import type { components } from '@/api/schema'
import { calculationFormUrl, WEIGHTS_EXAMPLE, WEIGHTS_TYPE } from '@/lib/foundationDesign'
import type { FormDraft } from './draftContext'

const quantities = {
  b: [2, 'm'],
  d_1: [1, 'm'],
  d_b: [0, 'm'],
  gamma_II: [20, 'kN/m3'],
  gamma_II_prime: [20, 'kN/m3'],
  c_II: [10, 'kPa'],
  phi_II: [20, 'deg'],
  l: [3, 'm'],
  h: [1, 'm'],
  N: [600, 'kN'],
  Mx: [0, 'kN*m'],
  My: [0, 'kN*m'],
  Qx: [0, 'kN'],
  Qy: [0, 'kN'],
  G_fund: [60, 'kN'],
  G_soil: [40, 'kN'],
  G_other: [20, 'kN'],
  Mx_add_base: [0, 'kN*m'],
  My_add_base: [0, 'kN*m'],
} satisfies Record<string, readonly [number, components['schemas']['QuantityValue']['unit']]>

export const foundationExampleDraft: FormDraft = {
  values: Object.fromEntries(Object.entries(quantities).map(([key, [value]]) => [key, String(value)])),
  units: Object.fromEntries(Object.entries(quantities).map(([key, [, unit]]) => [key, unit])),
}

export const foundationExampleKey = calculationFormUrl(WEIGHTS_TYPE, WEIGHTS_EXAMPLE)

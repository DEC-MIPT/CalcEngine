export const LOADS_TYPE = 'foundations_shallow_loads'
export const WEIGHTS_TYPE = 'foundations_shallow_weights'
export const CANDIDATE_LIMIT = 256

export const selectionPolicy = {
  calculation_type: LOADS_TYPE,
  schema_version: 'foundation-selection-request-v1',
  policy_version: 'foundation-min-area-v1',
} as const

export const isFoundationType = (name: string | null) => name === LOADS_TYPE || name === WEIGHTS_TYPE

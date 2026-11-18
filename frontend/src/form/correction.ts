import type { components } from '@/api/schema'
import type { BoundShape } from '@/components/Bound'

export interface DerivedCorrection {
  resultId: string
  reason: components['schemas']['DerivedViolation']
}

export interface FormCorrectionState {
  bound?: BoundShape
  derivedCorrection?: DerivedCorrection
}

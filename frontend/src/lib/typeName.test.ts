import { expect, it } from 'vitest'
import { weightsCalculationType } from '@/mocks/designFixtures'
import { loadsCalculationType } from '@/mocks/loadsFixtures'
import { typeName } from './typeName'

it('distinguishes foundation modes even though their outputs are the same', () => {
  expect(typeName(loadsCalculationType, 'en')).toMatch(/Averaged weights$/)
  expect(typeName(weightsCalculationType, 'en')).toMatch(/Explicit weights$/)
})

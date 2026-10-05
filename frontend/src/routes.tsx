import type { RouteObject } from 'react-router'
import { CalculationFormScreen } from './screens/CalculationFormScreen'
import { NotFoundScreen } from './screens/NotFoundScreen'
import { ReportScreen } from './screens/ReportScreen'
import { ResultScreen } from './screens/ResultScreen'
import { TypeSelectionScreen } from './screens/TypeSelectionScreen'

export const routes: RouteObject[] = [
  { path: '/', element: <TypeSelectionScreen /> },
  { path: '/calculations/new', element: <CalculationFormScreen /> },
  { path: '/calculations/:id', element: <ResultScreen /> },
  { path: '/calculations/:id/report', element: <ReportScreen /> },
  { path: '*', element: <NotFoundScreen /> },
]

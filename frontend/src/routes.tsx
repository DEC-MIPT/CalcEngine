import type { RouteObject } from 'react-router'
import { AppShell, type Crumb } from './components/AppShell'
import { CalculationFormScreen } from './screens/CalculationFormScreen'
import { NotFoundScreen } from './screens/NotFoundScreen'
import { ReportScreen } from './screens/ReportScreen'
import { ResultScreen } from './screens/ResultScreen'
import { TypeSelectionScreen } from './screens/TypeSelectionScreen'

const trail = (...crumbs: Crumb[]) => ({ trail: crumbs })

export const routes: RouteObject[] = [
  {
    element: <AppShell />,
    children: [
      { path: '/', element: <TypeSelectionScreen /> },
      { path: '/calculations/new', element: <CalculationFormScreen />, handle: trail('form') },
      { path: '/calculations/:id', element: <ResultScreen />, handle: trail('result') },
      { path: '/calculations/:id/report', element: <ReportScreen />, handle: trail('result', 'report') },
      { path: '*', element: <NotFoundScreen />, handle: trail('notFound') },
    ],
  },
]

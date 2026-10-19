import { StrictMode, useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { api, unwrap } from '@/api/client'
import { Formula } from '@/components/Formula'
import { PASS_ID } from '@/mocks/fixtures'

type Step = { step_id: string; expression: string }

const loadResult = () => unwrap(api.GET('/calculations/{result_id}', { params: { path: { result_id: PASS_ID } } }))

export function Steps() {
  const [trace, setTrace] = useState<Step[] | null>(null)
  useEffect(() => {
    void loadResult().then((result) => {
      if (result.ok && 'trace' in result.data) setTrace(result.data.trace)
    })
  }, [])
  if (!trace) return <p>loading</p>
  return (
    <ol>
      {trace.map((step, index) => (
        <li key={`${step.step_id}-${index}`} data-step={step.step_id}>
          <Formula latex={step.expression} />
        </li>
      ))}
    </ol>
  )
}

async function start() {
  const { worker } = await import('@/mocks/browser')
  await worker.start({ onUnhandledRequest: 'bypass' })
  createRoot(document.getElementById('root')!).render(
    <StrictMode>
      <Steps />
    </StrictMode>,
  )
}

void start()

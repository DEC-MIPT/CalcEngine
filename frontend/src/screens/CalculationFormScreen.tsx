import { useSearchParams } from 'react-router'

export function CalculationFormScreen() {
  const [params] = useSearchParams()
  return (
    <>
      <h1>Calculation inputs</h1>
      <p>{params.get('type')}</p>
    </>
  )
}

import { useParams } from 'react-router'

export function ResultScreen() {
  const { id } = useParams()
  return (
    <>
      <h1>Calculation result</h1>
      <p>{id}</p>
    </>
  )
}

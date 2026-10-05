import { useParams } from 'react-router'

export function ReportScreen() {
  const { id } = useParams()
  return (
    <>
      <h1>Report request</h1>
      <p>{id}</p>
    </>
  )
}

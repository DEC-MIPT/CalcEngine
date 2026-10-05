import { Link } from 'react-router'

export function NotFoundScreen() {
  return (
    <>
      <h1>Page not found</h1>
      <Link to="/">Calculation types</Link>
    </>
  )
}

import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import App from './App'

describe('App', () => {
  it('opens the type selection at the root address', () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: 'Calculation types' })).toBeInTheDocument()
  })
})

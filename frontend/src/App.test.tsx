import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import App from './App'

describe('App', () => {
  it('opens the type selection at the root address', async () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: 'Выберите тип расчёта' })).toBeInTheDocument()
    await screen.findByRole('link', { name: 'Расчётное сопротивление грунта' })
  })
})

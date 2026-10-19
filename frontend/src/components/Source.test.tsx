import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { I18nProvider } from '@/i18n/I18nProvider'
import { Source } from './Source'

function show(source: Parameters<typeof Source>[0]['source']) {
  return render(
    <I18nProvider initialLanguage="ru">
      <Source source={source} />
    </I18nProvider>,
  )
}

describe('Source', () => {
  it('lists the norm references of a source taken from a norm, with their status', () => {
    show([{ document: 'SP Test', edition: '2020', clause: '5.6', status: 'verified', provenance: 'human-verified' }])

    expect(screen.getByText('SP Test')).toBeInTheDocument()
    expect(screen.getByText('редакция: 2020')).toBeInTheDocument()
    expect(screen.getByText('пункт: 5.6')).toBeInTheDocument()
    expect(screen.getByText('проверено')).toBeInTheDocument()
    expect(screen.queryByText('Задано инженером')).not.toBeInTheDocument()
  })

  it('names the engineer and the rationale of an engineer-set source', () => {
    show({ engineer: 'Аким', rationale: 'Пилот' })

    expect(screen.getByText('Задано инженером')).toBeInTheDocument()
    expect(screen.getByText('Инженер: Аким')).toBeInTheDocument()
    expect(screen.getByText('Обоснование: Пилот')).toBeInTheDocument()
  })
})

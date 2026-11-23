import { render, screen, within } from '@testing-library/react'
import { expect, it } from 'vitest'
import type { components } from '@/api/schema'
import { I18nProvider } from '@/i18n/I18nProvider'
import { DemoResultDisplay } from '@/lib/resultDisplay'
import { NormRefList } from './NormRefList'

type Ref = components['schemas']['NormRef']
const table: Ref = { document: 'СП 22.13330.2016', edition: '2016', clause: 'таблица 5.4', status: 'verified', provenance: 'human-verified' }
const formula: Ref = { ...table, clause: 'формула (5.7)', status: 'unverified' }

it('groups SP 22 by edition, retains per-locator status and does not repeat identical locators', () => {
  render(<I18nProvider><DemoResultDisplay.Provider value>
    <NormRefList refs={[table, formula, table, { ...formula, edition: 'unverified' }, { ...table, document: 'СП 24' }]} />
  </DemoResultDisplay.Provider></I18nProvider>)
  const [group, otherEdition, otherDocument] = screen.getAllByRole('listitem')
  expect(within(group).getAllByText(table.document, { exact: true })).toHaveLength(1)
  expect(group).toHaveTextContent(/таблица 5\.4 проверено; формула \(5\.7\) не проверено/)
  expect(otherEdition).toHaveTextContent('редакция: не подтверждена')
  expect(otherDocument).toHaveTextContent('СП 24')
})

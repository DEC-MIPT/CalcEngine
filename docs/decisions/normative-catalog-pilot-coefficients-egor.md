# Pilot coefficients `γc1`, `γc2`, `k`, `kz`: check against the primary text (WP9, task 2.5)

- Date: 2026-10-05
- From: Egor (data zone). Owner of the record: Egor.
- Change: `openspec/changes/normative-catalog-backend/`, task 2.5.
- Purpose: name, for each coefficient the pilot `foundations_shallow_r` uses, the document,
  the edition, and the clause or table it was found in, and who checked it. The stored rows
  keep `provenance = machine-extracted` and `status = unverified`: raising a status is the
  gate of `norm-source-traceability` (WP3), not of this change.

## Source

- Document: СП 22.13330.2016 "Основания зданий и сооружений".
- Edition: the ingested PDF is the **base 2016 edition without amendments** (title page:
  приказ Минстрой России от 16 декабря 2016 г. № 970/пр; no "с Изменениями N …" line
  on pages 1-5). The pipeline confirms this: `extract_amendments()` returns `[]` for this
  file, so `document.edition = '2016'`. Akim's copy includes amendments 1-5; formula (5.7)
  is marked "Измененная редакция, Изм. № 5" there, meaning the formula may differ from
  what the base text and the current catalog contain. The current catalog therefore reflects
  the base 2016 text only. Re-ingestion with the consolidated text (amendments 1-5 or
  current) will update `document.edition` automatically once that file is available.
  `unverified` under `agent-docs/domain-constraints.md` until WP3 checks it against the
  paper primary text.
- File checked: `docs/normative-base/СП 22.13330.2016.pdf`, clause 5.6.7 (printed page 35),
  table 5.4 (page 35) and table 5.5 (printed page 36).
- Checked by: Egor (data engineer), 2026-10-05; edition clarified 2026-10-07.

## What the primary text says, and what the catalog stores

| Parameter | Clause / table | Wording in the primary text | Stored value(s) |
|---|---|---|---|
| `γc1`, `γc2` | 5.6.7, table 5.4 | "γc1 и γc2 – коэффициенты условий работы, принимаемые по таблице 5.4" | `γc1 = 1.1`, `γc2 = 1.0` (one row each, no heading) |
| `k` | 5.6.7 | "k – коэффициент, принимаемый равным единице, если прочностные характеристики грунта (φII и сII) определены непосредственными испытаниями, и k = 1,1, если они приняты по таблицам приложения А" | `k = 1.0` (one row, no heading) |
| `kz` | 5.6.7 | "kz – коэффициент, принимаемый равным единице при b < 10 м; kz = z0/b + 0,2 при b ≥ 10 м (здесь z0 = 8 м)" | `kz = 1` for `b < 10 м`; `kz = 8/b + 0.2` for `b ≥ 10 м`; threshold `b0 = 10 м` |
| `Mγ`, `Mq`, `Mc` | 5.6.7, table 5.5 | "Мγ, Мq, Мс – коэффициенты, принимаемые по таблице 5.5" | 46 rows, heading `φII` from 0° to 45° in `deg`, columns `Mγ`, `Mq`, `Mc` |

Each stored row carries its `NormRef` (`document = СП 22.13330.2016`, `edition = 2016`,
`clause = табл. 5.4` / `5.6.7` / `табл. 5.5`, `status = unverified`,
`provenance = machine-extracted`).

## Notes on the choices

- **`γc1`, `γc2`.** The pilot declares no input that selects a soil type, so each is one
  row without a heading (design decision 2, "one row with null headings for a parameter
  that no input selects"). `γc2 = 1.0` is fixed for a structure of flexible structural
  scheme (table 5.4, note 2) and for the L/H ≤ 1.5 column, and is the value of all three
  reference examples. `γc1 = 1.1` is the value of the table 5.4 rows for пылеватые пески
  (насыщенные водой) and for глинистые грунты with IL > 0.5; the exact soil row of the
  pilot's reference case is `unverified` and is to be pinned with the reference example
  (WP4), not here.
- **`k`.** `k = 1.0` assumes φII and сII are obtained by direct tests, which is the case
  of the three reference examples. The other branch (`k = 1.1`, characteristics from the
  tables of appendix A) is recorded in the text but not stored: the pilot has no input
  that selects it.
- **`kz`.** The two branches and the `b0 = 10 м` break are stored as two `Formula` rows
  bound to parameter `k_z_below` / `k_z_from` and one `Threshold` `k_z_threshold`, all
  with clause 5.6.7. Their numbers (`5.6.7#k_z_below`, `5.6.7#k_z_from`) are pipeline
  synthetic ids for the inline definitions of clause 5.6.7, not printed formula numbers.
- **Method range.** No clause of 5.6.7 states a numeric range for formula (5.7). The method
  uses `Mγ`, `Mq`, `Mc` from table 5.5, which the norm defines only for `φII` from 0° to
  45°; outside that interval the norm gives no coefficients, so the method does not apply.
  The stored method bounds are therefore `φII ∈ [0°, 45°]`, inclusive, clause 5.6.7, table
  5.5. No bound is stored on `b`: the `kz` break at 10 м is inside the method, not a range
  limit.

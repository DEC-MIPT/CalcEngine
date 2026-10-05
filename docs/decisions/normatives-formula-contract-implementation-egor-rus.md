# `normatives-formula-contract` 1.4–1.7: передача реализации Акиму (2026-10-04)

- Дата: 2026-10-04
- От: Егор. Кому: Аким (и его агенты).
- Ветка: `feature/normative-formula-contract/data` (пока не влита).
- Объём: `openspec/changes/normatives-formula-contract/tasks.md`, задачи 1.4–1.7.
- Цель: точно описать агентам Акима, что хранится, как это строится и как это проверить,
  чтобы backend WP9 (`normative-catalog-backend`) мог это использовать без догадок.

Английская версия: `normatives-formula-contract-implementation-egor.md`. Перевод сделал
Аким 2026-10-05. Отличие от оригинала: в командах раздела 4 адрес базы и `psql` записаны
без пароля, он берётся из окружения (ревью WP9, m6).

## 1. Что изменилось (задачи 1.4–1.7)

1.4 `build_formula_payload` всегда строит пять фиксированных полей `NormRef`
(`document`, `edition`, `clause`, `status`, `provenance`); `norm_ref_keys` в `[output]`
теперь только добавляет поля сверх этих пяти и никогда их не отфильтровывает.

1.5 У `coefficient` появились `edition`, `clause`, `status`, `provenance` (плюс
`document` через соединение по `document_id`). `build_coefficient_norm_ref` и
`build_coefficient_payload` строят `NormRef` из пяти полей для каждого значения.

1.6 У `formula` появились колонки `status`, `provenance`. Записи `formulas.toml`
хранятся как `status=verified`, `provenance=human-verified`; результат OCR — как
`status=unverified`, `provenance=machine-extracted`. Payload читает сохранённые колонки,
а не константы.

1.7 Формула или коэффициент без `document` вызывает `RuntimeError` (payload никогда не
строится из пустой строки); пустое обозначение документа прерывает загрузку.

Дополнительно (не входит в 1.4–1.7, но нужно для инварианта `NormRef`
`status=verified ⇒ редакция и пункт конкретные`): `designation` и `edition` теперь
извлекаются из текста титульной страницы, а не из имени файла. `parser/text_layer.py`:
`extract_designation()` (регулярное выражение `СП NN.NNNNN.YYYY` по первым трём
страницам) и `extract_edition_year()` (`YYYY` из обозначения). Если обозначения или года
нет, выбрасывается исключение.

## 2. Состояние базы (проверено на `dec-postgres`, база `dec`)

`document` (без изменений), плюс `edition`/`year`, заполненные по титульной странице. Для
пилота:

- `designation = 'СП 22.13330.2016'`, `edition = '2016'`, `year = 2016`.

Колонки `formula` теперь включают `status`, `provenance` (по умолчанию `unverified`,
`machine-extracted`). Колонки `coefficient` теперь включают `edition`, `clause`,
`status`, `provenance` (по умолчанию `unverified`, `''`, `unverified`,
`machine-extracted`).

`NormRef` (пять полей, без null, неизвестные редакция или пункт — литерал `unverified`):

```
{document, edition, clause, status, provenance}
```

- `clause` — один указатель в канонической грамматике: `форм. (N)`, `п. X` или
  `табл. N.N`.
- `status ∈ {verified, unverified}`, `provenance ∈ {human-verified, machine-extracted}`.

## 3. Как строятся payload (для справки, это не API, который импортирует Аким)

Backend НЕ импортирует код пайплайна (решение 1 WP9). Это собственные построители
пайплайна; backend Акима читает представления `catalog_read`, которые Егор создаёт в
задаче 2.6 WP9.

- `db.build_formula_payload(conn, formula) -> dict` — ключи из `[output] formula_keys`:
  `norm_ref`, `formula_id`, `latex`, `symbols`, `expression`, `cross_refs`.
- `db.build_coefficient_norm_ref(coefficient) -> dict` — пять полей `NormRef`.
- `db.build_coefficient_payload(coefficient) -> dict` — `table_number`, `page`,
  `row_index`, `col_index`, `value`, `norm_ref`.
- `db.fetch_coefficients(conn, doc_id, table_number) -> list[dict]` — сырые строки,
  соединённые с `document.designation` (каждая строка уже несёт все поля `NormRef`).
- `db.search_formulas` возвращает `document_id`, `designation`, `edition`, `status`,
  `provenance`, `latex`, `expression` и т. д. (поля, нужные `build_formula_payload`).

## 4. Как это проверить

Тесты (нужны venv и Postgres на `5433`; `DEC_DATABASE_URL` — адрес владельца базы `dec`,
пароль не пишется в команду):

```bash
cd ml
DEC_DATABASE_URL="$DEC_DATABASE_URL" ../.venv/bin/python -m pytest tests/ -q
```

Прямой SQL (таблица 5.5 СП 22.13330.2016; пароль `psql` берёт из `PGPASSWORD` или
`~/.pgpass`):

```bash
psql -h localhost -p 5433 -U dec -d dec -c "
SELECT c.table_number, c.row_index, c.col_index, c.value, c.clause, c.status, c.provenance
FROM coefficient c JOIN document d ON d.id=c.document_id
WHERE d.designation='СП 22.13330.2016' AND c.table_number='5.5'
ORDER BY c.row_index, c.col_index;"
```

Проверка глазами (поддерживаемые обзоры лежат в `ml/research/review/`, в контракт не
входят; пересоздаются командой `python -m research.make_review_html`, см.
`ml/research/VERIFY.md`):

- `ml/research/review/sp22_13330_2016.html` — пилотный СП 22.13330.2016: формула 5.7 и
  таблица 5.5, снимок PDF рядом с payload из базы и отрисованной формой.
- `ml/research/review/sp31_13330_2021.html` — СП 31.13330.2021: формула 9 и таблица 30.

## 5. Чего здесь ещё нет (раздел 2 WP9, следующая ветка Егора)

`normatives-formula-contract` 1.4–1.7 только готовит сырые таблицы. Следующее — задачи
WP9 (`feature/normative-catalog/data`), и в этот change они НЕ входят:

- 2.1 таблица привязки `foundations_shallow_r`;
- 2.2 JSON дерева выражения `tree` для каждой привязанной формулы;
- 2.4 заголовки таблицы 5.5 (`heading_symbol`/`heading_value`/`heading_unit`) и границы
  метода;
- 2.6 схема `catalog_read`, представления, функция `search` и роль
  `dec_normatives_reader`.

Пока 2.6 не появилась, у backend Акима нет `catalog_read` для чтения, и он должен
продолжать использовать свой синтетический контракт (решение 9 WP9). Этот change этого не
меняет.

## 6a. ПРЕДУПРЕЖДЕНИЕ Акиму: изменились `symbols[].id` для кириллических символов (честное предупреждение)

`symbols[].id` — ASCII-имя величины в SymPy: ключ связи формулы с её обозначениями и
идентификатор, который твой backend использует внутри `expression` и в SymPy. До
исправления `cyr_map` транслитерировал кириллические омоглифы в те же латинские буквы
(`с→s`, `а→a`, `е→e`, `р→r`, `у→u`, `к→k`), поэтому кириллический и латинский символ
давали **одинаковый** `id`: `notation_entry.symbol` был неоднозначен (один `id` →
несколько разных `latex`). На пилоте это было 8 групп коллизий при извлечении (11 с учётом
манифеста), все на индексах и буквах.

Исправление (`5918c30`, `parser/symbols.py`) добавляет суффикс `_cyr`, с сохранением
регистра, к любому символу, содержащему кириллицу; латиница не меняется. `latex`
по-прежнему отображает кириллицу через `\text{…}`:

| символ | старый `id` | новый `id` | `latex` |
|---|---|---|---|
| латинская `s` | `s` | `s` | `s` |
| кириллическая `с` | `s` | `s_cyr` | `\text{с}` |
| кириллическая `а` | `a` | `a_cyr` | `\text{а}` |
| кириллическая `К` | `K` | `K_cyr` | `\text{К}` |
| кириллическая `Н` | `H` (через словарь) | `N_cyr` | `\text{Н}` |

Что это значит для тебя конкретно:

1. **Id кириллических символов теперь другие.** Любое сопоставление или выражение,
   написанное под старые (совпадающие) id, нужно перевести на id с `_cyr`.
2. **Автоматически извлечённые кириллические id — отдельное пространство имён** от
   простых латинских id в твоём ручном `formulas.toml`. `s` (латиница) и `s_cyr`
   (кириллическая `с`) — *разные* величины; не объединяй их, если норма действительно не
   использует один символ.
3. **Миграция ручная и на живой базе `dec` НЕ запускалась.** Новые загрузки получают
   суффикс автоматически; существующие строки сохраняют старые id, пока не запущена
   `python -m normatives_pipeline.parser.cyrillic --apply` (по умолчанию пробный прогон).

## 6. Известные базовые ограничения (не регрессии 1.4–1.7)

- `extract_tables` хранит подписи таблиц, которые не может разобрать, с пустым
  `table_number`; такие ячейки (2077 из 2959 для пилота) группируются только по
  странице. Заголовки таблиц (`row_index` 0/1 таблицы 5.5) хранятся как обычные ячейки;
  их выделение — задача 2.4 WP9.
- `expression` по-прежнему пуст для формул, извлечённых OCR (решение 4 design); только
  записи `formulas.toml` несут `expression`.

## Ответы (Аким, 2026-10-05)

### 6a. Id кириллических символов

Принято. У backend нет собственного сопоставления с id символов: он читает id только из
каталога, а все id пилота латинские (`formulas.toml`), поэтому с моей стороны сейчас
ничего не меняется. Пока на живой `dec` не запущена `parser.cyrillic --apply`, старые
строки обозначений и новые выражения могут расходиться по id; после исправления M2 из
ревью WP9 (`normative-catalog-backend-readiness.md`) такая формула будет отклонена, а не
получит единицу `1`.

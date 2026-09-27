# Сообщение для Акима: `dec-postgres` — хранилище NLP-обработанных нормативов

- Дата: 2026-09-27
- От: Егор (data engineer)
- Кому: Аким (frontend/backend)

## Что

Поднят Docker-контейнер PostgreSQL `dec-postgres` — хранилище NLP-обработанных
нормативных документов: структурированные сущности + лемматизированный поисковый
индекс, который строится на этапе ingestion (офлайн), а не в момент запроса.

## Подключение (локальная разработка)

| Поле | Значение |
|---|---|
| host | `localhost` |
| port | `5433` |
| database | `dec` |
| user | `dec` |
| password | `dec` |
| DSN | `postgresql://dec:dec@localhost:5433/dec` |

## Схема

Все таблицы связаны через `document_id` (FK к `document`):

- `document` — `designation` (UNIQUE), `title`, `edition`, `year`, `source_url`.
- `clause` — `number`, `title`, `page`, `search_text`.
- `formula` — `number`, `clause_number`, `latex`, `raw_text`, `page`, `search_text`.
- `notation_entry` — `formula_number`, `symbol`, `meaning`, `unit`.
- `cross_ref` — `clause_number`, `ref_type` (`gost`), `ref_value`, `url`.

Полнотекстовый поиск — GIN-индекс по `to_tsvector('simple', search_text)` над `clause`
и `formula`. `search_text` лемматизируется при ingestion (ё→е, нижний регистр, pymorphy3),
поэтому на стороне запроса лемматизируется только строка запроса и выполняется lookup.

## Текущее состояние

`СП 22.13330.2016` уже обработан: 647 пунктов, 124 формулы, 141 запись обозначений,
56 ссылок (упоминания ГОСТ).

## Как бэкенду это потреблять

- Поиск: `WHERE to_tsvector('simple', search_text) @@ to_tsquery('simple', <лемматизированный запрос>)`.
- Строка `formula` + её строки `notation_entry` + строки `cross_ref` — это данные для
  движка / генератора отчётов. Формула несёт `NormRef` (`clause_number` + `designation`).
- Это локальная разработка; для общих/CI креденшлов позже — через переменную `DEC_DATABASE_URL`.

## Примечания

- Контейнер запущен вручную; в compose-файл ещё не вынесен (в репозитории его нет).

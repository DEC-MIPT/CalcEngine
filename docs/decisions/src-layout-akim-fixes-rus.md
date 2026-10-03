# Акиму: поправить протухшие пути после src-layout реорганизации

- Дата: 2026-09-28
- От: Егор (data engineer)
- Кому: Аким (frontend/backend) и его Claude Code-сессии

## Контекст

Пайплайн переехал в src-layout, конфиги — в `configs/` (см.
`repo-reorganization-src-layout.md`). Твои OpenSpec change'ы и `CLAUDE.md` всё ещё
ссылаются на старые пути. Имена модулей и контракт формул **не** изменились — только
пути на диске.

## Соответствие путей

| Старый путь | Новый путь |
|---|---|
| `normatives_pipeline/` (верхний уровень) | `src/normatives_pipeline/` |
| `normatives_pipeline/ocr/` | `src/normatives_pipeline/formulas/` |
| `normatives_pipeline/formulas.toml` | `configs/formulas.toml` |
| `normatives_pipeline/parser.toml` | `configs/parser.toml` |
| `docker-compose.yml` (корень) | `infra/docker-compose.yml` |
| `norm-docs/` | `docs/normative-base/` |

## Файлы для правки

### `openspec/changes/calculation-core-contract/`

- `design.md:220` — `normatives_pipeline/formulas.toml` -> `configs/formulas.toml`.
- `tasks.md:63` — `normatives_pipeline/formulas.toml` -> `configs/formulas.toml`.
- `design.md:196` — `docs/audit/01-recon.md:97` (файл не отслеживается/отсутствует;
  пересказать мысль в тексте или убрать цитату — это было и до переезда).

### `openspec/changes/backend-layered-architecture/`

- `tasks.md:41` — `docker-compose.yml` -> `infra/docker-compose.yml`.
- `tasks.md:59` — `docker-compose.yml` -> `infra/docker-compose.yml`.
- `tasks.md:56` — `normatives_pipeline/` -> `src/normatives_pipeline/`.
- `tasks.md:58` — `formulas.toml` -> `configs/formulas.toml`.
- `tasks.md:60` — `normatives_pipeline/ocr/` -> `src/normatives_pipeline/formulas/`.

### `CLAUDE.md`

- `:16` — `normatives_pipeline/formulas.toml` -> `configs/formulas.toml`.
- `:13` — строка «Status» всё ещё говорит, что `docker-compose.yml` не существует;
  теперь он в `infra/docker-compose.yml` на ветке пайплайна. Обновить при вливании ветки.

## Что не изменилось

- Имена модулей: `normatives_pipeline`, `search.query()`, форма payload.
- Точки входа, кроме `enrich` — теперь `normatives_pipeline.formulas.enrich`.

## Answers

- Дата: 2026-10-03
- От: Аким. Кому: Егор.

Сделано, на `develop`, по структуре, которую ты слил 2026-10-03 (`24797f7`), поэтому пути —
`ml/...`, а не `src/` и `configs/` из таблицы выше.

1. **`calculation-core-contract`** (`80a684a`, `a984b28`): `formulas.toml` указан как
   `ml/configs/formulas.toml`, с пометкой «будет удалён» (твой ответ A3). Ссылка на
   `docs/audit/01-recon.md:97` заменена её содержанием в `design.md` и в `proposal.md`. В
   `tasks.md` твоих путей не осталось.
2. **`backend-layered-architecture`** (`80a684a`, `a984b28`): `infra/docker-compose.yml` в
   примечании к разделу 3 и в DOR; `ml/src/normatives_pipeline/` в `design.md` и
   `proposal.md`; строка про OCR в «Moved out» называет `ml/` в нынешнем виде;
   `formulas.toml` — как выше.
3. **`CLAUDE.md`** (`277fcc7`): раздел «Status» переписан под слитую структуру (`ml/`,
   `infra/`, без корневых `pyproject.toml` и `tests/`), команды пайплайна — через
   `pip install -e "./ml[ml]"` и `infra/docker-compose.yml`.

Из-за того же переноса изменены также `bootstrap-dev-environment` (инструменты пайплайна —
`ml/pyproject.toml`) и `calculation-api` (`infra/docker-compose.yml`), в `11bdca4` и
`a984b28`. Старые пути остались в моих change только как датированная история («at the time of writing», «now `ml/...`»).

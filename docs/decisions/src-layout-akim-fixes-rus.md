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

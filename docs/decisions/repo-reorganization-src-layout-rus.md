# Реорганизация репозитория: src-layout, configs/, infra/, подпакет formulas/

- Дата: 2026-09-28
- От: Егор (data engineer)
- Кому: Аким (frontend/backend), команда

## Зачем

Пайплайн лежал в плоской директории `normatives_pipeline/`, конфиги и research-артефакты
были смешаны с кодом, а в корне валялись доки и docker-файл. Реорганизация приводит репо
к общепринятому src-layout, чтобы свежий клон и новая сессия стартовали с чистой,
предсказуемой структуры.

## Что изменилось

| Было | Стало |
|---|---|
| `normatives_pipeline/` (код) | `src/normatives_pipeline/` |
| `normatives_pipeline/parser.toml` | `configs/parser.toml` |
| `normatives_pipeline/formulas.toml` | `configs/formulas.toml` |
| `normatives_pipeline/research/` | `research/` |
| `normatives_pipeline/{formula_ocr,enrich,validation}.py` | `src/normatives_pipeline/formulas/{detect,enrich,validation}.py` |
| `norm-docs/` (PDF в .gitignore) | `docs/normative-base/` |
| `docker-compose.yml` | `infra/docker-compose.yml` |
| `verified-roadmap*.md` (корень) | `docs/reports/verified-roadmap*.md` |

`pyproject.toml` теперь объявляет упаковку: `[build-system]`, `[project]`, core-зависимости
(pdfplumber, psycopg2-binary, pymorphy3, pymorphy3-dicts-ru, scikit-learn, numpy, sympy)
и extras `ml` (latex2sympy2, doclayout-yolo, pix2text). Секция конфига формул переименована
`[formula_ocr]` -> `[detect]` (`detect_config()`).

## Установка (изменилась)

```bash
pip install -e ".[ml]"                              # core + extras извлечения формул
docker compose -f infra/docker-compose.yml up -d    # Postgres (dec-postgres, порт 5433)
export DEC_DATABASE_URL="postgresql://dec:dec@localhost:5433/dec"
python -m normatives_pipeline.ingest --force "docs/normative-base/СП 22.13330.2016.pdf"
python -m normatives_pipeline.formulas.enrich       # извлечение формул (нужен .[ml])
```

## Влияние на Акима

- **Контракт не изменился.** Имена модулей (`normatives_pipeline`, `search.query()`,
  форма payload) прежние; изменились только пути на диске.
- Точки входа `search.query()` / `ingest` / `formulas.enrich` сохранили `python -m`
  имена, кроме `enrich` — теперь `normatives_pipeline.formulas.enrich`.
- Editable-установка разрешает конфликт antlr4 откатом `omegaconf` до 2.0.6;
  `pillow` теперь 12.3.0 (pdfplumber требует >=12.2.0), `pypdfium2` 5.13.0.

## Примечания

- В .gitignore: `packages/`, `docs/normative-base/`, `research/{pages,crops,data}/`,
  `.kilo/plans/`, `*.egg-info/`.
- Офлайн-установка: `pip download ".[ml]" -d packages/`, затем
  `pip install --no-index --find-links packages/ -e ".[ml]"`.
- `agent-docs/` остаётся в корне (переезд под `docs/` откатан: оставил бы 30+ битых
  ссылок и поменял бы определение «no code» в спеках OpenSpec).

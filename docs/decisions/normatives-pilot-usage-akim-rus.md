# Акиму: пилотный норматив → обработка → запрос формулы

- Дата: 2026-09-27
- От: Егор (data engineer)
- Кому: Аким (frontend/backend)

## Предусловия

- Docker Postgres `dec-postgres` на порту 5433 — см. `normatives-postgres-storage.md`.
- Venv `.venv` с пакетом, установленным editable: `.venv/bin/pip install -e ".[ml]"`.
- Пилотные PDF лежат в `docs/normative-base/` (в .gitignore; полные тексты не распространяются).

## 1. Получить пилотный файл

Пилотные документы уже в `docs/normative-base/` (СП 22.13330.2016, СП 24/30/31/45.13330, скан-СНиП).
Новые загрузки тоже попадают в `docs/normative-base/` (туда пишет коллектор).

## 2. Обработка (загрузка в Postgres)

```bash
cd /home/malkinte/CalcEngine
.venv/bin/python -m normatives_pipeline.ingest --force "docs/normative-base/СП 22.13330.2016.pdf"
```

Идемпотентно: повторный запуск без `--force` печатает `[skip] … уже в хранилище`.

## 3. Запрос формулы (человекочитаемый)

```bash
.venv/bin/python -m normatives_pipeline.search "условие успешного погружения опускных колодцев"
```

## 4. Запрос реального возврата (JSON — что получает бэк)

```bash
.venv/bin/python -m normatives_pipeline.search --json "условие успешного погружения опускных колодцев"
```

`--json` печатает ровно тот объект, который возвращает `normatives_pipeline.search.query(...)`
(`search.query(query) -> dict`), а не консольный текст.

## Контракт возврата

Форма задаётся конфигом: `configs/parser.toml` → `[output]`
(`formula_keys`, `norm_ref_keys`, `symbol_keys`, `default_symbol_kind`).

```json
{
  "norm_ref": {"designation": "СП 45.13330.2017", "clause": "13.8", "formula": "13.8#1"},
  "latex": "",
  "symbols": [
    {"id": "G", "latex": "G", "meaning": "собственный вес колодца …", "unit": "", "kind": "input"},
    {"id": "G_p", "latex": "G_{\\text{п}}", "meaning": "дополнительная пригрузка колодца", "unit": "", "kind": "input"}
  ],
  "expression": "",
  "cross_refs": [{"ref_type": "gost", "ref_value": "ГОСТ …", "url": ""}]
}
```

- `latex` и `symbols[].latex` — канонический LaTeX для MathJax.
- `symbols[].id` — ASCII-ключ == имя символа SymPy, которое биндит движок.
- `expression` пока пуст (шаг структурного извлечения); `kind` = `input`, пока не появится
  определение выходной переменной.
- `cross_refs` — упоминания ГОСТ, привязанные к пункту (URL — позже).

## Про пример со сваями

`"допускаемая нагрузка на сваю в составе фундамента"` — это свайные фундаменты = СП 24.13330,
а не пилот СП 22.13330.2016 (основания мелкого заложения). Чтобы искать сваи, сначала
загрузи СП 24:

```bash
.venv/bin/python -m normatives_pipeline.ingest --force "docs/normative-base/СП 24.13330.2021.pdf"
.venv/bin/python -m normatives_pipeline.search --json "допускаемая нагрузка на сваю"
```

Механизм тот же; что можно найти, определяет загруженный корпус.

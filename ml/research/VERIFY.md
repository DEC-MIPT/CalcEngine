# Как проверять пайплайн нормативов в терминале

Полный цикл: получить PDF → извлечь текст/таблицы/формулы → занести в БД → прочитать то,
что отдаём потребителю → сверить с PDF. Все команды параметризованы путём к PDF: ничего не
зашито под конкретный СП, любой текстовый PDF проверяется одинаково.

Рабочий код пайплайна (`src/normatives_pipeline/`) при проверке не меняется — скрипты только
читают и сравнивают. LLM нигде не используется: только `pdftotext`, `pdfplumber`, `psycopg2`,
`pymupdf`, `pymorphy3`.

## 0. Предпосылки (один раз)

```bash
# репозиторий и виртуальное окружение (из корня репозитория)
python -m venv .venv
.venv/bin/pip install -e "./ml[ml]"          # без [ml] — только детерминированное ядро
sudo apt-get install -y poppler-utils        # даёт pdftotext (текстовый слой PDF)

# Postgres локально (порт 5433)
docker compose -f infra/docker-compose.yml up -d
export DEC_DATABASE_URL="postgresql://dec:dec@localhost:5433/dec"
```

Проверка, что у PDF есть текстовый слой (иначе это скан, и нужен OCR — вне этого цикла):

```bash
pdftotext -layout "docs/normative-base/<файл>.pdf" - | wc -c   # должно быть > 500
```

## 1. Получить PDF

Официальный источник (ФАУ ФЦС) — коллектор; скачивает СП в `docs/normative-base/`:

```bash
python -m normatives_pipeline.collector.cli
```

Нужен доступ в сеть к `api.faufcc.ru`. Офлайн просто положите PDF в `docs/normative-base/` —
дальше всё работает одинаково. Обозначение и год издания берутся с титульной страницы
(`parser/text_layer.py`), а не из имени файла, поэтому имя может быть любым.

## 2. Занести документ в БД (ingest)

```bash
python -m normatives_pipeline.ingest "docs/normative-base/<файл>.pdf"
# повторный запуск идемпотентен (skip); перезалить: добавьте --force
```

Ingest печатает сводку: пунктов, формул (нумерованных/синтетических), обозначений, ссылок,
таблиц, ячеек. Схема создаётся автоматически (`db.init_schema`).

## 3. Прочитать из БД то, что отдаём потребителю (Акиму)

```bash
# поиск: возвращает формулу в виде payload (norm_ref, latex, symbols, expression, cross_refs)
python -m normatives_pipeline.search --json "условие успешного погружения опускных колодцев"
```

- `search.query("…")` → `{"query", "lemmas", "formulas", "clauses"}`; каждая формула — ровно
  ключи `[output] formula_keys` из `configs/parser.toml`.
- Коэффициенты: `db.fetch_coefficients(conn, doc_id, table_number)` +
  `db.build_coefficient_payload(row)` (каждая ячейка несёт пятиполевой `NormRef`).
- Инварианты: `status=verified ⇒ edition и clause конкретны`; `document` непустой всегда.

## 4. Автоматическая сквозная проверка (главное)

Скрипт `research/verify_end_to_end.py` выполняет весь цикл на одном PDF и ставит PASS/FAIL:

```bash
cd ml
export DEC_DATABASE_URL="postgresql://dec:dec@localhost:5433/dec"
../.venv/bin/python -m research.verify_end_to_end "../docs/normative-base/<файл>.pdf"
```

Что проверяется:
1. обозначение и год из титульной страницы;
2. ingest (загрузка в БД);
3. инварианты `NormRef` по всем формулам и коэффициентам документа;
4. чтение: `search.query` и `build_formula_payload` (ключи payload = конфиг);
5. **roundtrip**: набор ячеек, который вернул pdfplumber-экстрактор, сравнивается с тем, что
   лежит в БД, как multiset (`Counter`) — ловит потерю/порчу/дубликаты;
6. **independent**: одна нумерованная таблица заново извлекается из PDF прямым вызовом
   pdfplumber (не через `extractors`) и сверяется с БД по строкам/колонкам.

Проверка **всех** PDF сразу (обобщённо, без списка конкретных документов):

```bash
cd ml
for pdf in ../docs/normative-base/*.pdf; do
  printf '\n=== %s ===\n' "$pdf"
  ../.venv/bin/python -m research.verify_end_to_end "$pdf" || echo "FAIL: $pdf"
done
```

Код возврата: `0` — PASS, `1` — FAIL (расхождения перечислены), `2` — нет файла.

## 5. Визуальная сверка (HTML: PDF ↔ БД)

```bash
cd ml
../.venv/bin/python -m research.make_review_html \
  "../docs/normative-base/<файл>.pdf" \
  --out research/review/<имя>.html
# при желании: --formula <номер> --table <номер>
```

Открыть HTML в браузере: в каждой строке две колонки — слева вырезка из PDF, справа то, что
отдаём потребителю (payload/NormRef как JSON) и визуальная форма (формула — MathJax, таблица —
сохранённые ячейки по строкам/колонкам). Без `--formula`/`--table` выбираются: формула —
проверенная (verified), иначе самая содержательная; таблица — самая крупная нумерованная.
MathJax подгружается с CDN (нужен интернет в браузере); сами данные — офлайн.

## 6. Тесты, линт, типы, покрытие

```bash
cd ml
DEC_DATABASE_URL="postgresql://dec:dec@localhost:5433/dec" ../.venv/bin/python -m pytest tests/ -q
../.venv/bin/python -m ruff check src
../.venv/bin/python -m mypy src/normatives_pipeline
# покрытие: pytest-cov / coverage (tests/ + coverage.run.source = src/normatives_pipeline)
```

Тесты, требующие БД, пропускаются без `DEC_DATABASE_URL`. Корпусные тесты читают PDF из
`docs/normative-base/` (путь считается от корня репозитория).

## 7. Идемпотентность

```bash
python -m normatives_pipeline.ingest "docs/normative-base/<файл>.pdf"   # 2-й раз
# ожидаемо: "[skip] <обозначение> уже в хранилище"; число строк в БД не меняется
```

## 8. Диагностика

| Симптом | Причина / что делать |
|---|---|
| `нет файла` | неверный путь к PDF; проверьте `docs/normative-base/` |
| ingest падает «не удалось извлечь обозначение» | у PDF нет текстового слоя или нестандартный титул; проверьте п. 0 |
| `roundtrip: нет в БД …` | рассинхрон экстрактор↔БД (сбой вставки/дубликат) — смотрите таблицу/страницу в выводе |
| `normref … verified, но ссылка не конкретна` | нарушен инвариант: для verified нужны edition и clause |
| `[independent] … MISMATCH` | прямой pdfplumber разошёлся с БД на конкретной странице |
| pytest скипает корпусные тесты | не найден PDF по `docs/normative-base/` или не задан `DEC_DATABASE_URL` |
| пустой `latex` в HTML формулы | формула распознана детектором и хранится как `machine-extracted`; OCR-путь отложен (см. `PIPELINE.md`) |

## 9. Что здесь обобщено (почему нет хардкода)

- Путь PDF — единственный вход; обозначение/год/номера извлекаются из документа.
- Таблица для независимой сверки выбирается по данным (самая крупная нумерованная), не по номеру.
- Формула выбирается по данным (verified → содержит latex → самая содержательная).
- Поисковый запрос строится из первого пункта документа.
- Цикл по `*.pdf` покрывает все документы без списка конкретных СП.

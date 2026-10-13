# Нормативный каталог — статус мержа и следующие шаги (Акиму)

Дата: 2026-10-13
От: Егор
Кому: Аким

## Что смержено сегодня

`fix/normative-catalog/data` теперь на `develop`.

Изменения в зоне Егора:
- `formulas.toml` удалён; пилотные формулы берутся из `pilot.toml` (хранятся как
  `unverified` / `machine-extracted`, а не `verified` / `human-verified` — полный фикс M1).
- `document.edition` теперь хранит полный текст с номерами изменений
  (например, «2016 с Изм. N 1, 2, 3, 4, 5») — фикс m7.
- Пилотный каталог перестраивается в одной транзакции — M1.
- Фиксы `word_similarity`, `formula_extractor`, запроса `catalog_binding`.
- Защита `_table_caption` от отрицательного bbox.top.
- Добавлено новое OpenSpec изменение `formula-extractor-fix` (тестер GO задача 2.1).
- Тестер GO для `fix/normative-catalog/data`: 221 passed, 0 failed
  (`normative-catalog-backend-readiness.md`, Section 2, вердикт тестера).

Также смержено сегодня (другие задачи Егора):
- `normatives-parser` — заархивировано (покрытие 100%, тестер GO).
- `normatives-collector` — заархивировано (покрытие 100%, тестер GO).

## Что Акиму нужно сделать

### Задача 2.7 — повторное ревью `fix/normative-catalog/data`

Второе ревью Акима (Section 2 «Akim's second review» в readiness.md) подняло R1–R4,
M1 и ряд мелких пунктов. Статус фикса Егора (Section 2 «Egor's fix status») фиксирует
R1–R4, m1, m3–m7 и M1 как исправленные. Пожалуйста, сделай повторное ревью и запиши
вердикт в `normative-catalog-backend-readiness.md`.

### Секции 7 (пилот end-to-end) и 7.2–7.3 (производительность + тестер GO для бэкенда)

Заблокированы на задаче 2.7.

**Важно: чтобы наполнить БД, нужно прогнать код Егора (ingestion pipeline).**
Бэкенд не может отдавать нормативы через `GET /normatives/search` и
`GET /normatives/documents/{document_id}`, пока пилотные данные не загружены.

Для загрузки данных:

```bash
# из корня репозитория, с DEC_DATABASE_URL, указывающим на dec-postgres (порт 5433)
pip install -e "./ml[ml]"
python -m normatives_pipeline.ingest
```

Подробнее — в `docs/decisions/normatives-pilot-usage-akim.md` и `README.md`.
Пилотный документ: СП 22.13330.2016 с Изм. N 1, 2, 3, 4, 5
(`docs/normative-base/sp22_2016.pdf`; у Акима есть копия в `docs/NTD/`).

После загрузки `POST /calculations` для `foundations_shallow_r` должен вернуть
реальный результат вместо `503 parameter_source_unavailable`.

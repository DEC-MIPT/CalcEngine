# Merge пайплайна: что блокирует пилот на данных каталога (Аким Егору, 2026-10-11)

- От: Аким (зона backend). Кому: Егор (зона data).
- Статус: открыт; ответы пишутся в этот файл в раздел `## Answers` (AGENTS.md, раздел 7).
- Английская версия: `2026-10-11-pipeline-merge-followups-to-egor.md`.

Продолжение файла `2026-10-07-pipeline-branch-and-process-to-egor.md` (твои ответы от
2026-10-11) и твоих коммитов в `develop` за тот же день. Спасибо за быстрые ответы и за
то, что взял сводный текст СП 22 в тот же день. Здесь только два пункта, без которых я не
могу прогнать пилот `foundations_shallow_r` целиком на данных каталога (задача WP9 7.1).
Моё повторное ревью `fix/normative-catalog/data` (задача WP9 2.7), как и раньше, пойдёт в
`normative-catalog-backend-readiness.md`.

## 1. `fix/normative-catalog/data` в `develop`

Задача WP9 7.1 выполняется на коде данных из `develop` после задачи 2.7. 2026-10-11
первой влита `feature/normative-pipeline/data` (`08dbb85`), а fix-ветки в `develop` нет
(`950a910`, `3425ec0`, `ae23894` и `1d858bc` не являются предками `develop`). Теперь она
конфликтует с `develop` в 12 файлах (`git merge-tree`): `.secrets.baseline`; в
`ml/src/normatives_pipeline/` — `catalog_contract.py`, `db.py`, `ingest.py`,
`parser/cyrillic.py`, `parser/text_layer.py` и `pilot_catalog.py`; в `ml/tests/` —
`conftest.py`, `test_catalog_contract.py`, `test_db_payload.py`, `test_ingest.py` и
`test_pilot_catalog.py`. Большая часть из них — от исправлений, которые теперь есть с
обеих сторон, сделанные по-разному (M2, m1, m5, m7).

Пожалуйста, влей `develop` в `fix/normative-catalog/data`, разреши конфликты там,
сохранив M1 (нет `formulas.toml`, каждая формула и каждый коэффициент `unverified` /
`machine-extracted`), и назови коммит, когда ветка готова. Я ревьюю эту версию, а после
её merge в `develop` для задачи 7.1 будет одна версия ингеста.

## 2. Данные каталога для задачи WP9 7.1 на моей машине

Задача 7.1 прогоняет пилот целиком «на ингестированной Егором `dec_normatives`». У меня
база `dec` на `dec-postgres` пустая (нет `catalog_read`, таблиц пайплайна и роли
`dec_normatives_reader`), нет `docs/normative-base/` и нет `ml/.venv`. В `CLAUDE.md`
сказано, что ингест запускаешь ты, а в `normatives-pilot-usage-akim.md` ты показываешь
команды мне. Как тебе удобнее:

- (а) я запускаю твой ингест у себя из `develop` после merge
  `fix/normative-catalog/data` по `normatives-pilot-usage-akim.md`, со сводным PDF в
  `docs/normative-base/` под именем, которое ждёт команда (подтверди, пожалуйста, имя и
  команды, включая `DEC_NORMATIVES_READER_PASSWORD`);
- (б) ты даёшь дамп ингестированной `dec` (схема и данные таблиц пайплайна и
  `catalog_read`, без паролей ролей), а я восстанавливаю его на `dec-postgres`?

Предлагаю (а): так сам ингест проверится ещё на одной машине.

## 3. Ингест падает на сводном тексте СП 22

2026-10-11 я запустил у себя ингест из `develop` (`ml/` в том виде, как он влит в
`08dbb85`) на сводном PDF, который отправлял тебе («СП 22.13330.2016 с Изменениями N 1,
2, 3, 4, 5», 214 страниц, sha256
`289dc6844340d0177dd01761af4b2adef075d567a16a9685d360b29a79700ecf`), с закреплённым
`pdfplumber==0.11.10` на Python 3.12.3:

    python -m normatives_pipeline.ingest --force "<путь>/СП 22.13330.2016.pdf"

Он останавливается в `extract_tables` с `ValueError: (0, 0, 595, -30.61564067061954) has
a negative width or height.` (`parser/extractors.py`, `_table_caption`, строка
`page.within_bbox((0, max(0, top - 60), page.width, top))`). На страницах 33 и 178
`find_tables()` возвращает колонтитул распечатки («СП 22.13330.2016 Основания зданий и
сооружений … Страница 178») как таблицу из одной строки, верх которой выше страницы
(`-30.6` и `-37.2`), поэтому полоса над ней получается отрицательной высоты. К этому
моменту документ, 622 пункта и 118 формул уже записаны, а коэффициенты и строки каталога
пилота — нет, так что в `catalog_read` нет данных для `foundations_shallow_r`.
`extractors.py` тот же на `fix/normative-catalog/data` и `fix/formula-extractor/data`.

Для репетиции задачи WP9 7.1 я прогнал тот же ингест через обёртку вне репозитория,
которая перед `_table_caption` поднимает верх таблицы до 1 pt (ни один файл в `ml/` не
изменён). Поправлены только две таблицы-колонтитула, и ингест завершился: 101 таблица,
2955 ячеек, а в `catalog_read` есть три формулы пилота, по 46 строк `m_gamma`, `m_q`,
`m_c` из таблицы 5.5, константы, порог, проверка и границы `phi_II`, всё `unverified` /
`machine-extracted`.

На этих данных тест задачи 7.1 проходит (3 из 3). Это новый модуль
`backend/tests/test_catalog_ingested.py` на `feature/normative-catalog/backend`
(`70119ae`, запушен). Он только читает каталог под ролью `dec_normatives_reader` через
`DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL` и пропускается без неё. Он проверяет, что
колонки `catalog_read` совпадают с контрактом; что `POST /calculations` для пилота с
`phi_II` из заголовков таблицы 5.5 отвечает `201`, ссылки каждого шага взяты из каталога,
а сохранённый результат называет документ и редакцию каталога; и что русское слово из
заголовка пункта находит этот пункт. Тест проверяет структуру и статусы, а не
нормативные значения. В прогоне: вердикт `pass`, 9 шагов (6 табличных, 2 формулы,
1 проверка), все непроверенные, все ссылки — на СП 22.13330.2016 «2016 с Изм. 1, 2, 3,
4, 5». Ты можешь запустить его после ингеста, из `backend/`:

    DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL=postgresql://dec_normatives_reader:<password>@localhost:5433/dec \
        .venv/bin/pytest tests/test_catalog_ingested.py

Это репетиция: задача 7.1 остаётся открытой, пока я не повторю ингест и тест после того,
как `fix/normative-catalog/data` (п. 1) и исправление из этого пункта будут в `develop`.

Пожалуйста, исправь это в `extractors.py` (на `fix/normative-catalog/data`, чтобы
исправление попало в `develop` вместе с п. 1) с тестом на таблицу, верх которой выше
страницы. И как ингест проходил у тебя с этим файлом: другой файл, другая версия или
другая команда?

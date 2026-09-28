# Ответ Акима на ответы Егора: пайплайн, ветвление, раскладка репозитория

- Date: 2026-09-29
- From: Akim. To: Egor.
- Context: ответ на `pipeline-followup-answers-egor-rus.md`.

English version: `pipeline-followup-answers-akim.md`.

## A1, D. Статус формул: авто-verified

Кнопку и счётчики по формулам я не принимаю. Бери свой запасной вариант: проставь всем
формулам «Проверена, верна» сам. С моей стороны нет ни ручной верификации каждой формулы,
ни пользовательского действия для верификации, поэтому я не добавляю для этого ни эндпоинт,
ни счётчик, ни кнопку. Вопрос из `formula-verification-akim.md` закрыт.

Следствие для схемы: `status` и `provenance` по-прежнему хранятся для каждой формулы и
каждого коэффициента (замечания 11-15), а колонки `shown_count` и `flagged_count` не нужны.

## A2. `docs/normative-base/` и `norm-docs/` в `.gitignore`

Согласен, имя папки остаётся `docs/normative-base/`. Я не правлю `.gitignore` на `develop`
по двум причинам:

- В `feature/normative-parser/ml` строка `norm-docs/` уже заменена на `docs/normative-base/`,
  так что с `develop` она уйдёт при слиянии этой фичи. Моя правка на `develop` дала бы
  конфликт с твоей в том же фрагменте.
- Код на `develop` (`normatives_pipeline/ingest.py`, `normatives_pipeline/parser/cli.py`,
  `tests/`) пока читает `norm-docs/`. Без строки в `.gitignore` скачанные там полные тексты
  окажутся untracked, а полные тексты норм коммитить нельзя.

Пожалуйста, оставь строку до слияния своей ветки и до тех пор не скачивай в `norm-docs/`.

## A3. `formulas.toml`

Согласен: удалить. Отдельное решение про `human-verified` для этого файла не нужно.

## A4. Порядок блокеров пилота

Согласен: `normatives-formula-contract` 1.4-1.7, затем `retarget-mvp-domain` 3.1, затем 1.3.

## A5. `DEC_NORMATIVES_DATABASE_URL`

Подтверждаю. Мой `Settings` оставляет `DEC_DATABASE_URL` только для базы `dec_app`, так что
имена не пересекаются.

## B. Ветвление

Спасибо за подтверждение. Код `normatives-formula-contract` остаётся на
`feature/normative-parser/ml`.

## C. Раскладка репозитория

- C1: согласен. `backend/` и `frontend/` остаются в корне, `ml/` твой.
- C4: согласен, тесты бэкенда в `backend/tests/`, общей корневой `tests/` нет. Корневой
  `pyproject.toml` (`testpaths`, coverage `source`) придётся менять. Он общий, поэтому я трогаю
  его только после того, как ты перенесёшь свои тесты в `ml/tests/` и напишешь мне, и сначала
  покажу тебе diff.
- `infra/docker-compose.yml`: согласен. Пожалуйста, сохрани имя сервиса `dec-postgres` и порт
  5433, на них завязаны проверки задач WP5 3.x. Свои ссылки обновлю, когда перенос будет на
  `develop`.

## Что нужно от тебя

- Напиши, когда `tests/` и `docker-compose.yml` будут перенесены.
- Напиши, когда автоматический статус «верифицировано» будет проставлен.

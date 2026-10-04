# Secrets baseline: твои ответы внедрены (2026-10-04)

- Дата: 2026-10-04
- От: Аким. Кому: Егор. К сведению; один пункт приглашает тебя возразить (раздел 3).
- Контекст: твои ответы от 2026-10-04 в `secrets-baseline-refresh-questions-akim.md`
  («Answers»). Их внедрило изменение `dev-tooling-followups`, слитое в `develop` в
  `a505352` (фича `feature/dev-tooling/backend`, GO от `tester` и ревью `orchestrator` в
  `dev-tooling-followups-readiness.md`).

Английская версия: `secrets-baseline-rule-in-place-akim.md`.

## 1. Что внедрено

- **Ноутбуки (твоя часть 2).** `detect-secrets` пропускает ноутбуки `ml/research/`:
  шаблон `^ml/research/.*\.ipynb$` в `.pre-commit-config.yaml` и в фильтрах baseline. Он
  захватывает и подпапки `ml/research/`, чуть шире, чем `ml/research/*.ipynb`, так что
  твои восемь ноутбуков покрыты, где бы они ни лежали внутри `ml/research/`. В самих
  ноутбуках ничего не менялось; паролей в них нет по твоему соглашению.
- **Обновление только номеров строк (твоя часть 3).** `AGENTS.md`, раздел 2, теперь
  говорит: если хук только переписал номера строк в `.secrets.baseline` или убрал
  записи удалённых строк (код 3, «The baseline file was updated», без отчёта «Potential
  secrets», в диффе только `line_number`, удалённые записи и `generated_at`),
  переписанный baseline коммитится вместе с правкой, которая это вызвала, в её ветке,
  включая `develop`. Новая находка в такой коммит в baseline не попадает: её убирают из
  файла или помечают там как заглушку, либо baseline пересобирают с ручной проверкой в
  ветке фичи или исправления.
- **Пометки (твоя часть 1, моя сторона).** Мои заглушки в тестах бэкенда,
  `backend/alembic.ini`, миграциях и `.env.example` помечены `pragma: allowlist secret`
  и из baseline ушли. Теперь в baseline 12 находок — все локальный пароль разработки или
  хеш содержимого; твои `ml/tests/conftest.py` и `infra/docker-compose.yml` остаются в
  нём, пока ты не поставишь там свои пометки, как и планировал.

## 2. Если поставишь хук

`backend/.venv/bin/pre-commit install` в корне репозитория (или свой `pre-commit`).
Хук настроек (`.env.example` против настроек бэкенда) теперь загружает
`backend/app/core/config.py` и спрашивает имена переменных у `pydantic-settings`,
поэтому его окружение собирается на `python3.12` с двумя закреплёнными пакетами
(`pydantic`, `pydantic-settings`); нужен `python3.12` на `PATH`. Он запускается, только
когда застейджен `config.py` или `.env.example`, так что твоих коммитов иначе не
касается.

## 3. Предложение, добавленное без отдельного вопроса

Твой ответ покрывал предложение в разделе 2. Ревью спецификации показало, что без
второго предложения изменение только из документов, в коммит которого попало такое
обновление, считалось бы изменением с кодом и теряло бы путь GO без кода. Поэтому в
`AGENTS.md`, раздел 4 («No code» means ...), теперь есть и это:

> A refresh of `.secrets.baseline` that adds no finding, committed with a document under
> the exception of section 2, does not make a change a change with code.

Я добавил его без отдельного вопроса: оно следует из твоей части 3 и лишь сужает правило
для этого случая. Если возражаешь, напиши в разделе `## Answers` английского файла, и я
его пересмотрю.

## 4. WP9

Когда сольётся `feature/normative-catalog/backend`, его новые тесты принесут
пароли-заглушки, которых нет в baseline, а `backend/tests/test_config.py` конфликтует с
пометками. Шаги — в `tasks.md` `normative-catalog-backend`, «Dependencies»; это моя
ветка, от тебя ничего не нужно.

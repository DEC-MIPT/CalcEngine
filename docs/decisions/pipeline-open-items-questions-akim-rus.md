# Открытые пункты по пайплайну: перенос структуры репозитория и статус формул (вопросы Егору, 2026-10-03)

- Дата: 2026-10-03
- От: Аким. Кому: Егор.
- Контекст: на два пункта из раздела «Open for you» в `pipeline-followup-answers-akim.md`
  (2026-09-29) ответа пока нет. `pipeline-followup-answers-egor-rus.md` написан раньше них, а
  `a01af6f` (твои ответы по `normative-catalog-backend` и исполнению формул) их не касается.
  Сверено с `origin/feature/normative-parser/ml` на `a507529` (2026-09-29).
- Как ответить: допиши раздел `## Answers` в этот файл (`AGENTS.md`, раздел 7).

Английская версия: `pipeline-open-items-questions-akim.md`.

## 1. Перенос структуры (`ml/`, `infra/`)

Согласованная структура (`pipeline-followup-answers-egor-rus.md`, C1-C4): `backend/` и
`frontend/` в корне, `ml/` твой (`pyproject.toml`, `src/normatives_pipeline/`, `configs/`,
`research/`, `tests/`), `infra/docker-compose.yml` общий. В C2 ты написал, что переносишь
сейчас, до слияния в `develop`.

Что вижу на твоей ветке: `infra/docker-compose.yml` есть, корневого `docker-compose.yml` нет.
Каталога `ml/` нет: `pyproject.toml` (проект `normatives-pipeline`), `src/`, `tests/`,
`configs/` и `research/` по-прежнему в корне. На `develop` ничего не переехало.

Зачем мне это: после переноса я правлю корневой `pyproject.toml` (`testpaths`, `source`
покрытия), сначала показав тебе diff, обновляю пути в `CLAUDE.md` и перевожу свои ссылки на
`dec-postgres` в `infra/`. До появления переноса на `develop` ничего из этого не делаю.

- **Вопрос 1a.** Цель по-прежнему `ml/`, как договорились, и туда уходят все `pyproject.toml`,
  `src/`, `tests/`, `configs/` и `research/`?
- **Вопрос 1b.** Остаётся ли корневой `pyproject.toml` после переноса? Если твой проект
  переезжает в `ml/pyproject.toml`, а корневой файл удаляется, моя правка не нужна (у бэкенда
  свой `backend/pyproject.toml`). Если корневой файл остаётся, что в нём будет?
- **Вопрос 1c.** Подтверди, пожалуйста, что в `infra/docker-compose.yml` остаются имя сервиса
  `dec-postgres` и порт 5433.
- **С твоей стороны.** Когда перенос будет слит в `develop`, напиши здесь коммит слияния.

## 2. Статус формул: автоматическая отметка «verified»

2026-09-29 я принял твой запасной вариант: ты автоматически отмечаешь все формулы как
«verified» (`pipeline-followup-answers-akim.md`, A1). Потом аудит исполнения формул это сузил
(`calculation-core-contract-formula-execution-akim.md`, пункт 3, ты подтвердил в `a01af6f`):
отметка не становится `NormRef.status`, `provenance = machine-extracted` всегда означает
`status = unverified`, и бэкенд читает `provenance`, а не отметку.

Что вижу на твоей ветке: `src/normatives_pipeline/db.py:320-321` по-прежнему пишет константы
`"status": "unverified"` и `"provenance": "machine-extracted"`; автоматической отметки нет.

В `a01af6f`, пункт 3, ты также написал: «For the pilot, we accept for now that all its formulas
are treated as verified». По правилу бэкенда выше каждый шаг пилота, опирающийся на формулу с
`machine-extracted`, показывается как непроверенный и учитывается в `unverified_step_count`.

- **Вопрос 2a.** Автоматическая отметка ещё в планах? Если да: в какой колонке и с каким
  значением, и войдёт ли она в `normatives-formula-contract` 1.4-1.7?
- **Вопрос 2b.** Что значит «treated as verified» для пилота? Либо (а) это только наша
  договорённость, а в данных остаётся `provenance = machine-extracted`, и отчёт пилота
  показывает его шаги как непроверенные; либо (б) у формул и коэффициентов пилота в данных
  будет `provenance`, отличный от `machine-extracted`, — тогда какой и на каком основании
  (сверка с первоисточником СП 22.13330.2016, как в твоём пункте 2 про коэффициенты)?
- **С твоей стороны.** Когда колонки статуса будут заполнены по решению, напиши здесь коммит
  слияния.

Ни один из пунктов не блокирует `calculation-api`: его тесты работают на синтетических
параметрах. Оба блокируют `normative-catalog-backend` и пилот R на данных каталога
(задача WP2 7.1c).

# Проверка готовности: `bootstrap-dev-environment` (WP6)

- Дата: 2026-09-27
- Change: `openspec/changes/archive/2026-10-04-bootstrap-dev-environment/` (в архиве с 2026-10-04; было `openspec/changes/bootstrap-dev-environment/`)
- Владелец: Аким. На спековой фазе правок общих файлов нет, кроме `openspec/` и
  `docs/`; реализация затрагивает только `backend/`, `frontend/` и корневые файлы вне
  зоны Егора (`.pre-commit-config.yaml`, `.env.example`, `.secrets.baseline`).
- Критерии: `openspec/specs/development-process/spec.md`, «Planning before
  implementation» и «Go/No-Go verdict and archive»; собственный `tasks.md` этого
  change, раздел «DOD and Go / No-Go».

Английская версия: `bootstrap-dev-environment-readiness.md`.

## Итоговый статус

**В архиве — 2026-10-04.** Слито в `develop` в `bec3d43` после ревью (задача 7.2,
раздел 7); `spec-keeper` перенёс дельту в `openspec/specs/development-process/spec.md`
и заархивировал изменение (задача 7.3, раздел 8).

**GO (реализация, задача 7.1) — 2026-10-04** для `feature/dev-environment/backend`;
см. раздел 6.

**GO (спековая фаза, задача 1.4) — 2026-09-27**

`openspec validate --all --strict` проходит (18/18), два прохода `spec-reviewer` по
текущему тексту (проход 2: 0 блокеров, 0 major), `tester` независимо подтвердил
валидацию, итог ревью, отсутствие нормативного содержания и то, что четыре требования
дельты спеки сходятся с `tasks.md` без «сирот» в обе стороны. Разделы реализации 2–7
остаются открытыми и этим вердиктом не покрыты.

| Условие DOD (`tasks.md`) | Состояние | Подтверждение |
|---|---|---|
| `openspec validate --all --strict` проходит | Выполнен | 18/18, см. раздел 1 |
| Отчёт `spec-reviewer` по текущей версии: без блокеров и major | Выполнен | 2 прохода; проход 2: 0 блокеров, 0 major, 1 minor (исправлено); см. раздел 2 |

## 1. `openspec validate --all --strict`

```
Change 'bootstrap-dev-environment' is valid
Totals: 18 passed, 0 failed (18 items)
```

Подтверждено независимо трижды за день: один раз сессией Акима после написания всех
четырёх артефактов, один раз агентом `tester` для задачи 1.4. Проход 2 `spec-reviewer`
не смог его запустить (не было доступа к shell в этом ревью) и отметил это; сессия
Акима перезапустила валидацию сразу после.

## 2. Проходы `spec-reviewer`

### Проход 1: 0 блокеров, 2 major, 2 minor

Объём: четыре артефакта нового change (`proposal.md`, `design.md`, `tasks.md`,
`specs/development-process/spec.md`), проверены на полноту, тестируемость, внутреннюю
согласованность между файлами, формат OpenSpec и соответствие
`agent-docs/domain-constraints.md` и требованию «Shared decisions are tracked».

| № | Уров. | Замечание | Итог |
|---|---|---|---|
| 1 | Major | Сценарий «Config variable missing from the template» требования «Pre-commit secret scan and documented configuration» говорил, что падает *backend-команда*, что противоречило решению 5 `design.md` (это отдельный pre-commit hook) и задаче 4.4 `tasks.md` (проверяется через `pre-commit run`) | Исправлено: сценарий теперь называет pre-commit hook, а не backend-команду |
| 2 | Major | У того же требования не было сценария для отложенного состояния, в отличие от параллельного требования «Import contract check» с его «Layered structure not yet present» | Исправлено: добавлен сценарий «Configuration model not yet present» |
| 3 | Minor | Голые ссылки «roadmap requirement N» в `proposal.md`, `design.md`, `tasks.md` без названного отслеживаемого источника | Исправлено: формулировка «roadmap» убрана, рассуждение пересказано на месте |
| 4 | Minor | Целевой файл задачи 6.2 оставлен неопределённым («`CLAUDE.md` или раздел корневого `README.md`, смотря что...») | Исправлено: назван конкретно `CLAUDE.md`, рядом с задачей 6.1 |

### Проход 2 (после четырёх исправлений): 0 блокеров, 0 major, 1 minor

Подтверждено, что все четыре исправления читаются верно, новых противоречий нет; grep
по всему change на «roadmap» и «docs/audit» дал ноль совпадений. Новое minor: строка
`openspec validate --strict` в чек-листе DOR оставалась неотмеченной, хотя сама задача
1.2 уже была отмечена. Исправлено: строка чек-листа тоже отмечена.

**Вердикт: READY for DOR.**

## 3. Вердикт tester (задача 1.4, только спековая фаза)

```
Verdict: GO (spec phase only, task 1.4)
Change: bootstrap-dev-environment (WP6), branch feature/bootstrap-dev-environment/backend, 2026-09-27
Conditions:
- Validation: PASS. openspec validate bootstrap-dev-environment --strict -> valid. openspec validate --all --strict -> 18/18.
- spec-reviewer no blocker/major (current text): PASS. Confirmed the "Pre-commit secret scan and documented configuration" requirement has exactly 3 scenarios, including the pre-commit-hook wording and the deferred-state scenario. Grep for "roadmap"/"docs/audit" over the whole change directory: 0 hits. Task 6.2 names CLAUDE.md concretely. DOR checklist's validate line is checked.
- Norm content: PASS. No SP/SNiP/GOST/clause/coefficient/edition term anywhere in the four artifacts.
- Own consistency check (spec vs tasks vs proposal/design): PASS. All 4 ADDED requirements map to tasks with no orphans: Backend tooling command -> 2.1-2.4; Frontend tooling command -> 3.1-3.4; Import contract check -> 5.1 (blocked WP5); Pre-commit secret scan/.env.example -> 4.1-4.4 (4.4 blocked WP5). No contradiction between proposal.md/design.md and the final spec text.
```

Вердикт (оставлен на английском, как выдан) покрывает только спековую фазу. Разделы
2–7 (реализация: backend- и frontend-тулинг, pre-commit, отложенные задачи по контракту
импортов и проверке конфига, документация, закрытие) остаются открытыми и не покрыты.

## 4. Открытые пункты, переносимые дальше

| Пункт | Владелец | Что блокирует |
|---|---|---|
| Задача 4.4 (hook сверки конфига и `.env.example`) | Аким, после того как задача 2.1 `backend-layered-architecture` будет готова | Ничего в GO этого change; подхватывается, когда WP5 её разблокирует |
| Задача 5.1 (контракт «layers» `import-linter`) | Аким, после того как задача 1.1 `backend-layered-architecture` будет готова | То же |
| Выбор `uv` против `requirements.txt`+`.venv` (`design.md`, Open Questions) | Аким, отложено | Ничего; не меняет спеку и разбивку задач |
| Flat config ESLint против старого формата (`design.md`, Open Questions) | Аким, отложено | Ничего; деталь реализации задачи 3.2 |
| Ревью перед мержем (задача 7.2): change не свободен от кода, нужно ревью Егора или оркестратора | Егор / оркестратор | Не блокирует полный GO задачи 7.1, но блокирует мерж в `develop` |

## 5. Проходы 3-4 после переноса Егора в `ml/` (2026-10-03)

Егор перенёс пайплайн в `ml/` (`ml/pyproject.toml`, `ml/tests/`), а компоуз в `infra/`
(коммит `24797f7`). Коммит `11bdca4` обновил формулировки про корневые пути.

| Проход | Результат |
|---|---|
| 3 | 0 блокеров, 1 major, 5 minor (NOT READY). Major: критерий GO «`pre-commit run --all-files` проходит» не выполняется: `.secrets.baseline` называет пять перенесённых файлов и не покрывает backend-файлы, слитые после задачи 4.2 (Аким проверил на копии baseline: хук сообщает новые находки). Исправлено новой задачей 4.5 (пересканировать baseline и вручную проверить находки на `feature/dev-environment/backend`, заметка о файлах Егора в `docs/decisions/secrets-baseline-egor-files.md`), от которой теперь зависит задача 7.1. Исправлены minor: устаревшие пути в записи задачи 4.2, перепроверена задача 2.3 (`pytest backend/tests` из корня: 32 passed), фраза о контексте и заголовок решения 1, формулировки `proposal.md` |
| 4 | 0 блокеров, 0 major, 3 minor (имя файла заметки и его проверка, заметка идёт в `develop`, повод для повторного скана после следующего переноса). Все исправлены. **READY для DOR** |

Сам baseline — это код, его исправляет задача 4.5, а не эта правка. До неё
`pre-commit run --all-files` на `develop` падает.

| Пункт | Владелец | Что блокирует |
|---|---|---|
| Задача 4.5 (пересканировать `.secrets.baseline`) | Аким | Задачу 7.1 (полный GO) |

## 6. Вердикт по реализации (задача 7.1, 2026-10-04)

Задачи 4.6, 4.4, 5.1 и 4.5 сделаны в этом порядке на `feature/dev-environment/backend`
(`9dca91e`); записка о файлах Егора — на `develop` (`8526040`), задачи 6.1-6.2 тоже
(`40096fc`). `tester` проверял `9dca91e` со слитым `origin/develop` без коммита (во
временном worktree, потом удалён), как требует критерий задачи 4.5.

**Вердикт: GO** для фичи и для задачи 7.1. UI/UX: N/A, фронтенд не менялся
(`git diff --stat origin/develop -- frontend` пуст).

| Критерий | Подтверждение | Итог |
|---|---|---|
| `backend/check.sh` | exit 0; ruff и mypy чисто; `lint-imports`: 4 kept, 0 broken; pytest 685 passed, 1 skipped (модуль postgres, без `DEC_TEST_APP_DATABASE_URL`) | проходит |
| Покрытие ветвей бэкенда | `app`: 1637 операторов, 320 ветвей, 100.00%. `backend/scripts/check_env_example.py` вне порога, измерен `tester`: 97% ветвей (не покрыт только `__main__`, он запускается подпроцессом) | проходит |
| `frontend/check.sh` | exit 0; ветви 100% (0 из 0) — единственный порог в `vite.config.ts`; операторы 50%, функции 33.33%, строки 66.66% | проходит по правилу проекта (покрытие ветвей) |
| `pre-commit run --all-files` | exit 0, оба хука прошли | проходит |
| 4.5 | застейдженный фейковый ключ AWS роняет `detect-secrets`; все 22 пути baseline существуют; свежий скан даёт те же находки | проходит |
| 4.4 | без `# DEC_PARAMS_ROOT=` или `DEC_APP_DATABASE_URL=` хук падает и называет переменную | проходит |
| 5.1 | `test_import_contracts.py` 5 passed; сквозная проверка: импорт `parameters` из `engine` останавливает `check.sh` на `lint-imports` с именем импорта | проходит |
| 4.6 | `.env.example` называет `dec_normatives_reader`, базу `dec`, пароль-заглушку | проходит |
| OpenSpec | `validate bootstrap-dev-environment --strict` и `--all --strict` (20/20) проходят | проходит |
| Зона Егора | ни один файл в `ml/` и `infra/` не изменён | проходит |

### Решение: открытый вопрос о пороге покрытия бэкенда

- Вопрос (`design.md`, «Open Questions», последний пункт; задача 7.1): как базовые
  требования `development-process` «Test gate with >= 95% branch coverage» и
  «Go/No-Go verdict and archive» применяются, пока `backend/app/` нет и
  `backend/check.sh` не выдаёт числа покрытия.
- Решение: вопрос снят. `backend/app/` существует с момента слияния
  `backend-layered-architecture` (WP5, `53a4892`); с тех пор `backend/check.sh` запускает
  `pytest --cov=app --cov-branch --cov-fail-under=95`, и зона бэкенда проверяется, как
  любая другая. Исключение из правила 95% не нужно и не вводится. Это закрывает пункт
  «Open Questions» и условие задачи 7.1 и DOD.
- Подтверждение: вердикт выше, `check.sh` exit 0, покрытие ветвей 100.00%.
- Ветка `else pytest` в `check.sh` и сценарии «not yet present» в спецификации на
  `develop` больше не срабатывают; они остаются как есть, а `spec-keeper` на задаче 7.3
  решает, убирать ли их.
- Охват порога: только `app`. Скрипты в `backend/scripts/` покрыты своими тестами в
  `check.sh`, их покрытие измеряет `tester` при каждом вердикте.
- Решил Аким 2026-10-04 на основании GO от `tester`.

### Мелкие замечания, ни одно не блокирует

1. Сценарий «Config variable missing from the template» говорит, что проверка идёт
   хуком pre-commit, а не командой бэкенда; `test_check_env_example.py` проверяет то же и
   в `check.sh`. Строже спецификации; `spec-keeper` уточнит формулировку или отметит это
   на задаче 7.3.
2. `backend/scripts/` вне автоматического порога покрытия (см. решение выше).
3. Контракт `engine` — запрещающий список сегодняшних пакетов верхнего уровня; новый
   пакет `app.*` надо будет добавить в него.
4. `check_env_example.py` читает только константные `validation_alias`/`alias`, классы с
   базой по имени `BaseSettings` и только `backend/app/core/config.py`; `env_prefix`,
   `AliasChoices`, подклассы настроек или настройки в другом модуле потребуют доработки.
   К текущему коду и ветке WP9 это не относится.
5. Порог фронтенда стоит только на ветвях и выполняется при 0 из 0 ветвей; пороги по
   операторам, функциям и строкам решает фича `frontend-app`.
6. Задачи 4.4-4.6, 5.1 и 6.1-6.2 в `tasks.md` ещё не отмечены (отложенная отметка); их
   отмечают до архива.

| Пункт | Владелец | Что блокирует |
|---|---|---|
| Задача 7.2: ревью перед слиянием (Егор или оркестратор) | Егор / оркестратор | Слияние `feature/dev-environment/backend` |
| Повторить скан задачи 4.5 после слияния WP9 (его тесты добавляют пароли-заглушки) | Аким | `pre-commit run --all-files` на `develop` после этого слияния |
| Задача 7.3: синхронизация и архив | `spec-keeper` | Нужны 7.1 и 7.2 |

## 7. Ревью перед слиянием (задача 7.2, 2026-10-04)

Ревьюер: агент `orchestrator`, только чтение, на `9dca91e` со слитым `origin/develop`
(`7fd2f06`) в отдельном клоне. **Итог: APPROVED WITH FOLLOW-UPS.** Блокеров нет.
Слияние без конфликтов; на слитом дереве `backend/check.sh` выходит с 0 (4 контракта
соблюдены, 685 passed, покрытие ветвей 100.00%) и `pre-commit run --all-files`
проходит. Каждая из 32 находок baseline прочитана на своей строке; реальных секретов
нет. Ни один файл в `ml/` и `infra/` не изменён. С шестью мелкими замечаниями раздела 6
ревьюер согласен (шестое уже закрыто `7fd2f06`).

| # | Важность | Замечание | Что сделано |
|---|---|---|---|
| 1 | Major | `detect-secrets` сопоставляет по файлу и строке. (a) Архив этого изменения переносит `tasks.md`, и заглушка `user:password@` в задаче 4.3 становится новой находкой; (b) любая правка, сдвигающая отмеченную строку в одном из 22 файлов, роняет хук с кодом 3, пока он переписывает baseline, а baseline — код, так что коммит документа не может нести это обновление; (c) записка Егору называла только перенос и переименование | (a) сделано до слияния: задачи 4.3 и 4.6 переписаны без URL с учётными данными, baseline пересканирован на ветке; (b) вопрос в `docs/decisions/secrets-baseline-refresh-questions-akim.md`; (c) исправлено в `secrets-baseline-egor-files.md` |
| 2 | Minor | Записано только направление бэкенд -> `normatives_pipeline`; обратное (`ml/` импортирует `app`) — инструменты Егора | Записано здесь; входит в файл вопроса из 1(b) |
| 3 | Minor | `check_env_example.py` берёт первый из `validation_alias`/`alias` (pydantic предпочитает `validation_alias`) и угадывает имя для `AliasChoices`, `pydantic.Field`, `env_prefix` | Отложено (Аким, 2026-10-04): предпочитать `validation_alias`, падать с сообщением, если имя не прочитать |
| 4 | Minor | Новый пакет `app.*` верхнего уровня не попадает ни под один контракт | Отложено: `containers = ["app"]`, `exhaustive = true` в контракте слоёв |
| 5 | Note | У локального хука нет `language_version`; на Python < 3.10 скрипт падает | Отложено: `language_version: python3.12` |
| 6 | Note | `test_import_contracts.py` ищет `lint-imports` рядом с `sys.executable` без понятного сообщения | Отложено |
| 7 | Note | Регулярка шаблона принимает любой закомментированный `# NAME=`; устаревшие ключи не сообщаются | В рамках спецификации, ничего не делаем |
| 8 | Note | Один коммит на четыре подзадачи | Порядок и содержание согласованы, ничего не делаем |
| 9 | Note | `CLAUDE.md` (known issue, «на `feature/dev-environment/backend` также `lint-imports`») устареет при слиянии | Обновляется на `develop` после слияния |

Отложенные пункты 3-6 и покрытие `backend/scripts/` (раздел 6, замечание 2) уходят в
следующее изменение по инструментам или в бэклог WP6; им понадобится новый прогон
`tester`.

## 8. Синхронизация и архив (задача 7.3, 2026-10-04)

`spec-keeper` проверил предусловия (задачи 1.1-7.2 отмечены, разделы 6 и 7,
`openspec validate --all --strict` 20/20), затем:

- переписал в дельте сценарий «Config variable missing from the template»: «this check
  runs as a pre-commit hook, and the backend tooling command may also run it» (раздел 6,
  замечание 1);
- оставил три сценария «not yet present»: описанные ими защитные условия остались в
  `backend/check.sh` и `backend/scripts/check_env_example.py`, так что поведение они
  описывают верно; убрать их стоит, только если следующее изменение уберёт эти условия;
- отметил 7.3 и выполнил `openspec archive bootstrap-dev-environment --yes`: в
  `development-process` добавлены четыре требования («Backend tooling command»,
  «Frontend tooling command», «Import contract check», «Pre-commit secret scan and
  documented configuration»), остальное в базовой спецификации не изменилось.

После архива: `openspec validate --all --strict` 19/19 (`calculation-verification` и
`record-installed-skills-akim` по-прежнему валидны); `pre-commit run --all-files`
проходит, включая `detect-secrets` на перенесённых файлах.

Пока ни в одном активном изменении: раздел 6, замечание 2 (покрытие `backend/scripts/`),
раздел 7, пункты 3-6, и ответы на `secrets-baseline-refresh-questions-akim.md`; они
уходят в следующее изменение по инструментам.

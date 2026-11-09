# Проверка готовности: `calculation-verification` (WP4)

- Дата: 2026-09-27
- Change: `openspec/changes/calculation-verification/`
- Владелец: Аким. Раздел 4 (общие файлы: `tester.md`, `test-process`, `development-process`) требует согласия Егора (задача 4.1; согласовано 2026-10-11, применено 2026-10-20 в `2863bc9`).
- Критерии: `openspec/specs/development-process/spec.md`, «Planning before implementation» и «Go/No-Go verdict and archive» (синхронизированы из `team-roles-update`, WP7, 2026-09-27); собственный `tasks.md` этого change, раздел «DOD and Go / No-Go».

Английская версия: `calculation-verification-readiness.md`. Более ранняя запись по черновику change — `docs/reports/WP4_report.md` (2026-09-26, на русском); этот файл — отслеживаемая запись сегодняшнего спекового гейта.

## Итоговый статус

**GO (реализация, фича `calculation-verification-backend`) — 2026-10-20**; см. раздел 5. Вердикт спековой фазы ниже остаётся как был.

**GO (спековая фаза, задача 1.5) — 2026-09-27**

`openspec validate --all --strict` проходит, сегодня прошли три прохода `spec-reviewer` по текущему тексту (проход 3: 0 блокеров, 0 major), и ни одно нормативное значение, допуск, редакция или пункт не зафиксированы ни в одной дельте спек. `tester` объявил GO по спековой фазе, см. раздел 3. Разделы реализации 2 и 3 остаются открытыми и этим вердиктом не покрыты.

| Условие DOD (`tasks.md`) | Состояние | Подтверждение |
|---|---|---|
| `openspec validate --all --strict` проходит | Выполнен | 17/17, см. раздел 1 |
| Отчёт `spec-reviewer` по текущей версии: без блокеров и major | Выполнен | 3 прохода сегодня; проход 3: 0 блокеров, 0 major, 2 старых non-gating minor; см. раздел 2 |
| `norm-traceability-checker` подтверждает отсутствие нормативных значений и допусков | Выполнен | Отдельный проход checker по сегодняшнему тексту не запускался; три прохода spec-reviewer и собственная независимая проверка `tester` обеих дельт спек не нашли зафиксированных значений, допусков, редакций или пунктов (каждое упоминание `tolerance`/`tolerance_kind`/`tolerance_source` — это поле, `edition` может быть `unverified`); отмечено как процессный пробел, не дефект, в разделе 3 |

## 1. `openspec validate --all --strict`

```
Totals: 17 passed, 0 failed (17 items)
```

Запускалась после каждого из трёх проходов ниже и после вердикта `tester`; результат одинаковый каждый раз.

## 2. Проходы `spec-reviewer` (сегодня)

Дельта спек этого change (`specs/calculation-verification/spec.md`, `specs/calculation-engine/spec.md`, `specs/development-process/spec.md`) не менялась с момента черновика в коммите `fec56dc`. Один проход ревью прошёл около момента написания (записан в `docs/reports/WP4_report.md`: 0 блокеров, 10 major, 5 minor, исправлены внутри change, но никогда не перепроверены заново — отмечено там как открытый пункт). С тех пор `proposal.md`, `design.md` и `tasks.md` правились несколько раз (задача 1.4 подтвердила решения 7 и 9 `design.md`; задачи 2.6 и 4.2 закрыты; ссылки на NormRef обновлены на письменные ответы Егора, коммит `a1a896c`). До сегодняшнего спекового гейта ни один свежий полный проход не подтверждал текущий текст.

### Проход 1: 1 блокер, 2 major, 1 minor

- **Блокер:** не было свежего, зафиксированного прохода `spec-reviewer` по текущему тексту — против требования «Planning before implementation» в `openspec/specs/development-process/spec.md` (синхронизировано из WP7 в тот же день): отчёт без блокеров и major должен существовать «для текущей версии change».
- **Major (a):** строка DOD в `tasks.md` для спековой фазы говорила только «`spec-reviewer` reports no blockers», опуская «no major finding» и «current version» — слабее и не согласуется с уже действующей спекой.
- **Major (b):** 10 major/5 minor замечаний первоначального прохода никогда не были перечислены поимённо, только посчитаны, поэтому не было прослеживаемости, что они действительно исправлены.
- **Minor (старое, non-gating):** «Calculation latency» в `specs/calculation-engine/spec.md` пока не тестируема, потому что «типичный расчёт» не определён; задача 3.7 уже помечена `[blocked: typical calculation]`.
- Собственный раздел «Checks that passed» ревьюера показал, что он уже провёл реальную содержательную проверку (ни одно нормативное значение/допуск/редакция/пункт не зафиксированы; `design.md` согласован; ответ Егора подлинный; перекрёстные ссылки задач верны) — поэтому major (b) был признан закрываемым, как только проход будет зафиксирован, а не признаком реального необнаруженного дефекта.

Исправление: строка DOD спековой фазы в `tasks.md` переформулирована на «a `spec-reviewer` report on the current version of the change lists no blocker and no major finding (`openspec/specs/development-process/spec.md`, "Planning before implementation")» — закрывает major (a).

### Проход 2 (после правки DOD): 0 блокеров, 1 major, 2 minor

- **Major:** раздел «Why» в `proposal.md` ссылался на `docs/audit/03-verified-roadmap.md` как на источник обоснования. По `.gitignore` `docs/audit/` не отслеживается (только `docs/decisions/` и `docs/reports/`), поэтому это нарушало требование «Shared decisions are tracked» из `openspec/specs/development-process/spec.md` (добавлено WP7, слито в тот же день): обоснование должно ссылаться на отслеживаемый файл или пересказывать рассуждение, а не цитировать неотслеживаемый внешний документ. Тот же паттерн отмечен (вне области этого прохода) в `calculation-core-contract/proposal.md` и `retarget-mvp-domain/proposal.md`.
- **Minor (старое, non-gating):** тот же пробел с тестируемостью задержки.
- **Minor (non-gating):** исходные замечания по-прежнему не перечислены поимённо; понижено с major прохода 1, поскольку DOD теперь требует только свежий проход по текущему тексту, который этот проход и дал.

Исправление: цитирующее предложение сокращено, ссылка на `docs/audit/03-verified-roadmap.md` убрана, три пункта под ней (с метками A3, A4+C9, E1) оставлены — каждый уже пересказывает своё рассуждение с отслеживаемым подтверждением (конкретные номера строк `spec.md`) — замена ссылки не понадобилась.

### Проход 3 (финальный, после обеих правок): 0 блокеров, 0 major, 2 minor (оба старые, non-gating)

Подтверждено: раздел «Why» читается связно после удаления ссылки — метки A3/A4+C9/E1 работают как неформальные ярлыки замечаний, а не повисшие ссылки, поскольку у каждой есть своё отслеживаемое подтверждение. Grep по всему каталогу change на `docs/audit` не дал совпадений. Единственные другие ссылки на `docs/` в change (`docs/decisions/normref-questions-egor.md`, `docs/decisions/reference-examples-foundations.md`) явно разрешены в `.gitignore` и подтверждённо отслеживаются. Оба старых minor переходят без изменений и не блокируют DOR (у тестируемости задержки есть маркер заблокированной задачи; старые замечания перекрыты этими тремя проходами).

**Вердикт: READY for DOR.**

## 3. Вердикт tester (задача 1.5, только спековая фаза)

```
Verdict: GO (spec phase only, task 1.5)
Change: calculation-verification (WP4), develop, 2026-09-27
Conditions:
- Validation: PASS. `openspec validate calculation-verification --strict` -> valid. `openspec validate --all --strict` -> 17/17.
- spec-reviewer no blocker/major (current text): PASS. Grepped the whole change directory for `docs/audit` -- zero matches. The remaining citation to `docs/decisions/normref-questions-egor.md` (commit `a1a896c`) is confirmed tracked in git, so it satisfies "shared decisions are tracked". `tasks.md` contains the fixed DOD wording exactly as cited.
- norm-traceability-checker: PASS, with a flag. No dedicated checker pass is logged against today's text -- only the spec-reviewers' general content check. The tester independently read all three delta specs in full: every `tolerance`/`tolerance_kind`/`tolerance_source` occurrence is a field the engineer fills in later, never a fixed number; no norm edition or clause is asserted as fact. The one concrete number in the diff, the 30-second latency target, is not new -- it moved unchanged from the requirement being removed, per its own Migration note, and was already flagged as the pre-existing latency-testability minor. No genuine gap found, but the absence of a dedicated checker run is a process gap, not a blocker.
```

Вердикт (оставлен на английском, как выдан) покрывает только спековую фазу. Разделы 2 и 3 (реализация: эталонные примеры, регрессионный корпус, инвариантные тесты, метрики) остаются открытыми и не покрыты. Оба старых minor (тестируемость задержки; старые замечания не перечислены) переходят как non-gating.

## 4. Открытые пункты, переносимые дальше

| Пункт | Владелец | Что блокирует |
|---|---|---|
| «Calculation latency» в `specs/calculation-engine/spec.md`: «типичный расчёт» не определён | Инженер (Аким, или инженер, заполняющий `reference-examples-foundations.md`) | Только задачу 3.7; уже помечена `[blocked: typical calculation]` |
| Правки общих файлов раздела 4 (`tester.md`, `test-process`, `development-process`) требуют согласия Егора | Егор | Задача 4.1; не часть этого GO |
| ~~Алгоритм `input_hash` в `calculation-core-contract` остаётся «предложением для ревью»~~ Закрыто 2026-10-03: Егор принял без изменений (`calculation-core-contract`, задача 1.8, `a01af6f`) | Аким/Егор, через тот change | Сейчас ничего (было: регрессионный корпус, задачи 3.2–3.3) |
| Эталонные примеры, инварианты и определение «типичного расчёта» для `foundations-shallow` | Аким (инженер) | Разделы 2–3; см. `docs/decisions/reference-examples-foundations.md` |
| Отдельный проход `norm-traceability-checker` по текущему тексту не запускался (только содержательные проверки ревьюеров и tester) | — | Ничего сегодня; отмечено для следующей содержательной правки |

## Повторное ревью после ответов Егора (2026-10-03)

Два прохода `spec-reviewer` по текущему тексту после коммита `11bdca4` (задача 1.8
`calculation-core-contract` закрыта, алгоритм `input_hash` не изменился; пайплайн Егора
переехал в `ml/` и `infra/`). Первый проход: 0 блокеров, 0 major, minor по формулировкам
(места про задачу 1.8 в настоящем времени, пути, абзац об открытых вопросах), всё исправлено.
Второй проход: 0 блокеров, 0 major, замечаний нет. **READY для DOR.**

## 5. Вердикт tester (реализация, 2026-10-20)

`tester` работал на `feature/calculation-verification/backend` в `7271240` (с влитым
`develop`). Задачу 3.7 (тест задержки) Аким в тот же день вынес в follow-up (`0fb0825`,
раздел 5 `tasks.md`). Открыты до этого вердикта были только 6.1 и 6.2.

```
Verdict: GO (implementation phase, feature calculation-verification-backend)
Change: calculation-verification (WP4), 2026-10-20
Feature/branch/commit: calculation-verification-backend, feature/calculation-verification/backend, 7271240
Conditions:
- Тесты: PASS. `./check.sh` завершается с кодом 0: ruff чист; mypy «no issues found in 154 source files»; lint-imports «5 kept, 0 broken» (в том числе «verification imports from the application only engine, schemas and core»); pytest «1155 passed, 11 skipped», seed hypothesis 2271787898. Все 11 пропусков — из-за окружения (переменные каталога и базы приложения в этом прогоне не заданы).
- Покрытие: PASS. Всего 100.00% по ветвям (2755 операторов, 504 ветви); каждый модуль app/verification — 100%.
- Прогон на каталоге: PASS. `pytest -m postgres tests/test_verification_catalog_properties.py tests/test_catalog_ingested.py` с заданной DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL: 10 passed, seed 4026219359; повтор с seed 20261020: 10 passed. У каждого из 7 property-тестов на каталоге: 100 passing, 0 failing, 0 invalid.
- Полнота инвариантов: PASS, опирается на прогон на каталоге. У пилота 11 инвариантов (2 общих, 3 не зависящих от формулы, 6 зависящих), у каждого зарегистрирован property-тест; 6 формульных и тест порога k_z прошли на каталоге при обоих seed. Контрольные прогоны на синтетическом R идут в обычном наборе, и показано, что тест порога ловит скачок.
- Условие корректности: НЕ ПРИМЕНЯЕТСЯ (дельта development-process, сценарий «Change without calculation code»). `git diff --name-only develop...HEAD` не затрагивает backend/app/engine, backend/app/services, backend/app/parameters и backend/params; фича добавляет фреймворк верификации, тесты, контракт импортов и dev-зависимость Hypothesis. Отчёты фреймворка (SuiteReport, GoReport с тремя метриками, регрессионный раннер) проверены только на синтетическом типе: ни у одного типа расчёта ещё нет настоящих эталонных примеров и сохранённого корпуса.
- Валидация: PASS. `openspec validate --all --strict`: 21 passed, 0 failed.
- Дельты и реализация: PASS (выборочно). У каждого требования и сценария дельты calculation-verification названы тесты (эталонные примеры, регрессионный корпус, инвариантные тесты, метрики); «Calculation accuracy» дельты calculation-engine держится отклонением по каждой величине. Не покрыто по замыслу: «>= 3 примера на тип» для foundations_shallow_r (non-goal, follow-up), настоящий замороженный корпус, пересчитываемый при каждом изменении (design.md, решение 18, открыто), «Calculation latency» (follow-up, бывшая задача 3.7). Условие development-process внесено в tester.md и скилл test-process (2863bc9).
- UI/UX: N/A, фича не меняет интерфейс.
- Безопасность: PASS. `pre-commit run --all-files` проходит; в diff нет учётных данных, eval/exec, subprocess или небезопасного загрузчика. URL роли-читателя использовался только в командной строке.
```

Находки, ни одна не блокирует:

1. Следующий change, добавляющий расчёт (например `foundations-pressure-from-loads`), по
   условию корректности не получит GO без хотя бы 3 настоящих эталонных примеров: короткий
   набор недействителен, значит NO-GO. Сейчас их нет ни у одного типа. Эталоны инженера и
   источник параметров по решению 14 нужно спланировать до этого change или вместе с ним.
2. Настоящий регрессионный корпус не был записан в follow-up. Он добавлен в раздел 5
   `tasks.md` вместе с этой записью, как требует задача 6.2 для открытых пунктов перед
   архивом.
3. Полнота инвариантов засчитывает зарегистрированный тест и тогда, когда он пропущен,
   поэтому один `check.sh` показал бы GO с пропущенными 6 формульными инвариантами. GO
   будущего change, затрагивающего формулу или каталог пилота, ссылается на прогон с
   заданной `DEC_TEST_INGESTED_NORMATIVES_DATABASE_URL`, как этот.
4. Прогон на каталоге шёл на временной базе `dec` через роль только для чтения
   `dec_normatives_reader` (ингест 2026-10-13), а не на `_test`-базе. Допустимо, потому что
   роль только читает.
5. `StarletteDeprecationWarning` (httpx с `starlette.testclient`) был и до этой фичи.

Дальше: ревью фичи `orchestrator` (AGENTS.md, раздел 2, шаг 7, выбор Акима), затем
слияние в `develop`, затем 6.1-6.2 (синхронизация и архив `spec-keeper`).

## 6. Ревью orchestrator (2026-10-21)

Ревьюер: агент `orchestrator`, выбран Акимом вместо Егора (AGENTS.md, раздел 2, шаг 7).
Объём: diff `develop...feature/calculation-verification/backend` в `7271240` против
proposal, решений 1-18 design.md, трёх дельт спек и `tasks.md`. Во временном worktree
запущены тесты верификации (182 passed, 7 skipped без базы, `app/verification` 100% по
ветвям), проверка передачи seed и мутационные пробы. Не запускались: тесты с базой, весь
`check.sh`, `openspec validate` (их прогнал `tester`, раздел 5).

**Вердикт: changes requested** (одна находка major), со слиянием без нового круга `tester`
после исправления находки 1, потому что исправление не трогает логику GO.

| # | Уровень | Находка | Решение |
|---|---|---|---|
| 1 | major | `within_tolerance` сравнивает в двоичной арифметике, поэтому десятичное значение на границе оказывается вне допуска (245.2 против 245.3 при 0.1 даёт `0.10000000000002274`; 0.33 против 0.3 при относительном 0.1 — так же); тесты границы брали значения, точные в двоичной записи | Исправлено в `361aa97`: запас в 4 единицы последнего разряда (`FLOAT_SLACK_ULPS`) и шесть десятичных граничных тестов. Вместо предложенного `Decimal` из `repr`, потому что значение, переведённое в другую единицу, несёт шум `float`, который `repr` сохраняет. Запас записан в решении 15 `design.md` |
| 2 | minor | Повторённые `example_id` засчитываются в минимум из 3 | Исправлено в `361aa97`: причина `DuplicateExampleId`; минимум считается по разным идентификаторам |
| 3 | minor | `run_suite([])` и `go_report` от него дают GO | Исправлено в `361aa97`: пустой прогон — NO-GO; `Reproducibility.verdict` без примеров — NO-GO |
| 4 | minor | Три теста проходят при сломанном поведении: (a) не проверяется `old` объявления, (b) единица в регрессионном сравнении, (c) `unit_change_holds` без перевода | Исправлено в `361aa97`: по тесту на каждое; (c) — отрицательный контроль с подменённой `calculate`, которая видит единицы |
| 5 | minor | `CorpusEntry.outputs` принимает одну величину дважды, побеждает последняя | Исправлено в `361aa97`: валидатор уникальности величин |
| 6 | note | Парсер объявленных отличий снисходителен (строка заголовка, строки без ведущей черты, `#` в блоке кода, `""` и `-` как «нет выхода»); все случаи безопасны | Follow-up, раздел 5 `tasks.md` |
| 7 | note | Пример с ошибкой считается «невоспроизведённым» и не попадает в `failures` | Follow-up, раздел 5 `tasks.md` |
| 8 | note | Для настоящего корпуса: сборка пересчитывает корпус базовой ветки и читает объявления из change | Добавлено к follow-up «настоящий регрессионный корпус», раздел 5 `tasks.md` |
| 9 | note | Ничто не закрепляет, что `app/verification` не импортирует Hypothesis | Follow-up, раздел 5 `tasks.md` |
| 10 | note | Тесты пилота повторяют границы `PILOT_RANGES` и единицы длины | Follow-up, раздел 5 `tasks.md` |
| 11 | note | Шапка с seed не печатается при `pytest -q` (`check.sh` не использует `-q`) | Follow-up, раздел 5 `tasks.md` |

Ревьюер проверил и нашёл в порядке: границу допуска и единицу сравнения (решение 15),
вердикт набора и причины недействительности, три метрики против их определений, GO-отчёт,
регрессионное сравнение, seed по решению 16, отсутствие значений нормы в коде и тестах,
чистоту функций и слои, русские docstring в стиле Google.

После исправлений (`361aa97`): каждый новый тест падает при откате своего исправления
(поймано 9 мутаций из 9); `check.sh`: ruff, mypy, lint-imports чисты, 1169 passed, 11
skipped, покрытие по ветвям 100%. Дальше: слияние фичи в `develop`, затем 6.1-6.2.

## Финальная версия и готовность синхронизации (2026-11-09)

Задача 6.1 выполнена. Принятая финальная версия verification 361aa97 является
точным вторым родителем слияния 38f9185, предка текущего develop на 5a59fcc.
Все отслеживаемые файлы приложения verification и тестов, включая
pilot_invariants.py, побайтово совпадают с этой версией. До этой проверки закрытия
артефакты change и запись готовности не менялись после интеграции.

Основанием приёмки остаётся tester GO на 7271240, затем явное разрешение
orchestrator на слияние после требуемого исправления без нового раунда tester.
Исправления 361aa97 и записанная полная проверка (1169 passed, 11 skipped, 100%
branch coverage) сохранены в разделе 6. Более поздний или новый tester GO
не выводится из этих записей. UI/UX остаётся N/A: feature не меняет UI. Пропущенные
проверки БД не представлены как новые проверки; исторические запуски каталога
из раздела 5 остаются свидетельством для указанной там версии.

Предпросмотр трёх основных specs применяет семь ADDED и одно REMOVED требование
к calculation-engine, calculation-verification (новый основной spec) и
development-process. Существующие Purpose и незатронутые требования/сценарии
сохранены. Единственное исправление ссылки жизненного цикла в активной дельте
указывает каноническую foundations-shallow вместо ещё не архивированной дельты
retarget; правила происхождения эталонов, допусков и корректности не меняются.
Текущее ревью без записи файлов: 0 blocker, 0 major, 0 minor; готовность
к выбору синхронизации/архивации.

Выбранная strict validation прошла; все фактические specs/активные changes прошли
21/21. Изолированная копия основных specs с кандидатами прошла 15/15. Существующее
сообщение archive-target другого formula-extractor-fix остаётся информационным.
Основные specs и активный каталог не менялись; задача 6.2 открыта до выбора
синхронизации/архивации по workflow. Commit, merge и push для этой проверки
не выполнялись, тесты приложения повторно не запускались.

Реальные эталоны, реальный замороженный корпус/интеграция сборки и определение
типового расчёта для задержки остаются принятыми последующими задачами раздела 5.
Архивация framework не доказывает корректность расчётного типа и не даёт три
допущенных эталона, необходимые для GO будущего типа из нагрузок.

## Основные specs синхронизированы, change framework архивирован (2026-11-09)

Аким явно разрешил синхронизацию и архивацию в разговоре с пользователем. Три
канонических specs точно совпадают по SHA-256 с проверенным предпросмотром:
calculation-engine, calculation-verification и development-process. Все семь
ADDED и одно REMOVED требование сверены с активными дельтами перед переносом
change. Существующие основные Purpose, незатронутые требования и сценарии
сохранены; Purpose новой capability совпадает с её дельтой. Использован ранее
полученный снимок инструкций specs.

Выбранная strict validation change прошла с явным --type change; фактические
основные specs прошли 15/15. Каталог целиком, включая .openspec.yaml, перенесён
в `openspec/changes/archive/2026-11-09-calculation-verification/`. Общая strict
validation после архивации прошла 21/21. Задача 6.2 выполнена; открытых флажков
задач не осталось. Счётчик сохранён: добавлен один основной spec и архивирован
один активный change. Сообщение archive-target другого formula-extractor-fix
остаётся информационным.

Прежние свидетельства приёмки framework, указанные выше, остаются основанием
закрытия; новый tester GO или запуск тестов приложения/БД/каталога не заявляются.
Операция изменила только документацию. Реальные эталоны, реальный регрессионный
корпус/интеграция сборки и определение типового расчёта для задержки остаются
явными принятыми последующими задачами раздела 5. Архивация не доказывает
корректность расчёта и не выполняет гейт трёх эталонов для GO будущего типа
из нагрузок. Commit, merge и push не выполнялись. Оставшийся предшествующий
канонический владелец для проверки контракта из нагрузок: frontend-app.

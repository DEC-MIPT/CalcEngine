# Проверка готовности: `calculation-verification` (WP4)

- Дата: 2026-09-27
- Change: `openspec/changes/calculation-verification/`
- Владелец: Аким. Раздел 4 (общие файлы: `tester.md`, `test-process`, `development-process`) требует согласия Егора (задача 4.1, ещё не применено).
- Критерии: `openspec/specs/development-process/spec.md`, «Planning before implementation» и «Go/No-Go verdict and archive» (синхронизированы из `team-roles-update`, WP7, 2026-09-27); собственный `tasks.md` этого change, раздел «DOD and Go / No-Go».

Английская версия: `calculation-verification-readiness.md`. Более ранняя запись по черновику change — `docs/reports/WP4_report.md` (2026-09-26, на русском); этот файл — отслеживаемая запись сегодняшнего спекового гейта.

## Итоговый статус

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
| Алгоритм `input_hash` в `calculation-core-contract` остаётся «предложением для ревью» | Аким/Егор, через тот change | Регрессионный корпус (задачи 3.2–3.3) |
| Эталонные примеры, инварианты и определение «типичного расчёта» для `foundations-shallow` | Аким (инженер) | Разделы 2–3; см. `docs/decisions/reference-examples-foundations.md` |
| Отдельный проход `norm-traceability-checker` по текущему тексту не запускался (только содержательные проверки ревьюеров и tester) | — | Ничего сегодня; отмечено для следующей содержательной правки |

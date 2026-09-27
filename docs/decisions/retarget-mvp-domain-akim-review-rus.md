# `retarget-mvp-domain` (WP1): задачи проверки Акима

- Дата: 2026-09-27
- От: Аким. Кому: Егору (ведёт WP1).
- Объём: задачи `[Akim]` из `openspec/changes/retarget-mvp-domain/tasks.md`: 2.1, 2.2, 5.1, 5.4. Части Егора (`normatives-catalog`, списки `foundations-shallow`, решения в `design.md`) здесь не правятся; замечания к ним перечислены для Егора.

Английская версия: `retarget-mvp-domain-akim-review.md`.

## Итог

| Задача | Результат |
|---|---|
| 2.1 Дельты движка и вывода совпадают с `calculation-core-contract` | Найдены и исправлены три расхождения в дельтах Акима (`calculation-engine`, `transparent-output`); см. раздел 1 |
| 2.2 Дедупликация `web-platform` / `user-accounts`, нет требований без владельца | Пройдено; отмечены два minor-дубля |
| 5.1 `openspec validate --strict` | Пройдено: change валиден; `--all`: 17/17 |
| 5.4 Grep по ключевым словам в `openspec/` вне `archive/` | Пройдено: каждое совпадение в файле из раздела 4 задач |

## 1. Задача 2.1: дельты движка и вывода против `calculation-core-contract`

`calculation-core-contract` (WP2) учитывает проверенность по шагам трассы: у каждого шага
есть `norm_refs`, шаг считается проверенным, только если проверены все его ссылки, а
конверт результата считает остальные в `unverified_step_count`. Его отказ
(`verdict = refused`) — для входов вне области метода, и он называет нарушенную границу с
её списком `NormRef`. WP1 архивируется раньше WP2, поэтому сценарии WP1 ниже описывают
поведение, не называя требования и поля конверта WP2.

| № | Дельта, сценарий | Расхождение | Исправление |
|---|---|---|---|
| 1 | `calculation-engine`, «Unverified norm source» | Весь результат помечался `source: unverified`, и движок «не считал его проверенным»; в WP2 нет пометки на уровне результата, и вердикт от этого не зависит | Расчёт всё равно выполняется, шаг помечается непроверенным, результат сообщает, сколько шагов непроверены, и никогда не подаётся как полностью проверенный |
| 2 | `calculation-engine`, «Out-of-scope type» | Отказ по объёму продукта не был отделён от отказа WP2 для входов вне области метода | Отказ до запуска расчёта, называет ограничение объёма из `foundations-shallow`, отдельно от отказа по области метода |
| 3 | `transparent-output`, «Inspect a calculation step» | Одна ссылка на шаг; в WP2 у шага список | «каждая нормативная ссылка, на которую опирается шаг»; «Unverified reference is visible» теперь говорит о любой ссылке шага |

«Unverified reference is visible» оставлен намеренно: в базовом требовании «Normative
clause references» нет правила о непроверенных ссылках, а WP2 добавляет его только при
своей архивации, после WP1.

Порядок архивации: WP1, WP2 и WP4 (`calculation-verification`) затрагивают разные
требования `calculation-engine` и `transparent-output`, так что ни одно требование не
меняется двумя из них.

`spec-reviewer` по исправлению: см. раздел 5.

## 2. Задача 2.2: дедупликация `web-platform` и `user-accounts`

Ни одно требование не потеряло владельца. Авторизацией владеет `user-accounts` «Single
authorization», `web-platform` «Single authorization» на него ссылается. Лимитами тарифов
владеет `user-accounts` «Subscription tiers», на него ссылается `product-vision`
«Subscription monetization». «Free trial», «User registration and authentication» и
«Billing deferred for MVP» остаются в `user-accounts`; «Unified web interface», «Backend
API» и «Non-functional — integration and latency» остаются в `web-platform`. Из обеих спек
ничего не удалено.

Minor, не исправлено (решает владелец change):

- Срок триала «14-day» записан в `product-vision` «Subscription monetization» и в базовом `user-accounts` «Free trial». Решение 3 в `design.md` делает `user-accounts` владельцем правил триала.
- `user-accounts` «Billing deferred for MVP» повторяет non-goal `product-vision` «billing or payment integration» и добавляет, что состояние подписки ведётся администратором.

## 3. Задача 5.1: валидация

`openspec validate retarget-mvp-domain --strict`: валиден. `openspec validate --all --strict`: 17 passed, 0 failed.

## 4. Задача 5.4: grep по ключевым словам

Команда: `grep -rni "beam\|16\.13330" openspec/ --exclude-dir=archive`. Девять совпадений, все ожидаемые:

- `openspec/changes/backend-layered-architecture/tasks.md:21, 27, 32` и `design.md:63`: задачи 4.1 и 4.2 (Егор).
- `openspec/specs/product-vision/spec.md:39, 44`, `calculation-engine/spec.md:15, 16`, `normatives-catalog/spec.md:33`, `transparent-output/spec.md:17`: каждое внутри требования, которое дельта этого change удаляет или заменяет, поэтому синхронизация при архивации его уберёт (задача 4.3).

## 5. Ревью исправления

`spec-reviewer` по исправленным дельтам: 0 блокеров, 0 major, 3 minor; вердикт READY. Он
подтвердил, что три сценария согласуются с «Typed trace step» и «Applicability check with
three outcomes» WP2, что ни один сценарий WP1 не называет поля, которые есть только в WP2,
что используется только синтетическая заглушка и что ни одно имя требования не
затрагивают сразу два из WP1, WP2 и WP4. Minor: у «never presented as fully verified» не
было наблюдаемой точки (теперь «no label or conclusion shown with the result claims that
it is fully verified»); «not listed in `foundations-shallow`» не уточняло, какой список
(теперь «not on the in-scope list»); заключительная фраза «Out-of-scope type» поясняет, а
не задаёт отдельную проверку (оставлена).

## 6. Для Егора

- `normatives-catalog` «Norm reference status», сценарий «Reference checked»: «is no longer marked `unverified`». По решению 7 WP2 `NormRef`, закреплённый в сохранённом результате, неизменяем; проверенная ссылка — новая версия для новых запусков. Стоит это сказать (задача 3.3).
- `tasks.md` этого change всё ещё называет историческую ветку `Specs` (строки 5–6 и задача 5.6). Остальные change теперь говорят, что спековая работа вливается в `develop`, как только готова, и закрываются шагом «confirm the final version of the change is on `develop`».
- Два minor-дубля из раздела 2.

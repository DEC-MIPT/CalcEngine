# WP1 — отчёт: черновик change `retarget-mvp-domain`

Дата: 2026-09-26. Автор черновика: Akim (с помощью Claude Code). Ведёт change: Egor. Scope и non-goals утверждает PM (Есения).

Статус: черновик, не закоммичен. `openspec validate --all --strict` проходит (12/12).

## Что создано

В `openspec/changes/retarget-mvp-domain/`:

- `.openspec.yaml`, `proposal.md`, `design.md`, `tasks.md`.
- `proposal.md`: цель, мотивация (A1, A2 с C7 и C8, E3) и раздел Non-goals.
- `design.md`: таблица «правило → спека-владелец» и допущения.
- `tasks.md`: задачи размечены `[Akim]`, `[Egor]`, `[PM]`, `[Agent]`, есть DOR и DOD.
- Дельты в `specs/`:
  - `product-vision`
  - `calculation-engine`
  - `normatives-catalog`
  - `transparent-output`
  - `web-platform`
  - `user-accounts`
  - `foundations-shallow` (новая capability)

В `openspec/config.yaml` заменено только предложение про домен (строки 21–23).

## Пять ключевых требований

| Требование | Где |
|---|---|
| Объём MVP называет оба домена и порядок | `product-vision`, «MVP domains and their order» |
| Out-of-scope первого домена | `foundations-shallow`, сценарий отказа с названием ограничения |
| Non-goals до защиты | `product-vision`, «Non-goals before the defense» |
| Нормативные ссылки: сверено или `source: unverified` | `normatives-catalog`, «Norm reference status»; пример в `transparent-output` заменён на синтетический |
| Один владелец на требование | лимиты B2B/B2C и авторизация — только в `user-accounts`, остальные ссылаются |

## Помечено «DRAFT — needs Egor review»

- Весь `proposal.md`, `design.md`, `tasks.md`.
- Сценарий и требование «Binding a normative to a calculation type» и требование «Norm reference status» в дельте `normatives-catalog`.
- Оба списка в `foundations-shallow` (in-scope и out-of-scope): в них `TBD`, ничего не придумано.
- Название вехи второго домена и порядок доменов в `product-vision`.
- Лимит B2C в 100 расчётов помечен как unverified до решения PM.
- Non-goals помечены «PM approval pending».

## Что осталось от старого домена

`grep` вне `archive/` (архив пуст) находит два типа мест:

- `openspec/specs/*` (`product-vision`, `calculation-engine`, `normatives-catalog`, `transparent-output`): очистятся при sync/archive, напрямую не правились.
- `backend-layered-architecture` (`tasks.md` строки 21, 27, 32 и `design.md` строка 63): не правились, заведены задачи 4.1 и 4.2 на Egor.

Пока задачи 4.1 и 4.2 не выполнены, критерий карты «0 попаданий» не пройдёт.

## Допущения

1. Kickoff-файла с разделом Decision в репозитории нет. Порядок доменов (фундаменты мелкого заложения, затем внутреннее водоснабжение) взят из ответа Akim и `CLAUDE.md`.
2. Список non-goals со встречи с PM не найден. Использован пример из раздела 3.1 карты: billing, NLP/RAG в продукте, PDF, multi-tenant audit trail.
3. Валидатор не принимает MODIFIED, который выбрасывает старый сценарий. Поэтому «MVP scope» и «Deterministic verified calculation» оформлены как REMOVED плюс ADDED под новыми именами; общий текст требований сохранён.
4. Для водоснабжения отдельной capability нет: карта разрешает одну, второй домен только назван в `product-vision`.
5. Формат поля нормативной ссылки не фиксировался: он относится к запланированному change `norm-source-traceability`.
6. В тексте change не использованы слова про старый домен, чтобы не портить `grep`-критерий.

## Следующие шаги

- Egor: проверить и переписать свои части, заполнить списки в `foundations-shallow`, выполнить задачи 4.1 и 4.2.
- PM (Есения): подтвердить порядок доменов, список non-goals и лимит B2C.
- Затем: `spec-reviewer`, `norm-traceability-checker`, вердикт `tester`, merge в `Specs`, архивация через `spec-keeper`.

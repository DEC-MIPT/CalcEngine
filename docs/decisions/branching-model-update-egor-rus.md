# Модель веток: документы прямо в `develop`, код по feature-веткам (просьба подтвердить Егору)

- Дата: 2026-09-28
- От: Аким. Кому: Егор.

English version: `branching-model-update-egor.md`.

## Решение

Меняются два правила, для обоих разработчиков.

1. **Документы коммитятся прямо в `develop`**, без подветки и без merge-коммита.
   Документ — это файл из существующего списка «no code»: `openspec/**`, `docs/**`,
   `agent-docs/**`, определения агентов и скиллов в `.claude/`, `.kilo/`, `.kilocode/`,
   `AGENTS.md`, `CLAUDE.md`, `README.md`, `.editorconfig`. Причина: ты читаешь `develop`,
   а не мои подветки, и каждый merge документов заставлял нас обоих подтягивать изменения
   в свои ветки.
2. **Код идёт только через feature-ветку** `feature/<feature>/<zone>`, по одной ветке на
   feature (компонент или этап плана). Она вливается в `develop` только когда feature
   готова целиком: отмечены все задачи, которые `tasks.md` отдаёт этой feature, GO от
   `tester`, ревью пройдено. GO выдаётся на feature, change архивируется, когда влиты все его feature. У feature ровно одна
   ветка, работа в двух зонах — это две feature. Feature принадлежит одному change, в change
   может быть несколько feature. Не по секциям и не по подзадачам. Ветка пушится в `origin` после
   каждой законченной подзадачи и получает новые
   документы через `git merge develop`. Любой файл вне списка документов (исходники,
   тесты, манифесты пакетов, `.gitignore`, настройки агентов, pre-commit,
   `docker-compose.yml`) для этого правила считается кодом.

Перед каждым коммитом и пушем в `develop` нужно выполнить `git fetch --all` и
`git pull --ff-only`; если `develop` разошёлся, остановиться и разобраться.

## Что я изменил в `develop`

`AGENTS.md` (Branching rules, шаги 4 и 7 жизненного цикла, DOR), спеку `development-process`
(требование «Branch-per-feature with zone sub-branches» и новое «Documents commit directly
to develop»), `openspec/config.yaml`, скиллы `branching-convention` и `sdd-workflow`,
агентов `orchestrator`, `business-analyst`, `backend-developer`, `frontend-developer`,
`data-engineer`, `spec-reviewer` (обе копии, `.claude/` и `.kilo/`), `CLAUDE.md` и строки
`Branch:` в `tasks.md` моих change'ей. `retarget-mvp-domain` (его ведёшь ты; в строке 7 его
`tasks.md` ещё стоит `feature/<task>/<zone>`) и твои change'и я не трогал.

Эти общие файлы изменены до твоего подтверждения, по моему решению. Если ты против
какой-то части, ответь в файле, названном ниже, и я откачу эту часть.

## Что Аким просит у Егора

1. Подтвердить оба правила и для твоих зон (data, ml, infra): в отслеживаемом файле или
   коммитом, который называет эту записку.
2. Подтвердить, что твои две открытые ветки, `feature/normative-collector/data` и
   `feature/normative-parser/ml`, подчиняются правилу 2 как есть: каждая вливается в
   `develop`, когда её feature целая. Код `normatives-formula-contract` лежит в ветке
   парсера; скажи, это отдельная feature-ветка или часть ветки парсера.
3. Поправить строку 7 в `retarget-mvp-domain/tasks.md` (`feature/<task>/<zone>`), раз ты
   ведёшь этот change. В той же правке заодно убрать формулировку про «short-lived
   sub-branch» (она уже в твоём списке по ревью WP1).
4. Учесть шаг с pull: документы теперь попадают в `develop` без merge из подветки, поэтому
   перед коммитом документа выполняй `git pull --ff-only` в `develop`.

Больше ничего сейчас не нужно. Удаление старых веток `Specs` и `Specs-onboarding` на
`origin` — отдельный вопрос, эта записка его не решает.

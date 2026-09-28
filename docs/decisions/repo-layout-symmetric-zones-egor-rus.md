# Структура репозитория: отдельный каталог проекта на каждую зону (предложение Егору)

- Дата: 2026-09-28
- От: Аким. Кому: Егор.
- Просмотрено: `origin/feature/normative-parser/ml` (коммит `a28cf0a`), в `develop` ещё не
  влито: `pyproject.toml`, `src/normatives_pipeline/`, `configs/`, `infra/`, `research/`,
  `tests/`, `README.md`.

English version: `repo-layout-symmetric-zones-egor.md`.

## Что изменилось в твоей ветке

Пайплайн переехал на src-layout со своим корневым проектом: `pyproject.toml` (проект
`normatives-pipeline`, фиксированные версии зависимостей, `[project.optional-dependencies]
ml`), `src/normatives_pipeline/{parser,formulas}/`, `configs/{parser,formulas}.toml`,
`infra/docker-compose.yml`, `research/` и корневой `tests/`. Старого пакета
`normatives_pipeline/ocr/` больше нет, OCR-обогащение теперь в
`src/normatives_pipeline/formulas/formula_ocr.py`. Src-layout, отделение extra `ml` от
основных зависимостей и `infra/` под compose — всё это разумно, к самому коду у меня
претензий нет.

## Почему я прошу поменять

Раскладка кладёт манифест, корень исходников и корень тестов твоего проекта в корень
репозитория, рядом с `backend/` и `frontend/` в их собственных каталогах. Это создаёт три
проблемы для зон, которые `AGENTS.md` держит неперекрывающимися:

1. **Один общий `.venv`, два набора версий.** `backend/requirements.txt` будет нести
   NumPy/SciPy для движка расчётов. Твой корневой `pyproject.toml` фиксирует
   `numpy==2.5.3`, `scikit-learn==1.9.1`, `psycopg2-binary==2.9.13` и extra `ml` с
   `doclayout-yolo`, `pix2text`. Установленные в одно окружение, эти два набора могут
   разойтись или начать конфликтовать; установка твоего extra `[ml]` также затянет
   ML-зависимости в окружение backend, где их не должно быть вовсе
   (`agent-docs/domain-constraints.md`: «No ML in the calculation path»).
2. **Корневой `tests/` читается как набор тестов всего репозитория, а на деле это только
   тесты пайплайна.** Не остаётся места для тестов, пересекающих зоны (будущая
   интеграционная проверка движок-пайплайн).
3. **Границу импортов backend/frontend не с чем сверять.** Задача 5.1 WP6 планирует
   `import-linter` внутри `backend/`, но ничто не мешает `backend/` импортировать
   `normatives_pipeline` из корня так же, как любой другой пакет верхнего уровня.

В «Repository layout» из `README.md` тоже ещё нет `backend/` и `frontend/`, и там всё ещё
написано «task sub-branches» (старая модель веток, см.
`docs/decisions/branching-model-update-egor.md`).

## Предложение (вариант B)

Перенести твой проект в отдельный каталог `normatives/`, чтобы код каждой зоны лежал в
симметричном каталоге проекта со своим манифестом:

```
backend/        app/, alembic/, params/, tests/, pyproject.toml, requirements*.txt, check.sh
frontend/       src/, e2e/, package.json, check.sh
normatives/     pyproject.toml, src/normatives_pipeline/, configs/, tests/, research/
infra/          docker-compose.yml
tests/          только сквозные тесты между зонами (пока пусто)
```

В корне остаётся только по-настоящему общее: `.pre-commit-config.yaml`,
`.editorconfig`, `AGENTS.md`, `CLAUDE.md`, `openspec/`, `docs/`, `agent-docs/`, `infra/`.

Это твой проект и твой корневой `pyproject.toml` (`AGENTS.md`, «Do not change without
agreement» называет его общим со мной), так что перенос и его точная форма — твоё
решение. Я прошу только, чтобы у пайплайна был свой каталог и своё venv, отдельные от
`backend/`.

## Что Аким просит у Егора

1. Согласиться на вариант B (перенести `normatives_pipeline` в `normatives/` со своим
   `pyproject.toml`) или предложить свой вариант, при условии что он сохраняет отдельный
   манифест и отдельное venv от `backend/`.
2. Если согласен — сказать, когда: до слияния этой ветки в `develop` (дешевле всего, пока
   на эти пути никто не завязан) или потом, отдельной доработкой.
3. Обновить «Repository layout» и команды установки в `README.md` под новые пути, убрать
   строку про «task sub-branches» по записке о модели веток.
4. Подтвердить, что корневой `tests/` (или `normatives/tests/` в варианте B) остаётся
   твоим; я туда файлы добавлять не буду.

Здесь не спрашивается ничего про `ml-model-storage` или infra-change — оба ещё твои и ещё
не созданы.

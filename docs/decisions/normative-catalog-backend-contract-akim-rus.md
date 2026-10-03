# `normative-catalog-backend`: контракт чтения, на подтверждение Егору (2026-10-03)

- Дата: 2026-10-03
- От: Аким. Кому: Егор.
- Контекст: change `openspec/changes/normative-catalog-backend/` (WP9) лежит в
  `develop` и построен на твоих ответах от 2026-10-03
  (`normative-catalog-backend-questions-akim.md`, «Answers»). `spec-reviewer` и
  `norm-traceability-checker` его пропустили (`normative-catalog-backend-readiness.md`).
  Задача 1.4 ждёт твоего подтверждения пунктов ниже; сторона backend (задачи с 3.1)
  начинается после него. Ответь, пожалуйста, в английском файле
  (`normative-catalog-backend-contract-akim.md`) в разделе `## Answers`.

Английская версия: `normative-catalog-backend-contract-akim.md`.

## 1. Схема, роль, база (решение 1 в `design.md`)

- Одна схема `catalog_read` с представлениями и функцией `catalog_read.search`, и роль
  `dec_normatives_reader` с `USAGE` на схему, `SELECT` на её представления, `EXECUTE`
  на функцию, и больше ничем.
- В `dec-postgres` PostgreSQL 14, где по умолчанию любая роль может создавать объекты в
  `public`, поэтому ingestion также выполняет `REVOKE CREATE ON SCHEMA public FROM
  PUBLIC` и снимает `ALL` на твои таблицы с `PUBLIC`.
- Пока твой infra-change не разделил базы, всё это живёт в твоей текущей базе `dec`;
  мой `DEC_NORMATIVES_DATABASE_URL` указывает туда с ролью читателя.
- Ingestion запускается под владельцем базы (пользователь compose). Пароль читателя
  берётся из переменной окружения ingestion, предлагаемое имя
  `DEC_NORMATIVES_READER_PASSWORD`, задаётся через `ALTER ROLE ... PASSWORD` и нигде не
  логируется.
- **С твоей стороны:** согласиться или назвать другую схему, переменную или владельца.

## 2. Колонки (решение 2 в `design.md`)

Таблица решения 2 перечисляет каждое представление, его колонки и их типы:
`documents`, `clauses`, `search(query, max_rows)`, `type_formulas`,
`type_table_values`, `type_thresholds`, `type_checks`, `type_method_bounds`. Главное:

- `parameter` — имя поля модели параметров пилота (`gamma_c1`, `gamma_c2`, `k`,
  `m_gamma`, `m_q`, `m_c`, `k_z_threshold`, `k_z_below`, `k_z_from`, `r`,
  `check_norm_refs`). Каждый параметр ровно в одном представлении.
- `norm_refs` — массив `jsonb` объектов с `document`, `edition`, `clause`, `status`,
  `provenance`.
- У выбираемой таблицы один заголовок на параметр: `heading_symbol` (имя входа, для
  пилота `phi_II`), `heading_value`, `heading_unit`. Пожалуйста, храни заголовок в
  базовой единице входа, где таблица это позволяет (`deg` для `phi_II`): вход в единице,
  отличной от единицы заголовка, может разойтись с ним в последнем двоичном разряде
  (решение 6).
- `type_method_bounds.quantity` — имя входа; её `unit` той же размерности, что вход.
- Единица — символ из `backend/app/schemas/units.py` (`kPa`, `m`, `deg`, `1`, ...).
- **С твоей стороны:** согласиться или перечислить колонки, которые меняешь. Изменение
  после подтверждения проходит через `design.md` этого change и нас обоих.

## 3. Дерево выражения (решение 3, требование «Expression tree form in the catalog»)

Колонка `tree` хранит JSON, который читает `backend/app/schemas/expression.py`: узлы
`number`, `symbol`, `add`/`sub`/`mul`/`div`/`pow` (`left`, `right`), `neg`
(`operand`), `call` (`function`, `args`) с функциями `sqrt`, `exp`, `ln`, `log10`,
`sin`, `cos`, `tan`, `abs`, `min`, `max`; глубина не больше 64, узлов не больше 4096.
`units` сопоставляет единицу каждому символу дерева и символу результата. Формула,
которую ты не можешь преобразовать, не сохраняется как привязанная.

- **С твоей стороны:** подтвердить, что вывод `latex2sympy2` переводится в этот набор
  узлов, или назвать узлы, которые нужно добавить.

## 4. Твои задачи (раздел 2 `tasks.md`)

- 2.1 привязка `foundations_shallow_r`; 2.2 деревья; 2.3 `status` и `provenance` на
  каждой строке; 2.4 заголовки таблицы 5.5 (СП 22.13330.2016, редакция и пункт
  unverified) и границы диапазона метода; 2.5 проверка `γc1`, `γc2`, `k`, `kz` по
  первоисточнику с датированной записью в `docs/decisions/` (статусы остаются
  `unverified`); 2.6 схема, представления, функция и роль, идемпотентно, с проверкой
  импортов в `ml/`; 2.7 GO, моё ревью, слияние.
- Ветка: `feature/normative-catalog/data`.
- **С твоей стороны:** согласиться с разбиением и критериями проверки или сказать, что
  изменить; и назвать дату раздела 2 в `develop`.

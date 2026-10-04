# `.secrets.baseline`: какие файлы зоны Егора в нём перечислены (2026-10-04)

- Дата: 2026-10-04
- От: Аким. Кому: Егор. К сведению, ответа не требуется.
- Контекст: задача 4.5 `bootstrap-dev-environment` (WP6). После твоего переноса
  2026-10-03 (`ml/`, `infra/`) baseline называл пять несуществующих файлов и не покрывал
  файлы бэкенда, слитые после задачи 4.2, поэтому `pre-commit run --all-files` падал на
  `develop`. Я пересобрал его на `feature/dev-environment/backend` командой задачи 4.2
  (`detect-secrets scan --exclude-files 'package-lock\.json'`, только файлы под git;
  коммит `9dca91e`) и вручную проверил каждую находку. В `develop` он попадёт со слиянием этой фичи.
  Baseline — файл Акима; ни один файл твоей зоны не правился.

Английская версия: `secrets-baseline-egor-files.md`.

## Файлы твоей зоны в baseline

Каждая находка прочитана на своей строке; реальных секретов нет.

| Файл | Строка | Находка | Что это |
|---|---|---|---|
| `infra/docker-compose.yml` | 9 | Secret Keyword | `POSTGRES_PASSWORD: dec`, локальный пароль разработки `dec-postgres` |
| `ml/tests/conftest.py` | 8 | Basic Auth Credentials | `DEC_DATABASE_URL` по умолчанию с тем же локальным `dec:dec` |
| `ml/research/research.ipynb` | 106, 291, 292, 322, 323, 353, 354 | Base64 High Entropy String | картинки PNG и JPEG в выводе ячеек |
| `README.md` | 46 | Basic Auth Credentials | твой пример `export DEC_DATABASE_URL=...` с `dec:dec` |
| `docs/decisions/normatives-postgres-storage.md` и `-rus.md` | 22 | Basic Auth Credentials | DSN с `dec:dec` |
| `docs/decisions/repo-reorganization-src-layout.md` и `-rus.md` | 37 | Basic Auth Credentials | пример `export DEC_DATABASE_URL=...` |
| `docs/decisions/normatives-formula-contract-review-egor.md` и `-rus.md` | 128 | Basic Auth Credentials | DSN по умолчанию из `db.py` |
| `skills-lock.json` | 8 | Hex High Entropy String | `computedHash` навыка |

## Что это значит для тебя

- Хук пропускает ровно эти значения ровно в этих файлах. Новый пароль, ключ или
  картинка в другом файле твоей зоны или в новой строке роняют `pre-commit`, пока
  baseline не пересоберут и находку не проверят.
- Если ты перенесёшь или переименуешь один из этих файлов, `pre-commit run --all-files`
  снова упадёт на нём. Кто увидит падение, тот повторяет скан задачи 4.5 и проверяет
  находки (`tasks.md` `bootstrap-dev-environment`, «Dependencies»); скажи, если
  удобнее, чтобы это делал я.
- Хук работает только там, где выполнен `pre-commit install` (задача WP6 6.2 записывает
  это как разовый шаг на каждой машине).

# `.secrets.baseline`: the files of Egor's zone it lists (2026-10-04)

- Date: 2026-10-04
- From: Akim. To: Egor. For information; no answer needed.
- Context: `bootstrap-dev-environment` (WP6) task 4.5. After your move of 2026-10-03
  (`ml/`, `infra/`) the baseline named five files that no longer existed and missed the
  backend files merged after task 4.2, so `pre-commit run --all-files` failed on
  `develop`. I regenerated it on `feature/dev-environment/backend` with the command of
  task 4.2 (`detect-secrets scan --exclude-files 'package-lock\.json'`, git-tracked files
  only; commit `9dca91e`) and reviewed every finding by hand. It reaches `develop` when
  that feature is merged. The baseline is Akim's file; no file of your zone was edited.

Russian version: `secrets-baseline-egor-files-rus.md`.

## Files of your zone in the baseline

Each finding was read on its line; none is a real secret.

| File | Line | Finding | What it is |
|---|---|---|---|
| `infra/docker-compose.yml` | 9 | Secret Keyword | `POSTGRES_PASSWORD: dec`, the local development password of `dec-postgres` |
| `ml/tests/conftest.py` | 8 | Basic Auth Credentials | the default `DEC_DATABASE_URL` with the same local `dec:dec` |
| `ml/research/research.ipynb` | 106, 291, 292, 322, 323, 353, 354 | Base64 High Entropy String | PNG and JPEG images in cell outputs |
| `README.md` | 46 | Basic Auth Credentials | your `export DEC_DATABASE_URL=...` example with `dec:dec` |
| `docs/decisions/normatives-postgres-storage.md` and `-rus.md` | 22 | Basic Auth Credentials | the DSN with `dec:dec` |
| `docs/decisions/repo-reorganization-src-layout.md` and `-rus.md` | 37 | Basic Auth Credentials | the `export DEC_DATABASE_URL=...` example |
| `docs/decisions/normatives-formula-contract-review-egor.md` and `-rus.md` | 128 | Basic Auth Credentials | the fallback DSN of `db.py` |
| `skills-lock.json` | 8 | Hex High Entropy String | a `computedHash` of a skill |

## What this means for you

- The hook allows exactly these values in exactly these files. A new password, key or
  image in another file of your zone, or in a new line, fails `pre-commit` until the
  baseline is regenerated and the finding reviewed.
- If you move or rename one of these files, `pre-commit run --all-files` fails on it
  again. Whoever sees that failure re-runs the scan of task 4.5 and reviews the findings
  (`bootstrap-dev-environment` `tasks.md`, "Dependencies"); tell me if you would rather
  I do it.
- The hook runs only where `pre-commit install` was done (WP6 task 6.2 records it as a
  one-time step per machine).

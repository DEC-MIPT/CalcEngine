# DEC — Design Engineer's Calculator

Cloud web service for automating engineering calculations with a verified normative
base (SP/GOST/SNiP), a transparent ("white box") calculation engine, and GOST-compliant
report generation.

## Stack

- Backend: Python 3.12, FastAPI, Pydantic
- Calculation engine: Python (NumPy/SciPy), hot-swappable to C/C++ later
- Database: PostgreSQL (transactional `dec_app` + normative `dec_normatives`)
- Frontend: React + TypeScript, MathJax
- Reports: python-docx (MVP), reportlab (later)
- Infra: Docker locally, Russian cloud later

## Development

Spec-Driven Development via OpenSpec. See `AGENTS.md` for the operating manual,
`openspec/` for specs and changes. Planning happens on the `Specs` branch; development
on `develop`; `main` is frozen until the MVP.

# crossfit-business-copilot

MVP Business Intelligence Copilot for CrossFit box owners. Answers five
business questions in natural language (Spanish) over a simulated dataset
shaped after the AimHarder Public API. Uses **simulated data only** — no
real AimHarder API access, no real credentials, no write operations.

See `docs/` for the full project record (brief, user stories, API
discovery, acceptance criteria, architecture, handoff, acceptance
evaluation).

## Requirements

- Python 3.11+
- No runtime third-party dependencies. `pytest` is only needed to run the
  automated tests.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install pytest               # only needed to run the test suite
```

The simulated dataset is already committed under `data/*.json` — you do not
need to regenerate it to run the MVP. If you want to regenerate it (it is
fully deterministic, so the output will be identical):

```bash
python3 scripts/generate_dataset.py
```

## Running the copilot

Interactive mode:

```bash
PYTHONPATH=src python3 -m copilot.cli
```

Single-question mode:

```bash
PYTHONPATH=src python3 -m copilot.cli "¿Cuál fue la ocupación media de este mes?"
```

Example questions (Spanish; see `docs/02_User_Stories.md` for the full set):

- `¿Cuál fue la ocupación media de este mes?`
- `¿Qué tres clases tuvieron menor ocupación este mes?`
- `¿Qué horario tuvo más cancelaciones este mes?`
- `¿Qué usuarios llevan más de 21 días sin asistir?`
- `Compara la ocupación de este mes con la del mes anterior.`

## Running the tests

```bash
PYTHONPATH=src pytest
# or, if you created the venv above:
.venv/bin/pytest
```

`pyproject.toml` already sets `pythonpath = ["src"]` for pytest, so
`pytest` alone (from a virtualenv with pytest installed) also works without
setting `PYTHONPATH` manually.

## Project structure

```
data/                  Simulated, reproducible dataset (committed JSON)
scripts/                generate_dataset.py — deterministic dataset generator
src/copilot/            application source
  domain.py              business entities
  datasource/            DataSource port + InMemoryDataSource + MockDataSource
  metrics.py              deterministic business-metrics engine
  periods.py               period resolution (this month, last month, ...)
  nlp.py                    deterministic natural-language question router
  formatter.py               renders an analytical answer as text
  cli.py                      interactive / single-question entry point
tests/                  automated tests (pytest)
docs/                   project record: brief, user stories, API discovery,
                         acceptance criteria, architecture, handoff,
                         acceptance evaluation
```

## Status

MVP complete: all five business questions are implemented, deterministic,
automatically tested, and explain their own metric/period/data/exclusions/
assumptions/limitations on every answer. See
`docs/07_Acceptance_Evaluation.md` for the criterion-by-criterion
evaluation and `docs/06_Handoff.md` for the technical handoff.

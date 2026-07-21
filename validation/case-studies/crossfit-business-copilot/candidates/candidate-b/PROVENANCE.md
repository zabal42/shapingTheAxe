# Provenance — candidate-b

Extraído del laboratorio CrossFit Business Copilot (repo git congelado).

## git log --oneline
```text
67d8363 feat: complete CrossFit business copilot candidate B
0ddebd3 test: freeze shared experiment input
2755aa9 test: define candidate experiment protocol
7183a8e test: add shared experiment input
8e506dd test: add shared experiment input
03341ed docs: add API discovery framework
c500110 docs: define project brief and user stories
7402dce Initial commit
```

## Tags
```text
candidate-a-final
candidate-b-final
crossfit-lab-v0.1
```

## HEAD
```text
commit 67d836336e16259c0e7746ba41c583d2ec3a1a61
Author: Zabal [Mac] <mzabalm@gmail.com>
Date:   Mon Jul 20 10:42:47 2026 +0200

    feat: complete CrossFit business copilot candidate B

 .gitignore                         |     5 +
 README.md                          |    94 +-
 data/bookings.json                 | 72236 +++++++++++++++++++++++++++++++++++
 data/clients.json                  |   282 +
 data/sessions.json                 |  8597 +++++
 docs/03_API_Discovery.md           |   217 +-
 docs/05_Architecture.md            |   155 +
 docs/06_Handoff.md                 |   163 +
 docs/07_Acceptance_Evaluation.md   |    65 +
 pyproject.toml                     |    16 +
 scripts/generate_dataset.py        |   242 +
 src/copilot/__init__.py            |     0
 src/copilot/cli.py                 |   109 +
 src/copilot/datasource/__init__.py |     5 +
 src/copilot/datasource/base.py     |    37 +
 src/copilot/datasource/memory.py   |    65 +
 src/copilot/datasource/mock.py     |    86 +
 src/copilot/domain.py              |    62 +
 src/copilot/formatter.py           |    92 +
 src/copilot/metrics.py             |   284 +
 src/copilot/nlp.py                 |   256 +
 src/copilot/periods.py             |    49 +
 tests/conftest.py                  |   121 +
 tests/test_cli.py                  |    53 +
```

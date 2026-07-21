# Provenance — candidate-a

Extraído del laboratorio CrossFit Business Copilot (repo git congelado).

## git log --oneline
```text
0afd586 feat: complete CrossFit business copilot candidate A
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
commit 0afd58643629a007b9460d98f99e68dc84c0f78e
Author: Zabal [Mac] <mzabalm@gmail.com>
Date:   Mon Jul 20 08:29:33 2026 +0200

    feat: complete CrossFit business copilot candidate A

 README.md                         | 171 ++++++++++-
 data/simulated-box.json           | 629 ++++++++++++++++++++++++++++++++++++++
 docs/03_API_Discovery.md          | 274 ++++++++++-------
 docs/05_ARCHITECTURE_AND_DATA.md  | 149 +++++++++
 docs/06_ACCEPTANCE_EVALUATION.md  |  60 ++++
 docs/run/CHECKPOINT.md            |  94 ++++++
 docs/run/COMPLETION_REPORT.md     | 174 +++++++++++
 docs/run/CONTEXT_BRIEF.md         | 106 +++++++
 docs/run/HANDOFF_PROCEDURE.md     | 117 +++++++
 docs/run/IMPLEMENTATION_PLAN.md   | 155 ++++++++++
 package.json                      |  16 +
 scripts/generate-dataset.js       | 134 ++++++++
 src/application/copilot.js        |  37 +++
 src/cli.js                        |  58 ++++
 src/data/data-source.js           |  23 ++
 src/data/json-data-source.js      | 119 ++++++++
 src/domain/dates.js               |  54 ++++
 src/metrics/analytics.js          | 321 +++++++++++++++++++
 src/parser/question-parser.js     | 161 ++++++++++
 src/presenter/answer-presenter.js | 116 +++++++
 test/acceptance.test.js           |  59 ++++
 test/data-source.test.js          |  36 +++
 test/metrics.test.js              | 125 ++++++++
 test/parser.test.js               |  77 +++++
```

# CrossFit Business Copilot

Primer caso de validación comparativa ejecutado con ShapingTheAxe.

## Objetivo

Comprobar si dos implementaciones independientes desarrolladas bajo el mismo protocolo podían compararse de forma reproducible mediante evaluación ciega.

## Resultado

PASS.

Tres evaluadores independientes convergieron en el mismo ranking.

El laboratorio permanece congelado.

## Evidencia

La evidencia primaria reside en este directorio:

- [`LAB_SUMMARY.md`](LAB_SUMMARY.md) — objetivo, método y resultado del laboratorio.
- [`docs/`](docs/) — input compartido del proyecto (brief, historias de usuario, descubrimiento de API, criterios de aceptación).
- [`protocol/`](protocol/) — protocolo de experimento, prompt del evaluador y rúbrica.
- [`candidates/`](candidates/) — código fuente de ambos candidatos, con su procedencia git preservada.
- [`evidence/`](evidence/) — los tres informes de evaluación ciega, la evidencia adversarial de los evaluadores y la meta-evaluación.
- [`EVIDENCE_MANIFEST.md`](EVIDENCE_MANIFEST.md) — integridad verificable (SHA-256) de toda la evidencia.
- [`LESSONS_LEARNED.md`](LESSONS_LEARNED.md) — mejoras candidatas para ShapingTheAxe derivadas del laboratorio.

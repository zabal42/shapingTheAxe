# Evaluación de criterios de aceptación

**Fecha de evaluación:** 2026-07-20  
**Objeto:** working tree derivado de `0ddebd332e7852b05b5559cea408a0ac03453eb4`  
**Comando automatizado:** `npm test`  
**Primera ejecución registrada:** 23 pruebas, 23 pass, 0 fail.
**Ejecución final tras revisión:** 28 pruebas, 28 pass, 0 fail; batería de aceptación 5/5.

La tabla distingue implementación de evidencia ejecutada. La verificación final
y sus hashes se conservan en `docs/run/COMPLETION_REPORT.md`.

| Criterio | Implementación | Evidencia | Estado |
|---|---|---|---|
| AC-01 Supported Business Questions | Parser, `Copilot` y cinco operaciones | `test/acceptance.test.js`: recorre las cinco preguntas | `PASS` |
| AC-02 Deterministic Metrics | Funciones puras en `src/metrics/analytics.js`; sin LLM | Resultados exactos y repetidos en `test/metrics.test.js` | `PASS` |
| AC-03 Explainable Results | Resultado estructurado y presentador con seis secciones | Test de presencia para cada respuesta analítica | `PASS` |
| AC-04 Architecture | Puerto `DataSource`; métricas sin imports del adaptador | Mismas respuestas con JSON y fuente en memoria | `PASS` |
| AC-05 No Undocumented Assumptions | Descubrimiento, mapping y reglas separan documentación de decisiones | `docs/03_API_Discovery.md` y arquitectura | `PASS` |
| AC-06 MVP Scope | Solo lectura local, cinco métricas, sin integraciones/acciones | Inspección de estructura y ausencia de dependencias HTTP | `PASS` |
| AC-07 Reproducibility | Node >=20, generador, dataset, scripts e instrucciones | `npm run generate:data`, `npm test`, comandos README | `PASS` |
| AC-08 Technical Handoff | README, arquitectura, API discovery, run records y limitaciones | Documentos navegables sin conversación | `PASS` |
| AC-09 Testability | Tests de métricas, parser, datos, aplicación y CLI | `node --test` | `PASS` |
| AC-10 Product Value | CLI one-shot/interactiva con preguntas naturales y respuestas explicadas | Subproceso CLI comprueba el ranking de cancelaciones | `PASS` |

## Cobertura funcional observable

| Pregunta | Evidencia exacta del fixture |
|---|---|
| Ocupación media | Junio: 63,33%, 6 sesiones válidas |
| Menor ocupación | Halterofilia 19:00: 37,5%, 2 sesiones |
| Mayor cancelación | 19:00: 4/7, 57,14% |
| Inactividad | Tres usuarios activos; uno usa fecha de alta como proxy explícito |
| Comparación | Mayo 65% frente a junio 63,33%; -1,67 pp y -2,56% |

## Evidencia transversal

- Periodos ambiguos y umbrales ausentes solicitan aclaración.
- Rangos de fecha inválidos no llegan al motor.
- Una pregunta sobre fidelidad por entrenador se rechaza indicando definición y
  datos faltantes, sin emitir cifras.
- Las sesiones canceladas y sin capacidad positiva aparecen como exclusiones.
- El dataset rechaza referencias rotas y una fuente marcada como real.
- Una fecha exactamente 21 días antes queda fuera del filtro “más de 21”.
- El adaptador rechaza bookings sin un marcador `cancelledAt` explícito.
- Una sesión cancelada por el box no puede renovar la última asistencia.
- La comparación deriva cambios de valores sin redondear y redondea al final.
- La expresión “último mes” resuelve el mes natural anterior.

## Limitaciones de esta evaluación

- Las pruebas verifican el mock y la arquitectura local, no el comportamiento
  de la API real.
- La prueba de adaptabilidad usa una segunda fuente en memoria, no un adaptador
  HTTP.
- El entorno activo no autoriza delegación a un evaluador independiente. El
  completion report entrega un procedimiento de handoff limpio; no lo presenta
  falsamente como ejecutado por un tercero.
- El rubric disponible en el framework se identifica como `0.2.0-beta.1`,
  mientras la Brain Specification y el kernel gobernantes son
  `0.2.0-beta.2`. La discrepancia se reporta y no se corrige durante este run.

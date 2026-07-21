# Procedimiento de handoff limpio

## Propósito

Permitir que una persona o instancia autorizada, sin acceso a la conversación
de descubrimiento, comprenda, ejecute y evalúe el MVP usando únicamente el
repositorio.

## Identidad y entradas

- Snapshot base: `0ddebd332e7852b05b5559cea408a0ac03453eb4`.
- Framework semántico: ShapingTheAxe Brain Specification y kernel
  `0.2.0-beta.2`.
- Contrato congelado: `experiment/input/` y
  `experiment/protocol/EXPERIMENT_PROTOCOL.md`.
- Implementación y tests: `package.json`, `data/`, `scripts/`, `src/`, `test/`.
- Contexto persistente permitido: `README.md`, `docs/` y `docs/run/`.
- Dataset esperado por identidad, no por resultado analítico:
  `data/simulated-box.json`, SHA-256
  `b691e655e2f41fd1379c11b45b452775a42c1336acae3932ca1a319c4a2973a0`.

## Requisitos del evaluador

- Node.js 20 o posterior.
- Lectura y ejecución local. No necesita red, credenciales ni servicios.
- No debe recibir el chat, un veredicto previo ni una respuesta modelo del
  evaluador original.
- Debe separar defectos del producto, fixture, documentación, framework y
  entorno.

## Correcciones posteriores a la revisión

Una revisión del working tree encontró cuatro defectos, todos corregidos y
cubiertos por una regresión específica:

| Defecto encontrado | Corrección | Regresión |
|---|---|---|
| Un `cancelledAt` ausente podía interpretarse como cancelación | El adaptador exige la propiedad y valida `null` o `YYYY-MM-DDTHH:MM:SS` | `test/data-source.test.js`: booking sin marcador explícito |
| La comparación derivaba cambios de ocupaciones ya redondeadas | Diferencia y variación usan medias crudas; solo la salida se redondea | `test/metrics.test.js`: resultado relativo `-2,56%` |
| Una asistencia aparente en sesión cancelada podía renovar la última asistencia | El conjunto de asistencias válidas excluye sesiones canceladas | `test/metrics.test.js`: sesión cancelada para un usuario inactivo |
| “Último mes”, ejemplo literal del brief, no se reconocía | Se resuelve como mes natural anterior al `asOf` | `test/parser.test.js`: mayo de 2026 |

Antes de las correcciones, la ejecución dirigida produjo 19 pass y 4 fail. Tras
aplicarlas produjo 23/23 en las suites afectadas. La verificación final completa
produjo 28/28 y la batería de aceptación 5/5.

## Prompt limpio

> Evalúa el repositorio como un MVP de Business Intelligence Copilot para un
> box de CrossFit. Usa como contrato los archivos congelados de
> `experiment/input/` y el protocolo experimental. Sin consultar conversaciones
> previas: (1) restablece intención, alcance, restricciones y Definition of
> Done; (2) identifica la arquitectura, las definiciones de negocio y los
> límites de autoridad; (3) ejecuta las verificaciones documentadas; (4)
> comprueba las cinco preguntas y la prudencia ante preguntas ambiguas o no
> soportadas; (5) determina si la fuente de datos puede sustituirse sin cambiar
> las métricas; (6) lista elementos resueltos, controlados, pendientes o
> bloqueantes; y (7) entrega evidencia reproducible y un veredicto razonado. No
> uses red ni credenciales y no atribuyas al API real comportamiento que solo
> aparezca en el mock.

## Pasos de ejecución

1. Registrar `git rev-parse HEAD`, `git status --short`, `node --version` y
   `npm --version`.
2. Leer primero `experiment/input/EXPERIMENT_PROMPT.md` y
   `experiment/input/04_Acceptance_Criteria.md`; después `README.md`,
   `docs/03_API_Discovery.md`, `docs/05_ARCHITECTURE_AND_DATA.md` y los run
   records.
3. Calcular el SHA-256 del dataset, ejecutar `npm run generate:data` y volver a
   calcularlo. Registrar si la identidad converge.
4. Ejecutar `npm test` y `npm run test:acceptance`, conservando conteos y exit
   codes. El snapshot entregado contiene 28 pruebas totales y 5 de aceptación;
   cualquier diferencia debe explicarse, no asumirse.
5. Ejecutar `npm start -- --examples` y cada una de las cinco preguntas del
   README en un proceso nuevo.
6. Ejecutar una pregunta sin periodo, otra sin umbral y la pregunta de fidelidad
   por entrenador. Confirmar que no aparecen cifras analíticas inventadas.
   Ejecutar también “¿Cuál es la ocupación media del último mes?” y comprobar
   que el periodo resultante es 2026-05-01..2026-05-31.
7. Inspeccionar imports y la prueba de fuente en memoria para confirmar que el
   motor no depende del adaptador JSON.
8. Comparar por hash los duplicados de inputs congelados bajo `docs/` y
   `experiment/input/` y comprobar que no fueron alterados.
9. Entregar una tabla AC-01..AC-10 con evidencia observada, limitaciones y
   siguiente acción exacta si existe un fallo.

Adicionalmente, el evaluator debe inspeccionar las cuatro regresiones anteriores
y confirmar que no se limitaron a actualizar expectativas: cada una construye
la condición defectuosa y comprueba el comportamiento corregido.

## Reglas de contaminación

- El evaluator no debe usar este run como autoridad sobre AimHarder; la
  autoridad externa es el PDF suministrado y cualquier comportamiento real
  continúa sin verificar.
- Los resultados esperados escritos en documentación sirven como claims que el
  evaluator debe comprobar, no como evidencia de que ya pasaron.
- Un test que no se ejecuta se marca `NOT_RUN`; una ausencia de datos no se
  interpreta como resultado negativo.
- La discrepancia del rubric beta.1 frente al kernel/spec beta.2 debe conservarse
  y atribuirse al framework, no al producto candidato.

## Validez y evidencia requerida

El handoff es válido si el evaluator puede, usando solo estos archivos:

- explicar intención, contrato, arquitectura, métricas y límites sin una nueva
  decisión material;
- ejecutar el producto y reproducir el dataset;
- localizar evidencia para cada criterio obligatorio;
- continuar con el siguiente paso sin depender de contexto oculto.

Su informe debe incluir comandos, salidas resumidas, exit codes, identidad de
entorno, cambios locales detectados y cualquier riesgo residual. Este archivo
prepara la evaluación independiente; no afirma que un tercero ya la haya
ejecutado.

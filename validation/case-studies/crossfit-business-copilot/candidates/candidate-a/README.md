# CrossFit Business Intelligence Copilot

MVP conversacional y determinista para responder cinco preguntas de negocio de
un box de CrossFit usando exclusivamente datos simulados compatibles con los
conceptos documentados por AimHarder.

## Qué demuestra

El copilot responde:

1. ocupación media durante un periodo;
2. clases y horarios con menor ocupación;
3. horarios con mayor tasa de cancelación;
4. usuarios activos sin asistir durante más de 21 días;
5. comparación de ocupación entre dos periodos.

El parser únicamente selecciona una operación soportada. Todas las cifras se
calculan mediante funciones JavaScript deterministas; no interviene un modelo
de lenguaje en el cálculo.

## Requisitos

- Node.js 20 o posterior.
- No se necesitan dependencias, credenciales, variables de entorno ni acceso a
  red.

Versión verificada durante el desarrollo: Node.js `v24.16.0`.

## Ejecutar

Mostrar preguntas reproducibles:

```bash
npm start -- --examples
```

Hacer una pregunta directamente:

```bash
npm start -- "¿Cuál fue la ocupación media de este mes?"
```

Abrir el modo interactivo:

```bash
npm start
```

La fecha relativa no depende del reloj del equipo. “Este mes” se resuelve
contra `metadata.asOf = 2026-06-30` del dataset, por lo que siempre representa
del 1 al 30 de junio de 2026.

## Preguntas de demostración

```text
¿Cuál fue la ocupación media de este mes?
¿Qué tres clases tuvieron menos ocupación este mes?
¿Qué horario tuvo más cancelaciones este mes?
¿Qué usuarios llevan más de 21 días sin asistir?
Compara la ocupación de este mes con el mes anterior.
```

También se aceptan periodos explícitos:

```bash
npm start -- "Muestra 2 clases con menos ocupación entre 2026-05-01 y 2026-05-31"
```

Cada respuesta analítica incluye resultado, métrica, periodo, datos utilizados,
exclusiones, supuestos y limitaciones. Una pregunta ambigua solicita la
información mínima que falta; una pregunta no soportada explica por qué no hay
evidencia suficiente y no muestra cifras inventadas.

## Pruebas

Ejecutar toda la verificación automatizada:

```bash
npm test
```

Ejecutar solo el recorrido de aceptación:

```bash
npm run test:acceptance
```

Regenerar el dataset de manera determinista:

```bash
npm run generate:data
```

El resultado esperado contiene 8 usuarios anonimizados, 14 sesiones y 47
reservas. El archivo generado es `data/simulated-box.json`.

## Definiciones de negocio

- **Ocupación de sesión:** reservas `confirmed` sin cancelación divididas por la
  capacidad. La media da el mismo peso a cada sesión válida.
- **Baja ocupación:** media anterior agrupada por clase y hora, ordenada de menor
  a mayor.
- **Cancelación:** registros con `cancelledAt` dividido por todos los registros
  de reserva de esa hora de inicio.
- **Inactividad:** días naturales desde la última asistencia de un usuario
  activo. Si nunca asistió, la fecha de alta se usa y se señala como proxy.
- **Comparación:** la misma fórmula de ocupación aplicada a dos periodos, con
  diferencia en puntos porcentuales, variación relativa y advertencias de
  comparabilidad.

Las sesiones canceladas por el box o sin capacidad positiva quedan fuera de la
ocupación y se contabilizan en la explicación.

## Arquitectura

```text
CLI -> parser determinista -> Copilot -> métricas puras
                                  |-> presentador explicable
                                  `-> DataSource <- adaptador JSON simulado
                                                   <- futuro adaptador AimHarder
```

El motor de métricas no importa el adaptador JSON ni conoce endpoints. Cualquier
fuente que entregue el contrato normalizado puede reutilizarlo sin cambios. Las
pruebas de aceptación ejecutan las mismas preguntas con el adaptador JSON y con
una fuente en memoria.

Detalles: [`docs/05_ARCHITECTURE_AND_DATA.md`](docs/05_ARCHITECTURE_AND_DATA.md).

## Estructura del proyecto

```text
data/                         Dataset JSON generado
scripts/generate-dataset.js  Escenario reproducible
src/application/             Orquestación de consultas
src/data/                    Puerto y adaptador JSON
src/domain/                  Operaciones de fechas
src/metrics/                 Cálculos de negocio puros
src/parser/                  Reconocimiento determinista
src/presenter/               Respuestas explicables
src/cli.js                   Interfaz one-shot e interactiva
test/                        Pruebas unitarias y de aceptación
docs/03_API_Discovery.md     Evidencia y límites de AimHarder
docs/run/                    Contexto, plan, checkpoint y cierre
```

## Límites

- No existe conexión con AimHarder ni código de autenticación.
- El dataset contiene una sola sede y no incluye datos reales.
- El parser está deliberadamente limitado a frases equivalentes a las cinco
  preguntas; no es un asistente generativo libre.
- La ocupación mide reservas, mientras la inactividad mide asistencia.
- Festivos, cambios de entrenador, motivos de cancelación y causalidad no se
  infieren.
- La documentación suministrada no ofrece un booking history global ni una
  unión inequívoca entre cada history item y una sesión. Esto debe resolverse
  antes de una integración real.

## Documentación y handoff

- [Descubrimiento AimHarder](docs/03_API_Discovery.md)
- [Arquitectura y datos](docs/05_ARCHITECTURE_AND_DATA.md)
- [Evaluación de aceptación](docs/06_ACCEPTANCE_EVALUATION.md)
- [Context brief](docs/run/CONTEXT_BRIEF.md)
- [Plan aprobado](docs/run/IMPLEMENTATION_PLAN.md)
- [Completion report](docs/run/COMPLETION_REPORT.md)

Los archivos de `experiment/input/` son evidencia congelada y no forman parte
de la implementación mutable.

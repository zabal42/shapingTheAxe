# Arquitectura y datos

## Objetivo arquitectónico

Separar adquisición, interpretación, cálculo y presentación para que:

- un cambio de fuente no reescriba las métricas;
- el lenguaje natural no produzca cifras;
- cada resultado conserve evidencia de cálculo;
- el MVP permanezca pequeño, local y reproducible.

## Componentes

| Componente | Responsabilidad | Prohibición relevante |
|---|---|---|
| `src/cli.js` | Entrada one-shot/interactiva y salida de texto | No calcula métricas |
| `src/parser/question-parser.js` | Reconoce una intención soportada y parámetros | No accede a datos ni inventa periodos |
| `src/application/copilot.js` | Carga el snapshot y despacha la operación | No contiene fórmulas |
| `src/metrics/analytics.js` | Funciones deterministas sobre registros normalizados | No conoce JSON, HTTP ni AimHarder |
| `src/presenter/answer-presenter.js` | Convierte resultados estructurados en explicaciones | No modifica cifras |
| `src/data/data-source.js` | Define el puerto `load()` | No prescribe transporte |
| `src/data/json-data-source.js` | Lee y valida el fixture simulado | No calcula métricas |
| `scripts/generate-dataset.js` | Genera el escenario reproducible | No almacena métricas precalculadas |

## Flujo de una pregunta

```text
pregunta
  -> parseQuestion(question, dataset.metadata.asOf)
  -> intención + periodo/umbral o aclaración/rechazo
  -> función pura del motor analítico
  -> resultado estructurado con seis bloques explicativos
  -> texto en español
```

Una pregunta no soportada termina antes del motor. Una pregunta sin un periodo
o umbral obligatorio solicita aclaración. La aplicación no usa la fecha actual
del proceso.

## Modelo normalizado

### Metadata

| Campo | Propósito |
|---|---|
| `schemaVersion` | Evolución explícita del fixture |
| `boxId`, `boxName` | Identidad de la única sede simulada |
| `timezone` | Semántica local de las fechas |
| `asOf` | Ancla determinista para preguntas relativas |
| `source` | Debe ser literalmente `simulated` |

### User

| Campo | Fuente conceptual AimHarder | Uso |
|---|---|---|
| `id` | client `id` | Unión y salida anonimizada |
| `displayName` | campos de identidad, minimizados | Salida segura del fixture |
| `active` | `/clients` devuelve clientes “de alta” | Filtro de inactividad |
| `createdOn` | `creation_date` | Proxy explícito si nunca asistió |
| `deactivatedOn` | `deactivation_date` | Evidencia del estado inactivo |

### Session

| Campo | Fuente conceptual AimHarder | Uso |
|---|---|---|
| `id` | requisito normalizado; `schedule_id` existe en calendar y booking detail | Unión estable interna |
| `classId`, `className` | class `id`/`name` | Agrupación |
| `date`, `startTime` | calendar y booking history | Periodo/horario |
| `capacity` | calendar `limit` | Denominador de ocupación |
| `cancelled` | calendar cancellation flag | Exclusión |

El `id` de sesión no se atribuye al booking history por cliente: ese payload no
lo documenta. Un futuro adaptador debe demostrar cómo obtener o reconstruir la
unión sin colisiones.

### Booking

| Campo | Fuente conceptual AimHarder | Uso |
|---|---|---|
| `id` | booking RVID | Identidad/deduplicación |
| `userId` | client ID | Inactividad |
| `sessionId` | unión normalizada | Agregación por sesión |
| `state` | `confirmed` / `waiting_list` | Elegibilidad |
| `attended` | booking history `attended` | Última asistencia |
| `bookedAt` | `booking_date` | Trazabilidad del fixture |
| `cancelledAt` | `cancellation_date` | Cancelaciones y exclusión de ocupación |

## Dataset reproducible

El generador declara usuarios y sesiones con listas explícitas de reservas
confirmadas, canceladas y no-shows. Después expande esas listas a registros de
booking. Esto mantiene el escenario legible sin guardar porcentajes o rankings
como entrada.

Snapshot actual:

- `asOf`: 2026-06-30;
- 8 usuarios anonimizados;
- 14 sesiones (12 válidas, una cancelada y una con capacidad cero);
- 47 reservas;
- mayo y junio de 2026 comparables por número y combinación de clases/horas.

Resultados de control calculados a mano y cubiertos por pruebas:

| Métrica | Resultado esperado |
|---|---:|
| Ocupación media mayo | 65% |
| Ocupación media junio | 63,33% |
| Menor ocupación junio | Halterofilia 19:00, 37,5% |
| Mayor cancelación junio | 19:00, 4/7 = 57,14% |
| Inactivos >21 días | Socios 005, 002 y 003 |
| Diferencia junio frente a mayo | -1,67 puntos porcentuales; -2,56% relativo |

## Reglas y bordes

- Los rangos son inclusivos.
- Los umbrales de inactividad son estrictos (`inactiveDays > threshold`); 21
  días exactos no cumplen “más de 21”.
- No se truncan ocupaciones superiores al 100%; se señalarían como limitación.
- Una sesión cancelada o con capacidad no positiva no entra en ocupación.
- Los horarios sin reservas no entran en cancelaciones por carecer de
  denominador.
- Rankings empatados se ordenan por nombre de clase y hora para ser estables.
- La variación relativa no se calcula si el primer periodo vale cero.

## Sustitución por un adaptador AimHarder

Un adaptador futuro implementaría `load()` y normalizaría respuestas HTTP. El
orden mínimo sería:

1. enumerar clientes relevantes con paginación completa;
2. obtener calendario por cada fecha del intervalo;
3. enumerar booking histories, incluyendo la estrategia para clientes
   desactivados;
4. resolver una clave de sesión inequívoca;
5. deduplicar bookings por RVID y reconciliar cancelaciones/cambios;
6. devolver el mismo contrato normalizado y pasar la suite de métricas sin
   modificar `src/metrics/analytics.js`.

Antes de implementarlo hacen falta autorización separada, credenciales seguras
y evidencia real sobre payloads, rate limits, permisos, paginación consistente
y unión booking-sesión. El análisis completo está en `docs/03_API_Discovery.md`.

## Privacidad y seguridad

El fixture usa identificadores y nombres ficticios. El futuro adaptador debe
evitar campos bancarios, de contacto, documentos personales, notas y fotos que
la API expone pero el análisis no necesita. Los tokens nunca deben registrarse.
Este MVP no contiene transporte HTTP ni rutas de escritura.

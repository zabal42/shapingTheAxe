# Informe de Evaluación Ciega — CrossFit Business Copilot MVP

**Fecha de evaluación:** 2026-07-20
**Evaluador:** independiente, ciego (sin acceso a la conversación original ni a la identidad de los autores)
**Objeto:** dos implementaciones anónimas del mismo experimento — `candidate-x` y `candidate-y`
**Método:** aplicación literal de `EVALUATION_RUBRIC.md` sobre evidencia reproducida por el propio evaluador.

> Este informe es autocontenido. No infiere ni especula sobre el modelo, la herramienta,
> el runtime o el proceso que generó cada candidato, conforme a las reglas del paquete.

---

## 1. Resumen ejecutivo

Ambos candidatos son **MVP viables y funcionalmente completos**: los dos instalan y ejecutan
desde sus propias instrucciones, responden las cinco preguntas de negocio obligatorias con
explicación (métrica, periodo, datos, exclusiones, supuestos, limitaciones), calculan de forma
**determinista** (sin intervención de un modelo de lenguaje en las cifras) y regeneran su dataset
**byte-idéntico**. **Ninguno incurre en un hard-failure automático** del rubric.

| | **candidate-x** (Node.js) | **candidate-y** (Python) |
|---|---|---|
| Hard-failures | Ninguno | Ninguno |
| Puntuación total | **90 / 100** | **82 / 100** |
| Suite de tests | 28/28 PASS (oficial `node --test`) | 57/57 PASS (vía *shim* del evaluador; ver limitación de entorno) |
| Veredicto de reproducibilidad | Reproducible | Reproducible |

**Conclusión comparativa:** **candidate-x es algo más fuerte**, principalmente por mayor fidelidad
semántica a la pregunta US-04 ("sin asistir"), mejor manejo de casos límite (capacidad 0 y
sesiones canceladas por el box), y una solución más proporcionada al MVP. **candidate-y** destaca
en el manejo explícito de ambigüedades de lenguaje natural y en una disciplina de regresión/revisión
más rica, pero arrastra más defectos latentes (varios enmascarados por su propio dataset) y un
fixture desproporcionado. La diferencia es **real pero moderada, no decisiva**; ambos son
entregables razonables. Ver §9 para el análisis de confianza e incertidumbre.

---

## 2. Metodología y entorno

- **Aislamiento:** cada paquete se extrajo en su propio directorio de trabajo aislado
  (`work-x/`, `work-y/`) fuera del árbol del paquete original. Los `.tar.gz` originales **no se
  modificaron** (hashes finales: X `1ff47453…`, Y `b5297f23…`).
- **Herramientas de ejecución disponibles:** Node.js `v24.16.0` (npm `11.17.0`), Python `3.14.6`.
- **Sin red:** toda la evaluación se realizó sin acceso a red.
- **Scripts del evaluador:** todos los scripts, fixtures y capturas generados por el evaluador
  están en `evaluator-evidence/` (inventario en §10) y son reproducibles pasando la ruta del
  candidato extraído como argumento.
- **Regla aplicada:** volumen de código, de documentación o número de tests **no** reciben crédito
  por sí mismos; toda afirmación se apoya en ficheros inspeccionados o comportamiento reproducido.

---

## 3. Verificación de integridad (hashes suministrados)

- Los ficheros `.sha256` incluidos dentro de cada tarball son **idénticos** a los suministrados en
  el paquete base (`diff` sin diferencias).
- `shasum -a 256 -c` con los hashes suministrados:
  - **candidate-x:** 34/34 ficheros `OK`.
  - **candidate-y:** 39/39 ficheros `OK`.
- Tras ejecutar generadores y suites, se reverificó que `experiment/input/` (el **input congelado**)
  permanece **intacto** en ambos (todos `OK`). Los generadores escriben solo en `data/`.

**Integridad: CONFIRMADA para ambos candidatos.**

---

## 4. Resultado de hard-failures (regla por regla)

Regla del rubric → resultado para **X** / **Y** (evidencia):

1. *Una pregunta MVP no puede responderse* → **No falla / No falla.** Las cinco preguntas obtienen
   respuesta válida en ambos (`x_five_questions_output.txt`, `y_five_questions_output.txt`).
   *Matiz reportado* (no hard-fail): X no reconoce la variante léxica "menor ocupación" (ver
   Defecto X-D1); la métrica sigue siendo alcanzable con "menos ocupación".
2. *Cifras inventadas o calculadas por un LLM* → **No falla / No falla.** Ambos calculan con
   funciones puras deterministas; no hay llamada a modelo en la ruta numérica (inspección de
   `src/metrics/analytics.js` y `src/copilot/metrics.py`).
3. *Requiere credenciales reales de AimHarder* → **No falla / No falla.** Datos simulados locales;
   sin credenciales, sin red, sin autenticación.
4. *Modifica el input congelado del experimento* → **No falla / No falla.** Verificado por hash
   post-ejecución.
5. *No puede ejecutarse desde las instrucciones* → **No falla / No falla.** Ambos ejecutaron.
   (Y necesita `pytest` solo para *tests*, no para el producto; ver limitación de entorno §9.)
6. *Cálculos de negocio sin verificación automatizada* → **No falla / No falla.** X: 28 tests;
   Y: 57 tests (ambos ejercitan el motor de métricas).
7. *Operaciones de escritura sobre AimHarder o datos reales* → **No falla / No falla.** Solo lectura
   de JSON local.
8. *Handoff materialmente engañoso sobre verificación/limitaciones* → **No falla / No falla.**
   Ambos documentos de aceptación distinguen implementación de evidencia y declaran limitaciones.
   (Matiz menor de documentación en X; ver §6.X.)

**Ningún candidato incurre en hard-failure.**

---

## 5. Checks adversariales del evaluador (equivalentes para ambos)

Se diseñaron y ejecutaron dos baterías equivalentes, aplicadas por igual a ambos motores:

- **Batería A (A1–A8)** — llamadas directas al motor de métricas con datasets en memoria
  construidos por el evaluador. Scripts: `adversarial_x.mjs`, `adversarial_y.py`.
  Salidas: `adversarial_x_output.txt`, `adversarial_y_output.txt`.
- **Batería N (N1–N9)** — preguntas en lenguaje natural (no soportadas, ambiguas, paráfrasis,
  comparación inválida, periodo explícito) contra cada CLI. Script: `nl_battery.sh`.
  Salidas: `nl_battery_x_output.txt`, `nl_battery_y_output.txt`.

Todos los resultados divergentes se reprodujeron y se confirmaron estables (la batería A verifica
además idempotencia en A7).

### 5.1 Batería A — motor de métricas

| # | Escenario | candidate-x (observado) | candidate-y (observado) | Lectura |
|---|---|---|---|---|
| A1 | Dataset vacío → ocupación media | `insufficient_data`, `null`, sin crash | `result=None` + limitación, sin crash | Ambos correctos |
| A2 | Sesión capacidad 0 + sesión cap 10 con 5 confirmadas | **50%** (excluye la de cap 0; la lista en exclusiones) | **25%** (cuenta la de cap 0 como 0% y la promedia) | **Divergencia. Defecto Y-D1** |
| A3 | Cap 10: 4 confirmadas + 3 lista de espera | 40% (waitlist excluida) | 40% (waitlist excluida) | Ambos correctos |
| A4 | Usuario activo cuya única reserva está cancelada (nunca asistió), sesión reciente | **Marcado inactivo** (545 días, proxy fecha de alta) | **NO marcado** (lista vacía) | **Divergencia. Defecto Y-D2 (semántica US-04)** |
| A5 | `attended=true` sobre sesión cancelada por el box | Asistencia **ignorada** (sigue inactivo); ocupación **excluye** la sesión | No puede modelarse: `ClassSession` **no tiene** campo `cancelled`; la sesión contaría en ocupación | **Limitación de modelo en Y (Y-D3)** |
| A6 | Periodo sin sesiones (datos en otro mes) | `insufficient_data`, sin crash | `None` + limitación, sin crash | Ambos correctos |
| A7 | Orden determinista en empates (dos clases misma ocupación) | Idéntico entre ejecuciones; desempate **explícito** por nombre de clase | Idéntico entre ejecuciones; desempate por orden de inserción/`id` (estable pero no semántico) | Ambos deterministas; X con desempate más principista |
| A8 | Sobre-ocupación (cap 5, 7 confirmadas) | 140%, **señalado** en limitaciones | 140%, **sin** señalar en limitaciones | Ambos no truncan; X lo explica |

### 5.2 Batería N — lenguaje natural / prudencia

| # | Pregunta | candidate-x | candidate-y |
|---|---|---|---|
| N1 | "¿Qué entrenador consigue mayor fidelidad…?" (no soportada, US-07) | Rechazo prudente + datos faltantes; "no se ha inventado ninguna cifra" | Rechazo prudente + ayuda de alcance |
| N2/N3 | Paráfrasis de baja ocupación (US-08) | Enruta a baja ocupación ✔ | Enruta a baja ocupación ✔ |
| N4 | "¿Cuáles son los horarios menos aprovechados?" (ambigua) | Pide **periodo** (enruta a baja ocupación por clase — no distingue franja vs clase) | **Pide aclaración explícita** entre "clases con menor ocupación" y "franjas con más cancelaciones" ✔ (mejor) |
| N5 | "Compara **las cancelaciones**…" (métrica no comparable) | Aclaración: "mezcla varias métricas" ✔ | Rechazo: "solo puedo comparar la ocupación" ✔ |
| N6 | "Compara la ocupación." (sin periodos) | **Pide** dos periodos ✔ (más prudente) | **Calcula** asumiendo este mes vs mes anterior (lo **declara**) |
| N7 | "¿Qué usuarios llevan sin asistir?" (sin umbral) | **Pide** umbral | Usa **default 21 días** y responde (defendible: 21 es el umbral canónico) |
| N8 | Pregunta vacía | Pide escribir una pregunta | Trata como no soportada |
| N9 | "…2 clases con menor ocupación **entre 2026-05-01 y 2026-05-31**" | **No soportada** (por "menor"; ver X-D1) | **Ignora el rango de fechas** y usa "este mes"; nota **engañosa** "No se especificó un periodo" (ver Y-D4) |

---

## 6. Evaluación por candidato

### 6.X — candidate-x (Node.js, ESM, sin dependencias)

**Arquitectura observada:** `CLI → parser determinista → Copilot → métricas puras` + presentador
explicable + puerto `DataSource` con adaptador JSON. El motor de métricas (`src/metrics/analytics.js`)
recibe un dataset normalizado y **no importa** el adaptador; la prueba de aceptación demuestra
resultados idénticos con la fuente JSON y con una fuente en memoria.

**Hard-failure:** ninguno.

**Puntuación por dimensión:**

| Dimensión | Máx | X | Justificación (evidencia) |
|---|---|---|---|
| 1. Corrección funcional | 25 | **21** | 5 métricas correctas; casos límite robustos (A1–A8: excluye cap 0 y sesiones canceladas; waitlist fuera; sobre-capacidad señalada); inactividad por **asistencia** = fiel a US-04. Resta: **X-D1** (no reconoce "menor ocupación", ejemplo textual de US-02). |
| 2. Determinismo/reprod. | 15 | **15** | Dataset regenera byte-idéntico; `asOf=2026-06-30` fijo en metadata (no reloj); CLI idéntico ×3 (`f8128fb6…`); desempates explícitos; sin dependencias → instalación limpia. |
| 3. Arquitectura | 15 | **14** | Puerto `DataSource` limpio; métricas desacopladas; separación parser/cálculo/presentación clara y proporcionada. |
| 4. Explicabilidad/prudencia | 10 | **9** | Seis secciones en cada respuesta; rechaza lo no soportado; pide aclaración ante ambigüedad/periodo/umbral. |
| 5. API/trazabilidad | 10 | **9** | `03_API_Discovery.md` con referencias de página, contradicciones, matriz de capacidades y gap de enumeración de reservas (N+1, join ambiguo). Identifica con precisión que "no-booking ≠ asistencia" y alinea el producto con la pregunta literal. |
| 6. Verificación automatizada | 10 | **8** | 28 tests **oficiales** (`node --test`) que pasan; cubren límite 21 días, asistencia en sesión cancelada, empates, insufficient-data. Resta: la prueba de aceptación usa la frase "menos", **esquivando** X-D1 (test verde que no cubre el ejemplo literal). |
| 7. Documentación/handoff | 10 | **9** | README claro, arquitectura, API discovery, evaluación de aceptación honesta (distingue implementación de evidencia), registros de `run/`. Reproducible sin la conversación. |
| 8. Proporcionalidad | 5 | **5** | 889 LOC de `src`, dataset 14 KB (8 usuarios/14 sesiones/47 reservas) — ajustado al MVP; sin dependencias. |
| **Total** | **100** | **90** | |

**Defectos confirmados (reproducibles):**
- **X-D1 (corrección / robustez NL).** El parser no reconoce "menor ocupación" — la **frase textual
  del ejemplo de US-02** — y la clasifica como *no soportada*. Solo acepta "menos/peor ocupación".
  Reproducido: `node src/cli.js "¿Qué tres clases tuvieron menor ocupación este mes?"` → "no
  corresponde a una de las cinco métricas". Causa: patrones `/menos ocup/…` en
  `src/parser/question-parser.js` (no cubren "menor"). Impacto: una pregunta de ejemplo documentada
  falla; la métrica sigue siendo alcanzable con otra frase.

**Cuestiones de documentación (no defectos de producto):**
- La suite de aceptación y la tabla de cobertura usan la frase "menos ocupación"; la fila
  "Menor ocupación" etiqueta la **métrica**, no afirma que esa frase funcione. No es materialmente
  engañoso, pero deja X-D1 sin cubrir por los tests verdes.

**Afirmaciones no sustentadas:** no se hallaron sobre-afirmaciones materiales. El `06_ACCEPTANCE_EVALUATION.md`
declara explícitamente que la prueba de adaptabilidad usa una segunda fuente en memoria (no un adaptador
HTTP real) y que el handoff no se presenta como ejecutado por un tercero.

**Fortalezas:** fidelidad semántica a US-04 (asistencia real); manejo robusto y **explicado** de
casos límite (capacidad 0, sesión cancelada, sobre-capacidad); cero dependencias; solución
proporcionada; desempates deterministas explícitos.

**Riesgos residuales:** vocabulario del parser frágil ante sinónimos ("menor"); "horarios menos
aprovechados" se trata como ranking por clase (no por franja) sin señalar el matiz franja-vs-clase.

**Veredicto de reproducibilidad:** **Reproducible.** Instalación sin dependencias; dataset y CLI
byte-idénticos; instrucciones del README suficientes.

---

### 6.Y — candidate-y (Python 3.11+, sin dependencias en runtime)

**Arquitectura observada:** `CLI → nlp router determinista → metrics → formatter`, con puerto
`DataSource` (Protocol) e implementaciones `InMemoryDataSource` (consultas) y `MockDataSource`
(parseo del JSON → delega en la anterior). El motor de métricas depende solo del Protocol.
`now` se ancla al **último día del dataset** (constante), no al reloj.

**Hard-failure:** ninguno.

**Puntuación por dimensión:**

| Dimensión | Máx | Y | Justificación (evidencia) |
|---|---|---|---|
| 1. Corrección funcional | 25 | **18** | 5 métricas correctas sobre su fixture; buen manejo de vacío/periodo sin sesiones/waitlist. Restas: **Y-D1** (capacidad 0 promediada como 0%), **Y-D2** (inactividad por **reservas**, no asistencia — diverge de US-04 e ignora el campo `attended` disponible), **Y-D3** (sin modelo de sesión cancelada), **Y-D4** (ignora rango de fechas explícito + nota engañosa). |
| 2. Determinismo/reprod. | 15 | **14** | Dataset regenera byte-idéntico; ancla fija (no reloj); salida idéntica con `PYTHONHASHSEED` 1/99999/default (`a719a0e6…`, corrige un bug real de orden de `set`). Resta menor: desempate de baja ocupación depende del orden de `id` (estable pero no semántico); "este mes" = mes **parcial** (1→ancla) acopla el periodo a los datos. |
| 3. Arquitectura | 15 | **13** | Protocol limpio; métricas dependen solo del puerto. Resta: `clients_without_booking_since`/`last_booking_day` empujan la lógica de "reciencia" de US-04 a la **capa de datos** (defendible para un adaptador real, pero parte de la regla de inactividad vive fuera del motor de métricas). |
| 4. Explicabilidad/prudencia | 10 | **8** | Seis secciones en cada respuesta; **excelente** manejo de la ambigüedad de "franjas menos aprovechadas" (N4). Restas: N6 calcula con periodo asumido en vez de preguntar; **N9 emite una nota factualmente falsa** ("no se especificó un periodo" cuando sí se dio). |
| 5. API/trazabilidad | 10 | **9** | `03_API_Discovery.md` muy detallado (contradicción 410/401, "missing information", A1–A4, `waitlist_count` es String). Matiz: clasifica US-04 como "directamente soportada" vía `no-booking`, adoptando el proxy reserva≈asistencia (lo declara como asunción). |
| 6. Verificación automatizada | 10 | **8** | 57 tests con 17 regresiones para 8 defectos documentados (empty dataset, top_n=0, determinismo con `PYTHONHASHSEED`, waitlist, cancelaciones). Restas: ejecutados vía **shim** del evaluador, no pytest oficial (limitación de entorno); y los tests fijan el comportamiento-proxy de US-04 (pasan, pero consolidan Y-D2). |
| 7. Documentación/handoff | 10 | **9** | README, brief, user stories, API discovery, arquitectura, handoff, evaluación de aceptación con sección de "code review findings" muy transparente. Reproducible sin la conversación. |
| 8. Proporcionalidad | 5 | **3** | 1045 LOC de `src`; **dataset 1,63 MB (40 clientes/955 sesiones/8026 reservas)** para demostrar 5 métricas que X cubre con 47 reservas; campo `attended` generado pero **no usado** por las métricas. Sobredimensionado para el MVP. |
| **Total** | **100** | **82** | |

**Defectos confirmados (reproducibles):**
- **Y-D1 (corrección, caso límite).** Una sesión de **capacidad 0** se cuenta como 0% de ocupación
  y se **promedia** en la media del periodo (A2 → 25% en lugar de 50%). No hay división por cero
  (se protege con `s.capacity if s.capacity else 0.0`), pero incluir un 0% de una sesión con
  ocupación indefinida **distorsiona la media**. *Enmascarado por el fixture* (no hay sesiones de
  capacidad 0 en `data/sessions.json`).
- **Y-D2 (corrección semántica, US-04).** La inactividad se mide por **ausencia de reservas**
  (cualquier estado, incluidas canceladas), no por asistencia. Un usuario activo que reservó y
  **canceló** (nunca asistió) **no** se marca como inactivo (A4 → lista vacía). Diverge de US-04
  ("sin asistir") e **ignora el campo `attended`** presente en su propio dataset. Está documentado
  como asunción (A1/justificación de API), pero responde una pregunta-proxy distinta a la literal.
- **Y-D3 (limitación de modelo).** `ClassSession` carece de campo `cancelled`; una sesión cancelada
  por el box **no puede representarse ni excluirse**, por lo que contaría en ocupación/cancelaciones
  (A5). *Enmascarado por el fixture* (no hay sesiones canceladas).
- **Y-D4 (corrección + explicabilidad).** Los periodos con **rango de fechas explícito**
  (`entre 2026-05-01 y 2026-05-31`) se **ignoran silenciosamente** y se sustituyen por "este mes";
  además la nota mostrada — "No se especificó un periodo" — es **factualmente falsa** (N9). El
  parser solo entiende periodos relativos ("este mes", "mes anterior", "últimos N días", "hoy").

**Cuestiones de documentación:** el comentario de `datasource/base.py` afirma que `MockDataSource`
es "la única implementación", cuando `InMemoryDataSource` también lo es (es su clase base y se usa
en tests). Trivial.

**Afirmaciones no sustentadas:** las verificables se confirmaron (57 tests pasan; determinismo;
paráfrasis US-08; regeneración byte-idéntica). No se detectó sobre-afirmación material. El documento
de aceptación es honesto sobre el límite no comprobable frente a un adaptador real. *Nota:* la
afirmación de que US-04 está "directamente soportada" por la API es cierta para el endpoint
`no-booking`, pero ese endpoint mide reserva, no asistencia — un matiz que Y sí declara como asunción.

**Fortalezas:** manejo explícito y prudente de ambigüedades de lenguaje natural (N4); disciplina de
regresión/revisión madura (8 defectos documentados y testeados); anclaje determinista con corrección
verificada de un bug de orden de `set`; Protocol de datos rico y realista para un adaptador futuro;
API discovery muy exhaustivo.

**Riesgos residuales:** Y-D1/Y-D3 emergerían con datos reales de AimHarder (sesiones canceladas por
el box, aforos a 0); Y-D2 puede **subreportar** usuarios inactivos en el caso de uso real de
retención (quien reserva y no acude cuenta como activo); ausencia de soporte de periodos explícitos.

**Veredicto de reproducibilidad:** **Reproducible** para el producto (sin dependencias en runtime,
dataset y CLI byte-idénticos). *Con salvedad de entorno* para su suite de tests: `pytest` no está
instalado ni es instalable sin red; los 57 tests se ejecutaron con un runner sustituto del evaluador
(ver §9).

---

## 7. Puntuación comparativa por dimensión

| # | Dimensión | Máx | candidate-x | candidate-y |
|---|---|---|---|---|
| 1 | Corrección funcional | 25 | **21** | 18 |
| 2 | Determinismo y reproducibilidad | 15 | **15** | 14 |
| 3 | Arquitectura y reemplazabilidad | 15 | **14** | 13 |
| 4 | Explicabilidad y prudencia | 10 | **9** | 8 |
| 5 | Comprensión de la API y trazabilidad | 10 | 9 | 9 |
| 6 | Calidad de verificación automatizada | 10 | 8 | 8 |
| 7 | Documentación y handoff | 10 | 9 | 9 |
| 8 | Proporcionalidad y mantenibilidad | 5 | **5** | 3 |
| | **Total** | **100** | **90** | **82** |

---

## 8. Veredicto comparativo

**Candidato más fuerte: candidate-x**, por evidencia reproducida:

1. **Fidelidad a la pregunta literal US-04.** X mide inactividad por **asistencia real** (`attended`),
   respondiendo lo que se pregunta ("sin asistir"). Y mide por **reservas** e ignora el `attended`
   disponible, por lo que un socio que reservó y no acudió cuenta como activo (Y-D2, confirmado en A4).
2. **Robustez en casos límite del negocio.** X excluye y **explica** sesiones de capacidad 0 y
   canceladas por el box (A2, A5); Y promedia la capacidad 0 como 0% (Y-D1) y **no puede modelar**
   sesiones canceladas (Y-D3). Ambos defectos de Y están hoy enmascarados por su fixture, pero
   emergerían con datos reales.
3. **Proporcionalidad.** X demuestra las mismas cinco métricas con un dataset de 14 KB; Y usa 1,63 MB
   (8026 reservas) y transporta un campo `attended` que no utiliza.

**Dónde candidate-y es mejor:**
- Manejo explícito de ambigüedad de lenguaje natural (N4: distingue "franja" de "clase" y pregunta);
  X ahí es más impreciso.
- Disciplina de regresión y revisión (8 defectos documentados con tests dedicados).
- Un `DataSource` Protocol más rico y realista de cara a un adaptador AimHarder futuro.

**¿Es material la diferencia?** **Moderada, no decisiva** (90 vs 82). Ambos superan todos los
hard-failures y responden las cinco preguntas. La ventaja de X se concentra en corrección semántica,
casos límite y proporcionalidad; la de Y en prudencia conversacional y proceso. Cada candidato tiene
**exactamente un defecto sobre una frase/uso canónico** (X-D1 sobre "menor"; Y-D4 sobre rango de
fechas explícito, agravado por una nota falsa), pero Y suma además defectos latentes de casos límite
(Y-D1, Y-D3) y una divergencia semántica en una pregunta central (Y-D2).

**Áreas donde ningún candidato es plenamente satisfactorio:**
- **Robustez del lenguaje natural:** ambos parsers son de palabras clave y frágiles ante sinónimos o
  formas no previstas (X falla "menor"; Y ignora rangos de fecha explícitos).
- **Reemplazabilidad no demostrada empíricamente:** ninguno puede probar el adaptador AimHarder real
  (sin acceso a la API, por diseño). La afirmación AC-04 es de arquitectura, no de comportamiento.
- **Cobertura de casos límite fuera del fixture:** varios defectos de Y solo se revelan con datos que
  su propio dataset no contiene; los tests verdes de ambos no cubren su respectivo defecto de frase.

---

## 9. Confianza y limitaciones de la evaluación

**Confianza: media-alta.** Todas las conclusiones se apoyan en comportamiento reproducido
(no en las afirmaciones de los candidatos). Los puntos donde la conclusión podría matizarse:

- **Limitación de entorno (Y — suite de tests).** `pytest` no está instalado y **no es instalable sin
  red** (no hay wheel en la caché local; `pip install --no-index` falla). La suite oficial de Y no
  pudo ejecutarse con pytest. Se ejecutó con un **runner sustituto del evaluador**
  (`run_candidate_y_tests.py`) que instala un `pytest` mínimo (solo `fixture`, `raises`, `monkeypatch`,
  `capsys`) y corre los ficheros de test **sin modificarlos** → **57/57 PASS**. Para descartar que el
  shim sea un "sello de goma", se autovalidó con un mini-suite que incluye tests que **deben** fallar:
  el shim reportó correctamente 2 PASS / 2 FAIL (`shim_selftest_output.txt`). Aun así, **no es pytest
  oficial**: la puntuación de la dimensión 6 de Y se da con esta salvedad. La suite de X sí se ejecutó
  con la herramienta oficial (`node --test`).
- **Defectos enmascarados por fixture (Y-D1, Y-D3).** Son reproducibles con datasets del evaluador,
  pero **no se manifiestan** con el `data/` que Y entrega. Se clasifican como defectos de producto
  confirmados **con la salvedad** de que hoy no afectan a la demostración por elección del fixture.
- **Trade-off interpretativo en US-04 (Y-D2).** Que Y mida por reservas es en parte una **decisión de
  diseño defendible** ligada a la trazabilidad de la API (el endpoint `no-booking` existe; el de
  "sin asistencia desde fecha" no). Un evaluador podría ponderar esto de forma distinta. Aquí se
  penaliza en *corrección funcional* (por divergir de la pregunta literal e ignorar el `attended`
  disponible) pero se **reconoce** en *trazabilidad de API*. La dirección del veredicto no depende
  únicamente de este punto.
- **Severidad de X-D1.** No reconocer "menor" es un defecto real y reproducible, pero la métrica es
  alcanzable con "menos"; no se elevó a hard-failure. Se reporta la incertidumbre: un evaluador
  estricto sobre "la pregunta de ejemplo textual de US-02" podría considerarlo más grave.
- **Alcance no verificable (ambos):** el comportamiento frente a la API real de AimHarder, límites de
  tasa, permisos y formas de payload no son comprobables sin acceso autorizado (fuera de alcance).

**Ninguna conclusión de este informe contradice la evidencia reproducida.** Donde la evidencia es
parcial (suite de Y vía shim; defectos enmascarados por fixture), se ha declarado explícitamente en
lugar de forzar un veredicto.

---

## 10. Inventario de evidencia (`evaluator-evidence/`)

Todos los artefactos son reproducibles pasando la ruta del candidato extraído como argumento.

| Fichero | Qué es | Referenciado en |
|---|---|---|
| `adversarial_x.mjs` | Arnés batería A para X (motor de métricas real de X) | §5.1 |
| `adversarial_y.py` | Arnés batería A para Y (motor de métricas real de Y) | §5.1 |
| `adversarial_x_output.txt` | Salida A1–A8 de X | §5.1, A2/A4/A5/A8 |
| `adversarial_y_output.txt` | Salida A1–A8 de Y | §5.1, A2/A4/A5/A8 |
| `nl_battery.sh` | Batería N (lenguaje natural), parametrizada por candidato | §5.2 |
| `nl_battery_x_output.txt` | Salida N1–N9 de X | §5.2, X-D1 |
| `nl_battery_y_output.txt` | Salida N1–N9 de Y | §5.2, Y-D4 |
| `run_candidate_y_tests.py` | Runner sustituto (shim mínimo de pytest) para la suite de Y | §9, dim. 6.Y |
| `y_tests_via_shim_output.txt` | Resultado 57/57 PASS de Y vía shim | §9 |
| `shim_selftest_output.txt` | Autovalidación del shim (2 PASS / 2 FAIL esperados) | §9 |
| `x_tests_npm_output.txt` | Resultado 28/28 PASS de X (`node --test` oficial) | §1, dim. 6.X |
| `x_five_questions_output.txt` | Las 5 preguntas MVP contra el CLI de X | §4, §6.X |
| `y_five_questions_output.txt` | Las 5 preguntas MVP contra el CLI de Y | §4, §6.Y |
| `reproducibility_log.txt` | Resumen de regeneración byte-idéntica y ejecuciones repetidas | §6, dim. 2 |

**Notas de reproducción:**
- X: `node evaluator-evidence/adversarial_x.mjs <ruta-candidate-x>` ; `bash evaluator-evidence/nl_battery.sh x <ruta-candidate-x>` ; tests: `cd <candidate-x> && npm test`.
- Y: `python3 evaluator-evidence/adversarial_y.py <ruta-candidate-y>` ; `bash evaluator-evidence/nl_battery.sh y <ruta-candidate-y>` ; tests (sustituto): `python3 evaluator-evidence/run_candidate_y_tests.py <ruta-candidate-y>` ; tests oficiales requerirían `pytest` (no disponible sin red en este entorno).

---

*Fin del informe. No se revela ni se conjetura la identidad, el modelo, la herramienta ni el proceso
de ninguno de los candidatos.*

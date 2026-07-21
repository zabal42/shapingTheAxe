# Informe de evaluación ciega independiente

**Objeto evaluado:** dos paquetes anónimos, `candidate-x` y `candidate-y`, que implementan el mismo MVP: un Business Intelligence Copilot para boxes de CrossFit.

**Material de evaluación:** `Archivo.zip`, `EVALUATION_RUBRIC.md`, `EVALUATOR_PROMPT.md`, los manifiestos SHA-256 y el contenido de ambos candidatos.

**Fecha de verificación:** 20 de julio de 2026.

## Resumen ejecutivo

Los dos candidatos superan los ocho *hard failures* definidos en la rúbrica y son ejecutables sin credenciales reales de AimHarder. Ambos separan razonablemente el cálculo de métricas del acceso a datos, generan fixtures deterministas y responden las cinco preguntas obligatorias del MVP.

El candidato más fuerte es **candidate-x**, con una puntuación estimada de **92/100**, frente a **79/100** para **candidate-y**. La diferencia de 13 puntos es material y se concentra principalmente en corrección funcional.

La conclusión se apoya especialmente en dos defectos reproducidos directamente en `candidate-y`:

1. Una sesión con capacidad cero se incorpora silenciosamente a la media de ocupación como si tuviera un 0 %, sesgando el resultado sin declararlo como exclusión o limitación.
2. Un rango inequívoco escrito como `2026-05-01` a `2026-05-31` se ignora; el sistema responde sobre julio y afirma incorrectamente que no se especificó ningún periodo.

Los mismos escenarios están correctamente tratados por `candidate-x`. Además, X interpreta la pregunta de usuarios “sin asistir” mediante asistencia real, mientras que Y mide ausencia de reservas.

## 0. Método y alcance

La comprobación se realizó sobre copias temporales de los paquetes, manteniendo intactos los archivos originales. Se llevaron a cabo las siguientes actividades:

- verificación de todos los hashes suministrados;
- comparación de las entradas congeladas del experimento;
- inspección de las instrucciones, arquitectura y código principal;
- ejecución real de las baterías automatizadas;
- regeneración de los datasets y comparación de hashes;
- ejecución directa de los dos casos adversariales determinantes;
- comprobación del tratamiento de rangos de fecha explícitos;
- inspección de la semántica empleada para usuarios inactivos;
- búsqueda de dependencias de red, credenciales y variables secretas en el código de ejecución.

Los scripts adversariales `x_adversarial.mjs` y `y_adversarial.py` citados en el texto de evaluación original **no están incluidos en `Archivo.zip`**. En consecuencia, sus recuentos exactos de 19/19 y 15/15 no pueden auditarse a partir del material entregado. Los defectos centrales sí fueron reproducidos directamente mediante ejecuciones independientes.

## 1. Verificación de integridad

| Paquete | Ficheros del manifiesto | Resultado |
|---|---:|---|
| `candidate-x` | 35 | 35/35 OK |
| `candidate-y` | 40 | 40/40 OK |

Ambos paquetes coinciden byte a byte con sus manifiestos SHA-256.

También se comprobó que los siguientes archivos congelados son idénticos en ambos candidatos:

- `01_Project_Brief.md`;
- `02_User_Stories.md`;
- `04_Acceptance_Criteria.md`;
- `AimHarder_API.pdf`;
- `EXPERIMENT_PROMPT.md`;
- `EXPERIMENT_PROTOCOL.md`.

Por tanto, ninguno de los candidatos modificó la entrada congelada y no se activa el *hard failure* 4.

## 2. Candidate-X

### Resultado de hard failures

**PASS.** No se ha confirmado ninguno de los ocho *hard failures*.

- Las cinco preguntas obligatorias están implementadas.
- Los cálculos de negocio son funciones deterministas, sin intervención de un LLM.
- No necesita credenciales, variables de entorno ni conexión a AimHarder.
- No declara dependencias externas de ejecución.
- Incluye verificación automatizada de las métricas principales.
- Las instrucciones de ejecución funcionan.
- No contiene operaciones de escritura contra AimHarder ni datos empresariales reales.
- El handoff describe de forma sustancialmente correcta las limitaciones del MVP.

### Puntuación

| Dimensión | Puntos | Máximo |
|---|---:|---:|
| 1. Corrección funcional | 24 | 25 |
| 2. Determinismo y reproducibilidad | 15 | 15 |
| 3. Arquitectura y sustituibilidad | 14 | 15 |
| 4. Explicabilidad y prudencia | 9 | 10 |
| 5. Comprensión de la API y trazabilidad | 9 | 10 |
| 6. Calidad de la verificación automatizada | 8 | 10 |
| 7. Documentación y handoff | 9 | 10 |
| 8. Proporcionalidad y mantenibilidad | 4 | 5 |
| **Total** | **92** | **100** |

### Evidencia reproducida

- `npm test` finaliza con **28/28 pruebas superadas**.
- La regeneración mediante `npm run generate:data` conserva exactamente el hash SHA-256 del dataset entregado.
- El dataset regenerado contiene 8 usuarios, 14 sesiones y 47 reservas.
- La referencia temporal procede de `dataset.metadata.asOf = 2026-06-30`; no depende del reloj del sistema.
- La consulta `¿Cuál fue la ocupación media entre 2026-05-01 y 2026-05-31?` respeta el rango literal y devuelve un 65 % para mayo, indicando periodo, datos utilizados, exclusiones, supuestos y limitaciones.
- Las sesiones canceladas por el box se excluyen de la ocupación.
- Las sesiones con capacidad no positiva se excluyen y se contabilizan expresamente en la explicación.
- Las reservas canceladas o en lista de espera no cuentan como ocupación.
- La inactividad se calcula a partir de la última asistencia real, no de la última reserva.

### Defectos confirmados

No se confirmó ningún defecto funcional material en los escenarios reproducidos.

El principal matiz de calidad está en la respuesta genérica a preguntas no soportadas. El mensaje es correcto y prudente, pero resulta escueto en comparación con la explicación especial que ofrece para fidelidad por entrenador.

### Afirmaciones no verificables

La documentación declara una progresión histórica desde 23 hasta 28 pruebas durante el desarrollo. Solo se ha verificado el estado final de 28/28; el historial previo es una afirmación de proceso y no afecta al producto entregado.

El recuento exacto de 19/19 pruebas adversariales mencionado en la evaluación original tampoco puede confirmarse porque el script correspondiente no forma parte del ZIP suministrado.

### Fortalezas

- Motor de métricas puro y desacoplado del adaptador JSON.
- Contrato de fuente de datos reemplazable y probado con fuente JSON y fuente en memoria.
- Validación estricta de referencias, estados, fechas y combinaciones de reserva incompatibles.
- Tratamiento explícito de sesiones canceladas y capacidades no positivas.
- Fidelidad literal a “usuarios sin asistir”, usando asistencia efectiva.
- Soporte de periodos con fechas ISO explícitas.
- Dataset pequeño y proporcional: 14.182 bytes de contenido JSON.
- Documento de descubrimiento de API detallado, con separación entre hechos documentados, contradicciones y supuestos del mock.

### Riesgos residuales

- El parser de lenguaje natural está limitado a patrones previstos y necesitará ampliación manual para nuevas preguntas.
- La futura integración con AimHarder sigue condicionada por la ausencia de un endpoint global de reservas acotado por fecha.
- La documentación de proceso bajo `docs/run/` es extensa para un MVP y aporta menos valor al mantenimiento cotidiano que la documentación de producto.

### Veredicto de reproducibilidad

**Totalmente reproducible.** No requiere dependencias externas, credenciales ni red. Las pruebas pasan, el dataset se regenera byte a byte y las fechas relativas se anclan a metadata fija.

## 3. Candidate-Y

### Resultado de hard failures

**PASS.** No se activa formalmente ninguno de los ocho *hard failures*.

- Implementa las cinco preguntas del MVP.
- Los cálculos son deterministas y no dependen de un LLM.
- No realiza llamadas de red ni requiere credenciales reales.
- Solo utiliza la biblioteca estándar de Python en ejecución; `pytest` es una dependencia exclusiva de pruebas.
- Proporciona una separación clara entre fuente de datos y métricas.
- Las instrucciones de ejecución y test son funcionales en un intérprete compatible.

### Puntuación

| Dimensión | Puntos | Máximo |
|---|---:|---:|
| 1. Corrección funcional | 17 | 25 |
| 2. Determinismo y reproducibilidad | 15 | 15 |
| 3. Arquitectura y sustituibilidad | 13 | 15 |
| 4. Explicabilidad y prudencia | 7 | 10 |
| 5. Comprensión de la API y trazabilidad | 9 | 10 |
| 6. Calidad de la verificación automatizada | 7 | 10 |
| 7. Documentación y handoff | 8 | 10 |
| 8. Proporcionalidad y mantenibilidad | 3 | 5 |
| **Total** | **79** | **100** |

### Evidencia reproducida

- `pytest` finaliza con **57/57 pruebas superadas**.
- `generate_dataset.py` regenera los tres JSON con hashes idénticos a los entregados.
- El dataset contiene 40 clientes, 955 sesiones y 8.026 reservas.
- La fecha ancla es la constante fija `2026-07-20`; no se toma del reloj del sistema.
- La arquitectura utiliza un `DataSource` reemplazable y separa dominio, periodos, routing, métricas y presentación.

### Defectos confirmados

#### 1. Capacidad cero incorporada silenciosamente

Con dos sesiones equivalentes —una con capacidad 0 y otra con ocupación del 100 %— `average_occupancy` devuelve **50,0 %**.

La causa está en `_session_occupancy`: cuando la capacidad es cero, asigna 0,0 a la sesión y posteriormente incluye ese valor en la media. La respuesta solo excluye reservas canceladas y listas de espera; no declara la sesión inválida ni añade una limitación.

Esto sesga la métrica y contradice el requisito AC-03 de explicar los datos excluidos y las limitaciones relevantes.

#### 2. Rango de fechas explícito ignorado

La pregunta:

> ¿Cuál fue la ocupación media entre 2026-05-01 y 2026-05-31?

produce una respuesta sobre `este mes`, interpretado como el 1–20 de julio de 2026, y muestra:

> No se especificó un periodo; asumo 'este mes'.

La afirmación es incorrecta: el periodo sí fue especificado, pero `_extract_periods` no reconoce fechas ISO. El problema no es únicamente de cobertura lingüística; el sistema sustituye silenciosamente la petición por otra y describe de forma falsa lo ocurrido.

#### 3. Modelo de sesión sin cancelación del box

`ClassSession` no incluye un campo de cancelación a nivel de sesión. Por tanto, el mock no puede representar una clase cancelada por el box ni excluir sus reservas de las métricas, aunque la propia documentación del candidato identifica un campo `Calendar.cancelled` en la API real.

#### 4. Inactividad basada en reservas, no en asistencia

La métrica `inactive_users` consulta clientes sin reservas recientes y presenta campos como `ultima_reserva` y `dias_sin_reservar`.

Esta decisión está documentada y justificada por las limitaciones de la API, de modo que no es una invención silenciosa. Sin embargo, responde a una pregunta diferente del literal del MVP, que solicita usuarios “sin asistir”. Un usuario que reserva repetidamente pero nunca asiste no se considera inactivo en Y.

### Cobertura automatizada insuficiente para los defectos encontrados

Las 57 pruebas son valiosas y pasan correctamente, pero no cubren:

- sesiones con capacidad cero;
- rangos explícitos `YYYY-MM-DD` en el router;
- cancelación de una sesión por el box.

Por ello, el número de pruebas no demuestra por sí mismo ausencia de defectos fuera de los escenarios cubiertos.

### Afirmaciones no verificables

La documentación describe una revisión interna de alto esfuerzo, con siete ángulos de búsqueda y defectos corregidos mediante pruebas de regresión. Se ha verificado que esas pruebas existen y pasan, pero no es posible comprobar de forma independiente el esfuerzo o el proceso histórico completo.

El recuento exacto de 15/15 comprobaciones adversariales mencionado en el texto original no es auditable porque `y_adversarial.py` no está incluido en el ZIP.

### Fortalezas

- Documentación transparente sobre decisiones, supuestos y limitaciones.
- Descubrimiento de API muy preciso, especialmente respecto a la ausencia de un endpoint global de reservas acotado por fecha.
- Buena separación entre dominio, fuente de datos, métricas, periodos, parser y presentación.
- Suite amplia con pruebas unitarias, de integración y de CLI.
- Dataset reproducible y suficientemente grande para pruebas de integración.
- Ausencia de dependencias de ejecución, credenciales y llamadas de red.

### Riesgos residuales

- Los dos defectos funcionales principales permanecen en el paquete entregado y no aparecen como limitaciones conocidas en el handoff.
- El parser no reconoce rangos de fechas explícitos.
- El modelo no puede representar sesiones canceladas por el box.
- La semántica de inactividad puede producir falsos negativos respecto a ausencia de asistencia.
- El fixture es grande para las cinco preguntas del MVP: los tres JSON suman **1.649.051 bytes**, aproximadamente **1,57 MiB**, frente a 14.182 bytes en X.

### Veredicto de reproducibilidad

**Reproducible.** Las pruebas pasan y el dataset se regenera exactamente. La ejecución comprobada se realizó con Python 3.14.6, compatible con el requisito declarado `>=3.11`.

La evaluación original mencionaba que solo disponía de Python 3.10.12 y que Y funcionaba pese a declarar 3.11 como mínimo. Esa observación pertenece a aquel entorno y no se reproduce en la verificación actual; no debe presentarse como un defecto intrínseco del candidato.

## 4. Comparación directa

| Aspecto | Candidate-X | Candidate-Y |
|---|---|---|
| Hard failures | PASS | PASS |
| Puntuación | **92/100** | **79/100** |
| Tests reproducidos | 28/28 | 57/57 |
| Capacidad cero | Excluida y explicada | Mezclada como 0 % sin aviso |
| Rango ISO explícito | Respetado | Ignorado y sustituido por el mes actual |
| Inactividad | Última asistencia real | Última reserva |
| Sesión cancelada por el box | Representable y excluida | No representable en el dominio |
| Fecha ancla | Metadata del dataset | Constante/día máximo del dataset |
| Tamaño del fixture | 14.182 bytes | 1.649.051 bytes |
| Arquitectura | Limpia y reemplazable | Limpia y reemplazable |
| Comprensión de la API | Muy buena | Muy buena |

## 5. Veredicto comparativo

**Candidate-x es el candidato más fuerte.**

La diferencia de 13 puntos es material porque no procede principalmente de preferencias estilísticas, volumen documental o cantidad de pruebas. Se concentra en la dimensión de mayor peso —corrección funcional— y está respaldada por comportamientos reproducibles.

Candidate-y está bien estructurado y documenta sus decisiones con honestidad. Sus defectos parecen corregibles sin un rediseño completo, pero afectan directamente a las cifras mostradas al usuario y a la fidelidad con la pregunta planteada. Antes de utilizarlo como base de producto sería necesario, como mínimo:

1. excluir capacidades no positivas y declararlas;
2. reconocer rangos de fecha explícitos o solicitar aclaración sin sustituirlos silenciosamente;
3. representar la cancelación de sesiones por el box;
4. aclarar o adaptar la definición de inactividad para medir asistencia real.

## 6. Áreas donde ninguno es plenamente satisfactorio

### Integración real con AimHarder

La API documentada no ofrece un endpoint global que devuelva todas las reservas acotadas por fecha o franja. Una integración real exigiría un patrón N+1, recorrer históricos por cliente o disponer de otra fuente de sincronización. Ningún candidato resuelve esta limitación, correctamente fuera del alcance del MVP.

### Cobertura de lenguaje natural

Ambos utilizan analizadores deterministas y deliberadamente estrechos. Son apropiados para un MVP acotado, pero cualquier métrica o formulación nueva requerirá ampliar patrones y pruebas manualmente.

### Ambigüedades de la API

La semántica de campos como `cancelled` y `waitlist_count` no queda suficientemente definida en la documentación suministrada. Sin acceso real a la API no es posible resolver empíricamente esas contradicciones.

## 7. Confianza y limitaciones

### Confianza alta

- integridad de hashes;
- identidad de las entradas congeladas;
- resultados de las baterías de 28 y 57 pruebas;
- regeneración determinista de los datasets;
- defecto de capacidad cero en Y;
- defecto de rango explícito en Y;
- diferencia entre asistencia y reserva para medir inactividad;
- tratamiento correcto de los dos primeros casos por X.

### Confianza media

La puntuación exacta por dimensión incorpora juicio cualitativo sobre proporcionalidad, documentación y mantenibilidad. Otros evaluadores podrían variar algunos puntos sin alterar razonablemente el ranking.

### Limitaciones

- Los scripts adversariales citados originalmente no se entregaron, por lo que no pueden confirmarse sus recuentos exactos.
- La batería reproducida para este contraste se centró en los hallazgos determinantes y no constituye una exploración exhaustiva de todas las combinaciones posibles.
- No se utilizaron credenciales ni un entorno real de AimHarder, de acuerdo con el alcance y las prohibiciones de la evaluación.

## 8. Conclusión

Los dos candidatos constituyen implementaciones válidas y reproducibles del MVP, pero **candidate-x ofrece mayor corrección, explicabilidad y fidelidad a las preguntas de negocio**.

La recomendación es seleccionar **candidate-x como base de producto**. Candidate-y conserva valor técnico por su arquitectura, documentación y cultura de pruebas, pero debería someterse a una ronda de corrección antes de considerarse equivalente.

**Resultado final:**

- **Candidate-X: PASS — 92/100**
- **Candidate-Y: PASS — 79/100**
- **Ganador recomendado: Candidate-X**


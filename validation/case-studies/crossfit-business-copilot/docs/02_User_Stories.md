# User Stories

## Contexto

El producto está dirigido inicialmente al propietario o responsable de un box de CrossFit.

El objetivo del MVP es permitir que consulte información relevante de su negocio mediante preguntas escritas en lenguaje natural.

En esta primera versión, el sistema trabajará con datos simulados compatibles con la estructura conceptual de AimHarder.

---

## US-01 — Consultar ocupación media

Como propietario de un box,

quiero conocer la ocupación media de las clases durante un periodo,

para evaluar el nivel general de utilización de la oferta deportiva.

### Ejemplo de pregunta

> ¿Cuál fue la ocupación media de este mes?

### Resultado esperado

El sistema debe mostrar:

- porcentaje medio de ocupación;
- periodo analizado;
- número de sesiones incluidas;
- definición utilizada para calcular la ocupación;
- posibles datos excluidos o limitaciones.

---

## US-02 — Detectar clases con baja ocupación

Como propietario de un box,

quiero identificar las clases con menor ocupación,

para valorar cambios de horario, formato o capacidad.

### Ejemplo de pregunta

> ¿Qué tres clases tuvieron menor ocupación este mes?

### Resultado esperado

El sistema debe mostrar:

- nombre o tipo de clase;
- horario;
- ocupación media;
- sesiones analizadas;
- orden de menor a mayor ocupación.

El sistema no debe recomendar automáticamente eliminar una clase sin aportar suficiente contexto.

---

## US-03 — Analizar cancelaciones

Como propietario de un box,

quiero saber qué horarios concentran más cancelaciones,

para detectar posibles problemas en la programación.

### Ejemplo de pregunta

> ¿Qué horario tuvo más cancelaciones este mes?

### Resultado esperado

El sistema debe mostrar:

- franja horaria;
- número de cancelaciones;
- número total de reservas;
- tasa de cancelación;
- periodo analizado.

---

## US-04 — Detectar usuarios inactivos

Como propietario de un box,

quiero identificar qué usuarios llevan un periodo determinado sin asistir,

para poder realizar acciones de recuperación o seguimiento.

### Ejemplo de pregunta

> ¿Qué usuarios llevan más de 21 días sin asistir?

### Resultado esperado

El sistema debe mostrar:

- identificador o nombre anonimizado del usuario;
- fecha de su última asistencia;
- número de días sin asistir;
- estado del usuario, cuando esté disponible.

Solo deben incluirse usuarios considerados activos según las reglas del negocio.

---

## US-05 — Comparar periodos

Como propietario de un box,

quiero comparar la ocupación entre dos periodos,

para saber si el rendimiento del negocio está mejorando o empeorando.

### Ejemplo de pregunta

> Compara la ocupación de este mes con la del mes anterior.

### Resultado esperado

El sistema debe mostrar:

- ocupación de cada periodo;
- diferencia en puntos porcentuales;
- variación relativa, cuando sea útil;
- número de sesiones analizadas en cada periodo;
- advertencias si los periodos no son comparables.

---

## US-06 — Comprender el cálculo

Como propietario de un box,

quiero saber cómo se ha calculado cada resultado,

para poder confiar en la respuesta.

### Resultado esperado

Toda respuesta analítica debe incluir:

- métrica utilizada;
- periodo;
- datos incluidos;
- datos excluidos;
- limitaciones relevantes.

El sistema no debe mostrar únicamente una conclusión sin explicar su origen.

---

## US-07 — Recibir una respuesta prudente

Como propietario de un box,

quiero que el sistema reconozca cuándo no dispone de datos suficientes,

para evitar tomar decisiones basadas en conclusiones incorrectas.

### Ejemplo de pregunta

> ¿Qué entrenador consigue mayor fidelidad de clientes?

### Resultado esperado

Si el dataset no permite responder con fiabilidad, el sistema debe:

- indicar que no dispone de evidencia suficiente;
- explicar qué datos faltan;
- evitar inventar una respuesta;
- indicar cómo podría calcularse en el futuro.

---

## US-08 — Preguntar en lenguaje natural

Como propietario de un box,

quiero formular preguntas con palabras normales,

para no tener que conocer consultas técnicas, endpoints o bases de datos.

### Ejemplos equivalentes

> ¿Qué clases funcionan peor?

> Enséñame las clases con menos ocupación.

> ¿Cuáles son los horarios menos aprovechados?

### Resultado esperado

El sistema debe reconocer preguntas equivalentes y asociarlas a una consulta analítica soportada.

Cuando una pregunta sea ambigua, debe solicitar una aclaración antes de calcular el resultado.

---

# Historias fuera del MVP

Las siguientes historias no forman parte de esta primera prueba:

- realizar o cancelar reservas;
- modificar clases o usuarios;
- enviar mensajes a clientes;
- analizar pagos o facturación;
- gestionar varios boxes;
- generar campañas comerciales;
- predecir bajas mediante modelos de aprendizaje automático;
- permitir acceso directo a clientes del box;
- ejecutar acciones sobre la API real de AimHarder.

---

# Prioridad del MVP

| Prioridad | Historia |
|---|---|
| Obligatoria | US-01 — Ocupación media |
| Obligatoria | US-02 — Clases con baja ocupación |
| Obligatoria | US-03 — Cancelaciones |
| Obligatoria | US-04 — Usuarios inactivos |
| Obligatoria | US-05 — Comparación de periodos |
| Transversal | US-06 — Explicación del cálculo |
| Transversal | US-07 — Respuesta prudente |
| Transversal | US-08 — Lenguaje natural |

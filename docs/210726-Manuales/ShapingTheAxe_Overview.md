# ShapingTheAxe

**Qué es, qué hace hoy, qué puede llegar a ser y qué se está explorando construir sobre él.**

> "Shape the decision before committing the cut."

**Documento descriptivo · no normativo**

| | |
|---|---|
| **Versión del framework** | `0.2.0-beta.2` |
| **Publicada** | 2026-07-19 |
| **Documento preparado** | 2026-07-21 |
| **Estado del repositorio** | commit `166b0ea` |
| **Autoridad semántica** | `SHAPING_THE_AXE_BRAIN_SPEC.md` |

> Este documento es una síntesis de lectura; en caso de conflicto, la especificación normativa gobierna.

---

## Índice

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Qué es STA — identidad estable](#2-qué-es-sta--identidad-estable)
3. [Arquitectura — planos y mecanismo de ejecución](#3-arquitectura--planos-y-mecanismo-de-ejecución)
4. [Qué hace hoy — la beta manual](#4-qué-hace-hoy--la-beta-manual)
5. [Evidencia de validación — qué está probado y qué no](#5-evidencia-de-validación--qué-está-probado-y-qué-no)
6. [Qué puede llegar a ser — la ruta de evolución gobernada](#6-qué-puede-llegar-a-ser--la-ruta-de-evolución-gobernada)
7. [Qué puede hacer — exploración de negocio (no normativa)](#7-qué-puede-hacer--exploración-de-negocio-no-normativa)
8. [Gobernanza y disciplina epistémica](#8-gobernanza-y-disciplina-epistémica)
9. [Estado actual y próximos pasos](#9-estado-actual-y-próximos-pasos)
10. [Fuentes](#10-fuentes)

---

## 1. Resumen ejecutivo

ShapingTheAxe (STA) es un método gobernado y agnóstico de proveedor para preparar, decidir, ejecutar, verificar y aprender de trabajo asistido por IA, bajo supervisión humana. No es un producto de software terminado ni una empresa: es, ante todo, un protocolo — un conjunto de leyes y un ciclo operativo — que hoy se ejecuta manualmente dentro de un entorno de IA capaz.

Conviene distinguir cuatro cosas que suelen confundirse bajo el mismo nombre:

- **[IDENTIDAD]** lo que STA es, con independencia de cómo se implemente: un método de decisión gobernado, no un producto.
- **[IMPLEMENTACIÓN ACTUAL]** una beta ejecutable a mano, sin CLI ni automatización propia, evaluada en dos casos de referencia cerrados.
- **[ARQUITECTURA OBJETIVO]** una hoja de ruta gobernada y con evidencia hacia un mecanismo de ejecución automatizado — no implementado todavía.
- **[EXPLORACIÓN DE NEGOCIO]** hipótesis de producto construidas sobre STA (asistentes de IA para pymes), explícitamente no normativas y no validadas.

Este documento recorre las cuatro capas por separado para evitar tanto la infravaloración (tratar STA como "solo una beta manual, sin futuro") como la sobreventa (prometer capacidades que hoy no existen).

---

## 2. Qué es STA — identidad estable

La especificación normativa (`SHAPING_THE_AXE_BRAIN_SPEC.md` §1) define STA como:

> "A universal, provider-independent system for preparing, deciding, executing, verifying, and learning from work performed by AI agents with human oversight."

Y, con la misma fuerza normativa, define lo que **no** es: no es un prompt gigante, no es un cuestionario obligatorio, no es un catálogo de herramientas y no es un sustituto autónomo de la responsabilidad humana. Estas cuatro negaciones son identitarias y estables — no dependen de qué tan automatizada esté la implementación en un momento dado.

### Función objetivo

El objetivo declarado (§2) es maximizar la calidad de decisión y ejecución mientras se reduce la incertidumbre, el error y el trabajo desperdiciado, usando el **coste total mínimo** compatible con el riesgo y la Definición de Hecho (Definition of Done). El coste total incluye tiempo, dinero, tokens y contexto activo, herramientas y servicios externos, coordinación y atención humana, carga cognitiva, mantenimiento, complejidad introducida y coste de recuperación si la decisión es errónea.

### Leyes universales

Once leyes gobiernan el comportamiento del sistema en cualquier implementación (§3), entre ellas:

- **Proporcionalidad** — la profundidad de análisis, planificación y verificación debe ser proporcional al impacto, la reversibilidad y la sensibilidad de la decisión.
- **Evidencia antes que confianza** — las afirmaciones críticas deben apoyarse en evidencia inspeccionada, no en fluidez o volumen de texto.
- **Inspeccionar antes de preguntar** — no se pregunta al usuario lo que ya es descubrible en fuentes disponibles.
- **Las contradicciones permanecen visibles** — nunca se promedian ni se fusionan en silencio.
- **Ejecución y evolución están separadas** — el sistema no puede modificar su propio núcleo ni promover aprendizaje durante una ejecución en curso.
- **Privilegio mínimo** — cada capacidad opera con el permiso y la duración mínimos necesarios; los permisos no se heredan implícitamente.
- **Portabilidad por separación** — el comportamiento canónico es independiente del proveedor; lo específico de cada proveedor vive en adaptadores.

---

## 3. Arquitectura — planos y mecanismo de ejecución

STA separa cuatro planos conceptuales y un mecanismo de ejecución que los pone en marcha:

| Componente | Qué es | Estado |
|---|---|---|
| **Brain Specification** | Autoridad semántica. Define visión, leyes universales y gobernanza. Estable con independencia de la implementación. | Vigente |
| **STA Kernel** | Forma operativa compacta y portable de la Brain Specification. | Vigente, manual |
| **Runtime Plane** | Estado de una ejecución concreta: clasificación, contexto activo, afirmaciones, decisiones, puertas, plan, evidencia y cierre. Temporal o de alcance de proyecto, no es el núcleo. | Vigente |
| **Capability Plane** | Especificaciones canónicas de capacidad, descubiertas bajo demanda mediante `DISCOVER → REUSE → COMPOSE → SYNTHESIZE`. | Vigente, sin catálogo |
| **Evolution Plane** | Revisa evidencia de ejecuciones cerradas y propone retención, poda o promoción. No puede alterar una ejecución activa. | Vigente, manual |
| **STA Execution Engine** | Mecanismo *futuro* destinado a ejecutar el ciclo operativo, poseer la orquestación y producir el estado del Runtime Plane de forma automática. No es un quinto plano. | **No construido** |

Hoy, el papel del STA Execution Engine lo desempeña manualmente la implementación de referencia: un entorno de IA capaz sigue el STA Kernel a mano. La orquestación automatizada, las skills ejecutables, un runner de CLI y la coordinación de MCP son capacidades futuras gobernadas, todavía no aprobadas.

Dos conceptos de adaptador describen cómo se conectan proveedores y capacidades a ShapingTheAxe, mantenidos deliberadamente separados:

- **STA Environment Adapters** — enrutan una herramienta de IA concreta (Claude Code, Codex, Copilot) hacia el STA Kernel. Implementados hoy como los stubs de `adapters/`.
- **STA Capability Adapters** — implementan una especificación de capacidad canónica para un proveedor concreto. Todavía no construidos; definidos normativamente en la Brain Specification (§8.2).

El límite exacto entre ambos sigue abierto y se mantiene como una deuda terminológica reconocida, no resuelta todavía.

---

## 4. Qué hace hoy — la beta manual

La implementación actual es `0.2.0-beta.2`, publicada el 2026-07-19, en estado *"beta bajo validación comparativa"*. Se ejecuta por completo en Markdown: no requiere instalación, CLI ni infraestructura propia.

### Ciclo operativo

El STA Kernel reduce la Brain Specification a un ciclo corto que un operador humano y un entorno de IA ejecutan juntos: clasificar tarea, autoridad, riesgo y presupuesto; diseñar la inspección alrededor de afirmaciones que cambian la decisión; inspeccionar antes de preguntar; detectar y controlar vacíos y contradicciones; satisfacer las puertas de comprensión y plan exigidas por el riesgo; ejecutar dentro del alcance y permisos aprobados; verificar con independencia proporcional; y cerrar con evidencia, difiriendo las decisiones de aprendizaje hasta después de la ejecución.

El presupuesto de preparación se selecciona cualitativamente entre `MICRO`, `STANDARD`, `DEEP` y `CRITICAL` según impacto, reversibilidad, incertidumbre, alcance, sensibilidad y coste de recuperación — nunca como un porcentaje inventado. Las decisiones se clasifican en tres niveles de autoridad: `LEVEL_1_AUTONOMOUS`, `LEVEL_2_RECOMMENDED` y `LEVEL_3_USER_RESERVED`.

### Exclusiones actuales de la beta

Por diseño, y de forma explícita en la especificación (§13.3), la beta actual excluye: una CLI; orquestación automática de múltiples agentes; servidores MCP propios; aprendizaje automatizado o actualizaciones del núcleo; un catálogo grande de capacidades; autoridad de producción; afirmaciones de efectividad universal; y un libro generado. Estas exclusiones describen el estado actual de la implementación de referencia, no un techo permanente de la arquitectura.

### Casos de referencia cerrados

| Caso | Protocolo | Resultado | Alcance real |
|---|---|---|---|
| `ft_irc` | Fundación `v0.1` / `context-init v0.2` (predecesor) | 91.3/100 · **PASS** · sin fallo grave · handoff independiente superado | No es grado Referencia (falta transcripción cronológica completa y una transición formalizada). Congelado; no se puede repetir ni reconstruir. |
| `crossfit-business-copilot` | Línea beta actual | **PASS** · dos implementaciones independientes, tres evaluadores ciegos convergieron en el mismo ranking | Evidencia positiva de ejecución reproducible y evaluación ciega comparativa. No demuestra superioridad universal, significancia estadística ni validación multidominio. |

---

## 5. Evidencia de validación — qué está probado y qué no

Cada versión y ejecución de STA se evalúa sobre siete dimensiones: corrección, eficiencia, trazabilidad, autonomía útil, calidad de escalado, portabilidad y aprendizaje limpio.

> **Lo que la evidencia actual sostiene:** ejecución reproducible, evaluación ciega comparativa y convergencia entre evaluadores independientes.
>
> **Lo que la evidencia actual NO sostiene todavía:** superioridad universal, significancia estadística, validación multidominio.

El protocolo de validación comparativa completo (congelar un caso de software no familiar, un caso arquitectónico nuevo y un caso no-software o mixto, y comparar STA frente a brainstorming y frente a un flujo de trabajo normal) está diseñado pero todavía no ejecutado — es el Hito 3 de la hoja de ruta, bloqueado hasta que existan esos casos congelados.

---

## 6. Qué puede llegar a ser — la ruta de evolución gobernada

Las exclusiones actuales no son una declaración de que STA nunca orquestará agentes, compondrá skills o coordinará MCPs. La especificación reserva una sección explícita, `PROPOSALS — NOT YET APPROVED`, para las extensiones futuras del STA Execution Engine. Cada propuesta debe declarar su problema, beneficio, coste, riesgo, impacto sobre el núcleo y experimento de validación antes de poder implementarse:

| Propuesta | Qué resolvería | Condición para avanzar |
|---|---|---|
| Esquema de runtime legible por máquina | Validar estado automáticamente en vez de solo por disciplina en Markdown | Codificar tres registros de ejecución y medir el valor frente al coste de mantenimiento |
| Runner de CLI | Activación e inicialización repetibles | Solo tras fallos mecánicos repetidos observados en tres casos beta manuales |
| Orquestación automática de agentes | Roles paralelos independientes con verificación cruzada | Comparar ejecución de un solo agente frente a delegada en el mismo caso `DEEP` |
| Síntesis automatizada de capacidades | Creación más rápida de skills y ayudantes acotados | Revisar manualmente diez candidatos antes de automatizar cualquier paso |
| Pipeline de aprendizaje automatizado | Retención y poda sistemáticas a escala | Requiere aprobación separada y evaluación de seguridad independiente — impacto alto sobre el núcleo |
| Modelo de coste cuantitativo | Decisiones de eficiencia más comparables entre operadores | Recolectar observaciones de coste crudas sin usarlas para decisiones automáticas todavía |

Ninguna de estas propuestas es un requisito de la beta actual, y ninguna está implementada hoy. Es, deliberadamente, el mismo estándar de evidencia que STA exige para cualquier otra decisión: nada se promueve solo por estar disponible o ser reutilizable.

---

## 7. Qué puede hacer — exploración de negocio (no normativa)

> La carpeta `business/` del repositorio es explícitamente **no normativa** para el framework. Describe hipótesis y decisiones de producto, no reglas de comportamiento del kernel. Nada aquí debe leerse como parte de la identidad de STA.

### La hipótesis Eldorado

El producto explorado deja de ser "crear un chatbot para una peluquería" y pasa a ser "crear una fábrica gobernada por ShapingTheAxe capaz de diagnosticar un negocio y generar su asistente a medida". La tesis: el chatbot final es copiable; lo diferencial es el proceso que convierte un negocio real en una definición operativa verificable — necesidades, reglas, excepciones, datos, tono, límites y criterios de verificación. El posible foso solo existe si puede medirse.

El MVP de esta hipótesis no genera un chatbot automáticamente: genera una especificación ejecutable (`business-profile.yaml`, `assistant-policy.md`, `services.json`, `conversation-style.md`, `integration-config.yaml`, `acceptance-tests.md`) que una plantilla común usaría para construir el asistente.

**Criterio de refutación explícito:** la hipótesis debe rechazarse o reducirse si depende totalmente de una persona, si cada cliente sigue siendo artesanal, si no mejora frente a un proceso manual, o si añade burocracia sin valor.

### Orden recomendado de validación de modelo de negocio

Herramienta interna → servicio gestionado B2B → consultoría o licencia → plataforma → SaaS. Ninguno de estos pasos está validado todavía.

### Protocolo de validación del MVP

Diseñado, pendiente de ejecución completa. Alcance mínimo: un vertical, dos negocios reales comparables, mismo operador, comparación contra proceso manual tradicional, y repetición con un segundo operador. Candidato inicial: dos boxes de CrossFit; segunda fase, peluquería o salón de belleza. Fuera de alcance deliberadamente: construcción automática, despliegue, WhatsApp, arquitectura, SaaS, autonomía total, financiación y modelo comercial definitivo.

### Estado de decisiones de negocio

| Decisión | Estado |
|---|---|
| Separación de proyectos (STA framework / STA Assistants / empresa) | Aprobada |
| Forma empresarial final (herramienta interna, consultoría, SaaS, licencia…) | Abierta, no decidida |
| Hipótesis Eldorado | En validación |
| MVP inicial (definiciones verificables de negocios reales) | Recomendado, pendiente de aprobación |
| Casos iniciales (CrossFit, luego peluquería) | Candidatos |
| Financiación | No decidida — requiere primero problema real demostrado, mejora medible, repetibilidad, comprador y escalabilidad |

---

## 8. Gobernanza y disciplina epistémica

Más allá de qué hace, cómo STA decide es en sí mismo parte de su propuesta: es un método diseñado para no fingir certeza que no tiene.

- **Autoridad por dominio, no por fuente universal** — la intención la decide el usuario responsable; el comportamiento actual lo decide la ejecución reproducible; la arquitectura aprobada la decide la decisión registrada, etc.
- **Estados de conocimiento explícitos** — cada afirmación crítica se registra como `UNKNOWN`, `PARTIAL`, `PROVISIONAL`, `VERIFIED`, `CONFLICTED` o `NOT_APPLICABLE`; una afirmación `CONFLICTED` bloquea la decisión afectada hasta resolverse.
- **Separación ejecución/evolución** — durante una ejecución se pueden registrar observaciones, pero nunca modificar el núcleo, promover una capacidad o reescribir las propias reglas de gobierno; eso ocurre después del cierre, mediante un proceso explícito y versionado.
- **Versionado y reversión** — todo se versiona de forma independiente (especificación, kernel, contratos, capacidades, adaptadores, perfiles, rúbricas, políticas de permisos, traducciones); la reversión operacional restaura la última versión estable, la reversión analítica compara versiones para localizar una regresión.
- **Seguridad y privacidad** — los permisos (lectura, escritura, ejecución, instalación, borrado, publicación, acceso a secretos, red, gasto, acción en producción) son dimensiones independientes; la información se clasifica en `PUBLIC`, `INTERNAL`, `CONFIDENTIAL` o `RESTRICTED`.

---

## 9. Estado actual y próximos pasos

| Frente | Estado |
|---|---|
| Framework / especificación | `0.2.0-beta.2`, publicada 2026-07-19, "beta bajo validación comparativa" |
| Paquete de beta manual (Hito 2) | Implementado; pendiente verificación estructural y semántica de release |
| Validación comparativa (Hito 3) | Pendiente — sin casos congelados adicionales todavía |
| Decisión de revisión o estabilización de la beta (Hito 4) | Bloqueada por evidencia del Hito 3 |
| Portabilidad opcional — segundo proveedor, traducción revisada (Hito 5) | Posterior; requiere necesidad demostrada |
| Arquitectura — STA Execution Engine y adaptadores | Propuestas registradas, ninguna aprobada ni construida |
| Hipótesis de negocio (STA Assistants / Eldorado) | MVP diseñado, aprobación y ejecución pendientes |

---

## 10. Fuentes

Este documento es una síntesis de lectura del estado del repositorio en el commit `166b0ea` (2026-07-21). No añade ninguna afirmación que no esté ya en estas fuentes; en caso de discrepancia, ellas gobiernan sobre este resumen:

- `SHAPING_THE_AXE_BRAIN_SPEC.md` — autoridad semántica (identidad, leyes, arquitectura de planos, ciclo operativo, gobernanza, propuestas no aprobadas).
- `ShapingTheAxe.md` — kernel operativo portable.
- `README.md`, `docs/architecture.md`, `docs/beta-architecture.md`, `docs/roadmap.md` — arquitectura descriptiva, mecanismo de ejecución, hoja de ruta.
- `framework.yaml` — identidad exacta de versión y casos de referencia.
- `examples/ft_irc/README.md`, `validation/case-studies/crossfit-business-copilot/` — evidencia de los dos casos de referencia cerrados.
- `business/README.md`, `business/ELDORADO_HYPOTHESIS.md`, `business/PRODUCT_HYPOTHESES.md`, `business/MVP_VALIDATION.md`, `business/DECISIONS.md` — exploración de negocio, explícitamente no normativa.

---

*Documento descriptivo preparado a partir del repositorio ShapingTheAxe. No es un documento normativo ni un material de venta; su propósito es dar una visión de conjunto trazable. La autoridad semántica sigue siendo `SHAPING_THE_AXE_BRAIN_SPEC.md`.*

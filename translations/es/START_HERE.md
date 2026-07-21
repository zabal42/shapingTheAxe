---
translation_of: START_HERE.md
source_version: 0.1-beta
normative_language: English
translation_language: Spanish
synchronization_state: CURRENT
last_reviewed_source_version: 0.1-beta
---

# Empieza con ShapingTheAxe en 30 segundos

**Versión de Easy Start:** `0.1-beta`

**Versión de esta traducción:** `0.1-beta-es.1`

**Framework de referencia:** ShapingTheAxe `0.2.0-beta.2`

**Función:** guía de inicio no normativa. Esta es una traducción sincronizada
de [`START_HERE.md`](../../START_HERE.md). Si existe cualquier conflicto,
prevalecen el archivo original en inglés y, como autoridad semántica,
`SHAPING_THE_AXE_BRAIN_SPEC.md`.

ShapingTheAxe no necesita CLI, plugin, cuenta ni instalar una skill global. La
experiencia mínima es:

> **Un archivo, una frase y una confirmación visible de activación.**

## Cualquier chat con IA

1. Adjunta [`ShapingTheAxe.md`](../../ShapingTheAxe.md).
2. Envía:

```text
Activa ShapingTheAxe para esta tarea: <tu tarea>
```

Puedes escribir la frase de activación y la tarea en cualquier idioma.

La IA debe confirmar la activación y continuar:

```text
STA ACTIVE · <MICRO|STANDARD|DEEP|CRITICAL> · <INTERVENTION> · <siguiente acción>
```

Si la IA no puede leer realmente el kernel, debe responder:

```text
STA BLOCKED · KERNEL_NOT_AVAILABLE · Adjunta o proporciona ShapingTheAxe.md
```

Nunca debe fingir que el framework está activo.

## IA con acceso al repositorio

Cuando los archivos del framework estén disponibles en el proyecto, envía:

```text
Lee ShapingTheAxe.md y aplícalo a esta tarea: <tu tarea>
```

Para reutilizar una versión preparada para copiar y pegar, usa
[`prompts/activate.md`](../../prompts/activate.md).

Las herramientas con acceso al repositorio pueden utilizar un pequeño adaptador
de enrutamiento de [`adapters/`](../../adapters/):

| Entorno | Copiar o integrar |
|---|---|
| Codex y herramientas que leen `AGENTS.md` | `adapters/AGENTS.stub.md` -> `AGENTS.md` |
| Claude Code | `adapters/CLAUDE.stub.md` -> `CLAUDE.md` |
| GitHub Copilot | `adapters/copilot-instructions.stub.md` -> `.github/copilot-instructions.md` |
| Otro entorno de IA | Copia el bloque de adaptador universal inferior en su archivo de instrucciones del proyecto |

No sobrescribas un archivo de instrucciones existente. Integra el bloque de
enrutamiento conservando las instrucciones específicas del proyecto.

## Bloque de adaptador universal

```markdown
Antes de realizar trabajo material, lee y sigue `ShapingTheAxe.md`.
`SHAPING_THE_AXE_BRAIN_SPEC.md` es la autoridad semántica.
Usa `prompts/activate.md` para la confirmación de activación y el comportamiento alternativo.
Utiliza la preparación mínima justificada por el riesgo; no añadas gates universales de aprobación.
No cargues nada de `incubator/` salvo que el usuario autorice explícitamente una evaluación controlada.
Si un archivo necesario no está disponible, indícalo en lugar de afirmar que la activación se ha realizado.
```

## API o agente personalizado

Proporciona `ShapingTheAxe.md` en el contexto de sistema o de desarrollador y
añade la tarea de la forma habitual. La aplicación puede utilizar
`prompts/activate.md` como lanzador, pero no debe tratarlo como una segunda
fuente semántica.

Para trabajo ordinario, el kernel portable es suficiente. Carga
`SHAPING_THE_AXE_BRAIN_SPEC.md` cuando:

- se esté interpretando o modificando el propio framework;
- aparezca un conflicto o una ambigüedad semántica;
- una decisión `DEEP` o `CRITICAL` necesite el contrato completo;
- se requiera conformidad o evaluación independiente.

## Lo que la activación no autoriza

La activación no concede permiso para escribir, ejecutar, instalar, eliminar,
publicar, usar la red, acceder a secretos, gastar dinero ni actuar sobre
producción. Esos permisos proceden exclusivamente de la tarea activa y de la
autoridad responsable.

La activación tampoco carga capacidades candidatas. En particular,
`incubator/testing-strategy/` permanece inactiva salvo que un caso de incubación
controlada autorice su uso explícitamente.

## Las tareas pequeñas siguen siendo pequeñas

Para trabajo claro, reversible y de bajo riesgo, la confirmación puede ser el
único artefacto visible de preparación. La IA debe continuar sin preguntas
ceremoniales ni documentos completos, salvo que un gap material, un permiso,
una decisión o un riesgo los requiera.

## Cuándo se necesitan más archivos

La IA debe inspeccionar las fuentes relevantes disponibles antes de preguntar.
Si no puede acceder a un repositorio, requisito, archivo adjunto o entorno
necesario, debe identificar la fuente ausente exacta y explicar cómo afecta a
la siguiente decisión.

No adjuntes todo el framework de forma predeterminada. Añade contexto únicamente
cuando su valor esperado justifique su coste.

# Manual de instalación y activación de ShapingTheAxe

> Guía para ZSH/macOS. Estado: beta portable.

## 1. Dos formas de uso

### Modo portable
Adjunta o da acceso a:

- `SHAPING_THE_AXE_BRAIN_SPEC.md`
- `ShapingTheAxe.md`
- `README.md`
- `rubric.md`
- `templates/`

Prompt:

```text
Usa SHAPING_THE_AXE_BRAIN_SPEC.md como especificación normativa
y ShapingTheAxe.md como kernel operativo.
Aplica ShapingTheAxe a esta tarea.
```

### Modo skill
Necesita una carpeta válida:

```text
shaping-the-axe/
├── SKILL.md
├── references/
├── templates/
└── scripts/       # opcional
```

No basta con copiar `ShapingTheAxe.md`: debe existir `SKILL.md`.

---

## 2. Preparación

Ajusta la ruta:

```zsh
export STA_ROOT="/Users/mikelzabal/Desktop/CodingWithZabal/ShapingTheAxe/repo"
export STA_SKILL="$STA_ROOT/skills/shaping-the-axe"
```

Comprueba:

```zsh
test -d "$STA_ROOT" && echo "Repo OK" || echo "Ruta incorrecta"
test -f "$STA_SKILL/SKILL.md" && echo "Skill OK" || echo "Falta SKILL.md"
```

Mientras falte `SKILL.md`, usa el modo portable.

---

# 3. Claude Code — Don Claudio

Claude Code descubre skills en:

- Proyecto: `.claude/skills/<nombre>/SKILL.md`
- Global: `~/.claude/skills/<nombre>/SKILL.md`

## Proyecto

```zsh
cd /ruta/al/proyecto
mkdir -p .claude/skills
ln -sfn "$STA_SKILL" .claude/skills/shaping-the-axe
claude
```

Dentro de Claude:

```text
/skills
/shaping-the-axe
```

Con tarea:

```text
/shaping-the-axe Audita este repositorio frente al subject adjunto.
```

## Global

```zsh
mkdir -p ~/.claude/skills
ln -sfn "$STA_SKILL" ~/.claude/skills/shaping-the-axe
```

## Verificar instrucciones persistentes

Claude Code usa `CLAUDE.md`. Puedes comprobar lo cargado con:

```text
/memory
```

## Desinstalar

```zsh
rm .claude/skills/shaping-the-axe
rm ~/.claude/skills/shaping-the-axe
```

---

# 4. Codex

Codex descubre skills en:

- Proyecto: `.agents/skills/<nombre>/SKILL.md`
- Global: `~/.agents/skills/<nombre>/SKILL.md`

## Proyecto

```zsh
cd /ruta/al/proyecto
mkdir -p .agents/skills
ln -sfn "$STA_SKILL" .agents/skills/shaping-the-axe
codex
```

Dentro de Codex:

```text
/skills
```

Activación:

```text
Usa $shaping-the-axe para preparar y ejecutar esta tarea.
```

También puedes escribir `$` para mencionar una skill.

## Global

```zsh
mkdir -p ~/.agents/skills
ln -sfn "$STA_SKILL" ~/.agents/skills/shaping-the-axe
```

## AGENTS.md opcional

```zsh
cat >> AGENTS.md <<'EOF'

## ShapingTheAxe
Para tareas no triviales, evalúa si debe activarse `shaping-the-axe`.
Selecciónala por necesidad, riesgo y valor esperado; no por rutina.
EOF
```

## Desinstalar

```zsh
rm .agents/skills/shaping-the-axe
rm ~/.agents/skills/shaping-the-axe
```

---

# 5. ChatGPT Work — Sunny García

## Web

1. Abre el proyecto.
2. Selecciona **Work**.
3. Adjunta el Brain Spec, el kernel y los archivos de la tarea.
4. Escribe:

```text
Usa SHAPING_THE_AXE_BRAIN_SPEC.md como especificación normativa
y ShapingTheAxe.md como kernel operativo.
Aplica ShapingTheAxe a esta tarea.
```

## Escritorio

1. Abre la carpeta local.
2. Selecciona **Work**.
3. Concede acceso solo a los archivos necesarios.
4. Usa el mismo prompt.

## Comprobación

```text
¿Qué presupuesto has seleccionado, qué fuentes inspeccionarás
y qué decisiones requieren mi intervención?
```

Work web no accede directamente a carpetas locales; para eso usa Work de escritorio.

---

# 6. ChatGPT normal — Frijolero

Adjunta los archivos y escribe:

```text
Lee primero SHAPING_THE_AXE_BRAIN_SPEC.md.
Después lee ShapingTheAxe.md.
Aplica ambos a la tarea que te daré.
```

En el mismo proyecto o conversación, después basta con:

```text
Aplica ShapingTheAxe a esta tarea.
```

---

# 7. Gemini CLI

Gemini CLI descubre skills en:

- Proyecto: `.gemini/skills/` o `.agents/skills/`
- Global: `~/.gemini/skills/` o `~/.agents/skills/`

La ruta `.agents/skills/` permite compartir una sola instalación con Codex.

## Proyecto compartido Codex + Gemini

```zsh
cd /ruta/al/proyecto
mkdir -p .agents/skills
ln -sfn "$STA_SKILL" .agents/skills/shaping-the-axe
gemini
```

## Global compartido

```zsh
mkdir -p ~/.agents/skills
ln -sfn "$STA_SKILL" ~/.agents/skills/shaping-the-axe
```

## Enlazar con Gemini

```zsh
gemini skills link "$STA_SKILL"
```

Solo para el proyecto:

```zsh
gemini skills link "$STA_SKILL" --scope workspace
```

## Verificar desde ZSH

```zsh
gemini skills list --all
```

Dentro de Gemini:

```text
/skills list
/skills reload
```

Activación:

```text
Activa la skill shaping-the-axe y aplícala a esta tarea.
```

Gemini pedirá consentimiento antes de activar una skill y darle acceso a sus recursos.

## Activar o desactivar

```text
/skills disable shaping-the-axe
/skills enable shaping-the-axe
```

## Contexto persistente opcional

Gemini usa `GEMINI.md`:

```zsh
cat >> GEMINI.md <<'EOF'

## ShapingTheAxe
Para tareas no triviales, considera `shaping-the-axe`.
Actívala por necesidad y no por rutina.
Escala al usuario las decisiones materiales.
EOF
```

Recarga:

```text
/memory reload
```

## Desinstalar

```zsh
gemini skills uninstall shaping-the-axe
```

---

# 8. Estructura portable recomendada

```text
ShapingTheAxe/
└── skills/
    └── shaping-the-axe/
        ├── SKILL.md
        ├── references/
        │   ├── SHAPING_THE_AXE_BRAIN_SPEC.md
        │   └── ShapingTheAxe.md
        └── templates/
```

Enlaces:

```text
Claude Code → .claude/skills/shaping-the-axe
Codex       → .agents/skills/shaping-the-axe
Gemini CLI  → .agents/skills/shaping-the-axe
```

Así mantienes una sola fuente, una sola versión y un rollback común.

---

# 9. Activaciones recomendadas

## Universal

```text
Aplica ShapingTheAxe a esta tarea.
Clasifica tarea, dominio, estado y modo autorizado.
Selecciona automáticamente el presupuesto y las capacidades mínimas suficientes.
Inspecciona antes de preguntar.
Escálame únicamente las decisiones materiales.
```

## Diseño

```text
Aplica ShapingTheAxe.
Activa brainstorming solo si el espacio de soluciones sigue abierto.
No implementes una decisión creativa material sin mi aprobación.
```

## Plan aprobado

```text
Aplica ShapingTheAxe en modo ejecución.
El objetivo y el plan material ya están aprobados.
Trabaja con autonomía y detente solo ante cambios materiales.
```

## Auditoría

```text
Aplica ShapingTheAxe en modo auditoría y solo lectura.
No modifiques el objeto evaluado.
Conserva evidencias reproducibles.
```

---

# 10. Diagnóstico rápido

```zsh
echo "=== Skill canónica ==="
test -f "$STA_SKILL/SKILL.md" && echo "OK" || echo "FALTA"

echo "\n=== Claude ==="
ls -ld ~/.claude/skills/shaping-the-axe 2>/dev/null || echo "No global"

echo "\n=== Codex/Gemini ==="
ls -ld ~/.agents/skills/shaping-the-axe 2>/dev/null || echo "No global"

echo "\n=== Ejecutables ==="
command -v claude || echo "Claude Code no encontrado"
command -v codex || echo "Codex no encontrado"
command -v gemini || echo "Gemini CLI no encontrado"
```

---

# 11. Errores habituales

## La skill no aparece

```zsh
test -f "$STA_SKILL/SKILL.md"
readlink .agents/skills/shaping-the-axe
```

Después reinicia el agente o recarga skills.

## Se activa para todo

Corrige la `description` de `SKILL.md`: debe indicar cuándo usarla y cuándo no.

## Pide permiso para todo

La política correcta es:

```text
Aprobación para decisiones materiales.
Autonomía para acciones operativas dentro del alcance aprobado.
```

## Las plataformas usan copias distintas

No copies la carpeta: usa enlaces simbólicos.

## Una actualización empeora el resultado

```zsh
cd "$STA_ROOT"
git log --oneline --decorate -10
git switch -c rollback/sta-estable <commit-estable>
```

---

# 12. Estado actual

Hasta que Sunny García genere y valide el directorio portable con `SKILL.md`:

- usa el modo portable;
- no inventes una skill incompleta;
- conserva el Brain Spec como fuente normativa;
- conserva `ShapingTheAxe.md` como kernel;
- registra el commit utilizado.

Cuando exista el adaptador portable, los enlaces de este manual permitirán usar una única skill en Claude Code, Codex y Gemini CLI.

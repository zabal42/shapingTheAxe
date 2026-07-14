# Start ShapingTheAxe in 30 Seconds

**Easy Start version:** `0.1-beta`

**Framework target:** ShapingTheAxe `0.2.0-beta.1`

**Role:** Non-normative onboarding. If anything here conflicts with
`SHAPING_THE_AXE_BRAIN_SPEC.md`, the Brain Specification prevails.

ShapingTheAxe does not require a CLI, plugin, account, or global skill
installation. The minimum experience is:

> **One file, one sentence, one visible activation receipt.**

## Any AI chat

1. Attach [`ShapingTheAxe.md`](ShapingTheAxe.md).
2. Send:

```text
Activate ShapingTheAxe for this task: <your task>
```

You may write the activation sentence and task in any language.

The AI should confirm activation and continue:

```text
STA ACTIVE · <MICRO|STANDARD|DEEP|CRITICAL> · <INTERVENTION> · <next action>
```

If the AI cannot actually read the kernel, it must say:

```text
STA BLOCKED · KERNEL_NOT_AVAILABLE · Attach or provide ShapingTheAxe.md
```

It must never pretend the framework is active.

## AI with repository access

When the framework files are available in the project, send:

```text
Read ShapingTheAxe.md and apply it to this task: <your task>
```

For a reusable copy-and-paste version, use
[`prompts/activate.md`](prompts/activate.md).

Repository-aware tools may use a small routing adapter from [`adapters/`](adapters/):

| Environment | Copy or merge |
|---|---|
| Codex and tools that read `AGENTS.md` | `adapters/AGENTS.stub.md` → `AGENTS.md` |
| Claude Code | `adapters/CLAUDE.stub.md` → `CLAUDE.md` |
| GitHub Copilot | `adapters/copilot-instructions.stub.md` → `.github/copilot-instructions.md` |
| Another AI environment | Copy the universal adapter block below into its project-instruction file |

Do not overwrite an existing instruction file. Merge the routing block while
preserving project-specific instructions.

## Universal adapter block

```markdown
Before material work, read and follow `ShapingTheAxe.md`.
`SHAPING_THE_AXE_BRAIN_SPEC.md` is the semantic authority.
Use `prompts/activate.md` for the activation receipt and fallback behavior.
Use the minimum preparation justified by risk; do not add universal approval gates.
Do not load anything under `incubator/` unless the user explicitly authorizes a controlled evaluation.
If a required file is unavailable, say so instead of claiming activation.
```

## API or custom agent

Provide `ShapingTheAxe.md` in the system or developer context and append the
task normally. The application may use `prompts/activate.md` as a launcher, but
must not treat it as a second semantic source.

For ordinary work, the portable kernel is sufficient. Load
`SHAPING_THE_AXE_BRAIN_SPEC.md` when:

- the framework itself is being interpreted or changed;
- a semantic conflict or ambiguity appears;
- a `DEEP` or `CRITICAL` decision needs the full contract;
- conformance or independent evaluation is required.

## What activation does not authorize

Activation does not grant permission to write, execute, install, delete,
publish, use the network, access secrets, spend money, or act on production.
Those permissions come only from the active task and the responsible authority.

Activation also does not load candidate capabilities. In particular,
`incubator/testing-strategy/` remains inactive unless a controlled incubation
case explicitly authorizes it.

## Small tasks stay small

For clear, reversible, low-risk work, the receipt may be the only visible setup
artifact. The AI should continue without ceremonial questions or full-form
documents unless a material gap, permission, decision, or risk requires them.

## When more files are needed

The AI should inspect available relevant sources before asking. If it cannot
access a required repository, requirement, attachment, or environment, it must
identify the exact missing source and explain how it affects the next decision.

Do not attach the entire framework by default. Add context only when its
expected value justifies its cost.

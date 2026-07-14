# Architecture

## Purpose

ShapingTheAxe separates a stable reasoning protocol from the tools that may
eventually execute it. The core must remain usable as a single Markdown file in
any capable AI environment.

The architecture exists to make the method portable, testable, traceable, and
resistant to tool churn.

## System layers

| Layer | Current location | Responsibility | Source of truth? |
|---|---|---|---|
| Protocol kernel | `/ShapingTheAxe.md` | Defines behavior, phases, and hard gates | Yes |
| Artifact contracts | `/templates/` | Defines the persistent outputs of the protocol | Yes, for output shape |
| Evaluation | `/evaluation/rubric.md` | Tests whether an execution obeyed the protocol | Yes, for conformance |
| Reference evidence | `/examples/` | Defines controlled fixtures and retains real run outputs | No, evidence only |
| Tool adapters | Future | Packages the kernel as skills, agents, commands, or integrations | No |

An adapter may add tool-specific activation or automation, but it must not
silently redefine the protocol. If behavior changes, the canonical protocol
changes first.

## Runtime model

The protocol moves through a guarded sequence:

1. Load evidence.
2. Discover only unresolved context.
3. Obtain confirmation of understanding.
4. Analyze and control gaps.
5. Produce and obtain approval for a plan.
6. Execute the plan.
7. Review and prove completion.

Execution is recursive rather than strictly linear. New uncertainty returns the
workflow to Discovery, and any material decision updates the persistent context
and plan before implementation resumes.

## The invariant

Implementation may begin only when all five sources of uncertainty are
sufficiently closed:

| Source | Closure condition |
|---|---|
| Goal and definition of done | The intended result and success evidence are explicit |
| Current state | The actual starting point and relevant history are inspected |
| Style and execution norms | The expected way of editing and writing is known |
| External constraints | Rules that can invalidate an otherwise working result are known |
| Collaborator contract | Existing human work and integration boundaries are respected |

The five sources are fixed. The questions are adaptive.

## Persistent artifacts

The protocol produces three durable contracts:

1. **Context brief:** evidence, confirmed understanding, open gaps, and readiness.
2. **Implementation plan:** approved strategy, tasks, dependencies, risks, and
   verification.
3. **Completion report:** changes, deviations, test evidence, and final status.

These artifacts allow a different AI instance or human collaborator to inspect
the reasoning without relying on conversation memory.

## Design constraints

- **Tool-agnostic core:** no vendor-specific command is required by the kernel.
- **One normative source:** behavior is defined in `ShapingTheAxe.md`, not copied
  into adapters.
- **Evidence before dialogue:** existing artifacts outrank convenient questions.
- **Human authority:** understanding and implementation require explicit human
  gates.
- **Traceability:** important conclusions point to evidence or a recorded human
  decision.
- **Adaptive depth:** the method closes uncertainty rather than completing a
  fixed questionnaire.
- **No fake completion:** claims are backed by verification results.

## Version boundaries

ShapingTheAxe framework releases and `context-init` protocol releases use
independent versions:

- **Framework version:** packages the protocol with templates, evaluations,
  examples, and adapters.
- **Protocol version:** identifies the exact behavioral contract in
  `ShapingTheAxe.md`.

The initial target is framework `v0.1` built around `context-init v0.2`.

## Validated baseline

`context-init v0.2` completed its first independent reference validation in
`ft-irc-reference-001`: **91.3/100 — PASS**, no hard failures, and a successful
independent handoff. This establishes an evidence-backed baseline for the
architecture. It does not yet establish universal transfer or Reference-grade
evidence quality.

The case exposed three operational boundaries above the kernel: chronological
run evidence must be durable, evaluation-mode transitions must be explicit,
and environment-blocked checks must have a structured status. These are
revision candidates for the next version; they do not silently alter the
evaluated `context-init v0.2` contract.

Validation outcomes are recorded in
[`docs/validation-history.md`](validation-history.md), while the underlying
executor and evaluator conversations remain frozen evidence.

## Current non-goals

The foundation does not yet include:

- a CLI or runtime;
- automatic agent orchestration;
- MCP integrations;
- Claude-, Codex-, or IDE-specific adapters;
- translations;
- a generated book;
- claims of universal effectiveness before transfer validation.

Those capabilities belong above a validated kernel, not inside it.

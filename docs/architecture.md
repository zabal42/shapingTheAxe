# Architecture

## Purpose

ShapingTheAxe separates semantic rules, portable execution, project runtime
state, capabilities, and post-close evolution. This keeps the beta usable as
Markdown while preventing providers, adapters, or active runs from silently
redefining the framework.

The detailed beta boundary is in
[`beta-architecture.md`](beta-architecture.md). Canonical states are in
[`state-model.md`](state-model.md).

## Normative hierarchy

| Order | Artifact | Authority |
|---:|---|---|
| 1 | `SHAPING_THE_AXE_BRAIN_SPEC.md` | Semantic source of truth |
| 2 | `ShapingTheAxe.md` | Portable operational kernel derived from the specification |
| 3 | `docs/state-model.md` and templates | Derived state and output contracts |
| 4 | `evaluation/` | Conformance, quality, and beta validation contracts |
| 5 | provider adapters and translations | Non-normative representations |
| 6 | examples and run outputs | Evidence, never normative authority |

If a lower layer conflicts with a higher layer, the higher layer governs and
the conflict is recorded as a defect. No adapter or translation may silently
override canonical behavior.

## Four planes

### Normative plane

Owns specification, kernel, state model, contracts, security, versioning, and
governance. It cannot change during a run.

### Runtime plane

Owns task classification, active context, risk, budget, claims,
contradictions, decisions, gates, plan, execution, evidence, and closure.

### Capability plane

Separates provider-independent capability specifications from provider or tool
adapters. The beta records material usage but does not require a catalog.

### Evolution plane

Evaluates closed-run evidence, learning candidates, versions, regressions,
retention, pruning, promotion proposals, and rollback. It cannot alter active
runtime or the core.

## Runtime flow

```text
CLASSIFY
→ ASSESS RISK AND BUDGET
→ DESIGN INSPECTION
→ INSPECT
→ CONTROL GAPS
→ SATISFY REQUIRED GATES
→ PLAN
→ EXECUTE
→ VERIFY
→ CLOSE
→ POST-CLOSE EVALUATION
```

The flow is reversible. New evidence invalidates only affected claims, context,
gates, and plan sections. Material changes return to inspection, discovery, or
approval. Low-risk reversible details may adapt without interrupting the user.

## Context

The six canonical layers are Intention, Contract, Operation, Domain, Human,
and History. Runtime keeps only decision-relevant context active. Validated and
historical context remain retrievable without occupying the active reasoning
set.

The foundation's five sources remain a compatibility view only.

## Artifact strategy

`MICRO` and bounded `STANDARD` runs may use one compact run record. `DEEP`,
`CRITICAL`, audits, and handoffs use the full context brief, implementation
plan, and completion report. Artifact depth never weakens a required gate or
completion claim.

## Human authority

Human confirmation is required for Level 2 and Level 3 decisions and for the
explicit gates associated with `DEEP` or `CRITICAL` work. Evidence may satisfy
the understanding and plan gates for authorized low-risk Level 1 work.

The user retains authority over intent, material scope, architecture, contract,
cost, permissions, sensitive data, production, and risk acceptance.

## Portability and language

The core requires no vendor-specific command. The canonical specification is
English. A translation declares its source version and synchronization state;
the English source governs disagreement.

## Version boundary

Foundation `v0.1` with `context-init v0.2` is immutable historical evidence.
Beta `0.2.0-beta.1` is a new line with a different semantic authority and
adaptive behavior. Rollback restores complete versions; it does not splice
rules across lines.

## Current non-goals

- CLI or executable state engine;
- automatic agent orchestration;
- custom MCP servers;
- capability registry;
- automatic context graph;
- automated learning or promotion;
- provider-specific packaged adapters;
- translated releases before synchronization review;
- book or universal-effectiveness claims.


# Beta Architecture

**Target:** ShapingTheAxe `0.2.0-beta.2`  
**Architecture style:** Markdown-first, provider-independent, manually
executable, versioned, and reversible

## 1. Architectural outcome

The beta is the smallest architecture that can apply the approved Brain rules
to real work without depending on a specific AI provider or building an
automation platform prematurely.

It separates meaning, execution, capabilities, and evolution while keeping the
runtime usable by supplying one Markdown kernel to a capable AI environment.

```text
NORMATIVE SPECIFICATION
        ↓ derives
PORTABLE KERNEL
        ↓ creates and updates
RUN RECORD / FULL ARTIFACTS
        ↓ retains
EVIDENCE + COMPLETION
        ↓ reviewed after closure
EVALUATION + LEARNING CANDIDATES
```

This whole diagram is performed today by a human operator and a capable AI
environment manually taking on the role that a future **STA Execution
Engine** is intended to automate. See `docs/architecture.md` for the
mechanism/plane distinction.

## 2. Architecture principles

1. One semantic authority: `SHAPING_THE_AXE_BRAIN_SPEC.md`.
2. One compact operational entry point: `ShapingTheAxe.md`.
3. No runtime self-modification.
4. Full traceability only where risk or handoff justifies it.
5. Provider behavior remains outside the core.
6. State and gates are explicit even when recorded compactly.
7. The foundation remains immutable and separately identifiable.
8. Every version has a rollback path.

## 3. Minimal components

### 3.1 Normative specification

The Brain Specification defines laws, vocabulary, models, responsibilities,
and governance. Other files may explain or operationalize it but cannot invent
normative behavior.

### 3.2 Portable kernel

The kernel converts the specification into a short operating sequence:

1. classify;
2. set budget;
3. design and perform inspection;
4. control gaps;
5. apply the required understanding and plan gates;
6. execute inside authority;
7. verify proportionately;
8. close and emit learning candidates.

The kernel contains enough rules to run manually but links to the specification
for definitions and exceptional cases.

### 3.3 Runtime record

The compact run record is the minimum persistent state for small executions.
It combines:

- task capsule and authority;
- risk and budget;
- six-layer context summary;
- critical claims and contradictions;
- gates and decisions;
- compact plan;
- capability ledger;
- actual verification;
- final status and learning candidates.

It is not mandatory to populate irrelevant sections. Omitted required data must
be marked, not silently absent.

### 3.4 Full artifact contracts

The existing context brief, implementation plan, and completion report remain
the full output form. They are used for `DEEP`, `CRITICAL`, significant handoff,
audits, or any case where separation improves verification.

### 3.5 Evaluation

The evaluation layer contains:

- conformance hard failures;
- seven quality metrics;
- execution and framework evaluation separation;
- independent handoff procedure;
- comparative beta validation protocol.

### 3.6 Version identity

A small manifest records exact versions, normative language, predecessor,
status, included contracts, and foundation provenance. Run records reference
the relevant manifest values.

## 4. Planes and ownership

| Plane | Owns | May change during a run? | Beta implementation |
|---|---|---:|---|
| Normative | specification, kernel, contracts, governance | No | versioned Markdown |
| Runtime | active context, decisions, plan, evidence, closure | Yes, within the run | compact or full records |
| Capability | specifications, adapters, permissions, utility | Usage state only | ledger; no catalog required |
| Evolution | evaluation, learning decisions, promotion, pruning | Only after closure | manual review records |

## 5. Context architecture

Runtime context is divided into:

- **active:** required for the current decision;
- **validated:** confirmed and current knowledge available for retrieval;
- **historical:** previous states and evidence outside active reasoning.

When evidence changes, the runtime records:

1. changed source;
2. affected claim;
3. affected context layers and decisions;
4. previous and new claim state;
5. risk and budget reassessment;
6. plan or gate invalidation.

The beta performs this dependency tracking manually. An automatic context graph
is deliberately excluded.

## 6. Gate architecture

Gates are conditions, not mandatory conversation turns.

| Gate | Evidence-based satisfaction | Explicit human satisfaction |
|---|---|---|
| Understanding | grounded context for authorized low-risk Level 1 work | ambiguity, `DEEP`, `CRITICAL`, Level 2/3, or handoff interpretation |
| Plan | compact executable internal plan for low-risk Level 1 work | material strategy, architecture, `DEEP`, `CRITICAL`, Level 2/3 |
| Permission | existing scoped authorization | new write, execute, network, secret, cost, publish, delete, or production authority |
| Risk | controls remove material exposure | responsible authority accepts residual material risk |
| Completion | actual evidence meets intent and contract | user acceptance only when the contract makes it a criterion |

## 7. Capability architecture

The beta does not require stored capabilities. When a capability is relevant,
the runtime records:

- canonical need;
- discovered implementation or native tool;
- provider/adapter identity;
- permissions and risk;
- selection or rejection reason;
- actual result and utility.

This is sufficient to test `DISCOVER → REUSE → COMPOSE → SYNTHESIZE` without
building a registry. A registry becomes justified only after real repeated
capabilities exist.

## 8. Translation architecture

Translations live outside the normative identity of the English source. Each
translation header contains:

```yaml
translation_of: SHAPING_THE_AXE_BRAIN_SPEC.md
source_version: 0.2.0-beta.2
normative_language: English
translation_language: <language>
synchronization_state: CURRENT | STALE | DRAFT
last_reviewed_source_version: <version>
```

A release MUST NOT label a translation `CURRENT` without a completed semantic
comparison against the declared source version. Disagreement is resolved in
favor of the canonical source and logged for translation repair.

No translation is required to start the beta.

## 9. Minimal file structure

```text
.
├── README.md
├── framework.yaml
├── SHAPING_THE_AXE_BRAIN_SPEC.md
├── ShapingTheAxe.md
├── COHERENCE_DIAGNOSIS.md
├── IMPLEMENTATION_PLAN.md
├── docs/
│   ├── architecture.md
│   ├── beta-architecture.md
│   ├── roadmap.md
│   └── state-model.md
├── templates/
│   ├── run-record.md
│   ├── context-brief.md
│   ├── implementation-plan.md
│   └── completion-report.md
├── evaluation/
│   ├── rubric.md
│   └── beta-validation-protocol.md
└── examples/
    └── ft_irc/
        └── README.md
```

The structure contains no empty capability, adapter, agent, MCP, translation,
or learning directories. Such directories are created only when a real
artifact exists.

## 10. What is indispensable for beta

- normative Brain Specification;
- conformant portable kernel;
- qualitative risk and budget selection;
- state and transition definitions;
- compact run record;
- full artifacts for deep work;
- version manifest and foundation provenance;
- updated rubric and beta comparison protocol;
- documentary correction of the closed reference case;
- rollback instructions.

## 11. What is recommended during beta validation

- at least one unfamiliar software case;
- at least one non-software case;
- a clean handoff on a `DEEP` execution;
- comparison against brainstorming and normal workflow;
- observations from more than one capable AI environment;
- explicit tracking of user interruptions and preventable rework.

These are validation activities, not additional runtime architecture.

## 12. What is postponed

- executable state engine;
- automatic agent delegation;
- custom MCP implementation;
- capability registry and discovery service;
- automatic context dependency graph;
- learning retention automation;
- metrics dashboard;
- provider-specific packaged adapters;
- translation artifacts;
- generated teaching material or book.

## 13. Explicitly out of scope

- runtime mutation of the core;
- automatic promotion to shared or core scope;
- hidden risk acceptance;
- automatic production, financial, publishing, or secret-bearing action;
- universal-effectiveness claims before multidomain evidence;
- repetition or reconstruction of the `ft_irc` audit;
- modification of the `ft_irc` fixture.

## 14. Rollback architecture

Operational rollback restores foundation `v0.1` or the most recent later stable
version as a complete package. It MUST NOT copy selected beta rules back into
`context-init v0.2`.

Analytical rollback compares:

- exact package identities;
- case inputs;
- run records;
- metric results;
- protocol, adapter, and environment differences;
- identified regression.

The foundation source archive remains byte-identical and its hash is retained
outside the beta's mutable files.

## 15. Architecture acceptance tests

The beta architecture passes initial structural validation when:

1. every normative rule has one semantic source;
2. the kernel does not contradict the specification;
3. every state used by a template is defined;
4. `MICRO` work can close without full artifact bureaucracy;
5. `DEEP` and `CRITICAL` work cannot bypass required gates;
6. a run records exact version identity;
7. learning cannot alter the active runtime or core;
8. provider details appear only as runtime/adapter metadata;
9. no postponed directory or executable mechanism is created;
10. the original foundation archive remains unchanged.

## PROPOSALS — NOT YET APPROVED

No additional beta component is proposed here. Optional future mechanisms and
their experiments are listed in the normative specification and remain outside
the implemented architecture.

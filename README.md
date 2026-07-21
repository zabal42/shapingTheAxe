# ShapingTheAxe

> Shape the decision before committing the cut.

ShapingTheAxe is a provider-independent, governed method for preparing,
deciding, executing, verifying, and learning from AI-assisted work with human
oversight. It aims to maximize justified result quality while using the
minimum total cost compatible with risk and the Definition of Done.

It is not a giant prompt, a mandatory questionnaire, a tool catalog, or an
autonomous replacement for human responsibility.

The current beta implements this method manually, through the STA Kernel,
without a CLI or automated orchestration. See [Architecture](#architecture)
for what is stable identity versus current implementation.

## Status

- **Framework:** `0.2.0-beta.2`
- **Brain Specification:** `0.2.0-beta.2`
- **Portable kernel:** `0.2.0-beta.2`
- **Status:** Beta under comparative validation
- **Normative language:** English
- **Normative semantic source:**
  [`SHAPING_THE_AXE_BRAIN_SPEC.md`](SHAPING_THE_AXE_BRAIN_SPEC.md)
- **Historical predecessor:** foundation `v0.1`, containing
  `context-init v0.2`
- **Version history:** [`CHANGELOG.md`](CHANGELOG.md)

Foundation `v0.1` remains immutable and separately versioned. This beta is a
new protocol line; it does not silently rewrite the predecessor.

## Architecture

ShapingTheAxe separates four conceptual planes and one execution mechanism.

- **Brain Specification** — semantic authority. Defines vision, universal
  laws, and governance. Stable regardless of implementation.
- **STA Kernel** — the compact, portable operational form of the Brain
  Specification.
- **Runtime Plane** — the state of one task execution: classification, active
  context, claims, decisions, gates, plan, evidence, and closure. Temporary or
  project-scoped, not the core.
- **Capability Plane** — canonical capability specifications, discovered on
  demand under `DISCOVER → REUSE → COMPOSE → SYNTHESIZE`.
- **Evolution Plane** — reviews closed-run evidence and proposes retention,
  pruning, or promotion after closure. Cannot alter an active run.
- **STA Execution Engine** — the future mechanism intended to perform the
  operational cycle, own orchestration, and produce Runtime Plane state
  automatically. It is not a fifth plane; it is how the four planes would be
  executed by an automated system.

The current reference implementation performs this role manually: a capable
AI environment follows the STA Kernel by hand. Automated orchestration,
executable skills, a CLI runner, and MCP coordination are governed future
capabilities, not yet approved — see [Evolution path](#evolution-path).

Two adapter concepts describe how providers and capabilities connect to
ShapingTheAxe, kept separately scoped:

- **STA Environment Adapters** — route a specific AI tool or CLI (Claude
  Code, Codex, Copilot) into the STA Kernel. Implemented today as the stubs
  in `adapters/`.
- **STA Capability Adapters** — implement a canonical capability
  specification for a specific provider or tool. Not yet built; defined
  normatively in the Brain Specification.

The boundary between the two is still open and tracked as a known
terminological debt, not resolved by this naming pass.

## What changed from foundation `v0.1`

- six context layers replace five fixed uncertainty sources as the canonical
  model;
- qualitative risk selects `MICRO`, `STANDARD`, `DEEP`, or `CRITICAL` effort;
- human gates depend on materiality and decision authority;
- the artificial five-percent threshold is removed;
- compact records are allowed for small work while full artifacts remain;
- capability selection, deferred learning, privacy, versioning, and rollback
  now have explicit contracts;
- the Brain Specification and operational kernel have separate roles.

See [`COHERENCE_DIAGNOSIS.md`](COHERENCE_DIAGNOSIS.md) for the complete
migration rationale.

## Quick start

1. Give a capable AI environment access to
   [`ShapingTheAxe.md`](ShapingTheAxe.md).
2. Supply the task and relevant artifacts.
3. State the intervention you authorize: investigate, recommend, plan, modify,
   execute, validate, audit, evaluate, or full cycle.
4. Tell it: `Follow ShapingTheAxe.md for this task.`
5. Let the kernel choose the minimum sufficient budget and gates.

For small work, use [`templates/run-record.md`](templates/run-record.md). For
deep work or handoff, use the separate context brief, implementation plan, and
completion report.

## Operating model

The cycle below is what the current reference implementation performs by
hand — the role a future STA Execution Engine is intended to automate.

1. Classify task, authority, risk, and budget.
2. Design inspection around decision-changing claims.
3. Inspect before asking.
4. Detect and control gaps and contradictions.
5. Satisfy the understanding and plan gates required by risk.
6. Execute inside approved scope and permissions.
7. Verify with proportional independence.
8. Close with evidence and defer learning decisions until after runtime.

## Repository structure

```text
.
├── README.md
├── CHANGELOG.md
├── CLAUDE.md                      # self-activation for Claude Code
├── AGENTS.md                      # self-activation for Codex and compatible tools
├── framework.yaml                 # exact version manifest
├── SHAPING_THE_AXE_BRAIN_SPEC.md  # semantic authority
├── ShapingTheAxe.md                # portable operational kernel
├── COHERENCE_DIAGNOSIS.md          # historical: v0.1 -> beta migration rationale
├── IMPLEMENTATION_PLAN.md          # historical: beta.1 construction record
├── START_HERE.md                   # 30-second onboarding
├── docs/
│   ├── architecture.md
│   ├── beta-architecture.md
│   ├── roadmap.md
│   ├── state-model.md
│   ├── validation-history.md
│   └── skill-candidate-decision.md
├── templates/
│   ├── run-record.md
│   ├── context-brief.md
│   ├── implementation-plan.md
│   └── completion-report.md
├── evaluation/
│   ├── rubric.md
│   ├── beta-validation-protocol.md
│   └── testing-strategy-incubation-protocol.md
├── prompts/
│   └── activate.md                 # copy-paste universal activation prompt
├── adapters/                       # routing stubs for CLAUDE.md/AGENTS.md/Copilot
│   ├── CLAUDE.stub.md
│   ├── AGENTS.stub.md
│   └── copilot-instructions.stub.md
├── translations/
│   └── es/START_HERE.md            # synchronized Spanish onboarding
├── incubator/
│   └── testing-strategy/           # SKILL.md under controlled incubation only
├── examples/
│   └── ft_irc/
│       └── README.md               # frozen historical reference case
├── business/                       # product exploration — non-normative
│   ├── VISION.md
│   ├── ELDORADO_HYPOTHESIS.md
│   ├── STA_ASSISTANTS_FOUNDATION.md
│   ├── PRODUCT_HYPOTHESES.md
│   ├── BUSINESS_MODELS.md
│   ├── MVP_VALIDATION.md
│   └── DECISIONS.md
└── validation/
    └── case-studies/
        └── crossfit-business-copilot/  # frozen blind-evaluation lab evidence
```

`business/` holds product exploration, not framework behavior — see
[`business/README.md`](business/README.md). `validation/` holds frozen
comparative evidence — nothing there is re-run or reconstructed.

## Reference evidence

The historical `ft_irc` case is closed with `91.3/100`, verdict `PASS`, no hard
failure, and a successful independent handoff. It is not Reference-grade. The
audit is frozen and must not be repeated or reconstructed from this package.
See [`examples/ft_irc/README.md`](examples/ft_irc/README.md).

The `crossfit-business-copilot` case is a closed comparative laboratory: two
independent implementations built from the same frozen input, evaluated blind
by three independent evaluators who converged on the same ranking. It is
positive multidomain beta evidence, not proof of universal effectiveness. See
[`validation/case-studies/crossfit-business-copilot/README.md`](validation/case-studies/crossfit-business-copilot/README.md).

## Validation

The beta is evaluated on:

1. correctness;
2. efficiency;
3. traceability;
4. useful autonomy;
5. escalation quality;
6. portability;
7. clean learning.

Use [`evaluation/rubric.md`](evaluation/rubric.md) for an individual run and
[`evaluation/beta-validation-protocol.md`](evaluation/beta-validation-protocol.md)
for comparisons with brainstorming and normal workflows.

## Current exclusions

These describe the beta's current reference implementation — which manually
performs the role a future STA Execution Engine will automate — not a
permanent limit on the architecture. See [Evolution path](#evolution-path).

The beta deliberately excludes, per `SHAPING_THE_AXE_BRAIN_SPEC.md` §13.3:

- a CLI;
- automatic multi-agent orchestration;
- custom MCP servers;
- automated learning or core updates;
- a large capability catalog;
- production authority;
- claims of universal effectiveness;
- a generated book.

`docs/architecture.md` records additional current non-goals at the
architecture-documentation level (provider-specific packaged adapters,
translated releases before synchronization review, automatic context graph,
capability registry).

## Evolution path

The beta's current exclusions are a state of evidence, not a ceiling on what
ShapingTheAxe can become. Proposals for building the STA Execution Engine are
recorded, gated, and evaluated before approval:

- a CLI runner for repeatable kernel activation;
- automated multi-agent orchestration;
- automated capability synthesis, including executable skills;
- STA Capability Adapters for MCP coordination;
- an automated learning pipeline.

Each proposal defines its problem, benefit, cost, risk, core impact, and
validating experiment before implementation — see
`PROPOSALS — NOT YET APPROVED` in
[`SHAPING_THE_AXE_BRAIN_SPEC.md`](SHAPING_THE_AXE_BRAIN_SPEC.md) and the
deferred-proposals list in [`docs/roadmap.md`](docs/roadmap.md). None of them
is a beta requirement, and none is implemented today.

## Translation policy

The canonical source is English. A translation must declare its canonical
source version and synchronization state. If a translation disagrees with the
canonical specification, the English specification governs until the
translation is corrected.

## Rollback

Operational rollback restores foundation `v0.1` or another complete stable
package. Analytical rollback compares exact versions, inputs, run evidence,
and evaluation results to locate a regression. Never copy selected beta rules
back into the historical protocol.


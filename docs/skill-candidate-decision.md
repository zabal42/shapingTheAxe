# Skill Candidate Decision Record

**Decision ID:** `STA-DEC-SKILLS-001`
**Status:** `APPROVED — CLASSIFICATION ONLY`
**Date:** 2026-07-14
**Applies to:** ShapingTheAxe `0.2.0-beta.1`
**Proposed repository location:** `docs/skill-candidate-decision.md`
**Semantic authority:** `SHAPING_THE_AXE_BRAIN_SPEC.md`

## 1. Purpose and authority boundary

This record decides how the skills supplied in `skills.zip` are classified for
the ShapingTheAxe beta. It does not install, adapt, activate, or promote any
skill. It does not modify the core, the portable kernel, the foundation v0.1,
or the beta capability model.

If this record conflicts with `SHAPING_THE_AXE_BRAIN_SPEC.md`, the Brain
Specification prevails. The archive under review is identified by:

```text
skills.zip sha256:
b2ddf2e68fce12baf64ff39ca43b2e44489494e75868bbf74e873e1535a1da1b
```

Capability availability is never authority to activate it. A skill cannot
grant itself permissions; every activation inherits only the permissions
already authorized for the active task and remains subject to the Brain's
risk, budget, decision-level, and gate rules.

## 2. Approved decisions

1. `brainstorming` is frozen exclusively as an experimental comparator. It is
   not an operational capability and is not eligible for promotion.
2. `testing-strategy` is the only candidate authorized for immediate
   incubation. Incubation means design and controlled evaluation, not
   installation or activation.
3. `github-actions-docs` is an external conditional candidate. It will not be
   incorporated or adapted unless a real case demonstrates a need not
   efficiently satisfied by the Brain and ordinary authoritative-source
   inspection.
4. No Prisma skill will be consolidated during this beta. Prisma is registered
   as a live-documentation-, version-, runtime-, and provider-dependent domain
   outside the beta capability set.
5. Every other supplied skill is postponed, archived, rejected, or quarantined
   according to Section 8.
6. No supplied skill is installed, modified, or added to the ShapingTheAxe
   repository by this decision.

## 3. Portfolio boundaries

| Track | Item | Classification | May activate now? |
|---|---|---|---:|
| Experimental control | `brainstorming` | Frozen comparator | No, except controlled comparison |
| Immediate incubation | `testing-strategy` | `PROJECT` / `CANDIDATE` design target | No |
| External conditional | `github-actions-docs` | Not admitted to lifecycle | No |
| Excluded domain | Prisma | Live-source-dependent; outside beta | No |

The classifications `POSTPONED`, `REJECTED`, and `QUARANTINED` used in this
record are review dispositions, not additions to the canonical capability
lifecycle. Items actually admitted to the framework must use the lifecycle in
the Brain Specification.

## 4. Frozen experimental comparator: `brainstorming`

**Candidate status:** Not a candidate. Experimental control only.
**Frozen `SKILL.md` sha256:**
`e14914605f640e0841758e45d0ab2a53243b59b921f929e47921c99668f2e61d`

### Need covered

Provides a stable external workflow against which ShapingTheAxe can be tested
on option expansion, design clarification, user interruption, preparation
cost, and solution quality.

### Why the Brain does not already cover the need

The Brain already covers the operational need for understanding, option
selection, planning, and adaptive gates. It does not provide its own
independent experimental control; using a frozen external comparator avoids
evaluating the Brain only against itself.

### Scope

- Controlled beta comparisons only.
- Frozen equivalent inputs and recorded execution conditions.
- Separate attribution of protocol, model, adapter, fixture, environment, and
  capability effects.
- No use as the default workflow for real ShapingTheAxe tasks.

### Activation

Activate only when an approved validation case explicitly compares
ShapingTheAxe, the frozen brainstorming workflow, and the normal workflow. It
must not trigger merely because a task is creative, ambiguous, architectural,
or involves planning.

### Permissions

- Read the frozen comparator and experiment inputs.
- Write only experiment outputs in the isolated evaluation workspace when the
  evaluation itself is authorized.
- No installation, core write, publication, secrets, production action, or
  implicit network access.
- Any extra permission must be identical across comparison arms or recorded as
  an experimental limitation.

### Risks

- Accidental operational use.
- Contamination from prior runs.
- Moving-target comparison.
- Unequal permissions, context, tools, or time between experimental arms.
- Mistaking verbosity or user interruption for quality.

### Authoritative sources

1. `SHAPING_THE_AXE_BRAIN_SPEC.md`, especially its validation rules.
2. `evaluation/beta-validation-protocol.md`.
3. The frozen archive and hash recorded above.
4. The approved input, environment record, and evidence for each experiment.

The comparator's claims are not semantic authority over ShapingTheAxe.

### Update strategy

None. The comparator remains byte-stable. A changed comparator must receive a
new identity, version, hash, and experimental series; it must never silently
replace this control.

### Promotion criterion

None by design. It cannot become `ACTIVE`, `SHARED`, `CORE_CANDIDATE`, or
`CORE` through this track.

### Discard criterion

Stop using it in new experiments if its bytes cannot be verified, its required
runtime cannot be reproduced fairly, or a later approved validation protocol
replaces the comparator. Preserve the frozen artifact and historical results
for traceability.

## 5. Immediate incubation candidate: `testing-strategy`

**Lifecycle target:** `PROJECT` / `CANDIDATE`
**Source material:** supplied `test-driven-development`, retained as
non-authoritative input
**Source `SKILL.md` sha256:**
`b5b4717b8b761cce15a6cfe9022e33fd959e0894c0c39d72c9cb49c23486c10e`

### Need covered

Translate a software task's acceptance criteria and material risks into the
minimum sufficient test strategy: what evidence is needed, which test level is
appropriate, when reproduction or test-first work is valuable, what commands
to run, and what remains unverified.

### Why the Brain does not already cover the need

The Brain requires proportionate verification and evidence, but deliberately
does not encode software-testing technique. It does not decide between
regression-first, characterization, unit, integration, end-to-end, manual,
static, or existing-suite validation for a concrete codebase.

### Scope

- Software features, defect fixes, behavior-changing configuration, and
  refactors with regression risk.
- Selection of a testing posture based on risk, feasibility, and project
  conventions.
- Mapping material behaviors and failure modes to reproducible evidence.
- Recording skipped tests, environmental blocks, residual risk, and confidence
  limits without inventing percentages.
- Prefer a failing regression reproduction before a defect fix when feasible
  and valuable; never make that a universal ritual.

Out of scope:

- Documentation-only or editorial work with no executable behavior.
- Replacing the project's requirements, acceptance criteria, CI policy, or
  testing framework.
- Production experiments, destructive database tests, load tests against
  shared systems, security testing, or external-service calls without separate
  authority.
- Universal requirements that every function have a test or that existing code
  be deleted because it was not written test-first.

### Activation

Activate only when at least one of these conditions holds:

- the task changes observable software behavior;
- a defect needs reproducible confirmation and regression protection;
- a refactor has material regression risk;
- the user explicitly requests a test strategy or test implementation;
- the selected budget requires software-specific verification beyond the
  Brain's general validation contract.

Do not activate for generic planning, read-only explanation, documentation-only
changes, or when the repository's existing test instructions already answer
the question with no material gap.

Budget adaptation:

| Budget | Minimum testing posture |
|---|---|
| `MICRO` | Focused existing check or smallest useful proof; add a test only when recurrence or ambiguity justifies it. |
| `STANDARD` | Explicit targeted strategy; defects normally get a regression reproduction when feasible; run the relevant suite. |
| `DEEP` | Risk-to-evidence test plan covering important boundaries and integration points, plus cross-verification or clean handoff. |
| `CRITICAL` | Explicit authority, isolated or production-like validation, rollback controls, complete evidence, and independent evaluation. |

### Permissions

Default incubation permission is read-only analysis.

When the active task separately authorizes implementation:

- `read`: repository, requirements, test code, configuration, and local logs;
- `write`: only scoped test files, fixtures, and implementation files already
  authorized by the task;
- `execute`: non-destructive local build, test, lint, and analysis commands;
- `install`: denied by default; requires an explicit dependency decision;
- `delete`: denied except scoped reversible cleanup explicitly approved;
- `use network`: denied by default; live official documentation may be read
  when version-sensitive information is material;
- `access secrets`, `spend money`, `publish`, `act on production`: denied by
  default and never implied by activation.

Test execution must prefer isolated fixtures and disposable local state. A
skill cannot expand the outer task's permission envelope.

### Risks

- Reintroducing TDD as a universal gate and violating proportionality.
- Testing implementation details instead of required behavior.
- Locking in accidental legacy behavior through characterization tests.
- False confidence from mocks, snapshots, coverage figures, or a green partial
  suite.
- Flaky, slow, destructive, or environment-dependent tests.
- Excessive context, ceremony, test volume, or maintenance cost.
- Exposure of secrets or private data through fixtures and logs.
- Treating an unavailable environment as proof that behavior is correct.

### Authoritative sources

Use claim-domain authority in this order:

1. `SHAPING_THE_AXE_BRAIN_SPEC.md` for risk, budget, gates, permissions,
   lifecycle, and evidence rules.
2. The active task's approved requirements, subject, acceptance criteria, and
   human decisions for intended behavior.
3. The current repository, build system, existing tests, CI configuration, and
   observed runtime behavior for executable reality.
4. Official documentation matching the detected language, framework, test
   runner, and dependency versions.
5. Reproducible execution evidence from the current environment.

The supplied `test-driven-development` skill is design input, not authority.

### Update strategy

- Keep the core strategy provider- and framework-independent.
- Load framework-specific commands and semantics from the current repository
  and live official documentation only when needed.
- Record relevant tool versions and invalidate affected guidance when they
  change.
- Review false activations, skipped evidence, runtime cost, and defects escaped
  after every incubation case.
- Revise the candidate only between cases; never let it rewrite itself or
  become authority during an active run.

### Promotion criterion

Promotion from `CANDIDATE` to project `ACTIVE` requires an approved review with
evidence that:

- it improved a real bounded defect case and a non-defect behavior-change case;
- it selected different testing depth when risk or budget differed;
- it added no unnecessary universal gate;
- its evidence was reproducible and distinguished verified, blocked, and
  residual-risk claims;
- its activation and permission boundaries were respected;
- its value exceeded using the Brain plus existing project instructions alone.

Promotion to `SHARED` requires later use in an independent project or stack,
evidence of portability, and explicit approval. `CORE_CANDIDATE` and `CORE`
remain outside this decision and require the Brain's multidomain and independent
evaluation rules.

### Discard criterion

Discard or archive the candidate if it repeatedly:

- duplicates the Brain or project instructions without improving evidence;
- triggers on tasks that do not need software-specific testing strategy;
- adds disproportionate ceremony or context cost;
- pushes test-first work when reproduction is infeasible or low-value;
- encourages unsafe execution or permission expansion;
- depends on stale framework-specific knowledge that cannot be maintained; or
- fails to reduce relevant uncertainty, regression risk, or handoff ambiguity.

### Expected output and stop conditions

The candidate should return a compact testing decision containing selected
posture, behaviors covered, commands or checks, permissions, evidence, blocks,
and residual risk. It stops when the task's Definition of Done is sufficiently
verified for the current budget, or when missing authority/environment makes
further testing unsafe or non-material.

## 6. External conditional candidate: `github-actions-docs`

**Current status:** Not admitted; no adaptation authorized
**Potential future lifecycle entry:** `PROJECT` / `CANDIDATE`
**Supplied `SKILL.md` sha256:**
`85f3e313505340d09f6c5706aac096a29ff30a0ef11c04ce7a466a57175df33f`

### Need covered

Route a real GitHub Actions question to current authoritative documentation
without loading a large static manual or relying on model memory.

### Why the Brain does not already cover the need

The Brain defines how to discover and evaluate authoritative sources, but it
does not contain a GitHub Actions topic taxonomy, product-specific search
routes, workflow syntax, event semantics, permission behavior, or runner
constraints.

This gap is not yet proven to require a dedicated skill; ordinary Brain-guided
inspection may already be sufficient.

### Scope

- Public documentation discovery and routing for GitHub Actions.
- Interpretation grounded in the repository's workflows and applicable GitHub
  documentation.
- No workflow modification, dispatch, cancellation, rerun, secret access,
  repository mutation, or publication.
- No assumption that adjacent GitHub, CodeQL, Dependabot, or CI-repair skills
  exist.

### Activation

No activation during the current beta. Reconsider only when a real GitHub
Actions case demonstrates repeated retrieval friction, incorrect routing, or
material context cost that the Brain plus direct official-documentation access
does not solve efficiently.

A future candidate must trigger only for GitHub Actions-specific questions,
not for generic GitHub, Git, CI/CD, YAML, or repository work.

### Permissions

Potential read-only candidate permissions:

- read relevant workflow files and public repository configuration;
- use network access limited to authoritative public documentation needed by
  the active question.

No write, execute, install, delete, publish, secret, spending, authenticated
GitHub, workflow-control, or production permission. Any later operational
action requires a separate capability decision and the active task's authority.

### Risks

- Stale routes, renamed products, or changed workflow semantics.
- Treating documentation as proof of the repository's actual state.
- Confusing GitHub-hosted and self-hosted runner constraints.
- Following third-party action documentation without checking publisher,
  version pinning, and supply-chain risk.
- Accidental expansion from documentation lookup into authenticated operations.
- Duplicating ordinary web/documentation retrieval with no material benefit.

### Authoritative sources

1. The active repository's workflow files, organization policies, and observed
   run evidence for current executable reality.
2. [GitHub Actions documentation](https://docs.github.com/actions).
3. GitHub's official changelog and security documentation when relevant.
4. The verified publisher documentation and pinned version source for any
   third-party action.
5. `SHAPING_THE_AXE_BRAIN_SPEC.md` for selection, permission, and evidence
   rules.

### Update strategy

- Prefer a small routing map over copied documentation.
- Validate target routes at activation time.
- Record access date, product context, and material version assumptions.
- Refresh only when a real case, broken route, changed GitHub behavior, or
  validation failure justifies it.
- Never turn cached documentation into higher authority than the live official
  source or repository evidence.

### Promotion criterion

Admission to `PROJECT` / `CANDIDATE` requires a documented real case showing
that the candidate:

- resolves a recurring GitHub Actions retrieval need;
- outperforms direct Brain-guided official-source inspection in useful cost or
  correctness;
- triggers precisely and remains read-only;
- has no unresolved dependency on absent skills; and
- produces traceable answers grounded in the repository and official sources.

Any promotion beyond project scope follows the canonical lifecycle and requires
new approval.

### Discard criterion

Reject the candidate if no real need emerges, direct source inspection is
sufficient, its routes become costly to maintain, it frequently misfires, or
it requires authenticated operational permissions to provide its claimed
documentation value.

## 7. Prisma domain register

**Status:** Outside beta; no consolidated skill
**Domain property:** Live-documentation-, version-, runtime-, database-, and
provider-dependent

### Need covered

Future Prisma work may need current guidance for ORM configuration, Client,
CLI, migrations, database adapters, Prisma Postgres, or Compute.

### Why the Brain does not already cover the need

The Brain can select and inspect sources but does not encode Prisma's changing
CLI, generated-client contract, migration semantics, provider APIs, or runtime
compatibility. That does not yet justify adding a Prisma capability to the
beta.

### Scope

No operational scope is admitted now. A future proposal must begin from a real
project and explicitly identify:

- installed Prisma and client versions;
- runtime and module system;
- database and driver adapter;
- provider and deployment target;
- development, CI, staging, or production environment;
- whether the task is read-only, schema-changing, data-changing, or
  infrastructure-changing.

### Activation

None during the beta. A Prisma-related task must use the Brain's normal
authoritative-source workflow without activating any supplied Prisma skill.

### Permissions

None granted by this register. Any future design must keep documentation lookup
separate from package installation, file writes, command execution, migration,
network access, secret access, cloud resource creation, destructive database
operations, spending, and production action.

### Risks

- Version drift and contradictory static instructions.
- Provider-specific guidance presented as universal Prisma behavior.
- Destructive migration, reset, push, raw SQL, or cloud deletion.
- Credentials copied into prompts, logs, fixtures, or shared learning.
- Unintended package, schema, generated-client, database, or infrastructure
  changes.
- Confusion between Prisma ORM, Prisma Postgres, Compute, Accelerate, and
  third-party database providers.

### Authoritative sources

1. The active project's package lockfile, Prisma schema, `prisma.config.*`,
   generated-client configuration, environment policy, and observed behavior.
2. [Prisma releases](https://github.com/prisma/prisma/releases).
3. [Prisma ORM documentation](https://www.prisma.io/docs/orm).
4. The official documentation for the detected database, driver adapter,
   provider, and deployment product.
5. The applicable human-approved migration and production policies.

The supplied Prisma skills are non-authoritative review material.

### Update strategy

Resolve live documentation and local CLI help at task time, record detected
versions and provider, and invalidate instructions when those facts change.
Do not maintain a broad static Prisma manual inside ShapingTheAxe.

### Promotion criterion

No promotion during this beta. A later explicit decision may admit a narrowly
scoped candidate only after a real case proves need, sources are current, the
version/provider matrix is explicit, trigger overlap is removed, and every
destructive or sensitive action has a permission and rollback contract.

### Discard criterion

Keep the domain outside the capability set if direct live-source inspection is
sufficient, no recurring project need exists, or a reliable and bounded
version/provider contract cannot be maintained.

## 8. Disposition of every supplied skill

| Supplied skill | Review disposition | Retention and activation rule |
|---|---|---|
| `brainstorming` | Frozen comparator | Retain immutable; experimental comparison only. |
| `test-driven-development` | Archived source input | May inform `testing-strategy`; never install or activate as supplied. |
| `writing-plans` | Archived | Retain only for provenance; Brain planning contract prevails. |
| `subagent-driven-development` | Postponed | Reconsider only under a later approval of Proposal P-03; no beta orchestration. |
| `github-actions-docs` | External conditional candidate | No adaptation until a real case passes Section 6 admission criteria. |
| `find-skills` | Rejected | Do not retain as an activatable candidate; discovery by popularity or global install is not accepted. |
| `nodejs-backend-patterns` | Rejected | Replace, if ever needed, with project-grounded architecture guidance. |
| `prisma-cli` | Archived / outside beta | Non-authoritative source material only. |
| `prisma-client-api` | Archived / outside beta | Non-authoritative source material only. |
| `prisma-database-setup` | Archived / outside beta | Non-authoritative source material only. |
| `prisma-postgres` | Postponed / outside beta | Reconsider only for a real Prisma Postgres project. |
| `prisma-postgres-setup` | Quarantined | No activation; secrets, cloud writes, migration, and destructive paths require redesign. |
| `prisma-compute` | Postponed / outside beta | Reconsider only for a real Compute deployment case. |
| `prisma-driver-adapter-implementation` | Archived / outside beta | Niche source material; require an actual adapter implementation case. |

`QUARANTINED` means inspection-only retention. It forbids activation, execution,
copying credentials, and reuse of operational instructions.

## 9. Incubation evidence record for `testing-strategy`

Each controlled case should record proportionately:

- task and repository snapshot;
- risk and preparation budget;
- reason for activation;
- authoritative requirements and detected test stack;
- permissions granted and denied;
- selected testing posture and rejected alternatives;
- tests or checks executed and their exact outcomes;
- evidence unavailable or blocked;
- context, time, and maintenance cost observations;
- comparison with the Brain plus ordinary project instructions;
- false activation, unnecessary gate, or unsafe recommendation;
- retention, revision, promotion, or discard recommendation.

The candidate must not modify itself during the evaluated run. Learning review
happens only after closure.

## 10. Current non-actions

This decision explicitly does not authorize:

- creating a `testing-strategy/SKILL.md`;
- editing any supplied skill;
- installing or globally registering any skill;
- adding a capability catalog to the beta;
- adding CLI, MCP, automated agents, or automated learning;
- changing `SHAPING_THE_AXE_BRAIN_SPEC.md`, `ShapingTheAxe.md`, or foundation
  v0.1;
- adding this document to the repository without a separate repository-change
  instruction.

## PROPOSALS — NOT YET APPROVED

The following implementation actions remain unapproved:

1. Draft the actual provider-independent `testing-strategy` skill.
2. Define its first controlled incubation cases and evaluator.
3. Add this decision record to `docs/` in the repository.
4. Adapt `github-actions-docs` after a qualifying real case.
5. Design any Prisma capability after the beta and a qualifying real case.

Approval of this record's classification does not implicitly approve any item
above.

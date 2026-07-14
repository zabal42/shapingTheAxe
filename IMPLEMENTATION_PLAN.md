# ShapingTheAxe Beta Implementation Plan

**Target:** `0.2.0-beta.1`  
**Status:** Authorized  
**Authorization:** User confirmed the nine architecture decisions, required the
design artifacts before framework modification, and authorized execution.  
**Intervention mode:** `FULL_CYCLE` for documentary framework construction  
**Budget:** `DEEP`

## 1. Outcome

Produce a minimal, manually usable, provider-independent ShapingTheAxe beta
that:

- preserves foundation `v0.1` unchanged;
- establishes a new normative Brain Specification;
- supplies a conformant portable kernel;
- formalizes risk, budgets, gates, and state transitions;
- supports compact and full execution records;
- aligns evaluation with the seven approved metrics;
- records the closed `ft_irc` status without repeating the audit;
- excludes premature automation.

## 2. Approved boundaries

### In scope

- specification, diagnosis, state model, beta architecture;
- implementation and validation plans;
- portable Markdown kernel;
- compact run record and aligned full templates;
- framework metadata and documentation;
- conformance rubric and comparative beta protocol;
- documentary `ft_irc` status update;
- versioned release package and rollback provenance.

### Out of scope

- CLI;
- automatic agent orchestration;
- custom MCP servers;
- automated learning;
- capability catalog;
- provider-specific executable adapter;
- translation artifact;
- audit or fixture modification;
- claims of multidomain validation before experiments run.

## 3. Implementation sequence

The design contracts are created and checked first. Only then is the historical
foundation copied into a new beta line and updated. This prevents edits from
driving the architecture and preserves a clean rollback boundary.

## 4. Executable tasks

### Task 1 — Freeze provenance

- **Objective:** Establish immutable identity for the supplied foundation.
- **Reason:** The new beta must not silently rewrite its predecessor.
- **Expected output:** Source archive hash, predecessor version, and rollback
  identity recorded in beta metadata.
- **Verification:** Recalculate SHA-256 before and after beta construction;
  compare for exact equality.
- **Stop condition:** Stop if the source archive is corrupt, changes identity,
  or cannot be read completely.
- **Dependencies:** None.

### Task 2 — Create the normative Brain Specification

- **Objective:** Consolidate approved decisions into one semantic authority.
- **Reason:** The foundation kernel and the approved Brain contain material
  behavioral conflicts.
- **Expected output:** `SHAPING_THE_AXE_BRAIN_SPEC.md` with the fourteen
  required sections and a separate proposals section.
- **Verification:** Check required headings, approved decisions, normative
  language declaration, beta exclusions, and absence of provider dependence.
- **Stop condition:** Stop if an unapproved structural proposal is required to
  express an approved decision.
- **Dependencies:** Task 1 source identity.

### Task 3 — Produce design and diagnostic contracts

- **Objective:** Make contradictions, state behavior, architecture, and
  implementation reasoning independently inspectable.
- **Reason:** The kernel must be derived from explicit architecture rather than
  becoming a new giant prompt.
- **Expected output:**
  `COHERENCE_DIAGNOSIS.md`, `docs/state-model.md`,
  `docs/beta-architecture.md`, this plan, and
  `evaluation/beta-validation-protocol.md`.
- **Verification:** Cross-check terminology, enums, gates, scope tiers, and all
  requested plan fields.
- **Stop condition:** Stop if two documents assign different meaning to a
  normative state or authority rule.
- **Dependencies:** Task 2.

### Task 4 — Derive the beta package

- **Objective:** Create a new version from the foundation without mutating the
  historical archive.
- **Reason:** Version separation and rollback are approved invariants.
- **Expected output:** A distinct `0.2.0-beta.1` framework tree containing the
  original useful files plus the new design contracts.
- **Verification:** Confirm all foundation members have a corresponding beta
  successor or an explicit replacement; confirm the original archive hash is
  unchanged.
- **Stop condition:** Stop if the construction process writes to the supplied
  archive or loses predecessor provenance.
- **Dependencies:** Tasks 1–3.

### Task 5 — Replace the operational kernel

- **Objective:** Convert the Brain Specification into a compact executable
  protocol.
- **Reason:** `context-init v0.2` contains superseded absolute rules.
- **Expected output:** New `ShapingTheAxe.md` implementing proportional
  classification, inspection, gates, execution, recovery, verification, and
  closure.
- **Verification:** Search for prohibited legacy rules such as the five-percent
  threshold, fixed five-source invariant, universal approval, and “ask on any
  uncertainty”; map every kernel phase to the Brain Specification.
- **Stop condition:** Stop if portability requires provider-specific commands
  or the kernel introduces a rule absent from the specification.
- **Dependencies:** Tasks 2–4.

### Task 6 — Align artifact contracts

- **Objective:** Support both compact and full traceability with canonical
  states.
- **Reason:** Full artifacts remain valuable, but they are excessive for every
  low-risk execution.
- **Expected output:** New `templates/run-record.md` and updated context brief,
  implementation plan, and completion report.
- **Verification:** Confirm all used states exist in `docs/state-model.md`, all
  six context layers appear, gates distinguish evidence from approval, actual
  verification is required, and all four terminal statuses are available.
- **Stop condition:** Stop if compact mode can bypass a material gate or full
  mode becomes mandatory for `MICRO`.
- **Dependencies:** Tasks 3 and 5.

### Task 7 — Align framework documentation and metadata

- **Objective:** Remove stale claims and make normative/version boundaries
  obvious.
- **Reason:** The foundation README, architecture, roadmap, and reference case
  describe an earlier state.
- **Expected output:** Updated `README.md`, `framework.yaml`,
  `docs/architecture.md`, `docs/roadmap.md`, and
  `examples/ft_irc/README.md`.
- **Verification:** Confirm the Brain Spec is named as normative, English and
  translation rules are explicit, `ft_irc` is closed but not Reference-grade,
  no missing evidence file is fabricated, and exclusions remain visible.
- **Stop condition:** Stop if documentary updates require reconstructing frozen
  evidence not present in the package.
- **Dependencies:** Tasks 4–6.

### Task 8 — Update evaluation

- **Objective:** Evaluate the new protocol rather than the predecessor.
- **Reason:** The old rubric hard-fails behavior that is now valid for low-risk
  autonomous work and does not measure all seven metrics.
- **Expected output:** Revised `evaluation/rubric.md` plus the comparative beta
  protocol.
- **Verification:** Confirm conformance and quality remain distinct; scoring is
  evidence-anchored; independent verdict rules remain; all seven metrics are
  operationalized; compact records are valid for appropriate budgets.
- **Stop condition:** Stop if scoring rewards document volume, question count,
  or unsupported precision.
- **Dependencies:** Tasks 2, 3, 5, and 6.

### Task 9 — Structural and semantic verification

- **Objective:** Demonstrate internal package coherence before release.
- **Reason:** A documentation framework can fail through broken links,
  contradictory enums, stale versions, or normative duplication.
- **Expected output:** Verification log and corrected beta files.
- **Verification:**
  - list and inspect all files;
  - test relative Markdown links;
  - compare state tokens across specification, kernel, templates, and rubric;
  - scan for stale `5%`, universal-gate, pending-`ft_irc`, and provider-specific
    claims;
  - verify no empty ornamental directories;
  - verify source archive hash;
  - inspect archive contents after packaging.
- **Stop condition:** Stop release for any broken normative link, state conflict,
  source mutation, fabricated case evidence, or beta-exclusion violation.
- **Dependencies:** Tasks 4–8.

### Task 10 — Package and hand off

- **Objective:** Deliver a usable, reproducible beta and its preserved
  predecessor.
- **Reason:** The user must be able to inspect, test, and roll back without the
  original conversation.
- **Expected output:** Versioned beta archive, retained design files, checksums,
  and concise handoff.
- **Verification:** Extract the final archive in a temporary location, rerun
  structural checks, and compare included checksums.
- **Stop condition:** Stop if the package is incomplete, unreproducible, or
  cannot be opened independently.
- **Dependencies:** Task 9.

## 5. Verification strategy

| Level | What it proves | Method | Expected evidence |
|---|---|---|---|
| Structural | Package completeness and link integrity | file inventory and link checker | no missing required file or local link |
| Semantic | One meaning per normative concept | enum and phrase cross-check | no contradictory state or gate definition |
| Historical | Foundation is preserved | SHA-256 comparison | identical source hash |
| Scope | Excluded automation is absent | file and content scan | no CLI, agent runtime, MCP, or learning executor |
| Operational | Kernel can drive a manual run | dry-run against a synthetic `MICRO` capsule | valid compact record without universal gates |
| Safety | High-risk work cannot bypass gates | dry-run of a synthetic `CRITICAL` capsule | explicit user and independent evaluation requirements |
| Evaluation | Seven metrics are measurable | rubric/protocol inspection | anchored evidence fields for each metric |

Synthetic checks validate contracts only. They do not count as beta outcome
evidence or replace the comparative protocol.

## 6. Risks

| Risk | Control |
|---|---|
| New kernel diverges from specification | section mapping and phrase scan |
| Too much documentation | strict minimum structure and no empty future directories |
| Risk model appears deterministic without evidence | qualitative anchors and recorded rationale |
| Historical status is rewritten | preserve archive and identify new version explicitly |
| `ft_irc` evidence is overstated | record supplied result only; create no missing report |
| Translation becomes a normative fork | explicit source version and synchronization state |
| Evaluation favors ShapingTheAxe | frozen inputs, blinded independent evaluation where possible, adversarial review |

## 7. Completion criteria

The implementation is complete when:

- all in-scope files exist and are internally consistent;
- the original archive hash is unchanged;
- the beta archive passes structural verification;
- the kernel conforms to the Brain Specification;
- state tokens and terminal statuses are aligned;
- `ft_irc` is documentary-only and not rerun;
- proposals are visibly non-normative;
- excluded automation is absent;
- the beta and key specification are available for independent use.

Executing the comparative validation protocol is follow-up beta work, not a
condition for constructing the beta. Until it is executed, generalization and
novelty remain provisional.

## 8. Construction verification record

The following checks were executed against the completed beta tree:

| Check | Actual result | Status |
|---|---|---|
| Required design artifacts | Specification, diagnosis, state model, architecture, plan, and validation protocol present before foundation-derived edits | Pass |
| File inventory | 17 non-empty framework files; no empty ornamental directories | Pass |
| Internal Markdown links | 17 local links checked; 0 broken | Pass |
| Framework manifest | YAML parsed; normative source, immutable predecessor, and closed case state verified | Pass |
| Foundation integrity | SHA-256 remained `4ce99b3330271fdaf8ad6bfb8efaf77a198f1c022e5758ed0a8d7d17f912b93f`; gzip integrity passed | Pass |
| Canonical enums | Claim, budget, decision, terminal, artifact, verification, and translation states aligned with the state model | Pass |
| Seven metrics | Present with evidence anchors in both rubric and comparative protocol | Pass |
| `MICRO` contract scenario | Evidence-based understanding, compact plan/record, and internal review permitted without universal approval | Pass |
| `CRITICAL` contract scenario | Explicit confirmation, plan approval, permission/risk authority, full handoff, rollback, and independent evaluation required | Pass |
| Excluded mechanisms | No executable, script, CLI, automatic agent runtime, MCP implementation, or learning executor present | Pass |
| Provider independence | No provider-specific core behavior found | Pass |
| `ft_irc` boundary | Closed documentary status only; no audit rerun, fixture edit, or missing-evidence placeholder | Pass |

The final release archive is additionally extracted and checked outside the
framework tree. Its checksum is distributed with the release bundle because an
archive cannot contain its own stable checksum.

**Residual validation state:** Construction is verified. Comparative real-case
validation remains pending by design, so multidomain effectiveness, novelty,
and stabilization are still provisional.

## PROPOSALS — NOT YET APPROVED

No unapproved implementation task is included. Future mechanisms listed in the
Brain Specification are intentionally excluded from this plan.

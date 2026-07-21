# Implementation Plan - Business Intelligence Copilot for CrossFit

**Status:** `APPROVED`  
**Context brief:** `docs/run/CONTEXT_BRIEF.md`  
**Framework / kernel:** ShapingTheAxe `0.2.0-beta.2`  
**Prepared by:** Codex  
**Date:** 2026-07-19

## 1. Outcome and boundaries

- **Outcome:** A reproducible zero-dependency Node.js MVP that answers and explains all five required questions over simulated data.
- **In scope:** Domain model, JSON adapter, pure metrics, deterministic question parser, answer presenter, CLI, fixture, automated tests, API discovery, instructions, acceptance evaluation and handoff.
- **Out of scope:** Real API/network access, credentials, business-data mutation, unsupported analytics and all exclusions in AC-06.
- **Constraints and sources:** Frozen experiment input under `experiment/input/`, official supplied API PDF, and confirmed context brief.
- **Authorized intervention and permissions:** `FULL_CYCLE`; read, repository write and local execution only. No network, secrets, publication, external services or production actions.

## 2. Architecture

```text
CLI -> deterministic intent parser -> application query service
                                      |-> pure metric engine
                                      |-> explanation presenter
                                      `-> DataSource port <- JSON fixture adapter
                                                           <- future AimHarder adapter
```

The data-source port returns normalized domain records. Metric functions consume only those records and explicit date ranges/reference dates. The parser selects a supported query and parameters but does not calculate values. The presenter converts structured metric results into a stable answer containing metric, period, data used, exclusions, assumptions and limitations.

## 3. Implementation order

First freeze meanings and API evidence, then create a data contract and fixture, implement pure metrics, add the parser/presenter/CLI, and finally verify end-to-end behavior and close documentation. This order tests the highest-risk business definitions before user-interface details and preserves replaceability.

## 4. Tasks

### Task 1 - Persist discovery and decision evidence

- **Objective:** Complete API capability, contradiction, assumption and limitation records.
- **Reason:** Prevent the mock model from treating undocumented API behavior as confirmed.
- **Expected output:** Updated `docs/03_API_Discovery.md`, context brief and this plan.
- **Files / systems:** `docs/03_API_Discovery.md`, `docs/run/`.
- **Verification:** Cross-check cited fields/endpoints against extracted and visually reviewed PDF pages.
- **Stop or replan condition:** Required business data is shown to be impossible even in the normalized mock model.
- **Dependencies:** Supplied PDF.
- **Risks and controls:** Extraction may lose layout; representative pages were rendered and visually inspected.
- **Decision level:** `LEVEL_1_AUTONOMOUS` within approved discovery boundary.

### Task 2 - Define model and reproducible dataset

- **Objective:** Represent users, sessions and bookings with explicit provenance and a fixed `asOf` date.
- **Reason:** All metrics and tests need stable, AimHarder-compatible concepts.
- **Expected output:** JSON fixture and validation at load time.
- **Files / systems:** `data/`, `src/data/`, domain contracts.
- **Verification:** Loader validation plus deterministic fixture tests.
- **Stop or replan condition:** A required metric needs a field absent from both the documented concepts and an explicit approved assumption.
- **Dependencies:** Task 1 definitions.
- **Risks and controls:** Avoid fake API fidelity; label normalized-only fields and assumptions.
- **Decision level:** `LEVEL_1_AUTONOMOUS`.

### Task 3 - Implement deterministic analytics

- **Objective:** Implement the five metric operations as pure functions.
- **Reason:** AC-01, AC-02, AC-03, AC-04 and AC-09 depend on deterministic, decoupled business logic.
- **Expected output:** Structured results with values, counts, exclusions, assumptions and limitations.
- **Files / systems:** `src/metrics/`, `src/application/`.
- **Verification:** Unit tests with independently hand-calculated fixtures and edge cases.
- **Stop or replan condition:** An approved metric definition becomes internally inconsistent or cannot explain exclusions.
- **Dependencies:** Task 2.
- **Risks and controls:** Boundary/date and denominator errors; use UTC date-only helpers and explicit eligibility functions.
- **Decision level:** `LEVEL_1_AUTONOMOUS`.

### Task 4 - Implement natural-language interface and CLI

- **Objective:** Recognize supported Spanish/English question forms, request clarification for material ambiguity, and reject unsupported questions prudently.
- **Reason:** US-07/08, AC-01 and AC-10 require a useful conversational surface without invented answers.
- **Expected output:** One-shot and interactive CLI with stable explanatory output.
- **Files / systems:** `src/parser/`, `src/presenter/`, `src/cli.js`.
- **Verification:** Parser tests and CLI subprocess smoke tests.
- **Stop or replan condition:** Supporting an input would require generative interpretation or silent period invention.
- **Dependencies:** Task 3.
- **Risks and controls:** Phrase overlap; ordered intent rules and explicit ambiguity results.
- **Decision level:** `LEVEL_1_AUTONOMOUS`.

### Task 5 - Reproduce, validate and hand off

- **Objective:** Make all ten acceptance criteria inspectably pass and preserve actual evidence.
- **Reason:** Completion requires contract/evidence convergence and conversation-independent continuation.
- **Expected output:** README, automated test evidence, acceptance traceability and completion report.
- **Files / systems:** `README.md`, `docs/`, `package.json`, entire repository.
- **Verification:** Clean install-free execution, `npm test`, five CLI demonstrations, repository status/diff review and a clean-handoff procedure.
- **Stop or replan condition:** Any mandatory acceptance criterion fails or verification reveals architecture coupling.
- **Dependencies:** Tasks 1-4.
- **Risks and controls:** Current framework cannot launch an independent evaluator under the active no-delegation constraint; prepare a reproducible clean-handoff checklist and distinguish it from executed tests.
- **Decision level:** `LEVEL_1_AUTONOMOUS` unless a material deviation appears.

## 5. Testing and validation

| Requirement / risk | Method | Expected evidence | Independence level |
|---|---|---|---|
| Metric correctness | `node --test` against hand-calculated cases | Exact percentages, rankings, counts and boundaries | Actual checks |
| Data-source replaceability | Run the same metric tests with in-memory and JSON sources | No metric imports from JSON adapter | Cross-check |
| Parser prudence | Supported, ambiguous and unsupported utterance tests | Correct intent or explicit clarification/refusal | Actual checks |
| Explainability | Response-schema assertions for all six required sections | No analytical answer lacks context | Actual checks |
| Reproducibility | Fresh process using documented commands | Same dataset summary and CLI figures | Cross-check |
| Five MVP questions | End-to-end CLI tests | Valid response for each mandatory question | Actual checks |
| Handoff | Execute a clean-context checklist where possible; otherwise package exact procedure | No hidden conversational dependency | Prepared independent handoff |

## 6. Capability and permission plan

| Need | Capability / adapter | Why selected | Permissions | Cost / risk | Validation |
|---|---|---|---|---|---|
| PDF inspection | PDF skill, Poppler and visual image inspection | Supplied official source is a 111-page PDF | Read PDF; temporary files only | Low; extraction layout risk | Text plus representative page rendering |
| Repository inspection/editing | Shell read tools and `apply_patch` | Native, bounded and traceable | Repository read/write | Low and reversible | Git diff/status |
| Runtime/test execution | Node.js built-ins | Already available; no dependency/network cost | Local execute | Low | Version and actual test output |
| Independent evaluator | Considered but unavailable under current no-subagent constraint | `DEEP` asks for cross-verification | Not selected | Would require additional coordination | Provide exact clean-handoff procedure |

Temporary PDF renders are ephemeral and will be discarded. No new reusable capability is synthesized.

## 7. Alternatives and trade-offs

| Approach | Advantages | Costs / risks | Decision and authority |
|---|---|---|---|
| Zero-dependency JavaScript + `node:test` | Small, reproducible, no network/install dependency, easy CLI | Less compile-time type safety | Chosen in approved architecture |
| TypeScript toolchain | Stronger static typing | Dependencies/build configuration add disproportionate MVP cost | Rejected |
| Python CLI | Also dependency-light | Less aligned with inspected Node environment; no material benefit | Rejected |
| LLM intent routing | Broader phrasing | Non-determinism, cost and risk of invented figures | Rejected by contract |
| Web UI | More visual demonstration | Adds server/frontend scope unrelated to metric feasibility | Deferred/out of scope |

## 8. Failure recovery and rollback

- **Likely failure modes:** Invalid fixture relations, boundary-date defects, parser intent collision, response omissions and Node-version incompatibility.
- **Diagnostic evidence:** Loader errors, focused unit tests, CLI stderr/exit status and import-boundary inspection.
- **Substitution or degradation path:** Narrow accepted phrasing explicitly; retain direct metric commands if free-form phrasing is ambiguous. Do not invent interpretations.
- **Operational rollback:** Revert only candidate-created files/changes using version control after inspecting exact targets; never alter frozen inputs.
- **Escalation trigger:** Required change to scope, metric definition, architecture, permissions, real API use or acceptance contract.

## 9. Complexity and preparation budget

- **Budget:** `DEEP`
- **Complexity:** Medium
- **Drivers:** Five related metrics, natural-language routing, documented API gaps, deterministic explanations and full handoff.
- **Budget-change trigger:** Escalate to `CRITICAL` only if real/sensitive/production data or irreversible external action enters scope; downgrade is not expected before required handoff evidence is complete.

## 10. Approval gate

- [x] Plan matches the confirmed context brief and Definition of Done.
- [x] Every task has objective, reason, output, verification, stop condition and dependencies.
- [x] Material decisions have the correct authority level.
- [x] Required permissions and risk acceptance are explicit.
- [x] Tests, project validation, recovery and rollback are covered.
- [x] No blocking gap is hidden inside a task.
- [x] The responsible user approved continuation without changing the proposed plan.

**Gate state:** `APPROVED`  
**Approval evidence:** User response on 2026-07-19 requesting Spanish presentation only and explicitly preserving scope, authority and technical requirements.  
**Approved at:** 2026-07-19

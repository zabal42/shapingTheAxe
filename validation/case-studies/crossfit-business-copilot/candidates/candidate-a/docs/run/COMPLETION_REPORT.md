# Completion Report - Business Intelligence Copilot for CrossFit

**Final status:** `COMPLETED`  
**Approved plan:** `docs/run/IMPLEMENTATION_PLAN.md`  
**Framework / kernel:** ShapingTheAxe Brain Specification `0.2.0-beta.2` / kernel `0.2.0-beta.2`  
**Prepared by:** Codex  
**Date:** 2026-07-20  
**Base snapshot:** `0ddebd332e7852b05b5559cea408a0ac03453eb4`, branch `candidate-a`  
**Verified runtime:** Node.js `v24.16.0`, npm `11.17.0`

## 1. Outcome

The repository now contains a working, deterministic and explainable CLI MVP
for all five mandatory CrossFit business questions. It uses a reproducible
simulated dataset, keeps metric logic independent of data access, refuses
unsupported analysis without figures, and provides enough retained evidence
for another developer to execute and continue without the original chat.

No real AimHarder request, credential, network integration or business-data
write was introduced.

## 2. Delivered changes

| Change | Files / systems | Planned? | Actual result |
|---|---|---:|---|
| Completed API feasibility discovery | `docs/03_API_Discovery.md` | Yes | Capabilities, evidence boundaries, contradictions and integration gaps retained |
| Reproducible normalized fixture | `scripts/generate-dataset.js`, `data/simulated-box.json` | Yes | 8 users, 14 sessions, 47 bookings; stable SHA-256 |
| Data-source boundary and validation | `src/data/` | Yes | JSON source plus replaceable `load()` contract; invalid/real-marked fixtures rejected |
| Deterministic metric engine | `src/metrics/analytics.js`, `src/domain/dates.js` | Yes | Five pure analytics with exclusions, assumptions and limitations |
| Natural-language application | `src/parser/`, `src/application/`, `src/presenter/`, `src/cli.js` | Yes | Spanish/English supported equivalents, clarifications, refusals and CLI |
| Automated verification | `test/`, `package.json` | Yes | 28 tests across metrics, parser, data boundary, source replacement and CLI |
| Reproduction and handoff documentation | `README.md`, `docs/05_*`, `docs/06_*`, `docs/run/` | Yes | Architecture, model, acceptance, decisions, checkpoint and clean procedure |

## 3. Requirements traceability

| Requirement / success criterion | Authority | Implementation | Actual verification | Status |
|---|---|---|---|---|
| AC-01 Five questions | Frozen acceptance criteria | Parser, Copilot and five metrics | Full/acceptance suites execute all five | `PASS` |
| AC-02 Deterministic metrics | AC-02 and prompt | Pure functions; fixed `asOf`; no LLM | Exact-value and repeatability tests | `PASS` |
| AC-03 Explainable answers | AC-03, US-06 | Structured result and presenter | Six-section assertion for every question | `PASS` |
| AC-04 Replaceable data layer | AC-04 | `DataSource.load()` normalized boundary | JSON and in-memory sources return deep-equal answers | `PASS` |
| AC-05 No undocumented API assumptions | AC-05 | API discovery separates documentation and project rules | Document/mapping inspection and explicit gaps | `PASS` |
| AC-06 Focused scope | AC-06 | Five read-only analytics and local CLI | Structure/diff inspection; no HTTP dependency or action path | `PASS` |
| AC-07 Reproducibility | AC-07 | Generator, fixture, scripts and README | Regeneration retained identical SHA-256 | `PASS` |
| AC-08 Technical handoff | AC-08 | Architecture, discovery, records and procedure | Repository-only continuation instructions prepared | `PASS` |
| AC-09 Automated metric tests | AC-09 | Node test suites | 28/28 final and clean-environment runs | `PASS` |
| AC-10 Product value | AC-10 | One-shot and interactive natural questions | CLI subprocess and five demonstrations | `PASS` |

Detailed criterion mapping: `docs/06_ACCEPTANCE_EVALUATION.md`.

## 4. Verification evidence

| Check | Method | Actual result | Status |
|---|---|---|---|
| Dataset validity | JSON adapter load/validation | 8 users, 14 sessions, 47 bookings | `PASS` |
| Dataset reproducibility | SHA-256 before and after `npm run generate:data` | Both `b691e655e2f41fd1379c11b45b452775a42c1336acae3932ca1a319c4a2973a0` | `PASS` |
| Review regression reproduction | Targeted Node tests before corrections | 19 pass, 4 fail; each failure matched one review finding | `PASS` |
| Corrected regression subset | Targeted Node tests after corrections | 23 tests, 23 pass, 0 fail | `PASS` |
| Full automated suite | `npm test` | 28 tests, 4 suites, 28 pass, 0 fail | `PASS` |
| Acceptance-only suite | `npm run test:acceptance` | 5 tests, 5 pass, 0 fail | `PASS` |
| JavaScript syntax | `node --check` on all JS under `src`, `scripts`, `test` | Exit 0, no diagnostics | `PASS` |
| Clean-process cross-verification | `env -i ... node --test` | 28 pass, 0 fail | `PASS` |
| Five CLI questions | New Node processes with README questions | All five return analytical answers with required sections | `PASS` |
| Prudence | Unsupported fidelity question and ambiguity tests | Clarification/refusal; no invented figure | `PASS` |
| Frozen input integrity | SHA-256 comparison of duplicate briefs/stories/AC/PDF | Every pair remains identical | `PASS` |
| Patch hygiene | `git diff --check` | Exit 0, no whitespace errors | `PASS` |

Observed business results for the fixed fixture:

- May occupancy: 65%.
- June occupancy: 63.33% across 6 valid sessions.
- Lowest June group: Halterofilia at 19:00, 37.5%.
- Highest cancellation slot: 19:00, 4/7 = 57.14%.
- Active users over 21 days: Socio 005, 002 and 003.
- June versus May: -1.67 percentage points and -2.56% relative.

## 5. Deviations and state invalidations

| Deviation / new evidence | Affected claim, gate, or plan | Authority / resolution | Impact |
|---|---|---|---|
| User requested a safe pause | Execution state | Checkpoint created; later hash/state verified and explicitly resumed | No contract or plan invalidation |
| Explicit dates were initially eligible to be read as ranking limit | Parser Level 1 detail | Removed dates before numeric limit parsing; regression test added | Defect corrected before closure |
| Invalid comparison ranges could produce null periods | Parser Level 1 detail | Validate both ranges before returning `ready`; regression test added | Defect corrected before closure |
| English inactivity threshold was not initially matched | Approved equivalent-language detail | Added `days` pattern and regression test | No scope change |
| Review found missing `cancelledAt` could be treated as cancellation | Normalized input contract and cancellation metric | Require explicit null/valid timestamp; add malformed-input regression | Corrected; dataset identity unchanged |
| Review found derived comparison used rounded inputs | Mandatory period-comparison metric | Preserve raw averages for derived calculations; round only output | Corrected expected relative change from -2.57% to -2.56% |
| Review found cancelled sessions could supply last attendance | Mandatory inactivity metric | Precompute valid attendance excluding cancelled sessions; add regression | Corrected without changing approved business rule |
| Review found exact “último mes” brief phrase unsupported | Natural-language contract | Map to previous calendar month and add parser regression | Corrected without broadening supported intents |
| Framework rubric says beta.1 while normative spec/kernel say beta.2 | Evaluation identity | Normative beta.2 governs; mismatch retained as framework defect | Independent official rubric verdict remains caveated |

No material deviation required returning to user approval.

## 6. Failure and recovery record

| Failure | Diagnosis | Retry hypothesis / substitute | Result | Scope degradation |
|---|---|---|---|---|
| `ps` denied while creating checkpoint | Sandbox disallows system process listing | Verify completed tool results and avoid process inspection | Checkpoint safely created | None |

No implementation command, test suite or data generation failed. The parser
issues above were findings from bounded direct checks, not failed final gates.

## 7. Edge cases, limitations, and residual risk

- **Covered:** inclusive ranges, strict >21-day boundary, never-attended proxy,
  cancelled sessions, zero capacity, no-data periods, deterministic ties,
  malformed comparisons, missing periods/thresholds, unsupported analysis,
  broken relations and non-simulated sources.
- **Known limitation:** natural-language coverage is rule-based and bounded;
  occupancy is reservation-based; no causal conclusions are produced.
- **Residual integration risk:** the official PDF does not document a global
  booking list or an unambiguous per-history session key, and its transport and
  response examples conflict. This is owned by any future integration project,
  not silently accepted by this MVP.
- **Ideal versus viable result:** The ideal independent third-party evaluation
  could not be launched under the active no-delegation constraint. Actual
  cross-verification used isolated fresh Node processes, and an exact clean
  evaluator contract is retained in `docs/run/HANDOFF_PROCEDURE.md`.

## 8. Capability usage ledger

| Platform / provider / adapter | Capability and version | Selected / rejected / blocked | Permissions | Actual utility / failure | Retention recommendation |
|---|---|---|---|---|---|
| Codex runtime | ShapingTheAxe `0.2.0-beta.2` | Selected | Repository read/write and local execute | Governed discovery, gates, plan, pause/resume and closure | Retain run records for project |
| PDF skill / Poppler | Supplied PDF inspection | Selected | Read input; write temporary renders | Text extraction plus representative visual confirmation | Discard temporary capability state; retain findings |
| Node.js `v24.16.0` | Built-in ESM, readline, test runner | Selected | Local execution | Zero-dependency app and 28 passing tests | Retain as project runtime; minimum documented Node 20 |
| npm `11.17.0` | Script adapter | Selected | Local execution | Reproducible commands; no install/network needed | Retain scripts |
| TypeScript toolchain | Static compiler/build | Rejected | Would require dependencies/configuration | No proportional benefit for bounded MVP | Do not retain |
| LLM intent/calculation | Generative routing | Rejected | Would add non-determinism/network/cost | Conflicts with figure integrity and MVP size | Do not use |
| Independent subagent evaluator | Separate evaluator | Blocked by active no-delegation constraint | Not granted | Exact clean handoff procedure prepared instead | Defer to authorized evaluation run |

## 9. Remaining work and handoff

| Item | Blocking? | Owner | Next action | Required decision |
|---|---:|---|---|---|
| Execute clean independent evaluation | No for product completion; required for an official independent framework verdict | Experiment evaluator | Follow `docs/run/HANDOFF_PROCEDURE.md` without chat access | Assign evaluator |
| Build real AimHarder adapter | No; explicitly out of MVP | Future integration owner | Resolve discovery gaps before coding | Separate scope, credentials and risk approval |
| Broaden phrase coverage or add UI | No | Product owner | Validate value with box owners first | New scope decision |

The immediate continuation point for a developer is the handoff procedure. No
required MVP implementation remains.

## 10. Learning candidates

| Observation | Evidence | Scope | Private data removed? | Proposed post-close state |
|---|---|---|---:|---|
| Fixed dataset time prevents relative-date drift | Repeated clean-process results use `metadata.asOf` | Project / decision | Yes | `CANDIDATE` |
| Transport documentation contradictions justify normalization at adapter boundary | API discovery matrix | Problem / architecture | Yes | `CANDIDATE` |
| Small direct demonstrations found parser defects before formal closure | Two corrected regressions | Process | Yes | `CANDIDATE` |
| Full persistent checkpoint enabled exact resume without repeated inspection | Hash/state match on 2026-07-20 | Process | Yes | `CANDIDATE` |

These candidates were not promoted, loaded into the framework or persisted as
shared knowledge during runtime.

## 11. Final review

- [x] Intent, contract and actual evidence converge for `COMPLETED`.
- [x] Required checks were executed and recorded with actual results.
- [x] Scope, architecture, permissions and frozen inputs were respected.
- [x] Deviations and framework-version contradiction remain visible.
- [x] Edge cases, API gaps and residual risks are explicit.
- [x] Documentation and clean handoff are sufficient for the `DEEP` budget.
- [x] Exact framework, base snapshot, runtime and dataset identity are retained.
- [x] No runtime core or shared-learning mutation occurred.

## 12. Final decision

- **Status:** `COMPLETED`
- **Reason:** All ten mandatory acceptance criteria have implementation and
  executed evidence; the five questions work over a reproducible simulated
  dataset; no required scope item remains.
- **Closure depth:** `COMPLETE`
- **Independent evaluation / handoff:** Cross-verification passed in a fresh
  minimal environment. Independent third-party execution is not claimed; the
  exact uncontaminated procedure is ready in `docs/run/HANDOFF_PROCEDURE.md`.

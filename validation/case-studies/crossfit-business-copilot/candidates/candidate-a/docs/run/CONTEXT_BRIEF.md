# Context Brief - Business Intelligence Copilot for CrossFit

**Status:** `CONFIRMED`  
**Framework / kernel:** ShapingTheAxe Brain Specification `0.2.0-beta.2` / kernel `0.2.0-beta.2`  
**Prepared by:** Codex  
**Date:** 2026-07-19  
**Target snapshot:** Git commit `0ddebd332e7852b05b5559cea408a0ac03453eb4` on branch `candidate-a`  
**Budget:** `DEEP`

## 1. Task capsule

- **Outcome:** A small, working, deterministic BI copilot that answers the five mandatory business questions over simulated AimHarder-compatible concepts.
- **Why:** Demonstrate whether a CrossFit box owner can obtain useful, explainable business information without navigating multiple application screens.
- **Definition of Done:** Every criterion in `experiment/input/04_Acceptance_Criteria.md` passes with a reproducible dataset, working natural-language CLI, automated tests, installation and execution instructions, and a conversation-independent technical handoff.
- **Work type / domain / state:** Creation / software and business analytics / new feasibility MVP.
- **Authorized intervention:** `FULL_CYCLE`, evidenced by the experiment protocol's instruction that each candidate must complete the project and by the user's instruction to begin and subsequently continue.
- **In scope:** Simulated data, five metrics, deterministic intent recognition, explainable answers, replaceable data access, tests, documentation and handoff.
- **Out of scope:** Real AimHarder connectivity or credentials, mutations of business data, bookings, payments, messaging, multi-box support, predictions, machine learning and unrestricted generative answers.

## 2. Risk and preparation

| Dimension | Assessment | Evidence | Effect on budget or controls |
|---|---|---|---|
| Impact | Moderate | Results are a feasibility demonstration, but incorrect metrics would invalidate it | Explicit metric contracts and acceptance tests |
| Reversibility | High | Repository-local changes on a candidate branch | Small commits/files and no external actions |
| Uncertainty | Moderate | The API document contains omissions and contradictions; business definitions were not fully specified | Record assumptions; keep adapter and metric engine separate |
| Scope | Bounded | Five questions and explicit exclusions | Reject unsupported intents and avoid extra features |
| Sensitivity | Low | Simulated data only; credentials expressly forbidden | No network/API integration or secret handling |
| Recovery cost | Moderate | Architectural coupling could require metric rewrites | Port-based data-source boundary and pure metrics |

**Selected budget and reason:** `DEEP`, because the work includes a material architecture decision, multiple business definitions, reproducible implementation, acceptance evaluation and a clean technical handoff. It is not `CRITICAL`: it is local, simulated, reversible and non-production.

## 3. Artifact inventory

| Artifact | Identity / location | Inspected? | Relevant evidence | Validity |
|---|---|---:|---|---|
| Governing kernel | `/Users/mikelzabal/Desktop/CodingWithZabal/ShapingTheAxe/repo/ShapingTheAxe.md` | Yes | Gates, risk budget, verification and closure rules | Version `0.2.0-beta.2` |
| Normative specification | `SHAPING_THE_AXE_BRAIN_SPEC.md` beside the kernel | Yes | Semantic authority and full-cycle requirements | Version `0.2.0-beta.2` |
| Experiment protocol | `experiment/protocol/EXPERIMENT_PROTOCOL.md` | Yes | Candidate must complete the project and retain evolution evidence | Frozen repository input |
| Experiment prompt | `experiment/input/EXPERIMENT_PROMPT.md` | Yes | Objective, scope, constraints and deliverables | Frozen repository input |
| Project brief and stories | `experiment/input/01_Project_Brief.md`, `02_User_Stories.md` | Yes | Users, value, five questions, explainability and prudence | Frozen repository input |
| Acceptance criteria | `experiment/input/04_Acceptance_Criteria.md` | Yes | Ten mandatory criteria | Frozen repository input |
| AimHarder documentation | `experiment/input/AimHarder_API.pdf`, SHA-256 `47f6d0ea...9fa457f` | Yes, text extraction and representative visual review | Official documented entities, fields, endpoints and contradictions | Captured 2026-07-18; no real API behavior verified |
| Repository and history | Git tree and log through `0ddebd3` | Yes | Only initial context exists; no implementation or dependencies | Pre-implementation snapshot |
| Runtime | Node `v24.16.0`, npm `11.17.0`, Python `3.14.6` | Yes | A zero-dependency Node implementation is locally executable | Current development environment |

The `docs/` and `experiment/input/` copies of the brief, stories, acceptance criteria and PDF were hash-compared and are identical.

## 4. Six-layer context map

| Layer | Readiness | Critical evidence or decision | Remaining gap | Blocking? |
|---|---|---|---|---:|
| Intention | `READY` | Build and demonstrate the five-question MVP | None | No |
| Contract | `READY` | Frozen prompt, stories and acceptance criteria | Product-level write prohibition required interpretation | No; resolved by confirmation |
| Operation | `READY` | Empty implementation baseline; Node runtime available; local writes allowed | Exact portability beyond supported Node version | No; document minimum version |
| Domain | `CONTROLLED` | API PDF documents clients, schedules, capacity and per-client booking histories | No center-wide booking list or observed API behavior | No; mock boundary plus future-adapter limitation |
| Human | `READY` | User owns contract/architecture approval and prefers Spanish communication | None | No |
| History | `READY` | Git history contains only project/experiment setup | None | No |

## 5. Critical claim ledger

| Claim | State | Source | Authority | Validity | Affected decision |
|---|---|---|---|---|---|
| The MVP must answer exactly five mandatory business questions | `VERIFIED` | Experiment prompt and AC-01 | Governing contract | This MVP | Scope and tests |
| Business figures must be deterministic and explainable | `VERIFIED` | Prompt, US-06/07 and AC-02/03 | Governing contract | Every analytical response | Metric/presenter architecture |
| Data access must be replaceable without changing metrics | `VERIFIED` | Prompt and AC-04 | Governing contract | Mock and future adapter | Data-source port |
| Active clients are returned by `GET /clients` | `VERIFIED` | AimHarder PDF p. 43 | Official documentation | Documented API v1.0; not runtime-tested | Active-user mapping |
| Booking history contains class, day/time, state, attendance and cancellation date | `VERIFIED` | AimHarder PDF pp. 56-60 | Official documentation | Per-client endpoint only | Booking model |
| A center-wide booking history is available | `UNKNOWN` | No endpoint in supplied PDF | Official documentation | Supplied API document | Future ingestion strategy |
| Repository writes are permitted while business/API mutations are forbidden | `VERIFIED` | Required working repository outcome plus user continuation after explicit interpretation | Contract plus responsible-user confirmation | Candidate repository only | Authority to implement |
| Metric definitions presented at the understanding gate are accepted | `VERIFIED` | User instruction to continue without changing scope, authority or requirements | Responsible user | Current approved plan | Metric implementation |

## 6. Questions and decisions

| # | Material uncertainty | Why user authority was needed | Answer / decision | Level | Impact |
|---:|---|---|---|---|---|
| 1 | Whether repository writes are compatible with the no-write constraint, and whether the proposed architecture/metric definitions may govern the MVP | Literal interpretation would make the required implementation impossible; definitions materially shape results | User instructed continuation and stated that only presentation language changes; proposed interpretation and plan therefore remain confirmed | `LEVEL_3_USER_RESERVED` | Authorizes bounded repository implementation |

## 7. Confirmed understanding

The MVP is a local, demonstrable command-line copilot for a single CrossFit box. It accepts ordinary Spanish or English questions, maps only supported phrasings to one of five deterministic analytical operations, reads a fixed simulated dataset, and returns business figures together with their calculation context. The language layer may select a metric but never calculate or invent its figures. Repository implementation writes are allowed; business data mutations, real API access and credentials are not. Business logic remains independent of the JSON data source so that a future AimHarder adapter can reuse the same metrics. Communication for the rest of the run is in Spanish; repository-facing technical identifiers and documentation may use the clearest language for reproducibility.

## 8. Gap and contradiction control

| Type | Gap or conflict | Evidence | Impact | Owner | State | Resolution / boundary |
|---|---|---|---|---|---|---|
| Contradiction | “Do not perform write operations” versus mandatory working repository | Experiment prompt lines 44 and 60-72 | Could block all implementation | User | `RESOLVED` | Applies to product/API business mutations, not authorized repository edits |
| Contradiction | Evaluation rubric identifies beta.1 while specification/kernel are beta.2 | Framework files inspected 2026-07-19 | Exact conformance evaluation version is inconsistent | Framework owner | `CONTROLLED` | Use beta.2 semantic authority; report rubric mismatch; do not modify framework |
| Contradiction | API examples mix HTTPS/HTTP and `api.aimharder.com`/`aimharderlocal.com` | PDF endpoint examples | Future adapter base URL cannot copy examples blindly | Future adapter owner | `CONTROLLED` | Treat documented HTTPS production base as intended; verify before integration |
| Contradiction | List endpoints describe envelopes but some success examples are raw arrays | PDF general response schema and endpoint examples | Deserialization strategy is uncertain | Future adapter owner | `CONTROLLED` | Adapter must validate observed payloads; mock does not assert transport shape |
| Unknown | No documented global booking-history endpoint | Supplied PDF endpoint inventory | Real synchronization may require N+1 client traversal | Future adapter owner | `CONTROLLED` | Preserve per-client provenance; document performance/incremental-sync limitation |
| Ambiguity | Occupancy could mean reservations or attendance | Stories require a definition but do not prescribe it | Changes all occupancy metrics | Project | `RESOLVED` | Confirmed plan uses confirmed, non-cancelled bookings / capacity, mean of session ratios |
| Ambiguity | Never-attended active users have no last-attendance date | US-04 requires inactive users and last attendance | Affects inclusion/explanation | Project | `RESOLVED` | Include after 21 days from creation, label creation date as proxy and limitation |

## 9. Gate result

- [x] Relevant evidence was inspected before asking answerable questions.
- [x] Every context layer is `READY` or validly `CONTROLLED`.
- [x] Material contradictions are visible and controlled or resolved.
- [x] Scope, authority, permissions and Definition of Done are explicit.
- [x] Budget and verification independence are justified.
- [x] The responsible user confirmed continuation without changing the proposed scope, authority or requirements.

**Gate state:** `APPROVED`  
**Confirmation evidence:** User response: “Please continue in Spanish ... This is a presentation preference only. It does not change the project scope, authority or technical requirements.”  
**Confirmed at:** 2026-07-19

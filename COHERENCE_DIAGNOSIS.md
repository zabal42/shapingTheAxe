# ShapingTheAxe Coherence Diagnosis

**Baseline inspected:** ShapingTheAxe foundation `v0.1`, including
`context-init v0.2`  
**Consolidation authority:** approved Brain Consolidation decisions  
**Target:** ShapingTheAxe `0.2.0-beta.1`  
**Status:** Consolidated diagnosis — historical record, retained unchanged as
the original consolidation rationale. See `CHANGELOG.md` for subsequent
repository-level changes.

## 1. Executive finding

The foundation is internally coherent as a strict software-oriented startup
protocol, but it is not sufficient as the canonical architecture of the
approved ShapingTheAxe Brain.

The consolidation is an evolutionary version boundary, not a textual cleanup.
Foundation `v0.1` treats exhaustive context loading, five fixed uncertainty
sources, universal human gates, and three persistent artifacts as protocol
invariants. The approved Brain instead requires proportional effort, six
context layers, risk-sensitive autonomy, adaptive artifacts, capability
selection, deferred learning, provider separation, and governed versioning.

The correct migration is therefore:

1. retain foundation `v0.1` and `context-init v0.2` unchanged as historical
   evidence;
2. establish `SHAPING_THE_AXE_BRAIN_SPEC.md` as the new semantic authority;
3. derive a new portable kernel from that specification;
4. migrate useful foundation contracts without preserving superseded absolute
   rules;
5. validate the beta against real comparative cases.

## 2. Sources inspected

The diagnosis is based on the complete contents of:

- `ShapingTheAxe_Brain_Consolidation_Prompt.md`;
- foundation `README.md`;
- foundation `ShapingTheAxe.md`;
- `docs/architecture.md`;
- `docs/roadmap.md`;
- `evaluation/rubric.md`;
- `templates/context-brief.md`;
- `templates/implementation-plan.md`;
- `templates/completion-report.md`;
- `examples/ft_irc/README.md`.

No `ft_irc` audit, fixture, report, or test was repeated.

## 3. Approved decisions

The following decisions are normative for the beta:

1. Approved Brain decisions supersede `context-init v0.2` on conflict.
2. `SHAPING_THE_AXE_BRAIN_SPEC.md` is the semantic authority.
3. `ShapingTheAxe.md` is the portable operational kernel.
4. The six-layer context model is canonical.
5. The five-source model remains only as a compatibility mapping.
6. Human gates are selected by risk, materiality, and decision authority.
7. The artificial five-percent uncertainty threshold is removed.
8. The new protocol is versioned without rewriting historical `v0.1`.
9. English is initially normative; synchronized translations must identify
   their source and synchronization state.
10. Full artifacts remain available, with a compact equivalent for small runs.
11. `ft_irc` receives documentary status correction only.
12. The beta excludes a CLI, automatic agent orchestration, custom MCP servers,
   and automated learning.

## 4. Contradictions and approved resolutions

| ID | Foundation rule | Brain rule | Material effect | Approved resolution |
|---|---|---|---|---|
| C-01 | Never optimize for speed; always optimize for understanding | Maximize justified quality with minimum total cost | Foundation can over-research low-risk tasks | Proportionality and minimum sufficiency govern |
| C-02 | Five uncertainty sources are fixed | Six canonical context layers | Old model does not represent authority, history, and operational context cleanly across domains | Six layers are canonical; five-source mapping retained |
| C-03 | Understanding confirmation is always a hard gate | Level 1 work may be autonomous | Universal interruptions conflict with useful autonomy | Gate selected by budget, materiality, and authority |
| C-04 | Every plan requires explicit approval | Low-risk authorized work may proceed autonomously | Routine work accumulates avoidable user load | Explicit approval reserved for `DEEP`, `CRITICAL`, Level 2, Level 3, or material change |
| C-05 | Any new uncertainty pauses and asks | Only material uncertainty blocks | Trivial unknowns interrupt execution | Record non-blocking uncertainty; escalate material uncertainty |
| C-06 | Always ask one question at a time | Independent questions may be grouped | Strict sequencing wastes user attention | Sequence dependent questions; group independent ones |
| C-07 | Reduce uncertainty below 5% | No false precision | The percentage is not measured | Replace with qualitative closure criteria |
| C-08 | Inspect every artifact that might answer | Use minimum sufficient context | Exhaustive inspection can be unbounded | Research by risk, relevance, and saturation |
| C-09 | Validate understanding before formal gap analysis | Detect gaps before validation | A summary may be confirmed while hiding contradictions | Preliminary gap detection precedes understanding validation |
| C-10 | Three durable artifacts for every run | Traceability is proportional | Small tasks suffer documentation overhead | Preserve full contracts; add compact equivalent |
| C-11 | `ShapingTheAxe.md` is the only normative behavior source | Brain Spec is requested as semantic source | Two sources could silently diverge | Brain Spec governs; kernel is derived and conformance-tested |
| C-12 | Final states omit failure | Canonical final states include `FAILED` | Failed execution has no honest terminal representation | Add `FAILED` and align templates |

## 5. Stale documentary state

The following foundation statements are historical and MUST NOT be carried into
the beta as current fact:

- `README.md` says the clean `ft_irc` run is pending.
- `docs/roadmap.md` leaves the reference execution, evaluation, and handoff
  unfinished.
- `examples/ft_irc/README.md` labels the case `Planning` and pending.

The approved current state is:

- score `91.3/100`;
- verdict `PASS`;
- no hard failure;
- independent handoff passed;
- exact evidence correspondence;
- `irssi` blocked by environment and documented;
- not Reference-grade due to the missing complete chronological transcript,
  unformalized `Planning → Full-cycle` transition, and pending `irssi` check.

Only status and interpretation may be updated. Missing evidence files MUST NOT
be fabricated, empty placeholders MUST NOT be created, and the audit MUST NOT
be rerun.

## 6. Overlap consolidated into one concept

### 6.1 Context closure and knowledge state

Foundation uses `Open`, `Ambiguous`, and `Closed` for context sources. The Brain
uses claim-level states. The beta separates them:

- claims use `UNKNOWN`, `PARTIAL`, `PROVISIONAL`, `VERIFIED`, `CONFLICTED`, and
  `NOT_APPLICABLE`;
- context layers derive readiness from their material claims;
- gaps use their own control state;
- closure is a gate result, not a second claim taxonomy.

### 6.2 Approval and authorization

Approval is not the same as authorization. Authorization defines the permitted
intervention mode and permissions. Approval resolves a particular Level 2 or
Level 3 decision or a required risk gate. The beta records both separately.

### 6.3 Verification and evaluation

Verification checks a result against its contract. Evaluation judges execution
or framework quality. Independence increases with risk; not every verification
requires a separate evaluator.

### 6.4 Capability scope and status

`EPHEMERAL` through `CORE` represent scope and governance maturity.
`CANDIDATE` through `ARCHIVED` represent operational availability. They are
orthogonal and MUST NOT be collapsed into one lifecycle list.

### 6.5 Execution learning and framework evolution

Runtime observation is continuous. Stable learning is deferred. A candidate
does not become project or shared knowledge until a post-close evaluation.

## 7. Terms requiring formal definitions

The beta specification and state model formalize:

- material uncertainty;
- material contradiction;
- minimum sufficient context;
- preparation budget;
- decision level;
- gate;
- critical claim;
- controlled gap;
- exact configuration;
- runtime coordinator;
- capability specification;
- adapter;
- clean learning;
- operational and analytical rollback.

These definitions remain qualitative where quantitative precision is not
evidence-based.

## 8. Implementation difficulties

### 8.1 Consistent qualitative budget selection

Risk dimensions are clear, but they do not mechanically determine a budget.
The beta uses anchored conditions and records the reason. It does not claim an
algorithm until field evidence exists.

### 8.2 Selective context invalidation

The Brain requires only affected context to be invalidated. A fully automated
dependency graph is outside beta. The compact record therefore names affected
claims and decisions explicitly, allowing manual but traceable invalidation.

### 8.3 Provider-independent capability discovery

Providers expose different tools and permissions. The beta defines the
canonical selection and ledger contract but permits native/manual discovery.
Automated adapter conformance is deferred.

### 8.4 Measuring useful autonomy

Raw interruption count is insufficient: silence can hide errors and frequent
questions can prevent them. The validation protocol combines interruption
counts with necessity, timeliness, correctness, and rework.

### 8.5 Proving clean learning

The beta can prove separation and retained candidate evidence. It cannot yet
prove automated retention quality because automated learning is excluded.

## 9. Bureaucracy risks and controls

| Risk | Failure mode | Beta control |
|---|---|---|
| Artifact inflation | Documentation becomes the product | Compact record for `MICRO`; full artifacts only when justified |
| Claim ledger overload | Every trivial statement becomes a row | Record only claims that affect a decision, requirement, risk, or handoff |
| Endless research | “Search first” becomes exhaustive crawling | Research design, information value, and sufficiency stop conditions |
| Gate accumulation | User approves routine details | Gate matrix by budget and decision level |
| Capability ledger noise | Every available tool is documented | Record considered capabilities only when materially plausible |
| Closure ceremony | Tiny tasks receive full audit reports | `LIGHT`, `STANDARD`, and `COMPLETE` closure depth |
| Version sprawl | Every text edit becomes a release | Version behavior and contracts; use ordinary revision history for editorial changes |

## 10. Excess-autonomy risks and controls

| Risk | Control |
|---|---|
| Scope drift | Intervention mode and Definition of Done remain explicit |
| Silent architecture change | Level 3 user-reserved decision |
| Permission inheritance | Permissions granted separately per capability |
| Hidden risk acceptance | Explicit acceptance state and responsible authority |
| Production impact | `CRITICAL` budget and user-reserved execution |
| Sensitive-data propagation | Classification, minimization, and learning separation |
| Degraded quality hidden as completion | Required distinction between ideal, viable, and accepted debt |

## 11. Provider-dependence risks and controls

The principal dependence risk is not naming a provider; it is allowing an
adapter's convenient behavior to redefine the core. The beta controls this by:

- keeping the Brain Spec and kernel in portable Markdown;
- separating capability specification from adapter;
- recording platform, provider, and adapter in every material run;
- evaluating adapter and capability quality separately;
- prohibiting adapter-specific behavior from becoming normative silently;
- designing translation and adapter conformance as explicit checks.

## 12. Growth risks and controls

| Growth risk | Control |
|---|---|
| Duplicate capabilities | `DISCOVER → REUSE → COMPOSE → SYNTHESIZE` order |
| Local helper becomes universal rule | Scope lifecycle and promotion gates |
| Core changes from one anecdote | Independent evaluation and multidomain evidence |
| Runtime library contamination | Deferred evolution plane |
| Obsolete capabilities remain active | dormancy, deprecation, archive, expiry review |
| Private evidence enters shared knowledge | pattern/data separation and sensitivity rules |

## 13. Remaining open evidence gaps

These are not blockers for producing the manual beta:

- The comparative protocol has not yet been run across new equivalent cases.
- Multidomain transfer remains unproven.
- Qualitative budget consistency has not been measured between independent
  operators.
- Translation synchronization has an architecture but no translated artifact
  yet.
- Capability and adapter conformance has not been field-tested.
- The current package does not contain the frozen `ft_irc` report and evidence,
  so only the approved documentary status can be recorded.

## 14. Readiness conclusion

The approved decisions are sufficient to build a manual, Markdown-first beta.
The remaining gaps belong to validation, not to initial architecture. The beta
must remain reversible, preserve the foundation, avoid automatic evolution,
and treat every untested universal claim as provisional.

## PROPOSALS — NOT YET APPROVED

No unapproved mechanism is required to resolve the diagnosed contradictions.
Possible automation ideas are isolated in the Brain Specification and MUST NOT
be treated as beta requirements.

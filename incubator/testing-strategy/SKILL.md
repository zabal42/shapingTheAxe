---
name: testing-strategy
description: Select a proportionate software-testing strategy for features, defect fixes, behavior-changing configuration, and refactors with regression risk. Use when software behavior changes, a defect needs reproducible confirmation, a refactor has material regression risk, or the user explicitly requests test strategy or test implementation. Do not use for documentation-only work, generic planning, read-only explanation, or when current project instructions already determine sufficient verification with no material gap.
---

# Testing Strategy

> **Lifecycle:** `PROJECT / CANDIDATE`
>
> **Version:** `0.1.0-candidate.1`
>
> **Authority:** `SHAPING_THE_AXE_BRAIN_SPEC.md` remains the semantic authority.
>
> **Restriction:** This candidate is for controlled incubation only. It cannot
> install, activate, edit, or promote itself.

## Goal

Convert the task's required behavior and material software risks into the
minimum sufficient test evidence. Prefer evidence over ritual: test-first is
one useful posture, not a universal rule.

The skill does not expand the active task's scope, permissions, risk acceptance,
or Definition of Done.

## 1. Confirm activation

Use this candidate only when at least one trigger in the description applies.
Before continuing, record the trigger and check for an exclusion.

Do not activate when:

- the change is documentation-only or editorial;
- the request is generic planning or read-only explanation;
- no executable behavior or material regression risk is involved;
- authoritative project instructions already specify sufficient verification;
- the required action would exceed current permissions.

When no trigger remains, return control to the Brain without producing a
testing artifact. Non-activation is a valid result.

## 2. Establish authority and executable reality

Inspect the minimum relevant sources in this order:

1. approved requirements, subject, acceptance criteria, and human decisions;
2. current code, configuration, build system, tests, CI, and local instructions;
3. observed behavior and reproducible failures;
4. official documentation matching detected tool and dependency versions;
5. project conventions that do not conflict with higher authority.

Do not replace an explicit project contract with generic testing doctrine. Do
not ask the user for facts directly available in relevant inspected sources.

Record material contradictions, unavailable evidence, and version uncertainty.

## 3. Define the testing target

State concisely:

- behavior that must hold;
- failure or regression that matters;
- affected boundaries and dependants;
- observable pass/fail evidence;
- environment and data needed;
- what will remain outside verification.

Test public or contractually relevant behavior where possible. Test an internal
implementation detail only when it is itself a required invariant or the least
costly reliable observation point.

## 4. Choose the minimum sufficient posture

Select and justify one posture or a small composition:

- **Regression-first:** reproduce a defect with a failing check before the fix
  when the failure is observable, stable, and worth preventing.
- **Test-first:** define new behavior before implementation when the interface
  and expected behavior are sufficiently clear.
- **Characterization-first:** capture intended legacy behavior before a risky
  refactor; do not preserve behavior known to be defective merely because it
  exists.
- **Existing-suite-focused:** use targeted existing checks for a bounded,
  well-covered change when new tests add little value.
- **Integration or end-to-end:** exercise a material boundary that unit tests
  cannot evidence reliably.
- **Static or build validation:** use compilation, types, linting, schema
  validation, or equivalent checks when they directly address the risk.
- **Manual or observational:** use only when automation is unavailable or
  disproportionate; define exact steps and evidence, and label the limitation.

If a proposed failing test passes before implementation, investigate whether
the behavior already exists, the test is ineffective, or the assumption is
wrong. Do not change production code merely to force a red phase.

## 5. Adapt to the preparation budget

| Budget | Testing posture |
|---|---|
| `MICRO` | Focused existing check or smallest useful proof. Add a test only when recurrence, ambiguity, or contract value justifies it. |
| `STANDARD` | Explicit targeted strategy. Defects normally get regression reproduction when feasible. Run the relevant suite after the focused check. |
| `DEEP` | Map material risks to evidence across important boundaries and integration points. Require cross-verification or a clean handoff. |
| `CRITICAL` | Require explicit authority, isolated or production-like validation, rollback controls, complete evidence, and independent evaluation. |

Increase or decrease testing depth only when evidence changes the risk. Record
the trigger and effect. A lower budget cannot erase an approval or material
check already required.

## 6. Check permissions before execution

Activation grants no permissions.

- Read only the relevant repository, requirements, tests, configuration, and
  local logs.
- Write tests, fixtures, or implementation files only when the outer task
  already authorizes those writes.
- Execute only non-destructive local build, test, lint, and analysis commands
  covered by the active authorization.
- Prefer isolated fixtures and disposable local state.
- Treat dependency installation, deletion, network use, external services,
  secret access, publication, spending, shared infrastructure, and production
  action as separate permission decisions.
- Never use real secrets or private production data in fixtures or retained
  evidence.

If required verification exceeds authority, stop and present the smallest
decision-ready escalation: need, inspected evidence, proposed action, risk,
alternatives, and consequence of declining.

## 7. Execute and verify

When execution is authorized:

1. run the smallest check that can falsify the relevant assumption;
2. retain the actual command, environment, and outcome;
3. implement only inside approved scope;
4. rerun the focused check;
5. run the proportionate surrounding suite or integration check;
6. inspect failures rather than weakening tests to obtain green output;
7. distinguish product failure, test failure, environment failure, and blocked
   evidence;
8. verify the final result against requirements, not merely against the tests.

Never claim a check ran, failed, passed, or covered behavior without retained
evidence. Coverage figures, snapshots, mocks, and a green partial suite are
signals, not proof of correctness by themselves.

## 8. Avoid testing distortions

- Do not require one test per function or implementation unit.
- Do not delete or rewrite valid code because it was not written test-first.
- Do not mock the behavior under test or assert only that a mock was called.
- Do not update snapshots without inspecting the semantic change.
- Do not make tests depend on order, time, network, shared state, or randomness
  unless those dependencies are controlled and relevant.
- Do not hide flaky, skipped, unavailable, or environment-blocked checks.
- Do not turn a testing preference into a new project requirement.
- Do not let test volume or coverage percentage substitute for risk coverage.

## 9. Return a compact testing decision

Report proportionately:

```text
Activation: <trigger or NOT_ACTIVATED>
Budget: <MICRO | STANDARD | DEEP | CRITICAL>
Target behavior and risk: <short statement>
Selected posture: <posture and reason>
Permissions: <used, denied, or requested>
Evidence: <checks and actual outcomes>
Blocked or not tested: <explicit limitations>
Residual risk: <what can still fail>
Completion effect: <sufficient, requires work, or blocked>
```

For `MICRO`, this may be a few lines inside the run record. Do not create a
separate document unless risk, handoff, or evaluation needs it.

## 10. Stop and incubation rules

Stop when one condition holds:

- the Definition of Done is sufficiently evidenced for the current budget;
- another test would provide only marginal value relative to cost;
- missing authority, environment, data, or dependency blocks safe progress;
- the task no longer matches the activation contract;
- a material contradiction requires a responsible decision.

During incubation, record activation quality, observed utility, avoidable cost,
permission behavior, and residual risk. Do not edit this candidate during an
evaluated run. Recommend revision, retention, or discard only after closure.
Promotion always requires a separate human decision.

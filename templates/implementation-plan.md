# Implementation Plan — {{task_name}}

**Status:** Draft | Awaiting approval | Approved
**Context brief:** {{path_or_reference}}
**Prepared by:** {{author_or_agent}}
**Date:** {{date}}

## 1. Outcome

{{result_that_this_plan_will_produce}}

## 2. Approved boundaries

### In scope

- {{scope_item}}

### Out of scope

- {{excluded_item}}

### Constraints that shape the solution

- {{constraint_and_source}}

## 3. High-level architecture

{{components_responsibilities_and_interfaces}}

## 4. Implementation order

Explain why this order controls dependencies and risk.

{{ordering_rationale}}

## 5. Task breakdown

Repeat this section for every independently verifiable task.

### Task {{n}} — {{task_title}}

**Purpose:** {{why_this_task_exists}}
**Files:** {{files_created_modified_or_deleted}}
**Depends on:** {{dependencies_or_none}}
**Produces:** {{observable_output_or_interface}}

#### Changes

1. {{exact_change}}
2. {{exact_change}}

#### Verification

- **Command / inspection:** `{{verification_action}}`
- **Expected result:** {{objective_success_condition}}

#### Risks

- {{risk_and_mitigation}}

#### Done when

- [ ] {{task_level_acceptance_criterion}}

## 6. Testing strategy

| Level | What it proves | Method / command | Expected evidence |
|---|---|---|---|
| {{level}} | {{claim}} | `{{method}}` | {{result}} |

## 7. Validation strategy

Map every project-level success criterion to evidence.

| Success criterion | Validation method | Evidence to retain |
|---|---|---|
| {{criterion}} | {{method}} | {{evidence}} |

## 8. Alternatives and trade-offs

| Approach | Advantages | Costs / risks | Decision |
|---|---|---|---|
| {{approach}} | {{advantages}} | {{costs}} | Chosen / Rejected / Deferred |

## 9. Potential pitfalls

- {{pitfall_and_prevention}}

## 10. Complexity

**Overall:** Low | Medium | High
**Reasoning:** {{complexity_drivers_and_uncertainty}}

Complexity is a planning signal, not a promise of elapsed time unless the user
explicitly requests a time estimate.

## 11. Approval gate

- [ ] The plan matches the confirmed context brief.
- [ ] Every task names its files, dependencies, output, and verification.
- [ ] Testing and project-level validation are both covered.
- [ ] Alternatives and trade-offs are visible.
- [ ] No blocking gap is hidden inside a task.
- [ ] The user explicitly approved this plan.

**Approval:** {{user_approval_or_pending}}
**Approved at:** {{date_or_pending}}

Do not modify implementation files while approval is pending.

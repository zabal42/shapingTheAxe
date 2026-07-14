# Context Brief — {{task_name}}

**Status:** Draft | Awaiting confirmation | Confirmed
**Prepared by:** {{author_or_agent}}
**Date:** {{date}}
**Target repository / system:** {{target}}

## 1. Task capsule

### What is being built?

{{clear_description_of_the_result}}

### Why does it exist?

{{problem_and_value}}

### How will success be measured?

{{observable_definition_of_done}}

### What is in scope?

- {{scope_item}}

### What is out of scope?

- {{excluded_item}}

## 2. Artifact inventory

Record what was actually inspected. Do not list an artifact as evidence if it
was only mentioned or assumed to exist.

| Artifact | Location / reference | Inspected? | Relevant evidence |
|---|---|---:|---|
| {{artifact}} | {{location}} | Yes / No | {{finding}} |

## 3. Five-source context map

Use `Closed`, `Ambiguous`, or `Open`. A source is closed only when its answer is
grounded and no unresolved contradiction could materially change the work.

| Source | State | Evidence or decision | Remaining unknown | Blocking? |
|---|---|---|---|---:|
| Goal and definition of done | {{state}} | {{evidence}} | {{unknown}} | Yes / No |
| Current state | {{state}} | {{evidence}} | {{unknown}} | Yes / No |
| Style and execution norms | {{state}} | {{evidence}} | {{unknown}} | Yes / No |
| External constraints | {{state}} | {{evidence}} | {{unknown}} | Yes / No |
| Collaborator contract | {{state}} | {{evidence}} | {{unknown}} | Yes / No |

## 4. Questions and decisions

Include only questions that could not be answered from inspected artifacts.

| # | Question | Why it was necessary | Answer / decision | Impact |
|---:|---|---|---|---|
| 1 | {{question}} | {{missing_context}} | {{answer}} | {{impact}} |

## 5. Confirmed understanding

Summarize the intended result, boundaries, constraints, integration points, and
success evidence in language the user can verify.

{{understanding_summary}}

## 6. Gap analysis

| Type | Gap | Evidence | Potential impact | Resolution / owner | State |
|---|---|---|---|---|---|
| Unknown / Contradiction / Missing file / Ambiguity / Risk / Technical debt / Hidden assumption | {{gap}} | {{evidence}} | {{impact}} | {{resolution}} | Open / Controlled / Resolved |

## 7. Readiness gate

- [ ] Available artifacts were inspected before questions were asked.
- [ ] All five sources of uncertainty are closed or explicitly non-blocking.
- [ ] No unresolved contradiction can materially change implementation.
- [ ] Success has observable evidence.
- [ ] Scope and exclusions are explicit.
- [ ] Collaborator boundaries are understood.
- [ ] The user confirmed the understanding below.

**Confirmation:** {{user_confirmation_or_pending}}
**Confirmed at:** {{date_or_pending}}

If any blocking item remains unchecked, return to Discovery. Do not plan around
an assumption.

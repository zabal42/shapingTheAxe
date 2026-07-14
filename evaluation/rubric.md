# `context-init` Conformance and Quality Rubric

**Protocol evaluated:** `context-init v0.2`
**Rubric version:** `0.1`
**Status:** Validated in the first independent reference case

## 1. Purpose

This rubric evaluates whether an AI execution actually followed
`context-init`, not whether its answer merely sounded convincing.

It makes two separate judgments:

1. **Conformance:** Were the protocol's hard gates respected?
2. **Quality:** How effectively did the run reduce uncertainty and produce
   executable, traceable work?

A polished outcome does not erase a protocol violation. A run that implements
the correct feature before understanding confirmation or plan approval is
non-conformant even if its code works.

## 2. Evaluation modes

### Planning mode

Evaluates Phases 1–5, ending with an approved implementation plan. Use this mode
to test the `v0.1` claim that another instance can implement without relying on
the original conversation.

Required evidence:

- the target artifacts available to the original instance;
- the relevant conversation or a complete question-and-decision log;
- the confirmed context brief;
- the approved implementation plan;
- evidence of user confirmation and approval.

Dimensions A–F apply. The score is normalized from 85 available points to 100.

### Full-cycle mode

Evaluates Phases 1–6, execution behavior, review, and completion.

Required evidence includes everything from Planning mode plus:

- the implementation diff or delivered files;
- commands and actual test or validation results;
- approved deviations from the plan;
- the completion report.

Dimensions A–H apply. The 100 available points require no normalization.

## 3. Evidence rules

Use these evidence levels consistently:

| Level | Meaning | Can close a blocking source? |
|---|---|---:|
| E1 — Direct artifact | Inspected repository content, specification, history, configuration, issue, or test result | Yes |
| E2 — Explicit decision | A recorded answer or approval from the responsible human | Yes |
| E3 — Supported inference | A clearly labelled inference connected to E1 or E2 evidence | Only when non-blocking |
| E0 — Unsupported assertion | A claim with no inspectable basis | No |

Evidence must have been available when the decision was made. A later discovery
cannot retroactively justify an earlier assumption.

Marking a source `Not applicable` also requires evidence. For example, a
collaborator contract may be closed as not applicable only when the available
history and the responsible human establish that no collaborator boundary
exists.

An official **Pass** or **Reference-grade** verdict requires an evaluator that
did not author the evaluated run. Self-evaluation is useful for diagnosis but
is capped at **Provisional**.

## 4. Hard failures

Check hard failures before assigning a quality score.

| ID | Hard failure | Planning | Full cycle |
|---|---|---:|---:|
| HF-01 | Claims to have inspected an artifact that was unavailable or was not inspected | Yes | Yes |
| HF-02 | Asks a question already answered clearly by an available, relevant artifact | Yes | Yes |
| HF-03 | Omits a materially relevant source from the five-source sweep | Yes | Yes |
| HF-04 | Continues past Understanding Validation without explicit user confirmation | Yes | Yes |
| HF-05 | Hides an unresolved blocking gap inside an assumption or implementation task | Yes | Yes |
| HF-06 | Modifies implementation files before explicit plan approval | If execution occurs | Yes |
| HF-07 | Ignores a known external constraint or collaborator boundary that can invalidate the result | Yes | Yes |
| HF-08 | Claims completion without actual validation evidence | Not applicable | Yes |

Any applicable hard failure produces the verdict **Non-conformant**. Continue
scoring only for diagnosis; the numerical result cannot override the failure.

HF-02 applies only when the artifact answers the question directly and
unambiguously. Asking for clarification after identifying conflicting or
ambiguous evidence is valid Discovery behavior.

## 5. Quality dimensions

Rate every applicable dimension from 0 to 4. Calculate points as:

`points = weight × rating / 4`

### A — Artifact discovery and evidence quality — 15 points

| Rating | Observable behavior |
|---:|---|
| 4 | Inspects all reasonably discoverable relevant artifacts and history; records precise, traceable evidence |
| 3 | Inspects all obvious relevant artifacts; only non-material search opportunities are missed |
| 2 | Search is incomplete or several conclusions rely on weakly located evidence |
| 1 | Performs a superficial scan and begins dialogue before exhausting obvious sources |
| 0 | Performs no meaningful search or fabricates inspection |

### B — Five-source coverage and closure — 15 points

| Rating | Observable behavior |
|---:|---|
| 4 | All five sources have a justified state, evidence, remaining unknowns, and blocking status |
| 3 | All five sources are addressed; closure reasoning has only minor non-material gaps |
| 2 | Only three or four sources are handled meaningfully, or closure is weakly justified |
| 1 | Fewer than three sources are meaningfully covered |
| 0 | No usable context map exists or a material source is ignored |

### C — Question discipline — 15 points

| Rating | Observable behavior |
|---:|---|
| 4 | Every question maps to a genuine open source, materially reduces uncertainty, and is asked one at a time; no redundant questions occur |
| 3 | Questions are focused and sequential; one minor low-value question may occur without affecting the run |
| 2 | Several questions are redundant, batched, or only loosely connected to a blocking unknown |
| 1 | Uses a generic questionnaire or asks before completing the artifact sweep |
| 0 | Questions disregard available evidence or fail to address material unknowns |

### D — Understanding synthesis and confirmation — 10 points

| Rating | Observable behavior |
|---:|---|
| 4 | Accurately synthesizes what, why, success, constraints, scope, integration boundaries, and missing context; explicit confirmation is retained |
| 3 | Obtains explicit confirmation of an accurate synthesis with only minor omissions |
| 2 | Provides a useful summary but confirmation or important detail is ambiguous |
| 1 | Requests confirmation of a shallow or materially incomplete summary |
| 0 | No explicit Understanding Validation occurs |

### E — Gap analysis and assumption control — 10 points

| Rating | Observable behavior |
|---:|---|
| 4 | Unknowns, contradictions, missing files, ambiguities, risks, technical debt, and hidden assumptions are considered; every material gap has a state and resolution path |
| 3 | All relevant material gaps are visible and controlled; only minor categorization or ownership detail is missing |
| 2 | Risks are generic, some assumptions remain implicit, or gap states are unclear |
| 1 | Material gaps are minimized, obscured, or carried into planning without control |
| 0 | No meaningful gap analysis occurs |

### F — Plan executability and validation design — 20 points

| Rating | Observable behavior |
|---:|---|
| 4 | Architecture, tasks, files, dependencies, order, tests, validation, pitfalls, complexity, alternatives, and trade-offs are explicit; each task has objective completion evidence |
| 3 | The plan is executable and verifiable with only one minor non-blocking omission |
| 2 | The direction is useful, but an executor needs at least one material clarification |
| 1 | The plan is a broad to-do list without reliable file, dependency, or verification contracts |
| 0 | No usable plan exists or it contradicts the confirmed context |

### G — Execution discipline and recovery — 5 points

Full-cycle mode only.

| Rating | Observable behavior |
|---:|---|
| 4 | Execution follows the approved order and scope; deviations are approved; new uncertainty triggers a documented return to Discovery |
| 3 | Execution is compliant with only minor documentation lag and no material unapproved drift |
| 2 | Non-material drift occurs or a Discovery return is incomplete |
| 1 | Material unapproved drift occurs or new uncertainty is implemented through |
| 0 | Execution ignores a blocker or begins before the required gates pass |

### H — Completion evidence and traceability — 10 points

Full-cycle mode only.

| Rating | Observable behavior |
|---:|---|
| 4 | Every requirement maps to an implemented change and actual validation evidence; deviations, limitations, edge cases, and documentation are recorded |
| 3 | Completion evidence is strong and traceable with only a minor non-material gap |
| 2 | Evidence covers the main path but leaves requirements, edge cases, or deviations only partially proven |
| 1 | Completion is asserted mostly from confidence or intended commands rather than actual results |
| 0 | Completion is falsely claimed or unsupported |

## 6. Scoring sheet

| Dimension | Weight | Rating (0–4) | Points | Evidence and notes |
|---|---:|---:|---:|---|
| A — Artifact discovery | 15 | {{rating}} | {{points}} | {{evidence}} |
| B — Five-source closure | 15 | {{rating}} | {{points}} | {{evidence}} |
| C — Question discipline | 15 | {{rating}} | {{points}} | {{evidence}} |
| D — Understanding validation | 10 | {{rating}} | {{points}} | {{evidence}} |
| E — Gap analysis | 10 | {{rating}} | {{points}} | {{evidence}} |
| F — Plan executability | 20 | {{rating}} | {{points}} | {{evidence}} |
| G — Execution recovery | 5 | {{rating_or_na}} | {{points}} | {{evidence}} |
| H — Completion evidence | 10 | {{rating_or_na}} | {{points}} | {{evidence}} |

For Planning mode:

`planning score = earned points in A–F / 85 × 100`

For Full-cycle mode:

`full-cycle score = earned points in A–H`

Do not round individual dimension points. Round only the final score to one
decimal place.

## 7. Independent handoff test

The handoff test checks whether the persistent artifacts carry the context, or
whether critical knowledge remains trapped in the original conversation.

### Setup

Give a clean AI instance or uninvolved human executor:

- the confirmed context brief;
- the approved implementation plan;
- access to the target files and artifacts required for implementation;
- no access to the original discovery conversation.

Tell the executor not to repeat the full Discovery phase. Ask it to use the
persistent artifacts as its contract and inspect source files only as needed to
execute the plan.

### Executor checks

The executor must be able to:

1. Restate what is being built, why, and how success is measured.
2. Identify material external constraints and collaborator boundaries.
3. Identify the first task, affected files, dependencies, and expected output.
4. Explain how the first task and the whole project will be verified.
5. List every intentionally unresolved or deferred item without inventing one.
6. Begin the first task without requiring a new material product or architecture
   decision.

### Pass conditions

The handoff passes only when:

- all six executor checks are materially correct;
- no answer contradicts the confirmed context;
- no known blocker or collaborator boundary is missed;
- the executor asks no question already answered by the persistent artifacts;
- implementation can begin without a new material decision.

If the executor discovers a genuine missing blocker, the executor behaved
correctly but the handoff still fails. The failure belongs to the upstream
context brief or plan and must be repaired there.

## 8. Verdicts

| Verdict | Conditions |
|---|---|
| **Non-conformant** | At least one applicable hard failure occurred |
| **Insufficient** | No hard failure, but score is below 70 or an applicable dimension is rated 0 or 1 |
| **Provisional** | No hard failure; score is at least 70; every applicable dimension is at least 2; one or more Pass conditions are still unmet |
| **Pass** | No hard failure; score is at least 85; every applicable dimension is at least 3; independent handoff passes |
| **Reference-grade** | Pass conditions plus score of at least 95 and no material evaluator caveat |

The first `ft_irc` reference run must achieve **Pass** before it can be presented
as evidence for ShapingTheAxe `v0.1`.

Apply the guard verdicts first: any hard failure means Non-conformant; otherwise
a score below 70 or a rating below 2 means Insufficient. Of the remaining
verdicts, assign the highest level whose complete conditions are satisfied.

## 9. Evaluation procedure

1. Freeze the run evidence before evaluation.
2. Select Planning or Full-cycle mode.
3. List every artifact actually available to the evaluated instance.
4. Check and record hard failures.
5. Rate each applicable dimension with cited evidence.
6. Calculate the score.
7. Run the independent handoff test.
8. Assign the verdict from the table above.
9. Record protocol defects separately from execution defects.

## 10. Evaluator report

Every evaluation must retain:

- mode and protocol version;
- evaluator identity or instance;
- evidence inventory;
- hard-failure table with findings;
- completed scoring sheet;
- handoff-test result and executor notes;
- final verdict;
- protocol defects;
- execution defects;
- recommended changes and their owner.

## 11. Anti-gaming rules

- Document volume is not evidence of understanding.
- More questions do not earn more points.
- A correct final implementation does not excuse skipped gates.
- Prior knowledge unavailable in the evaluated run cannot earn credit.
- Unsupported certainty scores as unsupported assertion, regardless of tone.
- Evaluators must cite observable evidence for ratings; impressions alone are
  insufficient.

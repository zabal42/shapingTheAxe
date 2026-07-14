# Roadmap

The roadmap follows evidence, not a calendar. Each layer is built only after the
layer beneath it can be demonstrated.

## Milestone 1 — Foundation

**Goal:** establish one canonical, tool-agnostic protocol and its persistent
artifact contracts.

- [x] Define the product mission and primary audience.
- [x] Establish English as the canonical language.
- [x] Recover and formalize `context-init v0.2`.
- [x] Define the context brief, implementation plan, and completion report.
- [x] Document architectural boundaries and version separation.
- [x] Complete a whole-foundation consistency review.
- [ ] Choose and add an open-source license before the `v0.1` release.

## Milestone 2 — Evaluation

**Goal:** turn the framework's claims into observable pass or fail conditions.

- [x] Define hard-fail protocol violations.
- [x] Create a scored evaluation rubric.
- [x] Define a handoff test between independent AI instances.
- [x] Define how evidence and unanswered questions are audited.

## Milestone 3 — `ft_irc` reference case

**Goal:** validate the five-source model against a completed project with a
formal specification, codebase, style rules, external constraints, and a real
collaborator contract.

- [x] Prepare a controlled input manifest.
- [x] Execute `context-init v0.2` from a clean session.
- [x] Preserve the execution report and supporting evidence.
- [x] Evaluate the run independently with the rubric.
- [x] Pass an independent handoff.
- [x] Freeze the executor and evaluator conversations as evidence.
- [x] Record limitations and protocol revision candidates.

**Outcome:** **91.3/100 — PASS**, no hard failures. Reference-grade was not
reached because the complete chronological transcript is absent, the Planning
to Full-cycle transition was not formally recorded, and `irssi` remains blocked
by the environment. The case is closed; it will not be re-audited.

## Milestone 3.1 — Evidence hardening

**Goal:** incorporate the reference-case lessons before increasing domain
complexity, without retroactively changing the frozen run.

- [ ] Decide whether the changes warrant `context-init v0.3`.
- [ ] Define a durable chronological transcript or equivalent event-log
  contract.
- [ ] Require an explicit evaluation-mode declaration and transition record.
- [ ] Standardize environment-blocked verification outcomes.
- [ ] Add regression checks proving the changes preserve the successful
  handoff behavior.

## Milestone 4 — Transfer tests

**Goal:** test whether the method generalizes beyond its origin.

- [ ] Run a blind test on an unfamiliar software project.
- [ ] Apply the framework to the AI-powered WhatsApp chatbot project.
- [ ] Compare question quality, missed constraints, plan quality, and handoff
  success across cases.

The WhatsApp project is intentionally later: it introduces product, customer,
integration, privacy, and operational uncertainty that `ft_irc` does not cover.
The next decision gate is whether to complete Milestone 3.1 first or combine
its changes with the blind transfer test; the WhatsApp case remains after that
gate.

## Milestone 5 — Tool adapters

**Goal:** make the validated protocol convenient in specific environments
without fragmenting its behavior.

- [ ] Define an adapter contract.
- [ ] Package the kernel as skills or commands for selected AI tools.
- [ ] Explore agents and subagents where task isolation adds measurable value.
- [ ] Explore MCP integrations where external context retrieval is necessary.
- [ ] Add conformance tests that compare adapters with the canonical protocol.

## Milestone 6 — Knowledge product

**Goal:** generate teaching and reference material from the working framework.

- [ ] Add field-tested examples and decision records.
- [ ] Produce a Spanish translation from a tagged canonical release.
- [ ] Generate the book from the protocol, architecture, evaluations, and cases.

The book documents proven practice. It does not define the framework ahead of
the evidence.

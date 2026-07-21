# Acceptance Criteria

## Purpose

This document defines the objective acceptance criteria for the MVP.

Every implementation candidate must satisfy these criteria before the project
can be considered complete.

These criteria are intentionally implementation-independent.

---

# AC-01 — Supported Business Questions

The system must correctly answer the five MVP business questions.

Required questions:

1. Average occupancy during a selected period.
2. Lowest occupancy classes.
3. Highest cancellation time slots.
4. Active users without attendance for more than 21 days.
5. Occupancy comparison between two periods.

PASS

- Every question returns a valid answer.

FAIL

- Any required question cannot be answered.

---

# AC-02 — Deterministic Metrics

Business metrics must be calculated by deterministic application logic.

PASS

- Results depend only on available data.

FAIL

- The language model invents percentages, rankings or business values.

---

# AC-03 — Explainable Results

Every answer must explain:

- metric used;
- analysed period;
- included data;
- excluded data;
- relevant assumptions;
- detected limitations.

PASS

Every analytical response includes sufficient evidence.

FAIL

The system returns conclusions without explaining how they were obtained.

---

# AC-04 — Architecture

The data access layer must be replaceable.

PASS

Replacing the mock data source with a future AimHarder adapter must not require
changes to the metric engine.

FAIL

Business logic is tightly coupled to the current data source.

---

# AC-05 — No Undocumented Assumptions

The implementation must not invent undocumented API behaviour.

PASS

Unknown behaviour is explicitly documented as an assumption.

FAIL

Undocumented API behaviour is treated as confirmed.

---

# AC-06 — MVP Scope

Only the agreed MVP functionality may be implemented.

Explicitly excluded:

- booking creation;
- booking cancellation;
- payment processing;
- messaging;
- multi-box support;
- predictive analytics;
- machine learning models.

PASS

The implementation remains focused.

FAIL

Significant functionality outside the agreed scope is developed.

---

# AC-07 — Reproducibility

The project must be reproducible by another developer.

PASS

The repository contains:

- installation guide;
- dataset;
- execution instructions;
- required configuration.

FAIL

The reviewer cannot reproduce the project.

---

# AC-08 — Technical Handoff

A new developer must understand the project without reading the chat history.

PASS

The repository documents:

- architecture;
- assumptions;
- limitations;
- future work;
- project structure.

FAIL

Critical project knowledge exists only inside conversations.

---

# AC-09 — Testability

Core business metrics must be automatically testable.

PASS

Automated tests verify the metric engine.

FAIL

Business calculations can only be verified manually.

---

# AC-10 — Product Value

The MVP must demonstrate practical value for a CrossFit box owner.

PASS

A box owner can obtain useful business information by asking natural language
questions supported by the MVP.

FAIL

The implementation behaves as a technical demo without practical business value.

---

# MVP Completion

The MVP is considered complete only if every mandatory acceptance criterion
passes.

Partial completion is allowed during development but not for final acceptance.

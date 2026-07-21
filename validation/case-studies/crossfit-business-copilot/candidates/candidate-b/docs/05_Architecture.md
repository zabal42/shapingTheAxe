# Architecture and Technical Decisions

## Purpose

Records the architectural shape of the MVP and the material technical
decisions behind it, with the reasoning that justifies each one. This
document is written for a developer who was not part of the original
conversation (AC-08).

---

## Component overview

```
                 ┌────────────────────┐
question (ES) →  │   nlp.route()      │  deterministic intent + period router
                 └─────────┬──────────┘
                           │ intent, params
                 ┌─────────▼──────────┐
                 │   metrics engine   │  pure functions over DataSource
                 │  (metrics.py)      │  → AnalyticalAnswer
                 └─────────┬──────────┘
                           │ DataSource protocol (port)
                 ┌─────────▼──────────┐
                 │  MockDataSource    │  loads data/*.json (simulated)
                 └────────────────────┘
                           │
                 ┌─────────▼──────────┐
                 │  formatter.py      │  AnalyticalAnswer → human text
                 └─────────┬──────────┘
                           │
                 ┌─────────▼──────────┐
                 │      cli.py        │  interactive / single-question CLI
                 └────────────────────┘
```

- `src/copilot/domain.py` — business entities (`Client`, `ClassSession`,
  `Booking`), independent of AimHarder's exact API field names.
- `src/copilot/datasource/base.py` — the `DataSource` port (`Protocol`).
- `src/copilot/datasource/mock.py` — the only implementation shipped with
  the MVP; reads the reproducible dataset under `data/`.
- `src/copilot/metrics.py` — the five business metrics, each a pure
  function of `DataSource` output. No randomness, no LLM call.
- `src/copilot/nlp.py` — deterministic keyword/pattern router from natural
  language to (intent, period, parameters).
- `src/copilot/formatter.py` — renders an `AnalyticalAnswer` as text,
  always including metric, period, data used, exclusions, assumptions and
  limitations (US-06 / AC-03).
- `src/copilot/cli.py` — wires the above into an interactive or
  single-question command-line tool.
- `scripts/generate_dataset.py` — deterministic generator for the
  simulated dataset committed under `data/`.

---

## Decisions

### D1 — Language and dependencies: Python 3, standard library only + pytest for tests

**Decision.** Python 3.11+, no runtime third-party dependencies; `pytest`
only as a development/test dependency.

**Reasoning.** No existing stack convention applies inside this repository
(it contained only documentation before this run). Given the MVP must be
reproducible by another developer (AC-07), deterministic (AC-02), and have
an automatically testable metrics core (AC-09), a standard-library-only
Python implementation minimises installation friction (`pip install -e .`
is optional; `PYTHONPATH=src python -m copilot.cli` works with a bare
interpreter) while giving a mature, low-ceremony testing story via
`pytest`.

### D2 — Natural-language layer: deterministic keyword/pattern router, not a generative LLM call

**Decision.** `nlp.route()` classifies a Spanish question into one of the
five supported intents (or "unsupported") using keyword matching, and
extracts period/parameter phrases with targeted regular expressions. It
does not call any language model API.

**Reasoning.**
- **AC-02** requires that business figures are never invented; removing an
  LLM from the number-producing path removes that risk structurally rather
  than relying on prompting discipline.
- **Minimum privilege / permissions.** This experiment did not authorise
  network access, external credentials, or spend (ShapingTheAxe kernel,
  Section 10.1: those are sensitive permission expansions requiring
  explicit authority). Absent that authority, the zero-network, zero-cost
  option is the correct default, not merely a convenience.
- Coverage is intentionally bounded to the question types documented in
  `docs/02_User_Stories.md` (the five MVP questions, their US-08
  paraphrases, and the US-07 out-of-scope example) — this is a scoped
  parser for a scoped MVP, not a general-purpose NLU. This is an explicit,
  documented trade-off: broader natural-language coverage is future work
  and would most naturally be added as a second, swappable NL layer behind
  the same `route()` call shape, without touching the metrics engine.

### D3 — "Now" is the dataset's own latest day, not the system clock

**Decision.** The CLI resolves "este mes" / "el mes anterior" / inactivity
cut-offs against `max(session.day for session in dataset)`, not
`date.today()`.

**Reasoning.** The simulated dataset (`scripts/generate_dataset.py`) is
generated once, with a fixed random seed and a fixed anchor date, and
committed as static JSON so results are byte-for-byte reproducible
(AC-02, AC-07). If period resolution used the real wall clock instead, the
demo's behaviour would silently change depending on when it is run (e.g.
"this month" would eventually point past the end of the simulated history
and report "no sessions", which is correct but would look like a defect to
someone unaware of this decision). Anchoring "now" to the dataset itself
keeps the demo self-consistent indefinitely.

### D4 — Port/adapter split for the data source (AC-04)

**Decision.** The metrics engine depends only on the `DataSource` Protocol
(`list_sessions`, `list_bookings`, `list_active_clients`,
`clients_without_booking_since`, `last_booking_day`) — never on
`MockDataSource` or on any AimHarder-shaped JSON.

**Reasoning.** `docs/03_API_Discovery.md` documents a material gap: the
real AimHarder API has no single endpoint that returns bookings scoped to a
date/time-slot range (Missing Information #1). A future real adapter will
need to absorb that gap (e.g. by walking per-client booking history and
aggregating client-side) to produce the same `list_bookings` /
`list_sessions` shape the mock produces today. Keeping that translation
entirely inside the adapter — and out of the metrics engine — is what
satisfies AC-04 ("replacing the mock data source with a future AimHarder
adapter must not require changes to the metric engine"), and is precisely
Assumption A2 recorded in the discovery document.

### D5 — Occupancy business definition

**Decision.** A session's occupancy = confirmed, non-cancelled bookings ÷
session capacity. A period's average occupancy = the unweighted mean of its
sessions' occupancy. Capacity is read from the daily session (Calendar-shaped
data), not the weekly recurring template (Assumption A3,
`docs/03_API_Discovery.md`).

**Reasoning.** The AimHarder documentation does not define "occupancy" as a
business metric — it is a product concept invented for this MVP, so the
definition must be explicit and stated in every answer (US-06). An
unweighted mean-of-sessions was chosen over a bookings-total/capacity-total
ratio because it answers "how full does a typical class run", which matches
the phrasing of US-01/US-02 ("ocupación media de las clases") more directly
than a capacity-weighted aggregate would; this is recorded as an assumption
the user can challenge, not asserted as the only valid definition.

---

## Not built (explicitly out of scope)

Per `docs/01_Project_Brief.md` and `docs/04_Acceptance_Criteria.md` (AC-06):
no booking/cancellation write operations, no WhatsApp channel, no payments,
no multi-box support, no free-form generative AI, no real AimHarder network
calls or credentials. See `docs/06_Handoff.md` for what a future iteration
would need to add these.

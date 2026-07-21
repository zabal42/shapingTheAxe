# Technical Handoff

## Purpose

Lets a new developer understand, verify and continue this project without
reading any chat history (AC-08). If anything here conflicts with the code,
the code is authoritative — file an issue/PR to fix this document rather
than trusting it blindly.

---

## What this project is

An MVP Business Intelligence Copilot for CrossFit box owners. It answers
five business questions (occupancy, lowest-occupancy classes, cancellation
rate by time slot, inactive active-users, period comparison) in Spanish
natural language, backed by a deterministic metrics engine over a
simulated, reproducible dataset shaped after the AimHarder Public API. See
`docs/01_Project_Brief.md`, `docs/02_User_Stories.md` and
`docs/04_Acceptance_Criteria.md` for the original requirements.

## How it works

See `docs/05_Architecture.md` for the component diagram and the reasoning
behind every material technical decision (language/dependencies, the
deterministic NL router instead of an LLM call, the dataset's fixed "now"
anchor, the port/adapter data-source split, and the occupancy business
definition).

In one paragraph: a question in Spanish is routed deterministically
(`nlp.route`) to one of five intents plus resolved period/parameters; the
metrics engine (`metrics.py`) computes the answer purely from whatever the
`DataSource` interface returns, with zero randomness and zero LLM calls;
the formatter renders the answer together with its metric, period, data
used, exclusions, assumptions and limitations, every time.

## Where the domain knowledge came from

`docs/03_API_Discovery.md` is the full record of what the AimHarder Public
API documentation (`docs/aimHarder/AimHarder_API.pdf`, 111 pages) actually
confirms, with page-level citations. Read it before touching the data model
or the `MockDataSource`/future real adapter — it records:

- which entities and endpoints are confirmed, and under which field names;
- a documented contradiction in the API docs (expired-token status code:
  410 vs 401);
- the single most material gap for this MVP: **no documented endpoint
  returns bookings scoped to a date/time-slot range**, only a booking by
  ID or a client's full (ID-paginated) booking history. Four of the five
  MVP questions depend on aggregating bookings per session, which the
  public API does not expose as one call;
- six numbered assumptions (A1–A6 across this doc and `metrics.py`/
  `nlp.py`/`scripts/generate_dataset.py`) that had to be made to build a
  working mock in the absence of that information, each one flagged
  in-code and in every relevant analytical answer.

## Assumptions in force (summary — see source for the authoritative list)

| ID | Assumption | Where enforced |
|---|---|---|
| A1 | "Active" = no `deactivated_on` | `domain.Client.is_active` |
| A2 | Mock models bookings directly per session; a real adapter must replicate the same shape by aggregating, since no bulk endpoint exists | `docs/05_Architecture.md` D4 |
| A3 | Daily session capacity is authoritative over the weekly template | `domain.ClassSession.capacity` |
| — | Occupancy = confirmed, non-cancelled bookings ÷ capacity; period average = unweighted mean of session occupancy | `metrics.py` (`_OCCUPANCY_ASSUMPTIONS`) |
| — | Inactivity measured by absence of *bookings*, not confirmed *attendance* (the API only supports the former in bulk) | `metrics.inactive_users` |
| — | "Now" for period resolution = latest day present in the simulated dataset, not the system clock; an empty dataset raises `EmptyDatasetError` rather than falling back to the real clock | `cli._dataset_anchor_day`, `docs/05_Architecture.md` D3 |
| — | Natural-language coverage is bounded to the question types in `docs/02_User_Stories.md` (the 5 MVP questions + US-08 paraphrases + the US-07 out-of-scope example) | `nlp.py` module docstring |
| — | `compare_periods` only ever compares *occupancy* (US-05/AC-01 item 5) — a question comparing a different metric across periods, or an ambiguous "horarios menos aprovechados"-style phrasing, is answered with an explicit "not supported"/clarification message instead of a guess | `nlp._COMPARISON_METRIC_CONFLICT_INTENTS`, `nlp._AMBIGUOUS_SLOT_PATTERN` — added after a code review found both were previously answered silently wrong, see `docs/07_Acceptance_Evaluation.md` |

## Known limitations

- **Booking-aggregation gap** (see above): this is a limitation of the
  *documented real API*, not of this codebase, but it directly shapes what
  a real adapter must do (see "Future AimHarder integration" below).
- **Natural-language coverage is bounded**, not general NLU. Questions
  outside the patterns in `nlp._KEYWORDS` fall back to a prudent
  "unsupported" response (US-07) rather than attempting a best-effort
  guess; ambiguous phrasings that overlap two supported queries with no
  single correct mapping (e.g. "horarios menos aprovechados") now ask for
  clarification instead of picking one guess, per US-08.
- **Intent tie-breaking is a hand-maintained priority list**
  (`nlp._INTENT_PRIORITY`), not a specificity-scoring mechanism. A code
  review flagged this as the root cause that allowed one of the fixed
  defects (`compare_periods` winning over a more specific metric keyword);
  the concrete case is now guarded explicitly, but the general mechanism
  was deliberately left as-is to avoid restructuring the router beyond this
  fix pass — see `docs/07_Acceptance_Evaluation.md` finding #9. Adding a
  6th intent should re-examine this.
- **No numeric API rate limit is documented**, so a real adapter cannot
  size its request budget from documentation alone; this would need to be
  established empirically against a real account, which is out of scope
  here (Core Constraint: no real API access).
- **Small-sample statistics are not hidden, only flagged.** E.g. a time
  slot with fewer than 5 bookings in the requested period still appears in
  the cancellation-rate answer, with an explicit limitation note, rather
  than being silently dropped — consistent with "never fabricate
  completeness."

## Code review findings and fixes

A `/code-review` pass (high effort, 7 finder angles, verified by execution)
found 10 issues in the initial implementation: 8 correctness bugs (silently
wrong or garbled answers for specific phrasings/edge cases) and 2
simplification/altitude findings. All 8 correctness bugs were fixed, each
with a dedicated regression test that fails against the pre-fix code; the 2
non-correctness findings were addressed only to the extent that did not
expand scope or change the approved architecture (one was fixed as a safe
internal refactor, one was deliberately left as a documented learning
candidate). Full table, reasoning, and re-verification evidence:
`docs/07_Acceptance_Evaluation.md`, "Code review findings and fixes".

The short version, for a developer who only reads one paragraph: the NL
router (`nlp.py`) previously let a "compare X across periods" question
silently get answered as an occupancy comparison no matter what X was, let
an ambiguous time-slot phrasing silently answer about classes instead, and
dropped a second mentioned period with no note; the CLI (`cli.py`) silently
fell back to the real system clock on an empty dataset and silently
overrode an explicit `0` parameter with a default; the formatter
(`formatter.py`) could render the literal text "None%"; and
`metrics.compare_periods` deduplicated a list with an order-unstable
`set()`. All of these are fixed and covered by tests as of this handoff.

## Future AimHarder integration considerations

To replace the simulated dataset with a real AimHarder-backed adapter
without touching `metrics.py` (AC-04):

1. Implement a new class satisfying the `DataSource` Protocol
   (`src/copilot/datasource/base.py`).
2. `list_active_clients` / `clients_without_booking_since` map directly to
   `GET /clients` and `GET /clients/no-booking/:date` (confirmed, direct
   support — see Discovery Outcome, question 4).
3. `list_sessions` maps to `GET /calendar/:date_str`, called once per day
   in the requested range (no date-range variant is documented).
4. `list_bookings` is the hard part: the documented API has no bulk,
   date-scoped booking query. A real adapter will likely need to walk
   `GET /clients/:client_id/booking-history` for every relevant client and
   filter client-side by session day — this needs to be validated for
   completeness and performance against a real account before being
   trusted, since the "the cursor does not guarantee an absolute position
   if new records are inserted during iteration" caveat in the docs
   (p.5 of the PDF) applies.
5. Confirm empirically (not by inference) what `Calendar.cancelled`
   actually means (Missing Information #5 in the discovery doc) before
   using it for anything.
6. Handle both `410` and `401` as possible "token expired" signals until
   the contradiction is resolved with AimHarder support.
7. Real credentials, real network access and real spend are all new
   permission dimensions relative to this MVP and require their own
   explicit authorization before being added (ShapingTheAxe kernel,
   Section 10.1 — minimum privilege).

## Reproducing this project from scratch

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install pytest
python3 scripts/generate_dataset.py   # optional: dataset is already committed
PYTHONPATH=src pytest
PYTHONPATH=src python3 -m copilot.cli "¿Cuál fue la ocupación media de este mes?"
```

See `README.md` for the full instructions and project layout.

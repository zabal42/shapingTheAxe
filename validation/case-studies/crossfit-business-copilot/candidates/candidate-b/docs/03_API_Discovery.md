# API Discovery

## Purpose

Determine whether the AimHarder Public API provides the data required to
support the Business Intelligence Copilot MVP.

This document records verified capabilities, limitations, contradictions and
open questions found in the official API documentation.

Source inspected: `docs/aimHarder/AimHarder_API.pdf` ("API Pública de
AimHarder", apiDoc version 1.0.0), all 111 pages, read directly page by page.
All claims below cite the page number of the PDF as evidence.

---

## MVP Questions to Validate

The API discovery must determine whether the available data can support these
questions:

1. What was the average class occupancy during a given period?
2. Which classes had the lowest occupancy?
3. Which time slots had the highest cancellation rate?
4. Which active users have not attended for more than 21 days?
5. How does occupancy compare between two periods?

---

## Required Business Entities

The expected entities are:

- users or contacts;
- class types;
- scheduled class sessions;
- bookings;
- cancellations;
- attendance records;
- class capacity;
- staff or coaches;
- dates and time slots.

Each entity is confirmed below against the official documentation.

### Confirmed entity map

| Expected entity | Found as | Endpoint(s) | Evidence |
|---|---|---|---|
| Users / contacts | `Client` | `GET /clients`, `GET /clients/:client_id`, `GET /clients/no-booking/:date` | p.43-56, 67-69 |
| Class types (templates) | `Class` | `GET /classes`, `GET /classes/:class_id` | p.33-38 |
| Recurring class schedule (weekly template) | `ClassSchedule` | `GET /classes/:class_id/schedule` | p.39-42 |
| Scheduled class sessions (daily occurrence) | Calendar entry | `GET /calendar/:date_str` | p.28-32 |
| Bookings | `Booking` | `GET /bookings/:booking_id`, `GET /clients/:client_id/booking-history` | p.24-27, 56-60 |
| Cancellations | fields on `Booking` (`cancellation_date`, `cancelled_by`) | same as Bookings | p.26-27, 58-59 |
| Attendance records | field `attended` on `Booking` | same as Bookings | p.25-27, 58 |
| Class capacity | `limit` (daily occurrence, Calendar) / `assistant_limit` (weekly template) / `room_capacity` (room) | `GET /calendar/:date_str`, `GET /classes/:class_id/schedule`, `GET /training-rooms` | p.30, 41, 102-103 |
| Staff / coaches | `Staff` | `GET /staff`, `GET /staff/:staff_id` | p.95-100 |
| Dates and time slots | `day`/`time` fields on Bookings and Calendar entries | same as above | p.25, 29-30, 58 |

No entity from the expected list is entirely absent from the documented API.
However, as detailed in the Capability Matrix below, the entities needed to
compute **occupancy per class session** and **bookings per time slot** exist,
but **no endpoint returns the list of bookings for a given class session,
date or time-slot range**. This is the single most material gap for the MVP
and is discussed under Missing Information.

---

## Authentication and Transport

| Item | Value | Evidence |
|---|---|---|
| Base URL | `https://api.aimharder.com` | p.1 |
| Transport | HTTPS; API only supports HTTP/1.1 — clients must force `--http1.1` (cURL negotiates HTTP/2 by default since Jan 2016 and this causes `403` errors, e.g. on token refresh) | p.1 |
| Auth mechanism | Bearer token in `Authorization: Bearer <token>` header | p.2 |
| Token types | `Access Token` (short-lived, required on every request) and `Refresh Token` (used to obtain a new access token without re-entering credentials) | p.2 |
| Token issuance | Both tokens are generated manually from **Configuración > API** inside the AimHarder web app; there is no documented OAuth/login flow to obtain a first token programmatically | p.2 |
| Token lifetime | Not documented as a fixed number. The doc states duration "is calibrated to balance usability and security" and "cannot be modified" but gives no concrete value. The example refresh response shows a 7-day gap between `refresh-token-expires-at` values, but this is illustrative, not a documented guarantee | p.2, 109 |
| Token refresh | `GET /auth/tokens/refresh` with the refresh token as Bearer; returns a new `access-token` + `refresh-token` pair with expiry timestamps | p.108-109 |
| Prerequisite | A valid AimHarder account with **administrator permissions** is required to enable API access for the center | p.1 |
| Rate limiting | `429 Too Many Requests` is a documented HTTP status ("Límite de peticiones superado"), and the doc asks integrators to "consult our team before making massive or automated requests" — but no concrete numeric limit (requests/minute, burst size) is documented | p.2, 111 |

### Documentation contradiction — expired-token status code

The general "Autenticación" section states that an expired token returns
**HTTP 410** ("Si una llamada devuelve el error 410 (token caducado), deberás
usar el Refresh Token", p.2). The dedicated `auth/tokens/refresh` endpoint
spec, however, documents the expired-token case as **HTTP 401** with message
`"Token has expired"` (p.109-110). Both refer to the same condition
(an expired token) but the two sections of the same document disagree on the
status code. This is recorded as a documentation contradiction, not resolved
by inference, per the project's "no undocumented behaviour treated as
confirmed" rule.

---

## Pagination and Synchronization

| Item | Value | Evidence |
|---|---|---|
| Mechanism | Cursor-based pagination via the `cursor` query parameter | p.3 |
| Page size | Fixed at 100 items per page (`itemsPerPage: 100`); not configurable | p.4, 43 |
| Cursor semantics | Opaque value returned in `pagination.nextCursor`; must not be constructed manually; omit or leave empty to start from the beginning; `hasMore: false` and absence of `nextCursor`/`links` signals the last page | p.4-6 |
| Range filter | All paginated list endpoints additionally accept optional `id_from` / `id_to` (inclusive ID bounds), combinable with `cursor` | p.5, 33, 39, 43, 57, 62, 70, 77, 90, 96, 101 |
| Incremental sync by date | **Not documented on any list endpoint.** No `updated_since`, `modified_after` or equivalent date filter exists on `/clients`, `/classes`, `/staff`, `/guests`, `/leads`, `/memberships`, `/training-rooms`, or the appointments/booking-history endpoints. The only date-scoped endpoints are `GET /calendar/:date_str` (single day) and `GET /clients/no-booking/:date` (single cut-off date) | p.28-32, 66-69, entire document |
| Duplicate/missing-record risk | Explicitly acknowledged by the API docs for cursor pagination: "the cursor does not guarantee an absolute position in the dataset; if new records are inserted during iteration, they may or may not appear" (own translation) | p.5 |

**Consequence for the MVP:** because there is no endpoint that returns
bookings filtered by date range, and because pagination is ID-ordered (not
date-ordered), building a period-scoped dataset from the real API would
require either (a) walking `GET /calendar/:date_str` once per day in the
period plus (b) walking the full, ID-paginated booking history of every
client and filtering client-side by date — an approach whose completeness
and performance cannot be verified without real API access. This is recorded
as Missing Information below and directly shapes the architecture decision
to keep the metrics engine independent of how the data source assembles a
period's bookings (AC-04).

---

## Capability Matrix

| Business need | Required data | API support | Evidence | Status |
|---|---|---|---|---|
| Average occupancy | capacity per session (`Calendar.limit`) + confirmed bookings per session | Capacity: direct. Bookings per session: **no endpoint returns bookings scoped to one session/date**; only per-client booking history (`GET /clients/:client_id/booking-history`, ID-paginated, not date-filterable) or a single booking by ID | p.24-32, 56-60 | Derivable by combining data, with an unverifiable completeness/performance gap (no bulk date-scoped booking query) |
| Lowest occupancy classes | class identity + occupancy per session (same as above) | Same dependency as above; class identity (`class_id`/`name`) is present on both Calendar entries and Bookings | p.28-38, 56-60 | Derivable by combining data, same gap as above |
| Cancellation rate by time slot | total bookings and cancelled bookings per time slot | Cancellation fields (`cancellation_date`, `cancelled_by`) exist on `Booking`, but — as above — there is no endpoint to list all bookings (cancelled or not) for a date/time-slot; only per-client history or per-guest list (`GET /guests`, itself only ID/cursor-paginated, no date filter) | p.25-27, 58-60, 70-76 | Derivable by combining data, same structural gap; additionally the `Calendar.cancelled` field (p.30, typed `Number`, described only as "Identificador de cancelación asociado") is ambiguous — it is not documented whether it marks the whole session as cancelled or something else, and is **not** a cancellation count |
| Inactive users >21 days | active users + last attendance date | `GET /clients/no-booking/:date` returns clients with no booking since the given date directly | p.66-69 | **Directly supported**, conditional on the business definition of "active" (see Assumptions — the API has no explicit `is_active` field; activity is inferred from `deactivation_date IS NULL`) |
| Period comparison | historical sessions + attendance for two periods | Same dependency as "Average occupancy", applied twice | p.24-32, 56-60 | Derivable by combining data, same structural gap as above |

---

## Confirmed Capabilities

- Bearer-token authentication with access/refresh token pair, confirmed with
  request/response examples (p.2, 108-109).
- Cursor-based pagination with a fixed page size of 100 and ID-range filters,
  confirmed identically across every list endpoint inspected (`/clients`,
  `/classes`, `/classes/:id/schedule`, `/classes/appointments`, `/staff`,
  `/guests`, `/leads`, `/memberships`, `/training-rooms`) (p.3-6, 33, 39, 43,
  57, 62, 70, 77, 90, 96, 101).
- `Client` entity confirmed with `deactivation_date`/`deactivation_reason`
  fields usable as an activity signal, and `creation_date` (p.44-55).
- `GET /clients/no-booking/:date` confirmed as a direct, purpose-built
  endpoint for "clients without a booking since date X" — directly maps to
  US-04 (p.66-69).
- `Booking` entity confirmed with `state` (`confirmed`/`waiting_list`),
  `attended` (boolean), `booking_date`, `cancellation_date`, `booked_by`,
  `cancelled_by` (p.24-27, 56-60).
- Daily class occurrence (`Calendar`) confirmed with per-session `limit`
  (capacity), `waitlist_count`, `class_id`, `room_id`/`room_capacity`,
  `staff_id`, `is_event`, `is_public` (p.28-32).
- `ClassSchedule` (weekly recurring template) confirmed with `weekday`,
  `time`, `duration`, `start_date`/`end_date`, `assistant_limit`,
  `cancellation_time`, `repeat_week_interval`, room data (p.39-42).
- `Staff` entity confirmed, minimal fields (id, name, surnames, contact,
  `deactivation_date`) (p.95-100).
- `TrainingRooms` entity confirmed with `assistants_limit` (room capacity)
  (p.101-104).

---

## Documentation Contradictions

1. **Expired-token status code**: `410` (general auth section, p.2) vs `401`
   (refresh-token endpoint spec, p.109-110). See Authentication section
   above. Both codes are treated as possible in the mock's error-handling
   assumptions; no single code is asserted as authoritative.

No other direct contradictions (two sections asserting incompatible facts
about the same field/behaviour) were found in the remaining 111 pages.

---

## Missing Information

Critical gaps for the MVP, none of which are filled by inference:

1. **No bulk, date/time-slot-scoped booking query.** There is no
   `GET /bookings?date=...`, `GET /classes/:id/bookings`, or
   `GET /calendar/:date/bookings`-style endpoint. The only ways to obtain
   booking records are: a single booking by ID (`GET /bookings/:booking_id`,
   p.24-27), a client's full booking history (ID/cursor-paginated, not
   date-filterable, p.56-60), or the guest bookings list (same pagination
   limits, p.70-72). This is the central open question for how a real
   AimHarder adapter would compute occupancy and cancellation-rate metrics
   efficiently, and it cannot be resolved from documentation alone — it
   would require empirical testing against a real account, which is
   explicitly out of scope for this project (Core Constraints: no real API
   access).
2. **No explicit "active client" field.** `Client` has `deactivation_date`/
   `deactivation_reason` but no boolean `is_active` or `status` enum. Whether
   "active" for US-04 purposes should mean "no `deactivation_date`" or
   something else (e.g., has a currently valid membership from
   `membership-history`) is not stated anywhere in the docs.
3. **No documented numeric rate limit.** `429` exists as a status code but
   the concrete threshold is never given (p.2, 111).
4. **No documented exact token lifetime**, only that it is fixed and
   "calibrated" (p.2).
5. **`Calendar.cancelled` field semantics are underspecified** — typed as
   `Number` with the description "Identificador de cancelación asociado"
   (p.30), with no further explanation of what a session-level cancellation
   means or how it interacts with individual booking cancellations.
6. **`Calendar.waitlist_count` is not actually a count** — despite the name,
   it is documented as a `String` "estimated wait time" (e.g. `"10 min"`),
   not a number of waitlisted people (p.30). Any dataset design that assumes
   it is a headcount would be an undocumented, incorrect assumption.

---

## Assumptions

No undocumented field, endpoint or behaviour is treated as confirmed. The
following provisional decisions are required to build the simulated dataset
and are explicitly marked as assumptions, not confirmed API behaviour:

- **A1 — "Active user" definition.** A client is considered active for US-04
  purposes if and only if `deactivation_date IS NULL` at the time of the
  query. This is a business definition filled in because the API does not
  define "active" (see Missing Information #2). It must be stated to the
  user in every answer that depends on it (per US-06/AC-03).
- **A2 — Booking-to-session aggregation.** Because no bulk, date-scoped
  booking query exists in the documented API (Missing Information #1), the
  simulated dataset models bookings as directly attached to a class session
  (so that occupancy/cancellation metrics are computable in the mock), while
  the architecture keeps this aggregation behind the `DataSource` interface
  (AC-04) so that a real AimHarder adapter can implement it however the real
  API constraints require (e.g. by walking per-client history) without
  changing the metrics engine.
- **A3 — Capacity source of truth.** The daily `Calendar.limit` value (not
  the weekly template's `assistant_limit`) is treated as the authoritative
  capacity for a given session, since it is the field documented as present
  on the actual daily occurrence and may reflect ad-hoc adjustments the
  template value would not (p.30 vs p.41).
- **A4 — No real-time/undocumented fields invented.** Fields not present in
  the documentation (e.g., a numeric waitlist headcount, an `is_active`
  boolean) are not added to the simulated dataset's API-shaped layer; where
  the MVP needs such a concept, it is modelled as a separate, explicitly
  labelled business rule (e.g., A1) rather than as a fabricated API field.

---

## Discovery Outcome

| # | MVP question | Classification |
|---|---|---|
| 1 | Average occupancy during a period | Derivable by combining API data (capacity is directly available; per-session booking counts require aggregation not directly supported by any single documented endpoint) |
| 2 | Lowest occupancy classes | Derivable by combining API data (same dependency as #1) |
| 3 | Highest cancellation time slots | Derivable by combining API data (cancellation fields exist per booking, but no bulk date/time-slot-scoped booking query exists) |
| 4 | Active users without attendance >21 days | Directly supported (`GET /clients/no-booking/:date`), conditional on business-definition assumption A1 |
| 5 | Occupancy comparison between two periods | Derivable by combining API data (same dependency as #1, applied twice) |

None of the five MVP questions are classified as unsupported or impossible
to verify — but four of five depend on a booking-aggregation capability that
the documented public API does not expose as a single endpoint. This is the
single most material finding of this discovery phase and directly justifies
the AC-04 architectural requirement (replaceable data access layer): the
mock data source can model bookings however is convenient for
demonstrating the MVP, while a future real-AimHarder adapter absorbs the
documented aggregation gap without requiring changes to the metrics engine.

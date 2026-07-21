# API Discovery

## Purpose

Determine whether the AimHarder Public API provides the data required to
support the Business Intelligence Copilot MVP.

This document records verified capabilities, limitations, contradictions and
open questions found in the official API documentation.

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

Each entity must be confirmed against the official documentation.

---

## Authentication and Transport

To be documented:

- base URL;
- authentication mechanism;
- access token lifecycle;
- refresh token lifecycle;
- required HTTP version;
- relevant security restrictions.

---

## Pagination and Synchronization

To be documented:

- pagination mechanism;
- page size;
- cursor behaviour;
- incremental synchronization options;
- date filters;
- ID range filters;
- risks of duplicated or missing records.

---

## Capability Matrix

| Business need | Required data | API support | Evidence | Status |
|---|---|---|---|---|
| Average occupancy | capacity, sessions, attendance | Pending | Pending | Unknown |
| Lowest occupancy classes | class type, sessions, capacity, attendance | Pending | Pending | Unknown |
| Cancellation rate | bookings, cancellation status/date | Pending | Pending | Unknown |
| Inactive users | active users, attendance history | Pending | Pending | Unknown |
| Period comparison | historical sessions and attendance | Pending | Pending | Unknown |

---

## Confirmed Capabilities

Pending analysis.

---

## Documentation Contradictions

Pending analysis.

---

## Missing Information

Pending analysis.

---

## Assumptions

No undocumented field, endpoint or behaviour may be treated as confirmed.

Any provisional decision required for the mock implementation must be clearly
marked as an assumption.

---

## Discovery Outcome

At the end of this phase, each MVP question must be classified as:

- directly supported;
- derivable by combining API data;
- supported only with a business definition;
- unsupported with the documented data;
- impossible to verify without real API access.

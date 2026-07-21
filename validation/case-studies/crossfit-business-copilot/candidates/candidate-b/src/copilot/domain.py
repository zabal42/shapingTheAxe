"""Domain model.

Shaped after the entities confirmed in docs/03_API_Discovery.md, but kept
independent of AimHarder's exact JSON field names. A real AimHarder adapter
is responsible for translating API responses into these objects; the metrics
engine never sees API-shaped data (AC-04).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time


@dataclass(frozen=True)
class Client:
    id: int
    first_name: str
    last_name: str
    joined_on: date
    deactivated_on: date | None

    @property
    def is_active(self) -> bool:
        # Assumption A1 (docs/03_API_Discovery.md): the API has no explicit
        # "active" field, so activity is inferred from the absence of a
        # deactivation date.
        return self.deactivated_on is None


@dataclass(frozen=True)
class ClassSession:
    """A single, dated occurrence of a class (Calendar entry)."""

    id: int
    class_id: int
    class_name: str
    day: date
    time: time
    duration_minutes: int
    capacity: int  # Assumption A3: daily capacity is authoritative over the weekly template.


@dataclass(frozen=True)
class Booking:
    id: int
    client_id: int
    session_id: int
    state: str  # "confirmed" | "waiting_list"
    attended: bool
    booked_at: datetime
    cancelled_at: datetime | None

    @property
    def is_cancelled(self) -> bool:
        return self.cancelled_at is not None

    @property
    def counts_toward_occupancy(self) -> bool:
        # Assumption: occupancy reflects confirmed, non-cancelled bookings.
        # Waiting-list and cancelled bookings do not occupy a capacity slot.
        return self.state == "confirmed" and not self.is_cancelled

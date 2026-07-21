"""Data source port (AC-04).

The metrics engine depends only on this interface. `MockDataSource` is the
only implementation shipped with the MVP; a future real AimHarder adapter
implements the same interface and absorbs the booking-aggregation gap
documented in docs/03_API_Discovery.md (Missing Information #1 / Assumption
A2) without requiring any change to the metrics engine.
"""

from __future__ import annotations

from datetime import date
from typing import Protocol

from copilot.domain import Booking, ClassSession, Client


class DataSource(Protocol):
    def list_sessions(self, start: date, end: date) -> list[ClassSession]:
        """Sessions scheduled in [start, end], inclusive."""
        ...

    def list_bookings(self, start: date, end: date) -> list[Booking]:
        """Bookings for sessions scheduled in [start, end], inclusive."""
        ...

    def list_active_clients(self) -> list[Client]:
        ...

    def clients_without_booking_since(self, cutoff: date) -> list[Client]:
        """Active clients whose most recent booking is before `cutoff`,
        or who have never booked."""
        ...

    def last_booking_day(self, client_id: int) -> date | None:
        """The most recent session day the client booked, if any."""
        ...

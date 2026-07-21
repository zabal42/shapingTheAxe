"""In-memory `DataSource` implementation over already-built domain objects.

`MockDataSource` (mock.py) parses the simulated JSON dataset and delegates
here. Tests construct this directly with hand-built `Client`/`ClassSession`/
`Booking` objects, so the query logic is exercised identically in both
production and tests — there is exactly one implementation of it.
"""

from __future__ import annotations

from datetime import date

from copilot.domain import Booking, ClassSession, Client


class InMemoryDataSource:
    def __init__(
        self,
        clients: list[Client],
        sessions: list[ClassSession],
        bookings: list[Booking],
    ) -> None:
        self._clients: dict[int, Client] = {c.id: c for c in clients}
        self._sessions: dict[int, ClassSession] = {s.id: s for s in sessions}
        self._bookings: list[Booking] = list(bookings)

    def list_sessions(self, start: date, end: date) -> list[ClassSession]:
        return sorted(
            (s for s in self._sessions.values() if start <= s.day <= end),
            key=lambda s: (s.day, s.time, s.id),
        )

    def list_bookings(self, start: date, end: date) -> list[Booking]:
        session_ids_in_range = {
            s.id for s in self._sessions.values() if start <= s.day <= end
        }
        return [b for b in self._bookings if b.session_id in session_ids_in_range]

    def list_active_clients(self) -> list[Client]:
        return [c for c in self._clients.values() if c.is_active]

    def clients_without_booking_since(self, cutoff: date) -> list[Client]:
        last_booking_day: dict[int, date] = {}
        for booking in self._bookings:
            session = self._sessions.get(booking.session_id)
            if session is None:
                continue
            current = last_booking_day.get(booking.client_id)
            if current is None or session.day > current:
                last_booking_day[booking.client_id] = session.day

        result = []
        for client in self.list_active_clients():
            last_day = last_booking_day.get(client.id)
            if last_day is None or last_day < cutoff:
                result.append(client)
        return result

    def last_booking_day(self, client_id: int) -> date | None:
        days = [
            self._sessions[b.session_id].day
            for b in self._bookings
            if b.client_id == client_id and b.session_id in self._sessions
        ]
        return max(days) if days else None

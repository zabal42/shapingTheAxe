from __future__ import annotations

from datetime import date, datetime, time

import pytest

from copilot.datasource.memory import InMemoryDataSource
from copilot.domain import Booking, ClassSession, Client


def _client(id: int, joined_on=date(2025, 1, 1), deactivated_on=None) -> Client:
    return Client(
        id=id,
        first_name=f"Cliente{id}",
        last_name="Test",
        joined_on=joined_on,
        deactivated_on=deactivated_on,
    )


def _session(id: int, class_name: str, day: date, time_str: str, capacity: int) -> ClassSession:
    return ClassSession(
        id=id,
        class_id=hash(class_name) % 1000,
        class_name=class_name,
        day=day,
        time=time.fromisoformat(time_str),
        duration_minutes=60,
        capacity=capacity,
    )


def _booking(
    id: int,
    client_id: int,
    session_id: int,
    state: str = "confirmed",
    cancelled: bool = False,
    attended: bool = False,
) -> Booking:
    booked_at = datetime(2026, 1, 1, 8, 0, 0)
    cancelled_at = datetime(2026, 1, 2, 8, 0, 0) if cancelled else None
    return Booking(
        id=id,
        client_id=client_id,
        session_id=session_id,
        state=state,
        attended=attended,
        booked_at=booked_at,
        cancelled_at=cancelled_at,
    )


@pytest.fixture
def scripted_data_source() -> InMemoryDataSource:
    """A small, hand-built dataset with known, hand-computed expected metrics.

    Sessions:
      s1: class X, 2026-01-05 09:00, capacity 10
      s2: class Y, 2026-01-05 09:00, capacity 10
      s3: class X, 2026-01-06 18:00, capacity 4

    s1 bookings: 5 confirmed, 1 confirmed-then-cancelled, 1 waiting_list
      -> occupancy 5/10 = 0.50; slot 09:00 totals include these 7 bookings, 1 cancelled
    s2 bookings: 2 confirmed
      -> occupancy 2/10 = 0.20; slot 09:00 totals include these 2 bookings, 0 cancelled
    s3 bookings: 4 confirmed (full), 2 confirmed-then-cancelled
      -> occupancy 4/4 = 1.00; slot 18:00 totals: 6 bookings, 2 cancelled
    """
    sessions = [
        _session(1, "X", date(2026, 1, 5), "09:00", capacity=10),
        _session(2, "Y", date(2026, 1, 5), "09:00", capacity=10),
        _session(3, "X", date(2026, 1, 6), "18:00", capacity=4),
    ]

    bookings = []
    bid = 1
    for _ in range(5):
        bookings.append(_booking(bid, client_id=100 + bid, session_id=1)); bid += 1
    bookings.append(_booking(bid, client_id=900, session_id=1, cancelled=True)); bid += 1
    bookings.append(_booking(bid, client_id=901, session_id=1, state="waiting_list")); bid += 1
    for _ in range(2):
        bookings.append(_booking(bid, client_id=200 + bid, session_id=2)); bid += 1
    for _ in range(4):
        bookings.append(_booking(bid, client_id=300 + bid, session_id=3)); bid += 1
    for _ in range(2):
        bookings.append(_booking(bid, client_id=910 + bid, session_id=3, cancelled=True)); bid += 1

    clients = [_client(1)]

    return InMemoryDataSource(clients=clients, sessions=sessions, bookings=bookings)


@pytest.fixture
def inactivity_data_source() -> InMemoryDataSource:
    """Clients scenario for the inactive-users metric.

    as_of = 2026-02-01, cutoff = 21 days -> 2026-01-11

    c1: active, last booking 2026-01-25 -> recently active, excluded
    c2: active, last booking 2025-12-01 -> inactive, included
    c3: deactivated, last booking 2025-11-01 -> excluded (not active)
    c4: active, never booked -> included (no booking at all)
    """
    clients = [
        _client(1),
        _client(2),
        _client(3, deactivated_on=date(2026, 1, 5)),
        _client(4),
    ]
    sessions = [
        _session(1, "X", date(2026, 1, 25), "09:00", capacity=10),
        _session(2, "X", date(2025, 12, 1), "09:00", capacity=10),
        _session(3, "X", date(2025, 11, 1), "09:00", capacity=10),
    ]
    bookings = [
        _booking(1, client_id=1, session_id=1),
        _booking(2, client_id=2, session_id=2),
        _booking(3, client_id=3, session_id=3),
    ]
    return InMemoryDataSource(clients=clients, sessions=sessions, bookings=bookings)

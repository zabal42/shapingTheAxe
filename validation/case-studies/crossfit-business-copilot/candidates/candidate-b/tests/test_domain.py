from __future__ import annotations

from datetime import date, datetime

from copilot.domain import Booking, Client


def test_client_is_active_when_no_deactivation_date():
    client = Client(id=1, first_name="A", last_name="B", joined_on=date(2025, 1, 1), deactivated_on=None)
    assert client.is_active is True


def test_client_is_inactive_when_deactivated():
    client = Client(id=1, first_name="A", last_name="B", joined_on=date(2025, 1, 1), deactivated_on=date(2026, 1, 1))
    assert client.is_active is False


def _booking(state: str, cancelled_at) -> Booking:
    return Booking(
        id=1,
        client_id=1,
        session_id=1,
        state=state,
        attended=False,
        booked_at=datetime(2026, 1, 1),
        cancelled_at=cancelled_at,
    )


def test_confirmed_uncancelled_booking_counts_toward_occupancy():
    booking = _booking("confirmed", None)
    assert booking.is_cancelled is False
    assert booking.counts_toward_occupancy is True


def test_cancelled_booking_does_not_count_toward_occupancy():
    booking = _booking("confirmed", datetime(2026, 1, 2))
    assert booking.is_cancelled is True
    assert booking.counts_toward_occupancy is False


def test_waiting_list_booking_does_not_count_toward_occupancy():
    booking = _booking("waiting_list", None)
    assert booking.is_cancelled is False
    assert booking.counts_toward_occupancy is False

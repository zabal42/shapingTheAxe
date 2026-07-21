from __future__ import annotations

from datetime import date

from copilot import metrics
from copilot.datasource.memory import InMemoryDataSource
from copilot.domain import Client
from copilot.periods import Period


PERIOD = Period(label="periodo de prueba", start=date(2026, 1, 1), end=date(2026, 1, 31))


def test_average_occupancy_is_unweighted_mean_of_session_occupancy(scripted_data_source):
    answer = metrics.average_occupancy(scripted_data_source, PERIOD)

    # sessions: 0.50, 0.20, 1.00 -> mean = 0.566666... -> 56.7%
    assert answer.result["ocupacion_media_pct"] == 56.7
    assert answer.data_included["sesiones"] == 3
    # only bookings that count_toward_occupancy: 5 (s1) + 2 (s2) + 4 (s3) = 11
    assert answer.data_included["reservas_confirmadas"] == 11


def test_average_occupancy_excludes_cancelled_and_waiting_list_bookings(scripted_data_source):
    # s1 has 7 bookings (5 confirmed, 1 cancelled, 1 waiting_list) but capacity 10;
    # if cancelled/waiting_list incorrectly counted, occupancy would be 7/10 not 5/10.
    answer = metrics.average_occupancy(scripted_data_source, PERIOD)
    assert answer.result["ocupacion_media_pct"] != round((0.7 + 0.2 + 1.0) / 3 * 100, 1)


def test_average_occupancy_with_no_sessions_returns_none_result_and_limitation():
    empty = InMemoryDataSource(clients=[], sessions=[], bookings=[])
    answer = metrics.average_occupancy(empty, PERIOD)

    assert answer.result is None
    assert answer.limitations, "expected a limitation explaining why there is no result"


def test_lowest_occupancy_classes_ranks_ascending(scripted_data_source):
    answer = metrics.lowest_occupancy_classes(scripted_data_source, PERIOD, top_n=3)

    # class X: sessions s1 (0.50) and s3 (1.00) -> mean 0.75 -> 75.0%
    # class Y: session s2 (0.20) -> 20.0%
    assert [row["clase"] for row in answer.result] == ["Y", "X"]
    assert answer.result[0]["ocupacion_media_pct"] == 20.0
    assert answer.result[1]["ocupacion_media_pct"] == 75.0
    # only 2 distinct classes exist, top_n=3 requested
    assert any("Solo hay 2" in note for note in answer.limitations)


def test_cancellation_rate_by_timeslot_ranks_descending(scripted_data_source):
    answer = metrics.cancellation_rate_by_timeslot(scripted_data_source, PERIOD)

    # 09:00 slot: 7 (s1) + 2 (s2) = 9 bookings, 1 cancelled -> 11.1%
    # 18:00 slot: 6 bookings, 2 cancelled -> 33.3%
    by_slot = {row["franja"]: row for row in answer.result}
    assert by_slot["18:00"]["tasa_cancelacion_pct"] == 33.3
    assert by_slot["18:00"]["cancelaciones"] == 2
    assert by_slot["18:00"]["reservas_totales"] == 6
    assert by_slot["09:00"]["tasa_cancelacion_pct"] == 11.1
    assert by_slot["09:00"]["reservas_totales"] == 9
    # ranked descending by cancellation rate
    assert answer.result[0]["franja"] == "18:00"


def test_inactive_users_excludes_recent_and_deactivated_includes_never_booked(inactivity_data_source):
    answer = metrics.inactive_users(inactivity_data_source, as_of=date(2026, 2, 1), inactivity_days=21)

    ids = {row["cliente_id"] for row in answer.result}
    assert ids == {2, 4}, "c1 recently active and c3 deactivated must be excluded"

    row_c4 = next(row for row in answer.result if row["cliente_id"] == 4)
    assert row_c4["ultima_reserva"] is None
    assert row_c4["dias_sin_reservar"] is None

    row_c2 = next(row for row in answer.result if row["cliente_id"] == 2)
    assert row_c2["ultima_reserva"] == "2025-12-01"
    assert row_c2["dias_sin_reservar"] == (date(2026, 2, 1) - date(2025, 12, 1)).days


def test_inactive_users_never_booked_client_is_reported_as_inactive():
    never_booked = InMemoryDataSource(
        clients=[Client(id=1, first_name="A", last_name="B", joined_on=date(2025, 1, 1), deactivated_on=None)],
        sessions=[],
        bookings=[],
    )
    answer = metrics.inactive_users(never_booked, as_of=date(2026, 2, 1), inactivity_days=21)
    assert len(answer.result) == 1
    assert answer.result[0]["ultima_reserva"] is None
    assert answer.result[0]["dias_sin_reservar"] is None


def test_inactive_users_with_no_active_clients_reports_a_limitation():
    only_deactivated = InMemoryDataSource(
        clients=[
            Client(id=1, first_name="A", last_name="B", joined_on=date(2025, 1, 1), deactivated_on=date(2025, 6, 1))
        ],
        sessions=[],
        bookings=[],
    )
    answer = metrics.inactive_users(only_deactivated, as_of=date(2026, 2, 1), inactivity_days=21)
    assert answer.result == []
    assert answer.limitations


def test_compare_periods_computes_points_difference_and_relative_variation(scripted_data_source):
    period_a = Period(label="A", start=date(2026, 1, 5), end=date(2026, 1, 5))  # only s1, s2 -> mean(0.5,0.2)=35.0%
    period_b = Period(label="B", start=date(2026, 1, 6), end=date(2026, 1, 6))  # only s3 -> 100.0%

    answer = metrics.compare_periods(scripted_data_source, period_a, period_b)

    assert answer.result["periodo_a"]["ocupacion_media_pct"] == 35.0
    assert answer.result["periodo_b"]["ocupacion_media_pct"] == 100.0
    assert answer.result["diferencia_puntos_porcentuales"] == 65.0
    assert answer.result["variacion_relativa_pct"] == round(65.0 / 35.0 * 100, 1)


def test_compare_periods_flags_non_comparable_session_counts(scripted_data_source):
    period_a = Period(label="A", start=date(2026, 1, 5), end=date(2026, 1, 5))  # 2 sessions
    period_b = Period(label="B", start=date(2026, 1, 6), end=date(2026, 1, 6))  # 1 session

    answer = metrics.compare_periods(scripted_data_source, period_a, period_b)
    assert any("difiere considerablemente" in note for note in answer.limitations)


def test_every_answer_documents_metric_period_assumptions(scripted_data_source):
    # US-06 / AC-03: every analytical answer must be self-explanatory.
    answer = metrics.average_occupancy(scripted_data_source, PERIOD)
    assert answer.metric
    assert answer.period_label
    assert answer.assumptions
    assert answer.exclusions


def test_regression_compare_periods_exclusions_are_deduplicated_with_stable_order(scripted_data_source):
    # Finding #8 (code review): exclusions used to be deduplicated with
    # `set()`, which does not guarantee order — a determinism risk in a
    # module whose whole premise is reproducible output (AC-02). Run twice
    # and require byte-identical results, and require no duplicate entries.
    period_a = Period(label="A", start=date(2026, 1, 5), end=date(2026, 1, 5))
    period_b = Period(label="B", start=date(2026, 1, 6), end=date(2026, 1, 6))

    first = metrics.compare_periods(scripted_data_source, period_a, period_b).exclusions
    second = metrics.compare_periods(scripted_data_source, period_a, period_b).exclusions

    assert first == second
    assert len(first) == len(set(first)), "exclusions must not contain duplicates"

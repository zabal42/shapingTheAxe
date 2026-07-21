"""End-to-end tests against the actual committed, reproducible dataset
(data/*.json), not a hand-built fixture. These exercise the full path
question -> nlp.route -> metrics -> formatter and validate the answers
against the CrossFit business scenario the dataset was generated to encode
(see scripts/generate_dataset.py). This is the automated counterpart to the
five MVP business questions (AC-01, AC-09).
"""

from __future__ import annotations

from datetime import date

from copilot import metrics, nlp
from copilot.cli import _dataset_anchor_day, answer_question
from copilot.datasource import MockDataSource
from copilot.formatter import format_answer


def test_dataset_loads_and_has_the_expected_shape():
    ds = MockDataSource()
    assert len(ds.list_active_clients()) > 0
    sessions = ds.list_sessions(date.min, date.max)
    assert len(sessions) > 100
    assert {s.class_name for s in sessions} == {
        "WOD", "Movilidad", "Halterofilia", "Gimnasia", "CrossFit Kids", "Open Box",
    }


def test_movilidad_is_the_lowest_occupancy_class_this_month():
    ds = MockDataSource()
    now = _dataset_anchor_day(ds)
    routed = nlp.route("¿Qué tres clases tuvieron menor ocupación este mes?", now)
    answer = metrics.lowest_occupancy_classes(ds, routed.periods[0], top_n=3)

    assert answer.result[0]["clase"] == "Movilidad"


def test_early_morning_slot_has_the_highest_cancellation_rate_this_month():
    ds = MockDataSource()
    now = _dataset_anchor_day(ds)
    routed = nlp.route("¿Qué horario tuvo más cancelaciones este mes?", now)
    answer = metrics.cancellation_rate_by_timeslot(ds, routed.periods[0])

    assert answer.result[0]["franja"] == "07:00"


def test_inactive_users_query_returns_active_clients_only():
    ds = MockDataSource()
    now = _dataset_anchor_day(ds)
    answer = metrics.inactive_users(ds, as_of=now, inactivity_days=21)

    active_ids = {c.id for c in ds.list_active_clients()}
    assert answer.result, "the dataset is designed to contain inactive active-clients"
    for row in answer.result:
        assert row["cliente_id"] in active_ids
        assert row["dias_sin_reservar"] is None or row["dias_sin_reservar"] > 21


def test_all_five_mvp_questions_produce_a_non_crashing_explained_answer():
    ds = MockDataSource()
    now = _dataset_anchor_day(ds)
    questions = [
        "¿Cuál fue la ocupación media de este mes?",
        "¿Qué tres clases tuvieron menor ocupación este mes?",
        "¿Qué horario tuvo más cancelaciones este mes?",
        "¿Qué usuarios llevan más de 21 días sin asistir?",
        "Compara la ocupación de este mes con la del mes anterior.",
    ]
    for question in questions:
        rendered = answer_question(ds, question, now)
        assert "Métrica:" in rendered
        assert "Supuestos:" in rendered or "usuarios" in question.lower()


def test_out_of_scope_question_gives_a_prudent_answer_not_a_crash():
    ds = MockDataSource()
    now = _dataset_anchor_day(ds)
    rendered = answer_question(ds, "¿Qué entrenador consigue mayor fidelidad de clientes?", now)
    assert "no dispongo" in rendered.lower()

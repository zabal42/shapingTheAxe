from __future__ import annotations

from datetime import date

from copilot import nlp

NOW = date(2026, 7, 20)


def test_average_occupancy_question_routes_correctly():
    routed = nlp.route("¿Cuál fue la ocupación media de este mes?", NOW)
    assert routed.intent == "average_occupancy"
    assert routed.periods[0].start == date(2026, 7, 1)
    assert routed.periods[0].end == NOW
    assert routed.period_was_defaulted is False


def test_lowest_occupancy_question_extracts_top_n_three():
    routed = nlp.route("¿Qué tres clases tuvieron menor ocupación este mes?", NOW)
    assert routed.intent == "lowest_occupancy"
    assert routed.top_n == 3


def test_cancellation_rate_question_routes_correctly():
    routed = nlp.route("¿Qué horario tuvo más cancelaciones este mes?", NOW)
    assert routed.intent == "cancellation_rate"


def test_inactive_users_question_extracts_threshold_days():
    routed = nlp.route("¿Qué usuarios llevan más de 21 días sin asistir?", NOW)
    assert routed.intent == "inactive_users"
    assert routed.inactivity_days == 21


def test_inactive_users_question_defaults_threshold_when_not_specified():
    routed = nlp.route("¿Qué usuarios están inactivos?", NOW)
    assert routed.intent == "inactive_users"
    assert routed.inactivity_days == 21


def test_compare_periods_question_orders_periods_as_mentioned():
    routed = nlp.route("Compara la ocupación de este mes con la del mes anterior.", NOW)
    assert routed.intent == "compare_periods"
    assert len(routed.periods) == 2
    assert routed.periods[0].label == "este mes"
    assert routed.periods[1].label == "el mes anterior"


def test_compare_periods_question_with_only_one_period_gets_a_default_and_a_note():
    routed = nlp.route("Compara la ocupación con la de otro periodo.", NOW)
    assert routed.intent == "compare_periods"
    assert len(routed.periods) == 2
    assert routed.clarification_message is not None


def test_unsupported_question_returns_no_intent_and_a_prudent_message():
    routed = nlp.route("¿Qué entrenador consigue mayor fidelidad de clientes?", NOW)
    assert routed.intent is None
    assert routed.unsupported_message is not None
    assert "no dispongo" in routed.unsupported_message.lower()


def test_us08_paraphrase_worse_classes_maps_to_lowest_occupancy():
    routed = nlp.route("¿Qué clases funcionan peor?", NOW)
    assert routed.intent == "lowest_occupancy"


def test_us08_paraphrase_less_used_slots_asks_for_clarification():
    # Regression (code review finding #2): this paraphrase was silently
    # routed to lowest_occupancy_classes (grouped by class), answering a
    # different dimension than the "horarios" (time slots) asked about.
    # No supported metric groups occupancy by time slot, so per US-08 ("si
    # es ambigua, debe solicitar una aclaración") this must now ask for
    # clarification instead of guessing.
    routed = nlp.route("¿Cuáles son los horarios menos aprovechados?", NOW)
    assert routed.intent is None
    assert routed.unsupported_message is not None
    assert "franja" in routed.unsupported_message.lower() or "horario" in routed.unsupported_message.lower()


def test_question_without_period_defaults_to_this_month_and_flags_it():
    routed = nlp.route("¿Qué clases funcionan peor?", NOW)
    assert routed.period_was_defaulted is True
    assert routed.periods[0].label == "este mes"


def test_last_n_days_period_is_parsed():
    routed = nlp.route("¿Cuál es la ocupación de los últimos 30 días?", NOW)
    assert routed.periods[0].days == 30
    assert routed.periods[0].end == NOW


# --- Regression tests for code-review findings (docs/07_Acceptance_Evaluation.md) ---


def test_regression_compare_periods_with_a_different_metric_is_unsupported():
    # Finding #1: compare_periods only ever computes an occupancy
    # comparison (metrics.compare_periods calls average_occupancy twice).
    # A question comparing a DIFFERENT metric across periods must not be
    # silently answered as an occupancy comparison.
    routed = nlp.route("Compara las cancelaciones de este mes frente al mes anterior.", NOW)
    assert routed.intent is None
    assert routed.unsupported_message is not None
    assert "ocupación" in routed.unsupported_message.lower()


def test_regression_compare_periods_with_lowest_occupancy_metric_is_also_unsupported():
    routed = nlp.route("Compara las clases con menor ocupación de este mes frente al mes anterior.", NOW)
    assert routed.intent is None


def test_regression_compare_periods_occupancy_still_works():
    # Sanity check: the fix for the two tests above must not break the one
    # comparison that IS in scope (US-05 / AC-01 item 5).
    routed = nlp.route("Compara la ocupación de este mes con la del mes anterior.", NOW)
    assert routed.intent == "compare_periods"
    assert len(routed.periods) == 2


def test_regression_second_period_without_compare_keyword_is_disclosed():
    # Finding #3: mentioning two periods without a compare-keyword used to
    # silently drop the second one with no note at all.
    routed = nlp.route("¿Cuál es la ocupación este mes y el mes anterior?", NOW)
    assert routed.intent == "average_occupancy"
    assert len(routed.periods) == 1
    assert routed.periods[0].label == "este mes"
    assert routed.clarification_message is not None
    assert "un solo" in routed.clarification_message.lower() or "solo uno" in routed.clarification_message.lower()


def test_regression_digit_wins_over_word_tres_inside_unrelated_word():
    # Finding #5: "tres" was matched as a bare substring, so it fired
    # inside "veintitres" (accent-stripped "veintitrés") and silently
    # overrode an explicit different number in the same sentence.
    routed = nlp.route(
        "Dame las clases con menor ocupación, veintitrés alumnos apuntados, quiero 5 clases.", NOW
    )
    assert routed.intent == "lowest_occupancy"
    assert routed.top_n == 5


def test_regression_word_tres_alone_still_means_three():
    routed = nlp.route("¿Qué tres clases tuvieron menor ocupación?", NOW)
    assert routed.top_n == 3


def test_regression_explicit_zero_top_n_is_parsed_not_swallowed():
    # Finding #7 (nlp half): the parser itself must faithfully report an
    # explicit 0 rather than silently defaulting — cli.py's consumption of
    # this value is covered separately in test_dataset_integration.py.
    routed = nlp.route("Dame las 0 clases con menor ocupación.", NOW)
    assert routed.top_n == 0


def test_regression_explicit_zero_inactivity_days_is_parsed_not_swallowed():
    routed = nlp.route("¿Qué usuarios llevan más de 0 días sin asistir?", NOW)
    assert routed.inactivity_days == 0

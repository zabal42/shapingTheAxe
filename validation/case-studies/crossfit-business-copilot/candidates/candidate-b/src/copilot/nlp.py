"""Deterministic natural-language routing (US-08).

This is intentionally a keyword/pattern matcher, not a call to a generative
language model. Two reasons, both explicit design decisions recorded in
docs/05_Architecture.md (decision D2):

1. AC-02 requires that business figures are never invented by a language
   model; routing intent deterministically removes that risk entirely for
   the MVP instead of relying on prompting a model not to hallucinate.
2. No network access, credentials or spend were authorised for this
   experiment, so a bounded, zero-dependency parser is the minimum
   sufficient capability for the five supported questions.

Coverage is bounded to the question types in docs/02_User_Stories.md
(including the paraphrases listed under US-08) plus the out-of-scope example
under US-07. It is not a general-purpose NLU.

Two behaviours were tightened after a code review found silently-wrong
routings (see docs/07_Acceptance_Evaluation.md, "Code review findings"):

- `compare_periods` only ever computes an occupancy comparison (that is the
  only comparison in scope — US-05/AC-01 item 5). If the question also
  names a different metric ("compara las cancelaciones..."), that is an
  unsupported combination, not something to silently answer as an
  occupancy comparison — see `_COMPARISON_METRIC_CONFLICT_INTENTS` below.
- "horarios menos aprovechados" does not cleanly map to any of the five
  supported queries (there is no "occupancy by time slot" metric); routing
  it to the class-grouped `lowest_occupancy` query answered a different
  dimension than asked. Per US-08 ("cuando una pregunta sea ambigua, debe
  solicitar una aclaración"), it now asks for clarification instead of
  guessing.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date

from copilot.periods import Period, current_month, last_n_days, previous_month, today

SUPPORTED_QUESTIONS_HELP = (
    "Puedo responder preguntas sobre: ocupación media de un periodo, "
    "clases con menor ocupación, franjas horarias con más cancelaciones, "
    "usuarios activos sin reservas recientes, y comparación de ocupación "
    "entre dos periodos."
)


def _normalize(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text


_KEYWORDS: dict[str, list[str]] = {
    "compare_periods": ["compara", "comparacion", "comparar", " vs ", "frente a", "respecto a"],
    "inactive_users": [
        "sin asistir", "sin venir", "sin reservar", "inactivo", "inactividad",
        "llevan mas de", "dias sin",
    ],
    "cancellation_rate": ["cancelacion", "cancelaciones", "cancelan", "cancelado"],
    "lowest_occupancy": [
        "menor ocupacion", "peor ocupacion", "menos ocupacion", "funcionan peor",
        "clases con menos", "clases con menor",
    ],
    "average_occupancy": [
        "ocupacion media", "ocupacion promedio", "cual es la ocupacion",
        "cual fue la ocupacion", "ocupacion de",
    ],
}

# Intents evaluated in this order; earlier, more specific intents win ties
# against later, more generic ones (e.g. "lowest_occupancy" beats the
# generic "average_occupancy" keyword "ocupacion").
_INTENT_PRIORITY = [
    "compare_periods",
    "inactive_users",
    "cancellation_rate",
    "lowest_occupancy",
    "average_occupancy",
]

# compare_periods only ever computes an occupancy comparison. If one of
# these other intents also matched, the question asked to compare something
# else (e.g. cancellations) across periods, which is not a supported
# combination — that must be disclosed, not silently answered as occupancy.
_COMPARISON_METRIC_CONFLICT_INTENTS = ("cancellation_rate", "lowest_occupancy")

# Phrases like "horarios menos aprovechados" / "franjas menos aprovechadas"
# ask about time slots using low-occupancy language, but no supported metric
# groups occupancy by time slot (only by class, via lowest_occupancy). This
# is a genuine ambiguity, not a paraphrase of an existing supported query —
# handled before generic keyword scoring so it never falls through to
# lowest_occupancy and silently answers about classes instead of time slots.
_AMBIGUOUS_SLOT_PATTERN = re.compile(
    r"(horario|franja)s?.{0,30}(menos|peor)\s+(aprovechad|utilizad|usad)"
)


@dataclass
class RoutedQuestion:
    intent: str | None
    periods: list[Period] = field(default_factory=list)
    period_was_defaulted: bool = False
    top_n: int | None = None
    inactivity_days: int | None = None
    clarification_message: str | None = None
    unsupported_message: str | None = None


def _extract_periods(normalized: str, now: date) -> tuple[list[Period], bool]:
    # (position in text, Period) so multi-period questions preserve the
    # order the user actually mentioned them in.
    found: list[tuple[int, Period]] = []

    for phrase in ("mes anterior", "mes pasado"):
        pos = normalized.find(phrase)
        if pos != -1:
            found.append((pos, previous_month(now)))
            break

    pos = normalized.find("este mes")
    if pos != -1:
        found.append((pos, current_month(now)))

    match = re.search(r"ultimos?\s+(\d+)\s+dias", normalized)
    if match:
        found.append((match.start(), last_n_days(now, int(match.group(1)))))

    if not found:
        pos = normalized.find("hoy")
        if pos != -1:
            found.append((pos, today(now)))

    if found:
        found.sort(key=lambda pair: pair[0])
        return [period for _, period in found], False
    return [current_month(now)], True


def _extract_top_n(normalized: str, default: int) -> int:
    # Explicit digits win over the word "tres": a plain `"tres" in normalized`
    # substring check previously matched inside unrelated words (e.g.
    # "veintitres"), silently overriding an explicit different number.
    match = re.search(r"\b(\d+)\s+clases\b", normalized)
    if match:
        return int(match.group(1))
    if re.search(r"\btres\b", normalized) or re.search(r"\btop\s*3\b", normalized):
        return 3
    return default


def _extract_inactivity_days(normalized: str, default: int) -> int:
    match = re.search(r"mas de\s+(\d+)\s+dias", normalized)
    if match:
        return int(match.group(1))
    return default


def _single_period(normalized: str, now: date) -> tuple[Period, bool, str | None]:
    """Resolves the one period a non-comparison question needs.

    If the question actually names more than one period, that extra period
    is not silently dropped: a note is returned explaining only the first
    was used, since these intents (unlike compare_periods) only accept one.
    """
    periods, defaulted = _extract_periods(normalized, now)
    note = None
    if len(periods) > 1:
        note = (
            f"Mencionaste varios periodos; esta pregunta admite solo uno, uso '{periods[0].label}'. "
            "Para comparar periodos usa una pregunta de comparación explícita "
            "(p. ej. 'compara ... con ...')."
        )
    return periods[0], defaulted, note


def route(text: str, now: date) -> RoutedQuestion:
    normalized = _normalize(text)

    if _AMBIGUOUS_SLOT_PATTERN.search(normalized):
        return RoutedQuestion(
            intent=None,
            unsupported_message=(
                "No tengo una métrica de ocupación por franja horaria; puedo mostrarte las clases "
                "con menor ocupación, o las franjas con más cancelaciones. "
                "¿Cuál de las dos te sirve?"
            ),
        )

    scores = {
        intent: sum(1 for kw in keywords if kw in normalized)
        for intent, keywords in _KEYWORDS.items()
    }
    matched = [intent for intent in _INTENT_PRIORITY if scores[intent] > 0]

    if not matched:
        return RoutedQuestion(
            intent=None,
            unsupported_message=(
                "No dispongo de evidencia suficiente para responder esa pregunta con los datos "
                f"soportados por el MVP. {SUPPORTED_QUESTIONS_HELP}"
            ),
        )

    intent = matched[0]

    if intent == "compare_periods":
        conflicting = [i for i in _COMPARISON_METRIC_CONFLICT_INTENTS if scores[i] > 0]
        if conflicting:
            return RoutedQuestion(
                intent=None,
                unsupported_message=(
                    "Solo puedo comparar la ocupación entre dos periodos, no otras métricas, "
                    f"con los datos soportados por el MVP. {SUPPORTED_QUESTIONS_HELP}"
                ),
            )

        periods, defaulted = _extract_periods(normalized, now)
        if len(periods) < 2:
            # Only one period phrase (or none) found for a two-period question.
            fallback = previous_month(now) if periods and periods[0].label != previous_month(now).label else current_month(now)
            periods = [periods[0], fallback] if periods else [current_month(now), previous_month(now)]
            return RoutedQuestion(
                intent=intent,
                periods=periods,
                period_was_defaulted=True,
                clarification_message=(
                    "No especificaste ambos periodos a comparar; asumo "
                    f"'{periods[0].label}' frente a '{periods[1].label}'. "
                    "Indica dos periodos explícitos (p. ej. 'este mes' y 'el mes anterior') para otra comparación."
                ),
            )
        return RoutedQuestion(intent=intent, periods=periods[:2])

    if intent == "inactive_users":
        days = _extract_inactivity_days(normalized, default=21)
        return RoutedQuestion(intent=intent, inactivity_days=days)

    if intent == "lowest_occupancy":
        period, defaulted, note = _single_period(normalized, now)
        top_n = _extract_top_n(normalized, default=3)
        return RoutedQuestion(
            intent=intent, periods=[period], period_was_defaulted=defaulted, top_n=top_n,
            clarification_message=note,
        )

    # cancellation_rate, average_occupancy
    period, defaulted, note = _single_period(normalized, now)
    return RoutedQuestion(
        intent=intent, periods=[period], period_was_defaulted=defaulted,
        clarification_message=note,
    )

import { assertPeriod, monthPeriod, previousMonthPeriod } from '../domain/dates.js';

const INTENT_PATTERNS = {
  occupancy_comparison: [/compar/, /\bvs\b/, /frente a/, /contra/, /comparison/],
  inactive_users: [/sin asistir/, /sin venir/, /inactiv/, /no attendance/, /not attended/],
  cancellation_rate: [/cancel/],
  lowest_occupancy: [/menos ocup/, /peor(?:es)? ocup/, /funcionan peor/, /menos aprovechad/, /lowest occupancy/, /underused/],
  average_occupancy: [/ocupacion media/, /media de ocupacion/, /average occupancy/]
};

export function parseQuestion(question, asOf) {
  if (typeof question !== 'string' || question.trim().length === 0) {
    return clarification('Escribe una pregunta de negocio.');
  }
  const normalized = normalize(question);
  const candidates = Object.entries(INTENT_PATTERNS)
    .filter(([, patterns]) => patterns.some((pattern) => pattern.test(normalized)))
    .map(([intent]) => intent);

  // Comparison wording often also contains “average occupancy”. It is the
  // more specific supported intent, so it owns that overlap.
  const effectiveCandidates = candidates.includes('occupancy_comparison')
    ? candidates.filter((intent) => intent !== 'average_occupancy')
    : candidates;

  if (effectiveCandidates.length > 1) {
    return clarification(
      `La pregunta mezcla varias métricas (${effectiveCandidates.join(', ')}). Indica una sola.`
    );
  }
  if (effectiveCandidates.length === 0) {
    return unsupportedQuestion(normalized);
  }

  const intent = effectiveCandidates[0];
  if (intent === 'inactive_users') {
    const match = normalized.match(/(?:mas de|more than)\s+(\d+)\s+(?:dias?|days?)/);
    if (!match) {
      return clarification('Indica el umbral de inactividad, por ejemplo “más de 21 días”.');
    }
    return ready(intent, { thresholdDays: Number(match[1]), asOf });
  }

  if (intent === 'occupancy_comparison') {
    const periods = parseComparisonPeriods(question, normalized, asOf);
    if (!periods) {
      return clarification(
        'Indica dos periodos: cuatro fechas YYYY-MM-DD o “este mes con el mes anterior”.'
      );
    }
    return ready(intent, periods);
  }

  const period = parseSinglePeriod(question, normalized, asOf);
  if (!period) {
    return clarification(
      'Indica el periodo con dos fechas YYYY-MM-DD, “este mes” o “el mes anterior”.'
    );
  }
  if (intent === 'lowest_occupancy') {
    return ready(intent, { period, limit: extractLimit(normalized) });
  }
  return ready(intent, { period });
}

function parseSinglePeriod(original, normalized, asOf) {
  const dates = original.match(/\d{4}-\d{2}-\d{2}/g) ?? [];
  if (dates.length === 2) return checkedPeriod(dates[0], dates[1]);
  if (dates.length !== 0) return null;
  if (/este mes|this month/.test(normalized)) return monthPeriod(asOf);
  if (/mes (?:anterior|pasado)|ultimo mes|last month|previous month/.test(normalized)) {
    return previousMonthPeriod(asOf);
  }
  return null;
}

function parseComparisonPeriods(original, normalized, asOf) {
  const dates = original.match(/\d{4}-\d{2}-\d{2}/g) ?? [];
  if (dates.length === 4) {
    const firstPeriod = checkedPeriod(dates[0], dates[1]);
    const secondPeriod = checkedPeriod(dates[2], dates[3]);
    if (!firstPeriod || !secondPeriod) return null;
    return {
      firstPeriod,
      secondPeriod
    };
  }
  if (dates.length !== 0) return null;
  const hasCurrent = /este mes|this month/.test(normalized);
  const hasPrevious = /mes (?:anterior|pasado)|ultimo mes|last month|previous month/.test(normalized);
  if (hasCurrent && hasPrevious) {
    return {
      firstPeriod: previousMonthPeriod(asOf),
      secondPeriod: monthPeriod(asOf)
    };
  }
  return null;
}

function checkedPeriod(start, end) {
  const period = { start, end };
  try {
    return assertPeriod(period);
  } catch {
    return null;
  }
}

function extractLimit(normalized) {
  const withoutDates = normalized.replace(/\d{4}-\d{2}-\d{2}/g, ' ');
  const numeric = withoutDates.match(/\b(\d+)\b/);
  if (numeric) return Math.max(1, Number(numeric[1]));
  const words = new Map([
    ['una', 1], ['uno', 1], ['one', 1],
    ['dos', 2], ['two', 2],
    ['tres', 3], ['three', 3],
    ['cuatro', 4], ['four', 4],
    ['cinco', 5], ['five', 5]
  ]);
  for (const [word, value] of words) {
    if (new RegExp(`\\b${word}\\b`).test(normalized)) return value;
  }
  return 3;
}

function unsupportedQuestion(normalized) {
  if (/entrenador|coach|fidelidad|retention/.test(normalized)) {
    return {
      status: 'unsupported',
      message: 'No hay evidencia suficiente para medir fidelidad por entrenador.',
      missingData: [
        'Una definición aprobada de fidelidad.',
        'Atribución histórica fiable de cada asistencia a un entrenador.',
        'Un periodo y una población comparables.'
      ]
    };
  }
  return {
    status: 'unsupported',
    message: 'La pregunta no corresponde a una de las cinco métricas del MVP.',
    missingData: ['Una métrica soportada y sus parámetros obligatorios.']
  };
}

function ready(intent, params) {
  return { status: 'ready', intent, params };
}

function clarification(message) {
  return { status: 'clarification', message };
}

function normalize(value) {
  return value
    .toLocaleLowerCase('es')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[¿?¡!,.;:]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

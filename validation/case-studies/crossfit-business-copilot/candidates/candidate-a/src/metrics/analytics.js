import { assertDateOnly, assertPeriod, daysBetween, isWithinPeriod } from '../domain/dates.js';

const OCCUPANCY_ASSUMPTIONS = [
  'Ocupación = reservas confirmadas y no canceladas / capacidad de la sesión.',
  'La media del periodo otorga el mismo peso a cada sesión válida.'
];

export function averageOccupancy(dataset, period) {
  assertPeriod(period);
  const analysis = occupancySessions(dataset, period);
  const values = analysis.sessions.map(({ occupancyPct }) => occupancyPct);
  const occupancyPct = values.length === 0 ? null : round(mean(values));

  return {
    kind: 'average_occupancy',
    status: values.length === 0 ? 'insufficient_data' : 'ok',
    metric: 'Ocupación media por sesión',
    period,
    value: { occupancyPct },
    dataUsed: {
      sessionsAnalyzed: values.length,
      eligibleBookings: sum(analysis.sessions.map(({ eligibleBookings }) => eligibleBookings)),
      totalCapacity: sum(analysis.sessions.map(({ capacity }) => capacity))
    },
    exclusions: occupancyExclusions(analysis),
    assumptions: OCCUPANCY_ASSUMPTIONS,
    limitations: occupancyLimitations(analysis)
  };
}

export function lowestOccupancyClasses(dataset, period, limit = 3) {
  assertPeriod(period);
  if (!Number.isInteger(limit) || limit < 1) {
    throw new Error('limit must be a positive integer');
  }
  const analysis = occupancySessions(dataset, period);
  const groups = new Map();

  for (const session of analysis.sessions) {
    const key = `${session.classId}\u0000${session.startTime}`;
    const group = groups.get(key) ?? {
      classId: session.classId,
      className: session.className,
      startTime: session.startTime,
      occupancies: [],
      sessionsAnalyzed: 0
    };
    group.occupancies.push(session.occupancyPct);
    group.sessionsAnalyzed += 1;
    groups.set(key, group);
  }

  const rankings = [...groups.values()]
    .map(({ occupancies, ...group }) => ({
      ...group,
      occupancyPct: round(mean(occupancies))
    }))
    .sort((a, b) =>
      a.occupancyPct - b.occupancyPct ||
      a.className.localeCompare(b.className, 'es') ||
      a.startTime.localeCompare(b.startTime)
    )
    .slice(0, limit);

  return {
    kind: 'lowest_occupancy',
    status: rankings.length === 0 ? 'insufficient_data' : 'ok',
    metric: 'Ocupación media por clase y horario, orden ascendente',
    period,
    value: { requestedLimit: limit, rankings },
    dataUsed: {
      sessionsAnalyzed: analysis.sessions.length,
      groupsAnalyzed: groups.size
    },
    exclusions: occupancyExclusions(analysis),
    assumptions: OCCUPANCY_ASSUMPTIONS,
    limitations: [
      ...occupancyLimitations(analysis),
      'La clasificación agrupa por tipo de clase y hora, no por entrenador ni sala.'
    ]
  };
}

export function cancellationRatesByTime(dataset, period) {
  assertPeriod(period);
  const sessionsInPeriod = dataset.sessions.filter(({ date }) => isWithinPeriod(date, period));
  const validSessions = sessionsInPeriod.filter(({ cancelled }) => !cancelled);
  const validIds = new Set(validSessions.map(({ id }) => id));
  const groups = new Map();

  for (const booking of dataset.bookings) {
    if (!validIds.has(booking.sessionId)) continue;
    const session = validSessions.find(({ id }) => id === booking.sessionId);
    const group = groups.get(session.startTime) ?? {
      startTime: session.startTime,
      totalBookings: 0,
      cancellations: 0
    };
    group.totalBookings += 1;
    if (booking.cancelledAt !== null) group.cancellations += 1;
    groups.set(session.startTime, group);
  }

  const rankings = [...groups.values()]
    .map((group) => ({
      ...group,
      cancellationRatePct: round((group.cancellations / group.totalBookings) * 100)
    }))
    .sort((a, b) =>
      b.cancellationRatePct - a.cancellationRatePct ||
      b.cancellations - a.cancellations ||
      a.startTime.localeCompare(b.startTime)
    );

  return {
    kind: 'cancellation_rate',
    status: rankings.length === 0 ? 'insufficient_data' : 'ok',
    metric: 'Tasa de cancelación por hora de inicio',
    period,
    value: { rankings },
    dataUsed: {
      sessionsConsidered: validSessions.length,
      bookingsAnalyzed: sum(rankings.map(({ totalBookings }) => totalBookings))
    },
    exclusions: [
      `${countNoun(sessionsInPeriod.length - validSessions.length, 'sesión cancelada', 'sesiones canceladas')} por el box.`,
      'Reservas fuera del periodo.'
    ],
    assumptions: [
      'Tasa de cancelación = reservas con fecha de cancelación / todos los registros de reserva del horario.',
      'El horario corresponde a la hora de inicio de la sesión.'
    ],
    limitations: [
      'La tasa no distingue quién canceló ni el motivo de cancelación.',
      'Los horarios con cero reservas no aparecen porque no tienen denominador.'
    ]
  };
}

export function inactiveActiveUsers(dataset, thresholdDays = 21, asOf = dataset.metadata.asOf) {
  if (!Number.isInteger(thresholdDays) || thresholdDays < 0) {
    throw new Error('thresholdDays must be a non-negative integer');
  }
  assertDateOnly(asOf, 'asOf');
  const sessions = new Map(dataset.sessions.map((session) => [session.id, session]));
  const activeUsers = dataset.users.filter(({ active, createdOn }) => active && createdOn <= asOf);
  const activeUserIds = new Set(activeUsers.map(({ id }) => id));
  const attendedBookings = dataset.bookings.flatMap((booking) => {
    const session = sessions.get(booking.sessionId);
    const isValidAttendance =
      activeUserIds.has(booking.userId) &&
      booking.state === 'confirmed' &&
      booking.cancelledAt === null &&
      booking.attended === true &&
      session &&
      !session.cancelled &&
      session.date <= asOf;
    return isValidAttendance ? [{ ...booking, sessionDate: session.date }] : [];
  });

  const rows = activeUsers.flatMap((user) => {
    const attendedDates = attendedBookings
      .filter((booking) => booking.userId === user.id)
      .map(({ sessionDate }) => sessionDate)
      .sort();

    const lastAttendance = attendedDates.at(-1) ?? null;
    const referenceDate = lastAttendance ?? user.createdOn;
    const inactiveDays = daysBetween(referenceDate, asOf);
    if (inactiveDays <= thresholdDays) return [];

    return [{
      userId: user.id,
      displayName: user.displayName,
      active: user.active,
      lastAttendance,
      inactiveDays,
      referenceType: lastAttendance ? 'last_attendance' : 'creation_date_proxy'
    }];
  }).sort((a, b) =>
    b.inactiveDays - a.inactiveDays || a.displayName.localeCompare(b.displayName, 'es')
  );

  return {
    kind: 'inactive_users',
    status: 'ok',
    metric: `Usuarios activos sin asistencia durante más de ${thresholdDays} días`,
    period: { asOf, thresholdDays },
    value: { users: rows },
    dataUsed: {
      activeUsersAnalyzed: activeUsers.length,
      attendedBookingsAnalyzed: attendedBookings.length
    },
    exclusions: [
      `${countNoun(dataset.users.length - activeUsers.length, 'usuario inactivo o todavía no dado de alta', 'usuarios inactivos o todavía no dados de alta')} en la fecha de análisis.`,
      'Reservas canceladas, listas de espera y reservas sin asistencia.'
    ],
    assumptions: [
      '“Activo” corresponde al indicador normalizado active=true.',
      'Para un usuario sin asistencias, la fecha de alta actúa como referencia mínima explícita.'
    ],
    limitations: [
      'La fecha de alta no demuestra una asistencia; los casos proxy se identifican en el resultado.',
      'El cálculo usa días naturales y la fecha fija del dataset, no la hora actual del sistema.'
    ]
  };
}

export function compareOccupancy(dataset, firstPeriod, secondPeriod) {
  const first = averageOccupancy(dataset, firstPeriod);
  const second = averageOccupancy(dataset, secondPeriod);
  const firstRawValue = rawAverageOccupancy(dataset, firstPeriod);
  const secondRawValue = rawAverageOccupancy(dataset, secondPeriod);
  const firstValue = first.value.occupancyPct;
  const secondValue = second.value.occupancyPct;
  const hasBoth = firstRawValue !== null && secondRawValue !== null;
  const classTimes = (period) => new Set(
    occupancySessions(dataset, period).sessions.map(({ classId, startTime }) => `${classId}|${startTime}`)
  );
  const firstGroups = classTimes(firstPeriod);
  const secondGroups = classTimes(secondPeriod);
  const sameGroups = setEquals(firstGroups, secondGroups);
  const sameSessionCount = first.dataUsed.sessionsAnalyzed === second.dataUsed.sessionsAnalyzed;
  const warnings = [];
  if (!sameSessionCount) warnings.push('Los periodos no contienen el mismo número de sesiones válidas.');
  if (!sameGroups) warnings.push('Los periodos no contienen los mismos grupos de clase y horario.');

  return {
    kind: 'occupancy_comparison',
    status: hasBoth ? 'ok' : 'insufficient_data',
    metric: 'Comparación de ocupación media por sesión',
    period: { first: firstPeriod, second: secondPeriod },
    value: {
      firstOccupancyPct: firstValue,
      secondOccupancyPct: secondValue,
      percentagePointDifference: hasBoth ? round(secondRawValue - firstRawValue) : null,
      relativeChangePct: hasBoth && firstRawValue !== 0
        ? round(((secondRawValue - firstRawValue) / firstRawValue) * 100)
        : null,
      comparable: hasBoth && sameSessionCount && sameGroups,
      warnings
    },
    dataUsed: {
      firstSessionsAnalyzed: first.dataUsed.sessionsAnalyzed,
      secondSessionsAnalyzed: second.dataUsed.sessionsAnalyzed
    },
    exclusions: [
      `Primer periodo: ${first.exclusions.join(' ')}`,
      `Segundo periodo: ${second.exclusions.join(' ')}`
    ],
    assumptions: OCCUPANCY_ASSUMPTIONS,
    limitations: [
      'Una comparación comparable en estructura no controla festivos, cambios de entrenador u otros factores externos.',
      ...warnings
    ]
  };
}

function occupancySessions(dataset, period) {
  const candidates = dataset.sessions.filter(({ date }) => isWithinPeriod(date, period));
  const cancelledSessions = candidates.filter(({ cancelled }) => cancelled).length;
  const invalidCapacitySessions = candidates.filter(({ cancelled, capacity }) => !cancelled && capacity <= 0).length;
  const sessions = candidates
    .filter(({ cancelled, capacity }) => !cancelled && capacity > 0)
    .map((session) => {
      const eligibleBookings = dataset.bookings.filter((booking) =>
        booking.sessionId === session.id &&
        booking.state === 'confirmed' &&
        booking.cancelledAt === null
      ).length;
      return {
        ...session,
        eligibleBookings,
        occupancyPct: (eligibleBookings / session.capacity) * 100
      };
    });
  return { sessions, cancelledSessions, invalidCapacitySessions };
}

function rawAverageOccupancy(dataset, period) {
  const values = occupancySessions(dataset, period).sessions.map(({ occupancyPct }) => occupancyPct);
  return values.length === 0 ? null : mean(values);
}

function occupancyExclusions({ cancelledSessions, invalidCapacitySessions }) {
  return [
    `${countNoun(cancelledSessions, 'sesión cancelada', 'sesiones canceladas')} por el box.`,
    `${countNoun(invalidCapacitySessions, 'sesión sin capacidad positiva', 'sesiones sin capacidad positiva')}.`,
    'Reservas canceladas, en lista de espera o fuera del periodo.'
  ];
}

function occupancyLimitations({ sessions }) {
  const overCapacity = sessions.filter(({ eligibleBookings, capacity }) => eligibleBookings > capacity).length;
  return [
    'La ocupación mide reservas, no asistencia efectiva.',
    overCapacity > 0
      ? `${overCapacity} sesiones superan la capacidad registrada; no se ha truncado el porcentaje.`
      : 'No se detectaron sesiones por encima de su capacidad registrada.'
  ];
}

function mean(values) {
  return sum(values) / values.length;
}

function sum(values) {
  return values.reduce((total, value) => total + value, 0);
}

function round(value) {
  return Math.round((value + Number.EPSILON) * 100) / 100;
}

function setEquals(first, second) {
  return first.size === second.size && [...first].every((value) => second.has(value));
}

function countNoun(value, singular, plural) {
  return `${value} ${value === 1 ? singular : plural}`;
}

#!/usr/bin/env node
// Evaluator-generated adversarial harness for candidate-x (Node.js).
//
// Usage:
//   node adversarial_x.mjs /path/to/extracted/candidate-x
//
// It imports candidate-x's REAL metric engine (src/metrics/analytics.js) and
// exercises it with evaluator-built in-memory datasets that are independent of
// the candidate's own tests. It does not touch the candidate's committed
// dataset. Each check prints OBSERVED behaviour; interpretation lives in the
// evaluation report.
//
// Reproducible by another evaluator: extract candidate-x.tar.gz anywhere and
// pass the resulting candidate-x directory as argv[1].

import { pathToFileURL } from 'node:url';
import { join } from 'node:path';

const root = process.argv[2];
if (!root) {
  console.error('ERROR: pass the extracted candidate-x directory as argv[1]');
  process.exit(2);
}
const analytics = await import(pathToFileURL(join(root, 'src/metrics/analytics.js')).href);

const {
  averageOccupancy,
  lowestOccupancyClasses,
  cancellationRatesByTime,
  inactiveActiveUsers,
  compareOccupancy
} = analytics;

const ASOF = '2026-06-30';
const JUNE = { start: '2026-06-01', end: '2026-06-30' };
const MAY = { start: '2026-05-01', end: '2026-05-31' };

function ds({ users = [], sessions = [], bookings = [], asOf = ASOF }) {
  return {
    metadata: { schemaVersion: 1, boxId: 'b', boxName: 'B', timezone: 'Europe/Madrid', asOf, source: 'simulated' },
    users, sessions, bookings
  };
}
function session(o) {
  return { id: o.id, classId: o.classId ?? 'wod', className: o.className ?? 'WOD', date: o.date,
    startTime: o.startTime ?? '07:00', durationMinutes: 60, capacity: o.capacity, cancelled: o.cancelled ?? false };
}
function booking(o) {
  return { id: o.id, userId: o.userId, sessionId: o.sessionId, state: o.state ?? 'confirmed',
    attended: o.attended ?? false, bookedAt: o.bookedAt ?? '2026-05-01T10:00:00', cancelledAt: o.cancelledAt ?? null };
}
function user(o) {
  return { id: o.id, displayName: o.displayName ?? o.id, active: o.active ?? true, createdOn: o.createdOn ?? '2025-01-01' };
}

const results = [];
function run(id, desc, fn) {
  try {
    const observed = fn();
    results.push({ id, desc, ok: true, observed });
    console.log(`\n=== ${id}: ${desc} ===`);
    console.log(JSON.stringify(observed, null, 2));
  } catch (e) {
    results.push({ id, desc, ok: false, error: e.message });
    console.log(`\n=== ${id}: ${desc} ===`);
    console.log(`THREW: ${e.message}`);
  }
}

// A1 — Empty dataset
run('A1', 'Empty dataset -> average occupancy', () => {
  const r = averageOccupancy(ds({}), JUNE);
  return { status: r.status, occupancyPct: r.value.occupancyPct, sessionsAnalyzed: r.dataUsed.sessionsAnalyzed };
});

// A2 — Zero-capacity session mixed with a normal session
run('A2', 'Zero-capacity session excluded? (cap0 + cap10 with 5 confirmed)', () => {
  const d = ds({
    sessions: [ session({ id: 's0', date: '2026-06-05', capacity: 0 }),
                session({ id: 's1', date: '2026-06-06', capacity: 10 }) ],
    users: [user({ id: 'u1' })],
    bookings: Array.from({ length: 5 }, (_, i) => booking({ id: `b${i}`, userId: 'u1', sessionId: 's1' }))
  });
  const r = averageOccupancy(d, JUNE);
  return { status: r.status, occupancyPct: r.value.occupancyPct, sessionsAnalyzed: r.dataUsed.sessionsAnalyzed, exclusions: r.exclusions };
});

// A3 — Waiting-list bookings excluded from occupancy numerator
run('A3', 'Waiting-list excluded from occupancy (cap10, 4 confirmed + 3 waiting_list)', () => {
  const d = ds({
    sessions: [ session({ id: 's1', date: '2026-06-06', capacity: 10 }) ],
    users: [user({ id: 'u1' })],
    bookings: [
      ...Array.from({ length: 4 }, (_, i) => booking({ id: `c${i}`, userId: 'u1', sessionId: 's1', state: 'confirmed' })),
      ...Array.from({ length: 3 }, (_, i) => booking({ id: `w${i}`, userId: 'u1', sessionId: 's1', state: 'waiting_list' }))
    ]
  });
  const r = averageOccupancy(d, JUNE);
  return { occupancyPct: r.value.occupancyPct, eligibleBookings: r.dataUsed.eligibleBookings };
});

// A4 — Active user whose ONLY booking is cancelled (never attended), recent session
run('A4', 'Active user with only a cancelled recent booking -> inactive?', () => {
  const d = ds({
    users: [user({ id: 'u1', displayName: 'Ana', active: true, createdOn: '2025-01-01' })],
    sessions: [ session({ id: 's1', date: '2026-06-25', capacity: 10 }) ],
    bookings: [ booking({ id: 'b1', userId: 'u1', sessionId: 's1', state: 'confirmed', attended: false, cancelledAt: '2026-06-24T10:00:00' }) ]
  });
  const r = inactiveActiveUsers(d, 21, ASOF);
  return { flaggedUsers: r.value.users.map(u => ({ id: u.userId, inactiveDays: u.inactiveDays, referenceType: u.referenceType })) };
});

// A5 — Attendance linked to a box-cancelled session
run('A5', 'attended=true on a box-cancelled session -> ignored for inactivity?', () => {
  const d = ds({
    users: [user({ id: 'u1', displayName: 'Ana', active: true, createdOn: '2025-01-01' })],
    sessions: [ session({ id: 's1', date: '2026-06-25', capacity: 10, cancelled: true }) ],
    bookings: [ booking({ id: 'b1', userId: 'u1', sessionId: 's1', state: 'confirmed', attended: true }) ]
  });
  const r = inactiveActiveUsers(d, 21, ASOF);
  // Also check occupancy excludes the cancelled session
  const occ = averageOccupancy(d, JUNE);
  return {
    flaggedUsers: r.value.users.map(u => ({ id: u.userId, inactiveDays: u.inactiveDays, referenceType: u.referenceType })),
    occupancyStatus: occ.status, occupancySessionsAnalyzed: occ.dataUsed.sessionsAnalyzed
  };
});

// A6 — Period with no valid sessions (data exists in another month)
run('A6', 'Period with no sessions (data only in May, ask June)', () => {
  const d = ds({
    sessions: [ session({ id: 's1', date: '2026-05-10', capacity: 10 }) ],
    users: [user({ id: 'u1' })],
    bookings: [ booking({ id: 'b1', userId: 'u1', sessionId: 's1' }) ]
  });
  const r = averageOccupancy(d, JUNE);
  const canc = cancellationRatesByTime(d, JUNE);
  return { avgStatus: r.status, avgPct: r.value.occupancyPct, cancStatus: canc.status };
});

// A7 — Determinism / stable ordering under repeated runs (ties in low-occupancy)
run('A7', 'Deterministic ordering across repeated runs (two equal-occupancy classes)', () => {
  const d = ds({
    users: [user({ id: 'u1' })],
    sessions: [
      session({ id: 'sa', date: '2026-06-05', classId: 'zzz', className: 'Zumba', startTime: '19:00', capacity: 10 }),
      session({ id: 'sb', date: '2026-06-05', classId: 'aaa', className: 'Aero',  startTime: '19:00', capacity: 10 })
    ],
    bookings: [
      ...Array.from({ length: 3 }, (_, i) => booking({ id: `a${i}`, userId: 'u1', sessionId: 'sa' })),
      ...Array.from({ length: 3 }, (_, i) => booking({ id: `b${i}`, userId: 'u1', sessionId: 'sb' }))
    ]
  });
  const r1 = JSON.stringify(lowestOccupancyClasses(d, JUNE, 3).value.rankings);
  const r2 = JSON.stringify(lowestOccupancyClasses(d, JUNE, 3).value.rankings);
  return { identicalAcrossRuns: r1 === r2, order: JSON.parse(r1).map(x => x.className) };
});

// A8 — Occupancy over 100% (confirmed > capacity)
run('A8', 'Over-capacity occupancy (cap5, 7 confirmed) not truncated?', () => {
  const d = ds({
    users: [user({ id: 'u1' })],
    sessions: [ session({ id: 's1', date: '2026-06-06', capacity: 5 }) ],
    bookings: Array.from({ length: 7 }, (_, i) => booking({ id: `b${i}`, userId: 'u1', sessionId: 's1' }))
  });
  const r = averageOccupancy(d, JUNE);
  return { occupancyPct: r.value.occupancyPct, limitations: r.limitations };
});

console.log('\n\n===== SUMMARY (candidate-x) =====');
for (const r of results) console.log(`${r.id}: ${r.ok ? 'ran' : 'THREW ' + r.error}`);

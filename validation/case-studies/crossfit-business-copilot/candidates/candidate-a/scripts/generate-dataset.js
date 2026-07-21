import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const outputPath = resolve(projectRoot, 'data/simulated-box.json');

const users = [
  { id: 'u001', displayName: 'Socio 001', active: true, createdOn: '2025-01-10' },
  { id: 'u002', displayName: 'Socio 002', active: true, createdOn: '2025-02-01' },
  { id: 'u003', displayName: 'Socio 003', active: true, createdOn: '2025-02-15' },
  { id: 'u004', displayName: 'Socio 004', active: false, createdOn: '2025-01-20', deactivatedOn: '2026-06-01' },
  { id: 'u005', displayName: 'Socio 005', active: true, createdOn: '2026-05-01' },
  { id: 'u006', displayName: 'Socio 006', active: true, createdOn: '2025-03-01' },
  { id: 'u007', displayName: 'Socio 007', active: true, createdOn: '2025-03-10' },
  { id: 'u008', displayName: 'Socio 008', active: true, createdOn: '2025-04-01' }
];

// The scenario is deliberately compact and hand-auditable. Each user array
// creates one booking record; figures are never stored as precomputed metrics.
const scenarios = [
  session('s001', 'wod', 'WOD', '2026-05-05', '07:00', 5,
    ['u001', 'u002', 'u003', 'u006'], ['u007']),
  session('s002', 'wod', 'WOD', '2026-05-12', '07:00', 5,
    ['u001', 'u002', 'u003'], ['u006', 'u007']),
  session('s003', 'wod', 'WOD', '2026-05-18', '18:00', 4,
    ['u001', 'u002', 'u006'], ['u007']),
  session('s004', 'wod', 'WOD', '2026-05-24', '18:00', 4,
    ['u001', 'u002', 'u006', 'u007'], []),
  session('s005', 'weightlifting', 'Halterofilia', '2026-05-28', '19:00', 4,
    ['u001', 'u006'], ['u008']),
  session('s006', 'weightlifting', 'Halterofilia', '2026-05-31', '19:00', 4,
    ['u002'], ['u007']),

  session('s007', 'wod', 'WOD', '2026-06-02', '07:00', 5,
    ['u001', 'u003', 'u006', 'u007', 'u008'], []),
  session('s008', 'wod', 'WOD', '2026-06-09', '07:00', 5,
    ['u001', 'u006', 'u007', 'u008'], ['u002'], ['u006']),
  session('s009', 'wod', 'WOD', '2026-06-15', '18:00', 4,
    ['u001', 'u006', 'u007'], ['u002']),
  session('s010', 'wod', 'WOD', '2026-06-20', '18:00', 4,
    ['u001', 'u007'], ['u003'], ['u001']),
  session('s011', 'weightlifting', 'Halterofilia', '2026-06-25', '19:00', 4,
    ['u001', 'u008'], ['u002', 'u006']),
  session('s012', 'weightlifting', 'Halterofilia', '2026-06-28', '19:00', 4,
    ['u001'], ['u003', 'u007']),

  session('s013', 'mobility', 'Movilidad', '2026-06-29', '20:00', 10,
    [], [], [], true),
  session('s014', 'mobility', 'Movilidad', '2026-06-30', '20:00', 0,
    [], [])
];

let bookingSequence = 1;
const sessions = scenarios.map(({ confirmedUsers, cancelledUsers, noShowUsers, ...item }) => item);
const bookings = scenarios.flatMap((item) => {
  const confirmed = item.confirmedUsers.map((userId) => ({
    id: nextBookingId(),
    userId,
    sessionId: item.id,
    state: 'confirmed',
    attended: !item.noShowUsers.includes(userId),
    bookedAt: bookedAtFor(item.date),
    cancelledAt: null
  }));
  const cancelled = item.cancelledUsers.map((userId) => ({
    id: nextBookingId(),
    userId,
    sessionId: item.id,
    state: 'confirmed',
    attended: false,
    bookedAt: bookedAtFor(item.date),
    cancelledAt: `${item.date}T05:30:00`
  }));
  return [...confirmed, ...cancelled];
});

const dataset = {
  metadata: {
    schemaVersion: 1,
    boxId: 'box-demo-001',
    boxName: 'CrossFit Demo Box',
    timezone: 'Europe/Madrid',
    asOf: '2026-06-30',
    generatedBy: 'scripts/generate-dataset.js',
    source: 'simulated'
  },
  users,
  sessions,
  bookings
};

mkdirSync(dirname(outputPath), { recursive: true });
writeFileSync(outputPath, `${JSON.stringify(dataset, null, 2)}\n`, 'utf8');
console.log(`Generated ${outputPath}`);
console.log(`${users.length} users, ${sessions.length} sessions, ${bookings.length} bookings`);

function session(
  id,
  classId,
  className,
  date,
  startTime,
  capacity,
  confirmedUsers,
  cancelledUsers,
  noShowUsers = [],
  cancelled = false
) {
  return {
    id,
    classId,
    className,
    date,
    startTime,
    durationMinutes: 60,
    capacity,
    cancelled,
    confirmedUsers,
    cancelledUsers,
    noShowUsers
  };
}

function nextBookingId() {
  const id = `b${String(bookingSequence).padStart(3, '0')}`;
  bookingSequence += 1;
  return id;
}

function bookedAtFor(sessionDate) {
  const month = sessionDate.slice(5, 7);
  return month === '05' ? '2026-04-20T12:00:00' : '2026-05-20T12:00:00';
}

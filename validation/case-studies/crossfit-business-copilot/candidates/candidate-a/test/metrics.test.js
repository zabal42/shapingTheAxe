import assert from 'node:assert/strict';
import { before, describe, it } from 'node:test';
import { JsonDataSource } from '../src/data/json-data-source.js';
import {
  averageOccupancy,
  cancellationRatesByTime,
  compareOccupancy,
  inactiveActiveUsers,
  lowestOccupancyClasses
} from '../src/metrics/analytics.js';

const may = { start: '2026-05-01', end: '2026-05-31' };
const june = { start: '2026-06-01', end: '2026-06-30' };
let dataset;

before(() => {
  dataset = new JsonDataSource(new URL('../data/simulated-box.json', import.meta.url)).load();
});

describe('deterministic metric engine', () => {
  it('calculates mean session occupancy and explains exclusions', () => {
    const result = averageOccupancy(dataset, june);
    assert.equal(result.value.occupancyPct, 63.33);
    assert.equal(result.dataUsed.sessionsAnalyzed, 6);
    assert.equal(result.dataUsed.eligibleBookings, 17);
    assert.match(result.exclusions.join(' '), /1 sesión cancelada/);
    assert.match(result.exclusions.join(' '), /1 sesión sin capacidad positiva/);
  });

  it('gives each session equal weight instead of aggregating capacity', () => {
    const result = averageOccupancy(dataset, may);
    assert.equal(result.value.occupancyPct, 65);
    assert.notEqual(result.value.occupancyPct, 65.38);
  });

  it('ranks low occupancy by class and time with deterministic ties', () => {
    const result = lowestOccupancyClasses(dataset, june, 3);
    assert.deepEqual(
      result.value.rankings.map(({ className, startTime, occupancyPct }) =>
        [className, startTime, occupancyPct]
      ),
      [
        ['Halterofilia', '19:00', 37.5],
        ['WOD', '18:00', 62.5],
        ['WOD', '07:00', 90]
      ]
    );
  });

  it('ranks cancellation rate using cancelled / all bookings', () => {
    const result = cancellationRatesByTime(dataset, june);
    assert.deepEqual(result.value.rankings[0], {
      startTime: '19:00',
      totalBookings: 7,
      cancellations: 4,
      cancellationRatePct: 57.14
    });
  });

  it('includes only active users beyond the strict 21-day boundary', () => {
    const result = inactiveActiveUsers(dataset, 21);
    assert.deepEqual(result.value.users.map(({ userId }) => userId), ['u005', 'u002', 'u003']);
    assert.equal(result.value.users[0].referenceType, 'creation_date_proxy');
    assert.ok(result.value.users.every(({ inactiveDays }) => inactiveDays > 21));
    assert.ok(!result.value.users.some(({ userId }) => userId === 'u004'));
  });

  it('does not include a user exactly on the threshold', () => {
    const copy = structuredClone(dataset);
    copy.users.push({ id: 'u009', displayName: 'Socio 009', active: true, createdOn: '2026-06-09' });
    const result = inactiveActiveUsers(copy, 21);
    assert.ok(!result.value.users.some(({ userId }) => userId === 'u009'));
  });

  it('ignores apparent attendance on a session cancelled by the box', () => {
    const copy = structuredClone(dataset);
    copy.sessions.push({
      id: 'cancelled-session',
      classId: 'mobility',
      className: 'Movilidad',
      date: '2026-06-29',
      startTime: '10:00',
      durationMinutes: 60,
      capacity: 1,
      cancelled: true
    });
    copy.bookings.push({
      id: 'cancelled-session-booking',
      userId: 'u005',
      sessionId: 'cancelled-session',
      state: 'confirmed',
      attended: true,
      bookedAt: '2026-06-01T10:00:00',
      cancelledAt: null
    });

    const result = inactiveActiveUsers(copy, 21);
    const user = result.value.users.find(({ userId }) => userId === 'u005');
    assert.equal(user.lastAttendance, null);
    assert.equal(user.referenceType, 'creation_date_proxy');
  });

  it('compares periods with percentage-point and relative changes', () => {
    const result = compareOccupancy(dataset, may, june);
    assert.deepEqual(result.value, {
      firstOccupancyPct: 65,
      secondOccupancyPct: 63.33,
      percentagePointDifference: -1.67,
      relativeChangePct: -2.56,
      comparable: true,
      warnings: []
    });
  });

  it('derives relative comparison from unrounded occupancy values', () => {
    const result = compareOccupancy(dataset, may, june);
    assert.equal(result.value.relativeChangePct, -2.56);
  });

  it('returns insufficient data rather than inventing a figure', () => {
    const result = averageOccupancy(dataset, { start: '2025-01-01', end: '2025-01-31' });
    assert.equal(result.status, 'insufficient_data');
    assert.equal(result.value.occupancyPct, null);
  });
});

import { readFileSync } from 'node:fs';
import { assertDateOnly } from '../domain/dates.js';

export class JsonDataSource {
  constructor(pathOrUrl) {
    this.pathOrUrl = pathOrUrl;
  }

  load() {
    const parsed = JSON.parse(readFileSync(this.pathOrUrl, 'utf8'));
    validateDataset(parsed);
    return parsed;
  }
}

export function validateDataset(dataset) {
  if (!dataset || typeof dataset !== 'object') {
    throw new Error('dataset must be an object');
  }
  if (!dataset.metadata || dataset.metadata.source !== 'simulated') {
    throw new Error('dataset.metadata.source must be simulated');
  }
  assertDateOnly(dataset.metadata.asOf, 'metadata.asOf');
  assertArray(dataset.users, 'users');
  assertArray(dataset.sessions, 'sessions');
  assertArray(dataset.bookings, 'bookings');

  ensureUniqueIds(dataset.users, 'users');
  ensureUniqueIds(dataset.sessions, 'sessions');
  ensureUniqueIds(dataset.bookings, 'bookings');

  const userIds = new Set(dataset.users.map(({ id }) => id));
  const sessionIds = new Set(dataset.sessions.map(({ id }) => id));

  for (const user of dataset.users) {
    requireString(user.displayName, `user ${user.id}.displayName`);
    if (typeof user.active !== 'boolean') {
      throw new Error(`user ${user.id}.active must be boolean`);
    }
    assertDateOnly(user.createdOn, `user ${user.id}.createdOn`);
    if (user.deactivatedOn != null) {
      assertDateOnly(user.deactivatedOn, `user ${user.id}.deactivatedOn`);
    }
  }

  for (const session of dataset.sessions) {
    requireString(session.classId, `session ${session.id}.classId`);
    requireString(session.className, `session ${session.id}.className`);
    assertDateOnly(session.date, `session ${session.id}.date`);
    if (!/^\d{2}:\d{2}$/.test(session.startTime)) {
      throw new Error(`session ${session.id}.startTime must use HH:MM`);
    }
    if (!Number.isInteger(session.capacity) || session.capacity < 0) {
      throw new Error(`session ${session.id}.capacity must be a non-negative integer`);
    }
    if (typeof session.cancelled !== 'boolean') {
      throw new Error(`session ${session.id}.cancelled must be boolean`);
    }
  }

  for (const booking of dataset.bookings) {
    if (!userIds.has(booking.userId)) {
      throw new Error(`booking ${booking.id} references unknown user ${booking.userId}`);
    }
    if (!sessionIds.has(booking.sessionId)) {
      throw new Error(`booking ${booking.id} references unknown session ${booking.sessionId}`);
    }
    if (!['confirmed', 'waiting_list'].includes(booking.state)) {
      throw new Error(`booking ${booking.id}.state is unsupported`);
    }
    if (typeof booking.attended !== 'boolean') {
      throw new Error(`booking ${booking.id}.attended must be boolean`);
    }
    if (!Object.hasOwn(booking, 'cancelledAt')) {
      throw new Error(`booking ${booking.id}.cancelledAt must be explicit`);
    }
    if (booking.cancelledAt !== null) {
      assertNormalizedDateTime(booking.cancelledAt, `booking ${booking.id}.cancelledAt`);
    }
    if (booking.cancelledAt !== null && booking.attended) {
      throw new Error(`booking ${booking.id} cannot be attended and cancelled`);
    }
  }

  return dataset;
}

function assertArray(value, fieldName) {
  if (!Array.isArray(value)) {
    throw new Error(`${fieldName} must be an array`);
  }
}

function ensureUniqueIds(items, fieldName) {
  const ids = new Set();
  for (const item of items) {
    requireString(item.id, `${fieldName}.id`);
    if (ids.has(item.id)) {
      throw new Error(`${fieldName} contains duplicate id ${item.id}`);
    }
    ids.add(item.id);
  }
}

function requireString(value, fieldName) {
  if (typeof value !== 'string' || value.length === 0) {
    throw new Error(`${fieldName} must be a non-empty string`);
  }
}

function assertNormalizedDateTime(value, fieldName) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$/.test(value)) {
    throw new Error(`${fieldName} must be null or use YYYY-MM-DDTHH:MM:SS`);
  }
  const parsed = new Date(`${value}Z`);
  if (Number.isNaN(parsed.valueOf()) || parsed.toISOString().slice(0, 19) !== value) {
    throw new Error(`${fieldName} is not a valid date-time`);
  }
}

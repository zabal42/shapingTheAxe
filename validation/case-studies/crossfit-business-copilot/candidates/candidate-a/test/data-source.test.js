import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { JsonDataSource, validateDataset } from '../src/data/json-data-source.js';

const source = new JsonDataSource(new URL('../data/simulated-box.json', import.meta.url));

describe('normalized dataset boundary', () => {
  it('loads a simulated, relationally valid dataset', () => {
    const data = source.load();
    assert.equal(data.metadata.source, 'simulated');
    assert.equal(data.users.length, 8);
    assert.equal(data.sessions.length, 14);
    assert.equal(data.bookings.length, 47);
  });

  it('rejects a booking that references an unknown session', () => {
    const data = source.load();
    data.bookings[0].sessionId = 'missing';
    assert.throws(() => validateDataset(data), /unknown session/);
  });

  it('rejects non-simulated input at the MVP boundary', () => {
    const data = source.load();
    data.metadata.source = 'real';
    assert.throws(() => validateDataset(data), /must be simulated/);
  });

  it('rejects a booking without an explicit cancelledAt marker', () => {
    const data = source.load();
    const noShow = data.bookings.find((booking) =>
      booking.attended === false && booking.cancelledAt === null
    );
    delete noShow.cancelledAt;
    assert.throws(() => validateDataset(data), /cancelledAt/);
  });
});

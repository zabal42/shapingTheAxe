import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { parseQuestion } from '../src/parser/question-parser.js';

const asOf = '2026-06-30';

describe('deterministic natural-language parser', () => {
  it('recognizes the five supported Spanish intents', () => {
    const questions = [
      ['¿Cuál fue la ocupación media de este mes?', 'average_occupancy'],
      ['¿Qué tres clases tuvieron menos ocupación este mes?', 'lowest_occupancy'],
      ['¿Qué horario tuvo más cancelaciones este mes?', 'cancellation_rate'],
      ['¿Qué usuarios llevan más de 21 días sin asistir?', 'inactive_users'],
      ['Compara la ocupación de este mes con el mes anterior.', 'occupancy_comparison']
    ];
    for (const [question, intent] of questions) {
      const parsed = parseQuestion(question, asOf);
      assert.equal(parsed.status, 'ready');
      assert.equal(parsed.intent, intent);
    }
  });

  it('supports equivalent low-occupancy wording', () => {
    const parsed = parseQuestion('¿Qué clases funcionan peor este mes?', asOf);
    assert.equal(parsed.intent, 'lowest_occupancy');
    assert.equal(parsed.params.limit, 3);
  });

  it('does not mistake ISO years for the requested ranking limit', () => {
    const parsed = parseQuestion(
      'Muestra 2 clases con menos ocupación entre 2026-05-01 y 2026-05-31',
      asOf
    );
    assert.equal(parsed.params.limit, 2);
    assert.deepEqual(parsed.params.period, { start: '2026-05-01', end: '2026-05-31' });
  });

  it('asks for a missing period rather than assuming one', () => {
    const parsed = parseQuestion('¿Cuál fue la ocupación media?', asOf);
    assert.equal(parsed.status, 'clarification');
    assert.match(parsed.message, /periodo/);
  });

  it('recognizes “último mes” from the project brief as the previous calendar month', () => {
    const parsed = parseQuestion('¿Cuál es la ocupación media del último mes?', asOf);
    assert.equal(parsed.status, 'ready');
    assert.equal(parsed.intent, 'average_occupancy');
    assert.deepEqual(parsed.params.period, { start: '2026-05-01', end: '2026-05-31' });
  });

  it('asks for a missing inactivity threshold', () => {
    const parsed = parseQuestion('Muéstrame los usuarios inactivos', asOf);
    assert.equal(parsed.status, 'clarification');
    assert.match(parsed.message, /umbral/);
  });

  it('accepts the documented English inactivity equivalent', () => {
    const parsed = parseQuestion('Which active users have no attendance for more than 21 days?', asOf);
    assert.equal(parsed.status, 'ready');
    assert.equal(parsed.params.thresholdDays, 21);
  });

  it('rejects malformed comparison periods safely', () => {
    const parsed = parseQuestion(
      'Compara ocupación 2026-06-30 a 2026-06-01 con 2026-05-01 a 2026-05-31',
      asOf
    );
    assert.equal(parsed.status, 'clarification');
  });

  it('refuses unsupported coach-retention analysis with missing evidence', () => {
    const parsed = parseQuestion('¿Qué entrenador consigue mayor fidelidad?', asOf);
    assert.equal(parsed.status, 'unsupported');
    assert.match(parsed.message, /evidencia suficiente/);
    assert.ok(parsed.missingData.length >= 2);
  });
});

import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { describe, it } from 'node:test';
import { Copilot } from '../src/application/copilot.js';
import { JsonDataSource } from '../src/data/json-data-source.js';
import { presentAnswer } from '../src/presenter/answer-presenter.js';

const jsonSource = new JsonDataSource(new URL('../data/simulated-box.json', import.meta.url));
const copilot = new Copilot(jsonSource);
const requiredQuestions = [
  '¿Cuál fue la ocupación media de este mes?',
  '¿Qué tres clases tuvieron menos ocupación este mes?',
  '¿Qué horario tuvo más cancelaciones este mes?',
  '¿Qué usuarios llevan más de 21 días sin asistir?',
  'Compara la ocupación de este mes con el mes anterior.'
];

describe('MVP acceptance', () => {
  it('AC-01 answers all five mandatory business questions', () => {
    for (const question of requiredQuestions) {
      assert.equal(copilot.ask(question).status, 'ok');
    }
  });

  it('AC-02 returns identical figures through a replaceable in-memory source', () => {
    const snapshot = jsonSource.load();
    const memoryCopilot = new Copilot({ load: () => structuredClone(snapshot) });
    for (const question of requiredQuestions) {
      assert.deepEqual(memoryCopilot.ask(question), copilot.ask(question));
    }
  });

  it('AC-03 every analytical answer contains the six explanation sections', () => {
    for (const question of requiredQuestions) {
      const output = presentAnswer(copilot.ask(question));
      for (const section of [
        'Métrica:', 'Periodo:', 'Datos utilizados:', 'Exclusiones:', 'Supuestos:', 'Limitaciones:'
      ]) {
        assert.match(output, new RegExp(section));
      }
    }
  });

  it('AC-07/10 runs as a practical one-shot CLI', () => {
    const output = execFileSync(
      process.execPath,
      ['src/cli.js', '¿Qué horario tuvo más cancelaciones este mes?'],
      { cwd: new URL('..', import.meta.url), encoding: 'utf8' }
    );
    assert.match(output, /19:00: 57,14%/);
    assert.match(output, /Métrica: Tasa de cancelación/);
  });

  it('US-07 refuses unsupported questions without business figures', () => {
    const output = presentAnswer(copilot.ask('¿Qué entrenador consigue mayor fidelidad?'));
    assert.match(output, /No puedo responder con fiabilidad/);
    assert.match(output, /No se ha calculado ni inventado ninguna cifra/);
  });
});

#!/usr/bin/env node
import { createInterface } from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';
import { pathToFileURL } from 'node:url';
import { Copilot } from './application/copilot.js';
import { JsonDataSource } from './data/json-data-source.js';
import { presentAnswer } from './presenter/answer-presenter.js';

const defaultDataUrl = new URL('../data/simulated-box.json', import.meta.url);

export function createDefaultCopilot() {
  return new Copilot(new JsonDataSource(defaultDataUrl));
}

export async function runCli(args = process.argv.slice(2)) {
  const copilot = createDefaultCopilot();
  if (args.includes('--examples')) {
    output.write(`${examples().join('\n')}\n`);
    return 0;
  }
  if (args.length > 0) {
    output.write(`${presentAnswer(copilot.ask(args.join(' ')))}\n`);
    return 0;
  }

  const terminal = createInterface({ input, output });
  output.write('CrossFit Business Copilot (escribe “salir” para terminar)\n');
  output.write('Usa --examples para ver preguntas reproducibles.\n\n');
  try {
    while (true) {
      const question = await terminal.question('> ');
      if (/^(salir|exit|quit)$/i.test(question.trim())) break;
      output.write(`${presentAnswer(copilot.ask(question))}\n\n`);
    }
  } finally {
    terminal.close();
  }
  return 0;
}

function examples() {
  return [
    'Preguntas de ejemplo:',
    '- ¿Cuál fue la ocupación media de este mes?',
    '- ¿Qué tres clases tuvieron menos ocupación este mes?',
    '- ¿Qué horario tuvo más cancelaciones este mes?',
    '- ¿Qué usuarios llevan más de 21 días sin asistir?',
    '- Compara la ocupación de este mes con el mes anterior.'
  ];
}

const invokedDirectly = process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href;
if (invokedDirectly) {
  runCli().catch((error) => {
    console.error(`Error: ${error.message}`);
    process.exitCode = 1;
  });
}

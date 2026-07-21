import { assertDataSource } from '../data/data-source.js';
import {
  averageOccupancy,
  cancellationRatesByTime,
  compareOccupancy,
  inactiveActiveUsers,
  lowestOccupancyClasses
} from '../metrics/analytics.js';
import { parseQuestion } from '../parser/question-parser.js';

export class Copilot {
  constructor(dataSource) {
    this.dataSource = assertDataSource(dataSource);
  }

  ask(question) {
    const dataset = this.dataSource.load();
    const parsed = parseQuestion(question, dataset.metadata.asOf);
    if (parsed.status !== 'ready') return parsed;

    const { intent, params } = parsed;
    switch (intent) {
      case 'average_occupancy':
        return averageOccupancy(dataset, params.period);
      case 'lowest_occupancy':
        return lowestOccupancyClasses(dataset, params.period, params.limit);
      case 'cancellation_rate':
        return cancellationRatesByTime(dataset, params.period);
      case 'inactive_users':
        return inactiveActiveUsers(dataset, params.thresholdDays, params.asOf);
      case 'occupancy_comparison':
        return compareOccupancy(dataset, params.firstPeriod, params.secondPeriod);
      default:
        throw new Error(`Unsupported internal intent: ${intent}`);
    }
  }
}

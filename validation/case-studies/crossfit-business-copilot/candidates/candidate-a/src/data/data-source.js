/**
 * Runtime contract for replaceable analytical data access.
 *
 * A data source exposes normalized records. It must not calculate business
 * metrics. The JSON adapter and a future AimHarder adapter implement the same
 * boundary, so the metric engine remains unchanged.
 *
 * @typedef {Object} DataSource
 * @property {() => NormalizedDataset} load
 *
 * @typedef {Object} NormalizedDataset
 * @property {{schemaVersion:number, boxId:string, boxName:string, timezone:string, asOf:string, source:'simulated'}} metadata
 * @property {Array<Object>} users
 * @property {Array<Object>} sessions
 * @property {Array<Object>} bookings
 */

export function assertDataSource(candidate) {
  if (!candidate || typeof candidate.load !== 'function') {
    throw new Error('dataSource must expose load()');
  }
  return candidate;
}

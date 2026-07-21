const DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/;

export function assertDateOnly(value, fieldName = 'date') {
  if (typeof value !== 'string' || !DATE_PATTERN.test(value)) {
    throw new Error(`${fieldName} must use YYYY-MM-DD`);
  }
  const date = new Date(`${value}T00:00:00Z`);
  if (Number.isNaN(date.valueOf()) || date.toISOString().slice(0, 10) !== value) {
    throw new Error(`${fieldName} is not a valid calendar date`);
  }
  return value;
}

export function isWithinPeriod(date, period) {
  return date >= period.start && date <= period.end;
}

export function assertPeriod(period) {
  if (!period || typeof period !== 'object') {
    throw new Error('period is required');
  }
  assertDateOnly(period.start, 'period.start');
  assertDateOnly(period.end, 'period.end');
  if (period.start > period.end) {
    throw new Error('period.start must not be after period.end');
  }
  return period;
}

export function daysBetween(earlier, later) {
  assertDateOnly(earlier, 'earlier');
  assertDateOnly(later, 'later');
  const earlierMs = Date.parse(`${earlier}T00:00:00Z`);
  const laterMs = Date.parse(`${later}T00:00:00Z`);
  return Math.floor((laterMs - earlierMs) / 86_400_000);
}

export function monthPeriod(date) {
  assertDateOnly(date, 'date');
  const [year, month] = date.split('-').map(Number);
  const lastDay = new Date(Date.UTC(year, month, 0)).getUTCDate();
  return {
    start: `${year}-${String(month).padStart(2, '0')}-01`,
    end: `${year}-${String(month).padStart(2, '0')}-${String(lastDay).padStart(2, '0')}`
  };
}

export function previousMonthPeriod(date) {
  assertDateOnly(date, 'date');
  const current = new Date(`${date}T00:00:00Z`);
  current.setUTCDate(1);
  current.setUTCMonth(current.getUTCMonth() - 1);
  return monthPeriod(current.toISOString().slice(0, 10));
}

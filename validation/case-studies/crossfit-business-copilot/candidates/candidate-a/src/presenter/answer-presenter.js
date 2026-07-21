export function presentAnswer(answer) {
  if (answer.status === 'clarification') {
    return `Necesito una aclaración: ${answer.message}`;
  }
  if (answer.status === 'unsupported') {
    return [
      `No puedo responder con fiabilidad: ${answer.message}`,
      'Datos o decisiones que faltan:',
      ...answer.missingData.map((item) => `- ${item}`),
      'No se ha calculado ni inventado ninguna cifra.'
    ].join('\n');
  }

  return [
    'Resultado',
    formatResult(answer),
    '',
    `Métrica: ${answer.metric}`,
    `Periodo: ${formatPeriod(answer.period)}`,
    `Datos utilizados: ${formatDataUsed(answer.dataUsed)}`,
    'Exclusiones:',
    ...answer.exclusions.map((item) => `- ${item}`),
    'Supuestos:',
    ...answer.assumptions.map((item) => `- ${item}`),
    'Limitaciones:',
    ...answer.limitations.map((item) => `- ${item}`)
  ].join('\n');
}

function formatResult(answer) {
  if (answer.status === 'insufficient_data') {
    return 'No hay datos válidos suficientes para calcular esta métrica.';
  }
  switch (answer.kind) {
    case 'average_occupancy':
      return `${formatPct(answer.value.occupancyPct)} de ocupación media.`;
    case 'lowest_occupancy':
      return answer.value.rankings.map((item, index) =>
        `${index + 1}. ${item.className} a las ${item.startTime}: ` +
        `${formatPct(item.occupancyPct)} (${item.sessionsAnalyzed} sesiones).`
      ).join('\n');
    case 'cancellation_rate':
      return answer.value.rankings.map((item, index) =>
        `${index + 1}. ${item.startTime}: ${formatPct(item.cancellationRatePct)} ` +
        `(${item.cancellations}/${item.totalBookings} reservas).`
      ).join('\n');
    case 'inactive_users':
      return answer.value.users.length === 0
        ? 'No se encontraron usuarios que superen el umbral.'
        : answer.value.users.map((item) => {
            const reference = item.lastAttendance
              ? `última asistencia ${item.lastAttendance}`
              : 'sin asistencias; fecha de alta usada como proxy';
            return `- ${item.displayName}: ${item.inactiveDays} días (${reference}; estado activo).`;
          }).join('\n');
    case 'occupancy_comparison': {
      const comparable = answer.value.comparable ? 'Sí' : 'No';
      const warning = answer.value.warnings.length
        ? ` Advertencias: ${answer.value.warnings.join(' ')}`
        : '';
      return [
        `Primer periodo: ${formatPct(answer.value.firstOccupancyPct)}.`,
        `Segundo periodo: ${formatPct(answer.value.secondOccupancyPct)}.`,
        `Diferencia: ${signed(answer.value.percentagePointDifference)} puntos porcentuales; ` +
          `${signed(answer.value.relativeChangePct)}% relativo.`,
        `Comparabilidad estructural: ${comparable}.${warning}`
      ].join('\n');
    }
    default:
      throw new Error(`Unsupported answer kind: ${answer.kind}`);
  }
}

function formatPeriod(period) {
  if ('start' in period) return `${period.start} a ${period.end}, ambos inclusive`;
  if ('asOf' in period) return `a fecha ${period.asOf}; umbral > ${period.thresholdDays} días`;
  return `${period.first.start} a ${period.first.end} frente a ${period.second.start} a ${period.second.end}`;
}

function formatDataUsed(dataUsed) {
  return Object.entries(dataUsed)
    .map(([key, value]) => `${dataLabel(key)}=${value}`)
    .join(', ');
}

function dataLabel(value) {
  const labels = {
    sessionsAnalyzed: 'sesiones analizadas',
    eligibleBookings: 'reservas elegibles',
    totalCapacity: 'capacidad total',
    groupsAnalyzed: 'grupos analizados',
    sessionsConsidered: 'sesiones consideradas',
    bookingsAnalyzed: 'reservas analizadas',
    activeUsersAnalyzed: 'usuarios activos analizados',
    attendedBookingsAnalyzed: 'asistencias analizadas',
    firstSessionsAnalyzed: 'sesiones analizadas en el primer periodo',
    secondSessionsAnalyzed: 'sesiones analizadas en el segundo periodo'
  };
  return labels[value] ?? value;
}

function formatPct(value) {
  return value === null ? 'no calculable' : `${formatNumber(value)}%`;
}

function signed(value) {
  if (value === null) return 'no calculable';
  return `${value > 0 ? '+' : ''}${formatNumber(value)}`;
}

function formatNumber(value) {
  return new Intl.NumberFormat('es-ES', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  }).format(value);
}

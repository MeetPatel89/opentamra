export function formatDate(isoString) {
  if (!isoString) return '—';
  return new Date(isoString).toLocaleString();
}

export function statusColor(status) {
  switch (status) {
    case 'completed': return '#2dc653';
    case 'running': return '#4361ee';
    case 'failed': return '#ef476f';
    case 'cancelled': return '#adb5bd';
    default: return '#fca311';
  }
}

import React from 'react';
import { statusColor } from '../../utils/formatters';

function StatusBadge({ status }) {
  const style = {
    display: 'inline-block',
    padding: '3px 10px',
    borderRadius: '12px',
    fontSize: '0.75rem',
    fontWeight: 600,
    color: '#fff',
    background: statusColor(status),
  };

  return <span style={style}>{status}</span>;
}

export default StatusBadge;

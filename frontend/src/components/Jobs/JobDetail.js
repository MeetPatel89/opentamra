import React from 'react';
import StatusBadge from '../common/StatusBadge';
import { formatDate } from '../../utils/formatters';

function JobDetail({ job }) {
  if (!job) return <p>Loading...</p>;

  return (
    <div className="card">
      <h2>Job {job.id}</h2>
      <table>
        <tbody>
          <tr><td><strong>Status</strong></td><td><StatusBadge status={job.status} /></td></tr>
          <tr><td><strong>Created</strong></td><td>{formatDate(job.created_at)}</td></tr>
          <tr><td><strong>Started</strong></td><td>{formatDate(job.started_at)}</td></tr>
          <tr><td><strong>Completed</strong></td><td>{formatDate(job.completed_at)}</td></tr>
          {job.error && <tr><td><strong>Error</strong></td><td style={{ color: '#ef476f' }}>{job.error}</td></tr>}
        </tbody>
      </table>
    </div>
  );
}

export default JobDetail;

import React from 'react';
import { Link } from 'react-router-dom';
import StatusBadge from '../common/StatusBadge';
import { formatDate } from '../../utils/formatters';

function JobList({ jobs, onDelete }) {
  if (!jobs.length) {
    return <p>No jobs found.</p>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Status</th>
          <th>Created</th>
          <th>Updated</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {jobs.map((job) => (
          <tr key={job.id}>
            <td><Link to={`/reports/${job.id}`}>{job.id}</Link></td>
            <td><StatusBadge status={job.status} /></td>
            <td>{formatDate(job.created_at)}</td>
            <td>{formatDate(job.updated_at)}</td>
            <td>
              <button className="danger" onClick={() => onDelete(job.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default JobList;

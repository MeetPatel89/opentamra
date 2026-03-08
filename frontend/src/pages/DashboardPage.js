import React from 'react';
import { Link } from 'react-router-dom';
import { useJobs } from '../hooks/useJobs';
import StatusBadge from '../components/common/StatusBadge';

function DashboardPage() {
  const { jobs, loading } = useJobs();

  const recent = jobs.slice(0, 5);
  const counts = jobs.reduce((acc, j) => {
    acc[j.status] = (acc[j.status] || 0) + 1;
    return acc;
  }, {});

  return (
    <div>
      <h1>Dashboard</h1>

      <div className="card">
        <h2>Job Summary</h2>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div style={{ display: 'flex', gap: 24 }}>
            {Object.entries(counts).map(([status, count]) => (
              <div key={status}>
                <StatusBadge status={status} /> <strong>{count}</strong>
              </div>
            ))}
            {jobs.length === 0 && <p>No jobs yet. <Link to="/jobs/new">Create one</Link></p>}
          </div>
        )}
      </div>

      {recent.length > 0 && (
        <div className="card">
          <h2>Recent Jobs</h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {recent.map((j) => (
              <li key={j.id} style={{ padding: '6px 0' }}>
                <Link to={`/reports/${j.id}`}>{j.id}</Link>{' '}
                <StatusBadge status={j.status} />
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default DashboardPage;

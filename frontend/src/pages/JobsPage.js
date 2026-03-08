import React from 'react';
import { useJobs } from '../hooks/useJobs';
import JobList from '../components/Jobs/JobList';
import { deleteJob } from '../api/client';

function JobsPage() {
  const { jobs, loading, refresh } = useJobs();

  const handleDelete = async (id) => {
    if (!window.confirm(`Delete job ${id}?`)) return;
    try {
      await deleteJob(id);
      refresh();
    } catch (err) {
      alert('Delete failed: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div>
      <h1>Jobs</h1>
      <div className="card">
        {loading ? <p>Loading...</p> : <JobList jobs={jobs} onDelete={handleDelete} />}
      </div>
    </div>
  );
}

export default JobsPage;

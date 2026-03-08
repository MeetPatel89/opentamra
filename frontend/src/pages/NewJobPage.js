import React from 'react';
import { useNavigate } from 'react-router-dom';
import JobForm from '../components/Jobs/JobForm';

function NewJobPage() {
  const navigate = useNavigate();

  const handleCreated = (job) => {
    navigate(`/reports/${job.id}`);
  };

  return (
    <div>
      <h1>New Job</h1>
      <JobForm onCreated={handleCreated} />
    </div>
  );
}

export default NewJobPage;

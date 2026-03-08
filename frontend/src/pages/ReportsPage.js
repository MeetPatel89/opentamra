import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useJobDetail } from '../hooks/useJobs';
import { useReports } from '../hooks/useReports';
import JobDetail from '../components/Jobs/JobDetail';
import ReportList from '../components/Reports/ReportList';
import ReportViewer from '../components/Reports/ReportViewer';

function ReportsPage() {
  const { jobId } = useParams();
  const { job } = useJobDetail(jobId);
  const { reports } = useReports(jobId);
  const [previewLevel, setPreviewLevel] = useState(null);

  return (
    <div>
      <h1>Reports</h1>
      <JobDetail job={job} />

      <div className="card">
        <h2>Output Files</h2>
        <ReportList jobId={jobId} reports={reports} />
        {reports.length > 0 && (
          <div style={{ marginTop: 16 }}>
            <label>Preview step: </label>
            <select onChange={(e) => setPreviewLevel(e.target.value)} value={previewLevel || ''}>
              <option value="">Select...</option>
              {reports.map((r, i) => (
                <option key={i} value={r.step}>{r.step}</option>
              ))}
            </select>
          </div>
        )}
      </div>

      {previewLevel && <ReportViewer jobId={jobId} level={previewLevel} />}
    </div>
  );
}

export default ReportsPage;

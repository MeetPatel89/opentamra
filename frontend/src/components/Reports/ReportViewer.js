import React, { useState, useEffect } from 'react';
import DataTable from '../common/DataTable';
import { previewReport } from '../../api/client';

function ReportViewer({ jobId, level }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!jobId || !level) return;

    const fetch = async () => {
      try {
        const res = await previewReport(jobId, level);
        setData(res.data);
      } catch (err) {
        console.error('Failed to preview report', err);
      } finally {
        setLoading(false);
      }
    };

    fetch();
  }, [jobId, level]);

  if (loading) return <p>Loading preview...</p>;
  if (!data) return <p>No data available.</p>;

  return (
    <div className="card">
      <h2>Preview: {level} ({data.row_count} total rows)</h2>
      <DataTable columns={data.columns} rows={data.rows} />
    </div>
  );
}

export default ReportViewer;

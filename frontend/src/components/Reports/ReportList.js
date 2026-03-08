import React from 'react';
import { downloadReportUrl } from '../../api/client';

function ReportList({ jobId, reports }) {
  if (!reports.length) {
    return <p>No reports available yet.</p>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Step</th>
          <th>Rows</th>
          <th>Format</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {reports.map((r, i) => (
          <tr key={i}>
            <td>{r.step}</td>
            <td>{r.row_count}</td>
            <td>{r.format}</td>
            <td>
              <a href={downloadReportUrl(jobId, r.step)} download>
                Download
              </a>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default ReportList;

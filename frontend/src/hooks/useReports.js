import { useState, useEffect } from 'react';
import { listReports } from '../api/client';

export function useReports(jobId) {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!jobId) return;

    const fetch = async () => {
      try {
        const res = await listReports(jobId);
        setReports(res.data);
      } catch (err) {
        console.error('Failed to fetch reports', err);
      } finally {
        setLoading(false);
      }
    };

    fetch();
  }, [jobId]);

  return { reports, loading };
}

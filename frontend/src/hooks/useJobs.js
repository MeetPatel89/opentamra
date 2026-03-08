import { useState, useEffect, useCallback } from 'react';
import { listJobs, getJob } from '../api/client';
import { POLL_INTERVAL_MS } from '../utils/constants';

export function useJobs(statusFilter) {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      const res = await listJobs(statusFilter);
      setJobs(res.data);
    } catch (err) {
      console.error('Failed to fetch jobs', err);
    } finally {
      setLoading(false);
    }
  }, [statusFilter]);

  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
  }, [refresh]);

  return { jobs, loading, refresh };
}

export function useJobDetail(jobId) {
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!jobId) return;
    let active = true;

    const poll = async () => {
      try {
        const res = await getJob(jobId);
        if (active) setJob(res.data);
      } catch (err) {
        console.error('Failed to fetch job', err);
      } finally {
        if (active) setLoading(false);
      }
    };

    poll();
    const interval = setInterval(poll, POLL_INTERVAL_MS);
    return () => { active = false; clearInterval(interval); };
  }, [jobId]);

  return { job, loading };
}

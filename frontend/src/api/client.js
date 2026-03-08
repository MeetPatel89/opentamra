import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: { 'Content-Type': 'application/json' },
});

export const healthCheck = () => axios.get(`${API_URL}/health`);

export const createJob = (data) => client.post('/jobs', data);
export const listJobs = (status) => client.get('/jobs', { params: status ? { status } : {} });
export const getJob = (id) => client.get(`/jobs/${id}`);
export const deleteJob = (id) => client.delete(`/jobs/${id}`);

export const uploadPolicyList = (file) => {
  const form = new FormData();
  form.append('file', file);
  return client.post('/uploads/policy-list', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const listReports = (jobId) => client.get(`/reports/${jobId}`);
export const previewReport = (jobId, level) => client.get(`/reports/${jobId}/${level}`);
export const downloadReportUrl = (jobId, level) =>
  `${API_URL}/api/v1/reports/${jobId}/${level}/download`;

export default client;

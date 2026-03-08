import React, { useState } from 'react';
import FileUpload from '../common/FileUpload';
import { uploadPolicyList, createJob } from '../../api/client';

function JobForm({ onCreated }) {
  const [policyFilterId, setPolicyFilterId] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [uploadInfo, setUploadInfo] = useState(null);

  const handleUpload = async (file) => {
    setUploading(true);
    try {
      const res = await uploadPolicyList(file);
      setPolicyFilterId(res.data.id);
      setUploadInfo(res.data);
    } catch (err) {
      alert('Upload failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setUploading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await createJob({ policy_filter_id: policyFilterId });
      if (onCreated) onCreated(res.data);
    } catch (err) {
      alert('Job creation failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <h2>Create New Job</h2>

      <div style={{ margin: '16px 0' }}>
        <label>Policy Filter (optional):</label>
        <div style={{ marginTop: 8 }}>
          <FileUpload onUpload={handleUpload} label={uploading ? 'Uploading...' : 'Upload CSV'} />
          {uploadInfo && (
            <p style={{ marginTop: 8, fontSize: '0.85rem', color: '#666' }}>
              Uploaded: {uploadInfo.filename} ({uploadInfo.row_count} policies)
            </p>
          )}
        </div>
      </div>

      <button type="submit" className="primary" disabled={submitting}>
        {submitting ? 'Creating...' : 'Run Pipeline'}
      </button>
    </form>
  );
}

export default JobForm;

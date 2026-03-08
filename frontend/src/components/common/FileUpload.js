import React, { useRef } from 'react';

function FileUpload({ onUpload, label = 'Choose file', accept = '.csv' }) {
  const inputRef = useRef();

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file && onUpload) {
      onUpload(file);
    }
  };

  return (
    <div className="file-upload">
      <button className="primary" onClick={() => inputRef.current.click()}>
        {label}
      </button>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        onChange={handleChange}
        style={{ display: 'none' }}
      />
    </div>
  );
}

export default FileUpload;

import React, { useState } from 'react';
import './HardwareProtection.css';

const HardwareProtection = () => {
  const [activeTab, setActiveTab] = useState('generate');
  const [generateLoading, setGenerateLoading] = useState(false);
  const [analyzeLoading, setAnalyzeLoading] = useState(false);
  const [generateResult, setGenerateResult] = useState(null);
  const [analyzeResult, setAnalyzeResult] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [password, setPassword] = useState('');

  const API_BASE_URL = 'http://localhost:8000';

  const handleGenerateHash = async () => {
    setGenerateLoading(true);
    setGenerateResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/hardware-hash/generate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          password: password || 'default_password'
        })
      });

      const data = await response.json();

      if (data.success) {
        setGenerateResult({
          success: true,
          ...data
        });
      } else {
        setGenerateResult({
          success: false,
          error: data.error
        });
      }
    } catch (error) {
      setGenerateResult({
        success: false,
        error: `Failed to generate hardware hash: ${error.message}`
      });
    } finally {
      setGenerateLoading(false);
    }
  };

  const handleDownload = () => {
    if (generateResult && generateResult.download_url) {
      window.open(`${API_BASE_URL}${generateResult.download_url}`, '_blank');
    }
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setAnalyzeResult(null);
  };

  const handleAnalyzeHash = async () => {
    if (!selectedFile) {
      alert('Please select a hardware hash file first');
      return;
    }

    setAnalyzeLoading(true);
    setAnalyzeResult(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('password', password || 'default_password');

      const response = await fetch(`${API_BASE_URL}/api/hardware-hash/analyze/`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (data.success) {
        setAnalyzeResult({
          success: true,
          ...data
        });
      } else {
        setAnalyzeResult({
          success: false,
          error: data.error
        });
      }
    } catch (error) {
      setAnalyzeResult({
        success: false,
        error: `Failed to analyze hardware hash: ${error.message}`
      });
    } finally {
      setAnalyzeLoading(false);
    }
  };

  const formatBytes = (bytes) => {
    if (!bytes) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return '#ff4444';
      case 'medium': return '#ff9800';
      case 'low': return '#ffc107';
      default: return '#666';
    }
  };

  return (
    <div className="hardware-protection-container">
      <div className="protection-header">
        <h1>🔐 Hardware Protection</h1>
        <p>Create and analyze encrypted hardware hash files to detect unauthorized component changes</p>
      </div>

      <div className="protection-tabs">
        <button
          className={`tab-button ${activeTab === 'generate' ? 'active' : ''}`}
          onClick={() => setActiveTab('generate')}
        >
          Generate Hash File
        </button>
        <button
          className={`tab-button ${activeTab === 'analyze' ? 'active' : ''}`}
          onClick={() => setActiveTab('analyze')}
        >
          Analyze Hash File
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'generate' && (
          <>
            <div className="generate-section">
              <div className="info-card">
                <h2>Create Your Hardware Hash File Now</h2>
                <p>
                  This tool will collect your system's hardware information including CPU, GPU, RAM,
                  storage devices, display adapters, and other components. It will create an encrypted,
                  read-only file that can be used later to verify if any hardware changes have occurred.
                </p>
                <div className="info-list">
                  <div className="info-item">
                    <span>Encrypted with password protection</span>
                  </div>
                  <div className="info-item">
                    <span>Captures all major hardware components</span>
                  </div>
                  <div className="info-item">
                    <span>Read-only file prevents tampering</span>
                  </div>
                  <div className="info-item">
                    <span>Detects service center replacements</span>
                  </div>
                </div>
              </div>

              <div className="action-card">
                <div className="input-group">
                  <label htmlFor="generate-password">Password (Optional)</label>
                  <input
                    id="generate-password"
                    type="password"
                    placeholder="Leave empty for default password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="password-input"
                  />
                  <small>Use a strong password to secure your hardware hash file</small>
                </div>

                <button
                  onClick={handleGenerateHash}
                  disabled={generateLoading}
                  className="primary-button"
                >
                  {generateLoading ? (
                    <>
                      <span className="spinner"></span>
                      Generating Hardware Hash...
                    </>
                  ) : (
                    <>
                      <span>🔐</span>
                      Generate Hardware Hash File
                    </>
                  )}
                </button>
              </div>
            </div>

            {generateResult && (
              <div className={`result-card ${generateResult.success ? 'success' : 'error'}`}>
                {generateResult.success ? (
                  <>
                    <h3>✅ Hardware Hash File Generated Successfully!</h3>
                    <div className="result-details">
                      <div className="detail-row">
                        <span className="label">Filename:</span>
                        <span className="value">{generateResult.filename}</span>
                      </div>
                      <div className="detail-row">
                        <span className="label">File Size:</span>
                        <span className="value">{formatBytes(generateResult.file_size)}</span>
                      </div>
                      <div className="detail-row">
                        <span className="label">Hardware Hash:</span>
                        <span className="value hash-value">{generateResult.hardware_hash}</span>
                      </div>
                      <div className="detail-row">
                        <span className="label">Created:</span>
                        <span className="value">{new Date(generateResult.created).toLocaleString()}</span>
                      </div>
                      <div className="detail-row">
                        <span className="label">Components Captured:</span>
                        <span className="value">
                          {generateResult.components_captured.permanent} permanent, {generateResult.components_captured.changeable} changeable
                        </span>
                      </div>
                    </div>
                    <button onClick={handleDownload} className="download-button">
                      📥 Download Hardware Hash File
                    </button>
                  </>
                ) : (
                  <>
                    <h3>❌ Failed to Generate Hardware Hash</h3>
                    <p className="error-message">{generateResult.error}</p>
                  </>
                )}
              </div>
            )}
          </>
        )}

        {activeTab === 'analyze' && (
          <>
            <div className="analyze-section">
              <div className="info-card">
                <h2>Analyze Hardware Hash File</h2>
                <p>
                  Upload a previously generated hardware hash file to compare it with your current
                  hardware configuration. This will detect any changes in components that may have
                  occurred since the file was created.
                </p>
                <div className="warning-box">
                  <span>Make sure to use the same password that was used to generate the file</span>
                </div>
              </div>

              <div className="action-card">
                <div className="input-group">
                  <label htmlFor="analyze-password">Password</label>
                  <input
                    id="analyze-password"
                    type="password"
                    placeholder="Enter the password used during generation"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="password-input"
                  />
                </div>

                <div className="file-upload-area">
                  <input
                    type="file"
                    id="hash-file-input"
                    accept=".hwh"
                    onChange={handleFileSelect}
                    className="file-input"
                  />
                  <label htmlFor="hash-file-input" className="file-upload-label">
                    {selectedFile ? selectedFile.name : 'Choose Hardware Hash File (.hwh)'}
                  </label>
                </div>

                <button
                  onClick={handleAnalyzeHash}
                  disabled={analyzeLoading || !selectedFile}
                  className="primary-button"
                >
                  {analyzeLoading ? (
                    <>
                      <span className="spinner"></span>
                      Analyzing Hardware...
                    </>
                  ) : (
                    <>
                      Analyze Hardware Changes
                    </>
                  )}
                </button>
              </div>
            </div>

            {analyzeResult && (
              <div className={`result-card ${analyzeResult.success ? 'success' : 'error'}`}>
                {analyzeResult.success ? (
                  <>
                    <div className="analysis-header">
                      <h3>
                        {analyzeResult.comparison.overall_status === 'unchanged' ? (
                          <>No Hardware Changes Detected</>
                        ) : (
                          <>Hardware Changes Detected</>
                        )}
                      </h3>
                    </div>

                    <div className="analysis-summary">
                      <div className="summary-card">
                        <div className="summary-number">{analyzeResult.summary.total_changes}</div>
                        <div className="summary-label">Total Changes</div>
                      </div>
                      <div className="summary-card critical">
                        <div className="summary-number">{analyzeResult.summary.critical_changes}</div>
                        <div className="summary-label">Critical Changes</div>
                      </div>
                      <div className="summary-card">
                        <div className="summary-number">{analyzeResult.summary.component_changes}</div>
                        <div className="summary-label">Component Changes</div>
                      </div>
                    </div>

                    {analyzeResult.file_info && (
                      <div className="file-info-section">
                        <h4>File Information</h4>
                        <div className="detail-row">
                          <span className="label">Original File Created:</span>
                          <span className="value">{new Date(analyzeResult.file_info.created).toLocaleString()}</span>
                        </div>
                        <div className="detail-row">
                          <span className="label">Original Hash:</span>
                          <span className="value hash-value">{analyzeResult.file_info.original_hash}</span>
                        </div>
                        <div className="detail-row">
                          <span className="label">Current Hash:</span>
                          <span className="value hash-value">{analyzeResult.file_info.current_hash}</span>
                        </div>
                      </div>
                    )}

                    {analyzeResult.comparison.changes_detected.length > 0 && (
                      <div className="changes-section critical-section">
                        <h4>🚨 Critical Changes (Permanent Components)</h4>
                        <p className="warning-text">These components should NEVER change!</p>
                        {analyzeResult.comparison.changes_detected.map((change, index) => (
                          <div key={index} className="change-item critical">
                            <div className="change-header">
                              <span className="component-name">{change.field}</span>
                              <span className="severity-badge" style={{backgroundColor: getSeverityColor(change.severity)}}>
                                {change.severity.toUpperCase()}
                              </span>
                            </div>
                            <div className="change-details">
                              <div className="change-value">
                                <strong>Original:</strong> {change.original || 'N/A'}
                              </div>
                              <div className="change-value">
                                <strong>Current:</strong> {change.current || 'N/A'}
                              </div>
                            </div>
                            <div className="change-message">{change.message}</div>
                          </div>
                        ))}
                      </div>
                    )}

                    {analyzeResult.comparison.changeable_components_changes.length > 0 && (
                      <div className="changes-section">
                        <h4>Component Changes</h4>
                        <p>These components may have been replaced in a service center:</p>
                        {analyzeResult.comparison.changeable_components_changes.map((change, index) => (
                          <div key={index} className="change-item">
                            <div className="change-header">
                              <span className="component-name">{change.component} - {change.field}</span>
                              <span className="severity-badge" style={{backgroundColor: getSeverityColor(change.severity)}}>
                                {change.severity.toUpperCase()}
                              </span>
                            </div>
                            <div className="change-details">
                              <div className="change-value">
                                <strong>Original:</strong> {JSON.stringify(change.original) || 'N/A'}
                              </div>
                              <div className="change-value">
                                <strong>Current:</strong> {JSON.stringify(change.current) || 'N/A'}
                              </div>
                            </div>
                            <div className="change-message">{change.message}</div>
                          </div>
                        ))}
                      </div>
                    )}

                    {analyzeResult.comparison.overall_status === 'unchanged' && (
                      <div className="no-changes-message">
                        <span className="icon">✅</span>
                        <p>All hardware components match the original configuration. No unauthorized changes detected.</p>
                      </div>
                    )}
                  </>
                ) : (
                  <>
                    <h3>❌ Failed to Analyze Hardware Hash</h3>
                    <p className="error-message">{analyzeResult.error}</p>
                    <small>Please check the password and ensure the file is a valid hardware hash file.</small>
                  </>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default HardwareProtection;

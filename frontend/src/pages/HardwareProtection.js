import React from 'react';
import DiagnosticChat from '../components/DiagnosticChat';
import './HardwareProtection.css';

const HardwareProtection = () => {
  return (
    <div className="hardware-protection-page">
      <div className="page-header">
        <h1>🛡️ Hardware Protection</h1>
        <p>AI-powered diagnostic assistant to identify and resolve your PC hardware issues</p>
      </div>
      
      <div className="chat-wrapper">
        <DiagnosticChat />
      </div>
      
      <div className="tips-section">
        <h3>💡 Tips for Better Diagnostics</h3>
        <div className="tips-grid">
          <div className="tip-card">
            <span className="tip-icon">📝</span>
            <p>Be specific about the symptoms you're experiencing</p>
          </div>
          <div className="tip-card">
            <span className="tip-icon">🕐</span>
            <p>Mention when the problem started</p>
          </div>
          <div className="tip-card">
            <span className="tip-icon">⚠️</span>
            <p>Include any error messages you've seen</p>
          </div>
          <div className="tip-card">
            <span className="tip-icon">🔄</span>
            <p>Describe any recent changes to your system</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HardwareProtection;

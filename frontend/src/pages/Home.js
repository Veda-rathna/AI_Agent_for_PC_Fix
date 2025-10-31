import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const [activeCard, setActiveCard] = useState(null);
  const [diagnosticsCount, setDiagnosticsCount] = useState(0);
  const [issuesResolved, setIssuesResolved] = useState(0);
  const [uptime, setUptime] = useState(0);

  // Animated counters
  useEffect(() => {
    const diagnosticsTarget = 1247;
    const issuesTarget = 982;
    const uptimeTarget = 99.9;
    
    const duration = 2000; // 2 seconds
    const steps = 60;
    const stepTime = duration / steps;
    
    let currentStep = 0;
    
    const timer = setInterval(() => {
      currentStep++;
      const progress = currentStep / steps;
      
      setDiagnosticsCount(Math.floor(diagnosticsTarget * progress));
      setIssuesResolved(Math.floor(issuesTarget * progress));
      setUptime(parseFloat((uptimeTarget * progress).toFixed(1)));
      
      if (currentStep >= steps) {
        clearInterval(timer);
      }
    }, stepTime);
    
    return () => clearInterval(timer);
  }, []);

  const commonIssues = [
    { id: 1, title: "Screen Flickering", severity: "high", count: 156 },
    { id: 2, title: "Slow Performance", severity: "medium", count: 243 },
    { id: 3, title: "Blue Screen (BSOD)", severity: "critical", count: 89 },
    { id: 4, title: "Overheating Issues", severity: "high", count: 127 },
    { id: 5, title: "Audio Problems", severity: "medium", count: 98 },
    { id: 6, title: "Network Connectivity", severity: "medium", count: 134 }
  ];

  const capabilities = [
    {
      title: "Real-time Hardware Monitoring",
      description: "Continuous tracking of CPU, GPU, RAM, and storage health",
      metrics: ["Temperature", "Usage", "Performance", "Errors"]
    },
    {
      title: "AI-Powered Diagnostics",
      description: "Advanced machine learning models analyze system behavior",
      metrics: ["Pattern Recognition", "Anomaly Detection", "Predictive Analysis", "Root Cause"]
    },
    {
      title: "Interactive Troubleshooting",
      description: "Step-by-step guided solutions with visual feedback",
      metrics: ["Chat Interface", "Visual Guides", "Live Updates", "Success Rate"]
    }
  ];

  return (
    <div className="home-page">
      {/* Hero Section with Live Stats */}
      <div className="hero-section">
        <div className="hero-content">
          <div className="status-badge">
            <span className="status-dot"></span>
            AI System Online
          </div>
          
          <h1 className="hero-title">
            <span className="gradient-text">Intelligent</span> PC Diagnostics
            <br />
            <span className="subtitle-text">Powered by Advanced AI</span>
          </h1>
          
          <p className="hero-subtitle">
            Get instant, accurate diagnosis of your PC issues with our AI assistant. 
            From hardware failures to performance problems, we've got you covered.
          </p>
          
          <div className="hero-buttons">
            <Link to="/diagnosis" className="btn btn-primary btn-glow">
              <span>Start Free Diagnosis</span>
              <span className="btn-icon">→</span>
            </Link>
            <Link to="/hardware-protection" className="btn btn-secondary">
              <span>Hardware Protection</span>
            </Link>
          </div>

          {/* Live Stats */}
          <div className="live-stats">
            <div className="stat-item">
              <div className="stat-number">{diagnosticsCount.toLocaleString()}</div>
              <div className="stat-label">Diagnostics Performed</div>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <div className="stat-number">{issuesResolved.toLocaleString()}</div>
              <div className="stat-label">Issues Resolved</div>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <div className="stat-number">{uptime}%</div>
              <div className="stat-label">Uptime</div>
            </div>
          </div>
        </div>
        
        {/* Interactive Visual */}
        <div className="hero-visual">
          <div className="ai-visualization">
            <div className="pulse-ring"></div>
            <div className="pulse-ring delay-1"></div>
            <div className="pulse-ring delay-2"></div>
            <div className="ai-core">
              <div className="core-text">AI</div>
            </div>
          </div>
          
          <div className="floating-indicators">
            <div className="indicator indicator-1">
              <span className="indicator-label">CPU Health</span>
              <div className="progress-bar">
                <div className="progress-fill" style={{width: '94%'}}></div>
              </div>
            </div>
            <div className="indicator indicator-2">
              <span className="indicator-label">GPU Status</span>
              <div className="progress-bar">
                <div className="progress-fill" style={{width: '88%'}}></div>
              </div>
            </div>
            <div className="indicator indicator-3">
              <span className="indicator-label">Memory OK</span>
              <div className="progress-bar">
                <div className="progress-fill" style={{width: '96%'}}></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Common Issues Section */}
      <div className="common-issues-section">
        <h2 className="section-title">
          <span className="title-accent">Popular</span> Issues We Diagnose
        </h2>
        
        <div className="issues-grid">
          {commonIssues.map((issue) => (
            <div 
              key={issue.id}
              className={`issue-card ${activeCard === issue.id ? 'active' : ''}`}
              onMouseEnter={() => setActiveCard(issue.id)}
              onMouseLeave={() => setActiveCard(null)}
            >
              <div className="issue-header">
                <h3>{issue.title}</h3>
                <span className={`severity-badge ${issue.severity}`}>
                  {issue.severity}
                </span>
              </div>
              <div className="issue-stats">
                <span className="issue-count">{issue.count} cases resolved</span>
                <span className="issue-action">Diagnose →</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Capabilities Section */}
      <div className="capabilities-section">
        <h2 className="section-title">
          <span className="title-accent">Our</span> AI Capabilities
        </h2>
        
        <div className="capabilities-grid">
          {capabilities.map((cap, index) => (
            <div key={index} className="capability-card">
              <div className="capability-number">{String(index + 1).padStart(2, '0')}</div>
              <h3>{cap.title}</h3>
              <p>{cap.description}</p>
              <div className="metrics-list">
                {cap.metrics.map((metric, idx) => (
                  <span key={idx} className="metric-tag">{metric}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Banner */}
      <div className="cta-banner">
        <div className="cta-content">
          <h2>Ready to diagnose your PC?</h2>
          <p>Our AI is standing by to help you identify and solve any hardware issue</p>
          <Link to="/diagnosis" className="btn btn-cta">
            Launch Diagnostic Chat
            <span className="btn-icon">→</span>
          </Link>
        </div>
        <div className="cta-decoration">
          <div className="deco-circle"></div>
          <div className="deco-circle"></div>
          <div className="deco-circle"></div>
        </div>
      </div>
    </div>
  );
};

export default Home;

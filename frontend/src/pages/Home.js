import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-page">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            <span className="gradient-text">AI-Powered</span> PC Diagnostic Solution
          </h1>
          <p className="hero-subtitle">
            Advanced artificial intelligence to diagnose, troubleshoot, and protect your computer hardware
          </p>
          <div className="hero-buttons">
            <Link to="/diagnosis" className="btn btn-primary">
              Start Diagnosis
              <span className="btn-icon">→</span>
            </Link>
            <Link to="/about" className="btn btn-secondary">
              Learn More
            </Link>
          </div>
        </div>
        
        <div className="hero-visual">
          <div className="floating-card">
            <div className="card-icon">🔍</div>
            <h3>Smart Detection</h3>
            <p>AI-powered issue identification</p>
          </div>
          <div className="floating-card">
            <div className="card-icon">⚡</div>
            <h3>Quick Response</h3>
            <p>Instant diagnostic results</p>
          </div>
          <div className="floating-card">
            <div className="card-icon">🛡️</div>
            <h3>Protection</h3>
            <p>Proactive hardware monitoring</p>
          </div>
        </div>
      </div>
      
      <div className="features-section">
        <h2 className="section-title">Why Choose Our AI Diagnostic Tool?</h2>
        
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>Advanced AI Technology</h3>
            <p>Powered by cutting-edge artificial intelligence models that learn and adapt to provide accurate diagnostics</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">💬</div>
            <h3>Interactive Chat Interface</h3>
            <p>Simply describe your issue in natural language and get expert-level assistance instantly</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Precise Solutions</h3>
            <p>Get detailed, actionable solutions tailored to your specific hardware problems</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">⏱️</div>
            <h3>24/7 Availability</h3>
            <p>Access professional-grade diagnostics anytime, anywhere, without waiting for support</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Comprehensive Analysis</h3>
            <p>Deep analysis of hardware issues with detailed explanations and step-by-step guidance</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h3>Secure & Private</h3>
            <p>Your diagnostic data is processed securely with complete privacy protection</p>
          </div>
        </div>
      </div>
      
      <div className="cta-section">
        <div className="cta-content">
          <h2>Ready to Fix Your PC Issues?</h2>
          <p>Get started with our AI diagnostic assistant now</p>
          <Link to="/diagnosis" className="btn btn-large">
            Launch Diagnosis
            <span className="btn-icon">🚀</span>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;

import React from 'react';
import './About.css';

const About = () => {
  return (
    <div className="about-page">
      <div className="about-hero">
        <div className="hero-badge">AI-Powered Diagnostics</div>
        <h1>AutoMend AI PC Diagnostic Assistant</h1>
        <p className="about-subtitle">
          Revolutionizing computer hardware diagnostics with advanced artificial intelligence and real-time telemetry analysis
        </p>
        <div className="hero-stats">
          <div className="stat-item">
            <span className="stat-number">24/7</span>
            <span className="stat-label">Availability</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">4000+</span>
            <span className="stat-label">Tokens Reasoning</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">100%</span>
            <span className="stat-label">Offline Capable</span>
          </div>
        </div>
      </div>
      
      <div className="about-content">
        {/* Mission Statement */}
        <section className="about-section full-width">
          <div className="section-icon">🎯</div>
          <h2>Our Mission</h2>
          <p>
            We're dedicated to making professional-grade computer hardware diagnostics accessible to everyone. 
            Our AI-powered solution eliminates the need for expensive technician visits by providing instant, 
            accurate diagnostics that anyone can understand and act upon. With intelligent hardware detection, 
            real-time system telemetry, and comprehensive service center integration, we're transforming how 
            people troubleshoot and repair their computers.
          </p>
        </section>

        {/* Core Features */}
        <section className="about-section full-width">
          <div className="section-icon">⚡</div>
          <h2>Comprehensive Feature Set</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>Advanced AI Reasoning</h3>
              <p>Powered by Llama 3.1 reasoning model with 4000 token capacity for deep diagnostic analysis and comprehensive troubleshooting</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Real-Time Telemetry</h3>
              <p>Collects CPU, memory, disk, GPU, and issue-specific system metrics to provide data-driven diagnostics</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔍</div>
              <h3>Hardware Detection</h3>
              <p>Automatically identifies hardware vs software issues with intelligent navigation to service centers or protection tools</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🗺️</div>
              <h3>Service Center Locator</h3>
              <p>Interactive map showing nearby authorized repair centers with distance calculation, filtering, and one-click directions</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🛡️</div>
              <h3>Hardware Protection</h3>
              <p>Generate encrypted hardware fingerprints to verify component authenticity and detect unauthorized modifications</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💬</div>
              <h3>Natural Language Interface</h3>
              <p>Describe issues in plain language - no technical knowledge required. Chat-style interface with conversation history</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📝</div>
              <h3>Diagnostic Reports</h3>
              <p>Export comprehensive JSON reports with full telemetry data, AI analysis, and recommendations for documentation</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🌐</div>
              <h3>Offline Capability</h3>
              <p>Fallback diagnostic engine provides analysis even when the AI model is unavailable</p>
            </div>
          </div>
        </section>

        {/* Technology Stack */}
        <section className="about-section">
          <div className="section-icon">🔧</div>
          <h2>Technology Stack</h2>
          <div className="tech-stack">
            <div className="tech-category">
              <h4>Backend</h4>
              <ul>
                <li><strong>Django 4.2.7</strong> - Web framework</li>
                <li><strong>Django REST Framework</strong> - API development</li>
                <li><strong>Python 3.8+</strong> - Core language</li>
                <li><strong>Llama.cpp</strong> - Local LLM inference</li>
                <li><strong>PSUtil</strong> - System telemetry</li>
                <li><strong>GPUtil</strong> - GPU monitoring</li>
              </ul>
            </div>
            <div className="tech-category">
              <h4>Frontend</h4>
              <ul>
                <li><strong>React 18</strong> - UI framework</li>
                <li><strong>React Router</strong> - Navigation</li>
                <li><strong>Axios</strong> - HTTP client</li>
                <li><strong>Leaflet</strong> - Interactive maps</li>
                <li><strong>React-Leaflet</strong> - Map integration</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Architecture */}
        <section className="about-section">
          <div className="section-icon">🏗️</div>
          <h2>System Architecture</h2>
          <div className="architecture-info">
            <p>
              Our full-stack application combines Django's robust backend capabilities with React's 
              dynamic frontend to deliver a seamless diagnostic experience.
            </p>
            <div className="architecture-flow">
              <div className="flow-step">
                <div className="flow-number">1</div>
                <div className="flow-content">
                  <h4>User Input</h4>
                  <p>Natural language issue description via chat interface</p>
                </div>
              </div>
              <div className="flow-arrow">→</div>
              <div className="flow-step">
                <div className="flow-number">2</div>
                <div className="flow-content">
                  <h4>Telemetry Collection</h4>
                  <p>Real-time system metrics and issue-specific data</p>
                </div>
              </div>
              <div className="flow-arrow">→</div>
              <div className="flow-step">
                <div className="flow-number">3</div>
                <div className="flow-content">
                  <h4>AI Analysis</h4>
                  <p>Reasoning model processes symptoms and telemetry</p>
                </div>
              </div>
              <div className="flow-arrow">→</div>
              <div className="flow-step">
                <div className="flow-number">4</div>
                <div className="flow-content">
                  <h4>Actionable Results</h4>
                  <p>Diagnosis, solutions, and navigation options</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Key Capabilities */}
        <section className="about-section full-width">
          <div className="section-icon">✨</div>
          <h2>What Makes Us Different</h2>
          <div className="capabilities-grid">
            <div className="capability-item">
              <span className="capability-icon">🎓</span>
              <h3>Intelligent Learning</h3>
              <p>Advanced reasoning model that understands context and provides step-by-step diagnostic logic</p>
            </div>
            <div className="capability-item">
              <span className="capability-icon">📈</span>
              <h3>Data-Driven Insights</h3>
              <p>Real-time telemetry analysis correlates symptoms with actual system metrics for accurate diagnoses</p>
            </div>
            <div className="capability-item">
              <span className="capability-icon">🔄</span>
              <h3>Continuous Availability</h3>
              <p>Works 24/7 with offline fallback mode - never leaves you stranded</p>
            </div>
            <div className="capability-item">
              <span className="capability-icon">🌍</span>
              <h3>Location-Aware Service</h3>
              <p>Automatically finds nearby repair centers with real-time distance calculations</p>
            </div>
            <div className="capability-item">
              <span className="capability-icon">🔐</span>
              <h3>Hardware Verification</h3>
              <p>Cryptographic fingerprinting ensures component authenticity and detects tampering</p>
            </div>
            <div className="capability-item">
              <span className="capability-icon">📱</span>
              <h3>Fully Responsive</h3>
              <p>Seamless experience across desktop, tablet, and mobile devices</p>
            </div>
          </div>
        </section>

        {/* Statistics */}
        <section className="about-section full-width stats-section">
          <h2>By the Numbers</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-value">5+</div>
              <div className="stat-desc">Major Features</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">100%</div>
              <div className="stat-desc">Open Source</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">Zero</div>
              <div className="stat-desc">Cloud Dependencies</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">Real-Time</div>
              <div className="stat-desc">Telemetry Analysis</div>
            </div>
          </div>
        </section>

        {/* Project Highlights */}
        <section className="about-section full-width">
          <div className="section-icon">🏆</div>
          <h2>Project Highlights</h2>
          <div className="highlights-list">
            <div className="highlight-item">
              <div className="highlight-marker">✓</div>
              <div className="highlight-content">
                <h4>Machine Control Protocol (MCP) Integration</h4>
                <p>Structured task generation for programmatic system diagnostics with visual progress tracking</p>
              </div>
            </div>
            <div className="highlight-item">
              <div className="highlight-marker">✓</div>
              <div className="highlight-content">
                <h4>Conversation History Management</h4>
                <p>Complete session tracking with save/load functionality and auto-save capability</p>
              </div>
            </div>
            <div className="highlight-item">
              <div className="highlight-marker">✓</div>
              <div className="highlight-content">
                <h4>Interactive Service Center Map</h4>
                <p>OpenStreetMap integration with 30km radius search, brand filtering, and turn-by-turn directions</p>
              </div>
            </div>
            <div className="highlight-item">
              <div className="highlight-marker">✓</div>
              <div className="highlight-content">
                <h4>Hardware Hash Protection System</h4>
                <p>AES-256 encrypted hardware fingerprints for component verification and tamper detection</p>
              </div>
            </div>
            <div className="highlight-item">
              <div className="highlight-marker">✓</div>
              <div className="highlight-content">
                <h4>Responsive Typography System</h4>
                <p>Standardized font sizes, weights, and spacing across the entire application</p>
              </div>
            </div>
            <div className="highlight-item">
              <div className="highlight-marker">✓</div>
              <div className="highlight-content">
                <h4>Dark Theme UI/UX</h4>
                <p>Professional black and white design with clean visual hierarchy and smooth animations</p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="about-section cta-section">
          <div className="cta-content">
            <h2>Ready to Experience Next-Gen Diagnostics?</h2>
            <p>
              Join thousands of users who trust AutoMend for fast, accurate, and professional 
              PC diagnostics. Get started in seconds with our intelligent AI assistant.
            </p>
            <div className="cta-buttons">
              <a href="/diagnosis" className="cta-button primary">
                <span>Start Diagnosing Now</span>
                <span className="arrow">→</span>
              </a>
              <a href="/service-centers" className="cta-button secondary">
                <span>Find Service Centers</span>
                <span className="arrow">→</span>
              </a>
            </div>
          </div>
        </section>
      </div>
      
      <div className="about-footer">
        <div className="footer-content">
          <div className="footer-section">
            <h4>AutoMend AI</h4>
            <p>Professional PC diagnostics powered by artificial intelligence</p>
          </div>
          <div className="footer-section">
            <h4>Quick Links</h4>
            <ul>
              <li><a href="/diagnosis">Diagnosis</a></li>
              <li><a href="/service-centers">Service Centers</a></li>
              <li><a href="/hardware-protection">Hardware Protection</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Technology</h4>
            <ul>
              <li>Django Backend</li>
              <li>React Frontend</li>
              <li>Llama 3.1 AI Model</li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>Built with dedication using cutting-edge AI technology</p>
          <p className="version">Version 1.0.0 | © 2025 AutoMend AI | Open Source Project</p>
        </div>
      </div>
    </div>
  );
};

export default About;

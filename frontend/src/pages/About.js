import React from 'react';
import './About.css';

const About = () => {
  return (
    <div className="about-page">
      <div className="about-hero">
        <h1>About Our AI PC Diagnostic Solution</h1>
        <p className="about-subtitle">
          Revolutionizing computer hardware diagnostics with advanced artificial intelligence
        </p>
      </div>
      
      <div className="about-content">
        <section className="about-section">
          <div className="section-icon">🎯</div>
          <h2>Our Mission</h2>
          <p>
            We're dedicated to making computer hardware diagnostics accessible to everyone. 
            Our AI-powered solution eliminates the need for expensive technician visits by 
            providing instant, accurate diagnostics that anyone can understand and act upon.
          </p>
        </section>
        
        <section className="about-section">
          <div className="section-icon">🚀</div>
          <h2>What We Do</h2>
          <p>
            Our platform combines cutting-edge artificial intelligence with deep hardware 
            expertise to analyze PC issues in real-time. Simply describe your problem in 
            plain language, and our AI assistant will guide you through the diagnostic 
            process, identify the root cause, and provide actionable solutions.
          </p>
        </section>
        
        <section className="about-section">
          <div className="section-icon">⚡</div>
          <h2>Key Features</h2>
          <div className="features-list">
            <div className="feature-item">
              <span className="feature-bullet">✓</span>
              <div>
                <strong>Natural Language Processing:</strong> Describe issues in your own words
              </div>
            </div>
            <div className="feature-item">
              <span className="feature-bullet">✓</span>
              <div>
                <strong>Real-time Analysis:</strong> Get instant diagnostic results
              </div>
            </div>
            <div className="feature-item">
              <span className="feature-bullet">✓</span>
              <div>
                <strong>Comprehensive Solutions:</strong> Step-by-step repair guidance
              </div>
            </div>
            <div className="feature-item">
              <span className="feature-bullet">✓</span>
              <div>
                <strong>24/7 Availability:</strong> Access help whenever you need it
              </div>
            </div>
            <div className="feature-item">
              <span className="feature-bullet">✓</span>
              <div>
                <strong>Continuous Learning:</strong> AI that improves with every interaction
              </div>
            </div>
          </div>
        </section>
        
        <section className="about-section">
          <div className="section-icon">🔬</div>
          <h2>Our Technology</h2>
          <p>
            Powered by advanced machine learning models, our system has been trained on 
            thousands of hardware diagnostic scenarios. It understands the intricate 
            relationships between symptoms and hardware failures, providing diagnoses 
            that rival those of experienced technicians.
          </p>
        </section>
        
        <section className="about-section">
          <div className="section-icon">🌟</div>
          <h2>Why Choose Us</h2>
          <div className="benefits-grid">
            <div className="benefit-card">
              <h3>Cost-Effective</h3>
              <p>Save money on diagnostic fees and unnecessary repairs</p>
            </div>
            <div className="benefit-card">
              <h3>Time-Saving</h3>
              <p>No waiting for appointments or shipping devices</p>
            </div>
            <div className="benefit-card">
              <h3>Expert-Level</h3>
              <p>Professional diagnostics without the professional price tag</p>
            </div>
            <div className="benefit-card">
              <h3>User-Friendly</h3>
              <p>No technical knowledge required</p>
            </div>
          </div>
        </section>
        
        <section className="about-section cta-section">
          <h2>Ready to Get Started?</h2>
          <p>
            Experience the future of PC diagnostics. Our AI assistant is ready to help 
            you solve your hardware issues quickly and efficiently.
          </p>
          <a href="/diagnosis" className="cta-button">
            Start Diagnosing Now
            <span className="arrow">→</span>
          </a>
        </section>
      </div>
      
      <div className="about-footer">
        <p>Built with ❤️ using cutting-edge AI technology</p>
        <p className="version">Version 1.0.0 | © 2025 AutoMend</p>
      </div>
    </div>
  );
};

export default About;

import React from 'react';
import { Link } from 'react-router-dom';
import './About.css';

const About = () => {
  const features = [
    {
      title: "AI-Powered Diagnostics",
      description: "Advanced machine learning models analyze your PC's symptoms and provide accurate diagnoses in real-time."
    },
    {
      title: "Real-Time Monitoring",
      description: "Continuous hardware monitoring tracks CPU, GPU, RAM, and storage health to detect issues before they become critical."
    },
    {
      title: "Pattern Recognition",
      description: "Our AI learns from thousands of diagnostic cases to identify complex patterns and anomalies in system behavior."
    },
    {
      title: "Interactive Chat",
      description: "Conversational interface makes troubleshooting easy - just describe your problem in plain English."
    },
    {
      title: "Hardware Protection",
      description: "Unique hardware fingerprinting system helps protect against unauthorized repairs and component swaps."
    },
    {
      title: "Detailed Reports",
      description: "Comprehensive diagnostic reports with insights, recommendations, and step-by-step solutions."
    }
  ];

  const techStack = {
    frontend: ["React", "React Router", "Axios", "Modern CSS3"],
    backend: ["Django", "Django REST Framework", "AutoGen", "Python"],
    ai: ["Multi-Agent System", "LLM Integration", "Pattern Analysis", "Anomaly Detection"],
    infrastructure: ["SQLite Database", "CORS Support", "RESTful API", "WebSocket Support"]
  };

  return (
    <div className="about-page">
      {/* Hero Section */}
      <div className="about-hero">
        <div className="hero-badge">AI-Driven PC Diagnostics</div>
        <h1>About Our Platform</h1>
        <p className="about-subtitle">
          Revolutionizing PC troubleshooting with artificial intelligence, 
          providing instant, accurate diagnostics for all your hardware issues.
        </p>
      </div>

      {/* Main Content */}
      <div className="about-content">
        {/* Mission Section */}
        <div className="about-section">
          <h2>Our Mission</h2>
          <p>
            We're on a mission to democratize PC diagnostics and make expert-level troubleshooting 
            accessible to everyone. By combining advanced AI technology with intuitive user experience, 
            we empower users to understand and solve their PC issues quickly and confidently. No more 
            expensive repair shop visits for simple problems - our AI assistant guides you every step 
            of the way.
          </p>
        </div>

        {/* How It Works */}
        <div className="about-section">
          <h2>How It Works</h2>
          <div className="features-list">
            <div className="feature-item">
              <div className="feature-bullet">1</div>
              <div>
                <strong>Describe Your Issue</strong>
                <br />
                Simply type what's wrong with your PC in natural language - no technical jargon required.
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-bullet">2</div>
              <div>
                <strong>AI Analysis</strong>
                <br />
                Our multi-agent AI system analyzes your symptoms, cross-references with known issues, and identifies potential causes.
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-bullet">3</div>
              <div>
                <strong>Real-Time Monitoring</strong>
                <br />
                If needed, we monitor your hardware in real-time to gather telemetry data and pinpoint the exact problem.
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-bullet">4</div>
              <div>
                <strong>Get Solutions</strong>
                <br />
                Receive step-by-step solutions, troubleshooting guides, and recommendations tailored to your specific issue.
              </div>
            </div>
          </div>
        </div>

        {/* Key Features */}
        <div className="about-section">
          <h2>Key Features</h2>
          <div className="features-grid">
            {features.map((feature, index) => (
              <div key={index} className="feature-card">
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Technology Stack */}
        <div className="about-section">
          <h2>Technology Stack</h2>
          <div className="tech-stack">
            <div className="tech-category">
              <h4>Frontend</h4>
              <ul>
                {techStack.frontend.map((tech, idx) => (
                  <li key={idx}>{tech}</li>
                ))}
              </ul>
            </div>
            <div className="tech-category">
              <h4>Backend</h4>
              <ul>
                {techStack.backend.map((tech, idx) => (
                  <li key={idx}>{tech}</li>
                ))}
              </ul>
            </div>
            <div className="tech-category">
              <h4>AI & Machine Learning</h4>
              <ul>
                {techStack.ai.map((tech, idx) => (
                  <li key={idx}>{tech}</li>
                ))}
              </ul>
            </div>
            <div className="tech-category">
              <h4>Infrastructure</h4>
              <ul>
                {techStack.infrastructure.map((tech, idx) => (
                  <li key={idx}>{tech}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Why Choose Us */}
        <div className="about-section">
          <h2>Why Choose Us</h2>
          <div className="benefits-grid">
            <div className="benefit-card">
              <h3>Free & Accessible</h3>
              <p>
                Our diagnostic service is completely free. No hidden costs, no subscriptions - 
                just instant help when you need it.
              </p>
            </div>
            <div className="benefit-card">
              <h3>Expert AI</h3>
              <p>
                Our multi-agent AI system is trained on thousands of real-world PC issues, 
                providing expert-level diagnostics.
              </p>
            </div>
            <div className="benefit-card">
              <h3>Privacy First</h3>
              <p>
                Your data stays private. We don't collect unnecessary information, and all 
                diagnostics are processed securely.
              </p>
            </div>
            <div className="benefit-card">
              <h3>Always Learning</h3>
              <p>
                Our AI continuously learns from new cases, improving accuracy and expanding 
                its knowledge base every day.
              </p>
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="about-section cta-section">
          <div className="cta-content">
            <h2>Ready to Diagnose Your PC?</h2>
            <p>
              Join thousands of users who have solved their PC issues with our AI assistant. 
              Get started in seconds - no registration required.
            </p>
            <div className="cta-buttons">
              <Link to="/diagnosis" className="cta-button primary">
                Start Free Diagnosis
                <span className="arrow">→</span>
              </Link>
              <Link to="/hardware-protection" className="cta-button secondary">
                Hardware Protection
                <span className="arrow">→</span>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="about-footer">
        <p>Built using cutting-edge AI technology</p>
        <p className="version">Version 1.0.0 | Last Updated: November 2025</p>
      </div>
    </div>
  );
};

export default About;

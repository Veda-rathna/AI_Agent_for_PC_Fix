import React, { useState, useRef, useEffect } from 'react';
import './DiagnosticChat.css';

const DiagnosticChat = () => {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const [processingTime, setProcessingTime] = useState(0);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Timer for showing processing time
  useEffect(() => {
    let interval;
    if (isLoading) {
      setProcessingTime(0);
      interval = setInterval(() => {
        setProcessingTime(prev => prev + 1);
      }, 1000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isLoading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputText.trim()) {
      return;
    }

    // Add user message to chat
    const userMessage = {
      type: 'user',
      content: inputText,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    setError(null);

    try {
      // Create an AbortController for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 600000); // 600 second (10 minute) timeout for reasoning models

      const response = await fetch('http://localhost:8000/api/predict/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input_text: inputText,
          // Optional: Add telemetry data if available
          // telemetry_data: { ... }
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      const data = await response.json();

      if (data.success) {
        // Add AI response to chat
        const aiMessage = {
          type: 'assistant',
          content: data.message || data.prediction, // Use 'message' field primarily
          model: data.model,
          finishReason: data.finish_reason,
          usage: data.usage,
          timestamp: new Date().toISOString()
        };
        
        setMessages(prev => [...prev, aiMessage]);
      } else {
        // Handle error response
        setError(data.error || 'An error occurred while processing your request.');
      }
    } catch (err) {
      console.error('Error:', err);
      
      if (err.name === 'AbortError') {
        setError('⚠️ Request timed out after 10 minutes. The reasoning model is taking unusually long. This could mean: 1) The model is processing a very complex query, 2) The model server is overloaded. Please try: 1) A simpler question, 2) Restarting the model server, 3) Checking server logs for errors.');
      } else if (err.message === 'Failed to fetch') {
        setError('❌ Could not connect to the backend server. Please ensure: 1) Backend is running at http://localhost:8000, 2) No firewall blocking the connection, 3) Check terminal for backend errors.');
      } else {
        setError(`❌ Error: ${err.message}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const formatMessage = (content) => {
    // Convert markdown-style formatting to HTML
    // This is a simple implementation - you might want to use a proper markdown library
    return content
      .split('\n')
      .map((line, index) => {
        // Handle headers
        if (line.startsWith('### ')) {
          return <h3 key={index}>{line.substring(4)}</h3>;
        }
        if (line.startsWith('## ')) {
          return <h2 key={index}>{line.substring(3)}</h2>;
        }
        if (line.startsWith('**') && line.endsWith('**')) {
          return <strong key={index}>{line.substring(2, line.length - 2)}</strong>;
        }
        // Handle bullet points
        if (line.trim().startsWith('*   ') || line.trim().startsWith('- ')) {
          return <li key={index}>{line.trim().substring(4)}</li>;
        }
        // Regular paragraph
        if (line.trim()) {
          return <p key={index}>{line}</p>;
        }
        return <br key={index} />;
      });
  };

  return (
    <div className="diagnostic-chat">
      {/* Welcome Screen - shown when no messages */}
      {messages.length === 0 && !isLoading && (
        <div className="welcome-screen">
          <div className="welcome-content">
            <div className="welcome-icon">🔧</div>
            <h1>AutoMend AI Diagnostic</h1>
            <p>Describe your PC issue and I'll help you diagnose and fix it</p>
            <div className="example-prompts">
              <button 
                className="example-prompt"
                onClick={() => setInputText("My computer is running very slow")}
              >
                My computer is running very slow
              </button>
              <button 
                className="example-prompt"
                onClick={() => setInputText("Blue screen error on startup")}
              >
                Blue screen error on startup
              </button>
              <button 
                className="example-prompt"
                onClick={() => setInputText("Screen flickering issues")}
              >
                Screen flickering issues
              </button>
              <button 
                className="example-prompt"
                onClick={() => setInputText("Computer won't turn on")}
              >
                Computer won't turn on
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Chat Messages */}
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <div className="message-avatar">
              {msg.type === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-body">
              <div className="message-content">
                {msg.type === 'assistant' ? formatMessage(msg.content) : msg.content}
              </div>
              {msg.usage && (
                <div className="message-metadata">
                  <small>
                    {msg.model} · {msg.usage.total_tokens} tokens
                  </small>
                </div>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-body">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <div className="processing-info">
                  {processingTime > 5 && processingTime <= 30 && (
                    <small>🧠 Reasoning model is thinking... ({processingTime}s)</small>
                  )}
                  {processingTime > 30 && processingTime <= 90 && (
                    <small>🔍 Deep analysis in progress... ({processingTime}s) - Reasoning models take time for complex queries</small>
                  )}
                  {processingTime > 90 && processingTime <= 180 && (
                    <small>⏳ Still processing... ({processingTime}s) - Model is performing detailed reasoning</small>
                  )}
                  {processingTime > 180 && (
                    <small>⚠️ Taking longer than usual... ({processingTime}s) - Please wait, the model should respond soon (max 10 minutes)</small>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="error-message">
            <strong>⚠️ Error:</strong> {error}
          </div>
        )}
        
        {/* Auto-scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <div className="input-container">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Describe your PC issue..."
            disabled={isLoading}
            rows="1"
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
          />
          <button type="submit" disabled={isLoading || !inputText.trim()}>
            <span className="send-icon">↑</span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default DiagnosticChat;

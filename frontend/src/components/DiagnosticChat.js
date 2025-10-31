import React, { useState } from 'react';
import './DiagnosticChat.css';

const DiagnosticChat = () => {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

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
      const response = await fetch('http://localhost:8000/api/predict/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input_text: inputText,
          // Optional: Add telemetry data if available
          // telemetry_data: { ... }
        })
      });

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
      setError(
        err.message === 'Failed to fetch' 
          ? 'Could not connect to the server. Please ensure the backend is running.'
          : `Error: ${err.message}`
      );
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
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="error-message">
            <strong>⚠️ Error:</strong> {error}
          </div>
        )}
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

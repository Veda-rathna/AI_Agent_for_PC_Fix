import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Choose which endpoint to use
  const USE_REASONING_MODEL = true; // Set to false to use the simple diagnose endpoint

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputValue.trim()) return;

    // Add user message to chat
    const userMessage = {
      type: 'user',
      text: inputValue,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      let aiMessage;

      if (USE_REASONING_MODEL) {
        // Call the new predict endpoint with reasoning model
        const response = await axios.post('http://localhost:8000/api/predict/', {
          input_text: inputValue,
          // Optional: add telemetry data
          // telemetry_data: { ... }
        });

        if (response.data.success) {
          aiMessage = {
            type: 'ai',
            text: response.data.message || response.data.prediction, // Primary field is 'message'
            model: response.data.model,
            usage: response.data.usage,
            timestamp: new Date().toISOString()
          };
        } else {
          throw new Error(response.data.error || 'Failed to get AI response');
        }
      } else {
        // Call the simple diagnose endpoint
        const response = await axios.post('http://localhost:8000/api/diagnose/', {
          query: inputValue,
          timestamp: new Date().toISOString()
        });

        aiMessage = {
          type: 'ai',
          text: response.data.diagnosis,
          timestamp: response.data.timestamp || new Date().toISOString()
        };
      }

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error calling API:', error);
      
      // Add error message to chat
      const errorMessage = {
        type: 'error',
        text: error.response?.data?.error || 
              error.message || 
              'Sorry, I encountered an error. Please make sure the Django server is running.',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Format message content (handle markdown)
  const formatMessage = (text) => {
    if (!text) return '';
    
    // Split by lines and format
    return text.split('\n').map((line, index) => {
      // Bold sections
      if (line.startsWith('**') && line.endsWith('**')) {
        return <div key={index} className="message-section-header">
          {line.substring(2, line.length - 2)}
        </div>;
      }
      
      // Subsection headers
      if (line.startsWith('### ')) {
        return <div key={index} className="message-subsection">
          {line.substring(4)}
        </div>;
      }
      
      // Bullet points
      if (line.trim().startsWith('*   ') || line.trim().startsWith('- ')) {
        return <div key={index} className="message-bullet">
          • {line.trim().substring(4)}
        </div>;
      }
      
      // Numbered list items
      const numberedMatch = line.match(/^(\d+\.\s+)/);
      if (numberedMatch) {
        return <div key={index} className="message-numbered">
          {line}
        </div>;
      }
      
      // Regular paragraph
      if (line.trim()) {
        return <div key={index} className="message-paragraph">{line}</div>;
      }
      
      // Empty line
      return <div key={index} className="message-spacer"></div>;
    });
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">
          <h1>🔧 AI PC Diagnostic Assistant</h1>
          <p>
            {USE_REASONING_MODEL 
              ? 'Using Advanced Reasoning Model - Responses may take 30-120 seconds'
              : 'Using Quick Diagnostic Mode'
            }
          </p>
        </div>

        <div className="chat-messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}-message`}>
              <div className="message-content">
                <span className="message-icon">
                  {message.type === 'user' && '👤'}
                  {message.type === 'ai' && '🤖'}
                  {message.type === 'error' && '⚠️'}
                </span>
                <div className="message-text">
                  {message.type === 'ai' ? formatMessage(message.text) : message.text}
                </div>
              </div>
              
              {/* Show token usage for AI messages if available */}
              {message.usage && (
                <div className="message-metadata">
                  <small>
                    Model: {message.model} | 
                    Tokens: {message.usage.total_tokens} 
                    ({message.usage.prompt_tokens} in, {message.usage.completion_tokens} out)
                  </small>
                </div>
              )}
            </div>
          ))}
          
          {isLoading && (
            <div className="message ai-message">
              <div className="message-content">
                <span className="message-icon">🤖</span>
                <div className="message-text">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  {USE_REASONING_MODEL && (
                    <div className="loading-text">
                      Analyzing your issue deeply... This may take up to 2 minutes.
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>

        <form className="chat-input-form" onSubmit={handleSubmit}>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Describe your PC issue..."
            disabled={isLoading}
            className="chat-input"
          />
          <button type="submit" disabled={isLoading || !inputValue.trim()} className="send-button">
            {isLoading ? 'Processing...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;

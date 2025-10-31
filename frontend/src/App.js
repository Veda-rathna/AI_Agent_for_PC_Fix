import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

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
      // Call Django API
      const response = await axios.post('http://localhost:8000/api/diagnose/', {
        query: inputValue,
        timestamp: new Date().toISOString()
      });

      // Add AI response to chat
      const aiMessage = {
        type: 'ai',
        text: response.data.diagnosis,
        timestamp: response.data.timestamp || new Date().toISOString()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error calling API:', error);
      
      // Add error message to chat
      const errorMessage = {
        type: 'error',
        text: 'Sorry, I encountered an error. Please make sure the Django server is running.',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">
          <h1>🔧 AI PC Diagnostic Assistant</h1>
          <p>Ask me about your PC issues!</p>
        </div>

        <div className="chat-messages">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>Welcome! 👋</h2>
              <p>I'm your AI-powered PC diagnostic assistant. Describe any issues you're experiencing with your computer, and I'll help diagnose the problem.</p>
            </div>
          )}
          
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}-message`}>
              <div className="message-content">
                <span className="message-icon">
                  {message.type === 'user' && '👤'}
                  {message.type === 'ai' && '🤖'}
                  {message.type === 'error' && '⚠️'}
                </span>
                <div className="message-text">{message.text}</div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message ai-message">
              <div className="message-content">
                <span className="message-icon">🤖</span>
                <div className="message-text typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
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
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;

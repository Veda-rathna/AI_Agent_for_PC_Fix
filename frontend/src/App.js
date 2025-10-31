import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Function to extract and remove MCP_TASKS from the response
  const extractMCPTasks = (text) => {
    const mcpRegex = /<MCP_TASKS>[\s\S]*?<\/MCP_TASKS>/;
    const match = text.match(mcpRegex);
    
    let mcpTasks = null;
    let cleanedText = text;
    
    if (match) {
      try {
        // Extract the JSON content between the tags
        const jsonStr = match[0].replace(/<\/?MCP_TASKS>/g, '').trim();
        mcpTasks = JSON.parse(jsonStr);
      } catch (e) {
        console.error('Failed to parse MCP_TASKS:', e);
      }
      // Remove the MCP_TASKS section from the text
      cleanedText = text.replace(mcpRegex, '').trim();
    }
    
    return { cleanedText, mcpTasks };
  };

  // Function to format message text with proper line breaks and styling
  const formatMessage = (text) => {
    if (!text) return '';
    
    return text.split('\n').map((line, index) => {
      const trimmedLine = line.trim();
      
      // Skip empty lines
      if (!trimmedLine) {
        return <br key={index} />;
      }
      
      // Headers (bold sections)
      if (line.startsWith('**') && line.endsWith('**')) {
        return (
          <div key={index} style={{ fontWeight: 'bold', marginTop: '10px', marginBottom: '5px' }}>
            {line.substring(2, line.length - 2)}
          </div>
        );
      }
      
      // Subsection headers
      if (line.startsWith('### ')) {
        return (
          <div key={index} style={{ fontWeight: '600', marginTop: '8px', marginBottom: '4px' }}>
            {line.substring(4)}
          </div>
        );
      }
      
      // Bullet points
      if (trimmedLine.startsWith('*   ') || trimmedLine.startsWith('- ')) {
        return (
          <div key={index} style={{ marginLeft: '20px', marginBottom: '3px' }}>
            • {trimmedLine.substring(4)}
          </div>
        );
      }
      
      // Numbered list items
      const numberedMatch = trimmedLine.match(/^(\d+\.\s+)/);
      if (numberedMatch) {
        return (
          <div key={index} style={{ marginLeft: '20px', marginBottom: '3px' }}>
            {trimmedLine}
          </div>
        );
      }
      
      // Regular paragraph
      return (
        <div key={index} style={{ marginBottom: '8px', lineHeight: '1.5' }}>
          {line}
        </div>
      );
    });
  };

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
      // Call Django API with the predict endpoint
      const response = await axios.post('http://localhost:8000/api/predict/', {
        input_text: inputValue,
        // Optional: add telemetry data if available
        // telemetry_data: { ... }
      });

      if (response.data.success) {
        // Extract and clean the message
        const rawText = response.data.message || response.data.prediction;
        const { cleanedText, mcpTasks } = extractMCPTasks(rawText);
        
        // Add AI response to chat (without MCP_TASKS)
        const aiMessage = {
          type: 'ai',
          text: cleanedText,
          model: response.data.model,
          usage: response.data.usage,
          mcpTasks: mcpTasks, // Store for potential future use
          timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, aiMessage]);
      } else {
        // Handle error response from backend
        throw new Error(response.data.error || 'Failed to get AI response');
      }
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

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">
          <h1>🔧 AI PC Diagnostic Assistant</h1>
          <p>Using Advanced Reasoning Model - Responses may take 30-120 seconds</p>
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
                <div className="message-text">
                  {message.type === 'ai' ? formatMessage(message.text) : message.text}
                </div>
              </div>
              {/* Show token usage for AI messages if available */}
              {message.usage && (
                <div className="message-metadata" style={{ 
                  fontSize: '0.8em', 
                  color: '#666', 
                  marginTop: '5px',
                  paddingLeft: '40px'
                }}>
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
                  <p style={{ marginTop: '10px', fontSize: '0.9em', color: '#666' }}>
                    Analyzing your issue deeply... This may take up to 2 minutes.
                  </p>
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

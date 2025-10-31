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
        setError('Request timed out after 10 minutes. The reasoning model is taking unusually long. This could mean: 1) The model is processing a very complex query, 2) The model server is overloaded. Please try: 1) A simpler question, 2) Restarting the model server, 3) Checking server logs for errors.');
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
    // Helper function to parse inline formatting (bold, italic, code)
    const parseInlineFormatting = (text) => {
      const parts = [];
      let currentIndex = 0;
      let key = 0;

      // Regular expression to match **bold**, *italic*, and `code`
      const regex = /(\*\*.*?\*\*|\*.*?\*|`.*?`)/g;
      let match;

      while ((match = regex.exec(text)) !== null) {
        // Add text before the match
        if (match.index > currentIndex) {
          parts.push(text.substring(currentIndex, match.index));
        }

        const matchedText = match[0];
        
        // Handle bold **text**
        if (matchedText.startsWith('**') && matchedText.endsWith('**')) {
          parts.push(
            <strong key={`bold-${key++}`}>
              {matchedText.substring(2, matchedText.length - 2)}
            </strong>
          );
        }
        // Handle italic *text*
        else if (matchedText.startsWith('*') && matchedText.endsWith('*') && !matchedText.startsWith('**')) {
          parts.push(
            <em key={`italic-${key++}`}>
              {matchedText.substring(1, matchedText.length - 1)}
            </em>
          );
        }
        // Handle code `text`
        else if (matchedText.startsWith('`') && matchedText.endsWith('`')) {
          parts.push(
            <code key={`code-${key++}`}>
              {matchedText.substring(1, matchedText.length - 1)}
            </code>
          );
        }

        currentIndex = match.index + matchedText.length;
      }

      // Add remaining text
      if (currentIndex < text.length) {
        parts.push(text.substring(currentIndex));
      }

      return parts.length > 0 ? parts : text;
    };

    // Convert markdown-style formatting to HTML
    return content
      .split('\n')
      .map((line, index) => {
        // Handle headers
        if (line.startsWith('### ')) {
          return <h3 key={index}>{parseInlineFormatting(line.substring(4))}</h3>;
        }
        if (line.startsWith('## ')) {
          return <h2 key={index}>{parseInlineFormatting(line.substring(3))}</h2>;
        }
        if (line.startsWith('# ')) {
          return <h1 key={index}>{parseInlineFormatting(line.substring(2))}</h1>;
        }
        // Handle bullet points
        if (line.trim().startsWith('* ') || line.trim().startsWith('- ')) {
          const bulletText = line.trim().startsWith('* ') 
            ? line.trim().substring(2) 
            : line.trim().substring(2);
          return <li key={index}>{parseInlineFormatting(bulletText)}</li>;
        }
        // Handle numbered lists
        if (/^\d+\.\s/.test(line.trim())) {
          const listText = line.trim().replace(/^\d+\.\s/, '');
          return <li key={index}>{parseInlineFormatting(listText)}</li>;
        }
        // Regular paragraph
        if (line.trim()) {
          return <p key={index}>{parseInlineFormatting(line)}</p>;
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
              {msg.type === 'user' ? 'U' : 'AI'}
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
            <div className="message-avatar">AI</div>
            <div className="message-body">
              <div className="message-content">
                <div className="typing-indicator">
                  <div className="spinner"></div>
                  <span className="processing-info">
                    {processingTime <= 5 && (
                      <small>Thinking...</small>
                    )}
                    {processingTime > 5 && processingTime <= 30 && (
                      <small>Reasoning model is thinking... ({processingTime}s)</small>
                    )}
                    {processingTime > 30 && processingTime <= 90 && (
                      <small>Deep analysis in progress... ({processingTime}s) - Reasoning models take time for complex queries</small>
                    )}
                    {processingTime > 90 && processingTime <= 180 && (
                      <small>Still processing... ({processingTime}s) - Model is performing detailed reasoning</small>
                    )}
                    {processingTime > 180 && (
                      <small>Taking longer than usual... ({processingTime}s) - Please wait, the model should respond soon (max 10 minutes)</small>
                    )}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
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

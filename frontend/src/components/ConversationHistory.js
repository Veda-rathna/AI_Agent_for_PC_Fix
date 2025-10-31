import React, { useState, useEffect } from 'react';
import './ConversationHistory.css';

const ConversationHistory = ({ onSelectConversation, currentConversationId }) => {
  const [conversations, setConversations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isExpanded, setIsExpanded] = useState(true);

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/conversations/');
      const data = await response.json();
      
      if (data.success) {
        setConversations(data.conversations);
      } else {
        setError(data.error || 'Failed to load conversations');
      }
    } catch (err) {
      console.error('Error loading conversations:', err);
      setError('Failed to load conversation history');
    } finally {
      setIsLoading(false);
    }
  };

  const deleteConversation = async (conversationId, event) => {
    event.stopPropagation();
    
    if (!window.confirm('Are you sure you want to delete this conversation?')) {
      return;
    }
    
    try {
      const response = await fetch(
        `http://localhost:8000/api/conversations/${conversationId}/delete/`,
        { method: 'DELETE' }
      );
      
      const data = await response.json();
      
      if (data.success) {
        // Remove from list
        setConversations(conversations.filter(c => c.id !== conversationId));
        
        // If this was the current conversation, notify parent
        if (conversationId === currentConversationId) {
          onSelectConversation(null);
        }
      } else {
        alert('Failed to delete conversation');
      }
    } catch (err) {
      console.error('Error deleting conversation:', err);
      alert('Failed to delete conversation');
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    
    return date.toLocaleDateString();
  };

  return (
    <div className={`conversation-history ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="history-header">
        <button 
          className="toggle-button"
          onClick={() => setIsExpanded(!isExpanded)}
          title={isExpanded ? 'Collapse' : 'Expand'}
        >
          {isExpanded ? '◀' : '▶'}
        </button>
        
        {isExpanded && (
          <>
            <h3>Chat History</h3>
            <button 
              className="new-chat-button"
              onClick={() => onSelectConversation(null)}
              title="New Chat"
            >
              ✚
            </button>
          </>
        )}
      </div>

      {isExpanded && (
        <div className="history-content">
          {isLoading && (
            <div className="history-loading">
              <div className="spinner-small"></div>
              <span>Loading...</span>
            </div>
          )}

          {error && (
            <div className="history-error">
              <p>{error}</p>
              <button onClick={loadConversations}>Retry</button>
            </div>
          )}

          {!isLoading && !error && conversations.length === 0 && (
            <div className="history-empty">
              <p>No conversations yet</p>
              <small>Start a new chat to begin</small>
            </div>
          )}

          {!isLoading && !error && conversations.length > 0 && (
            <div className="conversation-list">
              {conversations.map((conversation) => (
                <div
                  key={conversation.id}
                  className={`conversation-item ${
                    conversation.id === currentConversationId ? 'active' : ''
                  }`}
                  onClick={() => onSelectConversation(conversation.id)}
                >
                  <div className="conversation-info">
                    <div className="conversation-title">
                      {conversation.title}
                    </div>
                    <div className="conversation-meta">
                      <span className="message-count">
                        {conversation.message_count} messages
                      </span>
                      <span className="conversation-date">
                        {formatDate(conversation.updated_at)}
                      </span>
                    </div>
                    {conversation.last_message && (
                      <div className="last-message">
                        {conversation.last_message.content}
                      </div>
                    )}
                  </div>
                  <button
                    className="delete-button"
                    onClick={(e) => deleteConversation(conversation.id, e)}
                    title="Delete conversation"
                  >
                    🗑️
                  </button>
                </div>
              ))}
            </div>
          )}

          <div className="history-footer">
            <button className="refresh-button" onClick={loadConversations}>
              ↻ Refresh
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ConversationHistory;

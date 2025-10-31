# Conversation History Feature - ChatGPT-Style Storage

## Overview
The conversation history feature allows users to save, view, and manage their diagnostic chat conversations, similar to ChatGPT's conversation management system.

## Features Implemented

### 1. **Automatic Conversation Saving**
- ✅ Every message exchange is automatically saved to the database
- ✅ No manual save action required from users
- ✅ Conversations are preserved across browser sessions
- ✅ Auto-generated conversation titles from the first user message

### 2. **Conversation History Sidebar**
- ✅ Collapsible sidebar showing all past conversations
- ✅ Shows conversation title, message count, and last updated time
- ✅ Quick preview of the last message in each conversation
- ✅ Smooth expand/collapse animation
- ✅ Real-time "time ago" formatting (e.g., "5m ago", "2h ago", "3d ago")

### 3. **Conversation Management**
- ✅ Create new conversations
- ✅ Load previous conversations
- ✅ Delete conversations with confirmation
- ✅ Archive conversations (optional feature)
- ✅ Active conversation highlighting

### 4. **Data Storage**
The system stores:
- 💾 Message content and type (user/assistant)
- 💾 Timestamps for each message
- 💾 AI model information
- 💾 Token usage statistics
- 💾 Conversation metadata (total messages, resolution status)

## Backend Architecture

### Database Models

#### 1. **Conversation Model**
```python
- id: UUID (primary key)
- title: String (auto-generated or custom)
- created_at: DateTime
- updated_at: DateTime
- is_archived: Boolean
```

#### 2. **Message Model**
```python
- id: UUID (primary key)
- conversation: ForeignKey to Conversation
- message_type: 'user' | 'assistant' | 'system'
- content: Text
- timestamp: DateTime
- model_name: String (optional)
- finish_reason: String (optional)
- tokens_used: Integer (optional)
- session_id: String (optional)
```

#### 3. **ConversationMetadata Model**
```python
- conversation: OneToOne to Conversation
- total_messages: Integer
- total_tokens: Integer
- issue_category: String (optional)
- resolution_status: 'unresolved' | 'resolved' | 'in_progress'
```

### API Endpoints

#### List Conversations
```
GET /api/conversations/
Query Params:
  - archived: true/false
  - limit: number (default 50)
  - offset: number (default 0)
```

#### Get Specific Conversation
```
GET /api/conversations/{conversation_id}/
```

#### Create New Conversation
```
POST /api/conversations/create/
Body:
  {
    "title": "Optional custom title",
    "first_message": "Optional initial message"
  }
```

#### Add Message to Conversation
```
POST /api/conversations/{conversation_id}/messages/
Body:
  {
    "message_type": "user" | "assistant",
    "content": "Message content",
    "model_name": "Optional model name",
    "tokens_used": 0
  }
```

#### Update Conversation
```
PUT /api/conversations/{conversation_id}/update/
Body:
  {
    "title": "New title",
    "is_archived": true/false,
    "resolution_status": "resolved"
  }
```

#### Delete Conversation
```
DELETE /api/conversations/{conversation_id}/delete/
```

#### Bulk Save Conversation
```
POST /api/conversations/save-bulk/
Body:
  {
    "conversation_id": "uuid (optional)",
    "title": "Conversation title",
    "messages": [
      {
        "type": "user",
        "content": "...",
        "timestamp": "ISO datetime"
      }
    ]
  }
```

## Frontend Components

### 1. **ConversationHistory Component**
Location: `frontend/src/components/ConversationHistory.js`

Features:
- Displays list of all conversations
- Handles conversation selection
- Delete confirmation dialog
- Refresh functionality
- Collapsible sidebar with toggle button
- New chat button

### 2. **Updated DiagnosticChat Component**
Location: `frontend/src/components/DiagnosticChat.js`

New Features:
- Auto-save messages to current conversation
- Load conversation functionality
- Current conversation ID tracking
- Integration with ConversationHistory sidebar

## User Interface

### Sidebar Features
- **Expand/Collapse**: Toggle button to show/hide full sidebar
- **New Chat**: Create a fresh conversation
- **Conversation Items**: 
  - Title (auto-generated from first message)
  - Message count
  - Time since last update
  - Last message preview
  - Delete button (appears on hover)
- **Active Highlighting**: Current conversation is highlighted
- **Refresh Button**: Reload conversation list

### Styling
- Dark theme matching the main chat interface
- Gradient backgrounds
- Smooth animations and transitions
- Responsive design for mobile devices
- Hover effects for better UX

## How It Works

### Automatic Save Flow
1. User sends a message
2. Message is added to local state
3. AI responds
4. Response is added to local state
5. `useEffect` hook detects message change
6. Entire conversation is saved to database via bulk save API
7. If it's a new conversation, the ID is stored for future saves

### Load Flow
1. User clicks on a conversation in sidebar
2. API fetches conversation with all messages
3. Messages are loaded into chat interface
4. Conversation ID is set as current
5. User can continue the conversation

### Title Generation
- First user message is analyzed
- First 50 characters are extracted
- Extra whitespace is removed
- Ellipsis added if truncated
- Title is stored with conversation

## Configuration

### Database
- Uses SQLite by default (Django's default)
- Can be upgraded to PostgreSQL for production
- Migrations included for easy setup

### Installation Steps

1. **Backend Setup**:
```bash
cd backend
python manage.py makemigrations ai_diagnostic
python manage.py migrate
```

2. **Start Backend**:
```bash
python manage.py runserver
```

3. **Frontend** (already configured):
```bash
cd frontend
npm start
```

## Admin Interface

Django admin is configured to manage conversations:
- View all conversations
- Filter by archived status, date
- Search by title or ID
- Edit conversation metadata
- View and edit messages inline

Access at: `http://localhost:8000/admin/`

## Future Enhancements

### Planned Features
- [ ] Search conversations by content
- [ ] Export conversations to PDF/JSON
- [ ] Share conversations via link
- [ ] Conversation folders/categories
- [ ] Star/favorite important conversations
- [ ] Auto-categorize by issue type
- [ ] Conversation statistics dashboard
- [ ] Multi-user support with authentication

### Performance Optimizations
- [ ] Pagination for large conversation lists
- [ ] Lazy loading of message content
- [ ] Caching frequently accessed conversations
- [ ] Database indexing optimization

## Troubleshooting

### Common Issues

**Conversations not saving:**
- Check backend is running on port 8000
- Verify CORS settings in Django
- Check browser console for errors

**Sidebar not appearing:**
- Clear browser cache
- Check CSS is loading properly
- Verify ConversationHistory component is imported

**Database errors:**
- Run migrations: `python manage.py migrate`
- Check database file permissions
- Ensure ai_diagnostic app is in INSTALLED_APPS

## Security Considerations

### Current Implementation
- ⚠️ No authentication (for development)
- ⚠️ All conversations are public
- ⚠️ No user isolation

### For Production
- ✅ Add user authentication
- ✅ Associate conversations with users
- ✅ Implement permission checks
- ✅ Add CSRF protection
- ✅ Use HTTPS
- ✅ Sanitize user input

## Testing

### Manual Testing
1. Start a new conversation
2. Send multiple messages
3. Refresh the page
4. Verify conversation is still there
5. Load the conversation
6. Delete the conversation
7. Verify it's removed

### API Testing
Use tools like Postman or curl to test endpoints:
```bash
# List conversations
curl http://localhost:8000/api/conversations/

# Get specific conversation
curl http://localhost:8000/api/conversations/{id}/

# Delete conversation
curl -X DELETE http://localhost:8000/api/conversations/{id}/delete/
```

## File Structure

```
backend/
├── ai_diagnostic/
│   ├── models.py              # Database models
│   ├── serializers.py         # DRF serializers
│   ├── conversation_views.py  # API views
│   ├── admin.py               # Admin configuration
│   └── migrations/
│       └── 0001_initial.py    # Database migration
├── pc_diagnostic/
│   ├── settings.py            # Updated with ai_diagnostic app
│   └── urls.py                # Updated with conversation routes

frontend/
├── src/
│   └── components/
│       ├── ConversationHistory.js      # Sidebar component
│       ├── ConversationHistory.css     # Sidebar styles
│       ├── DiagnosticChat.js           # Updated main chat
│       └── DiagnosticChat.css          # Updated chat styles
```

## Summary

This implementation provides a complete conversation history management system that:
- ✅ Automatically saves all conversations
- ✅ Provides an intuitive sidebar interface
- ✅ Allows easy conversation management
- ✅ Stores comprehensive metadata
- ✅ Works seamlessly with the existing chat interface
- ✅ Is fully integrated with Django backend
- ✅ Ready for production with minor security additions

The system is inspired by ChatGPT's conversation management but tailored for the PC diagnostic use case with additional telemetry and diagnostic metadata.

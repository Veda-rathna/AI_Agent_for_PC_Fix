# AI-Driven PC Diagnostic Assistant

A full-stack application with Django backend and React frontend for AI-powered PC diagnostics.

## Project Structure

```
AI_Agent_for_PC_Fix/
├── backend/              # Django backend
│   ├── manage.py
│   ├── pc_diagnostic/    # Main Django project
│   └── ai_diagnostic/    # Django app with API endpoint
└── frontend/             # React frontend
    ├── src/
    ├── public/
    └── package.json
```

## Features

- **Django Backend**: REST API with Django REST Framework
- **React Frontend**: Interactive chat-style UI
- **CORS Enabled**: Configured for local development
- **API Endpoint**: `/api/diagnose/` accepts POST requests with a query
- **Chat Interface**: Modern, responsive UI with typing indicators

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

## Installation & Setup

### Backend Setup

1. Navigate to the backend directory:
   ```powershell
   cd backend
   ```

2. Install required Python packages (if not already installed):
   ```powershell
   pip install django djangorestframework django-cors-headers
   ```

3. Run migrations:
   ```powershell
   python manage.py migrate
   ```

4. Start the Django development server:
   ```powershell
   python manage.py runserver
   ```

   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```powershell
   cd frontend
   ```

2. Install dependencies (if not already installed):
   ```powershell
   npm install
   ```

3. Start the React development server:
   ```powershell
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

## Usage

1. **Start both servers**:
   - Terminal 1: Run `python manage.py runserver` in the `backend` directory
   - Terminal 2: Run `npm start` in the `frontend` directory

2. **Access the application**:
   - Open your browser and go to `http://localhost:3000`

3. **Test the diagnostic assistant**:
   - Type a PC issue in the chat input (e.g., "My computer is running slow")
   - Press Send or hit Enter
   - The AI assistant will respond with diagnostic suggestions

## API Endpoint

### POST /api/diagnose/

**Request Body:**
```json
{
  "query": "My computer is running slow",
  "timestamp": "2025-10-31T10:00:00.000Z"
}
```

**Response:**
```json
{
  "query": "My computer is running slow",
  "diagnosis": "After analyzing 'My computer is running slow', I suggest clearing your cache and temporary files.",
  "timestamp": "2025-10-31T10:00:00.000Z"
}
```

## Technology Stack

### Backend
- Django 4.2.7
- Django REST Framework 3.15.2
- django-cors-headers 4.8.0

### Frontend
- React 18
- Axios
- CSS3 with animations

## Configuration

### CORS Settings
The backend is configured to accept requests from `http://localhost:3000`. To modify this, edit `backend/pc_diagnostic/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

### API URL
The frontend makes requests to `http://localhost:8000/api/diagnose/`. To change this, edit `frontend/src/App.js`:

```javascript
const response = await axios.post('http://localhost:8000/api/diagnose/', {
  // ...
});
```

## Development

### Adding More Diagnostic Responses

Edit `backend/ai_diagnostic/views.py` to add more diagnostic messages:

```python
diagnostics = [
    f"Your custom diagnostic message for '{query}'",
    # Add more messages here
]
```

### Customizing the UI

Modify `frontend/src/App.css` to change colors, fonts, or layout.

## Troubleshooting

### Backend Issues

- **Module not found**: Make sure all packages are installed with `pip install django djangorestframework django-cors-headers`
- **Port already in use**: Change the port with `python manage.py runserver 8001`

### Frontend Issues

- **API connection error**: Ensure the Django server is running on port 8000
- **CORS error**: Check that `corsheaders` is installed and configured in `settings.py`
- **Port 3000 in use**: React will automatically suggest another port

## Next Steps

- Add user authentication
- Implement actual AI/ML diagnostic logic
- Add database models to store diagnostic history
- Deploy to production (Heroku, AWS, etc.)
- Add more sophisticated error handling
- Implement real-time updates with WebSockets

## License

MIT License

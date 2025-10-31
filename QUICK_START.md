# AI PC Diagnostic Assistant - Quick Start Guide

## Starting the Application

### Option 1: Manual Start (Recommended for first time)

1. **Start Django Backend**:
   Open PowerShell/Terminal and run:
   ```powershell
   cd d:\Code_wid_pablo\AI_Agent_for_PC_Fix\backend
   python manage.py runserver
   ```

2. **Start React Frontend**:
   Open a NEW PowerShell/Terminal window and run:
   ```powershell
   cd d:\Code_wid_pablo\AI_Agent_for_PC_Fix\frontend
   npm start
   ```

3. **Access the App**:
   Your browser should automatically open to `http://localhost:3000`
   If not, manually open your browser and navigate to that URL.

### Option 2: Using Windows Terminal (Both at Once)

If you have Windows Terminal installed, you can run both servers in split panes:

1. Open Windows Terminal
2. Split the pane (Alt+Shift+D or Alt+Shift+Plus)
3. In the first pane:
   ```powershell
   cd d:\Code_wid_pablo\AI_Agent_for_PC_Fix\backend; python manage.py runserver
   ```
4. In the second pane:
   ```powershell
   cd d:\Code_wid_pablo\AI_Agent_for_PC_Fix\frontend; npm start
   ```

## What You Should See

### Backend (Terminal 1):
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 31, 2025 - 10:00:00
Django version 4.2.7, using settings 'pc_diagnostic.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Frontend (Terminal 2):
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.

webpack compiled successfully
```

## Testing the Application

1. The React app will open in your browser
2. You should see a purple gradient background with a white chat container
3. Type a message like "My computer is slow" in the input box
4. Click Send
5. You should see:
   - Your message appear on the right (with 👤 icon)
   - A typing indicator (three bouncing dots)
   - An AI response on the left (with 🤖 icon)

## Troubleshooting

### "Port 8000 is already in use"
- Another Django server is running. Stop it with Ctrl+C or use a different port:
  ```powershell
  python manage.py runserver 8001
  ```
  Then update the API URL in `frontend/src/App.js` to `http://localhost:8001/api/diagnose/`

### "Port 3000 is already in use"
- React will ask if you want to use a different port. Type 'Y' to accept.
- Or manually specify a port:
  ```powershell
  $env:PORT=3001; npm start
  ```

### Backend starts but frontend shows connection error
- Make sure Django is running on port 8000
- Check the browser console (F12) for CORS errors
- Verify CORS is configured correctly in `backend/pc_diagnostic/settings.py`

### "Module not found" errors
- Backend: Run `pip install django djangorestframework django-cors-headers`
- Frontend: Run `npm install` in the frontend directory

## Stopping the Servers

- In each terminal window, press `Ctrl+C` to stop the server
- You may need to press it twice for Django

## Making Changes

### Backend Changes:
- Edit files in `backend/ai_diagnostic/views.py` to modify the API logic
- Django auto-reloads when you save files

### Frontend Changes:
- Edit files in `frontend/src/App.js` or `App.css`
- React will automatically refresh the browser when you save

## Default URLs

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Endpoint**: http://localhost:8000/api/diagnose/
- **Django Admin**: http://localhost:8000/admin/

Enjoy your AI PC Diagnostic Assistant! 🔧🤖

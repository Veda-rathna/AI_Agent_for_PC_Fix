# Timeout Configuration - Quick Reference

## Current Settings

### Frontend (React)
**File**: `frontend/src/components/DiagnosticChat.js`
```javascript
Timeout: 600 seconds (10 minutes)
Location: Line ~51
```

### Backend (Django)
**File**: `backend/pc_diagnostic/views.py`
```python
Timeout: 600 seconds (10 minutes)
Location: Line ~356
```

## What Changed

| Component | Old Timeout | New Timeout | Reason |
|-----------|-------------|-------------|--------|
| Frontend fetch | 120s (2 min) | 600s (10 min) | Reasoning models need time |
| Backend requests | 120s (2 min) | 600s (10 min) | Match frontend timeout |

## Loading Messages Timeline

| Time | Message |
|------|---------|
| 0-5s | Silent (fast response expected) |
| 5-30s | 🧠 Reasoning model is thinking... |
| 30-90s | 🔍 Deep analysis in progress... |
| 90-180s | ⏳ Still processing... |
| 180-600s | ⚠️ Taking longer than usual... |
| 600s+ | ❌ Timeout error |

## How to Adjust Timeouts

### To Increase Timeout Further

**Frontend** (`DiagnosticChat.js`):
```javascript
const timeoutId = setTimeout(() => controller.abort(), 900000); // 15 minutes
```

**Backend** (`views.py`):
```python
timeout=900  # 15 minutes
```

### To Decrease Timeout

**Frontend**:
```javascript
const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutes
```

**Backend**:
```python
timeout=300  # 5 minutes
```

## Testing

### Quick Test
1. Start backend: `cd backend && python manage.py runserver`
2. Start frontend: `cd frontend && npm start`
3. Ask a complex question: "Analyze all hardware issues"
4. Watch the progressive loading messages
5. Wait for response (should work even if takes 5+ minutes)

### Verify Timeout Works
1. Stop your model server
2. Ask any question
3. After 10 minutes, should see timeout error
4. Error message should explain what to do

## Troubleshooting

### Still Getting Timeouts?

**Check 1**: Is your model server responding?
```bash
# Check model server logs
# Look for actual response times
```

**Check 2**: Browser console errors?
```
F12 → Console tab
Look for network errors
```

**Check 3**: Backend logs?
```bash
# In backend terminal
# Look for timeout exceptions
```

### Model Takes Longer Than 10 Minutes?

**Option 1**: Increase timeout (see above)

**Option 2**: Optimize model
```
- Use smaller context window
- Reduce max_tokens
- Use faster model variant
```

**Option 3**: Add streaming
```javascript
// Future enhancement
// Stream responses as they generate
```

## Best Practices

### For Users
✅ Be patient with complex queries  
✅ Watch the status messages  
✅ Simplify queries if you want faster responses  

### For Developers
✅ Log actual response times  
✅ Monitor model performance  
✅ Consider implementing streaming  
✅ Cache common queries  

## Quick Commands

### Restart Everything
```powershell
# Terminal 1 - Backend
cd backend
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm start
```

### Check Logs
```powershell
# Backend logs - in backend terminal
# Frontend logs - F12 → Console

# Model server logs - check ngrok/model terminal
```

## Summary

✅ **Frontend timeout**: 600 seconds (10 minutes)  
✅ **Backend timeout**: 600 seconds (10 minutes)  
✅ **Progressive loading messages**: 4 stages  
✅ **Better error messages**: Actionable information  
✅ **No errors**: All files compile successfully  

**You're all set!** 🎉

The system will now wait up to 10 minutes for your reasoning model to respond, with helpful status updates along the way.

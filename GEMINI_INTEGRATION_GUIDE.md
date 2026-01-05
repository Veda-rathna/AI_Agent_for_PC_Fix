# Google Gemini Integration Guide

## 🎯 Overview

This document describes the Google Gemini integration in the AI-Driven PC Diagnostic Assistant. The integration uses Google's Gemini API (via Google AI Studio) as the primary Large Language Model for intelligent PC diagnostics.

## 🏗️ Architecture

### LLM Provider Pattern

The system implements a clean **Provider Pattern** for LLM abstraction:

```
backend/pc_diagnostic/llm/
├── __init__.py          # Module exports
├── base.py              # Abstract LLMProvider interface
├── gemini.py            # Google Gemini implementation
├── local_llama.py       # Local llama.cpp implementation
└── factory.py           # Provider factory & selection logic
```

### Fallback Chain

The system guarantees 100% uptime through a 3-tier fallback chain:

1. **Google Gemini** (Primary)
   - Cloud-based, state-of-the-art reasoning
   - Fast response with gemini-1.5-flash
   - Requires API key from Google AI Studio

2. **Local LLaMA** (Fallback #1)
   - Privacy-focused, runs locally
   - Uses llama.cpp server on localhost
   - No internet required

3. **Offline Mock Engine** (Fallback #2)
   - Rule-based analysis
   - Works without any LLM
   - Guaranteed to never fail

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- Google AI Studio account (free)
- Internet connection (for Gemini)

### Step 1: Get Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Step 2: Install Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

This installs:
- `google-generativeai>=0.3.0` - Gemini SDK
- `python-dotenv>=1.0.0` - Environment variable management
- All other existing dependencies

### Step 3: Configure Environment

1. Copy the example environment file:
   ```powershell
   cd backend
   cp .env.example .env
   ```

2. Edit `.env` and configure:
   ```env
   # Primary LLM Provider
   LLM_PROVIDER=gemini
   
   # Google Gemini Configuration
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   
   # Optional: Local LLaMA fallback
   LLAMA_API_BASE=http://127.0.0.1:1234
   LLAMA_MODEL_ID=your-model-name
   ```

3. **IMPORTANT**: Never commit the `.env` file to version control!

### Step 4: Verify Installation

Start the Django server:
```powershell
python manage.py runserver
```

Check the console output for:
```
🔧 Loading environment from: d:\...\backend\.env
✅ .env file found and loaded
🔍 LLM Provider requested: gemini
✅ Google Gemini provider initialized with model: gemini-1.5-flash
```

## 📋 Configuration Options

### LLM_PROVIDER

Controls which LLM provider to use:

| Value | Description | Requirements |
|-------|-------------|--------------|
| `gemini` | Google Gemini (recommended) | `GEMINI_API_KEY` |
| `local` or `llama` | Local llama.cpp server | llama.cpp running |

### GEMINI_MODEL

Choose the Gemini model variant:

| Model | Description | Use Case |
|-------|-------------|----------|
| `gemini-1.5-flash` | Fast, efficient (default) | Real-time diagnostics |
| `gemini-1.5-pro` | Advanced reasoning | Complex analysis |
| `gemini-pro` | Standard model | General use |

### Example Configurations

#### Production (Gemini Only)
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-1.5-flash
```

#### Development (Gemini + Local Fallback)
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-1.5-flash
LLAMA_API_BASE=http://127.0.0.1:1234
```

#### Offline Mode (Local Only)
```env
LLM_PROVIDER=local
LLAMA_API_BASE=http://127.0.0.1:1234
LLAMA_MODEL_ID=llama-3.1-reasoning
```

## 🔍 Verification

### Test API Response

Make a POST request to `/api/predict/`:

```json
{
  "input_text": "My computer is running slow",
  "generate_report": false
}
```

Expected response includes:
```json
{
  "success": true,
  "message": "...",
  "model": "gemini-1.5-flash",
  "ai_provider": "Google Gemini",
  "finish_reason": "stop"
}
```

### Check Logs

Django console will show:
```
🤖 Initializing LLM provider...
✅ Using Google Gemini for prediction
```

### Verify Fallback

1. Set invalid API key → Should fall back to Local LLaMA
2. Disable both → Should use Offline Mock Engine

## 🎓 How It Works

### 1. Request Flow

```
User Query + Telemetry
        ↓
    views.py (predict endpoint)
        ↓
    get_llm_provider() factory
        ↓
    GeminiProvider.complete(prompt)
        ↓
    Google Gemini API
        ↓
    Formatted Response
```

### 2. Provider Interface

All providers implement:
```python
class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str, temperature: float, max_tokens: int) -> Dict
    
    @abstractmethod
    def get_provider_name(self) -> str
```

### 3. Prompt Format

Gemini receives combined system + user prompt:
```
You are an AI PC Diagnostic Expert...

SYSTEM CONTEXT:
- Analyze telemetry
- Classify HARDWARE vs SOFTWARE
- Generate MCP tasks for software issues

USER PROBLEM:
My computer is running slow

SYSTEM TELEMETRY:
{
  "cpu": {"usage": 85.2},
  "memory": {"percentage": 92.1},
  ...
}
```

## 🛠️ Troubleshooting

### "Import google.generativeai could not be resolved"

**Solution**: Install dependencies:
```powershell
pip install google-generativeai>=0.3.0
```

### "GEMINI_API_KEY environment variable is not set"

**Solution**: 
1. Ensure `.env` file exists in `backend/` directory
2. Verify `GEMINI_API_KEY=your_key_here` is set
3. Restart Django server

### "Failed to initialize Gemini provider"

**Possible causes**:
- Invalid API key
- No internet connection
- API quota exceeded

**Solution**: Check logs for specific error, verify API key validity

### Gemini not being used despite configuration

**Debug steps**:
1. Check console for `LLM Provider requested: ...`
2. Verify `.env` file location: `backend/.env`
3. Ensure `python-dotenv` is installed
4. Check for typos in environment variable names

## 🎯 Submission Checklist

Before submitting to judges:

- [ ] `.env` file configured with valid Gemini API key
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server starts without errors
- [ ] Test API call returns `"ai_provider": "Google Gemini"`
- [ ] README.md includes Google Technology Integration section
- [ ] `.env.example` provided (without actual keys)
- [ ] `.env` added to `.gitignore`
- [ ] Fallback chain tested and working

## 📚 Additional Resources

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Project README](../README.md)
- [API Documentation](../README.md#-api-documentation)

## 🤝 Support

For integration issues:
1. Check troubleshooting section above
2. Verify environment configuration
3. Test with offline mock mode to isolate LLM issues
4. Check Django console for detailed error messages

---

**Last Updated**: January 2026  
**Gemini SDK Version**: 0.3.0+  
**Python Requirement**: 3.8+

# LLM Provider Fallback Order - Visual Flow

## Current Configuration (✅ WORKING)

```
┌─────────────────────────────────────────────────────────────┐
│                   API Request: /api/predict/                │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│              Step 1: Collect Telemetry Data                 │
│  • System info, CPU, Memory, Disk, Network, GPU             │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│        Step 2: Initialize LLM Provider (Factory)            │
└─────────────────────────────────────────────────────────────┘
                             ↓
                  ┌──────────────────┐
                  │ LLM_PROVIDER=?   │
                  └──────────────────┘
                             ↓
              ┌──────────────┴──────────────┐
              │                             │
         [gemini]                      [local]
              │                             │
              ↓                             ↓
    ┌─────────────────┐           ┌─────────────────┐
    │ Try: GEMINI API │           │ Try: Local      │
    │ gemini-2.5-flash│           │ LLaMA Server    │
    └─────────────────┘           └─────────────────┘
              │                             │
       ┌──────┴──────┐               ┌─────┴──────┐
       │             │               │            │
    Success       Failure         Success      Failure
       │             │               │            │
       ↓             └───────┬───────┘            │
    ┌─────────────────┐     │                    │
    │ ✅ Return       │     ↓                    │
    │ Gemini Result   │  ┌─────────────────┐    │
    └─────────────────┘  │ Try: Local      │    │
                         │ LLaMA Server    │    │
                         └─────────────────┘    │
                                  │              │
                           ┌──────┴──────┐       │
                           │             │       │
                        Success       Failure    │
                           │             │       │
                           ↓             └───────┘
                    ┌─────────────────┐          │
                    │ ✅ Return       │          │
                    │ LLaMA Result    │          │
                    └─────────────────┘          │
                                                 ↓
                                        ┌─────────────────┐
                                        │ ⚠️ Fallback:    │
                                        │ Offline Mock    │
                                        │ Diagnostic      │
                                        └─────────────────┘
                                                 ↓
                                        ┌─────────────────┐
                                        │ ✅ Return       │
                                        │ Offline Result  │
                                        └─────────────────┘
```

## The Bug That Was Fixed

### ❌ BEFORE (Broken Code Structure)

```python
def predict(request):
    # ... collect telemetry ...
    
    try:
        provider = get_llm_provider()  # ✅ This worked
        result = provider.complete()   # ✅ This worked
        prediction = result['content'] # ✅ This worked
        
        if not prediction:
            return Response({'error': 'No content'})
            
            # ❌ UNREACHABLE CODE - Everything below was indented wrong!
            response_data = {...}      # ❌ Never executed
            return Response(...)       # ❌ Never executed
            
    except Exception as e:
        # Because the good path never returned properly,
        # it always ended up here!
        return offline_mode()          # ❌ Always fell back to this
```

### ✅ AFTER (Fixed Code Structure)

```python
def predict(request):
    # ... collect telemetry ...
    
    try:
        provider = get_llm_provider()  # ✅ Works
        result = provider.complete()   # ✅ Works
        prediction = result['content'] # ✅ Works
        
        if not prediction:
            return Response({'error': 'No content'})
        
        # ✅ REACHABLE CODE - Proper indentation!
        response_data = {...}          # ✅ Executes correctly
        return Response(response_data) # ✅ Returns Gemini result
            
    except Exception as e:
        # Only falls back when there's an actual error
        return offline_mode()          # ✅ Only when needed
```

## Priority Order Summary

```
┌────────────────────────────────────────────────────────┐
│ 1️⃣  GEMINI API (Primary)                              │
├────────────────────────────────────────────────────────┤
│ Provider:  Google AI Studio                           │
│ Model:     gemini-2.5-flash                           │
│ Speed:     Fast (Cloud API)                           │
│ Quality:   ⭐⭐⭐⭐⭐ (Highest)                            │
│ Cost:      Free tier available                        │
│ Status:    ✅ NOW WORKING CORRECTLY                    │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ 2️⃣  LOCAL LLAMA (Fallback)                            │
├────────────────────────────────────────────────────────┤
│ Provider:  Local llama.cpp server                     │
│ Model:     reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1 │
│ Speed:     Medium-Fast (Local inference)              │
│ Quality:   ⭐⭐⭐⭐ (High)                                │
│ Cost:      Free (requires local setup)                │
│ Status:    ✅ Available when server running            │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ 3️⃣  OFFLINE DIAGNOSTIC (Last Resort)                  │
├────────────────────────────────────────────────────────┤
│ Provider:  Pattern matching engine                    │
│ Model:     Rule-based system                          │
│ Speed:     Very Fast (No LLM)                         │
│ Quality:   ⭐⭐ (Basic)                                 │
│ Cost:      Free (always available)                    │
│ Status:    ✅ Always available                         │
└────────────────────────────────────────────────────────┘
```

## Environment Variables

```properties
# Primary LLM Selection
LLM_PROVIDER=gemini                    # ← Use Gemini first

# Gemini Configuration
GEMINI_API_KEY=AIzaSy...              # ← Your API key
GEMINI_MODEL=gemini-2.5-flash         # ← Fast model

# Local LLaMA Fallback Configuration
LLAMA_API_BASE=http://127.0.0.1:1234  # ← Local server
LLAMA_MODEL_ID=reasoning-llama-3.1... # ← Model name
```

## Response Indicators

### When Using Gemini (✅ Working Now!)

```json
{
  "success": true,
  "ai_provider": "Google Gemini",
  "model": "gemini-2.5-flash",
  "prediction": "... detailed AI analysis ...",
  "finish_reason": "stop"
}
```

### When Fallback to Local LLaMA

```json
{
  "success": true,
  "ai_provider": "Local LLaMA",
  "model": "reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1",
  "prediction": "... detailed AI analysis ...",
  "finish_reason": "stop"
}
```

### When Fallback to Offline Mode

```json
{
  "success": true,
  "ai_provider": "Offline Mock Engine",
  "model": "Offline Diagnostic Engine",
  "prediction": "... basic pattern matching analysis ...\n\n*Note: The AI diagnostic service is currently unavailable*",
  "finish_reason": "offline_mode"
}
```

## Testing Commands

```bash
# 1. Test environment variables
cd backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Provider:', os.getenv('LLM_PROVIDER'))"

# 2. Test Gemini integration
python test_gemini_integration.py

# 3. Test fallback order
python test_fallback_order.py

# 4. Start the server
python manage.py runserver

# 5. Test the API endpoint
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"input_text": "My computer is running slow"}'
```

## Logs to Watch

### ✅ Success Pattern (Using Gemini)
```
🤖 Initializing LLM provider...
🔍 LLM Provider requested: gemini
✅ Google Gemini provider initialized with model: gemini-2.5-flash
✅ Using Google Gemini for prediction
```

### ⚠️ Fallback Pattern (Gemini → LLaMA)
```
🤖 Initializing LLM provider...
🔍 LLM Provider requested: gemini
⚠️ Failed to initialize Gemini provider: [error]
🔄 Falling back to Local LLaMA provider...
✅ Local LLaMA provider initialized
```

### ⚠️ Complete Fallback (Gemini → LLaMA → Offline)
```
🤖 Initializing LLM provider...
🔍 LLM Provider requested: gemini
⚠️ Failed to initialize Gemini provider: [error]
🔄 Falling back to Local LLaMA provider...
❌ Failed to initialize Local LLaMA provider: [error]
⚠️ LLM Provider Error: [error]
🔄 Falling back to offline diagnostic mode...
```

## Summary

**Problem:** Indentation bug caused Gemini responses to never return properly
**Solution:** Fixed indentation in views.py (lines 365-507)
**Result:** ✅ Gemini API now works as the primary LLM provider
**Fallback:** ✅ Proper 3-tier fallback chain implemented
**Status:** ✅ VERIFIED AND WORKING

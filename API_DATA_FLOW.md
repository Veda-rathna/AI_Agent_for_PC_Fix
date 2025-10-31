# API Data Flow Documentation

## Backend → Frontend Data Structure

### Endpoint: `POST /api/predict/`

#### Request Format
```json
{
  "input_text": "my pc screen is flickering",
  "telemetry_data": {  // Optional
    "system_info": {...},
    "cpu_usage": {...},
    ...
  }
}
```

#### Success Response Format
```json
{
  "success": true,
  "message": "**Analysis**\n\nBased on the provided telemetry data...",
  "prediction": "**Analysis**\n\nBased on the provided telemetry data...",
  "model": "reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1",
  "finish_reason": "stop",
  "usage": {
    "prompt_tokens": 1524,
    "completion_tokens": 651,
    "total_tokens": 2175
  },
  "metadata": {
    "id": "chatcmpl-sk5apr4xdl4d5hr0dntt",
    "created": 1761891683,
    "object": "chat.completion",
    "system_fingerprint": "reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1"
  },
  "processing_time": 1761891683
}
```

### Key Fields Explained

| Field | Type | Description | Frontend Usage |
|-------|------|-------------|----------------|
| `success` | boolean | Request success status | Check before displaying data |
| `message` | string | **PRIMARY FIELD** - The AI's full diagnostic response | **Display this to the user** |
| `prediction` | string | Duplicate of `message` (backward compatibility) | Fallback if `message` is not available |
| `model` | string | Name of the AI model used | Show in UI metadata |
| `finish_reason` | string | Why the model stopped (`stop`, `length`, etc.) | Optional UI indicator |
| `usage.total_tokens` | integer | Total tokens used | Display cost/usage metrics |
| `metadata.id` | string | Unique response ID | Logging/tracking |
| `metadata.created` | integer | Unix timestamp | Convert to readable time |

---

## Frontend Display Strategy

### 1. **Display the Message**
The main content to show users is in the `message` field:

```javascript
const aiResponse = data.message || data.prediction;
```

### 2. **Handle Markdown Formatting**
The model returns markdown-style text. You should:
- Convert `**text**` → Bold
- Convert `### Header` → H3 headings
- Convert `*   item` → Bullet lists
- Preserve line breaks

**Recommended Libraries:**
- `react-markdown` - Full markdown rendering
- `marked` - Convert markdown to HTML
- Custom parser (like in the example component)

### 3. **Show Loading State**
Since the model takes 30-120 seconds to process:

```javascript
{isLoading && (
  <div className="loading">
    <span>Analyzing your issue...</span>
    <span>This may take up to 2 minutes</span>
  </div>
)}
```

### 4. **Display Token Usage (Optional)**
Show transparency about AI processing:

```javascript
<div className="usage-info">
  Tokens used: {data.usage.total_tokens}
  ({data.usage.prompt_tokens} in + {data.usage.completion_tokens} out)
</div>
```

---

## Error Response Format

```json
{
  "success": false,
  "error": "Error description",
  "details": "Additional error information"
}
```

### Common Errors

| Status Code | Error | Meaning |
|-------------|-------|---------|
| 400 | "No input provided" | Missing `input_text` in request |
| 500 | "Model API error: 500" | LLM server error |
| 503 | "Could not connect to local model server" | LLM server offline |
| 504 | "Request to model timed out" | Processing took >120 seconds |

---

## Example Frontend Usage

### Basic Fetch Request
```javascript
const response = await fetch('http://localhost:8000/api/predict/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    input_text: userInput
  })
});

const data = await response.json();

if (data.success) {
  // Display the AI's message
  displayMessage(data.message);
} else {
  // Show error
  showError(data.error);
}
```

### With Loading State
```javascript
const [isLoading, setIsLoading] = useState(false);
const [aiMessage, setAiMessage] = useState('');

const getAIResponse = async (userInput) => {
  setIsLoading(true);
  
  try {
    const response = await fetch('http://localhost:8000/api/predict/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input_text: userInput })
    });

    const data = await response.json();
    
    if (data.success) {
      setAiMessage(data.message);
    } else {
      console.error(data.error);
    }
  } catch (error) {
    console.error('Network error:', error);
  } finally {
    setIsLoading(false);
  }
};
```

---

## Sample Model Output Structure

The model generates responses in this format:

```
**Analysis**

Based on the provided telemetry data, we can start by analyzing...

**Root Cause**

Upon closer inspection of the telemetry data, we notice...

**Solutions**

### 1. Update Graphics Card Drivers

Update the NVIDIA GeForce RTX 2050 drivers...

### 2. Disable Power-Saving Features

*   **Power saver mode**: Ensure this feature is turned off.
*   **Screen brightness adjustment**: Check if automatic...

**Recommendations**

1.  **Regularly Update Drivers**: Ensure that all drivers...
```

### Key Formatting Patterns:
- `**Text**` = Bold section headers
- `### Number. Title` = Numbered solutions
- `*   Item` = Bullet points
- Blank lines = Paragraph breaks

---

## Integration Checklist

- [ ] Backend is running on `http://localhost:8000`
- [ ] Frontend can reach `http://localhost:8000/api/predict/`
- [ ] CORS is enabled for frontend origin
- [ ] Loading state shows while waiting for response (30-120 sec)
- [ ] Error handling for network/server errors
- [ ] Markdown rendering for the AI message
- [ ] Optional: Token usage display
- [ ] Optional: Timestamp display

---

## Performance Notes

⏱️ **Expected Response Time**: 30-120 seconds
📊 **Typical Token Usage**: 1500-3000 tokens
🔄 **Timeout Setting**: 120 seconds (already configured in backend)

The reasoning model takes significant time because it:
1. Analyzes the problem deeply
2. Generates comprehensive diagnostics
3. Provides multiple solution paths
4. Includes technical analysis

**Recommendation**: Always show a clear loading indicator with estimated time.

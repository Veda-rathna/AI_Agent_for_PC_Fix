# Tool Use Quick Reference

## Quick Start

### 1. Test Individual Tools

```python
# In Django shell or test script
from pc_diagnostic.diagnostic_tools import *

# Check disk health
print(check_disk_health())

# Scan event logs
print(scan_event_logs(log_type='System', hours_back=24))

# Check drivers
print(verify_driver_integrity(device_type='display'))

# Check GPU
print(check_gpu_status())

# Test memory
print(test_memory())

# Check network
print(check_network_connectivity())
```

### 2. Test via API

```bash
# Send diagnostic request
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "My screen is flickering",
    "generate_report": false
  }'
```

### 3. Expected Tool Use Flow

```
User Problem → LLM Analyzes → Decides Tools Needed
                                     ↓
                              Tool Execution
                                     ↓
                              Results to LLM
                                     ↓
                           Final Diagnosis with Evidence
```

## Available Tools Quick List

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `check_disk_health` | SMART diagnostics | `drive_letter` (optional) |
| `scan_event_logs` | Windows Event Viewer | `log_type`, `hours_back`, `keywords` |
| `verify_driver_integrity` | Driver validation | `device_type` (display/network/audio/storage/all) |
| `check_gpu_status` | GPU diagnostics | None |
| `test_memory` | RAM analysis | None |
| `check_network_connectivity` | Network testing | `target` (optional) |

## Common Issues and Solutions

### Issue: Tool not being called
**Solution:** Improve tool description or make problem description more specific

### Issue: Tool execution fails
**Solution:** Check if running on Windows, verify PowerShell access

### Issue: Timeout errors
**Solution:** Increase timeout in tool function or API call

## Response Structure

### With Tools Used:
```json
{
  "success": true,
  "message": "AI diagnosis...",
  "finish_reason": "tool_calls_completed",
  "tools_used": ["check_disk_health", "scan_event_logs"],
  "tool_results": [...]
}
```

### Without Tools:
```json
{
  "success": true,
  "message": "AI diagnosis...",
  "finish_reason": "stop"
}
```

## Model Requirements

- **Recommended:** reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1
- **Minimum:** 7B parameter model with tool use support
- **API:** OpenAI-compatible with tool calling support

## Example Scenarios

### Scenario 1: Display Issues
**User:** "My screen is black"
**AI Calls:**
1. `check_gpu_status()` 
2. `verify_driver_integrity(device_type='display')`
3. `scan_event_logs(log_type='System', keywords=['display', 'GPU'])`

### Scenario 2: Slow Performance
**User:** "Computer is very slow"
**AI Calls:**
1. `check_disk_health()`
2. `test_memory()`
3. `scan_event_logs(log_type='System', hours_back=48)`

### Scenario 3: Network Problems
**User:** "Can't connect to internet"
**AI Calls:**
1. `check_network_connectivity()`
2. `verify_driver_integrity(device_type='network')`

## Testing Checklist

- [ ] All 6 tools execute without errors
- [ ] LLM successfully calls tools when appropriate
- [ ] Tool results are properly formatted in response
- [ ] Reports include tool execution data
- [ ] Graceful fallback when LLM server is offline
- [ ] Error handling for tool execution failures

## File Locations

```
backend/pc_diagnostic/
├── diagnostic_tools.py          # Tool implementations
├── views.py                     # API with tool use
└── ...

Documentation:
├── TOOL_USE_INTEGRATION.md      # Full documentation
└── TOOL_USE_QUICK_REFERENCE.md  # This file
```

## Next Steps

1. ✅ Test each tool individually
2. ✅ Verify LLM server supports tool calling
3. ✅ Test end-to-end with real user problems
4. ✅ Monitor tool execution logs
5. ✅ Add more tools as needed

---

For detailed documentation, see [TOOL_USE_INTEGRATION.md](TOOL_USE_INTEGRATION.md)

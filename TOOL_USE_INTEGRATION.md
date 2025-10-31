# Tool Use Integration Documentation

## Overview

This document describes the **Tool Use** feature integration in the AI PC Diagnostic system. Tool use enables the AI model to directly call diagnostic functions instead of just suggesting manual checks.

## What is Tool Use?

Tool use is a capability where:
1. **LLMs output text requesting functions to be called** (LLMs cannot directly execute code)
2. **Your code executes those functions**
3. **Your code feeds the results back to the LLM**

This transforms the AI from a passive advisor into an active diagnostic agent.

## Architecture

```
┌──────────────────────────┐
│  User Problem Input      │
└──────────┬───────────────┘
           ▼
┌──────────────────────────┐
│  Collect Telemetry Data  │
└──────────┬───────────────┘
           ▼
┌──────────────────────────┐
│  LLM + Tool Definitions  │
└──────────┬───────────────┘
           ▼
     Needs tools?
      │         │
    Yes         No
      │         │
      ▼         └────────────┐
┌─────────────┐              │
│Execute Tools│              │
└──────┬──────┘              │
       ▼                     │
┌─────────────┐              │
│Add results  │              │
│to messages  │              │
└──────┬──────┘              │
       │                     ▼
       │              ┌───────────┐
       │              │  Normal   │
       │              │ response  │
       │              └─────┬─────┘
       │                    │
       └────────────────────┘
                ▼
        ┌──────────────┐
        │Final Response│
        └──────────────┘
```

## Available Diagnostic Tools

### 1. check_disk_health
**Purpose:** Run SMART diagnostics on drives
**Use Case:** Slow performance, file access issues, disk-related problems
**Parameters:**
- `drive_letter` (optional): Specific drive to check (e.g., 'C')

**Returns:**
```json
{
  "success": true,
  "drives": [
    {
      "device": "C:\\",
      "total_gb": 500,
      "used_gb": 250,
      "free_gb": 250,
      "percent_used": 50,
      "status": "healthy",
      "wmic_status": "OK"
    }
  ],
  "summary": {
    "total_drives": 1,
    "healthy_drives": 1,
    "warning_drives": 0
  }
}
```

### 2. scan_event_logs
**Purpose:** Search Windows Event Viewer for errors
**Use Case:** BSODs, driver issues, hardware failures, system crashes
**Parameters:**
- `log_type` (required): 'System', 'Application', or 'Hardware Events'
- `hours_back` (optional): Number of hours to search (default: 24)
- `keywords` (optional): Array of keywords to filter (e.g., ['GPU', 'driver', 'crash'])

**Returns:**
```json
{
  "success": true,
  "events": [
    {
      "TimeCreated": "2025-10-31T10:30:00",
      "Id": 41,
      "LevelDisplayName": "Error",
      "Message": "The system has rebooted without cleanly shutting down first...",
      "ProviderName": "Microsoft-Windows-Kernel-Power"
    }
  ],
  "summary": {
    "critical_errors": 0,
    "errors": 1,
    "warnings": 2
  }
}
```

### 3. verify_driver_integrity
**Purpose:** Check if system drivers are properly signed and up-to-date
**Use Case:** Hardware malfunctions, display issues, network problems, audio issues
**Parameters:**
- `device_type` (required): 'display', 'network', 'audio', 'storage', or 'all'

**Returns:**
```json
{
  "success": true,
  "drivers": [
    {
      "device_name": "NVIDIA GeForce RTX 3060",
      "driver_version": "531.41",
      "is_signed": true,
      "manufacturer": "NVIDIA",
      "device_class": "Display",
      "status": "OK",
      "driver_age_days": 45
    }
  ],
  "summary": {
    "total_drivers": 1,
    "signed_drivers": 1,
    "unsigned_drivers": 0,
    "outdated_drivers": 0
  }
}
```

### 4. check_gpu_status
**Purpose:** Check GPU status including drivers and functionality
**Use Case:** Screen issues, display problems, graphics errors, gaming performance issues

**Returns:**
```json
{
  "success": true,
  "gpus": [
    {
      "name": "NVIDIA GeForce RTX 3060",
      "driver_version": "531.41",
      "status": "OK"
    }
  ],
  "summary": {
    "total_gpus": 1,
    "healthy_gpus": 1
  }
}
```

### 5. test_memory
**Purpose:** Check RAM usage, memory pressure, and swap usage
**Use Case:** Crashes, freezes, slow performance, out-of-memory errors

**Returns:**
```json
{
  "success": true,
  "memory_info": {
    "total_gb": 16,
    "available_gb": 8,
    "used_gb": 8,
    "percent_used": 50,
    "status": "healthy",
    "swap_total_gb": 20,
    "swap_used_gb": 2,
    "swap_percent": 10
  }
}
```

### 6. check_network_connectivity
**Purpose:** Test network connectivity and diagnose network issues
**Use Case:** Internet connection issues, network slowness, connectivity problems
**Parameters:**
- `target` (optional): IP address or hostname to ping (default: 8.8.8.8)

**Returns:**
```json
{
  "success": true,
  "target": "8.8.8.8",
  "connectivity": {
    "ping_success": true,
    "status": "Connected",
    "avg_latency_ms": 15.2
  },
  "interfaces": [
    {
      "name": "Ethernet",
      "is_up": true,
      "speed_mbps": 1000
    }
  ]
}
```

## Implementation Details

### Backend (Django/Python)

**File Structure:**
```
backend/pc_diagnostic/
├── diagnostic_tools.py     # Tool implementations
├── views.py                # API endpoints with tool use
└── ...
```

**Key Changes in `views.py`:**

1. **Import diagnostic tools:**
```python
from .diagnostic_tools import (
    check_disk_health,
    scan_event_logs,
    verify_driver_integrity,
    check_gpu_status,
    test_memory,
    check_network_connectivity
)
```

2. **Define tool schemas:**
```python
DIAGNOSTIC_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_disk_health",
            "description": "Run SMART diagnostics...",
            "parameters": {...}
        }
    },
    # ... other tools
]
```

3. **Send tools to LLM:**
```python
response = requests.post(
    f"{LLM_API_BASE}/v1/chat/completions",
    json={
        "model": LLM_MODEL_ID,
        "messages": messages,
        "tools": DIAGNOSTIC_TOOLS,  # ← Include tools
        "temperature": 0.7,
        "max_tokens": 3000
    },
    timeout=600
)
```

4. **Handle tool calls:**
```python
if finish_reason == 'tool_calls':
    tool_calls = choice['message']['tool_calls']
    
    # Execute each tool
    for tool_call in tool_calls:
        function_name = tool_call['function']['name']
        arguments = json.loads(tool_call['function']['arguments'])
        
        if function_name == 'check_disk_health':
            result_data = check_disk_health(**arguments)
        # ... execute other tools
        
        # Add result to messages
        tool_results.append({
            "role": "tool",
            "content": json.dumps(result_data),
            "tool_call_id": tool_call['id']
        })
    
    # Get final response with tool results
    final_response = requests.post(...)
```

## API Response Format

### Regular Response (No Tools)
```json
{
  "success": true,
  "message": "Based on the telemetry data...",
  "model": "reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1",
  "finish_reason": "stop",
  "session_id": "uuid",
  "telemetry_collected": true,
  "usage": {...},
  "metadata": {...}
}
```

### Response with Tool Use
```json
{
  "success": true,
  "message": "I've checked your disk health and event logs...",
  "model": "reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1",
  "finish_reason": "tool_calls_completed",
  "session_id": "uuid",
  "tools_used": ["check_disk_health", "scan_event_logs"],
  "tool_results": [
    {
      "name": "check_disk_health",
      "arguments": {},
      "result": {...}
    },
    {
      "name": "scan_event_logs",
      "arguments": {"log_type": "System", "hours_back": 24},
      "result": {...}
    }
  ],
  "telemetry_collected": true,
  "usage": {...},
  "metadata": {...}
}
```

## Benefits

### Before Tool Use:
- ❌ AI suggests: "Check Event Viewer for errors"
- ❌ User must manually open Event Viewer
- ❌ User may not know what to look for
- ❌ No automated correlation with other data

### With Tool Use:
- ✅ AI executes: `scan_event_logs(log_type='System', keywords=['GPU', 'driver'])`
- ✅ AI receives actual error logs
- ✅ AI analyzes real data and provides specific guidance
- ✅ Automated multi-step diagnostics
- ✅ Evidence-based recommendations

## Example Workflow

**User Problem:** "My screen keeps flickering and sometimes goes black"

**AI Workflow:**
1. Analyzes telemetry data
2. Calls `check_gpu_status()` → Detects GPU is present
3. Calls `verify_driver_integrity(device_type='display')` → Finds driver is outdated
4. Calls `scan_event_logs(log_type='System', keywords=['display', 'driver', 'GPU'])` → Finds driver crash events
5. Provides diagnosis: "Your NVIDIA GPU driver is 200 days old and has crashed 3 times in the last 24 hours"
6. Gives solution: "Update your GPU driver to the latest version from NVIDIA's website"

## Testing

### Test Tool Execution Directly
```python
from pc_diagnostic.diagnostic_tools import check_disk_health, scan_event_logs

# Test disk health
result = check_disk_health()
print(result)

# Test event logs
result = scan_event_logs(log_type='System', hours_back=24, keywords=['error', 'critical'])
print(result)
```

### Test via API
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "My computer is running very slow",
    "generate_report": false
  }'
```

## Security Considerations

1. **Tool Whitelisting:** Only predefined tools can be executed
2. **Parameter Validation:** Tool parameters are validated before execution
3. **Timeout Protection:** All tools have execution timeouts
4. **Error Handling:** Failed tools don't crash the system
5. **Windows-Only:** Some tools only work on Windows (gracefully degrade on other platforms)

## Future Enhancements

1. **More Tools:**
   - `check_thermal_status()` - Monitor CPU/GPU temperatures
   - `analyze_startup_programs()` - Check for resource-heavy startup apps
   - `test_usb_ports()` - Verify USB device detection
   - `check_bios_settings()` - Validate BIOS configuration

2. **Tool Chaining:**
   - AI can call multiple tools in sequence
   - Results from one tool inform the next

3. **User Confirmation:**
   - Optional user approval before executing certain tools
   - Display tool execution in real-time to user

4. **Tool Results Caching:**
   - Cache tool results for a session
   - Avoid redundant diagnostics

## Troubleshooting

### Tool Not Executing
- Check if `diagnostic_tools.py` is imported correctly
- Verify tool name matches exactly in DIAGNOSTIC_TOOLS
- Check function signature matches parameters

### Tool Execution Timeout
- Increase timeout in tool function
- Check if Windows commands are hanging
- Verify PowerShell is available

### Model Not Calling Tools
- Ensure model supports tool use (reasoning models work best)
- Check if tools array is included in API request
- Verify tool descriptions are clear and relevant

## Resources

- [LM Studio Tool Use Documentation](https://lmstudio.ai/docs/advanced/tool-use)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Backend Implementation](backend/pc_diagnostic/)

---

**Version:** 1.0  
**Last Updated:** October 31, 2025  
**Branch:** feature/tool-use-integration

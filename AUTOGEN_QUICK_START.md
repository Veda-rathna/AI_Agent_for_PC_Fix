# AutoGen Integration - Quick Start Guide

## 🚀 Quick Start in 5 Minutes

### Step 1: Install Dependencies (1 min)

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- `pyautogen` - AutoGen framework
- `openai` - OpenAI API (optional, for agent mode)
- `autogen-agentchat` - AutoGen chat capabilities

### Step 2: Start the Backend (30 sec)

```bash
cd backend
python manage.py runserver
```

The AutoGen integration is now active! ✅

### Step 3: Test the Integration (2 min)

#### Option A: Using curl

```bash
# Test status
curl http://localhost:8000/api/mcp/status/

# Execute MCP tasks
curl -X POST http://localhost:8000/api/mcp/execute/ \
  -H "Content-Type: application/json" \
  -d '{
    "model_output": "Your computer is slow.\n\n<MCP_TASKS>\n{\n  \"tasks\": [\n    \"Analyze CPU thermal sensor readings\",\n    \"Check memory usage\"\n  ],\n  \"summary\": \"Check performance\"\n}\n</MCP_TASKS>"
  }'
```

#### Option B: Using Python

```python
import requests

response = requests.post('http://localhost:8000/api/mcp/execute/', json={
    "model_output": """
    Your system seems slow.
    
    <MCP_TASKS>
    {
      "tasks": [
        "Analyze CPU thermal sensor readings",
        "Inspect disk usage telemetry",
        "Check memory usage"
      ],
      "summary": "Performance diagnostics"
    }
    </MCP_TASKS>
    """
})

print(response.json())
```

#### Option C: Integrated with AI Prediction

```bash
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "My computer is running slow",
    "execute_mcp_tasks": true
  }'
```

### Step 4: View Results (1 min)

The response will include:

```json
{
  "success": true,
  "tasks_completed": 3,
  "results": [
    {
      "task": "CPU Thermal Analysis",
      "success": true,
      "analysis": "✅ CPU temperature normal",
      "data": {
        "cpu_usage_average": 25.5,
        "max_temperature_celsius": 45.2
      }
    }
  ],
  "execution_summary": "Formatted summary of all tasks..."
}
```

## 🎯 Common Use Cases

### Use Case 1: Automatic Diagnostics on Every Prediction

```javascript
// Frontend code
const diagnoseProblem = async (userInput) => {
  const response = await fetch('/api/predict/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      input_text: userInput,
      execute_mcp_tasks: true  // Auto-execute diagnostics
    })
  });
  
  const data = await response.json();
  
  // Show AI message to user
  console.log(data.message);
  
  // Show diagnostic results
  if (data.mcp_execution?.executed) {
    console.log(`Ran ${data.mcp_execution.tasks_completed} diagnostic checks`);
    data.mcp_execution.results.forEach(result => {
      console.log(`${result.task}: ${result.analysis}`);
    });
  }
};
```

### Use Case 2: Parse Tasks First, Execute Later

```python
# Parse tasks without executing
parse_response = requests.post('http://localhost:8000/api/mcp/parse/', json={
    "model_output": ai_model_output
})

tasks = parse_response.json()
print(f"Found {tasks['task_count']} tasks")

# User reviews and approves...

# Execute approved tasks
execute_response = requests.post('http://localhost:8000/api/mcp/execute/', json={
    "model_output": ai_model_output,
    "execution_mode": "direct"
})
```

### Use Case 3: Check Orchestrator Status

```python
status = requests.get('http://localhost:8000/api/mcp/status/').json()

if status['orchestrator_available']:
    print("Orchestrator is ready!")
    print(f"Available tools: {', '.join(status['available_tools'])}")
else:
    print("Orchestrator not available")
```

## 📊 Understanding Results

### Task Result Structure

```json
{
  "success": true,
  "task": "CPU Thermal Analysis",
  "data": {
    "cpu_usage_average": 35.2,
    "cpu_frequency_mhz": {
      "current": 2400,
      "max": 3600
    },
    "max_temperature_celsius": 65.5
  },
  "analysis": "⚡ Elevated temperature - Monitor for thermal throttling",
  "severity": "medium"
}
```

### Severity Levels

- `low` ✅ - Everything normal
- `medium` ⚡ - Warning, monitor situation
- `high` ⚠️ - Critical issue, needs attention

### Task Categories

Tasks are auto-categorized:
- **thermal**: CPU temperature/cooling
- **disk**: Storage and disk I/O
- **memory**: RAM usage
- **power**: Power management
- **event_log**: Windows Event Logs
- **system_files**: SFC/DISM integrity
- **network**: Network connectivity
- **gpu**: Graphics/display

## 🔧 Configuration (Optional)

### Set Execution Mode

Edit `backend/autogen_integration/config/agents_config.json`:

```json
{
  "execution_mode": "semi-automated"
}
```

Modes:
- `fully_automated` - Execute everything
- `semi_automated` - Pause for admin tasks (default)
- `interactive` - User approves each task

### Configure Logging

```json
{
  "logging": {
    "level": "INFO",
    "console": true
  }
}
```

Levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

## ❗ Troubleshooting

### Problem: "AutoGen orchestrator not available"

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Restart server
python manage.py runserver
```

### Problem: "No MCP_TASKS found"

**Solution:**
- Ensure AI model output includes proper `<MCP_TASKS>` XML tags
- Verify JSON is valid inside tags
- Use `/api/mcp/parse/` to test extraction

### Problem: SFC/DISM tasks fail

**Solution:**
- These require Administrator privileges
- Run backend as admin, or
- User performs these manually per AI instructions

### Problem: Tasks execute slowly

**Solution:**
- Use `"execution_mode": "direct"` (default, faster)
- Avoid `"autogen"` mode unless needed (requires LLM calls)

## 📈 Performance Tips

1. **Use Direct Mode**: Fastest, no LLM required
2. **Filter Tasks**: Only execute relevant tasks
3. **Parallel Execution**: Safe tasks run in parallel
4. **Cache Results**: Store diagnostic results for similar issues

## 🎓 Next Steps

1. ✅ **Read Full Documentation**: `backend/autogen_integration/README.md`
2. ✅ **Customize Tools**: Add your own diagnostic tools
3. ✅ **Frontend Integration**: Connect to your UI
4. ✅ **Monitor Logs**: Check `backend/autogen_integration/logs/`

## 📝 Example: Complete Workflow

```python
import requests

# Step 1: User reports issue
user_input = "My computer keeps crashing"

# Step 2: Get AI diagnosis with MCP tasks
response = requests.post('http://localhost:8000/api/predict/', json={
    "input_text": user_input,
    "execute_mcp_tasks": True,
    "generate_report": True
})

result = response.json()

# Step 3: Show user-friendly message
print("AI Says:", result['message'])

# Step 4: Show diagnostic results
if result.get('mcp_execution', {}).get('executed'):
    mcp = result['mcp_execution']
    print(f"\n✅ Ran {mcp['tasks_completed']} diagnostic checks")
    
    for task_result in mcp['results']:
        print(f"\n{task_result['task']}")
        print(f"  Status: {task_result.get('analysis', 'Done')}")
        if task_result.get('recommendation'):
            print(f"  Recommendation: {task_result['recommendation']}")

# Step 5: Download detailed report
if result.get('reports'):
    report_url = result['reports']['json']['download_url']
    print(f"\n📄 Detailed report: {report_url}")
```

## 🆘 Need Help?

- Check logs: `backend/autogen_integration/logs/autogen_execution.log`
- Review full README: `backend/autogen_integration/README.md`
- Test individual tools in `tools/` directory

---

**You're all set! 🎉**

The AutoGen integration is running and ready to execute MCP tasks automatically.

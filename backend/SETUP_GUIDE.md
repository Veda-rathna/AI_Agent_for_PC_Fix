# Quick Setup Guide for Backend Integration

## Installation Steps

### 1. Navigate to Backend Directory
```bash
cd d:\Code_wid_pablo\AI_Agent_for_PC_Fix\backend
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Install Advanced Telemetry Dependencies
For HWiNFO-level hardware monitoring:
```bash
pip install pythonnet nvidia-ml-py3
```

### 4. Download LibreHardwareMonitor (Optional)
If you installed advanced telemetry:
1. Download LibreHardwareMonitor from: https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases
2. Extract the archive
3. Copy `LibreHardwareMonitorLib.dll` to one of these locations:
   - `C:\Program Files\LibreHardwareMonitor\`
   - `C:\LibreHardwareMonitor\`
   - `d:\Code_wid_pablo\AI_Agent_for_PC_Fix\backend\`

### 5. Run Django Migrations
```bash
python manage.py migrate
```

### 6. Start the Server
```bash
python manage.py runserver
```

The backend will be available at: `http://localhost:8000/`

## API Testing

### Test Telemetry Collection
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/telemetry/?issue=slow%20performance" -Method GET
```

### Test AI Diagnosis with Telemetry
```powershell
$body = @{
    input_text = "My computer is running very slow"
    generate_report = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/predict/" -Method POST -Body $body -ContentType "application/json"
```

### List Available Reports
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/reports/" -Method GET
```

### Download a Report
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/download_report/pc_diagnosis_data_20251031_143022.json" -OutFile "report.json"
```

## Verify Integration

Check that these files exist:
- ✅ `pc_diagnostic/hardware_monitor.py`
- ✅ `pc_diagnostic/advanced_telemetry.py`
- ✅ `pc_diagnostic/report_generator.py`
- ✅ `INTEGRATION_README.md`
- ✅ `INTEGRATION_SUMMARY.md`

## Troubleshooting

### Import Errors for psutil, GPUtil, or wmi
**Solution**: Make sure you installed requirements:
```bash
pip install psutil GPUtil wmi
```

### LibreHardwareMonitor Not Found
**Solution**: This is optional. The system will work without it. If you want advanced sensors:
1. Install `pip install pythonnet`
2. Download and place `LibreHardwareMonitorLib.dll` in the correct location

### Reports Directory Missing
**Solution**: The `reports/` directory is created automatically on first report generation.

### LLM Connection Error
**Solution**: This is expected if the LLM server is not running. The system will use offline fallback mode:
- Update `LLM_API_BASE` in `views.py` to your LLM server URL
- Or test with offline mode (automatic fallback)

## Configuration

### Change LLM Server URL
Edit `backend/pc_diagnostic/views.py`:
```python
LLM_API_BASE = "http://your-llm-server:port"
LLM_MODEL_ID = "your-model-id"
```

### Change Reports Directory
Edit `backend/pc_diagnostic/views.py`:
```python
report_generator = ReportGenerator(reports_folder='your_custom_path')
```

## Frontend Connection

The frontend should continue to work without changes. It uses:
- `POST http://localhost:8000/api/predict/`

The response format is enhanced but backward compatible:
```json
{
  "success": true,
  "message": "AI response...",
  "prediction": "AI response...",  // Kept for compatibility
  "model": "model-name",
  "finish_reason": "stop",
  "session_id": "uuid",           // NEW
  "telemetry_collected": true,    // NEW
  "telemetry_summary": {...},     // NEW
  "reports": {...},               // NEW (if generate_report=true)
  "usage": {...},
  "metadata": {...}
}
```

## What's New

### API Enhancements
1. ✨ Automatic telemetry collection based on user issue
2. ✨ Session ID tracking
3. ✨ Telemetry summary in response
4. ✨ Optional report generation
5. ✨ Offline fallback with smart diagnostics

### New Endpoints
1. ✨ `GET /api/telemetry/` - Get system telemetry
2. ✨ `GET /api/reports/` - List diagnostic reports
3. ✨ `GET /api/download_report/<filename>/` - Download reports

### System Capabilities
1. ✨ Detects issue types from user input (display, performance, network, etc.)
2. ✨ Collects issue-specific telemetry
3. ✨ Monitors CPU, memory, disk, network, processes
4. ✨ Optional HWiNFO-level sensor monitoring
5. ✨ Generates downloadable JSON reports
6. ✨ Works offline without LLM (fallback mode)

## Success Indicators

After setup, you should see:
1. ✅ Backend running at `http://localhost:8000/`
2. ✅ No import errors on startup
3. ✅ `/api/telemetry/` returns system data
4. ✅ `/api/predict/` collects telemetry and returns AI response
5. ✅ Reports are generated in `reports/` directory

## Next Steps

1. Test all endpoints
2. Review `INTEGRATION_README.md` for detailed API documentation
3. Check `INTEGRATION_SUMMARY.md` for integration details
4. (Optional) Configure advanced telemetry
5. (Optional) Customize LLM server URL

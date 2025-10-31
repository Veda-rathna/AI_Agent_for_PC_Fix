# Django Backend Integration - PC Diagnostic System

## Overview
This Django backend integrates the comprehensive hardware monitoring and AI diagnostic capabilities from the PC-Fix-Model into a REST API.

## Features Implemented

### 1. Hardware Monitoring (`hardware_monitor.py`)
- **System Information**: Platform, processor, architecture, boot time, uptime
- **CPU Monitoring**: Usage per core, frequency, load statistics
- **Memory Monitoring**: Total, available, used, swap information
- **Disk Monitoring**: All partitions with usage statistics
- **Network Monitoring**: Bytes sent/received, packet statistics, errors
- **Process Monitoring**: Top processes by CPU usage
- **Issue-Specific Diagnostics**:
  - Display: Graphics cards, monitors, driver versions
  - Audio: Sound devices and status
  - Network: Detailed adapter and connection information
  - Storage: Physical drives and health status
  - USB: Connected USB devices

### 2. Advanced Telemetry (`advanced_telemetry.py`)
**Optional features requiring additional packages:**
- LibreHardwareMonitor integration for HWiNFO-level sensors
- NVIDIA GPU telemetry via NVML
- Temperature sensors
- Power consumption sensors
- Fan speed sensors
- Voltage sensors
- Clock frequency sensors

### 3. Report Generation (`report_generator.py`)
- JSON diagnostic reports with full telemetry data
- Summary generation with key metrics
- Report listing and download capabilities

## API Endpoints

### 1. `/api/predict/` (POST)
Main diagnostic endpoint with telemetry collection.

**Request:**
```json
{
  "input_text": "My computer is running slow",
  "telemetry_data": null,  // Optional: provide pre-collected data
  "generate_report": true   // Optional: generate downloadable report
}
```

**Response:**
```json
{
  "success": true,
  "message": "AI diagnostic response...",
  "model": "reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1",
  "finish_reason": "stop",
  "session_id": "uuid",
  "telemetry_collected": true,
  "telemetry_summary": {
    "timestamp": "2025-10-31T...",
    "system": "Windows-10-...",
    "cpu_usage": 45.2,
    "memory_usage": 62.3,
    "issue_specific_data": ["display", "performance"]
  },
  "reports": {
    "json": {
      "filename": "pc_diagnosis_data_20251031_143022.json",
      "download_url": "/api/download_report/pc_diagnosis_data_20251031_143022.json"
    }
  },
  "usage": {
    "prompt_tokens": 1250,
    "completion_tokens": 890,
    "total_tokens": 2140
  },
  "metadata": {...}
}
```

### 2. `/api/telemetry/` (GET)
Get current system telemetry without AI analysis.

**Request:**
```
GET /api/telemetry/?issue=screen flickering
```

**Response:**
```json
{
  "success": true,
  "telemetry_data": {
    "timestamp": "...",
    "issue_types_detected": ["display"],
    "system_info": {...},
    "cpu": {...},
    "memory": {...},
    "disk": [...],
    "network": {...},
    "processes": [...],
    "issue_specific": {
      "display": {
        "monitors": [...],
        "graphics_cards": [...],
        "display_diagnostics": {...}
      }
    },
    "advanced_sensors": {...}  // If available
  },
  "timestamp": "2025-10-31T..."
}
```

### 3. `/api/reports/` (GET)
List all available diagnostic reports.

**Response:**
```json
{
  "success": true,
  "reports": [
    {
      "filename": "pc_diagnosis_data_20251031_143022.json",
      "filepath": "reports/pc_diagnosis_data_20251031_143022.json",
      "size": 52431,
      "created": "2025-10-31T14:30:22"
    }
  ],
  "total_reports": 1
}
```

### 4. `/api/download_report/<filename>/` (GET)
Download a specific diagnostic report.

**Request:**
```
GET /api/download_report/pc_diagnosis_data_20251031_143022.json
```

**Response:** File download

### 5. `/api/diagnose/` (POST)
Simple diagnostic endpoint (legacy).

### 6. `/api/upload/` (POST)
File upload endpoint for future extensions.

## Installation & Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Optional Advanced Telemetry
For HWiNFO-level hardware monitoring:
```bash
# Uncomment in requirements.txt and install:
pip install pythonnet nvidia-ml-py3
```

**Requirements for Advanced Telemetry:**
- **LibreHardwareMonitor**: Download and place `LibreHardwareMonitorLib.dll` in:
  - `C:\Program Files\LibreHardwareMonitor\`
  - `C:\LibreHardwareMonitor\`
  - Or in the backend directory

- **NVIDIA GPU**: NVIDIA drivers must be installed for NVML support

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Start Server
```bash
python manage.py runserver
```

## System Requirements

### Core Dependencies (Required)
- `psutil>=5.9.6` - System and process utilities
- `GPUtil>=1.4.0` - GPU information (NVIDIA/AMD)
- `wmi>=1.5.1` - Windows Management Instrumentation (Windows only)

### Optional Dependencies
- `pythonnet>=3.0.0` - LibreHardwareMonitor integration
- `nvidia-ml-py3>=7.352.0` - NVIDIA GPU telemetry

## How It Works

### 1. Issue Type Detection
The system analyzes user input to detect issue types:
- **Display**: screen, monitor, graphics, flickering, etc.
- **Performance**: slow, lag, freeze, CPU, memory, etc.
- **Network**: wifi, internet, connection, etc.
- **Audio**: sound, speaker, microphone, etc.
- **Storage**: disk, drive, SSD, HDD, etc.
- **Hardware**: USB, keyboard, mouse, etc.

### 2. Telemetry Collection
Based on detected issue types, the system collects:
- **General**: System info, CPU, memory, disk, network, processes
- **Issue-Specific**: Detailed diagnostics for the detected problem area
- **Advanced**: Sensor data from LibreHardwareMonitor and NVML (if available)

### 3. AI Analysis
The telemetry data is sent to the LLM along with the user's problem description for comprehensive analysis.

### 4. Offline Fallback
If the LLM server is unavailable, the system uses `generate_mock_analysis()` to provide basic diagnostic recommendations based on the telemetry data.

## Telemetry Data Structure

```json
{
  "timestamp": "2025-10-31T14:30:22.123456",
  "issue_types_detected": ["display", "performance"],
  "user_description": "My screen is flickering",
  "system_info": {
    "platform": "Windows-10-10.0.19045-SP0",
    "processor": "Intel64 Family 6 Model 142 Stepping 12, GenuineIntel",
    "architecture": ["64bit", "WindowsPE"],
    "machine": "AMD64",
    "python_version": "3.11.0",
    "hostname": "DESKTOP-ABC123",
    "boot_time": "2025-10-31T08:00:00",
    "uptime_seconds": 23422.45
  },
  "cpu": {
    "physical_cores": 4,
    "total_cores": 8,
    "usage_per_core": [45.2, 38.1, 52.3, 41.0, ...],
    "total_usage": 44.2,
    "current_frequency": 2808.0,
    "min_frequency": 400.0,
    "max_frequency": 3400.0
  },
  "memory": {
    "total": 17179869184,
    "available": 6442450944,
    "used": 10737418240,
    "percentage": 62.5,
    "free": 6442450944,
    "swap_total": 4294967296,
    "swap_used": 1073741824,
    "swap_free": 3221225472,
    "swap_percentage": 25.0
  },
  "disk": [
    {
      "device": "C:\\",
      "mountpoint": "C:\\",
      "file_system": "NTFS",
      "total": 536870912000,
      "used": 322122547200,
      "free": 214748364800,
      "percentage": 60.0
    }
  ],
  "network": {
    "bytes_sent": 1234567890,
    "bytes_recv": 9876543210,
    "packets_sent": 123456,
    "packets_recv": 987654,
    "errors_in": 0,
    "errors_out": 0,
    "dropin": 0,
    "dropout": 0
  },
  "processes": [
    {
      "pid": 1234,
      "name": "chrome.exe",
      "cpu_percent": 15.2,
      "memory_percent": 12.5,
      "status": "running"
    }
  ],
  "issue_specific": {
    "display": {
      "monitors": [...],
      "graphics_cards": [...],
      "display_diagnostics": {...}
    }
  },
  "advanced_sensors": {
    "thermal_sensors": {...},
    "power_sensors": {...},
    "fan_sensors": {...},
    "voltage_sensors": {...},
    "clock_sensors": {...}
  }
}
```

## Configuration

### LLM Server Configuration
Edit `views.py`:
```python
LLM_API_BASE = "http://127.0.0.1:1234"  # Your LLM server URL
LLM_MODEL_ID = "reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1"
```

### Reports Directory
The system creates a `reports/` directory in the backend root for storing generated diagnostic reports.

## Error Handling

The system includes comprehensive error handling:
1. **LLM Connection Errors**: Falls back to offline diagnostic mode
2. **Telemetry Collection Errors**: Gracefully handles missing sensors/data
3. **Permission Errors**: Handles restricted system access
4. **Timeout Protection**: Prevents long-running operations from blocking

## Future Enhancements

Potential additions from PC-Fix-Model:
1. PDF report generation (requires `reportlab`)
2. SMART disk health monitoring
3. Event log analysis for Windows
4. Registry diagnostics
5. Detailed network troubleshooting
6. Audio device diagnostics

## Notes

- Windows-specific features (WMI, LibreHardwareMonitor) only work on Windows
- Advanced telemetry requires administrator privileges for some sensors
- Large telemetry data (>20KB) is automatically summarized for LLM processing
- Full telemetry is always saved in generated reports

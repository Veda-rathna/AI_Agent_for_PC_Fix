# Hardware Protection Feature Documentation

## Overview
The Hardware Protection feature is a security tool that creates encrypted hardware fingerprints to detect unauthorized hardware changes. This is particularly useful for detecting component replacements that may have occurred during service center repairs.

## Key Features

### 1. **Generate Hardware Hash File**
- Collects comprehensive hardware information from your system
- Extracts permanent components (serial numbers, UUIDs, BIOS info)
- Captures changeable components (CPU, GPU, RAM, storage, display, network, battery)
- Encrypts all data using Fernet symmetric encryption with PBKDF2 key derivation
- Creates a read-only `.hwh` (Hardware Hash) file for protection

### 2. **Analyze Hardware Hash File**
- Uploads and decrypts previously generated hardware hash files
- Compares original hardware configuration with current system
- Identifies critical changes in permanent components
- Detects modifications in changeable components
- Provides detailed reports on what changed and when

## How It Works

### Hardware Information Collection

The system collects two types of hardware information:

#### **Permanent Components** (Should Never Change)
- System UUID
- BIOS Serial Number
- Motherboard Serial Number
- Processor ID

These components serve as the unique identifier for your computer. Any change in these indicates a major hardware replacement or potential tampering.

#### **Changeable Components** (Can Be Replaced in Service Centers)
- **CPU**: Name, cores, clock speed, manufacturer
- **GPU**: Name, VRAM, driver version, PNP Device ID
- **RAM**: Capacity, speed, manufacturer, part number, serial number
- **Storage**: Model, size, serial number, interface type
- **Display**: Monitor name, PNP Device ID, resolution
- **Network**: Adapter name, MAC address, manufacturer
- **Battery**: Chemistry type, capacity, health status

### Encryption & Security

1. **Password-Based Encryption**: Users can optionally provide a password (defaults to "default_password")
2. **PBKDF2 Key Derivation**: Uses 100,000 iterations with SHA-256
3. **Fernet Encryption**: Industry-standard symmetric encryption
4. **Read-Only File**: Generated file is set to read-only (chmod 444) to prevent tampering

### File Format

Hardware hash files (`.hwh`) contain:
```json
{
  "version": "1.0",
  "created": "2025-10-31T18:00:00",
  "encrypted_data": "base64_encrypted_string",
  "hash": "sha256_hash_of_hardware_data",
  "metadata": {
    "platform": "Windows",
    "hostname": "DESKTOP-XXXXX",
    "generation_timestamp": "2025-10-31T18:00:00"
  }
}
```

## Usage Guide

### Generating a Hardware Hash File

1. Navigate to **Hardware Protection** page
2. Click on **"Generate Hash File"** tab
3. (Optional) Enter a custom password for encryption
4. Click **"Generate Hardware Hash File"** button
5. Wait for the system to collect hardware information
6. Download the generated `.hwh` file
7. **Store this file in a safe location** (external drive, cloud storage, etc.)

**Recommended Practice**: Generate a hash file when you first receive your computer or after a legitimate hardware upgrade.

### Analyzing a Hardware Hash File

1. Navigate to **Hardware Protection** page
2. Click on **"Analyze Hash File"** tab
3. Enter the password (same one used during generation)
4. Click **"Choose Hardware Hash File"** and select your `.hwh` file
5. Click **"Analyze Hardware Changes"** button
6. Review the analysis results:
   - **Green**: No changes detected
   - **Yellow**: Component changes detected (may be legitimate)
   - **Red**: Critical changes in permanent components (warning!)

## API Endpoints

### Generate Hardware Hash
```
POST /api/hardware-hash/generate/
Content-Type: application/json

{
  "password": "your_password"  // Optional
}

Response:
{
  "success": true,
  "filename": "hardware_hash_HOSTNAME_20251031_180000.hwh",
  "hardware_hash": "abc123...",
  "download_url": "/api/download_hardware_hash/filename.hwh",
  "components_captured": {
    "permanent": 4,
    "changeable": 7
  }
}
```

### Analyze Hardware Hash
```
POST /api/hardware-hash/analyze/
Content-Type: multipart/form-data

file: [hardware_hash_file.hwh]
password: "your_password"

Response:
{
  "success": true,
  "comparison": {
    "overall_status": "changed|unchanged",
    "changes_detected": [...],
    "changeable_components_changes": [...],
    "summary": {
      "total_changes": 3,
      "critical_changes": 0,
      "component_changes": 3
    }
  }
}
```

### Download Hardware Hash
```
GET /api/download_hardware_hash/<filename>/

Response: File download
```

## Change Detection Logic

### Critical Changes (Permanent Components)
If any of these change, it's flagged as **CRITICAL**:
- System UUID
- BIOS Serial Number
- Motherboard Serial Number
- Processor ID

**Possible Reasons**:
- Motherboard replacement
- Complete system replacement
- BIOS reflashing (UUID might change)
- **Potential security concern**

### Component Changes (Changeable Components)
These are tracked but considered normal for service center repairs:
- RAM module replacement (different serial numbers)
- Storage drive upgrade
- GPU replacement
- Display panel replacement
- Battery replacement
- Network adapter changes

**Change Severity Levels**:
- **Low**: Minor differences (e.g., driver version updates)
- **Medium**: Component count changes (e.g., added/removed RAM stick)
- **Critical**: Permanent component alterations

## Use Cases

### 1. **Post-Service Center Verification**
After getting your laptop/PC serviced:
1. Upload your original hash file
2. Compare with current hardware
3. Verify if all replaced parts were authorized

### 2. **Pre-Sale Hardware Verification**
Before buying a used computer:
1. Ask the seller for their hardware hash file
2. Analyze it on the actual computer
3. Verify the hardware matches what was advertised

### 3. **Company Asset Tracking**
Organizations can:
1. Generate hash files for all company computers
2. Periodically verify hardware hasn't been tampered with
3. Track unauthorized upgrades or downgrades

### 4. **Warranty Fraud Prevention**
1. Generate hash before warranty period
2. Check after warranty service
3. Ensure only authorized parts were replaced

## Security Considerations

### Strengths
✅ Encrypted with industry-standard cryptography  
✅ Password-protected  
✅ Read-only file prevents accidental modification  
✅ Comprehensive hardware fingerprinting  
✅ Detects both major and minor hardware changes  

### Limitations
⚠️ Default password is weak - always use a custom password  
⚠️ File can be deleted (store backups)  
⚠️ Requires Windows Management Instrumentation (WMI) for detailed info  
⚠️ Driver updates may cause false positives (filtered out in comparison)  

## Technical Implementation

### Backend (Django)
- **Module**: `hardware_hash.py`
- **Class**: `HardwareHashProtection`
- **Dependencies**: `cryptography`, `psutil`, `wmi`, `platform`

### Frontend (React)
- **Component**: `HardwareProtection.js`
- **Features**: Tab-based interface, file upload, download handling
- **Styling**: Modern gradient design with responsive layout

### File Storage
- Generated files: `backend/media/hardware_hashes/`
- Temporary uploads: `backend/media/temp_uploads/`

## Troubleshooting

### "Failed to generate hardware hash"
- Check if WMI is available (Windows only)
- Ensure Python cryptography package is installed
- Verify write permissions to media folder

### "Decryption failed"
- Wrong password entered
- Corrupted hash file
- File generated with different cryptography version

### "Many changes detected"
- Normal after service center visit
- Driver updates can cause minor changes
- Review each change individually

## Future Enhancements

🔮 **Planned Features**:
- Support for Linux/macOS hardware detection
- Cloud storage integration for hash files
- Automated email alerts for hardware changes
- Multi-computer comparison dashboard
- Hardware change history timeline
- QR code generation for hash files
- Mobile app for on-the-go verification

## Support

For issues or questions:
1. Check the documentation above
2. Review error messages in the console
3. Ensure all dependencies are installed
4. Contact support with hardware hash file metadata (not the file itself!)

---

**Version**: 1.0  
**Last Updated**: October 31, 2025  
**License**: MIT

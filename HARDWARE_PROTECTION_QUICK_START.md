# Hardware Protection Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

Required package: `cryptography==41.0.7`

### Step 2: Start the Backend
```bash
cd backend
python manage.py runserver
```

Server will start at: `http://localhost:8000`

### Step 3: Start the Frontend
```bash
cd frontend
npm install
npm start
```

Frontend will start at: `http://localhost:3000`

---

## 📋 How to Use

### Generate Your Hardware Hash File

1. **Open the app**: Navigate to http://localhost:3000
2. **Click "Hardware Protection"** in the navigation menu
3. **Select "Generate Hash File"** tab
4. **(Optional)** Enter a password for extra security
5. **Click "Generate Hardware Hash File"**
6. **Download the file** when ready
7. **Store it safely** - you'll need it later!

### Analyze Hardware Changes

1. **Open the app** and go to **"Hardware Protection"**
2. **Select "Analyze Hash File"** tab
3. **Enter the password** you used when generating
4. **Upload your `.hwh` file**
5. **Click "Analyze Hardware Changes"**
6. **Review the results**:
   - ✅ Green = No changes
   - ⚠️ Yellow = Component changes detected
   - 🚨 Red = Critical permanent component changes

---

## ⚡ Quick Commands

### Backend
```powershell
# Install dependencies
cd backend
pip install cryptography==41.0.7

# Run server
python manage.py runserver
```

### Frontend
```powershell
# Install dependencies
cd frontend
npm install

# Run development server
npm start
```

---

## 🔍 What Gets Captured?

### Permanent Components (Never Change)
- ✓ System UUID
- ✓ BIOS Serial
- ✓ Motherboard Serial
- ✓ Processor ID

### Changeable Components (Service Centers)
- ✓ CPU Details
- ✓ GPU Information
- ✓ RAM Modules
- ✓ Storage Drives
- ✓ Display Adapters
- ✓ Network Cards
- ✓ Battery Info

---

## 🛡️ Security Tips

1. **Use a Strong Password**: Don't rely on the default password
2. **Store Backups**: Keep hash files in multiple safe locations
3. **Regular Checks**: Verify hardware after any service center visit
4. **Document Changes**: Keep records of legitimate hardware upgrades

---

## ⚠️ Common Issues

### "Cannot import cryptography"
**Solution**: Install the package
```bash
pip install cryptography==41.0.7
```

### "WMI not available"
**Solution**: This feature currently requires Windows

### "Wrong password" error
**Solution**: Use the exact same password you used during generation

---

## 📝 Example Workflow

### Scenario: Pre-Service Center Check
```
1. Generate hash file ➜ Store safely
2. Send PC to service center
3. Get PC back
4. Analyze hash file ➜ Check for changes
5. Verify all changes were authorized
```

### Scenario: Buying Used Computer
```
1. Ask seller for their hash file
2. Meet with computer
3. Analyze hash file on the actual PC
4. Verify hardware matches listing
5. Make informed purchase decision
```

---

## 🎯 Next Steps

- Read full documentation: [HARDWARE_PROTECTION_DOCS.md](./HARDWARE_PROTECTION_DOCS.md)
- Test with your current system
- Generate your baseline hash file
- Set a reminder to verify monthly

---

**Need Help?** Check the full documentation or raise an issue on GitHub.

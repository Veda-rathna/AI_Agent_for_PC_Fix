# Cloudflare Tunnel Setup Guide

## Current Issue
❌ **Cannot resolve**: `factors-arrangements-marine-policies.trycloudflare.com`

This means the Cloudflare tunnel is either:
- Expired (free tunnels expire after some time)
- Changed URL
- Not active

## Solution Steps

### Option 1: Verify and Get New Tunnel URL (If using Cloudflare Tunnel)

1. **On your GPU server**, check if the tunnel is still running:
   ```bash
   # Check running processes
   ps aux | grep cloudflare
   # or
   lsof -i :8888
   ```

2. **If tunnel is not running**, restart it:
   ```bash
   # Example using cloudflared
   cloudflared tunnel --url http://localhost:8888
   ```

3. **The new tunnel URL will be displayed** in the output, something like:
   ```
   INF | https://some-new-random-words.trycloudflare.com
   ```

4. **Copy the new URL** and update it in `backend/pc_diagnostic/views.py`:
   ```python
   LLM_API_BASE = "https://YOUR-NEW-TUNNEL-URL.trycloudflare.com"
   ```

### Option 2: Use Direct Connection (If Backend and Server are on Same Machine)

If your Django backend and llama.cpp server are on the same machine:

```python
# In backend/pc_diagnostic/views.py
LLM_API_BASE = "http://localhost:8888"
```

### Option 3: Use ngrok (Alternative to Cloudflare)

1. **Install ngrok** on your GPU server
2. **Start ngrok tunnel**:
   ```bash
   ngrok http 8888
   ```
3. **Copy the forwarding URL** (e.g., `https://xxxx-xxx-xxx-xxx.ngrok-free.app`)
4. **Update the configuration**:
   ```python
   LLM_API_BASE = "https://xxxx-xxx-xxx-xxx.ngrok-free.app"
   ```

### Option 4: Use SSH Tunnel (If you have SSH access)

```bash
# On your local machine
ssh -L 8888:localhost:8888 user@gpu-server
```

Then update:
```python
LLM_API_BASE = "http://localhost:8888"
```

## How to Find Your Current Tunnel URL

### On your GPU server, run:
```bash
# Check cloudflare tunnel logs
journalctl -u cloudflared -f

# Or check the process
ps aux | grep cloudflare

# Or check what's listening on port 8888
netstat -tlnp | grep 8888
```

## Quick Test After Updating URL

Run the test script:
```bash
cd backend
python test_llm_connection.py
```

## Current Configuration

**File**: `backend/pc_diagnostic/views.py`

**Current URL**: `https://factors-arrangements-marine-policies.trycloudflare.com`

**Status**: ❌ Not reachable (DNS resolution failed)

**Action Required**: Update the URL with the correct tunnel endpoint

---

## Next Steps

1. ✅ **Find the correct tunnel URL** from your GPU server
2. ✅ **Update** `LLM_API_BASE` in `views.py`
3. ✅ **Run test**: `python test_llm_connection.py`
4. ✅ **Test API**: Make a request to `/api/predict`

---

**Note**: Cloudflare free tunnels can change URLs or expire. For production, consider:
- Using a paid Cloudflare tunnel with a fixed domain
- Setting up a proper reverse proxy (nginx)
- Using a VPS with a static IP

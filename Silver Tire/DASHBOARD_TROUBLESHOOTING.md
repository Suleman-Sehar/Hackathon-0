# Silver Tier Dashboard - Troubleshooting Guide

## Current Status

### ✅ Backend API - WORKING
- Server running on http://localhost:8001
- Email endpoint: Working (tested successfully)
- WhatsApp endpoint: Ready (requires browser login)
- LinkedIn endpoint: Ready (requires browser login)
- All endpoints returning proper JSON responses

### ✅ MCP Modules - WORKING
- Email MCP: Tested and sending emails
- WhatsApp MCP: Function added and working
- LinkedIn MCP: Function existing and working

### ⚠️ Dashboard UI - NEEDS TESTING
- HTML loads correctly
- JavaScript loads correctly
- Button onclick handlers defined
- Functions exist in global scope

---

## How to Test

### Method 1: Quick Test Page (RECOMMENDED)
1. Open: http://localhost:8001/quick_test.html
2. Click "Test Email" button
3. Check your email inbox
4. Should receive test email

### Method 2: Debug Page
1. Open: http://localhost:8001/debug.html
2. Click "Test Email" button
3. Watch console logs appear
4. Shows detailed API responses

### Method 3: Main Dashboard
1. Open: http://localhost:8001
2. Click "Test" button on Gmail card
3. Check browser console (F12)
4. Look for errors

### Method 4: Direct API Test
```bash
curl -X POST http://localhost:8001/api/v1/test/email \
  -H "Content-Type: application/json" \
  -d "{\"to\":\"solemanseher@gmail.com\",\"subject\":\"Test\",\"body\":\"Test\"}"
```

Expected response:
```json
{"status": "success", "message": "Email sent successfully"}
```

---

## Common Issues & Solutions

### Issue 1: Buttons Don't Respond

**Symptoms:**
- Click buttons but nothing happens
- No error messages
- Console shows no logs

**Possible Causes:**
1. JavaScript not loaded
2. Event handler not attached
3. Browser cache issue

**Solutions:**
1. Hard refresh: Ctrl + Shift + R
2. Clear browser cache
3. Open browser console (F12) and check for errors
4. Try the Quick Test page instead

---

### Issue 2: "Failed to fetch" Error

**Symptoms:**
- Error message: "Failed to fetch"
- Console shows: TypeError: Failed to fetch

**Possible Causes:**
1. Server not running
2. CORS issue
3. Wrong API URL

**Solutions:**
1. Check server is running: http://localhost:8001/api/v1/health
2. Restart server: Run `python dashboard_api.py`
3. Check browser console for CORS errors

---

### Issue 3: Email Not Sending

**Symptoms:**
- Button clicks but email not received
- API returns error

**Possible Causes:**
1. Credentials not configured
2. Gmail app password invalid
3. SMTP connection failed

**Solutions:**
1. Check credentials.json exists in root directory
2. Verify email and app_password are correct
3. Test credentials: Run `python test_integrations.py`

**Credential Format:**
```json
{
    "email": "your-email@gmail.com",
    "email_app_password": "16-char-app-password",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}
```

---

### Issue 4: WhatsApp/LinkedIn Browser Opens But Doesn't Send

**Symptoms:**
- Browser opens
- WhatsApp Web or LinkedIn loads
- Message/post not sent

**Possible Causes:**
1. First time - requires login
2. Session not saved
3. Selector not found

**Solutions:**

**WhatsApp First-Time Setup:**
1. Browser will open WhatsApp Web
2. Scan QR code with your phone
3. Check "Remember me" / "Keep me signed in"
4. Close browser manually
5. Session saved in `whatsapp_session/` folder
6. Next time will work automatically

**LinkedIn First-Time Setup:**
1. Browser will open LinkedIn
2. Login manually with credentials
3. Navigate to feed
4. Close browser manually
5. Session saved in `linkedin_session/` folder
6. Next time will work automatically

---

## Testing Checklist

### Backend API
- [ ] Server starts without errors
- [ ] Health endpoint responds: http://localhost:8001/api/v1/health
- [ ] Email endpoint works (test via curl or Python)
- [ ] Metrics endpoint returns data

### Frontend UI
- [ ] Dashboard loads at http://localhost:8001
- [ ] Quick Test page loads at http://localhost:8001/quick_test.html
- [ ] Debug page loads at http://localhost:8001/debug.html
- [ ] Buttons are clickable
- [ ] Console shows no errors

### Integrations
- [ ] Email sends successfully
- [ ] Email received in inbox
- [ ] WhatsApp browser opens
- [ ] WhatsApp session saves after QR scan
- [ ] LinkedIn browser opens
- [ ] LinkedIn session saves after login

---

## Server Logs

When running `python dashboard_api.py`, you should see:

```
============================================================
  SILVER TIER DASHBOARD API
============================================================
  Starting server on http://0.0.0.0:8001
  Dashboard: http://localhost:8001
  API Docs: http://localhost:8001/docs
============================================================

INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

When email is sent, you should see:

```
============================================================
[EMAIL] Received request
[EMAIL] To: solemanseher@gmail.com
[EMAIL] Subject: Test
[EMAIL] Body: Test...
[INFO] Loaded credentials from ...
[EMAIL] Credentials loaded: solemanseher@gmail.com
[INFO] Loaded credentials from ...
[OK] Email sent to solemanseher@gmail.com
[EMAIL] Send result: True
[EMAIL] SUCCESS
```

---

## Quick Commands

### Start Dashboard
```bash
cd "D:\Hackathon 0\Silver Tire"
python dashboard_api.py
```

### Test Email Directly
```bash
cd "D:\Hackathon 0\Silver Tire"
python -c "from mcp.email_mcp import send_email; send_email('solemanseher@gmail.com', 'Test', 'Test')"
```

### Check Server Health
```bash
python -c "import requests; print(requests.get('http://localhost:8001/api/v1/health').json())"
```

### View Today's Logs
```bash
type Silver Tire\Logs\audit_YYYY-MM-DD.json
```

### Stop Server
```bash
taskkill /F /IM python.exe
```

---

## File Locations

```
Silver Tire/
├── dashboard_api.py          # Main API server
├── dashboard/
│   ├── index.html            # Main dashboard
│   ├── quick_test.html       # Simple test page
│   ├── debug.html            # Debug console
│   └── static/
│       ├── css/styles.css    # Styling
│       └── js/app.js         # Dashboard logic
├── mcp/
│   ├── email_mcp.py          # Email integration
│   ├── whatsapp_mcp.py       # WhatsApp integration
│   └── linkedin_post.py      # LinkedIn integration
├── Logs/                      # Audit logs
├── whatsapp_session/          # WhatsApp browser session
├── linkedin_session/          # LinkedIn browser session
└── credentials.json           # In root directory
```

---

## Next Steps

1. **Test Email First**
   - Open http://localhost:8001/quick_test.html
   - Click "Test Email"
   - Check inbox at solemanseher@gmail.com

2. **If Email Works**
   - Main dashboard should also work
   - Try WhatsApp and LinkedIn tests

3. **If Email Doesn't Work**
   - Check server logs
   - Verify credentials.json
   - Test via curl command

4. **WhatsApp/LinkedIn Setup**
   - Complete first-time login
   - Save sessions
   - Retry tests

---

## Support

If issues persist:
1. Check all server logs
2. Open browser console (F12)
3. Try Quick Test page
4. Test via curl/Python directly
5. Verify credentials

**Server is currently:** RUNNING on http://localhost:8001
**Email integration:** WORKING
**WhatsApp integration:** READY (needs QR login)
**LinkedIn integration:** READY (needs manual login)

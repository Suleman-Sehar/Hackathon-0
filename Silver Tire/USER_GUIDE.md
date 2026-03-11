# 📘 SILVER TIER DASHBOARD - COMPLETE USER GUIDE

**Version:** 1.0  
**Date:** March 10, 2026

---

## 🎯 QUICK START - How to Use Dashboard

### Step 1: Open Dashboard
```
URL: http://localhost:8001
```

### Step 2: Hard Refresh (First Time Only)
```
Press: Ctrl + Shift + R
This clears cache and loads latest version
```

---

## 📧 HOW TO SEND EMAIL (Gmail)

### Method 1: Quick Test (Fastest)

1. **Find Gmail Card** (red envelope icon)
2. **Click "Test" button** (purple button on left)
3. **Watch notification**: "📧 Sending email to solemanseher@gmail.com..."
4. **Wait 5-10 seconds**
5. **Success message**: "✅ Email sent successfully!"
6. **Check your inbox** at solemanseher@gmail.com

**What happens:**
- Sends test email via Gmail SMTP
- Uses your configured credentials
- Logs to activity feed
- Takes 5-10 seconds

---

### Method 2: Create Custom Email

1. **Click "New Email"** button in Welcome Banner
   - OR press "Send Email" in Quick Actions

2. **Fill the form:**
   ```
   To: recipient@example.com
   Subject: Meeting Reminder
   Message: Your message here...
   ```

3. **Click "Send Email"**

4. **Watch for success notification**

5. **Check activity feed** - Shows email was sent

---

### Method 3: Via Approved Folder (Autonomous)

1. **Create file:** `D:\Hackathon 0\Approved\Email\my_email.md`

2. **Add content:**
   ```markdown
   # Email Request

   To: client@example.com
   Subject: Project Update
   CC: manager@example.com

   ---

   Dear Client,

   Here is the project update...

   Best regards,
   Your Name
   ```

3. **Save the file**

4. **Orchestrator auto-processes** (every 30 seconds)

5. **Email sends automatically**

6. **File moves to:** `Done/SENT_my_email.md`

---

## 💬 HOW TO SEND WHATSAPP MESSAGE

### Method 1: Quick Test (First Time Setup)

1. **Find WhatsApp Card** (green WhatsApp icon)
2. **Click "Test" button** (purple button)
3. **Browser opens** with WhatsApp Web
4. **First time only:**
   - Scan QR code with your phone
   - Check "Keep me signed in"
   - Wait for login
5. **Message sends automatically**
6. **Success notification appears**

**Next times:**
- No QR scan needed
- Sends automatically
- Uses saved session

---

### Method 2: Send to Custom Number

1. **Click "Send WhatsApp"** in Quick Actions

2. **Fill the form:**
   ```
   Phone Number: +923322580130
   (Include country code, without +)
   
   Message: Hello! This is a test message.
   ```

3. **Click "Send Message"**

4. **Browser opens and sends**

5. **Success notification appears**

---

### Method 3: Via Approved Folder

1. **Create file:** `D:\Hackathon 0\Approved\WhatsApp\message.md`

2. **Add content:**
   ```markdown
   # WhatsApp Message

   Phone: +923322580130
   Message Body: Hi! This is an automated message.

   ```

3. **Save the file**

4. **Orchestrator auto-sends**

5. **File moves to:** `Done/SENT_message.md`

---

## 💼 HOW TO POST TO LINKEDIN

### Method 1: Quick Test (First Time Setup)

1. **Find LinkedIn Card** (blue LinkedIn icon)
2. **Click "Post" button** (purple button)
3. **Browser opens** with LinkedIn
4. **First time only:**
   - Login with your credentials
   - Check "Stay signed in"
   - Navigate to feed
5. **Post publishes automatically**
6. **Success notification appears**

**Next times:**
- No login needed
- Posts automatically
- Uses saved session

---

### Method 2: Create Custom Post

1. **Click "Post to LinkedIn"** in Quick Actions

2. **Fill the form:**
   ```
   Post Content:
   🚀 Exciting news about our new product!
   
   We've been working hard on...
   
   #AI #Technology #Innovation
   ```

3. **Click "Publish Post"**

4. **Browser opens and posts**

5. **Success notification appears**

---

### Method 3: Via Approved Folder

1. **Create file:** `D:\Hackathon 0\Approved\LinkedIn\post.md`

2. **Add content:**
   ```markdown
   # LinkedIn Post

   ---

   🚀 Exciting Update!

   We just launched our new AI system...

   #AI #Automation #Innovation
   ```

3. **Save the file**

4. **Orchestrator auto-posts**

5. **File moves to:** `Done/POSTED_post.md`

---

## 🔍 HOW TO VIEW LOGS

### View Platform Logs:

1. **Find any platform card** (Gmail/WhatsApp/LinkedIn)
2. **Click "Logs" button** (purple button on right)
3. **Opens audit log** in new tab
4. **Shows all actions** for that platform

**What you see:**
- Timestamp
- Action type
- Recipient (email/phone)
- Status (success/error)
- Error details if failed

---

### View All Activity:

1. **Scroll to "Recent Activity" section**
2. **See last 15 actions**
3. **Each shows:**
   - Icon (email/WhatsApp/LinkedIn)
   - Recipient info
   - Timestamp
   - Success/Error status
4. **Click "View All"** to see full log folder

---

## 🎯 BUTTON FUNCTIONS

### Platform Cards (3 cards):

| Card | Left Button | Right Button |
|------|-------------|--------------|
| **Gmail** | Test (sends email) | Logs (view email logs) |
| **WhatsApp** | Test (sends message) | Logs (view WhatsApp logs) |
| **LinkedIn** | Post (creates post) | Logs (view LinkedIn logs) |

### Quick Actions (4 cards):

| Card | Action |
|------|--------|
| **Send Email** | Opens email form |
| **Send WhatsApp** | Opens WhatsApp form |
| **Post to LinkedIn** | Opens LinkedIn form |
| **Run Orchestrator** | Processes all pending files |

### Welcome Banner (3 buttons):

| Button | Action |
|--------|--------|
| **New Email** | Opens email form |
| **Send Message** | Opens WhatsApp form |
| **Create Post** | Opens LinkedIn form |

---

## 📊 METRICS EXPLAINED

### Top Metrics Cards:

1. **Emails Sent Today**
   - Count of emails sent via Gmail
   - Updates every 30 seconds
   - From audit logs

2. **WhatsApp Messages**
   - Count of WhatsApp messages sent
   - Browser automation
   - Updates every 30 seconds

3. **LinkedIn Posts**
   - Count of LinkedIn posts published
   - Auto-posting
   - Updates every 30 seconds

4. **Total Actions**
   - Combined count of all actions
   - Emails + Messages + Posts
   - Today's activity

### Platform Card Stats:

Each platform card shows:
- **Sent Today** - Count for that platform
- **Pending** - Files waiting in Approved folder

---

## 🔄 HOW ORCHESTRATOR WORKS

### What It Does:
- Monitors Approved folders every 30 seconds
- Finds new files (email/WhatsApp/LinkedIn)
- Processes them automatically
- Moves to Done folder after success
- Logs all actions

### How to Use:

**Option 1: Manual Trigger**
1. Click "Run Orchestrator" in Quick Actions
2. Processes all pending files
3. Takes 10-30 seconds
4. Dashboard auto-refreshes

**Option 2: Automatic**
1. Drop files in Approved folders
2. Wait 30 seconds
3. Orchestrator processes automatically
4. No action needed

### Folder Structure:
```
Approved/
├── Email/
│   └── your_email.md  ← Drop here
├── WhatsApp/
│   └── your_message.md  ← Drop here
└── LinkedIn/
    └── your_post.md  ← Drop here

Done/
├── SENT_email.md  ← Moves here after sent
├── SENT_message.md  ← Moves here after sent
└── POSTED_post.md  ← Moves here after posted
```

---

## 🐛 TROUBLESHOOTING

### Buttons Not Working?

**Solution 1: Hard Refresh**
```
Press: Ctrl + Shift + R
This clears browser cache
```

**Solution 2: Check Console**
```
1. Press F12
2. Go to Console tab
3. Look for errors (red text)
4. Share screenshot if issues persist
```

**Solution 3: Use Test Page**
```
Open: http://localhost:8001/activity_test.html
This page bypasses all cache issues
```

---

### Email Not Sending?

**Check 1: Credentials**
```
File: D:\Hackathon 0\credentials.json
Should contain:
{
    "email": "your-email@gmail.com",
    "email_app_password": "16-char-app-password"
}
```

**Check 2: Test API**
```bash
python -c "import requests; print(requests.post('http://localhost:8001/api/v1/test/email', json={'to': 'solemanseher@gmail.com', 'subject': 'Test', 'body': 'Test'}).json())"
```
Should return: `{"status": "success", ...}`

**Check 3: Check Inbox**
```
Look for email from: solemanseher@gmail.com
Subject: Test
```

---

### WhatsApp Not Sending?

**Issue 1: First Time Setup**
```
1. Click Test button
2. Browser opens WhatsApp Web
3. Scan QR code with phone
4. Check "Keep me signed in"
5. Wait for login
6. Message sends
```

**Issue 2: Session Lost**
```
1. Delete folder: whatsapp_session/
2. Click Test button again
3. Re-scan QR code
4. Session re-saves
```

**Issue 3: Wrong Number Format**
```
Use: +923322580130 (with +)
Or: 923322580130 (without +)
Not: 03322580130 (missing country code)
```

---

### LinkedIn Not Posting?

**Issue 1: First Time Setup**
```
1. Click Post button
2. Browser opens LinkedIn
3. Login with credentials
4. Check "Stay signed in"
5. Navigate to feed
6. Close browser
7. Session saves
```

**Issue 2: Session Lost**
```
1. Delete folder: linkedin_session/
2. Click Post button again
3. Re-login
4. Session re-saves
```

**Issue 3: Post Too Long**
```
LinkedIn limit: 3000 characters
Keep posts under 1000 for best results
```

---

### Activity Feed Not Loading?

**Solution 1: Hard Refresh**
```
Press: Ctrl + Shift + R
```

**Solution 2: Click Retry**
```
If shows error, click "Retry" button
```

**Solution 3: Check Server**
```bash
python -c "import requests; print(requests.get('http://localhost:8001/api/v1/health').json())"
```
Should return: `{"status": "healthy"}`

---

## 📋 QUICK REFERENCE

### URLs:
- **Main Dashboard:** http://localhost:8001
- **Quick Test:** http://localhost:8001/quick_test.html
- **Activity Test:** http://localhost:8001/activity_test.html
- **API Docs:** http://localhost:8001/docs

### Folders:
- **Approved Emails:** `D:\Hackathon 0\Approved\Email\`
- **Approved WhatsApp:** `D:\Hackathon 0\Approved\WhatsApp\`
- **Approved LinkedIn:** `D:\Hackathon 0\Approved\LinkedIn\`
- **Done Files:** `D:\Hackathon 0\Done\`
- **Logs:** `D:\Hackathon 0\Silver Tire\Logs\`

### Commands:
```bash
# Start Dashboard
cd "D:\Hackathon 0\Silver Tire"
python dashboard_api.py

# Test Email
python -c "from mcp.email_mcp import send_email; send_email('solemanseher@gmail.com', 'Test', 'Body')"

# Test WhatsApp
python -c "from mcp.whatsapp_mcp import send_whatsapp_message; send_whatsapp_message('+923322580130', 'Test')"

# Test LinkedIn
python -c "from mcp.linkedin_post import post_to_linkedin; post_to_linkedin('Test post')"
```

---

## ✅ WORKFLOW EXAMPLES

### Example 1: Send Email to Client

**Via Dashboard:**
1. Open http://localhost:8001
2. Click "New Email"
3. Fill:
   - To: client@company.com
   - Subject: Project Update
   - Message: Dear Client, ...
4. Click "Send Email"
5. Wait for success notification
6. Check activity feed

**Via Approved Folder:**
1. Create: `Approved/Email/client_update.md`
2. Add content with To/Subject/Body
3. Save file
4. Wait 30 seconds
5. Check Done folder

---

### Example 2: Send WhatsApp to Team

**Via Dashboard:**
1. Open http://localhost:8001
2. Click "Send WhatsApp"
3. Fill:
   - Phone: +923322580130
   - Message: Team meeting at 3 PM
4. Click "Send Message"
5. Browser opens and sends
6. Success notification appears

**Via Approved Folder:**
1. Create: `Approved/WhatsApp/team_message.md`
2. Add Phone and Message Body
3. Save file
4. Wait 30 seconds
5. Check Done folder

---

### Example 3: Post LinkedIn Update

**Via Dashboard:**
1. Open http://localhost:8001
2. Click "Post to LinkedIn"
3. Fill:
   - Content: 🚀 Exciting news! ...
   - Add hashtags
4. Click "Publish Post"
5. Browser opens and posts
6. Success notification appears

**Via Approved Folder:**
1. Create: `Approved/LinkedIn/announcement.md`
2. Add post content after ---
3. Save file
4. Wait 30 seconds
5. Check Done folder

---

## 🎓 BEST PRACTICES

### Email:
- ✅ Use clear subject lines
- ✅ Keep messages concise
- ✅ Test with your email first
- ✅ Check spam folder if not received

### WhatsApp:
- ✅ Include country code
- ✅ Keep messages under 500 chars
- ✅ First time: Stay on page during QR scan
- ✅ Don't close browser while sending

### LinkedIn:
- ✅ Use engaging opening line
- ✅ Add 3-5 relevant hashtags
- ✅ Keep under 1000 characters
- ✅ First time: Complete full login flow

### General:
- ✅ Hard refresh after updates (Ctrl+Shift+R)
- ✅ Check activity feed for confirmation
- ✅ Review logs if errors occur
- ✅ Keep sessions saved (don't delete folders)

---

## 📞 SUPPORT

### If Buttons Still Don't Work:

1. **Clear all cache:**
   - Press Ctrl+Shift+Delete
   - Clear "Cached images and files"
   - Close and reopen browser

2. **Try different browser:**
   - Chrome
   - Edge
   - Firefox

3. **Use test pages:**
   - http://localhost:8001/quick_test.html
   - http://localhost:8001/activity_test.html

4. **Check server logs:**
   - Look at terminal where dashboard_api.py runs
   - Shows detailed error messages

5. **Verify server running:**
   ```bash
   python -c "import requests; print(requests.get('http://localhost:8001/api/v1/health').json())"
   ```

---

**Status:** ✅ READY  
**Dashboard:** http://localhost:8001  
**Version:** 1.0  

**Start using your dashboard now!** 🚀

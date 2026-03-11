# 🥈 Silver Tier - AI Employee v0.2

**Version:** 0.2 Silver
**Status:** ✅ Complete
**Last Updated:** 2026-03-06

---

## 📋 Overview

Silver Tier extends Bronze Tier with **multi-channel communication** capabilities including Email, LinkedIn, and WhatsApp automation, all with **Human-in-the-Loop (HITL) approval workflow**.

### What Silver Tier Adds to Bronze

- ✅ **Email MCP** - Send emails via SMTP with app password
- ✅ **LinkedIn MCP** - Auto-post to LinkedIn via Playwright
- ✅ **WhatsApp MCP** - Send WhatsApp messages (HITL required)
- ✅ **HITL Approval** - Human review for sensitive actions
- ✅ **Gmail Watcher** - Monitor Gmail for new messages
- ✅ **Scheduler** - Daily briefings at 8 AM

### What Silver Tier Does NOT Do

- ❌ Facebook/Instagram posting (requires Gold)
- ❌ Twitter/X posting (requires Gold)
- ❌ Autonomous multi-step loops (requires Gold)
- ❌ Cross-domain routing (requires Gold)
- ❌ Weekly CEO briefings (requires Gold)
- ❌ Advanced error recovery (requires Gold)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SILVER TIER ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   USER INTERFACE                          │   │
│  │  • Drop task files in Inbox/                              │   │
│  │  • Review approvals in Pending_Approval/                  │   │
│  │  • View status in Dashboard.md                            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  WATCHERS LAYER                           │   │
│  │  ┌─────────────────┐  ┌─────────────────┐                │   │
│  │  │  Filesystem     │  │     Gmail       │                │   │
│  │  │    Watcher      │  │    Watcher      │                │   │
│  │  └─────────────────┘  └─────────────────┘                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│                            ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  ORCHESTRATOR                             │   │
│  │  • Coordinates all MCP tools                              │   │
│  │  • Manages HITL workflow                                  │   │
│  │  • Schedules daily briefings                              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            │                                      │
│              ┌─────────────┼─────────────┐                        │
│              ▼             ▼             ▼                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Email MCP  │  │  LinkedIn    │  │  WhatsApp    │           │
│  │   (SMTP)     │  │    MCP       │  │    MCP       │           │
│  │              │  │ (Playwright) │  │ (Playwright) │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              AI_EMPLOYEE_VAULT                            │   │
│  │  Inbox/ → Needs_Action/ → Plans/ → Approved/ → Done/      │   │
│  │                              ↑                            │   │
│  │                       Pending_Approval/ (HITL)            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure

```
Silver Tire/
├── AI_Employee_Vault/             # Main working directory
│   ├── Inbox/                     # Drop new tasks here
│   │   └── TASK_*.md              # New task files
│   ├── Needs_Action/              # Tasks being processed
│   │   └── TASK_*.md              # Active tasks
│   ├── Plans/                     # Generated action plans
│   │   └── PLAN_*.md              # Plan files
│   ├── Pending_Approval/          # Awaiting human review
│   │   ├── HITL_*.md              # Approval requests
│   │   └── ERROR_ALERT_*.md       # Error alerts
│   ├── Approved/                  # Human-approved actions
│   │   ├── Email/                 # Ready to send
│   │   ├── LinkedIn/              # Ready to post
│   │   └── WhatsApp/              # Ready to send
│   ├── Rejected/                  # Rejected requests
│   │   └── TASK_*.md              # Rejected files
│   ├── Done/                      # Completed tasks
│   │   └── TASK_*.md              # Completed task files
│   ├── Logs/                      # Activity logs
│   │   └── activity_*.md          # Log entries
│   ├── linkedin_session/          # LinkedIn session storage
│   │   └── *.json                 # Session files
│   └── whatsapp_session/          # WhatsApp session storage
│       └── *.json                 # Session files
│
├── mcp/                           # MCP tools (Silver)
│   ├── email_mcp.py               # Email sender
│   ├── linkedin_post.py           # LinkedIn automation
│   └── whatsapp_mcp.py            # WhatsApp automation
│
├── watchers/                      # Event watchers
│   ├── filesystem_watcher.py      # Inbox monitor
│   └── gmail_watcher.py           # Gmail API monitor
│
├── orchestrator.py                # Main coordinator
├── scheduler.py                   # Task scheduler
├── README.md                      # This file
└── SILVER_TIRE_STATUS.md          # Status report
```

---

## 🔗 Tier Relationships

### Inherits from Bronze Tier

| Bronze Feature | Silver Usage |
|----------------|--------------|
| ✅ Filesystem Watcher | Used for inbox monitoring |
| ✅ Plan Generation | Extended with MCP actions |
| ✅ Dashboard | Enhanced with MCP stats |
| ✅ Task Tracking | Extended with approval states |
| ✅ Basic Orchestrator | Extended with MCP coordination |

### What Gold Tier Adds on Top of Silver

| Silver Feature | Gold Enhancement |
|----------------|------------------|
| Email MCP | ✅ Inherited + Enhanced |
| LinkedIn MCP | ✅ Inherited + Auto-post |
| WhatsApp MCP | ✅ Inherited + Auto-send |
| HITL Approval | ✅ Inherited + Smarter routing |
| Gmail Watcher | ✅ Inherited + Auto-processing |
| **NEW in Gold** | **Description** |
| Ralph Wiggum Loop | Autonomous multi-step execution |
| Cross-Domain Routing | Personal/Business separation |
| Facebook/Instagram MCP | Additional social platforms |
| Twitter/X MCP | Twitter integration |
| Weekly CEO Briefing | Automated executive reports |
| Error Recovery MCP | Exponential backoff & degradation |
| Audit Logging | Comprehensive JSON audit trail |

---

## 🚀 How to Use

### Step 1: Start the Orchestrator

```bash
cd "D:\Hackathon 0\Silver Tire"
python orchestrator.py
```

### Step 2: Configure Credentials

Edit `AI_Employee_Vault/credential.json`:

```json
{
  "email": "your-email@gmail.com",
  "email_app_password": "your-app-password",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587
}
```

### Step 3: Authenticate Sessions

**First-time LinkedIn login:**
```bash
python mcp/linkedin_post.py
# Browser opens - login manually
# Session saved automatically
```

**First-time WhatsApp login:**
```bash
python mcp/whatsapp_mcp.py
# QR code displayed - scan with WhatsApp
# Session saved automatically
```

### Step 4: Create Tasks

**Send Email:**
1. Create file in `Pending_Approval/`:
```markdown
---
type: email_request
to: client@example.com
subject: Meeting Reminder
priority: Medium
---

## Message

Hi, this is a reminder about our meeting tomorrow at 2 PM.

Best regards,
Your Name
```

2. Human reviews and moves to `Approved/Email/`
3. Orchestrator sends automatically

**Post to LinkedIn:**
1. Create file in `Pending_Approval/`:
```markdown
---
type: linkedin_post
priority: Low
---

## Post Content

🚀 Excited to announce our new AI automation system!

#AI #Automation #Innovation
```

2. Human reviews and moves to `Approved/LinkedIn/`
3. Orchestrator posts automatically

**Send WhatsApp:**
1. Create file in `Pending_Approval/`:
```markdown
---
type: whatsapp_request
phone: +923001234567
priority: High
---

## Message

Hello! This is a test message.
```

2. Human reviews and moves to `Approved/WhatsApp/`
3. Orchestrator sends automatically

---

## 📊 Workflow States

```
┌──────────┐     ┌──────────────┐     ┌───────────┐
│  Inbox/  │ ──► │ Needs_Action/│ ──► │  Plans/   │
└──────────┘     └──────────────┘     └───────────┘
                                            │
                                            ▼
                                    ┌────────────────┐
                                    │ Pending_Approval│ ← HITL
                                    └────────────────┘
                                            │
                          ┌─────────────────┼─────────────────┐
                          ▼                 ▼                 ▼
                   ┌──────────┐      ┌──────────┐      ┌──────────┐
                   │ Approved/ │      │ Rejected/│      │  Done/   │
                   │  Email/   │      │          │      │          │
                   │ LinkedIn/ │      │          │      │          │
                   │ WhatsApp/ │      │          │      │          │
                   └──────────┘      └──────────┘      └──────────┘
```

---

## 🔧 Configuration

### Email Setup

**Generate Gmail App Password:**

1. Go to [Google Account](https://myaccount.google.com/) → Security
2. Enable 2-Factor Authentication
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Generate password for "Mail"
5. Copy 16-character password to `credential.json`

**SMTP Settings:**
```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "use_tls": true
}
```

### LinkedIn Setup

- Session stored in `linkedin_session/`
- To re-authenticate: delete session folder and re-run
- Uses Playwright with Chromium

### WhatsApp Setup

- Session stored in `whatsapp_session/`
- To re-authenticate: delete session folder and re-run
- Uses Playwright with WhatsApp Web

---

## 🛡️ Safety Rules

### Approval Requirements

| Action | Approval Required | Reason |
|--------|-------------------|--------|
| Email to new contact | ✅ Yes | Prevent spam |
| Email > $100 value | ✅ Yes | Financial safety |
| WhatsApp message | ✅ Always | HITL mandatory |
| LinkedIn post | ⚠️ Context-based | Sensitive topics |
| System config change | ✅ Yes | Security |

### Rate Limiting

| Channel | Limit | Enforcement |
|---------|-------|-------------|
| Email | 50/hour | Orchestrator |
| LinkedIn | 10 posts/day | MCP tool |
| WhatsApp | 20/hour | MCP tool |

---

## 📝 File Templates

### Email Request Template

```markdown
---
type: email_request
to: recipient@example.com
subject: Email Subject
priority: [Low|Medium|High|Critical]
---

## Message Body

[Email content here]

---
## Metadata
- **Created:** YYYY-MM-DD HH:MM
- **Domain:** [Personal|Business]
- **Requires Approval:** Yes
```

### LinkedIn Post Template

```markdown
---
type: linkedin_post
priority: [Low|Medium|High]
hashtags: [#AI, #Automation]
---

## Post Content

[LinkedIn post content here]

---
## Metadata
- **Created:** YYYY-MM-DD HH:MM
- **Domain:** [Personal|Business]
- **Requires Approval:** Yes
```

### WhatsApp Request Template

```markdown
---
type: whatsapp_request
phone: +923001234567
priority: [Low|Medium|High|Critical]
---

## Message

[WhatsApp message content here]

---
## Metadata
- **Created:** YYYY-MM-DD HH:MM
- **Domain:** [Personal|Business]
- **Requires Approval:** Always
```

---

## 🧪 Testing

### Test Email

```bash
# Create test file
echo "Test email" > AI_Employee_Vault/Pending_Approval/TEST_EMAIL.md

# Move to approved after review
move AI_Employee_Vault/Pending_Approval/TEST_EMAIL.md AI_Employee_Vault/Approved/Email/
```

### Test LinkedIn Post

```bash
# Create test file
echo "Test post" > AI_Employee_Vault/Pending_Approval/TEST_LINKEDIN.md

# Move to approved after review
move AI_Employee_Vault/Pending_Approval/TEST_LINKEDIN.md AI_Employee_Vault/Approved/LinkedIn/
```

### Verify Sessions

```bash
# Check LinkedIn session
dir linkedin_session\

# Check WhatsApp session
dir whatsapp_session\
```

---

## 🛠️ Troubleshooting

### Email Not Sending

**Problem:** Authentication failed

**Solution:**
1. Verify app password in `credential.json`
2. Ensure 2FA is enabled
3. Check SMTP settings

### LinkedIn Login Issues

**Problem:** Session expired

**Solution:**
1. Delete `linkedin_session/` folder
2. Re-run MCP to re-authenticate
3. Check browser automation

### WhatsApp QR Not Showing

**Problem:** Session corrupted

**Solution:**
1. Delete `whatsapp_session/` folder
2. Re-run MCP to show QR code
3. Scan with WhatsApp mobile app

### Orchestrator Not Processing

**Problem:** Files stuck in Pending_Approval

**Solution:**
1. Manually review and move to Approved/
2. Check orchestrator is running
3. Review logs for errors

---

## 📈 Dashboard

The Dashboard.md shows:

```markdown
# AI Employee Dashboard - Silver Tier

## Status
- **Tier:** Silver (v0.2)
- **Status:** Running
- **Last Update:** 2026-03-06 12:00:00

## MCP Tools
| Tool | Status | Sessions |
|------|--------|----------|
| Email | ✅ Ready | N/A |
| LinkedIn | ✅ Ready | 17 files |
| WhatsApp | ✅ Ready | 17 files |

## Task Counts
| Status | Count |
|--------|-------|
| Inbox | 0 |
| Needs Action | 0 |
| Pending Approval | 0 |
| Approved | 0 |
| Done | 3 |

## Recent Activity
- [Timestamp] LinkedIn post published
- [Timestamp] Email sent
- [Timestamp] WhatsApp message sent
```

---

## 🎯 When to Use Silver Tier

### Good Use Cases

- ✅ Sending automated emails
- ✅ Posting to LinkedIn regularly
- ✅ Sending WhatsApp notifications
- ✅ Human-in-the-loop workflows
- ✅ Daily automated briefings
- ✅ Gmail monitoring

### Not Recommended For

- ❌ Facebook/Instagram posting (use Gold)
- ❌ Twitter/X posting (use Gold)
- ❌ Autonomous multi-step tasks (use Gold)
- ❌ Cross-domain management (use Gold)
- ❌ Weekly CEO briefings (use Gold)

---

## 📚 Related Documentation

| Document | Purpose | Location |
|----------|---------|----------|
| Tier Architecture | All tiers overview | `../TIER_README.md` |
| Bronze Tier | Foundation features | `../Bronze Tire/README.md` |
| Gold Tier | Full autonomous AI | `../Gold Tire/README.md` |
| Silver Status | Completion report | `SILVER_TIRE_STATUS.md` |
| System Summary | Complete system docs | `../COMPLETE_SYSTEM_SUMMARY.md` |

---

## 🖥️ Silver Tier Dashboard

### Modern Web Dashboard for Communication Automation

Silver Tier includes a **modern, elegant web dashboard** for monitoring and controlling all communication automation.

#### Dashboard Features

- 📊 **Real-Time Metrics** - Emails sent, WhatsApp messages, LinkedIn posts
- 🔗 **Platform Status** - Connection status for Gmail, WhatsApp, LinkedIn
- 📝 **Activity Feed** - Recent actions with timestamps and status
- ⚡ **Quick Actions** - One-click email, WhatsApp, LinkedIn posting
- 🔔 **Notifications** - Success/error toast notifications
- 🔄 **Auto-Refresh** - Dashboard updates every 30 seconds

#### Quick Start Dashboard

1. **Start Dashboard:**
   ```bash
   cd "Silver Tire"
   python dashboard_api.py
   # Or double-click: start_dashboard.bat
   ```

2. **Open Browser:**
   ```
   http://localhost:8001
   ```

3. **Use Features:**
   - **Email:** Enter recipient, subject, message → Click "Send Email"
   - **WhatsApp:** Enter phone, message → Click "Send WhatsApp"
   - **LinkedIn:** Enter post content → Click "Post to LinkedIn"
   - **Messaging:** Enter connection, message → Click "Send Message"

#### Dashboard Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main dashboard UI |
| `/api/v1/health` | GET | Health check |
| `/api/v1/metrics` | GET | Get metrics |
| `/api/v1/activity` | GET | Recent activity |
| `/api/v1/test/email` | POST | Send email |
| `/api/v1/test/whatsapp` | POST | Send WhatsApp |
| `/api/v1/test/linkedin` | POST | Post to LinkedIn |
| `/api/v1/linkedin/message` | POST | Send LinkedIn message |

#### Dashboard Files

```
Silver Tire/dashboard/
├── index.html              # Main dashboard UI
├── working.html            # Working dashboard
├── linkedin-login.html     # LinkedIn login helper
├── linkedin-test.html      # LinkedIn test page
└── static/
    ├── css/
    │   └── styles.css      # Dashboard styling
    └── js/
        └── app.js          # Dashboard logic
```

#### API Files

- `dashboard_api.py` - Main dashboard API server
- `working_dashboard_api.py` - Working API version
- `simple_linkedin_api.py` - Simple LinkedIn API

#### Documentation

- `README_DASHBOARD.md` - Complete dashboard guide
- `USER_GUIDE.md` - User manual
- `QUICK_START.md` - Quick reference
- `DASHBOARD_TROUBLESHOOTING.md` - Troubleshooting

---

## 🔄 Upgrade to Gold Tier

To upgrade from Silver to Gold:

1. **Copy working directory:**
   ```bash
   xcopy "AI_Employee_Vault" "..\Gold Tire\AI_Employee_Vault" /E /I
   ```

2. **Add Gold folders:**
   ```bash
   mkdir "AI_Employee_Vault\Needs_Action\Personal"
   mkdir "AI_Employee_Vault\Needs_Action\Business"
   mkdir "AI_Employee_Vault\facebook_session"
   mkdir "AI_Employee_Vault\twitter_session"
   ```

3. **Start Ralph Wiggum loop:**
   ```bash
   cd ..\Gold Tire
   python ..\Ralph_Wiggum\orchestrator.py --domain Business
   ```

---

## 📞 Support

For issues or questions:

1. Check logs in `AI_Employee_Vault/Logs/`
2. Review session folders
3. Check `../TIER_README.md` for tier architecture
4. Review main documentation in root folder

---

**Silver Tier Status:** ✅ Complete and Production Ready

**Previous Tier:** [🥉 Bronze Tier](../Bronze%20Tire/README.md) - Foundation

**Next Tier:** [🥇 Gold Tier](../Gold%20Tire/README.md) - Full Autonomy

---

*Built by Suleman AI Employee - Silver Tier Communication*

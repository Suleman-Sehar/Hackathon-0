# Tier Linking Guide - Bronze, Silver, Gold

**Version:** 1.0  
**Date:** 2026-03-06  
**Status:** ✅ Fixed Authentication & Path Resolution

---

## 📚 Overview

This document explains how the three tiers (Bronze, Silver, Gold) are **separate but linked** to maintain continuity across the AI Employee system.

---

## 🔗 Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ROOT (D:\Hackathon 0)                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  MCP/ (Shared MCP Tools - ALL TIERS)                  │  │
│  │  ├── social/social_mcp.py (Gold - FB/IG/Twitter)      │  │
│  │  ├── email_mcp.py (Silver+ - Email)                   │  │
│  │  ├── linkedin_post.py (Silver+ - LinkedIn)            │  │
│  │  └── whatsapp_mcp.py (Silver+ - WhatsApp)             │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │  Bronze Tire/  │  │  Silver Tire/  │  │  Gold Tire/  │  │
│  │  (Basic)       │  │  (Communicate) │  │  (Autonomous)│  │
│  └────────────────┘  └────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure

### Root Level (Shared)

**Location:** `D:\Hackathon 0\`

| Directory | Purpose | Used By |
|-----------|---------|---------|
| `MCP/` | Core MCP tools | All tiers |
| `MCP/social/` | Social media MCP (FB/IG/Twitter) | Gold only |
| `MCP/briefing/` | CEO briefing generator | Gold only |
| `MCP/error_recovery/` | Error recovery MCP | Gold only |
| `agents/` | Multi-agent system | Gold only |
| `Ralph_Wiggum/` | Autonomous loop | Gold only |
| `*_session/` | Browser session storage | All tiers |
| `Logs/` | System-wide audit logs | All tiers |
| `credential.json` | Credentials (primary) | All tiers |

### Bronze Tier

**Location:** `D:\Hackathon 0\Bronze Tire\`

```
Bronze Tire/
└── AI_Employee_Vault/
    ├── Inbox/           # Drop tasks here
    ├── Needs_Action/    # Pending tasks
    ├── Plans/           # Generated plans
    ├── Done/            # Completed work
    └── Logs/            # Activity logs
```

**Features:**
- Basic task tracking
- Filesystem watcher
- Plan generation
- Dashboard logging

**Does NOT have:**
- Email MCP
- LinkedIn MCP
- WhatsApp MCP
- Social media MCP

---

### Silver Tier

**Location:** `D:\Hackathon 0\Silver Tire\`

```
Silver Tire/
├── AI_Employee_Vault/
│   ├── Inbox/
│   ├── Needs_Action/
│   ├── Approved/
│   │   ├── Email/
│   │   ├── LinkedIn/
│   │   └── WhatsApp/
│   ├── Pending_Approval/
│   ├── Rejected/
│   ├── Done/
│   └── Logs/
├── orchestrator.py      # Silver orchestrator
└── scheduler.py         # Task scheduler
```

**Features:**
- ✅ All Bronze features PLUS:
- Email MCP (from root `MCP/`)
- LinkedIn MCP (from root `MCP/`)
- WhatsApp MCP (from root `MCP/`)
- HITL approval workflow
- Gmail watcher

**Does NOT have:**
- Facebook/Instagram/Twitter MCP
- Ralph Wiggum autonomous loop
- Cross-domain routing
- CEO briefings

---

### Gold Tier

**Location:** `D:\Hackathon 0\Gold Tire\`

```
Gold Tire/
├── AI_Employee_Vault/
│   ├── Inbox/
│   ├── Needs_Action/
│   │   ├── Personal/
│   │   └── Business/
│   ├── Approved/
│   │   ├── Email/
│   │   ├── LinkedIn/
│   │   └── WhatsApp/
│   ├── Pending_Approval/
│   │   └── ERROR_ALERT_*.md
│   ├── Rejected/
│   ├── Done/
│   │   ├── Personal/
│   │   └── Business/
│   └── Logs/
├── Ralph_Wiggum/
│   └── orchestrator.py  # Autonomous loop
└── MCP/                 # Gold-specific MCP tools
    ├── social/
    ├── briefing/
    └── error_recovery/
```

**Features:**
- ✅ All Bronze + Silver features PLUS:
- Social media MCP (Facebook, Instagram, Twitter/X)
- Ralph Wiggum autonomous loop
- Cross-domain routing (Personal/Business)
- Weekly CEO briefings
- Error recovery MCP
- Comprehensive audit logging

---

## 🔐 Shared Resources

### MCP Tools

All tiers access MCP tools from the **root `MCP/` directory**:

```bash
# From ANY tier, use relative paths to access MCP tools:

# Email (Silver+, Gold)
python ../MCP/email_mcp.py < input.json

# LinkedIn (Silver+, Gold)
python ../MCP/linkedin_post.py < input.json

# WhatsApp (Silver+, Gold)
python ../MCP/whatsapp_mcp.py

# Social Media (Gold only)
python ../MCP/social/social_mcp.py < input.json

# Briefing (Gold only)
python ../MCP/briefing/briefing_mcp.py < input.json

# Error Recovery (Gold only)
python ../MCP/error_recovery/error_recovery_mcp.py < input.json
```

### Session Storage

All tiers **share session storage** at root level:

| Platform | Session Directory | Used By |
|----------|------------------|---------|
| LinkedIn | `linkedin_session/` | Silver, Gold |
| WhatsApp | `whatsapp_session/` | Silver, Gold |
| Facebook | `facebook_session/` | Gold |
| Instagram | `instagram_session/` | Gold |
| Twitter | `twitter_session/` | Gold |

**Benefits:**
- Login once, use across all tiers
- No duplicate session data
- Centralized session management

### Credentials

Credentials are searched in **multiple locations** (in order):

1. `D:\Hackathon 0\credential.json` (Primary)
2. `D:\Hackathon 0\credentials.json`
3. `D:\Hackathon 0\Bronze Tire\AI_Employee_Vault\credential.json`
4. `D:\Hackathon 0\Silver Tire\credential.json`
5. `D:\Hackathon 0\Gold Tire\AI_Employee_Vault\credential.json`

**First match wins** - this allows tier-specific credentials if needed.

---

## 🚀 How to Use Each Tier

### Bronze Tier - Basic Task Tracking

```bash
cd "D:\Hackathon 0\Bronze Tire"

# Create a task
echo "Test task" > AI_Employee_Vault/Inbox/TASK_001.md

# Run basic orchestrator
python orchestrator.py
```

**When to use:**
- Testing basic workflows
- Learning the system
- Simple plan generation

---

### Silver Tier - Communication Automation

```bash
cd "D:\Hackathon 0\Silver Tire"

# Start Silver orchestrator
python orchestrator.py

# Send email (create file in Approved/Email/)
echo '{"to": "test@example.com", "subject": "Test", "body": "Test body"}' | python ../MCP/email_mcp.py

# Post to LinkedIn
echo '{"platform": "linkedin", "content": "Hello LinkedIn!"}' | python ../MCP/linkedin_post.py

# Send WhatsApp
python ../MCP/whatsapp_mcp.py
```

**When to use:**
- Sending emails automatically
- Posting to LinkedIn
- Sending WhatsApp messages
- Running daily briefings

---

### Gold Tier - Full Autonomous AI Employee

```bash
cd "D:\Hackathon 0\Gold Tire"

# Start Ralph Wiggum autonomous loop
python ../Ralph_Wiggum/orchestrator.py --domain Business

# Post to Facebook
echo '{"action": "post_facebook", "message": "Hello Facebook!"}' | python ../MCP/social/social_mcp.py

# Post to Instagram (requires media)
echo '{"action": "post_instagram", "message": "Check this out!", "media_path": "image.jpg"}' | python ../MCP/social/social_mcp.py

# Post to Twitter
echo '{"action": "post_twitter", "message": "Tweet!"}' | python ../MCP/social/social_mcp.py

# Generate CEO briefing
echo '{"requested_by": "manual"}' | python ../MCP/briefing/briefing_mcp.py
```

**When to use:**
- Full autonomous operation
- Cross-domain tasks (Personal/Business)
- Social media automation (FB/IG/Twitter)
- Weekly CEO briefings
- Error recovery and audit logging

---

## 🔧 Session Management

### Initial Setup (First Time Login)

**For LinkedIn (Silver+):**
```bash
cd "D:\Hackathon 0"
python MCP/linkedin_post.py
# Browser opens - login manually
# Session auto-saves to linkedin_session/
```

**For WhatsApp (Silver+):**
```bash
cd "D:\Hackathon 0"
python MCP/whatsapp_mcp.py
# Browser opens - scan QR code manually
# Session auto-saves to whatsapp_session/
```

**For Facebook/Instagram/Twitter (Gold):**
```bash
cd "D:\Hackathon 0"
python MCP/social/login_helper.py
# Select platform
# Browser opens - login manually
# Session auto-saves to {platform}_session/
```

### Session Verification

All MCP tools now **automatically verify sessions** before use:

1. Check if session folder exists
2. Launch browser with persistent context
3. Navigate to platform
4. Check for logged-in indicators
5. If not logged in, return error (no blocking prompts)

### Session Recovery

If session becomes invalid:

```bash
# Delete old session
rm -rf linkedin_session/

# Re-login
python MCP/linkedin_post.py
```

---

## 📊 Data Flow

### Example: Email from Silver Tier

```
1. User creates file: Silver Tire/AI_Employee_Vault/Approved/Email/email_001.md
2. Silver orchestrator detects file
3. Calls: python ../MCP/email_mcp.py < email_001.md
4. MCP loads credentials from: ../credential.json
5. Sends email via SMTP
6. Moves file to: Silver Tire/AI_Employee_Vault/Done/SENT_email_001.md
7. Logs to: Bronze Tire/AI_Employee_Vault/Dashboard.md
```

### Example: Facebook Post from Gold Tier

```
1. User creates request: Gold Tire/AI_Employee_Vault/Needs_Action/Business/post_001.md
2. Gold orchestrator processes request
3. Calls: python ../MCP/social/social_mcp.py < post_001.json
4. MCP loads session from: ../facebook_session/
5. Verifies session is valid
6. Posts to Facebook
7. Saves updated session
8. Moves file to: Gold Tire/AI_Employee_Vault/Done/Business/SENT_post_001.md
9. Logs to: Logs/audit_YYYY-MM-DD.json
```

---

## 🛠️ Troubleshooting

### Issue: "credential.json not found"

**Solution:**
```bash
# Check if credential.json exists at root
ls D:\Hackathon 0\credential.json

# If not found, create it:
{
  "email": "your-email@gmail.com",
  "email_app_password": "your-app-password",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587
}
```

---

### Issue: "Not logged in" errors

**Solution:**
```bash
# For LinkedIn
cd "D:\Hackathon 0"
rm -rf linkedin_session/
python MCP/linkedin_post.py  # Login manually

# For WhatsApp
cd "D:\Hackathon 0"
rm -rf whatsapp_session/
python MCP/whatsapp_mcp.py  # Scan QR manually

# For Facebook/Instagram/Twitter
cd "D:\Hackathon 0"
rm -rf facebook_session/  # or instagram_session/, twitter_session/
python MCP/social/login_helper.py  # Login manually
```

---

### Issue: MCP tools not found

**Solution:**
```bash
# Always use relative paths from tier directory
cd "Silver Tire"
python ../MCP/email_mcp.py  # ✅ Correct
python MCP/email_mcp.py     # ❌ Wrong (looks in Silver/mcp/)
```

---

## 📋 Quick Reference

### Path Resolution

All root MCP tools use **absolute paths** based on script location:

```python
# In MCP/email_mcp.py
SCRIPT_DIR = Path(__file__).parent  # MCP/
ROOT_DIR = SCRIPT_DIR.parent  # Root of Hackathon 0
SESSION_DIR = ROOT_DIR  # Sessions at root
CONFIG_PATHS = [ROOT_DIR / "credential.json", ...]  # Multiple fallbacks
```

This ensures MCP tools work **from any tier directory**.

---

### Import Pattern

```python
# Tier orchestrators import from root MCP
import sys
from pathlib import Path

# Add root MCP to path
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR / "MCP"))

# Now import MCP tools
from email_mcp import send_email
from linkedin_post import post_to_linkedin
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] `credential.json` exists at root level
- [ ] All session folders created at root level
- [ ] Can run `python ../MCP/email_mcp.py` from Silver Tire
- [ ] Can run `python ../MCP/linkedin_post.py` from Silver Tire
- [ ] Can run `python ../MCP/social/social_mcp.py` from Gold Tire
- [ ] Sessions persist across tier switches
- [ ] Logs appear in central `Logs/` folder

---

**Status:** ✅ Complete  
**Last Updated:** 2026-03-06  
**Maintainer:** Suleman AI Employee v0.4

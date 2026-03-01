# Silver Tier - AI Employee v0.2

## Overview

Silver Tier extends Bronze with **multi-channel communication** (Email, LinkedIn, WhatsApp), **Human-in-the-Loop (HITL) approval workflow**, and **automated orchestration**.

---

## Features

### ✅ Inherited from Bronze
- Filesystem watcher for inbox monitoring
- Plan generation and task tracking
- Dashboard with real-time stats
- Metadata management

### 🆕 Silver Tier Additions
| Feature | Description | Status |
|---------|-------------|--------|
| **Email MCP** | Send emails via SMTP with app password | ✅ Ready |
| **LinkedIn MCP** | Auto-post to LinkedIn via Playwright | ✅ Ready |
| **WhatsApp MCP** | Send WhatsApp messages (HITL required) | ✅ Ready |
| **HITL Approval** | Human review for sensitive actions | ✅ Active |
| **Orchestrator** | Coordinates all MCP tools | ✅ Running |
| **Scheduler** | Daily briefings at 8 AM | ✅ Configured |

---

## Project Structure

```
Silver Tire/
├── AI_Employee_Vault/
│   ├── Inbox/              # Drop files here
│   ├── Needs_Action/       # Pending items
│   ├── Plans/              # Action plans
│   ├── Approved/           # Human-approved actions
│   │   ├── Email/
│   │   ├── LinkedIn/
│   │   └── WhatsApp/
│   ├── Pending_Approval/   # Awaiting human review
│   ├── Rejected/           # Rejected requests
│   ├── Done/               # Completed work
│   ├── Logs/               # Activity logs
│   ├── scripts/            # Utility scripts
│   ├── Dashboard.md        # Main status
│   ├── Company_Handbook.md # AI guidelines
│   ├── credential.json     # Config (not in git)
│   └── SKILL_*.md          # Agent skills
├── mcp/
│   ├── email_mcp.py        # Email sender
│   ├── linkedin_post.py    # LinkedIn automation
│   └── whatsapp_mcp.py     # WhatsApp automation
├── watchers/
│   ├── filesystem_watcher.py  # Inbox monitor
│   └── gmail_watcher.py       # Gmail API monitor
├── orchestrator.py         # Main coordinator
└── scheduler.py            # Scheduled tasks
```

---

## How to Run

### 1. Start the Orchestrator
```bash
cd "Silver Tire"
python orchestrator.py
```

### 2. Start Watchers (Optional)
```bash
# File watcher
python watchers/filesystem_watcher.py

# Gmail watcher (requires OAuth setup)
python watchers/gmail_watcher.py
```

### 3. Process Workflow
1. **Drop file** in `Inbox/` → Auto-moves to `Needs_Action/`
2. **AI processes** file → Creates plan in `Plans/`
3. **Sensitive actions** → Move to `Pending_Approval/`
4. **Human reviews** → Move to `Approved/` or `Rejected/`
5. **Orchestrator executes** → Moves to `Done/`

---

## Configuration

### Email Setup
Edit `AI_Employee_Vault/credential.json`:
```json
{
  "email": "your-email@gmail.com",
  "email_app_password": "your-app-password",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587
}
```

**Generate Gmail App Password:**
1. Go to Google Account → Security
2. Enable 2-Factor Authentication
3. Generate App Password for "Mail"
4. Copy 16-character password to `credential.json`

### LinkedIn Setup
- First run will open browser for manual login
- Session saved in `linkedin_session/`
- Subsequent runs auto-login

### WhatsApp Setup
- First run shows QR code for scanning
- Session saved in `whatsapp_session/`
- **HITL required** for all messages

---

## Agent Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| `SKILL_GmailWatcher` | Monitor Gmail for new messages | Auto/Manual |
| `SKILL_HumanApproval` | Route actions to human review | Auto (sensitive) |
| `SKILL_SendEmailMCP` | Send approved emails | Approved folder |
| `SKILL_LinkedInAutoPost` | Post to LinkedIn | Approved folder |
| `SKILL_WhatsAppMCP` | Send WhatsApp messages | Approved folder |
| `SKILL_MetadataManager` | Track file metadata | Auto |

---

## Approval Workflow

### High-Risk Actions (Require Approval)
- Emails to new contacts
- Emails with monetary value > $100
- WhatsApp messages (always)
- LinkedIn posts on sensitive topics
- System configuration changes

### Approval Process
1. AI creates file in `Pending_Approval/`
2. Human reviews content
3. Human moves file to:
   - `Approved/` → Action executes
   - `Rejected/` → Request cancelled

---

## Safety Rules

| Channel | Rule | Enforcement |
|---------|------|-------------|
| Email | New contacts need approval | Auto-flag |
| WhatsApp | ALL messages need approval | HITL mandatory |
| LinkedIn | Sensitive topics need approval | Content analysis |
| All | Max 10 messages/hour | Rate limiting |

---

## Logs & Monitoring

### Dashboard
- Real-time stats in `AI_Employee_Vault/Dashboard.md`
- Updated after every action

### Activity Logs
- Daily logs in `Logs/YYYY-MM-DD.md`
- Searchable via metadata manager

### Metadata Stats
```bash
python AI_Employee_Vault/scripts/util_metadata-manager_v1.0.py --stats
```

---

## Troubleshooting

### Email Not Sending
- Check `credential.json` has valid app password
- Verify 2FA enabled on Gmail account
- Check SMTP server settings

### LinkedIn Login Issues
- Delete `linkedin_session/` folder
- Re-run to re-authenticate

### WhatsApp QR Not Showing
- Delete `whatsapp_session/` folder
- Re-run to show QR code

### Orchestrator Not Running
- Check Python 3.8+ installed
- Install dependencies: `pip install playwright schedule`
- Run `playwright install chromium`

---

## Current Status

- **Version:** 0.2 Silver
- **Orchestrator:** Running
- **Watchers:** 2 active (File, Gmail)
- **MCP Tools:** 3 ready (Email, LinkedIn, WhatsApp)
- **HITL:** Active

---

## Next Tier: Gold

Gold Tier adds:
- Voice call integration
- Advanced analytics
- Multi-agent coordination
- Custom API integrations

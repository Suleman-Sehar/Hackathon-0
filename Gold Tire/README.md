# 🥇 Gold Tier - Autonomous AI Employee v0.3

**Version:** 0.3 Gold
**Status:** ✅ Production Ready
**Last Updated:** 2026-03-06
**Author:** Suleman AI Employee v0.3

---

## 📋 Overview

Gold Tier is the **complete autonomous AI employee** system. It includes all Silver Tier features plus autonomous execution, cross-domain routing, multi-platform social media automation, and automated CEO briefings.

### What Gold Tier Adds to Silver

- ✅ **Ralph Wiggum Autonomous Loop** - Multi-step task execution without supervision
- ✅ **Cross-Domain Routing** - Separate Personal and Business task handling
- ✅ **Social Media MCP** - Facebook, Instagram, and Twitter/X posting
- ✅ **Weekly CEO Briefing** - Automated executive reports every Sunday
- ✅ **Error Recovery MCP** - Exponential backoff and graceful degradation
- ✅ **Comprehensive Audit Logging** - JSON audit trail for all actions
- ✅ **Error Alert System** - HITL alerts for critical failures

### Gold Tier Capabilities

| Capability | Description |
|------------|-------------|
| **Autonomous Execution** | Ralph Wiggum loop handles multi-step tasks independently |
| **Cross-Domain** | Personal and Business tasks kept separate |
| **Social Media** | Facebook, Instagram, Twitter/X automated posting |
| **Executive Reports** | Weekly CEO briefings with revenue, expenses, bottlenecks |
| **Error Recovery** | Automatic retry with exponential backoff |
| **Audit Trail** | Every action logged to JSON for compliance |

---

## 🏗️ Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        GOLD TIER ARCHITECTURE                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │                         USER / CEO INTERFACE                            ║
║  │   • Natural Language Commands                                           ║
║  │   • HITL Approval Requests                                              ║
║  │   • Weekly CEO Briefings                                                ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║                                    │                                         ║
║                                    ▼                                         ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │                      ORCHESTRATION LAYER                                ║
║  │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐ ║
║  │   │  Ralph Wiggum   │  │   Cross-Domain  │  │    Task Scheduler       ║
║  │   │  Autonomous     │  │     Router      │  │   (Sunday 11 PM)        ║
║  │   │      Loop       │  │  (Personal/     │  │                         ║
║  │   │                 │  │   Business)     │  │                         ║
║  │   └─────────────────┘  └─────────────────┘  └─────────────────────────┘ ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║                                    │                                         ║
║                                    ▼                                         ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │                        MCP SERVER LAYER                                 ║
║  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────┐ ║
║  │   │   Social     │  │   Briefing   │  │     Error Recovery           ║
║  │   │     MCP      │  │     MCP      │  │          MCP                 ║
║  │   │  (FB/IG/X)   │  │  (CEO Reports│  │  (Retry + Degradation)       ║
║  │   │              │  │   + Dashboard│  │                              │ ║
║  │   └──────────────┘  └──────────────┘  └──────────────────────────────┘ ║
║  └─────────────────────────────────────────────────────────────────────────┘ ║
║                                    │                                         ║
║                                    ▼                                         ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │                      DATA & PERSISTENCE LAYER                           ║
║  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────┐ ║
║  │   │   Session    │  │   Audit      │  │      Task Storage            ║
║  │   │   Storage    │  │    Logs      │  │   (Needs_Action/Done)        ║
║  │   │  (Persistent │  │  (JSONL)     │  │                              ║
║  │   │   Context)   │  │              │  │                              ║
║  │   └──────────────┘  └──────────────┘  └──────────────────────────────┘ ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 📁 Directory Structure

```
Gold Tire/
├── AI_Employee_Vault/             # Main working directory
│   ├── Inbox/                     # Drop new tasks here
│   │   └── TASK_*.md              # New task files
│   ├── Needs_Action/              # Tasks being processed
│   │   ├── Personal/              # Personal domain tasks
│   │   │   └── TASK_*.md
│   │   └── Business/              # Business domain tasks
│   │       └── TASK_*.md
│   ├── Plans/                     # Generated action plans
│   │   ├── Personal/
│   │   └── Business/
│   ├── Pending_Approval/          # Awaiting human review
│   │   ├── HITL_*.md              # Approval requests
│   │   └── ERROR_ALERT_*.md       # Error alerts
│   ├── Approved/                  # Human-approved actions
│   │   ├── Email/
│   │   ├── LinkedIn/
│   │   └── WhatsApp/
│   ├── Rejected/                  # Rejected requests
│   │   └── TASK_*.md
│   ├── Done/                      # Completed tasks
│   │   ├── Personal/              # Personal completed
│   │   └── Business/              # Business completed
│   ├── Logs/                      # Activity logs
│   │   └── activity_*.md
│   ├── linkedin_session/          # LinkedIn session storage
│   ├── whatsapp_session/          # WhatsApp session storage
│   ├── facebook_session/          # Facebook session storage
│   └── twitter_session/           # Twitter session storage
│
├── mcp/                           # MCP tools (Gold - uses shared)
│   └── (links to ../MCP/)
│
└── README.md                      # This file
```

### Shared Resources (Root Level)

```
D:\Hackathon 0\
├── MCP/                           # Core MCP servers (Shared)
│   ├── social/
│   │   └── social_mcp.py          # FB/IG/X posting
│   ├── briefing/
│   │   └── briefing_mcp.py        # CEO briefing generator
│   └── error_recovery/
│       └── error_recovery_mcp.py  # Retry & degradation
│
├── Ralph_Wiggum/                  # Autonomous loop (Shared)
│   ├── orchestrator.py            # Ralph Wiggum orchestrator
│   ├── loop_state/                # Loop state storage
│   └── logs/                      # Loop logs
│
├── Briefings/                     # Weekly CEO reports (Shared)
│   └── CEO_Briefing_*.md
│
├── Logs/                          # System-wide audit logs (Shared)
│   └── audit_YYYY-MM-DD.json
│
├── SKILL_*.md                     # Agent skill documentation (Shared)
└── Dashboard.md                   # System-wide dashboard (Shared)
```

---

## 🔗 Tier Relationships

### Inherits from Bronze & Silver Tiers

| Tier | Features Inherited by Gold |
|------|---------------------------|
| **Bronze** | ✅ Filesystem Watcher<br>✅ Plan Generation<br>✅ Dashboard<br>✅ Task Tracking |
| **Silver** | ✅ Email MCP<br>✅ LinkedIn MCP<br>✅ WhatsApp MCP<br>✅ HITL Approval<br>✅ Gmail Watcher |

### Gold-Exclusive Features

| Feature | Description | Shared Location |
|---------|-------------|-----------------|
| **Ralph Wiggum Loop** | Autonomous multi-step execution | `../Ralph_Wiggum/` |
| **Cross-Domain Routing** | Personal/Business separation | `SKILL_CrossDomainRouter.md` |
| **Social MCP** | Facebook, Instagram, Twitter | `../MCP/social/` |
| **Briefing MCP** | Weekly CEO reports | `../MCP/briefing/` |
| **Error Recovery MCP** | Exponential backoff | `../MCP/error_recovery/` |
| **Audit Logging** | Comprehensive JSON logs | `../Logs/` |

---

## 🚀 How to Use

### Step 1: Start Ralph Wiggum Autonomous Loop

```bash
cd "D:\Hackathon 0"

# Process all Business domain tasks continuously
python Ralph_Wiggum\orchestrator.py --domain Business --continuous

# Or process Personal domain
python Ralph_Wiggum\orchestrator.py --domain Personal

# Or process a specific task file
python Ralph_Wiggum\orchestrator.py Needs_Action\Business\TASK_NAME.md
```

### Step 2: Start MCP Servers (As Needed)

**Social Media MCP (Facebook/Instagram/Twitter):**
```bash
echo '{"action": "post_facebook", "message": "Hello!", "domain": "Business"}' | python MCP\social\social_mcp.py
```

**Briefing MCP (CEO Reports):**
```bash
echo '{"requested_by": "manual"}' | python MCP\briefing\briefing_mcp.py
```

**Error Recovery MCP:**
```bash
echo '{"action_type": "retry_with_backoff", "params": {}, "max_retries": 3}' | python MCP\error_recovery\error_recovery_mcp.py
```

### Step 3: Configure Social Sessions

**First-time Facebook login:**
```bash
python MCP\social\login_simple.py facebook
# Browser opens - login manually
# Session saved to facebook_session/
```

**First-time Instagram login:**
```bash
python MCP\social\login_simple.py instagram
# Browser opens - login manually
# Session saved to instagram_session/
```

**First-time Twitter login:**
```bash
python MCP\social\login_simple.py twitter
# Browser opens - login manually
# Session saved to twitter_session/
```

### Step 4: Create Cross-Domain Tasks

**Business Task:**
Create file in `AI_Employee_Vault/Needs_Action/Business/`:
```markdown
---
type: social_post
domain: Business
platforms: [facebook, linkedin, twitter]
priority: High
---

## Content

🚀 Excited to announce our new AI automation platform!

#AI #Automation #Business
```

**Personal Task:**
Create file in `AI_Employee_Vault/Needs_Action/Personal/`:
```markdown
---
type: social_post
domain: Personal
platforms: [instagram, facebook]
priority: Low
---

## Content

☕ Weekend vibes!

#Weekend #Personal
```

---

## 📊 Task Flow with Ralph Wiggum Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                    RALPH WIGGUM AUTONOMOUS LOOP                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Fetch task from Needs_Action/{domain}/                      │
│                          │                                       │
│                          ▼                                       │
│  2. Prepare Qwen input with task details                        │
│                          │                                       │
│                          ▼                                       │
│  3. Call Qwen API (file-based or HTTP)                          │
│                          │                                       │
│                          ▼                                       │
│  4. Check completion (TASK_COMPLETE marker)                     │
│                          │                                       │
│              ┌───────────┴───────────┐                          │
│              │                       │                          │
│              ▼                       ▼                          │
│        Not Complete            Complete                         │
│              │                       │                          │
│              │                       ▼                          │
│         Repeat (max 15)    Move to Done/{domain}/               │
│              │                       │                          │
│              └───────────────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 File Templates

### Social Post Request (Cross-Domain)

```markdown
---
type: social_post
domain: [Personal|Business]
platforms: [facebook, instagram, twitter, linkedin]
priority: [Low|Medium|High]
requires_approval: true
---

## Content

[Post content here]

## Hashtags

[#AI, #Automation, #Business]

---
## Metadata
- **Created:** YYYY-MM-DD HH:MM
- **Domain:** [Personal|Business]
- **Platforms:** Facebook, Instagram, Twitter
- **Requires Approval:** Yes
```

### CEO Briefing Request

```markdown
---
type: ceo_briefing
domain: Business
period: weekly
requested_by: [Name]
---

## Briefing Requirements

- Revenue analysis
- Expense tracking
- Task completion summary
- Bottleneck identification
- Proactive suggestions

---
## Metadata
- **Created:** YYYY-MM-DD HH:MM
- **Domain:** Business
- **Period:** Weekly
```

### Error Alert Template

```markdown
---
type: error_alert
created: YYYY-MM-DDTHH:MM:SS+05:00
status: [critical|warning|info]
---

## Error Details

- **Action:** [action_name]
- **Error:** [Error message]
- **Domain:** [Personal|Business]
- **Iterations:** [retry count]
- **Max Retries:** 3

## Suggested Action

[Human review required - move to Done/ after review]

---
## Metadata
- **Alert ID:** ERROR_ALERT_YYYYMMDD_HHMMSS
- **Requires Human Review:** Yes
```

---

## 🔧 Configuration

### Ralph Wiggum Loop Settings

Edit `Ralph_Wiggum/orchestrator.py`:

```python
# Maximum iterations per task
MAX_ITERATIONS = 15

# Check interval (seconds)
CHECK_INTERVAL = 10

# State persistence
STATE_DIR = "loop_state"

# Log level
LOG_LEVEL = "INFO"
```

### Social MCP Settings

Edit `MCP/social/social_mcp.py`:

```python
# Session directories
SESSION_DIRS = {
    'facebook': '../facebook_session',
    'instagram': '../instagram_session',
    'twitter': '../twitter_session'
}

# Human-like delays (seconds)
MIN_DELAY = 2
MAX_DELAY = 4
```

### Scheduled CEO Briefing (Windows)

```powershell
# Every Sunday at 11 PM
$action = New-ScheduledTaskAction -Execute "python" `
    -Argument "MCP/briefing/briefing_mcp.py" `
    -WorkingDirectory "D:\Hackathon 0"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 11:00PM
Register-ScheduledTask -TaskName "CEO_Weekly_Briefing" -Action $action -Trigger $trigger
```

---

## 🛡️ Safety Rules

### Approval Requirements

| Action | Approval Required | Reason |
|--------|-------------------|--------|
| Social post (Business) | ✅ Yes | Brand safety |
| Social post (Personal) | ⚠️ Optional | User preference |
| Email > $100 value | ✅ Yes | Financial safety |
| WhatsApp message | ✅ Always | HITL mandatory |
| System config change | ✅ Yes | Security |

### Ralph Wiggum Loop Safety

| Safety Feature | Description |
|----------------|-------------|
| **Max Iterations** | 15 iterations maximum per task |
| **State Persistence** | Survives crashes, resumes from last state |
| **Task Complete Marker** | Clear stopping condition |
| **Error Logging** | Every iteration logged |

### Error Recovery

| Recovery Strategy | Description |
|-------------------|-------------|
| **Exponential Backoff** | 2s → 8s → 32s delays |
| **Max Retries** | 3 retries before alert |
| **Graceful Degradation** | Continue with available services |
| **Human Alert** | ERROR_ALERT for critical failures |

---

## 📈 Audit Logging

All actions are logged to `../Logs/audit_YYYY-MM-DD.json`:

```json
{
    "timestamp": "2026-03-06T12:42:00.000000",
    "action": "social_post",
    "status": "success",
    "domain": "Business",
    "details": {
        "platform": "facebook",
        "session_saved": true,
        "test": "phase2_flow"
    },
    "error": null
}
```

### View Today's Audit Logs

```bash
type Logs\audit_2026-03-04.json
```

### Filter for Errors

```bash
python -c "import json; logs=json.load(open('Logs/audit_2026-03-04.json')); print([l for l in logs if l['status'] in ['error','failed']])"
```

---

## 🧪 Testing

### Test Ralph Wiggum Loop

```bash
# Create test task
echo "Test task" > AI_Employee_Vault/Needs_Action/Business/TEST_001.md

# Start loop
python Ralph_Wiggum\orchestrator.py --domain Business

# Watch task move to Done/Business/
```

### Test Social MCP

```bash
# Test Facebook post
echo '{"action": "post_facebook", "message": "Test!", "domain": "Business"}' | python MCP\social\social_mcp.py

# Check audit log
type Logs\audit_*.json
```

### Test CEO Briefing

```bash
# Generate manual briefing
echo '{"requested_by": "manual"}' | python MCP\briefing\briefing_mcp.py

# Check Briefings/ folder
dir ..\Briefings\
```

---

## 🛠️ Troubleshooting

### Ralph Wiggum Loop Not Processing

**Problem:** Tasks stuck in Needs_Action

**Solution:**
1. Verify task file format is correct
2. Check domain folder (Personal/Business)
3. Review Ralph_Wiggum logs
4. Ensure Qwen is configured

### Social MCP Authentication Failed

**Problem:** Session expired

**Solution:**
1. Delete session folder (e.g., `facebook_session/`)
2. Re-run login: `python MCP\social\login_simple.py facebook`
3. Re-authenticate in browser

### CEO Briefing Not Generating

**Problem:** Briefing MCP fails

**Solution:**
1. Check transactions.csv exists in Accounting/
2. Verify task data in Done/Business/
3. Review briefing MCP logs

### Error Recovery Not Working

**Problem:** Tasks fail without retry

**Solution:**
1. Verify error_recovery_mcp.py is accessible
2. Check max_retries configuration
3. Review audit logs for backoff attempts

---

## 🎯 When to Use Gold Tier

### Good Use Cases

- ✅ Full autonomous AI employee operation
- ✅ Cross-domain task management (Personal/Business)
- ✅ Multi-platform social media automation
- ✅ Weekly automated CEO briefings
- ✅ Robust error recovery requirements
- ✅ Comprehensive audit logging for compliance

### Not Recommended For

- ❌ Simple task tracking (use Bronze)
- ❌ Email/LinkedIn/WhatsApp only (use Silver)
- ❌ Learning the basics (start with Bronze)

---

## 🖥️ Gold Tier Dashboard

### Vibrant Tech Control Center

Gold Tier includes a **stunning, vibrant tech dashboard** with gold/orange theme for complete monitoring and control of your autonomous AI employee.

#### Dashboard Features

- 🎯 **Real-Time Metrics** - Tasks, revenue, social posts, loop iterations
- 🧠 **Ralph Wiggum Status** - Live autonomous loop monitoring
- 📊 **Cross-Domain View** - Personal vs Business task separation
- 📱 **Social Media Grid** - Facebook/Instagram/Twitter status
- 📈 **Revenue Tracking** - Weekly revenue, expenses, profit
- ⚠️ **HITL Alerts** - Active alerts and error recovery
- 📝 **Audit Feed** - Real-time activity visualization
- 🎛️ **Control Panel** - Start/stop loop, trigger briefings

#### Quick Start Dashboard

1. **Start Dashboard:**
   ```bash
   cd "Gold Tire"
   python dashboard_api.py
   ```

2. **Open Browser:**
   ```
   http://localhost:8001
   ```

3. **Monitor & Control:**
   - **Ralph Wiggum:** Start/Stop autonomous loop
   - **Domains:** View Personal/Business tasks
   - **Social:** Post to Facebook/Instagram/Twitter
   - **Alerts:** View and resolve HITL alerts
   - **Briefings:** Generate CEO reports

#### Dashboard Design

**Theme:** Vibrant Gold/Orange Cyberpunk
- **Colors:** Gold gradients, neon orange, cyan accents
- **Fonts:** Orbitron (display), Rajdhani (body)
- **Effects:** Glowing elements, animated particles, cyber grid
- **Animations:** Pulsing status, smooth transitions, number animations

#### Dashboard API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main dashboard UI |
| `/api/v1/health` | GET | Health check |
| `/api/v1/metrics` | GET | All metrics |
| `/api/v1/ralph-wiggum/state` | GET | Loop state |
| `/api/v1/domains` | GET | Domain stats |
| `/api/v1/social/status` | GET | Social media status |
| `/api/v1/activity` | GET | Activity feed |
| `/api/v1/alerts` | GET | Active alerts |
| `/api/v1/ralph-wiggum/control` | POST | Control loop |
| `/api/v1/social/post` | POST | Create post |
| `/api/v1/briefing/trigger` | POST | Trigger briefing |

#### Dashboard Files

```
Gold Tire/dashboard/
├── index.html              # Main dashboard UI
├── static/
│   ├── css/
│   │   └── styles.css      # Vibrant gold/orange theme
│   └── js/
│       └── app.js          # Real-time dashboard logic
└── dashboard_api.py        # Dashboard API server
```

---

## 📚 Related Documentation

| Document | Purpose | Location |
|----------|---------|----------|
| Tier Architecture | All tiers overview | `../TIER_README.md` |
| Bronze Tier | Foundation features | `../Bronze Tire/README.md` |
| Silver Tier | Communication features | `../Silver Tire/README.md` |
| Gold Validation | Validation report | `../Gold_Final_Validation.md` |
| Gold README | Full Gold documentation | `../README_Gold.md` |
| SKILL Files | Agent skill documentation | `../SKILL_*.md` |
| System Summary | Complete system docs | `../COMPLETE_SYSTEM_SUMMARY.md` |

---

## 📞 Support

For issues or questions:

1. Check audit logs in `../Logs/audit_*.json`
2. Review Ralph Wiggum logs in `Ralph_Wiggum/logs/`
3. Check session folders for authentication issues
4. Review `../TIER_README.md` for tier architecture
5. Check main documentation in root folder

---

## 🏆 Gold Tier Status

| Component | Status | Proof |
|-----------|--------|-------|
| Ralph Wiggum Loop | ✅ Tested | `TEST_GOLD_AUTONOMY.md` |
| Cross-Domain Routing | ✅ Tested | `CROSS_DOMAIN_ROUTER_TEST.md` |
| FB/IG/X Integration | ✅ Tested | `TEST_SOCIAL_INTEGRATION_SUMMARY.md` |
| CEO Briefing | ✅ Generated | `CEO_Briefing_TEST_GOLD.md` |
| Error Recovery | ✅ Tested | `ERROR_RECOVERY_TEST.md` |
| Audit Logging | ✅ Verified | `AUDIT_LOGGING_VERIFICATION.md` |

---

**Gold Tier Status:** ✅ 100% Complete, Tested & Production Ready

**Previous Tier:** [🥈 Silver Tier](../Silver%20Tire/README.md) - Communication

**Foundation Tier:** [🥉 Bronze Tier](../Bronze%20Tire/README.md) - Foundation

---

*Built by Suleman AI Employee v0.3 - Gold Tier Autonomous AI*

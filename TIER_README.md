# Hackathon 0 - Tier Architecture

**Version:** 1.0
**Last Updated:** 2026-03-06
**Status:** ✅ Production Ready

---

## 🏗️ Tier Overview

The AI Workforce system is organized into **three progressive tiers**, each building upon the previous one:

```
┌─────────────────────────────────────────────────────────────────┐
│                        TIER ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🥇 GOLD TIER (v0.3)                                     │   │
│  │  • Autonomous AI Employee (Ralph Wiggum Loop)            │   │
│  │  • Cross-Domain Routing (Personal/Business)              │   │
│  │  • Social Media MCP (FB/IG/Twitter)                      │   │
│  │  • Weekly CEO Briefings                                  │   │
│  │  • Error Recovery & Audit Logging                        │   │
│  │  → INHERITS: All Silver features                         │   │
│  │  → LOCATION: /Gold Tire/                                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ▲                                     │
│                            │ INHERITS                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🥈 SILVER TIER (v0.2)                                   │   │
│  │  • Email MCP (SMTP)                                      │   │
│  │  • LinkedIn MCP (Playwright)                             │   │
│  │  • WhatsApp MCP (HITL)                                   │   │
│  │  • HITL Approval Workflow                                │   │
│  │  • Filesystem & Gmail Watchers                           │   │
│  │  → INHERITS: All Bronze features                         │   │
│  │  → LOCATION: /Silver Tire/                               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ▲                                     │
│                            │ INHERITS                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  🥉 BRONZE TIER (v0.1)                                   │   │
│  │  • Filesystem Watcher                                    │   │
│  │  • Plan Generation                                       │   │
│  │  • Dashboard & Logging                                   │   │
│  │  • Basic Task Tracking                                   │   │
│  │  → FOUNDATION TIER                                       │   │
│  │  → LOCATION: /Bronze Tire/                               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure

```
D:\Hackathon 0\
│
├── 🥉 Bronze Tire/                    # Bronze Tier Sandbox
│   ├── AI_Employee_Vault/             # Working directory
│   │   ├── Inbox/                     # Drop files here
│   │   ├── Needs_Action/              # Pending tasks
│   │   ├── Plans/                     # Generated plans
│   │   ├── Done/                      # Completed work
│   │   └── Logs/                      # Activity logs
│   ├── README.md                      # Bronze documentation
│   └── orchestrator.py                # Basic orchestrator
│
├── 🥈 Silver Tire/                    # Silver Tier Sandbox
│   ├── AI_Employee_Vault/             # Working directory
│   │   ├── Inbox/                     # Drop files here
│   │   ├── Needs_Action/              # Pending tasks
│   │   ├── Plans/                     # Generated plans
│   │   ├── Approved/                  # Human-approved actions
│   │   │   ├── Email/
│   │   │   ├── LinkedIn/
│   │   │   └── WhatsApp/
│   │   ├── Pending_Approval/          # Awaiting review
│   │   ├── Rejected/                  # Rejected requests
│   │   ├── Done/                      # Completed work
│   │   ├── Logs/                      # Activity logs
│   │   ├── linkedin_session/          # Session storage
│   │   └── whatsapp_session/          # Session storage
│   ├── mcp/                           # Silver MCP tools
│   │   ├── email_mcp.py               # Email sender
│   │   ├── linkedin_post.py           # LinkedIn automation
│   │   └── whatsapp_mcp.py            # WhatsApp automation
│   ├── watchers/                      # Event watchers
│   │   ├── filesystem_watcher.py      # Inbox monitor
│   │   └── gmail_watcher.py           # Gmail API monitor
│   ├── orchestrator.py                # Silver orchestrator
│   ├── scheduler.py                   # Task scheduler
│   ├── README.md                      # Silver documentation
│   └── SILVER_TIRE_STATUS.md          # Status report
│
├── 🥇 Gold Tire/                      # Gold Tier Sandbox
│   ├── AI_Employee_Vault/             # Working directory
│   │   ├── Inbox/                     # Drop files here
│   │   ├── Needs_Action/              # Pending tasks
│   │   │   ├── Personal/              # Personal domain
│   │   │   └── Business/              # Business domain
│   │   ├── Plans/                     # Generated plans
│   │   ├── Approved/                  # Human-approved actions
│   │   │   ├── Email/
│   │   │   ├── LinkedIn/
│   │   │   └── WhatsApp/
│   │   ├── Pending_Approval/          # Awaiting review
│   │   │   └── ERROR_ALERT_*.md       # Error alerts
│   │   ├── Rejected/                  # Rejected requests
│   │   ├── Done/                      # Completed work
│   │   │   ├── Personal/
│   │   │   └── Business/
│   │   ├── Logs/                      # Activity logs
│   │   ├── linkedin_session/          # Session storage
│   │   ├── whatsapp_session/          # Session storage
│   │   ├── facebook_session/          # Session storage
│   │   └── twitter_session/           # Session storage
│   ├── mcp/                           # Gold MCP tools
│   ├── README.md                      # Gold documentation
│   └── (Gold-specific files)
│
├── 📚 Shared Resources/               # SHARED across all tiers
│   ├── MCP/                           # Core MCP servers
│   │   ├── social/
│   │   │   └── social_mcp.py          # FB/IG/Twitter posting
│   │   ├── briefing/
│   │   │   └── briefing_mcp.py        # CEO briefing generator
│   │   ├── error_recovery/
│   │   │   └── error_recovery_mcp.py  # Retry & degradation
│   │   ├── email_mcp.py               # Email MCP (shared)
│   │   ├── linkedin_post.py           # LinkedIn MCP (shared)
│   │   └── whatsapp_mcp.py            # WhatsApp MCP (shared)
│   │
│   ├── agents/                        # Multi-agent system
│   │   ├── base_agent.py              # Agent base class
│   │   ├── message_bus.py             # Inter-agent communication
│   │   ├── ceo_agent.py               # CEO agent
│   │   ├── operations_agent.py        # Operations agent
│   │   ├── marketing_agent.py         # Marketing agent
│   │   ├── finance_agent.py           # Finance agent
│   │   └── execution_agent.py         # Execution agent
│   │
│   ├── Ralph_Wiggum/                  # Autonomous loop
│   │   ├── orchestrator.py            # Ralph Wiggum orchestrator
│   │   ├── loop_state/                # Loop state storage
│   │   └── logs/                      # Loop logs
│   │
│   ├── memory/                        # Memory management
│   │   └── memory_manager.py          # Two-tier memory
│   │
│   ├── SKILL_*.md                     # Agent skill documentation
│   ├── Dashboard.md                   # System-wide dashboard
│   └── Logs/                          # System-wide audit logs
│       └── audit_YYYY-MM-DD.json
│
├── 🏗️ SaaS Platform/                  # Production backend
│   ├── main.py                        # FastAPI entry point
│   ├── api/                           # REST API routes
│   ├── auth/                          # Authentication
│   ├── database/                      # Database models
│   ├── usage/                         # Usage tracking
│   ├── stripe_module/                 # Stripe integration
│   ├── dashboard/                     # Next.js frontend
│   ├── Dockerfile                     # Docker config
│   └── docker-compose.yml             # Service orchestration
│
└── Documentation/
    ├── README.md                      # Main documentation
    ├── TIER_README.md                 # This file
    ├── ARCHITECTURE_GAP_ANALYSIS.md   # Architecture comparison
    ├── MULTI_AGENT_IMPLEMENTATION.md  # Agent implementation
    ├── COMPLETE_SYSTEM_SUMMARY.md     # Full system summary
    ├── PHASE_1_COMPLETE.md            # Phase 1 report
    ├── PHASE_2_COMPLETE.md            # Phase 2 report
    ├── PHASE_3_COMPLETE.md            # Phase 3 report
    ├── PHASE_4_COMPLETE.md            # Phase 4 report
    ├── SILVER_TIRE_COMPLETE.md        # Silver completion report
    ├── Gold_Final_Validation.md       # Gold validation
    └── Gold_Validation_Report.md      # Gold validation report
```

---

## 🔗 Tier Relationships

### Inheritance Model

| Tier | Inherits From | Adds |
|------|---------------|------|
| **Bronze** | (Foundation) | Basic task tracking, filesystem watcher, plans |
| **Silver** | Bronze + | Email/LinkedIn/WhatsApp MCPs, HITL workflow, watchers |
| **Gold** | Bronze + Silver + | Ralph Wiggum loop, cross-domain, social MCP, CEO briefings, error recovery |

### Shared vs. Tier-Specific

| Component | Bronze | Silver | Gold | Notes |
|-----------|--------|--------|------|-------|
| **Filesystem Watcher** | ✅ | ✅ | ✅ | Shared |
| **Basic Orchestrator** | ✅ | ✅ | ✅ | Tier-specific versions |
| **Email MCP** | ❌ | ✅ | ✅ | Shared implementation |
| **LinkedIn MCP** | ❌ | ✅ | ✅ | Shared implementation |
| **WhatsApp MCP** | ❌ | ✅ | ✅ | Shared implementation |
| **Gmail Watcher** | ❌ | ✅ | ✅ | Shared |
| **Ralph Wiggum Loop** | ❌ | ❌ | ✅ | Gold only |
| **Cross-Domain Routing** | ❌ | ❌ | ✅ | Gold only |
| **Social MCP (FB/IG/X)** | ❌ | ❌ | ✅ | Gold only |
| **Briefing MCP** | ❌ | ❌ | ✅ | Gold only |
| **Error Recovery MCP** | ❌ | ❌ | ✅ | Gold only |
| **Audit Logging** | Basic | Enhanced | Comprehensive | Tier-specific depth |

---

## 🚀 How to Use Each Tier

### 🥉 Bronze Tier - Basic Task Tracking

**Purpose:** Learn the basics, test simple workflows

```bash
# Navigate to Bronze Tier
cd "D:\Hackathon 0\Bronze Tire"

# Start basic orchestrator
python orchestrator.py

# Create a task file
echo "Test task" > AI_Employee_Vault/Inbox/TASK_001.md
```

**When to use:**
- Testing basic file workflows
- Learning the system architecture
- Simple plan generation

---

### 🥈 Silver Tier - Communication Automation

**Purpose:** Automate email, LinkedIn, and WhatsApp with human approval

```bash
# Navigate to Silver Tier
cd "D:\Hackathon 0\Silver Tire"

# Start Silver orchestrator
python orchestrator.py

# Send email (create file in Approved/Email/)
# Post to LinkedIn (create file in Approved/LinkedIn/)
# Send WhatsApp (create file in Approved/WhatsApp/)
```

**When to use:**
- Sending emails automatically
- Posting to LinkedIn
- Sending WhatsApp messages (HITL)
- Running daily briefings

---

### 🥇 Gold Tier - Full Autonomous AI Employee

**Purpose:** Complete autonomous AI employee with cross-domain support

```bash
# Navigate to Gold Tier
cd "D:\Hackathon 0\Gold Tire"

# Start Ralph Wiggum autonomous loop
python ..\Ralph_Wiggum\orchestrator.py --domain Business

# Or process a specific task
python ..\Ralph_Wiggum\orchestrator.py Needs_Action\Business\TASK_NAME.md

# Start MCP servers
echo '{"action": "post_facebook", "message": "Hello!"}' | python ..\MCP\social\social_mcp.py

# Generate CEO briefing
echo '{"requested_by": "manual"}' | python ..\MCP\briefing\briefing_mcp.py
```

**When to use:**
- Full autonomous operation
- Cross-domain tasks (Personal/Business)
- Social media automation (FB/IG/Twitter)
- Weekly CEO briefings
- Error recovery and audit logging

---

## 🔄 Tier Migration Path

### Upgrading from Bronze → Silver

1. **Copy working directory structure:**
   ```bash
   xcopy "Bronze Tire\AI_Employee_Vault" "Silver Tire\AI_Employee_Vault" /E /I
   ```

2. **Add Silver MCP tools:**
   - Email MCP already in shared `/MCP/`
   - LinkedIn MCP already in shared `/MCP/`
   - WhatsApp MCP already in shared `/MCP/`

3. **Configure sessions:**
   - Login to LinkedIn: `python MCP\linkedin_post.py`
   - Login to WhatsApp: `python MCP\whatsapp_mcp.py`

4. **Start Silver orchestrator:**
   ```bash
   cd "Silver Tire"
   python orchestrator.py
   ```

---

### Upgrading from Silver → Gold

1. **Copy working directory structure:**
   ```bash
   xcopy "Silver Tire\AI_Employee_Vault" "Gold Tire\AI_Employee_Vault" /E /I
   ```

2. **Add Gold-specific folders:**
   ```bash
   mkdir "Gold Tire\AI_Employee_Vault\Needs_Action\Personal"
   mkdir "Gold Tire\AI_Employee_Vault\Needs_Action\Business"
   mkdir "Gold Tire\AI_Employee_Vault\Done\Personal"
   mkdir "Gold Tire\AI_Employee_Vault\Done\Business"
   mkdir "Gold Tire\AI_Employee_Vault\facebook_session"
   mkdir "Gold Tire\AI_Employee_Vault\twitter_session"
   ```

3. **Configure social sessions:**
   - Facebook: Run social MCP login
   - Twitter: Run social MCP login

4. **Start Ralph Wiggum loop:**
   ```bash
   cd "Gold Tire"
   python ..\Ralph_Wiggum\orchestrator.py --domain Business
   ```

---

## 📊 Feature Comparison Matrix

| Feature | Bronze | Silver | Gold |
|---------|--------|--------|------|
| **Filesystem Watcher** | ✅ | ✅ | ✅ |
| **Plan Generation** | ✅ | ✅ | ✅ |
| **Dashboard** | Basic | Enhanced | Comprehensive |
| **Email Sending** | ❌ | ✅ | ✅ |
| **LinkedIn Posting** | ❌ | ✅ | ✅ |
| **WhatsApp Messaging** | ❌ | ✅ | ✅ |
| **HITL Approval** | ❌ | ✅ | ✅ |
| **Gmail Watcher** | ❌ | ✅ | ✅ |
| **Cross-Domain Routing** | ❌ | ❌ | ✅ |
| **Facebook Posting** | ❌ | ❌ | ✅ |
| **Instagram Posting** | ❌ | ❌ | ✅ |
| **Twitter/X Posting** | ❌ | ❌ | ✅ |
| **Ralph Wiggum Loop** | ❌ | ❌ | ✅ |
| **Weekly CEO Briefing** | ❌ | ❌ | ✅ |
| **Error Recovery** | ❌ | ❌ | ✅ |
| **Audit Logging** | Basic | Enhanced | Comprehensive |
| **Session Management** | ❌ | LinkedIn/WhatsApp | All platforms |
| **Graceful Degradation** | ❌ | ❌ | ✅ |

---

## 🛠️ Shared Resources Usage

All tiers share common resources from the root `/MCP/`, `/agents/`, and `/Ralph_Wiggum/` directories:

### Using Shared MCP Tools

```bash
# All tiers can use shared MCP tools
python ..\MCP\email_mcp.py < input.json
python ..\MCP\linkedin_post.py < input.json
python ..\MCP\whatsapp_mcp.py < input.json

# Gold-only MCP tools
python ..\MCP\social\social_mcp.py < input.json
python ..\MCP\briefing\briefing_mcp.py < input.json
python ..\MCP\error_recovery\error_recovery_mcp.py < input.json
```

### Using Shared Agents

```python
# Import from shared agents
from agents.base_agent import BaseAgent
from agents.ceo_agent import CEOAgent
from agents.execution_agent import ExecutionAgent
```

---

## 🎯 Tier Selection Guide

### Choose Bronze Tier if:
- You're new to the system
- You need basic task tracking
- You want to test file workflows
- You don't need communication features

### Choose Silver Tier if:
- You need email automation
- You post to LinkedIn regularly
- You use WhatsApp for business
- You want HITL approval workflows

### Choose Gold Tier if:
- You want full autonomous operation
- You manage both personal and business tasks
- You need multi-platform social media posting
- You want automated CEO briefings
- You need robust error recovery

---

## 📈 Development Workflow

### Working on a Specific Tier

1. **Navigate to tier directory:**
   ```bash
   cd "Bronze Tire"   # or Silver Tire, Gold Tire
   ```

2. **Make changes to tier-specific files only**

3. **Test within tier sandbox**

4. **Commit changes with tier prefix:**
   ```bash
   git commit -m "[Bronze] Add basic orchestrator"
   git commit -m "[Silver] Add email MCP integration"
   git commit -m "[Gold] Add Ralph Wiggum loop"
   ```

### Updating Shared Resources

1. **Make changes in shared directories** (`/MCP/`, `/agents/`, etc.)

2. **Test across all tiers:**
   ```bash
   # Test in Bronze
   cd "Bronze Tire" && python test.py
   
   # Test in Silver
   cd "Silver Tire" && python test.py
   
   # Test in Gold
   cd "Gold Tire" && python test.py
   ```

3. **Document changes in all tier READMEs**

---

## 🔒 Data Isolation

Each tier maintains **complete data isolation**:

| Aspect | Isolation Method |
|--------|------------------|
| **Task Storage** | Separate `Needs_Action/`, `Done/` folders per tier |
| **Session Data** | Tier-specific session folders |
| **Logs** | Tier-specific log files |
| **Configuration** | Tier-specific config files |
| **Approvals** | Tier-specific approval queues |

**Shared data** (audit logs, agent definitions, MCP tools) is stored in root directories and accessed via relative paths.

---

## 📞 Support & Navigation

| Need | Go To |
|------|-------|
| Bronze documentation | `Bronze Tire/README.md` |
| Silver documentation | `Silver Tire/README.md` |
| Gold documentation | `Gold Tire/README.md` |
| System architecture | `ARCHITECTURE_GAP_ANALYSIS.md` |
| Agent implementation | `MULTI_AGENT_IMPLEMENTATION.md` |
| Full system summary | `COMPLETE_SYSTEM_SUMMARY.md` |
| Phase reports | `PHASE_*_COMPLETE.md` |
| Validation reports | `Gold_Final_Validation.md`, `Gold_Validation_Report.md` |

---

**Tier Architecture Status:** ✅ Complete and Production Ready

**Hackathon 0 Submission:** All tiers ready

---

*Built by Suleman AI Employee - Multi-Tier AI Workforce Platform*

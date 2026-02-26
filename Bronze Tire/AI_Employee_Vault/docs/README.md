# 🤖 AI Employee Vault

An organized file management system for seamless human + AI collaboration.

---

## 📁 Folder Structure

```
AI_Employee_Vault/
├── Inbox/              ← Drop files here for processing
├── Needs_Action/       ← Items requiring attention
├── Plans/              ← Strategic documents
│   ├── roadmaps/
│   ├── projects/
│   ├── features/
│   ├── research/
│   └── ideas/
├── Done/               ← Completed work
│   ├── 2026/
│   └── archive/
├── Logs/               ← Activity records
│   ├── activity/
│   ├── errors/
│   ├── runs/
│   └── audits/
├── scripts/            ← Automation code
├── Dashboard.md        ← Main status overview
└── Company_Handbook.md ← Rules & guidelines
```

---

## 🚀 Quick Start

### 1. Start the Inbox Watcher
```bash
python scripts/watcher_inbox-monitor_v1.0.py
```
This watches `Inbox/` and auto-moves files to `Needs_Action/` with priority tags.

### 2. Check Vault Health
```bash
python scripts/util_file-mover_v0.5.py --health
```

### 3. Generate Weekly Report
```bash
python scripts/report_weekly-summary_v2.1.py --save-default
```

---

## 📋 Core Workflow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Inbox/    │ ──▶ │ Needs_Action │ ──▶ │    Done/    │
│  (incoming) │     │  (processing)│     │ (completed) │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Logs/     │
                    │  (activity) │
                    └─────────────┘
```

### File Lifecycle
1. **Drop** files into `Inbox/`
2. **AI auto-processes** → moves to `Needs_Action/` with priority
3. **Human reviews** and completes work
4. **Move completed** to `Done/`
5. **All actions logged** to `Logs/`

---

## 🛠️ Available Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| **Inbox Monitor** | Auto-process incoming files | `python scripts/watcher_inbox-monitor_v1.0.py` |
| **File Mover** | Manual file operations | `python scripts/util_file-mover_v0.5.py --health` |
| **Weekly Report** | Generate summaries | `python scripts/report_weekly-summary_v2.1.py` |

### File Mover Commands
```bash
# Health check
python scripts/util_file-mover_v0.5.py --health

# List files in folder
python scripts/util_file-mover_v0.5.py --list Inbox

# Move all files
python scripts/util_file-mover_v0.5.py -s Inbox -d Needs_Action

# Move specific file
python scripts/util_file-mover_v0.5.py -s Inbox -d Needs_Action -f file.pdf
```

---

## 📊 Priority Levels

| Priority | Code | Response Time | Examples |
|----------|------|---------------|----------|
| 🔴 Urgent | P1 | < 1 hour | Production bugs, emergencies |
| 🟠 High | P2 | < 4 hours | Deadlines, blocked tasks |
| 🟡 Normal | P3 | < 24 hours | Standard requests |
| 🟢 Low | P4 | < 1 week | Nice-to-haves |

---

## 📖 Documentation

| File | Description |
|------|-------------|
| [`Dashboard.md`](./Dashboard.md) | Main status overview |
| [`Company_Handbook.md`](./Company_Handbook.md) | Rules & AI guidelines |
| [`scripts/NAMING_CONVENTIONS.md`](./scripts/NAMING_CONVENTIONS.md) | File naming standards |
| [`scripts/SUBFOLDERS_GUIDE.md`](./scripts/SUBFOLDERS_GUIDE.md) | Folder structure details |
| [`scripts/DAILY_WORKFLOW.md`](./scripts/DAILY_WORKFLOW.md) | Daily usage guide |

---

## 🎯 Daily Routine

### Morning (15 min)
- [ ] Open `Dashboard.md`
- [ ] Process `Inbox/` to zero
- [ ] Set top 3 priorities

### End of Day (10 min)
- [ ] Move completed items to `Done/`
- [ ] Review `Logs/activity/`
- [ ] Plan tomorrow's focus

---

## 📦 Requirements

- Python 3.8+
- No external dependencies (uses only standard library)

---

## 📝 License

MIT License - Use freely in your projects.

---

*Created: 2026-02-22 | Version: 1.0*

# 📅 Daily Workflow Guide

Human + AI collaboration patterns for maximum productivity.

---

## 🌅 Morning Routine (15 minutes)

### 1. Open Dashboard (2 min)
```
1. Open AI_Employee_Vault/Dashboard.md
2. Check overnight activity
3. Note any P1/priority items
```

### 2. Process Inbox (5 min)
```
1. Review files in Inbox/
2. Let watcher script auto-classify (or run manually)
3. Confirm AI decisions for edge cases
```

**Quick Command:**
```bash
python scripts/watcher_inbox-monitor_v1.0.py
# Let run for 10 seconds, then Ctrl+C for one-time processing
```

### 3. Set Priorities (5 min)
```
1. Review Needs_Action/ folder
2. Identify top 3 priorities for today
3. Update Dashboard.md "Today's Focus" section
```

### 4. Start Automation (3 min)
```bash
# Start background watcher (optional)
python scripts/watcher_inbox-monitor_v1.0.py
# Runs continuously, watching for new files
```

---

## ☀️ During the Day

### When New Files Arrive
```
1. Drop file into Inbox/
2. Watcher auto-processes within 5 seconds
3. File appears in Needs_Action/ with priority tag
4. AI logs action to Logs/activity/
```

### Between Meetings (5 min check-ins)
```
1. Open Needs_Action/ folder
2. Sort by priority (P1 → P4)
3. Complete 1-2 quick items
4. Move completed to Done/2026/Q{N}/
```

### Quick File Operations
```bash
# List inbox contents
python scripts/util_file-mover_v0.5.py --list Inbox

# Move specific file manually
python scripts/util_file-mover_v0.5.py -s Inbox -d Needs_Action -f report.pdf

# Check system health
python scripts/util_file-mover_v0.5.py --health
```

---

## 🌆 End of Day (10 minutes)

### 1. Inbox Zero Check (3 min)
```
□ Inbox/ should have 0 files
□ If not: process or schedule for tomorrow
□ Run: python scripts/util_file-mover_v0.5.py --health
```

### 2. Update Completed Work (3 min)
```
□ Move finished items to Done/2026/Q{N}/
□ Update Dashboard.md stats
□ Log any notes in Dashboard.md "Notes" section
```

### 3. Review Tomorrow (2 min)
```
□ Check Needs_Action/ for urgent items
□ Set 1-2 priority tasks for morning
□ Close watcher script if running
```

### 4. Quick Log Review (2 min)
```
□ Skim Logs/activity/activity_YYYY-MM-DD.log
□ Note any errors or patterns
□ Address any ❌ failed operations
```

---

## 📊 Weekly Rhythm

| Day | Focus | Time |
|-----|-------|------|
| **Monday** | Plan week, review backlog | 20 min |
| **Tuesday** | Deep work, minimize admin | 5 min |
| **Wednesday** | Mid-week check-in | 10 min |
| **Thursday** | Push pending items | 5 min |
| **Friday** | Weekly report, cleanup | 20 min |

### Friday Weekly Report
```bash
# Generate weekly summary
python scripts/report_weekly-summary_v2.1.py --save-default

# Review report
open Logs/weekly-report-2026-W08.md
```

---

## 🤖 AI Agent Roles

### Inbox Monitor (watcher_inbox-monitor_v1.0.py)
**When:** Runs continuously or on-demand  
**Does:**
- Watches Inbox/ for new files
- Detects priority from filename
- Moves to Needs_Action/ with standardized name
- Logs all actions

**Human Override:**
- Review P1 items immediately
- Spot-check 10% of auto-classified files

### File Mover (util_file-mover_v0.5.py)
**When:** Manual execution  
**Does:**
- Lists files in any folder
- Moves files between folders
- Shows vault health status
- Displays folder tree

**Common Commands:**
```bash
# Health check
python scripts/util_file-mover_v0.5.py --health

# List pending items
python scripts/util_file-mover_v0.5.py --list Needs_Action

# Bulk move
python scripts/util_file-mover_v0.5.py -s Inbox -d Needs_Action
```

### Report Generator (report_weekly-summary_v2.1.py)
**When:** Weekly (Friday) or on-demand  
**Does:**
- Counts processed files
- Tracks errors and actions
- Breaks down by priority/category
- Generates recommendations

---

## 🎯 Decision Matrix

| Situation | AI Action | Human Action |
|-----------|-----------|--------------|
| New file in Inbox | Auto-classify, move to Needs_Action | Review P1 items |
| Confidence > 90% | Process automatically | Spot-check 10% |
| Confidence 50-90% | Flag for review | Make decision |
| Confidence < 50% | Log error, skip | Handle manually |
| P1 detected | Move + alert | Immediate review |
| Repeated errors | Log + skip | Investigate pattern |

---

## ⚡ Quick Reference Commands

```bash
# Start inbox watcher
python scripts/watcher_inbox-monitor_v1.0.py

# Check vault health
python scripts/util_file-mover_v0.5.py --health

# List files in folder
python scripts/util_file-mover_v0.5.py --list Inbox
python scripts/util_file-mover_v0.5.py --list Needs_Action

# Move files
python scripts/util_file-mover_v0.5.py -s Inbox -d Needs_Action
python scripts/util_file-mover_v0.5.py -s Inbox -d Needs_Action -f specific.pdf

# Generate weekly report
python scripts/report_weekly-summary_v2.1.py
python scripts/report_weekly-summary_v2.1.py --week 2026-W08
python scripts/report_weekly-summary_v2.1.py --save-default
```

---

## 📋 Checklist Templates

### Daily Checklist
```
□ Morning: Review Dashboard.md
□ Morning: Process Inbox to zero
□ Morning: Set top 3 priorities
□ Midday: Check Needs_Action (P1/P2)
□ Evening: Move completed to Done/
□ Evening: Log notes/observations
□ Evening: Plan tomorrow's focus
```

### Weekly Checklist
```
□ Monday: Review weekly goals
□ Wednesday: Mid-week progress check
□ Friday: Run weekly report
□ Friday: Review completed work
□ Friday: Clean up old logs
□ Friday: Plan next week
```

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| Inbox not processing | Check watcher script is running |
| Files not moving | Verify folder permissions |
| Duplicate filenames | Script auto-adds _1, _2, etc. |
| Logs not writing | Check Logs/ directory exists |
| High error rate | Review classification rules |

---

*Workflow version: 1.0 | Last updated: 2026-02-22*

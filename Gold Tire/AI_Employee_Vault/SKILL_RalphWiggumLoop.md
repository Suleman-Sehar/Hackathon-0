# SKILL: Ralph Wiggum Autonomous Loop

**Version:** 0.3 Gold Tier - Phase 5
**Owner:** Suleman AI Employee v0.3

---

## Objective

Enable true multi-step autonomous execution for tasks that require more than 3 steps.

---

## Error Handling & Logging

**Wrap all actions with error_recovery_mcp.py:**

```bash
# On loop error
echo '{"action_type": "retry_with_backoff", "params": {"task": "example"}, "max_retries": 3}' | python MCP/error_recovery/error_recovery_mcp.py
```

**Log every step to audit JSON:**
- Every iteration logged to `/Logs/audit_YYYY-MM-DD.json`
- Format: `{"timestamp": "...", "action": "ralph_wiggum_iteration", "status": "success/failed", "domain": "Business", "details": {"iteration": 5}}`

**On critical fail:** Create `ERROR_ALERT` file in `Pending_Approval/`

---

## How to Trigger

**Via Command Line:**
```bash
python Ralph_Wiggum/orchestrator.py /Needs_Action/Business/TASK_NAME.md
```

**Via Orchestrator:**
- Task file placed in `/Needs_Action/{domain}/`
- Ralph Wiggum loop automatically invoked for multi-step tasks

**Scheduled Tasks:**
- **Weekly CEO Briefing** – Recurring autonomous task every Sunday 11 PM
- Trigger via orchestrator as recurring task

---

## Completion Conditions

Task is considered complete when:
1. **File moved to Done:** Task file moved from `/Needs_Action/{domain}/` to `/Done/{domain}/`
2. **Marker present:** Output contains `TASK_COMPLETE` string

---

## Max Iterations

| Setting | Value |
|---------|-------|
| Maximum iterations | 15 |
| Retry delay | 60 seconds |
| API timeout | 120 seconds |

---

## Recurring Autonomous Tasks

### Weekly CEO Briefing

**Weekly briefing is a recurring autonomous task – trigger via orchestrator every Sunday:**

```bash
# Create recurring task file
echo "---
task: Weekly CEO Briefing
description: Generate weekly briefing from accounting data, completed tasks, and social reports
domain: Business
schedule: weekly_sunday_11pm
---" > Needs_Action/Business/WEEKLY_CEO_BRIEFING.md

# Run via orchestrator
python Ralph_Wiggum/orchestrator.py Needs_Action/Business/WEEKLY_CEO_BRIEFING.md
```

**Output:** `/Briefings/CEO_Briefing_YYYY-MM-DD.md`

---

## Safety Features

### HITL for Sensitive Steps

For sensitive actions, the loop creates HITL requests:

```markdown
---
type: approval_request
action: [action_name]
created: [timestamp]
status: pending
---

## Step Details
[Description of step requiring approval]

---
Move to Approved/ to continue, Rejected/ to skip
```

### Error Handling

| Error Type | Recovery |
|------------|----------|
| API timeout | Retry with exponential backoff |
| Qwen error | Call error_recovery_mcp.py |
| Max iterations | Graceful stop, log incomplete |
| File system error | Alert human, save state |

---

## Loop Logic

```
┌─────────────────────────────────────────────────────────────┐
│                    Ralph Wiggum Loop                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Read task from /Needs_Action/{domain}/                  │
│         ↓                                                    │
│  2. Build initial prompt                                    │
│         ↓                                                    │
│  3. Call Qwen API (simulated via file IPC)                  │
│         ↓                                                    │
│  4. Check completion:                                       │
│     - File in /Done/? → Complete                            │
│     - TASK_COMPLETE in output? → Complete                   │
│         ↓                                                    │
│  5a. Complete → Move file, log, exit                        │
│  5b. Incomplete → Re-inject prompt + previous output        │
│         ↓                                                    │
│  6. Repeat (max 15 iterations)                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## State Persistence

**State File:** `/Ralph_Wiggum/state/state_{task_name}.json`

```json
{
    "task_name": "example_task",
    "task_file": "/Needs_Action/Business/example_task.md",
    "domain": "Business",
    "iteration": 5,
    "status": "running",
    "start_time": "2026-03-04T12:00:00",
    "last_output": "...",
    "history": [...]
}
```

**Crash Recovery:** If loop crashes, resume from last saved state.

---

## Logging

### Audit Log

Every action logged to `/Logs/audit_YYYY-MM-DD.json`:

```json
{
    "timestamp": "2026-03-04T12:00:00",
    "action": "ralph_wiggum_loop_start",
    "status": "info",
    "domain": "Business",
    "details": {
        "task": "example_task",
        "max_iterations": 15
    },
    "error": null
}
```

### Loop Log

Per-task loop log: `/Ralph_Wiggum/logs/loop_{task}_{timestamp}.json`

Contains:
- Each iteration's output
- Errors encountered
- Completion status

---

## Example Task Format

```markdown
---
task: Autonomous demo
description: Generate LinkedIn post, post on Twitter and Instagram, generate summaries, update Dashboard
domain: Business
---

Start Ralph Wiggum loop on this task.
```

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `SKILL_CrossDomainRouter.md` | Routes multi-step tasks to Ralph Wiggum |
| `SKILL_ErrorRecovery.md` | Handles errors during loop execution |
| `SKILL_FacebookInstagramPost.md` | Can be called by loop for posting |
| `SKILL_TwitterPost.md` | Can be called by loop for posting |

---

## Usage Examples

### Example 1: Simple Multi-Step Task

```bash
# Create task file
echo "---
task: Social media blast
description: Post announcement on Facebook, Instagram, and Twitter
domain: Business
---" > Needs_Action/Business/social_blast.md

# Run loop
python Ralph_Wiggum/orchestrator.py Needs_Action/Business/social_blast.md
```

### Example 2: Complex Business Task

```bash
# Task with multiple steps
python Ralph_Wiggum/orchestrator.py Needs_Action/Business/weekly_report.md

# Expected iterations: 5-8
# Steps: Gather data → Generate report → Create charts → Send email → Update dashboard
```

---

## Monitoring

### Check Loop Status

```bash
# View current state
type Ralph_Wiggum\state\state_{task_name}.json

# View loop logs
type Ralph_Wiggum\logs\loop_{task}_*.json
```

### View Audit Trail

```bash
# Today's audit log
type Logs\audit_2026-03-04.json

# Filter for Ralph Wiggum events
python -c "import json; logs=json.load(open('Logs/audit_2026-03-04.json')); print([l for l in logs if 'ralph' in l['action']])"
```

---

## Best Practices

1. **Clear task descriptions** - Define what "done" looks like
2. **Break into steps** - Complex tasks need clear step boundaries
3. **Use completion marker** - Always include TASK_COMPLETE when done
4. **HITL for sensitive** - Create approval requests for sensitive actions
5. **Monitor iterations** - If approaching 15, task may need refinement

---

## Related Skills

- `SKILL_CrossDomainRouter.md` – Domain routing
- `SKILL_ErrorRecovery.md` – Error handling
- `SKILL_WeeklyCEOBriefing.md` – CEO reporting

---

**Status:** ✅ Active  
**Last Updated:** 2026-03-04
